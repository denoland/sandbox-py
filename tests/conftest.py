import os

import pytest

from deno_sandbox import AsyncDenoDeploy, DenoDeploy

# Test modules that run fully offline (no DENO_DEPLOY_TOKEN, no live sandbox).
# Every other module drives a real backend, so it is skipped when no token is
# available (e.g. in CI); a local run that sets DENO_DEPLOY_TOKEN still runs the
# whole suite. NB: a new offline test in a module not listed here is silently
# skipped in CI — add its module name to this set so it actually runs.
HERMETIC_TEST_MODULES = {"test_utils", "test_console_errors", "test_timeline_pin"}


def pytest_collection_modifyitems(config, items):  # noqa: ARG001
    if os.environ.get("DENO_DEPLOY_TOKEN"):
        return
    skip_live = pytest.mark.skip(
        reason="requires DENO_DEPLOY_TOKEN (live sandbox backend)"
    )
    for item in items:
        module_name = item.module.__name__.rsplit(".", 1)[-1]
        if module_name not in HERMETIC_TEST_MODULES:
            item.add_marker(skip_live)


@pytest.fixture(scope="module")
async def async_shared_sandbox():
    sdk = AsyncDenoDeploy()

    async with sdk.sandbox.create(debug=True) as sandbox:
        yield sandbox


@pytest.fixture(scope="module")
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
