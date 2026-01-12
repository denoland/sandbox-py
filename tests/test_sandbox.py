import pytest

from deno_sandbox.sandbox import AsyncSandbox
from deno_sandbox.api_generated import WriteTextFileWithContent


@pytest.mark.asyncio
async def test_create_sandbox_async() -> None:
    sandbox = AsyncSandbox()

    async with sandbox.create() as sb:
        assert sb is not None

        await sb.fs.write_text_file(
            WriteTextFileWithContent(path="foo.txt", content="foo")
        )
        content = await sb.fs.read_text_file(path="foo.txt")
        assert content == "foo"
