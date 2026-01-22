import pytest
import uuid

from deno_sandbox import AsyncDenoDeploy, DenoDeploy
from deno_sandbox.volumes import Volume


def gen_volume_name() -> str:
    return f"test-volume-{uuid.uuid4().hex[:8]}"


@pytest.mark.asyncio(loop_scope="session")
async def test_volume_create_async():
    sdk = AsyncDenoDeploy()

    slug = gen_volume_name()
    volume = await sdk.volumes.create(slug, "ord", "1GB")

    assert volume is not None
    assert volume["id"] is not None

    expected: Volume = {
        "id": volume["id"],
        "slug": slug,
        "capacity": 1000000000,
        "estimated_allocated_size": 8797184,
        "estimated_flattened_size": 8797184,
        "region": "ord",
        "base_snapshot": None,
        "is_bootable": False,
    }
    assert volume == expected


async def test_volume_create_sync():
    sdk = DenoDeploy()

    slug = gen_volume_name()
    volume = sdk.volumes.create(slug, "ord", "1GB")

    assert volume is not None
    assert volume["id"] is not None

    expected: Volume = {
        "id": volume["id"],
        "slug": slug,
        "capacity": 1000000000,
        "estimated_allocated_size": 8797184,
        "estimated_flattened_size": 8797184,
        "region": "ord",
        "base_snapshot": None,
        "is_bootable": False,
    }
    assert volume == expected


@pytest.mark.asyncio(loop_scope="session")
async def test_volume_delete_async():
    sdk = AsyncDenoDeploy()

    slug = gen_volume_name()
    volume = await sdk.volumes.create(slug, "ord", "1GB")

    await sdk.volumes.delete(volume["id"])
    result = await sdk.volumes.get(volume["id"])
    assert result is None


async def test_volume_delete_sync():
    sdk = DenoDeploy()

    slug = gen_volume_name()
    volume = sdk.volumes.create(slug, "ord", "1GB")

    sdk.volumes.delete(volume["id"])

    result = sdk.volumes.get(volume["id"])
    assert result is None


@pytest.mark.asyncio(loop_scope="session")
async def test_volume_get_async():
    sdk = AsyncDenoDeploy()

    slug = gen_volume_name()
    volume = await sdk.volumes.create(slug, "ord", "1GB")

    volume2 = await sdk.volumes.get(volume["id"])

    assert volume == volume2


async def test_volume_get_sync():
    sdk = DenoDeploy()

    slug = gen_volume_name()
    volume = sdk.volumes.create(slug, "ord", "1GB")

    volume2 = sdk.volumes.get(volume["id"])
    assert volume == volume2


@pytest.mark.asyncio(loop_scope="session")
async def test_volume_list_async():
    sdk = AsyncDenoDeploy()

    slug = gen_volume_name()
    volume = await sdk.volumes.create(slug, "ord", "1GB")

    volumes = await sdk.volumes.list()

    assert type(volumes.has_more) is bool
    assert volumes.next_cursor is None or type(volumes.next_cursor) is str
    assert any(v["id"] == volume["id"] for v in volumes.items)


async def test_volume_list_sync():
    sdk = DenoDeploy()

    slug = gen_volume_name()
    volume = sdk.volumes.create(slug, "ord", "1GB")

    volumes = sdk.volumes.list()

    assert type(volumes.has_more) is bool
    assert volumes.next_cursor is None or type(volumes.next_cursor) is str
    assert any(v["id"] == volume["id"] for v in volumes.items)
