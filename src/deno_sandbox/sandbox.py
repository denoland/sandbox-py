import asyncio
import base64
from contextlib import asynccontextmanager, contextmanager
import json
import sys
from typing import (
    Any,
    AsyncIterator,
    BinaryIO,
    NotRequired,
    Optional,
    TypedDict,
    cast,
)
from typing_extensions import Literal

from deno_sandbox.api_generated import (
    AsyncSandboxDeno,
    AsyncSandboxEnv,
    AsyncSandboxFs,
    SandboxDeno,
    SandboxEnv,
    SandboxFs,
)
from deno_sandbox.api_types_generated import (
    SandboxListOptions,
    SandboxCreateOptions,
    SandboxConnectOptions,
    SandboxMeta,
    SpawnOptions,
)
from deno_sandbox.bridge import AsyncBridge
from deno_sandbox.console import AsyncConsoleClient, ConsoleClient
from deno_sandbox.rpc import AsyncRpcClient, RpcClient
from deno_sandbox.transport import (
    WebSocketTransport,
)
from deno_sandbox.utils import to_snake_case
from deno_sandbox.wrappers import AbortSignal


type Mode = Literal["connect", "create"]
type StdIo = Literal["piped", "null"]


class SecretConfig(TypedDict):
    """List of hostnames where this secret can be used. Must have at least one host."""

    hosts: list[str]
    value: str


class VolumeInfo(TypedDict):
    volume: str
    path: str


class ChildProcessStatus(TypedDict):
    """Whether the subprocess exited successfully, i.e. with a zero exit code."""

    success: bool
    """The exit code of the subprocess. Negative values indicate that the process was killed by a signal."""
    code: int
    """The signal that caused the process to exit, if any. If the process exited normally, this will be `null`."""
    signal: AbortSignal | None


class AppConfig(TypedDict):
    stop_at_ms: NotRequired[int | None]
    labels: NotRequired[dict[str, str] | None]
    memory_mb: NotRequired[int | None]
    volumes: NotRequired[list[VolumeInfo] | None]
    allow_net: NotRequired[list]
    secrets: NotRequired[dict[str, SecretConfig] | None]


class ProcessSpawnResult(TypedDict):
    pid: int
    stdout_stream_id: int
    stderr_stream_id: int


class ProcessWaitResult(TypedDict):
    success: bool
    code: int
    signal: AbortSignal | None


class SandboxApi:
    def __init__(self, client: ConsoleClient, bridge: AsyncBridge):
        self._bridge = bridge
        self._client = client
        self._async_sandbox = AsyncSandboxApi(self._client._async)

    @contextmanager
    def create(self, options: Optional[SandboxCreateOptions] = None):
        async_cm = self._async_sandbox.create(options)
        async_handle = self._bridge.run(async_cm.__aenter__())

        rpc = RpcClient(async_handle._rpc, self._bridge)

        try:
            yield Sandbox(self._client, rpc, async_handle.id)
        except Exception:
            import sys

            self._bridge.run(async_cm.__aexit__(*sys.exc_info()))
            raise
        finally:
            self._bridge.run(async_cm.__aexit__(None, None, None))

    @contextmanager
    def connect(self, options: SandboxConnectOptions):
        async_cm = self._async_sandbox.connect(options)
        async_handle = self._bridge.run(async_cm.__aenter__())

        rpc = RpcClient(async_handle._rpc, self._bridge)

        try:
            yield Sandbox(self._client, rpc, async_handle.id)
        except Exception:
            import sys

            self._bridge.run(async_cm.__aexit__(*sys.exc_info()))
            raise
        finally:
            self._bridge.run(async_cm.__aexit__(None, None, None))

    def list(self, options: SandboxListOptions) -> list[SandboxMeta]:
        return self._client.sandboxes_list(options)


