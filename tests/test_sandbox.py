from datetime import datetime, timezone
import httpx
import pytest
import uuid

from deno_sandbox import AsyncDenoDeploy, DenoDeploy
from deno_sandbox.errors import RpcValidationError, UnknownRpcMethod


def gen_app_name() -> str:
    return f"test-deploy-{uuid.uuid4().hex[:8]}"


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
        args=["cowsay", "foo"],
        stdout="piped",
        stderr="piped",
    )

    status = await p.wait()
    assert status["code"] == 0

    stdout = await p.stdout.read(-1)
    stderr = await p.stderr.read(-1)
    assert "foo" in stdout.decode()
    assert "will be installed" in stderr.decode()


async def test_spawn_sync(shared_sandbox) -> None:
    sb = shared_sandbox

    p = sb.spawn(
        "npx",
        args=["cowsay", "foo"],
        stdout="piped",
        stderr="piped",
    )

    status = p.wait()
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
        code="Deno.serve({port: 4000}, req => new Response('ok'))",
    ) as cp:
        await cp.wait_http_ready()

        address = await sb.expose_http(port=4000)
        response = httpx.get(address)

        assert response.status_code == 200
        assert response.text == "ok"


def test_expose_http_sync(shared_sandbox):
    sb = shared_sandbox

    with sb.deno.run(
        code="Deno.serve({port: 4000}, req => new Response('ok'))",
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


@pytest.mark.asyncio(loop_scope="session")
async def test_deno_deploy_async():
    sdk = AsyncDenoDeploy()

    # Create a test app
    app_slug = gen_app_name()
    app = await sdk.apps.create(slug=app_slug)

    try:
        # Create sandbox and deploy
        async with sdk.sandbox.create() as sandbox:
            # Write a simple Deno server file
            await sandbox.fs.write_text_file(
                "main.ts",
                'Deno.serve(() => new Response("Hello from test!"))',
            )

            # Deploy to the app
            build = await sandbox.deno.deploy(
                app["slug"],
                entrypoint="main.ts",
                production=False,
            )

            # Verify build object
            assert build is not None
            assert build.id is not None
            assert isinstance(build.id, str)

            # Test logs streaming
            log_count = 0
            async for log in build.logs():
                assert "timestamp" in log
                assert "level" in log
                assert "message" in log
                assert log["level"] in ["info", "error"]
                log_count += 1
                # Only check first few logs to avoid long wait
                if log_count >= 5:
                    break

            # Test wait method
            revision = await build.wait()
            assert revision is not None
            assert revision["id"] == build.id
            assert revision["status"] in ["building", "ready", "error", "routed"]
            assert "created_at" in revision
            assert "updated_at" in revision

    finally:
        # Clean up the app
        await sdk.apps.delete(app["id"])


def test_deno_deploy_sync():
    sdk = DenoDeploy()

    # Create a test app
    app_slug = gen_app_name()
    app = sdk.apps.create(slug=app_slug)

    try:
        # Create sandbox and deploy
        with sdk.sandbox.create() as sandbox:
            # Write a simple Deno server file
            sandbox.fs.write_text_file(
                "main.ts",
                'Deno.serve(() => new Response("Hello from test!"))',
            )

            # Deploy to the app
            build = sandbox.deno.deploy(
                app["slug"],
                entrypoint="main.ts",
                production=False,
            )

            # Verify build object
            assert build is not None
            assert build.id is not None
            assert isinstance(build.id, str)

            # Test logs
            logs = build.logs()
            assert logs is not None
            assert isinstance(logs, list)
            # At least one log should be present
            if len(logs) > 0:
                log = logs[0]
                assert "timestamp" in log
                assert "level" in log
                assert "message" in log
                assert log["level"] in ["info", "error"]

            # Test wait method
            revision = build.wait()
            assert revision is not None
            assert revision["id"] == build.id
            assert revision["status"] in ["building", "ready", "error", "routed"]
            assert "created_at" in revision
            assert "updated_at" in revision

    finally:
        # Clean up the app
        sdk.apps.delete(app["id"])
