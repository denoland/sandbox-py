import asyncio
import base64
from contextlib import asynccontextmanager, contextmanager
import json
import sys
from typing import (
    Any,
    AsyncIterator,
    BinaryIO,
    Generator,
    NotRequired,
    Optional,
    TypedDict,
    cast,
)
from typing_extensions import Literal

from deno_sandbox.api_generated import (
    AsyncSandboxDenoCli,
    AsyncSandboxEnv,
    AsyncSandboxFs,
    AsyncSandboxNet,
    AsyncSandboxVSCode,
    AsyncSandboxProcess as GeneratedAsyncSandboxProcess,
    SandboxProcess as GeneratedSandboxProcess,
    SandboxDenoCli,
    SandboxEnv,
    SandboxFs,
    SandboxNet,
    SandboxVSCode,
)
from deno_sandbox.api_types_generated import (
    ProcessSpawnResult,
    ProcessWaitResult,
    SandboxListOptions,
    SandboxCreateOptions,
    SandboxConnectOptions,
    SandboxMeta,
    SpawnArgs,
)
from deno_sandbox.bridge import AsyncBridge
from deno_sandbox.console import ConsoleClient
from deno_sandbox.options import Options, get_internal_options
from deno_sandbox.rpc import AsyncRpcClient, RpcClient
from deno_sandbox.transport import (
    WebSocketTransport,
)


type Mode = Literal["connect", "create"]
type StdIo = Literal["piped", "null"]


class SecretConfig(TypedDict):
    """List of hostnames where this secret can be used. Must have at least one host."""

    hosts: list[str]
    value: str


class VolumeInfo(TypedDict):
    volume: str
    path: str


class AppConfig(TypedDict):
    stop_at_ms: NotRequired[int | None]
    labels: NotRequired[dict[str, str] | None]
    memory_mb: NotRequired[int | None]
    volumes: NotRequired[list[VolumeInfo] | None]
    allow_net: NotRequired[list]
    secrets: NotRequired[dict[str, SecretConfig] | None]


class Sandbox:
    def __init__(self, options: Options | None = None):
        self.__options = get_internal_options(options or Options())
        self._client = ConsoleClient(options)
        self._bridge = AsyncBridge()
        self._async_sandbox = AsyncSandboxHandle(self.__options)

    @contextmanager
    def create(self, options: Optional[SandboxCreateOptions]):
        async_cm = self._async_sandbox.create(options)
        async_handle = self._bridge.run(async_cm.__aenter__())

        rpc = RpcClient(async_handle._rpc, self._bridge)

        try:
            yield SandboxHandle(rpc, async_handle.id)
        finally:
            self._bridge.run(async_cm.__aexit__(None, None, None))

    def list(self, options: SandboxListOptions) -> list[SandboxMeta]:
        result = self._client.sandboxes_list(options.to_dict())
        return [cast(SandboxMeta, i) for i in result]

    def close(self):
        self._bridge.stop()


class AsyncSandboxWrapper:
    def __init__(
        self,
        options: Optional[Options] = None,
    ):
        self._options = get_internal_options(options)
        self._rpc: AsyncRpcClient | None = None

    @asynccontextmanager
    async def create(
        self, options: Optional[SandboxCreateOptions] = None
    ) -> AsyncIterator[AsyncSandboxHandle]:
        """Creates a new sandbox instance."""

        app_config: AppConfig = {
            "memory_mb": 1280,
        }

        # Ensure null values are not included
        if options is not None:
            for k, v in options.items():
                if v is not None:
                    app_config[k] = v

        json_config = json.dumps(app_config, separators=(",", ":")).encode("utf-8")

        url = f"{self._options['sandbox_ws_url']}api/v3/sandboxes/create"
        transport = WebSocketTransport()
        await transport.connect(
            url=url,
            headers={
                "Authorization": f"Bearer {self._options['token']}",
                "x-deno-sandbox-config": base64.b64encode(json_config).decode("utf-8"),
            },
        )

        sandbox_id = transport._ws.response.headers.get("x-deno-sandbox-id")

        try:
            self._rpc = AsyncRpcClient(transport)
            yield AsyncSandboxHandle(self._rpc, sandbox_id)
        finally:
            await transport.close()

    @asynccontextmanager
    async def connect(self, sandbox_id: str) -> AsyncIterator[AsyncSandboxHandle]:
        """Connects to an existing sandbox instance."""

        url = f"{self._options['sandbox_ws_url']}api/v3/sandbox/{sandbox_id}/connect"
        transport = WebSocketTransport()
        await transport.connect(
            url=url,
            headers={
                "Authorization": f"Bearer {self._options['token']}",
            },
        )

        try:
            rpc = AsyncRpcClient(transport)
            yield AsyncSandboxHandle(rpc, sandbox_id)
        finally:
            await transport.close()

    async def list(
        self, options: Optional[SandboxListOptions] = None
    ) -> list[SandboxMeta]:
        return await self._client.sandboxes_list(options)


