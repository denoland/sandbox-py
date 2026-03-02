"""Unit tests for console client HTTP error handling."""

from unittest.mock import AsyncMock, patch
import json

import httpx
import pytest

from deno_sandbox.console import AsyncConsoleClient
from deno_sandbox.errors import HTTPStatusError
from deno_sandbox.options import InternalOptions


def make_options() -> InternalOptions:
    return InternalOptions(
        console_url=httpx.URL("https://console.example.com"),
        sandbox_ws_url=httpx.URL("wss://sandbox.example.com"),
        sandbox_url=httpx.URL("https://sandbox.example.com"),
        token="test-token",
        regions=["ord"],
        sandbox_base_domain="sandbox.example.com",
    )


def make_response(
    status_code: int,
    body: str | None = None,
    trace_id: str | None = None,
) -> httpx.Response:
    """Build a fake httpx.Response with the given status, body, and optional trace ID."""
    headers: dict[str, str] = {}
    if body:
        headers["content-type"] = "application/json"
    if trace_id:
        headers["x-deno-trace-id"] = trace_id
    return httpx.Response(
        status_code=status_code,
        content=body.encode() if body else b"",
        headers=headers,
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_error_extracts_code_and_message():
    """API error response with code+message is surfaced in the exception."""
    client = AsyncConsoleClient(make_options())
    error_body = json.dumps({"code": "APP_NOT_FOUND", "message": "App does not exist"})
    mock_resp = make_response(404, error_body)

    with patch.object(client.client, "request", new=AsyncMock(return_value=mock_resp)):
        with pytest.raises(HTTPStatusError) as exc_info:
            await client.get("/api/apps/missing")

    err = exc_info.value
    assert err.status_code == 404
    assert err.code == "APP_NOT_FOUND"
    assert err.message == "App does not exist"
    assert err.trace_id is None
    assert str(err) == "App does not exist (status: 404, code: APP_NOT_FOUND)"


@pytest.mark.asyncio(loop_scope="session")
async def test_error_includes_trace_id():
    """Trace ID from x-deno-trace-id header is included in the exception."""
    client = AsyncConsoleClient(make_options())
    error_body = json.dumps({"code": "APP_NOT_FOUND", "message": "App does not exist"})
    mock_resp = make_response(404, error_body, trace_id="abc-123-def")

    with patch.object(client.client, "request", new=AsyncMock(return_value=mock_resp)):
        with pytest.raises(HTTPStatusError) as exc_info:
            await client.get("/api/apps/missing")

    err = exc_info.value
    assert err.status_code == 404
    assert err.code == "APP_NOT_FOUND"
    assert err.message == "App does not exist"
    assert err.trace_id == "abc-123-def"
    assert str(err) == "App does not exist (status: 404, code: APP_NOT_FOUND, traceId: abc-123-def)"


@pytest.mark.asyncio(loop_scope="session")
async def test_error_trace_id_with_fallback_message():
    """Trace ID is included even when falling back to a generic message."""
    client = AsyncConsoleClient(make_options())
    mock_resp = make_response(500, "Internal Server Error", trace_id="trace-xyz")

    with patch.object(client.client, "request", new=AsyncMock(return_value=mock_resp)):
        with pytest.raises(HTTPStatusError) as exc_info:
            await client.get("/api/apps/broken")

    err = exc_info.value
    assert err.status_code == 500
    assert err.code == "UNKNOWN_ERROR"
    assert err.trace_id == "trace-xyz"
    assert "traceId: trace-xyz" in str(err)
    assert "status: 500" in str(err)
    assert "code: UNKNOWN_ERROR" in str(err)


@pytest.mark.asyncio(loop_scope="session")
async def test_error_with_non_json_body():
    """Non-JSON response body falls back to a generic message."""
    client = AsyncConsoleClient(make_options())
    mock_resp = make_response(500, "Internal Server Error")

    with patch.object(client.client, "request", new=AsyncMock(return_value=mock_resp)):
        with pytest.raises(HTTPStatusError) as exc_info:
            await client.get("/api/apps/broken")

    err = exc_info.value
    assert err.status_code == 500
    assert err.code == "UNKNOWN_ERROR"
    assert "failed with status 500" in err.message


@pytest.mark.asyncio(loop_scope="session")
async def test_error_with_json_missing_fields():
    """JSON body without code/message fields falls back to a generic message."""
    client = AsyncConsoleClient(make_options())
    error_body = json.dumps({"error": "something went wrong"})
    mock_resp = make_response(400, error_body)

    with patch.object(client.client, "request", new=AsyncMock(return_value=mock_resp)):
        with pytest.raises(HTTPStatusError) as exc_info:
            await client.post("/api/apps", data={})

    err = exc_info.value
    assert err.status_code == 400
    assert err.code == "UNKNOWN_ERROR"
    assert "failed with status 400" in err.message


@pytest.mark.asyncio(loop_scope="session")
async def test_error_with_empty_body():
    """Empty response body falls back to a generic message."""
    client = AsyncConsoleClient(make_options())
    mock_resp = make_response(502)

    with patch.object(client.client, "request", new=AsyncMock(return_value=mock_resp)):
        with pytest.raises(HTTPStatusError) as exc_info:
            await client.get("/api/apps/bad-gateway")

    err = exc_info.value
    assert err.status_code == 502
    assert err.code == "UNKNOWN_ERROR"


@pytest.mark.asyncio(loop_scope="session")
async def test_error_with_non_string_code():
    """JSON body with non-string code/message falls back to generic message."""
    client = AsyncConsoleClient(make_options())
    error_body = json.dumps({"code": 123, "message": "not a string code"})
    mock_resp = make_response(400, error_body)

    with patch.object(client.client, "request", new=AsyncMock(return_value=mock_resp)):
        with pytest.raises(HTTPStatusError) as exc_info:
            await client.post("/api/apps", data={})

    err = exc_info.value
    assert err.status_code == 400
    assert err.code == "UNKNOWN_ERROR"


@pytest.mark.asyncio(loop_scope="session")
async def test_get_or_none_returns_none_on_404():
    """get_or_none returns None for 404 errors."""
    client = AsyncConsoleClient(make_options())
    error_body = json.dumps({"code": "NOT_FOUND", "message": "Not found"})
    mock_resp = make_response(404, error_body)

    with patch.object(client.client, "request", new=AsyncMock(return_value=mock_resp)):
        result = await client.get_or_none("/api/apps/missing")

    assert result is None


@pytest.mark.asyncio(loop_scope="session")
async def test_get_or_none_raises_on_non_404():
    """get_or_none re-raises non-404 errors."""
    client = AsyncConsoleClient(make_options())
    error_body = json.dumps({"code": "FORBIDDEN", "message": "Access denied"})
    mock_resp = make_response(403, error_body)

    with patch.object(client.client, "request", new=AsyncMock(return_value=mock_resp)):
        with pytest.raises(HTTPStatusError) as exc_info:
            await client.get_or_none("/api/apps/forbidden")

    err = exc_info.value
    assert err.status_code == 403
    assert err.code == "FORBIDDEN"
    assert err.message == "Access denied"


@pytest.mark.asyncio(loop_scope="session")
async def test_success_response_not_affected():
    """Successful responses are returned normally."""
    client = AsyncConsoleClient(make_options())
    mock_resp = make_response(200, json.dumps({"id": "app-123", "slug": "my-app"}))

    with patch.object(client.client, "request", new=AsyncMock(return_value=mock_resp)):
        result = await client.get("/api/apps/app-123")

    assert result == {"id": "app-123", "slug": "my-app"}
