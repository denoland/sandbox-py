import pytest


@pytest.mark.asyncio
async def test_create_async(async_shared_sandbox):
    sb = async_shared_sandbox

    result = await sb.deno.eval("1 + 2")
    assert result == 3


def test_create_sync(shared_sandbox):
    sb = shared_sandbox

    result = sb.deno.eval("1 + 2")
    assert result == 3
