import pytest


@pytest.mark.asyncio(loop_scope="session")
async def test_repl_eval_async(async_shared_sandbox):
    sb = async_shared_sandbox

    result = await sb.deno.eval("1 + 2")
    assert result == 3


def test_repl_eval_sync(shared_sandbox):
    sb = shared_sandbox

    result = sb.deno.eval("1 + 2")
    assert result == 3


@pytest.mark.asyncio(loop_scope="session")
async def test_repl_call_async(async_shared_sandbox):
    sb = async_shared_sandbox

    async with await sb.deno.repl() as repl:
        # TODO: API bug, expects JSON return values
        await repl.eval("const add = (a, b) => a + b; 1")

        result = await repl.call("add", [1, 2])
        assert result == 3


def test_repl_call_sync(shared_sandbox):
    sb = shared_sandbox

    with sb.deno.repl() as repl:
        # TODO: API bug, expects JSON return values
        repl.eval("const add = (a, b) => a + b; 1")

        result = repl.call("add", [1, 2])
        assert result == 3


@pytest.mark.asyncio(loop_scope="session")
async def test_deno_run_async(async_shared_sandbox):
    sb = async_shared_sandbox

    async with await sb.deno.run(
        code="console.log(42)",
        stdout="piped",
        stderr="piped",
    ) as cp:
        raw = await cp.stdout.read(-1)
        assert "42" in raw.decode()


def test_deno_run_sync(shared_sandbox):
    sb = shared_sandbox

    with sb.deno.run(
        code="console.log(42)",
        stdout="piped",
        stderr="piped",
    ) as cp:
        raw = cp.stdout.read(-1)
        assert "42" in raw.decode()


@pytest.mark.asyncio(loop_scope="session")
async def test_deno_run_http_ready_async(async_shared_sandbox):
    sb = async_shared_sandbox

    async with await sb.deno.run(
        code="Deno.serve(req => new Response('ok'))",
    ) as cp:
        ready = await cp.wait_http_ready()
        assert ready is True

        res = await cp.fetch(url="https://example.com", method="GET")

        assert res.status_code == 200

        headers = dict(res.headers)
        assert headers["content-type"] == "text/plain;charset=UTF-8"


def test_deno_run_http_ready_sync(shared_sandbox):
    sb = shared_sandbox

    with sb.deno.run(
        code="Deno.serve(req => new Response('ok'))",
    ) as cp:
        ready = cp.wait_http_ready()
        assert ready is True

        res = cp.fetch(url="https://example.com", method="GET")

        assert res.status_code == 200

        headers = dict(res.headers)
        assert headers["content-type"] == "text/plain;charset=UTF-8"
