"""Unit tests for timeline pinning and revision promotion.

These assert the request each method issues, so they run offline against a
mocked transport rather than a live backend.
"""

from unittest.mock import AsyncMock, patch

import httpx
import pytest

from deno_sandbox.bridge import AsyncBridge
from deno_sandbox.console import AsyncConsoleClient
from deno_sandbox.options import InternalOptions
from deno_sandbox.revisions import AsyncRevisions, Revisions
from deno_sandbox.timelines import AsyncTimelines, Timelines


def make_client() -> AsyncConsoleClient:
    return AsyncConsoleClient(
        InternalOptions(
            console_url=httpx.URL("https://console.example.com"),
            sandbox_ws_url=httpx.URL("wss://sandbox.example.com"),
            sandbox_url=httpx.URL("https://sandbox.example.com"),
            token="test-token",
            regions=["ord"],
            sandbox_base_domain="sandbox.example.com",
        )
    )


def no_content() -> httpx.Response:
    return httpx.Response(status_code=204)


@pytest.mark.asyncio(loop_scope="session")
async def test_pin_async():
    client = make_client()
    request = AsyncMock(return_value=no_content())

    with patch.object(client.client, "request", new=request):
        await AsyncTimelines(client).pin("my-app", "production", "rev-1")

    kwargs = request.call_args.kwargs
    assert kwargs["method"] == "PUT"
    assert (
        str(kwargs["url"])
        == "https://console.example.com/api/v2/apps/my-app/timelines/production/pin"
    )
    assert kwargs["json"] == {"revision": "rev-1"}


@pytest.mark.asyncio(loop_scope="session")
async def test_unpin_async():
    client = make_client()
    request = AsyncMock(return_value=no_content())

    with patch.object(client.client, "request", new=request):
        await AsyncTimelines(client).unpin("my-app", "production")

    kwargs = request.call_args.kwargs
    assert kwargs["method"] == "DELETE"
    assert (
        str(kwargs["url"])
        == "https://console.example.com/api/v2/apps/my-app/timelines/production/pin"
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_pin_escapes_parameterized_timeline_id():
    """A timeline ID carrying partition values stays a single path segment."""
    client = make_client()
    request = AsyncMock(return_value=no_content())

    with patch.object(client.client, "request", new=request):
        await AsyncTimelines(client).pin("my-app", "git-branch:feat%2Fx", "rev-1")

    url = str(request.call_args.kwargs["url"])
    assert url == (
        "https://console.example.com/api/v2/apps/my-app/timelines/"
        "git-branch%3Afeat%252Fx/pin"
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_promote_async():
    client = make_client()
    request = AsyncMock(return_value=no_content())

    with patch.object(client.client, "request", new=request):
        await AsyncRevisions(client).promote("rev-1")

    kwargs = request.call_args.kwargs
    assert kwargs["method"] == "POST"
    assert (
        str(kwargs["url"])
        == "https://console.example.com/api/v2/revisions/rev-1/promote"
    )


def test_pin_and_unpin_sync():
    client = make_client()
    bridge = AsyncBridge()
    request = AsyncMock(return_value=no_content())

    try:
        with patch.object(client.client, "request", new=request):
            timelines = Timelines(client, bridge)
            timelines.pin("my-app", "production", "rev-1")
            assert request.call_args.kwargs["method"] == "PUT"
            assert request.call_args.kwargs["json"] == {"revision": "rev-1"}

            timelines.unpin("my-app", "production")
            assert request.call_args.kwargs["method"] == "DELETE"
    finally:
        bridge.stop()


def test_promote_sync():
    client = make_client()
    bridge = AsyncBridge()
    request = AsyncMock(return_value=no_content())

    try:
        with patch.object(client.client, "request", new=request):
            Revisions(client, bridge).promote("rev-1")
    finally:
        bridge.stop()

    kwargs = request.call_args.kwargs
    assert kwargs["method"] == "POST"
    assert (
        str(kwargs["url"])
        == "https://console.example.com/api/v2/revisions/rev-1/promote"
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_list_preserves_timeline_fields():
    """`id`, `pinned_revision` and the partition keys survive response parsing.

    `get_paginated` runs every item through `convert_to_snake_case`, which
    rewrites dict keys — including the partition's, which are dotted label
    names that must be passed through untouched.
    """
    client = make_client()
    body = [
        {
            "id": "git-branch:main",
            "slug": "git-branch",
            "partition": {"deno.git.branch": "main"},
            "pinned_revision": "rev-1",
            "domains": [{"domain": "example.deno.net"}],
        },
        {
            "id": "production",
            "slug": "production",
            "partition": {},
            "pinned_revision": None,
            "domains": [],
        },
    ]
    response = httpx.Response(
        status_code=200,
        json=body,
        headers={"content-type": "application/json"},
        request=httpx.Request("GET", "https://console.example.com/"),
    )

    with patch.object(client.client, "request", new=AsyncMock(return_value=response)):
        timelines = await AsyncTimelines(client).list("my-app")

    branch, production = timelines.items
    assert branch["id"] == "git-branch:main"
    assert branch["partition"] == {"deno.git.branch": "main"}
    assert branch["pinned_revision"] == "rev-1"
    assert production["id"] == "production"
    assert production["pinned_revision"] is None
