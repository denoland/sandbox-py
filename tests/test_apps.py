import pytest
import uuid

from deno_sandbox import AsyncDenoDeploy, Config, DenoDeploy, EnvVarInput


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
async def test_apps_create_with_env_vars_async():
    sdk = AsyncDenoDeploy()

    slug = gen_app_name()
    env_vars: list[EnvVarInput] = [{"key": "MY_VAR", "value": "hello"}]
    app = await sdk.apps.create(slug=slug, env_vars=env_vars)

    assert app["slug"] == slug
    assert app.get("env_vars") is not None
    assert any(v["key"] == "MY_VAR" for v in app["env_vars"])

    await sdk.apps.delete(app["id"])


def test_apps_create_with_env_vars_sync():
    sdk = DenoDeploy()

    slug = gen_app_name()
    env_vars: list[EnvVarInput] = [{"key": "MY_VAR", "value": "hello"}]
    app = sdk.apps.create(slug=slug, env_vars=env_vars)

    assert app["slug"] == slug
    assert app.get("env_vars") is not None
    assert any(v["key"] == "MY_VAR" for v in app["env_vars"])

    sdk.apps.delete(app["id"])


@pytest.mark.asyncio(loop_scope="session")
async def test_apps_create_with_config_async():
    sdk = AsyncDenoDeploy()

    slug = gen_app_name()
    config: Config = {"runtime": {"type": "dynamic", "entrypoint": "main.ts"}}
    app = await sdk.apps.create(slug=slug, config=config)

    assert app["slug"] == slug
    assert app.get("config") is not None

    await sdk.apps.delete(app["id"])


def test_apps_create_with_config_sync():
    sdk = DenoDeploy()

    slug = gen_app_name()
    config: Config = {"runtime": {"type": "dynamic", "entrypoint": "main.ts"}}
    app = sdk.apps.create(slug=slug, config=config)

    assert app["slug"] == slug
    assert app.get("config") is not None

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
async def test_apps_update_env_vars_async():
    sdk = AsyncDenoDeploy()

    app = await sdk.apps.create(env_vars=[{"key": "FOO", "value": "bar"}])
    try:
        updated = await sdk.apps.update(
            app["id"],
            env_vars=[{"key": "BAZ", "value": "qux"}],
        )

        assert updated["id"] == app["id"]
        assert updated.get("env_vars") is not None
        keys = [v["key"] for v in updated["env_vars"]]
        assert "BAZ" in keys
    finally:
        await sdk.apps.delete(app["id"])


def test_apps_update_env_vars_sync():
    sdk = DenoDeploy()

    app = sdk.apps.create(env_vars=[{"key": "FOO", "value": "bar"}])
    try:
        updated = sdk.apps.update(
            app["id"],
            env_vars=[{"key": "BAZ", "value": "qux"}],
        )

        assert updated["id"] == app["id"]
        assert updated.get("env_vars") is not None
        keys = [v["key"] for v in updated["env_vars"]]
        assert "BAZ" in keys
    finally:
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
    try:
        apps = await sdk.apps.list()

        assert type(apps.has_more) is bool
        assert apps.next_cursor is None or type(apps.next_cursor) is str
        assert any(a["id"] == app["id"] for a in apps.items)
    finally:
        await sdk.apps.delete(app["id"])


def test_apps_list_sync():
    sdk = DenoDeploy()

    app = sdk.apps.create()
    try:
        apps = sdk.apps.list()

        assert type(apps.has_more) is bool
        assert apps.next_cursor is None or type(apps.next_cursor) is str
        assert any(a["id"] == app["id"] for a in apps.items)
    finally:
        sdk.apps.delete(app["id"])
