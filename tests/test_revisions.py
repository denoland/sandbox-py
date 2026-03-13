import asyncio
import time

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
async def test_revisions_deploy_async():
    sdk = AsyncDenoDeploy()
    app = await sdk.apps.create()
    try:
        revision = await sdk.revisions.deploy(
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
        while revision["status"] in ("queued", "building"):
            await asyncio.sleep(1)
            revision = await sdk.revisions.get(revision["id"])
            assert revision is not None
        assert revision["status"] == "succeeded", revision.get("failure_reason")
    finally:
        await sdk.apps.delete(app["id"])


@pytest.mark.timeout(60)
def test_revisions_deploy_sync():
    sdk = DenoDeploy()
    app = sdk.apps.create()
    try:
        revision = sdk.revisions.deploy(
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
        while revision["status"] in ("queued", "building"):
            time.sleep(1)
            revision = sdk.revisions.get(revision["id"])
            assert revision is not None
        assert revision["status"] == "succeeded", revision.get("failure_reason")
    finally:
        sdk.apps.delete(app["id"])


@pytest.mark.timeout(120)
@pytest.mark.asyncio(loop_scope="session")
async def test_revisions_deploy_preview_only_async():
    """Deploy with production=False, preview=True and verify timeline assignment."""
    sdk = AsyncDenoDeploy()
    app = await sdk.apps.create()
    try:
        revision = await sdk.revisions.deploy(
            app["id"],
            assets={
                "main.ts": {
                    "kind": "file",
                    "encoding": "utf-8",
                    "content": 'Deno.serve(() => new Response("Hello"))',
                }
            },
            production=False,
            preview=True,
        )
        assert revision["id"] is not None
        while revision["status"] in ("queued", "building"):
            await asyncio.sleep(1)
            revision = await sdk.revisions.get(revision["id"])
            assert revision is not None
        assert revision["status"] == "succeeded", revision.get("failure_reason")

        # Verify timeline assignment via the revision timelines API
        timelines = await sdk.revisions.timelines(revision["id"])
        production = [
            t
            for t in timelines
            if t["slug"] == "production"
            and not t.get("partition", {}).get("deno.revision.id")
        ]
        preview = [
            t
            for t in timelines
            if t["slug"] == "preview"
            and t.get("partition", {}).get("deno.revision.id") == revision["id"]
        ]
        assert len(production) == 0, "should not be on production timeline"
        assert len(preview) > 0, "should be on preview timeline"
    finally:
        await sdk.apps.delete(app["id"])


@pytest.mark.timeout(60)
@pytest.mark.asyncio(loop_scope="session")
async def test_revisions_deploy_crons_disabled_fails_async():
    sdk = AsyncDenoDeploy()
    app = await sdk.apps.create(config={"crons": False})
    try:
        revision = await sdk.revisions.deploy(
            app["id"],
            assets={
                "main.ts": {
                    "kind": "file",
                    "encoding": "utf-8",
                    "content": 'Deno.cron("test", "* * * * *", () => {}); Deno.serve(() => new Response("Hello"))',
                }
            },
        )
        while revision["status"] in ("queued", "building"):
            await asyncio.sleep(1)
            revision = await sdk.revisions.get(revision["id"])
            assert revision is not None
        assert revision["status"] == "failed"
    finally:
        await sdk.apps.delete(app["id"])


VALID_STAGE_STATUSES = {
    "pending",
    "running",
    "succeeded",
    "skipped",
    "failed",
    "timed_out",
    "cancelled",
    "errored",
}


def _assert_progress_events(events: list[dict]) -> None:
    """Shared assertions for progress event lists."""
    assert len(events) > 0, "Expected at least one progress event"

    for event in events:
        assert isinstance(event, dict)
        # Each event should have at least one known stage key
        stage_keys = {"queued", "preparing", "installing", "building", "deploying"}
        found_keys = stage_keys & event.keys()
        assert len(found_keys) > 0, f"No known stage keys in event: {event}"

        for key in found_keys:
            stage = event[key]
            assert "status" in stage, f"Stage {key} missing 'status'"
            assert stage["status"] in VALID_STAGE_STATUSES, (
                f"Stage {key} has unexpected status: {stage['status']}"
            )

    # The last event should have at least one stage in a terminal state
    last = events[-1]
    terminal_statuses = {"succeeded", "failed", "skipped"}
    has_terminal = any(
        last.get(k, {}).get("status") in terminal_statuses
        for k in ("queued", "preparing", "installing", "building", "deploying")
        if k in last
    )
    assert has_terminal, f"Last event has no terminal stage: {last}"


@pytest.mark.timeout(120)
@pytest.mark.asyncio(loop_scope="session")
async def test_revisions_progress_async():
    """Deploy a revision and stream progress until terminal state."""
    sdk = AsyncDenoDeploy()
    app = await sdk.apps.create()
    try:
        revision = await sdk.revisions.deploy(
            app["id"],
            assets={
                "main.ts": {
                    "kind": "file",
                    "encoding": "utf-8",
                    "content": 'Deno.serve(() => new Response("Hello"))',
                }
            },
        )

        events = []
        async for event in sdk.revisions.progress(revision["id"]):
            events.append(event)

        _assert_progress_events(events)
    finally:
        await sdk.apps.delete(app["id"])


@pytest.mark.timeout(120)
def test_revisions_progress_sync():
    """Deploy a revision and stream progress until terminal state (sync)."""
    sdk = DenoDeploy()
    app = sdk.apps.create()
    try:
        revision = sdk.revisions.deploy(
            app["id"],
            assets={
                "main.ts": {
                    "kind": "file",
                    "encoding": "utf-8",
                    "content": 'Deno.serve(() => new Response("Hello"))',
                }
            },
        )

        events = list(sdk.revisions.progress(revision["id"]))

        _assert_progress_events(events)
    finally:
        sdk.apps.delete(app["id"])


@pytest.mark.skip(reason="DELETE /v2/revisions/{id} returns 500 on staging")
@pytest.mark.timeout(120)
@pytest.mark.asyncio(loop_scope="session")
async def test_revisions_delete_async():
    """Deploy a preview-only revision, wait for it, then delete it."""
    sdk = AsyncDenoDeploy()
    app = await sdk.apps.create()
    try:
        revision = await sdk.revisions.deploy(
            app["id"],
            assets={
                "main.ts": {
                    "kind": "file",
                    "encoding": "utf-8",
                    "content": 'Deno.serve(() => new Response("Hello"))',
                }
            },
            production=False,
            preview=True,
        )
        # Wait for build to finish
        async for _ in sdk.revisions.progress(revision["id"]):
            pass

        await sdk.revisions.delete(revision["id"])

        fetched = await sdk.revisions.get(revision["id"])
        assert fetched is not None
        assert fetched.get("deleted_at") is not None
    finally:
        await sdk.apps.delete(app["id"])


@pytest.mark.skip(reason="DELETE /v2/revisions/{id} returns 500 on staging")
@pytest.mark.timeout(120)
def test_revisions_delete_sync():
    """Deploy a preview-only revision, wait for it, then delete it."""
    sdk = DenoDeploy()
    app = sdk.apps.create()
    try:
        revision = sdk.revisions.deploy(
            app["id"],
            assets={
                "main.ts": {
                    "kind": "file",
                    "encoding": "utf-8",
                    "content": 'Deno.serve(() => new Response("Hello"))',
                }
            },
            production=False,
            preview=True,
        )
        # Wait for build to finish
        list(sdk.revisions.progress(revision["id"]))

        sdk.revisions.delete(revision["id"])

        fetched = sdk.revisions.get(revision["id"])
        assert fetched is not None
        assert fetched.get("deleted_at") is not None
    finally:
        sdk.apps.delete(app["id"])


@pytest.mark.timeout(120)
@pytest.mark.asyncio(loop_scope="session")
async def test_revisions_build_logs_async():
    """Deploy a revision and stream build logs."""
    sdk = AsyncDenoDeploy()
    app = await sdk.apps.create()
    try:
        revision = await sdk.revisions.deploy(
            app["id"],
            assets={
                "main.ts": {
                    "kind": "file",
                    "encoding": "utf-8",
                    "content": 'Deno.serve(() => new Response("Hello"))',
                }
            },
        )

        logs = []
        async for entry in sdk.revisions.build_logs(revision["id"]):
            logs.append(entry)
            assert "timestamp" in entry
            assert "level" in entry
            assert "message" in entry

        assert len(logs) > 0, "Expected at least one build log entry"
    finally:
        await sdk.apps.delete(app["id"])


@pytest.mark.timeout(120)
def test_revisions_build_logs_sync():
    """Deploy a revision and stream build logs (sync)."""
    sdk = DenoDeploy()
    app = sdk.apps.create()
    try:
        revision = sdk.revisions.deploy(
            app["id"],
            assets={
                "main.ts": {
                    "kind": "file",
                    "encoding": "utf-8",
                    "content": 'Deno.serve(() => new Response("Hello"))',
                }
            },
        )

        logs = list(sdk.revisions.build_logs(revision["id"]))

        assert len(logs) > 0, "Expected at least one build log entry"
        for entry in logs:
            assert "timestamp" in entry
            assert "level" in entry
            assert "message" in entry
    finally:
        sdk.apps.delete(app["id"])


@pytest.mark.timeout(120)
@pytest.mark.asyncio(loop_scope="session")
async def test_revisions_timelines_async():
    """Deploy a revision and check its timelines."""
    sdk = AsyncDenoDeploy()
    app = await sdk.apps.create()
    try:
        revision = await sdk.revisions.deploy(
            app["id"],
            assets={
                "main.ts": {
                    "kind": "file",
                    "encoding": "utf-8",
                    "content": 'Deno.serve(() => new Response("Hello"))',
                }
            },
        )
        # Wait for build to finish
        async for _ in sdk.revisions.progress(revision["id"]):
            pass

        timelines = await sdk.revisions.timelines(revision["id"])
        assert isinstance(timelines, list)
        assert len(timelines) > 0
        for t in timelines:
            assert "slug" in t
            assert "partition" in t
            assert "domains" in t
    finally:
        await sdk.apps.delete(app["id"])


@pytest.mark.timeout(120)
def test_revisions_timelines_sync():
    """Deploy a revision and check its timelines (sync)."""
    sdk = DenoDeploy()
    app = sdk.apps.create()
    try:
        revision = sdk.revisions.deploy(
            app["id"],
            assets={
                "main.ts": {
                    "kind": "file",
                    "encoding": "utf-8",
                    "content": 'Deno.serve(() => new Response("Hello"))',
                }
            },
        )
        # Wait for build to finish
        list(sdk.revisions.progress(revision["id"]))

        timelines = sdk.revisions.timelines(revision["id"])
        assert isinstance(timelines, list)
        assert len(timelines) > 0
        for t in timelines:
            assert "slug" in t
            assert "partition" in t
            assert "domains" in t
    finally:
        sdk.apps.delete(app["id"])


@pytest.mark.asyncio(loop_scope="session")
async def test_revisions_list_with_status_async():
    """List revisions filtered by status."""
    sdk = AsyncDenoDeploy()
    app = await sdk.apps.create()
    try:
        revisions = await sdk.revisions.list(app["id"], status="succeeded")
        assert isinstance(revisions.items, list)
        for r in revisions.items:
            assert r["status"] == "succeeded"
    finally:
        await sdk.apps.delete(app["id"])


def test_revisions_list_with_status_sync():
    """List revisions filtered by status."""
    sdk = DenoDeploy()
    app = sdk.apps.create()
    try:
        revisions = sdk.revisions.list(app["id"], status="succeeded")
        assert isinstance(revisions.items, list)
        for r in revisions.items:
            assert r["status"] == "succeeded"
    finally:
        sdk.apps.delete(app["id"])
