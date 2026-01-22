import pytest
import uuid

from deno_sandbox import AsyncDenoDeploy, DenoDeploy


def gen_app_name() -> str:
    return f"test-app-{uuid.uuid4().hex[:8]}"


@pytest.mark.asyncio(loop_scope="session")
async def test_apps_create_async():
    sdk = AsyncDenoDeploy()

    app = await sdk.apps.create()
    assert app["id"] is not None

    await sdk.apps.delete(app["id"])


def test_apps_create_sync():
    sdk = DenoDeploy()

    app = sdk.apps.create()
    assert app["id"] is not None

    sdk.apps.delete(app["id"])


@pytest.mark.asyncio(loop_scope="session")
async def test_apps_create_options_async():
    sdk = AsyncDenoDeploy()

    slug = gen_app_name()
    app = await sdk.apps.create(slug=slug)

    assert app["slug"] == slug
    await sdk.apps.delete(app["id"])


def test_apps_create_options_sync():
    sdk = DenoDeploy()

    slug = gen_app_name()
    app = sdk.apps.create(slug=slug)

    assert app["slug"] == slug
    sdk.apps.delete(app["id"])


@pytest.mark.asyncio(loop_scope="session")
async def test_apps_update_async():
    sdk = AsyncDenoDeploy()

    app = await sdk.apps.create()

    slug = gen_app_name()
    updated = await sdk.apps.update(app["id"], slug=slug)

    assert updated["slug"] == slug
    assert updated["id"] == app["id"]
    assert updated["updated_at"] != app["updated_at"]
    assert updated["created_at"] == app["created_at"]

    await sdk.apps.delete(app["id"])


@pytest.mark.asyncio(loop_scope="session")
async def test_apps_update_sync():
    sdk = DenoDeploy()

    app = sdk.apps.create()

    slug = gen_app_name()
    updated = sdk.apps.update(app["id"], slug=slug)

    assert updated["slug"] == slug
    assert updated["id"] == app["id"]
    assert updated["updated_at"] != app["updated_at"]
    assert updated["created_at"] == app["created_at"]

    sdk.apps.delete(app["id"])


@pytest.mark.asyncio(loop_scope="session")
async def test_apps_delete_async():
    sdk = AsyncDenoDeploy()

    app = await sdk.apps.create()
    id = app["id"]
    await sdk.apps.delete(id)

    result = await sdk.apps.get(id)
    assert result is None


def test_apps_delete_sync():
    sdk = DenoDeploy()

    app = sdk.apps.create()
    id = app["id"]
    sdk.apps.delete(id)

    result = sdk.apps.get(id)
    assert result is None


@pytest.mark.asyncio(loop_scope="session")
async def test_apps_list_async():
    sdk = AsyncDenoDeploy()

    app = await sdk.apps.create()
    apps = await sdk.apps.list()

    assert type(apps.has_more) is bool
    assert apps.next_cursor is None or type(apps.next_cursor) is str
    assert any(a["id"] == app["id"] for a in apps.items)


def test_apps_list_sync():
    sdk = DenoDeploy()

    app = sdk.apps.create()
    apps = sdk.apps.list()

    assert type(apps.has_more) is bool
    assert apps.next_cursor is None or type(apps.next_cursor) is str
    assert any(a["id"] == app["id"] for a in apps.items)
