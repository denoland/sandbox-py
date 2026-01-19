import pytest

from deno_sandbox import AsyncDenoDeploy, DenoDeploy


@pytest.fixture(scope="session")
async def async_shared_sandbox():
    sdk = AsyncDenoDeploy()

    async with sdk.sandbox.create({"debug": True}) as sandbox:
        yield sandbox


@pytest.fixture(scope="session")
def shared_sandbox():
    sdk = DenoDeploy()

    with sdk.sandbox.create() as sandbox:
        yield sandbox
