import pytest
import uuid

from deno_sandbox import AsyncDenoDeploy, DenoDeploy, EnvVarInput


def gen_layer_slug() -> str:
    return f"test-layer-{uuid.uuid4().hex[:8]}"


@pytest.mark.asyncio(loop_scope="session")
async def test_layers_create_async():
    sdk = AsyncDenoDeploy()

    slug = gen_layer_slug()
    layer = await sdk.layers.create(slug)
    try:
        assert layer["id"] is not None
        assert layer["slug"] == slug
    finally:
        await sdk.layers.delete(layer["id"])


def test_layers_create_sync():
    sdk = DenoDeploy()

    slug = gen_layer_slug()
    layer = sdk.layers.create(slug)
    try:
        assert layer["id"] is not None
        assert layer["slug"] == slug
    finally:
        sdk.layers.delete(layer["id"])


@pytest.mark.asyncio(loop_scope="session")
async def test_layers_create_with_env_vars_async():
    sdk = AsyncDenoDeploy()

    slug = gen_layer_slug()
    env_vars: list[EnvVarInput] = [{"key": "MY_VAR", "value": "hello"}]
    layer = await sdk.layers.create(slug, env_vars=env_vars)
    try:
        assert layer["slug"] == slug
        assert any(v["key"] == "MY_VAR" for v in layer["env_vars"])
    finally:
        await sdk.layers.delete(layer["id"])


def test_layers_create_with_env_vars_sync():
    sdk = DenoDeploy()

    slug = gen_layer_slug()
    env_vars: list[EnvVarInput] = [{"key": "MY_VAR", "value": "hello"}]
    layer = sdk.layers.create(slug, env_vars=env_vars)
    try:
        assert layer["slug"] == slug
        assert any(v["key"] == "MY_VAR" for v in layer["env_vars"])
    finally:
        sdk.layers.delete(layer["id"])


@pytest.mark.asyncio(loop_scope="session")
async def test_layers_get_async():
    sdk = AsyncDenoDeploy()

    slug = gen_layer_slug()
    layer = await sdk.layers.create(slug, description="test layer")
    try:
        fetched = await sdk.layers.get(layer["id"])
        assert fetched is not None
        assert fetched["id"] == layer["id"]
        assert fetched["slug"] == slug

        fetched_by_slug = await sdk.layers.get(slug)
        assert fetched_by_slug is not None
        assert fetched_by_slug["id"] == layer["id"]
    finally:
        await sdk.layers.delete(layer["id"])


def test_layers_get_sync():
    sdk = DenoDeploy()

    slug = gen_layer_slug()
    layer = sdk.layers.create(slug, description="test layer")
    try:
        fetched = sdk.layers.get(layer["id"])
        assert fetched is not None
        assert fetched["id"] == layer["id"]
        assert fetched["slug"] == slug

        fetched_by_slug = sdk.layers.get(slug)
        assert fetched_by_slug is not None
        assert fetched_by_slug["id"] == layer["id"]
    finally:
        sdk.layers.delete(layer["id"])


@pytest.mark.asyncio(loop_scope="session")
async def test_layers_get_not_found_async():
    sdk = AsyncDenoDeploy()
    result = await sdk.layers.get("nonexistent-layer-id")
    assert result is None


def test_layers_get_not_found_sync():
    sdk = DenoDeploy()
    result = sdk.layers.get("nonexistent-layer-id")
    assert result is None


@pytest.mark.asyncio(loop_scope="session")
async def test_layers_list_async():
    sdk = AsyncDenoDeploy()

    slug = gen_layer_slug()
    layer = await sdk.layers.create(slug)
    try:
        layers = await sdk.layers.list()
        assert type(layers.has_more) is bool
        assert any(x["id"] == layer["id"] for x in layers.items)
    finally:
        await sdk.layers.delete(layer["id"])


def test_layers_list_sync():
    sdk = DenoDeploy()

    slug = gen_layer_slug()
    layer = sdk.layers.create(slug)
    try:
        layers = sdk.layers.list()
        assert type(layers.has_more) is bool
        assert any(x["id"] == layer["id"] for x in layers.items)
    finally:
        sdk.layers.delete(layer["id"])


@pytest.mark.asyncio(loop_scope="session")
async def test_layers_update_async():
    sdk = AsyncDenoDeploy()

    slug = gen_layer_slug()
    layer = await sdk.layers.create(slug)
    try:
        new_slug = gen_layer_slug()
        updated = await sdk.layers.update(layer["id"], slug=new_slug)
        assert updated["slug"] == new_slug
        assert updated["id"] == layer["id"]
    finally:
        await sdk.layers.delete(layer["id"])


def test_layers_update_sync():
    sdk = DenoDeploy()

    slug = gen_layer_slug()
    layer = sdk.layers.create(slug)
    try:
        new_slug = gen_layer_slug()
        updated = sdk.layers.update(layer["id"], slug=new_slug)
        assert updated["slug"] == new_slug
        assert updated["id"] == layer["id"]
    finally:
        sdk.layers.delete(layer["id"])


@pytest.mark.asyncio(loop_scope="session")
async def test_layers_update_env_vars_async():
    sdk = AsyncDenoDeploy()

    slug = gen_layer_slug()
    layer = await sdk.layers.create(slug, env_vars=[{"key": "FOO", "value": "bar"}])
    try:
        updated = await sdk.layers.update(
            layer["id"],
            env_vars=[{"key": "BAZ", "value": "qux"}],
        )
        keys = [v["key"] for v in updated["env_vars"]]
        assert "BAZ" in keys
    finally:
        await sdk.layers.delete(layer["id"])


def test_layers_update_env_vars_sync():
    sdk = DenoDeploy()

    slug = gen_layer_slug()
    layer = sdk.layers.create(slug, env_vars=[{"key": "FOO", "value": "bar"}])
    try:
        updated = sdk.layers.update(
            layer["id"],
            env_vars=[{"key": "BAZ", "value": "qux"}],
        )
        keys = [v["key"] for v in updated["env_vars"]]
        assert "BAZ" in keys
    finally:
        sdk.layers.delete(layer["id"])


@pytest.mark.asyncio(loop_scope="session")
async def test_layers_delete_async():
    sdk = AsyncDenoDeploy()

    slug = gen_layer_slug()
    layer = await sdk.layers.create(slug)
    await sdk.layers.delete(layer["id"])

    result = await sdk.layers.get(layer["id"])
    assert result is None


def test_layers_delete_sync():
    sdk = DenoDeploy()

    slug = gen_layer_slug()
    layer = sdk.layers.create(slug)
    sdk.layers.delete(layer["id"])

    result = sdk.layers.get(layer["id"])
    assert result is None


@pytest.mark.asyncio(loop_scope="session")
async def test_layers_apps_async():
    sdk = AsyncDenoDeploy()

    slug = gen_layer_slug()
    layer = await sdk.layers.create(slug)
    try:
        apps = await sdk.layers.apps(layer["id"])
        assert type(apps.has_more) is bool
        assert isinstance(apps.items, list)
    finally:
        await sdk.layers.delete(layer["id"])


def test_layers_apps_sync():
    sdk = DenoDeploy()

    slug = gen_layer_slug()
    layer = sdk.layers.create(slug)
    try:
        apps = sdk.layers.apps(layer["id"])
        assert type(apps.has_more) is bool
        assert isinstance(apps.items, list)
    finally:
        sdk.layers.delete(layer["id"])
