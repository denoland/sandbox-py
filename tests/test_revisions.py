import pytest
import uuid
import warnings

from deno_sandbox import AsyncDenoDeploy, DenoDeploy


def gen_app_name() -> str:
    return f"test-app-{uuid.uuid4().hex[:8]}"


@pytest.mark.asyncio(loop_scope="session")
async def test_revisions_list_async():
    sdk = AsyncDenoDeploy()

    app = await sdk.apps.create()
    try:
        revisions = await sdk.revisions.list(app["id"])

        assert type(revisions.has_more) is bool
        assert revisions.next_cursor is None or type(revisions.next_cursor) is str
        assert isinstance(revisions.items, list)
    finally:
        await sdk.apps.delete(app["id"])


def test_revisions_list_sync():
    sdk = DenoDeploy()

    app = sdk.apps.create()
    try:
        revisions = sdk.revisions.list(app["id"])

        assert type(revisions.has_more) is bool
        assert revisions.next_cursor is None or type(revisions.next_cursor) is str
        assert isinstance(revisions.items, list)
    finally:
        sdk.apps.delete(app["id"])


@pytest.mark.timeout(60)
@pytest.mark.asyncio(loop_scope="session")
async def test_revisions_get_async():
    """Deploy to create a revision, then fetch it by ID (single-arg form)."""
    sdk = AsyncDenoDeploy()

    app = await sdk.apps.create()
    try:
        async with sdk.sandbox.create() as sandbox:
            await sandbox.fs.write_text_file(
                "main.ts",
                'Deno.serve(() => new Response("Hello"))',
            )
            build = await sandbox.deno.deploy(app["slug"], entrypoint="main.ts")
            revision = await build.wait()

        fetched = await sdk.revisions.get(revision["id"])
        assert fetched is not None
        assert fetched["id"] == revision["id"]
        assert fetched["status"] in [
            "skipped",
            "queued",
            "building",
            "succeeded",
            "failed",
        ]
    finally:
        await sdk.apps.delete(app["id"])


@pytest.mark.timeout(60)
def test_revisions_get_sync():
    """Deploy to create a revision, then fetch it by ID (single-arg form)."""
    sdk = DenoDeploy()

    app = sdk.apps.create()
    try:
        with sdk.sandbox.create() as sandbox:
            sandbox.fs.write_text_file(
                "main.ts",
                'Deno.serve(() => new Response("Hello"))',
            )
            build = sandbox.deno.deploy(app["slug"], entrypoint="main.ts")
            revision = build.wait()

        fetched = sdk.revisions.get(revision["id"])
        assert fetched is not None
        assert fetched["id"] == revision["id"]
        assert fetched["status"] in [
            "skipped",
            "queued",
            "building",
            "succeeded",
            "failed",
        ]
    finally:
        sdk.apps.delete(app["id"])


@pytest.mark.asyncio(loop_scope="session")
async def test_revisions_get_not_found_async():
    sdk = AsyncDenoDeploy()

    result = await sdk.revisions.get("nonexistent-revision-id")
    assert result is None


def test_revisions_get_not_found_sync():
    sdk = DenoDeploy()

    result = sdk.revisions.get("nonexistent-revision-id")
    assert result is None


@pytest.mark.timeout(60)
@pytest.mark.asyncio(loop_scope="session")
async def test_revisions_get_deprecated_two_arg_async():
    """The old two-argument form should still work but emit a deprecation warning."""
    sdk = AsyncDenoDeploy()

    app = await sdk.apps.create()
    try:
        async with sdk.sandbox.create() as sandbox:
            await sandbox.fs.write_text_file(
                "main.ts",
                'Deno.serve(() => new Response("Hello"))',
            )
            build = await sandbox.deno.deploy(app["slug"], entrypoint="main.ts")
            revision = await build.wait()

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            fetched = await sdk.revisions.get(app["id"], revision["id"])
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert "deprecated" in str(w[0].message).lower()

        assert fetched is not None
        assert fetched["id"] == revision["id"]
    finally:
        await sdk.apps.delete(app["id"])


@pytest.mark.timeout(60)
@pytest.mark.asyncio(loop_scope="session")
async def test_revisions_create_async():
    sdk = AsyncDenoDeploy()
    app = await sdk.apps.create()
    try:
        revision = await sdk.revisions.create(
            app["id"],
            assets={
                "main.ts": {
                    "kind": "file",
                    "encoding": "utf-8",
                    "content": 'Deno.serve(() => new Response("Hello"))',
                }
            },
        )
        assert revision["id"] is not None
        assert revision["status"] in [
            "queued",
            "building",
            "succeeded",
            "failed",
        ]
    finally:
        await sdk.apps.delete(app["id"])


@pytest.mark.timeout(60)
def test_revisions_create_sync():
    sdk = DenoDeploy()
    app = sdk.apps.create()
    try:
        revision = sdk.revisions.create(
            app["id"],
            assets={
                "main.ts": {
                    "kind": "file",
                    "encoding": "utf-8",
                    "content": 'Deno.serve(() => new Response("Hello"))',
                }
            },
        )
        assert revision["id"] is not None
        assert revision["status"] in [
            "queued",
            "building",
            "succeeded",
            "failed",
        ]
    finally:
        sdk.apps.delete(app["id"])