class AsyncSandboxProcess(GeneratedAsyncSandboxProcess):
    async def spawn(self, args: SpawnArgs) -> AsyncRemoteProcess:
        options: RemoteProcessOptions = {
            "stdout_inherit": args.get("stdout", "inherit") == "inherit",
            "stderr_inherit": args.get("stderr", "inherit") == "inherit",
        }

        if args.get("stdout") is None:
            args["stdout"] = "piped"
        if args.get("stderr") is None:
            args["stderr"] = "piped"

        result: ProcessSpawnResult = await super().spawn(args)
        return await AsyncRemoteProcess.create(result, self._rpc, options)


class SandboxProcess(GeneratedSandboxProcess):
    def spawn(self, args: SpawnArgs) -> RemoteProcess:
        options: RemoteProcessOptions = {
            "stdout_inherit": args.get("stdout", "inherit") == "inherit",
            "stderr_inherit": args.get("stderr", "inherit") == "inherit",
        }

        if args.get("stdout") is None:
            args["stdout"] = "piped"
        if args.get("stderr") is None:
            args["stderr"] = "piped"

        result: ProcessSpawnResult = super().spawn(args)
        async_proc = self._rpc._bridge.run(
            AsyncRemoteProcess.create(result, self._rpc._async_client, options)
        )
        return RemoteProcess(result, self._rpc, async_proc)


class RemoteProcessOptions(TypedDict):
    stdout_inherit: bool
    stderr_inherit: bool


class AsyncRemoteProcess:
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
    ) -> AsyncRemoteProcess:
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

    async def wait(self) -> int:
        raw = await self._wait_task
        result = cast(ProcessWaitResult, raw)
        self.returncode = result["code"]
        return self.returncode

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


class RemoteProcess:
    def __init__(
        self,
        res: ProcessSpawnResult,
        rpc: RpcClient,
        async_proc: AsyncRemoteProcess,
    ):
        self.pid = res["pid"]
        self._rpc = rpc

        self._async_proc = async_proc
        self.stdout = SyncStreamReader(rpc._bridge, self._async_proc.stdout)
        self.stderr = SyncStreamReader(rpc._bridge, self._async_proc.stderr)
        self.returncode: int | None = None

    def wait(self) -> int:
        result = self._rpc._bridge.run(self._async_proc.wait())
        self.returncode = self._async_proc.returncode
        return result


class AsyncSandboxHandle:
    def __init__(self, rpc: AsyncRpcClient, sandbox_id: str):
        self._rpc = rpc
        self.id = sandbox_id
        self.fs = AsyncSandboxFs(rpc)
        self.net = AsyncSandboxNet(rpc)
        self.deno = AsyncSandboxDenoCli(rpc)
        self.vscode = AsyncSandboxVSCode(rpc)
        self.env = AsyncSandboxEnv(rpc)
        self.process = AsyncSandboxProcess(rpc)

    async def abort(self) -> None:
        await self._rpc.call("abort", {"abortId": self.id})


class SandboxHandle:
    def __init__(self, rpc: RpcClient, sandbox_id: str):
        self._rpc = rpc
        self.id = sandbox_id
        self.fs = SandboxFs(rpc)
        self.net = SandboxNet(rpc)
        self.deno = SandboxDenoCli(rpc)
        self.vscode = SandboxVSCode(rpc)
        self.env = SandboxEnv(rpc)
        self.process = SandboxProcess(rpc)

    def abort(self) -> None:
        self._rpc.call("abort", {"abortId": self.id})


class SandboxWrapper:
    def __init__(self, options: Optional[Options] = None):
        self._bridge = AsyncBridge()
        self._async_sandbox = AsyncSandboxWrapper(options)

    @contextmanager
    def create(
        self, options: Optional[SandboxCreateOptions] = None
    ) -> Generator[SandboxHandle, Any, Any]:
        async_cm = self._async_sandbox.create(options)
        async_handle = self._bridge.run(async_cm.__aenter__())

        rpc = RpcClient(async_handle._rpc, self._bridge)

        try:
            yield SandboxHandle(rpc, async_handle.id)
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
            yield SandboxHandle(rpc, async_handle.id)
        except Exception:
            import sys

            self._bridge.run(async_cm.__aexit__(*sys.exc_info()))
            raise
        finally:
            self._bridge.run(async_cm.__aexit__(None, None, None))

    def list(self, options: SandboxListOptions) -> list[SandboxMeta]:
        return self._client.sandboxes_list(options)

    def close(self):
        self._bridge.stop()
