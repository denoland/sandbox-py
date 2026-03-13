"""
Example: create an app, deploy a hello-world server via the assets API,
watch the build finish, and query runtime logs.
"""

import asyncio
import time
from datetime import datetime, timezone

import pytest

from deno_sandbox import AsyncDenoDeploy, Config, DenoDeploy
from deno_sandbox.errors import HTTPStatusError

HELLO_WORLD = 'Deno.serve(() => new Response("Hello from Deno Deploy!"))'

RUNTIME_CONFIG: Config = {
    "runtime": {
        "type": "dynamic",
        "entrypoint": "main.ts",
    }
}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@pytest.mark.timeout(120)
@pytest.mark.asyncio(loop_scope="session")
async def test_deploy_hello_world_async():
    sdk = AsyncDenoDeploy()

    # 1. Create an app
    app = await sdk.apps.create()
    try:
        # 2. Deploy a hello-world server using the assets endpoint
        deploy_start = utc_now_iso()
        revision = await sdk.revisions.deploy(
            app["id"],
            assets={
                "main.ts": {
                    "kind": "file",
                    "encoding": "utf-8",
                    "content": HELLO_WORLD,
                }
            },
            config=RUNTIME_CONFIG,
        )
        assert revision["id"] is not None
        assert revision["status"] in ("queued", "building", "succeeded")

        # 3. Observe build progress by polling the revision status
        while revision["status"] in ("queued", "building"):
            await asyncio.sleep(1)
            revision = await sdk.revisions.get(revision["id"])
            assert revision is not None
        assert revision["status"] == "succeeded", revision.get("failure_reason")

        # 4. Query runtime logs (best-effort — endpoint may not be available yet)
        await asyncio.sleep(2)  # give logs a moment to be indexed
        try:
            logs_resp = await sdk.apps.logs(
                app["id"],
                start=deploy_start,
                revision_id=revision["id"],
            )
            assert isinstance(logs_resp["logs"], list)
        except HTTPStatusError:
            pass  # logs endpoint not available yet
    finally:
        await sdk.apps.delete(app["id"])


@pytest.mark.timeout(120)
def test_deploy_hello_world_sync():
    sdk = DenoDeploy()

    # 1. Create an app
    app = sdk.apps.create()
    try:
        # 2. Deploy a hello-world server using the assets endpoint
        deploy_start = utc_now_iso()
        revision = sdk.revisions.deploy(
            app["id"],
            assets={
                "main.ts": {
                    "kind": "file",
                    "encoding": "utf-8",
                    "content": HELLO_WORLD,
                }
            },
            config=RUNTIME_CONFIG,
        )
        assert revision["id"] is not None
        assert revision["status"] in ("queued", "building", "succeeded")

        # 3. Observe build progress by polling the revision status
        while revision["status"] in ("queued", "building"):
            time.sleep(1)
            revision = sdk.revisions.get(revision["id"])
            assert revision is not None
        assert revision["status"] == "succeeded", revision.get("failure_reason")

        # 4. Query runtime logs (best-effort — endpoint may not be available yet)
        time.sleep(2)  # give logs a moment to be indexed
        try:
            logs_resp = sdk.apps.logs(
                app["id"],
                start=deploy_start,
                revision_id=revision["id"],
            )
            assert isinstance(logs_resp["logs"], list)
        except HTTPStatusError:
            pass  # logs endpoint not available yet
    finally:
        sdk.apps.delete(app["id"])
