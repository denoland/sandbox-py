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
async def test_rpc_missing_method(async_shared_sandbox) -> None:
    with pytest.raises(UnknownRpcMethod):
        await async_shared_sandbox._rpc.call("non_existent_method", {})


@pytest.mark.asyncio(loop_scope="session")
async def test_rpc_wrong_params(async_shared_sandbox) -> None:
    with pytest.raises(RpcValidationError):
        await async_shared_sandbox._rpc.call("readTextFile", {})
