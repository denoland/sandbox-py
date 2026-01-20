# Deno Sandbox Python SDK

Create isolated [Deno sandboxes](https://deno.com/deploy/sandboxes) to run code
in a lightweight Linux microVM. You can securely run shell scripts, spawn
processes, execute JavaScript applications and REPLs, and interact with files
remotely.

This Python SDK let's you create and manage sandboxes programmatically.

## Installation

```sh
uv add deno-sandbox
```

## Quick Start

Sync:

```py
from deno_sandbox import DenoDeploy

def main()
  sdk = DenoDeploy()

  with sdk.sandbox.create() as sb
    child_process = sb.spawn("npx", {
      "args": [
        "cowsay",
        "hello"
      ]
    })

    await p.wait()

if __name__ == "__main__"
  main()
```

Async:

```py
from deno_sandbox import AsyncDenoDeploy

async def main()
  sdk = AsyncDenoDeploy()

  async with sdk.sandbox.create() as sb
    child_process = await sb.spawn("npx", {
      "args": [
        "cowsay",
        "hello"
      ]
    })

    await p.wait()

if __name__ == "__main__"
  asyncio.run(main())
```

## License

`MIT`, see the [LICENSE file](./LICENSE)