class AsyncSandboxApi:
    def __init__(
        self,
        client: AsyncConsoleClient,
    ):
        self._client = client

    @asynccontextmanager
    async def create(
        self, options: Optional[SandboxCreateOptions] = None
    ) -> AsyncIterator[AsyncSandbox]:
        """Creates a new sandbox instance."""

        app_config: AppConfig = {
            "memory_mb": 1280,
        }

        # Ensure null values are not included
        if options is not None:
            for k, v in options.items():
                if v is not None:
                    if k == "root":
                        app_config["root"] = {"volume": v}
                    else:
                        app_config[k] = v

        json_config = json.dumps(app_config, separators=(",", ":")).encode("utf-8")

        url = self._client._options["sandbox_ws_url"].join("/api/v3/sandboxes/create")
        token = self._client._options["token"]

        transport = WebSocketTransport()
        await transport.connect(
            url=url,
            headers={
                "Authorization": f"Bearer {token}",
                "x-deno-sandbox-config": base64.b64encode(json_config).decode("utf-8"),
            },
        )

        sandbox_id = transport._ws.response.headers.get("x-deno-sandbox-id")

        try:
            rpc = AsyncRpcClient(transport)
            yield AsyncSandbox(self._client, rpc, sandbox_id)
        finally:
            await transport.close()

    @asynccontextmanager
    async def connect(self, sandbox_id: str) -> AsyncIterator[AsyncSandbox]:
        """Connects to an existing sandbox instance."""

        url = self._client._options["sandbox_ws_url"].join(
            f"/api/v3/sandbox/{sandbox_id}/connect"
        )
        token = self._client._options["token"]
        transport = WebSocketTransport()
        await transport.connect(
            url=url,
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        try:
            rpc = AsyncRpcClient(transport)
            yield AsyncSandbox(self._client, rpc, sandbox_id)
        finally:
            await transport.close()

    async def list(
        self, options: Optional[SandboxListOptions] = None
    ) -> list[SandboxMeta]:
        return await self._client.sandboxes_list(options)


class RemoteProcessOptions(TypedDict):
    stdout_inherit: bool
    stderr_inherit: bool


class AsyncChildProcess:
    def __init__(
        self,
        pid: int,
        stdout: asyncio.StreamReader,
        stderr: asyncio.StreamReader,
        wait_task: asyncio.Task,
    ):
        self.pid = pid
        self.stdout = stdout
        self.stderr = stderr
        self._wait_task = wait_task
        self.returncode = None

    @classmethod
    async def create(
        cls, res: ProcessSpawnResult, rpc: AsyncRpcClient, options: RemoteProcessOptions
    ) -> AsyncChildProcess:
        pid = res["pid"]

        stdout = asyncio.StreamReader()
        stderr = asyncio.StreamReader()

        rpc._pending_processes[res["stdout_stream_id"]] = stdout
        rpc._pending_processes[res["stderr_stream_id"]] = stderr

        wait_task = rpc._loop.create_task(rpc.call("processWait", {"pid": pid}))

        instance = cls(pid, stdout, stderr, wait_task)

        if options.get("stdout_inherit"):
            rpc._loop.create_task(instance._pipe_stream(stdout, sys.stdout.buffer))
        if options.get("stderr_inherit"):
            rpc._loop.create_task(instance._pipe_stream(stderr, sys.stderr.buffer))

        return instance

    @property
    async def status(self) -> ChildProcessStatus:
        raw = await self._wait_task
        result = cast(ProcessWaitResult, raw)
        return ChildProcessStatus(
            success=result["success"], code=result["code"], signal=result["signal"]
        )

    async def _pipe_stream(self, reader: asyncio.StreamReader, writer: BinaryIO):
        """Helper to pump data from the StreamReader to a local binary stream."""
        try:
            while not reader.at_eof():
                data = await reader.read(1024)
                if not data:
                    break

                writer.write(data)
                writer.flush()
        except Exception:
            # Handle potential connection drops or closed pipes silently
            pass


class SyncStreamReader:
    """Wraps asyncio.StreamReader to provide synchronous read methods."""

    def __init__(self, bridge: AsyncBridge, reader: asyncio.StreamReader):
        self._bridge = bridge
        self._reader = reader

    def read(self, n: int = -1) -> bytes:
        return self._bridge.run(self._reader.read(n))

    def readline(self) -> bytes:
        return self._bridge.run(self._reader.readline())

    def readexactly(self, n: int) -> bytes:
        return self._bridge.run(self._reader.readexactly(n))


class ChildProcess:
    def __init__(
        self,
        rpc: RpcClient,
        async_proc: AsyncChildProcess,
    ):
        self._rpc = rpc

        self._async_proc = async_proc
        self.stdout = SyncStreamReader(rpc._bridge, self._async_proc.stdout)
        self.stderr = SyncStreamReader(rpc._bridge, self._async_proc.stderr)
        self.returncode: int | None = None

    @property
    def pid(self) -> int:
        return self._async_proc.pid

    @property
    def status(self) -> ChildProcessStatus:
        return self._rpc._bridge.run(self._async_proc.status)


class VsCodeOptions(TypedDict):
    env: NotRequired[dict[str, str] | None]
    """Environment variables to pass to the VS Code instance."""

    extensions: NotRequired[list[str] | None]
    """
    The extensions to be loaded in the VSCode instance.
   
    The accepted values are:
    - an extension id
    - Coder extension marketplace
    - path to a .vsix file
    """

    preview: NotRequired[bool | None]
    """A URL of a page to load a preview window of inside the VSCode instance."""

    disable_stop_button: NotRequired[bool | None]
    """If true, the stop button in the VSCode instance will be disabled. Default: false"""

    editor_settings: NotRequired[dict[str, Any] | None]
    """The value for the default settings.json that VSCode will use."""


class AsyncSandbox:
    def __init__(
        self, client: AsyncConsoleClient, rpc: AsyncRpcClient, sandbox_id: str
    ):
        self._client = client
        self._rpc = rpc

        self.url: str | None = None
        self.ssh: None = None
        self.id = sandbox_id
        self.fs = AsyncSandboxFs(client, rpc)
        self.deno = AsyncSandboxDeno(client, rpc)
        self.env = AsyncSandboxEnv(client, rpc)

    @property
    def closed(self) -> bool:
        return self._rpc._transport.closed

    async def spawn(
        self, command: str, options: Optional[SpawnOptions] = None
    ) -> AsyncChildProcess:
        params = {
            "command": command,
            "stdout": "inherit",
            "stderr": "inherit",
        }

        if options is not None:
            for key, value in options.items():
                if value is not None:
                    params[to_snake_case(key)] = value

        opts = RemoteProcessOptions(
            stdout_inherit=params["stdout"] == "inherit",
            stderr_inherit=params["stderr"] == "inherit",
        )

        if params["stdout"] == "inherit":
            params["stdout"] = "piped"
        if params["stderr"] == "inherit":
            params["stderr"] = "piped"

        result: ProcessSpawnResult = await self._rpc.call("spawn", params)
        return await AsyncChildProcess.create(result, self._rpc, opts)

    # FIXME
    async def fetch() -> Any:
        pass

    async def close(self) -> None:
        await self._rpc.close()

    async def kill(self) -> None:
        pass

    async def extend_timeout(self, additional_s: int) -> None:
        pass

    async def expose_http(self, portOrPid: int) -> str:
        pass

    async def expose_ssh(self, portOrPid: int) -> str:
        pass

    async def expose_vscode(
        self, path: Optional[str] = None, options: Optional[VsCodeOptions] = None
    ) -> AsyncVsCode:
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


class Sandbox:
    def __init__(self, client: ConsoleClient, rpc: RpcClient, sandbox_id: str):
        self._client = client
        self._rpc = rpc
        self._async = AsyncSandbox(self._client._async, rpc._async_client, sandbox_id)

        self.url: str | None = None
        self.ssh: None = None
        self.id = sandbox_id
        self.fs = SandboxFs(client, rpc)
        self.deno = SandboxDeno(client, rpc)
        self.env = SandboxEnv(client, rpc)

    @property
    def closed(self) -> bool:
        return self._rpc._async_client._transport.closed

    def spawn(
        self, command: str, options: Optional[SpawnOptions] = None
    ) -> ChildProcess:
        async_child = self._client._bridge.run(self._async.spawn(command, options))
        return ChildProcess(self._rpc, async_child)

    # FIXME
    def fetch() -> Any:
        pass

    def close(self) -> None:
        self._client._bridge.run(self._async.close())

    def kill(self) -> None:
        self._client._bridge.run(self._async.kill())

    def extend_timeout(self, additional_s: int) -> None:
        self._client._bridge.run(self._async.extend_timeout(additional_s))

    def expose_http(self, port_or_pid: int) -> str:
        self._client._bridge.run(self._async.expose_http(port_or_pid))

    def expose_ssh(self, port_or_pid: int) -> str:
        self._client._bridge.run(self._async.expose_ssh(port_or_pid))

    def expose_vscode(
        self, path: Optional[str] = None, options: Optional[VsCodeOptions] = None
    ) -> VsCode:
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._client._bridge.run(self._async.__aexit__(exc_type, exc_val, exc_tb))


class AsyncVsCode:
    """Experimental! A VSCode instance running inside the sandbox."""

    def __init__(self, rpc: RpcClient, url: str):
        self._rpc = rpc
        self.url = url

    @property
    def stdout(self):
        # FIXME
        pass

    @property
    def stderr(self):
        # FIXME
        pass

    @property
    def status(self):
        # FIXME
        pass

    async def kill(self) -> None:
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.kill()
        await self.status


class VsCode:
    """Experimental! A VSCode instance running inside the sandbox."""

    def __init__(self, rpc: RpcClient, url: str):
        self._rpc = rpc
        self.url = url

    @property
    def stdout(self):
        # FIXME
        pass

    @property
    def stderr(self):
        # FIXME
        pass

    @property
    def status(self):
        # FIXME
        pass

    async def kill(self) -> None:
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.kill()
        await self.status
