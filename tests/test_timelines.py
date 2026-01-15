import pytest

from deno_sandbox import AsyncDenoDeploy, DenoDeploy


@pytest.mark.asyncio(loop_scope="session")
async def test_timeline_list_async():
    sdk = AsyncDenoDeploy()

    app = await sdk.apps.create()
    timelines = await sdk.timelines.list(app=app["id"])

    print(timelines.items)

    assert type(timelines.has_more) is bool
    assert timelines.next_cursor is None or type(timelines.next_cursor) is str
    assert isinstance(timelines.items, list)


async def test_timeline_list_sync():
    sdk = DenoDeploy()

    app = sdk.apps.create()
    timelines = sdk.timelines.list(app=app["id"])

    assert type(timelines.has_more) is bool
    assert timelines.next_cursor is None or type(timelines.next_cursor) is str
    assert isinstance(timelines.items, list)
