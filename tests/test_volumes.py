from pprint import pprint
import random
import pytest

from deno_sandbox import AsyncDenoDeploy, DenoDeploy
from deno_sandbox.api_types_generated import Volume


@pytest.mark.asyncio(loop_scope="session")
async def test_volume_create_async():
    sdk = AsyncDenoDeploy()

    slug = f"my-volume-{random.randint(1, 100)}"
    volume = await sdk.volumes.create(
        {"capacity": "1GB", "region": "ord", "slug": slug}
    )

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

    slug = f"my-volume-{random.randint(1, 100)}"
    volume = sdk.volumes.create({"capacity": "1GB", "region": "ord", "slug": slug})

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
async def test_volume_get_async():
    sdk = AsyncDenoDeploy()

    slug = f"my-volume-{random.randint(1, 100)}"
    volume = await sdk.volumes.create(
        {"capacity": "1GB", "region": "ord", "slug": slug}
    )

    volume2 = await sdk.volumes.get(volume["id"])

    assert volume == volume2


async def test_volume_get_sync():
    sdk = DenoDeploy()

    slug = f"my-volume-{random.randint(1, 100)}"
    volume = sdk.volumes.create({"capacity": "1GB", "region": "ord", "slug": slug})

    volume2 = sdk.volumes.get(volume["id"])
    assert volume == volume2


@pytest.mark.asyncio(loop_scope="session")
async def test_volume_list_async():
    sdk = AsyncDenoDeploy()

    slug = f"my-volume-{random.randint(1, 100)}"
    volume = await sdk.volumes.create(
        {"capacity": "1GB", "region": "ord", "slug": slug}
    )

    volumes = await sdk.volumes.list()

    pprint(volumes)

    assert type(volumes["has_more"]) is bool
    assert "next_cursor" in volumes
    assert any(v["id"] == volume["id"] for v in volumes["items"])
