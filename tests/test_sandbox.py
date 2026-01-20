from datetime import datetime, timezone
import httpx
import pytest

from deno_sandbox import AsyncDenoDeploy, DenoDeploy
from deno_sandbox.errors import RpcValidationError, UnknownRpcMethod


@pytest.mark.asyncio(loop_scope="session")
async def test_create_async():
    sdk = AsyncDenoDeploy()

    async with sdk.sandbox.create() as sandbox:
        assert sandbox is not None
        assert sandbox.id is not None


async def test_create_sync():
    sdk = DenoDeploy()

    with sdk.sandbox.create() as sandbox:
        assert sandbox is not None
        assert sandbox.id is not None


@pytest.mark.asyncio(loop_scope="session")
async def test_connect_async():
    sdk = AsyncDenoDeploy()

    async with sdk.sandbox.create() as sandbox:
        async with sdk.sandbox.connect(sandbox.id) as connected_sandbox:
            assert connected_sandbox is not None
            assert connected_sandbox.id == sandbox.id

            await connected_sandbox.fs.write_text_file("foo.txt", "foo")

        content = await sandbox.fs.read_text_file("foo.txt")
        assert content == "foo"


def test_connect_sync():
    sdk = DenoDeploy()

    with sdk.sandbox.create() as sandbox:
        with sdk.sandbox.connect(sandbox.id) as connected_sandbox:
            assert connected_sandbox is not None
            assert connected_sandbox.id == sandbox.id

            connected_sandbox.fs.write_text_file("foo.txt", "foo")

        content = sandbox.fs.read_text_file("foo.txt")
        assert content == "foo"


@pytest.mark.asyncio(loop_scope="session")
async def test_write_read_text_file_async(async_shared_sandbox):
    sb = async_shared_sandbox
    path = "foo.txt"
    await sb.fs.write_text_file(path, "foo")
    content = await sb.fs.read_text_file(path)
    assert content == "foo"


def test_write_read_text_file_sync(shared_sandbox) -> None:
    sb = shared_sandbox

    sb.fs.write_text_file("foo.txt", "foo")
    content = sb.fs.read_text_file("foo.txt")
    assert content == "foo"


@pytest.mark.asyncio(loop_scope="session")
async def test_spawn_async(async_shared_sandbox) -> None:
    sb = async_shared_sandbox

    p = await sb.spawn(
        "npx",
        {
            "args": ["cowsay", "foo"],
            "stdout": "piped",
            "stderr": "piped",
        },
    )

    status = await p.status
    assert status["code"] == 0

    stdout = await p.stdout.read(-1)
    stderr = await p.stderr.read(-1)
    assert "foo" in stdout.decode()
    assert "will be installed" in stderr.decode()


async def test_spawn_sync(shared_sandbox) -> None:
    sb = shared_sandbox

    p = sb.spawn(
        "npx",
        {
            "args": ["cowsay", "foo"],
            "stdout": "piped",
            "stderr": "piped",
        },
    )

    status = p.status
    assert status["code"] == 0

    stdout = p.stdout.read(-1)
    stderr = p.stderr.read(-1)
    assert "foo" in stdout.decode()
    assert "will be installed" in stderr.decode()


@pytest.mark.asyncio(loop_scope="session")
async def test_extend_timeout_async(async_shared_sandbox):
    sb = async_shared_sandbox

    now = datetime.now(timezone.utc)
    res = await sb.extend_timeout(10)
    assert now < res


def test_extend_timeout_sync(shared_sandbox):
    sb = shared_sandbox

    now = datetime.now(timezone.utc)
    res = sb.extend_timeout(10)
    assert now < res


@pytest.mark.asyncio(loop_scope="session")
async def test_fetch_async(async_shared_sandbox):
    sb = async_shared_sandbox

    res = await sb.fetch(url="https://example.com", method="GET")
    assert res.status_code == 200

    headers = dict(res.headers)
    assert headers["content-type"] == "text/html"


def test_fetch_sync(shared_sandbox):
    sb = shared_sandbox

    res = sb.fetch(url="https://example.com", method="GET")
    assert res.status_code == 200

    headers = dict(res.headers)
    assert headers["content-type"] == "text/html"


@pytest.mark.asyncio(loop_scope="session")
async def test_expose_http_async(async_shared_sandbox):
    sb = async_shared_sandbox

    async with await sb.deno.run(
        {
            "code": "Deno.serve({port: 4000}, req => new Response('ok'))",
        }
    ) as cp:
        await cp.wait_http_ready()

        address = await sb.expose_http(port=4000)
        response = httpx.get(address)

        assert response.status_code == 200
        assert response.text == "ok"


def test_expose_http_sync(shared_sandbox):
    sb = shared_sandbox

    with sb.deno.run(
        {
            "code": "Deno.serve({port: 4000}, req => new Response('ok'))",
        }
    ) as cp:
        cp.wait_http_ready()

        address = sb.expose_http(port=4000)
        response = httpx.get(address)

        assert response.status_code == 200
        assert response.text == "ok"


@pytest.mark.asyncio(loop_scope="session")
async def test_expose_ssh_async(async_shared_sandbox):
    sb = async_shared_sandbox

    res = await sb.expose_ssh()

    assert type(res["hostname"]) is str
    assert type(res["username"]) is str
    assert type(res["port"]) is int


def test_expose_ssh_sync(shared_sandbox):
    sb = shared_sandbox

    res = sb.expose_ssh()

    assert type(res["hostname"]) is str
    assert type(res["username"]) is str
    assert type(res["port"]) is int


@pytest.mark.asyncio(loop_scope="session")
async def test_rpc_missing_method(async_shared_sandbox) -> None:
    with pytest.raises(UnknownRpcMethod):
        await async_shared_sandbox._rpc.call("non_existent_method", {})


@pytest.mark.asyncio(loop_scope="session")
async def test_rpc_wrong_params(async_shared_sandbox) -> None:
    with pytest.raises(RpcValidationError):
        await async_shared_sandbox._rpc.call("readTextFile", {})
