# Project overview

This is the official Python SDK for [Deno Sandboxes](https://deno.com/deploy/sandboxes) (`deno-sandbox` on PyPI). It provides programmatic access to create and manage sandboxes, execute code, manage filesystems, volumes, apps, and deployments.

## Architecture

- **Async-first**: All I/O is implemented as async code first. The sync API wraps it via `AsyncBridge` (in `bridge.py`), which runs a separate event loop in a background thread.
- **Class naming**: Async classes are prefixed with `Async` (e.g., `AsyncDenoDeploy`, `AsyncSandbox`, `AsyncSandboxFs`). Sync wrappers drop the prefix (`DenoDeploy`, `Sandbox`, `SandboxFs`).
- **Data models**: Use `TypedDict` for all data models. Do NOT use dataclasses or Pydantic.
- **HTTP**: Uses `httpx.AsyncClient`. Do NOT introduce `requests` or `aiohttp`.
- **WebSocket**: Uses `websockets`. Do NOT introduce other WS libraries.
- **Source code**: `src/deno_sandbox/`
- **Public exports**: `src/deno_sandbox/__init__.py`

## Key files

- `bridge.py` — `AsyncBridge` that powers the sync API
- `sandbox.py` — Sandbox creation and management
- `fs.py` — Filesystem operations
- `process.py` — Child process management
- `rpc.py` — JSON-RPC 2.0 over WebSocket
- `console.py` — HTTP client for Console API
- `apps.py` — App management
- `revisions.py` — Deployment revisions
- `errors.py` — Custom exception classes
- `options.py` — Configuration

# API design

- MUST design pythonic APIs: snake_case, keyword arguments, no unnecessary classes.
- MUST be consistent with the existing API in this codebase. When unsure, read existing code first and ask the user.
- MUST NOT make breaking changes. If a breaking change would improve consistency, ask the user for permission first.
- MUST add tests for every bug fix and new feature. Place tests in `tests/test_<module>.py`.
- MUST implement every new feature for the async API first, then ensure the sync wrapper exposes it too. MUST add tests for both sync and async variants.

# Development

## Environment

- MUST use `uv` for all Python tooling (running scripts, installing packages, building, etc.). Do NOT use `pip`, `poetry`, `pipx`, or bare `python`.
- Tests hit the real Deno API (not mocked). Requires `DENO_DEPLOY_TOKEN` in `.env`.
- Python 3.10+.

## Running tests

```bash
uv run --env-file .env pytest
```

Run a specific test:

```bash
uv run --env-file .env pytest tests/test_revisions.py::test_revisions_get_async -xvs
```

## Test conventions

- Async tests: `test_<name>_async`, decorated with `@pytest.mark.asyncio(loop_scope="session")`
- Sync tests: `test_<name>_sync`
- Shared fixtures in `conftest.py`: `async_shared_sandbox`, `shared_sandbox`

## Code quality

IMPORTANT: Before finishing any task, MUST run both of these:

```bash
uv run ruff format
uv run ty check
```

## Releasing

Version is in `pyproject.toml`. Pushing a git tag `v<version>` triggers the publish workflow to PyPI.
