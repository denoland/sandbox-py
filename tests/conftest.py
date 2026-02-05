import pytest

from deno_sandbox import AsyncDenoDeploy, DenoDeploy


@pytest.fixture(scope="session")
async def async_shared_sandbox():
    sdk = AsyncDenoDeploy()

    async with sdk.sandbox.create(debug=True) as sandbox:
        yield sandbox


@pytest.fixture(scope="session")
def shared_sandbox():
    sdk = DenoDeploy()

    with sdk.sandbox.create(debug=True) as sandbox:
        yield sandbox


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):  # noqa: ARG001
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Check for sandbox fixtures
        for name in ("async_shared_sandbox", "shared_sandbox"):
            if name in item.funcargs:
                sandbox = item.funcargs[name]
                if hasattr(sandbox, "trace_id") and sandbox.trace_id:
                    print(f"\nTrace ID: {sandbox.trace_id}")
                break
