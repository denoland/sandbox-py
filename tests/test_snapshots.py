import asyncio
import pytest
import uuid

from deno_sandbox import AsyncDenoDeploy
from deno_sandbox.volumes import Volume


def gen_volume_name() -> str:
    return f"test-volume-{uuid.uuid4().hex[:8]}"


@pytest.mark.timeout(60)
@pytest.mark.asyncio(loop_scope="session")
async def test_volume_create_root_async():
    sdk = AsyncDenoDeploy()

    slug = gen_volume_name()
    volume = await sdk.volumes.create(
        slug, "ord", "10GB", from_snapshot="builtin:debian-13"
    )

    expected: Volume = {
        "id": volume["id"],
        "slug": slug,
        "capacity": 10000000000,
        "estimated_allocated_size": 0,
        "estimated_flattened_size": 0,
        "region": "ord",
        "base_snapshot": None,
        "is_bootable": True,
    }
    assert volume == expected

    async with sdk.sandbox.create(root=volume["slug"], region="ord") as sb:
        await sb.fs.write_text_file("/home/app/foo.txt", "foo")
        cp = await sb.spawn("sync")
        await cp.wait()

    await asyncio.sleep(1)

    async with sdk.sandbox.create(root=volume["slug"], region="ord") as sb:
        content = await sb.fs.read_text_file("/home/app/foo.txt")
        assert content == "foo"
