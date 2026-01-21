from __future__ import annotations

import base64
from contextlib import asynccontextmanager, contextmanager
from datetime import datetime, timedelta, timezone
import json
import os
from typing import (
    Any,
    AsyncIterable,
    AsyncIterator,
    BinaryIO,
    Iterable,
    Optional,
    TypedDict,
    Union,
    cast,
)
from typing_extensions import Literal, NotRequired, TypeAlias

from .stream import Streamable, complete_stream, start_stream, stream_data

from .api_generated import (
    AsyncSandboxEnv,
    AsyncSandboxFs as AsyncSandboxFsGenerated,
    SandboxEnv,
    SandboxFs as SandboxFsGenerated,
)
from .api_types_generated import (
    DenoReplOptions,
    DenoRunOptions,
    FsFileHandle,
    FsOpenOptions,
    ReadFileOptions,
    SandboxListOptions,
    SandboxCreateOptions,
    SandboxConnectOptions,
    SandboxMeta,
    SpawnOptions,
    WriteFileOptions,
)
from .bridge import AsyncBridge
from .console import (
    AsyncConsoleClient,
    AsyncPaginatedList,
    ConsoleClient,
    ExposeSSHResult,
    PaginatedList,
)
from .rpc import AsyncRpcClient, RpcClient
from .transport import (
    WebSocketTransport,
)
from .utils import (
    convert_to_camel_case,
    convert_to_snake_case,
    to_camel_case,
    to_snake_case,
)
from .wrappers import (
    AsyncChildProcess,
    AsyncDenoProcess,
    AsyncDenoRepl,
    AsyncFetchResponse,
    AsyncFsFile,
    ChildProcess,
    DenoProcess,
    DenoRepl,
    FetchResponse,
    FsFile,
    ProcessSpawnResult,
    RemoteProcessOptions,
)


Mode: TypeAlias = Literal["connect", "create"]
StdIo: TypeAlias = Literal["piped", "null"]


class SecretConfig(TypedDict):
    """List of hostnames where this secret can be used. Must have at least one host."""

    hosts: list[str]
    value: str


class VolumeInfo(TypedDict):
    volume: str
    path: str


class AppConfigVolume(TypedDict):
    volume: str


class AppConfig(TypedDict):
    stop_at_ms: NotRequired[int | None]
    labels: NotRequired[dict[str, str] | None]
    memory_mb: NotRequired[int | None]
    volumes: NotRequired[list[VolumeInfo] | None]
    allow_net: NotRequired[list[str] | None]
    root: NotRequired[AppConfigVolume | None]
    secrets: NotRequired[dict[str, SecretConfig] | None]


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
            yield Sandbox(self._client, rpc, async_handle)
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
            yield Sandbox(self._client, rpc, async_handle)
        except Exception:
            import sys

            self._bridge.run(async_cm.__aexit__(*sys.exc_info()))
            raise
        finally:
            self._bridge.run(async_cm.__aexit__(None, None, None))

    def list(
        self, options: SandboxListOptions
    ) -> PaginatedList[SandboxMeta, SandboxListOptions]:
        return self._client._sandboxes_list(options)


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

        config_dict: dict[str, Any] = {
            "memory_mb": 1280,
            "debug": options.get("debug", False) if options else False,
        }

        # Ensure null values are not included
        if options is not None:
            for k, v in options.items():
                if v is not None:
                    if k == "root":
                        config_dict["root"] = {"volume": v}
                    else:
                        config_dict[k] = v

        app_config = cast(AppConfig, config_dict)

        json_config = json.dumps(app_config, separators=(",", ":")).encode("utf-8")

        url = self._client._options["sandbox_ws_url"].join("/api/v3/sandboxes/create")
        token = self._client._options["token"]

        transport = WebSocketTransport()
        ws = await transport.connect(
            url=url,
            headers={
                "Authorization": f"Bearer {token}",
                "x-deno-sandbox-config": base64.b64encode(json_config).decode("utf-8"),
            },
        )

        response = ws.response
        if response is None:
            raise Exception("No response received")

        if response.headers is None:
            raise Exception("No response headers received")

        sandbox_id = response.headers.get("x-deno-sandbox-id")
        if sandbox_id is None:
            raise Exception("Sandbox ID not found in response headers")

        sandbox = None
        try:
            rpc = AsyncRpcClient(transport)
            sandbox = AsyncSandbox(self._client, rpc, sandbox_id)
            yield sandbox
        finally:
            if sandbox is not None:
                await sandbox.close()

    @asynccontextmanager
    async def connect(
        self, options: SandboxConnectOptions
    ) -> AsyncIterator[AsyncSandbox]:
        """Connects to an existing sandbox instance."""

        sandbox_id = options["id"]

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

        sandbox = None
        try:
            rpc = AsyncRpcClient(transport)
            sandbox = AsyncSandbox(self._client, rpc, sandbox_id)
            yield sandbox
        finally:
            if sandbox is not None:
                await sandbox.close()

    async def list(
        self, options: Optional[SandboxListOptions] = None
    ) -> AsyncPaginatedList[SandboxMeta, SandboxListOptions]:
        return await self._client._sandboxes_list(options)


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


class AsyncSandboxDeno:
    def __init__(
        self,
        client: AsyncConsoleClient,
        rpc: AsyncRpcClient,
        processes: list[AsyncChildProcess],
    ):
        self._client = client
        self._rpc = rpc
        self._processes = processes

    async def run(
        self,
        options: DenoRunOptions,
        stdin: Optional[Streamable] = None,
    ) -> AsyncDenoProcess:
        """Create a new Deno process from the specified entrypoint file or code. The runtime will execute the given code to completion, and then exit."""

        params = {
            "stdout": "inherit",
            "stderr": "inherit",
        }

        if options is not None:
            for key, value in options.items():
                if value is not None:
                    params[to_snake_case(key)] = value

        if "code" in params and "extension" not in params:
            params["extension"] = "ts"

        # If stdin data is provided, start stream first (but don't send data yet)
        stdin_writer = None
        if stdin is not None:
            params["stdin"] = "piped"
            stdin_stream_id, stdin_writer = await start_stream(self._rpc)
            params["stdinStreamId"] = stdin_stream_id

        opts = RemoteProcessOptions(
            stdout_inherit=params["stdout"] == "inherit",
            stderr_inherit=params["stderr"] == "inherit",
        )

        if params["stdout"] == "inherit":
            params["stdout"] = "piped"
        if params["stderr"] == "inherit":
            params["stderr"] = "piped"

        result = await self._rpc.call("spawnDeno", params)

        # Now that process is spawned, complete the stdin stream
        if stdin_writer is not None and stdin is not None:
            await complete_stream(stdin_writer, stdin)

        process = await AsyncDenoProcess.create(
            result, self._rpc, opts, self._processes
        )
        self._processes.append(process)
        return process

    async def eval(self, code: str) -> Any:
        repl = await self.repl()
        result = await repl.eval(code)
        await repl.close()
        return result

    # TODO: Support deploy method

    async def repl(self, options: Optional[DenoReplOptions] = None) -> AsyncDenoRepl:
        params = {"stdout": "piped", "stderr": "piped"}

        opts = RemoteProcessOptions(stdout_inherit=True, stderr_inherit=True)

        if options is not None:
            for key, value in options.items():
                if value is not None:
                    if key == "stdout" and value != "inherit":
                        opts["stdout_inherit"] = False
                    if key == "stderr" and value != "inherit":
                        opts["stderr_inherit"] = False

                    params[to_camel_case(key)] = value

        result: ProcessSpawnResult = await self._rpc.call("spawnDenoRepl", params)

        process = await AsyncDenoRepl.create(result, self._rpc, opts, self._processes)
        self._processes.append(process)
        return process


class SandboxDeno:
    def __init__(
        self,
        client: ConsoleClient,
        rpc: RpcClient,
        processes: list[AsyncChildProcess],
    ):
        self._client = client
        self._rpc = rpc

        self._async = AsyncSandboxDeno(
            self._client._async, rpc._async_client, processes
        )

    def run(
        self,
        options: DenoRunOptions,
        stdin: Optional[Union[Iterable[bytes], BinaryIO]] = None,
    ) -> DenoProcess:
        """
        Create a new Deno process from the specified entrypoint file or code. The runtime will execute the given code to completion, and then exit.
        """
        async_deno = self._client._bridge.run(self._async.run(options, stdin))
        return DenoProcess(self._rpc, async_deno)

    def eval(self, code: str) -> Any:
        return self._client._bridge.run(self._async.eval(code))

    def repl(self, options: Optional[DenoReplOptions] = None) -> DenoRepl:
        async_repl = self._client._bridge.run(self._async.repl(options))
        return DenoRepl(self._rpc, async_repl)


class AsyncSandbox:
    def __init__(
        self, client: AsyncConsoleClient, rpc: AsyncRpcClient, sandbox_id: str
    ):
        self._client = client
        self._rpc = rpc
        self._processes: list[AsyncChildProcess] = []

        self.url: str | None = None
        self.ssh: None = None
        self.id = sandbox_id
        self.fs = AsyncSandboxFs(client, rpc)
        self.deno = AsyncSandboxDeno(client, rpc, self._processes)
        self.env = AsyncSandboxEnv(client, rpc)

    @property
    def closed(self) -> bool:
        return self._rpc._transport.closed

    async def spawn(
        self,
        command: str,
        options: Optional[SpawnOptions] = None,
        stdin: Optional[Streamable] = None,
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

        # If stdin data is provided, start stream first (but don't send data yet)
        stdin_writer = None
        if stdin is not None:
            params["stdin"] = "piped"
            stdin_stream_id, stdin_writer = await start_stream(self._rpc)
            params["stdinStreamId"] = stdin_stream_id

        opts = RemoteProcessOptions(
            stdout_inherit=params["stdout"] == "inherit",
            stderr_inherit=params["stderr"] == "inherit",
        )

        if params["stdout"] == "inherit":
            params["stdout"] = "piped"
        if params["stderr"] == "inherit":
            params["stderr"] = "piped"

        result: ProcessSpawnResult = await self._rpc.call("spawn", params)

        # Now that process is spawned, complete the stdin stream
        if stdin_writer is not None and stdin is not None:
            await complete_stream(stdin_writer, stdin)

        process = await AsyncChildProcess.create(
            result, self._rpc, opts, self._processes
        )
        self._processes.append(process)
        return process

    async def fetch(
        self,
        url: str,
        method: Optional[str] = "GET",
        headers: Optional[dict[str, str]] = None,
        redirect: Optional[Literal["follow", "manual"]] = None,
    ) -> AsyncFetchResponse:
        return await self._rpc.fetch(url, method, headers, redirect)

    async def close(self) -> None:
        # Kill all tracked processes
        for process in self._processes:
            await process.kill()
        self._processes.clear()
        await self._rpc.close()

    async def kill(self) -> None:
        await self._client._kill_sandbox(self.id)

    async def extend_timeout(self, additional_s: int) -> datetime:
        """Request to extend the timeout of the sandbox by the specified duration.
        You can at max extend timeout of a sandbox by 30 minutes at once.

        Please note the extension is not guranteed to be the same as requested time.
        You should rely on the returned Date value to know the exact extension time.
        """

        now = datetime.now(timezone.utc)
        future_time = now + timedelta(seconds=additional_s)
        stop_at_ms = int(future_time.timestamp() * 1000)

        return await self._client._extend_timeout(self.id, stop_at_ms)

    async def expose_http(
        self, port: Optional[int] = None, pid: Optional[int] = None
    ) -> str:
        """Publicly expose a HTTP service via a publicly routeable URL.

        NOTE: when you call this API, the target HTTP service will be PUBLICLY
        EXPOSED WITHOUT AUTHENTICATION. Anyone with knowledge of the public domain
        will be able to send arbitrary requests to the exposed service.

        An exposed service can either be a service listening on an arbitrary HTTP
        port, or a JavaScript runtime that can handle HTTP requests.
        """

        if port is not None and pid is not None:
            raise ValueError("Only one of port or pid can be specified")

        params = {}
        if port is not None:
            params["port"] = port
        if pid is not None:
            params["pid"] = pid

        domain = await self._client._expose_http(self.id, params)

        params["domain"] = domain
        await self._rpc.call("exposeHttp", params)

        return f"https://{domain}"

    async def expose_ssh(self) -> ExposeSSHResult:
        """Expose an isolate over SSH, allowing access to the isolate's shell.

        NOTE: The SSH connection is authenticated through the 'username' field. This field is populated
        with a randomly generated, unique identifier. Anyone with knowledge of the 'username' can
        connect to the isolate's shell without further authentication.
        """

        return await self._client._expose_ssh(self.id)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


class Sandbox:
    def __init__(
        self, client: ConsoleClient, rpc: RpcClient, async_sandbox: AsyncSandbox
    ):
        self._client = client
        self._rpc = rpc
        self._async = async_sandbox

        self.url: str | None = None
        self.ssh: None = None
        self.id = async_sandbox.id
        self.fs = SandboxFs(client, rpc)
        self.deno = SandboxDeno(client, rpc, self._async._processes)
        self.env = SandboxEnv(client, rpc)

    @property
    def closed(self) -> bool:
        return self._rpc._async_client._transport.closed

    def spawn(
        self,
        command: str,
        options: Optional[SpawnOptions] = None,
        stdin: Optional[Union[Iterable[bytes], BinaryIO]] = None,
    ) -> ChildProcess:
        async_child = self._client._bridge.run(
            self._async.spawn(command, options, stdin)
        )
        return ChildProcess(self._rpc, async_child)

    def fetch(
        self,
        url: str,
        method: Optional[str] = "GET",
        headers: Optional[dict[str, str]] = None,
        redirect: Optional[Literal["follow", "manual"]] = None,
    ) -> FetchResponse:
        return self._rpc.fetch(url, method, headers, redirect, None)

    def close(self) -> None:
        self._client._bridge.run(self._async.close())

    def kill(self) -> None:
        self._client._bridge.run(self._async.kill())

    def extend_timeout(self, additional_s: int) -> datetime:
        """Request to extend the timeout of the sandbox by the specified duration.
        You can at max extend timeout of a sandbox by 30 minutes at once.

        Please note the extension is not guranteed to be the same as requested time.
        You should rely on the returned Date value to know the exact extension time.
        """
        return self._client._bridge.run(self._async.extend_timeout(additional_s))

    def expose_http(self, port: Optional[int] = None, pid: Optional[int] = None) -> str:
        """Publicly expose a HTTP service via a publicly routeable URL.

        NOTE: when you call this API, the target HTTP service will be PUBLICLY
        EXPOSED WITHOUT AUTHENTICATION. Anyone with knowledge of the public domain
        will be able to send arbitrary requests to the exposed service.

        An exposed service can either be a service listening on an arbitrary HTTP
        port, or a JavaScript runtime that can handle HTTP requests.
        """
        return self._client._bridge.run(self._async.expose_http(port=port, pid=pid))

    def expose_ssh(self) -> ExposeSSHResult:
        """Expose an isolate over SSH, allowing access to the isolate's shell.

        NOTE: The SSH connection is authenticated through the 'username' field. This field is populated
        with a randomly generated, unique identifier. Anyone with knowledge of the 'username' can
        connect to the isolate's shell without further authentication.
        """
        return self._client._bridge.run(self._async.expose_ssh())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._client._bridge.run(self._async.__aexit__(exc_type, exc_val, exc_tb))


class AsyncSandboxFs(AsyncSandboxFsGenerated):
    """Filesystem operations inside the sandbox."""

    async def read_file(
        self, path: str, options: Optional[ReadFileOptions] = None
    ) -> bytes:
        """Reads the entire contents of a file as bytes."""

        params: dict[str, Any] = {"path": path}
        if options is not None:
            params["options"] = convert_to_camel_case(options)

        result = await self._rpc.call("readFile", params)

        # Server returns base64-encoded data
        return base64.b64decode(result)

    async def create(self, path: str) -> AsyncFsFile:
        """Create a new, empty file at the specified path."""

        params = {"path": path}
        result = await self._rpc.call("create", params)

        raw_result = convert_to_snake_case(result)
        handle = cast(FsFileHandle, raw_result)

        return AsyncFsFile(self._rpc, handle["file_handle_id"])

    async def open(
        self, path: str, options: Optional[FsOpenOptions] = None
    ) -> AsyncFsFile:
        """Open a file and return a file descriptor."""

        params = {"path": path}
        if options is not None:
            params["options"] = convert_to_camel_case(options)

        result = await self._rpc.call("open", params)

        raw_result = convert_to_snake_case(result)
        handle = cast(FsFileHandle, raw_result)

        return AsyncFsFile(self._rpc, handle["file_handle_id"])

    async def write_file(
        self,
        path: str,
        data: Union[bytes, AsyncIterable[bytes], Iterable[bytes], BinaryIO],
        options: Optional[WriteFileOptions] = None,
    ) -> None:
        """Write bytes to file. Accepts bytes, async/sync iterables, or file objects."""

        if isinstance(data, bytes):
            # Stream bytes as a single chunk
            content_stream_id = await stream_data(self._rpc, iter([data]))
        else:
            # Stream data from iterable/file object
            content_stream_id = await stream_data(self._rpc, data)

        params: dict[str, Any] = {"path": path, "contentStreamId": content_stream_id}
        if options is not None:
            params["options"] = convert_to_camel_case(options)
        await self._rpc.call("writeFile", params)

    async def upload(self, local_path: str, sandbox_path: str) -> None:
        """Upload a file, directory, or symlink from local filesystem to the sandbox.

        Recursively uploads directories and their contents.
        Preserves symlinks by creating corresponding symlinks in the sandbox.
        """
        await self._upload_item(local_path, sandbox_path)

    async def _upload_item(self, local_path: str, sandbox_path: str) -> None:
        """Internal method to upload a single item (file, directory, or symlink)."""
        if os.path.islink(local_path):
            # It's a symlink - read the target and create a symlink in sandbox
            target = os.readlink(local_path)
            await self.symlink(target, sandbox_path)
        elif os.path.isdir(local_path):
            # It's a directory - create it and recursively upload contents
            await self.mkdir(sandbox_path, {"recursive": True})
            for entry in os.listdir(local_path):
                entry_local_path = os.path.join(local_path, entry)
                entry_sandbox_path = f"{sandbox_path}/{entry}"
                await self._upload_item(entry_local_path, entry_sandbox_path)
        elif os.path.isfile(local_path):
            # It's a file - stream it to write_file
            with open(local_path, "rb") as f:
                await self.write_file(sandbox_path, f)
        else:
            raise FileNotFoundError(f"Local path does not exist: {local_path}")


class SandboxFs(SandboxFsGenerated):
    """Filesystem operations inside the sandbox."""

    def read_file(self, path: str, options: Optional[ReadFileOptions] = None) -> bytes:
        """Reads the entire contents of a file as bytes."""

        params: dict[str, Any] = {"path": path}
        if options is not None:
            params["options"] = convert_to_camel_case(options)

        result = self._rpc.call("readFile", params)

        # Server returns base64-encoded data
        return base64.b64decode(result)

    def create(self, path: str) -> FsFile:
        """Create a new, empty file at the specified path."""

        params = {"path": path}
        result = self._rpc.call("create", params)

        raw_result = convert_to_snake_case(result)
        handle = cast(FsFileHandle, raw_result)

        return FsFile(self._rpc, handle["file_handle_id"])

    def open(self, path: str, options: Optional[FsOpenOptions] = None) -> FsFile:
        """Open a file and return a file descriptor."""

        params = {"path": path}
        if options is not None:
            params["options"] = convert_to_camel_case(options)

        result = self._rpc.call("open", params)

        raw_result = convert_to_snake_case(result)
        handle = cast(FsFileHandle, raw_result)

        return FsFile(self._rpc, handle["file_handle_id"])

    def write_file(
        self,
        path: str,
        data: Union[bytes, Iterable[bytes], BinaryIO],
        options: Optional[WriteFileOptions] = None,
    ) -> None:
        """Write bytes to file. Accepts bytes, sync iterables, or file objects."""

        if isinstance(data, bytes):
            # Stream bytes as a single chunk
            content_stream_id = self._client._bridge.run(
                stream_data(self._rpc._async_client, iter([data]))
            )
        else:
            # Stream data from iterable/file object
            content_stream_id = self._client._bridge.run(
                stream_data(self._rpc._async_client, data)
            )

        params: dict[str, Any] = {"path": path, "contentStreamId": content_stream_id}
        if options is not None:
            params["options"] = convert_to_camel_case(options)
        self._rpc.call("writeFile", params)

    def upload(self, local_path: str, sandbox_path: str) -> None:
        """Upload a file, directory, or symlink from local filesystem to the sandbox.

        Recursively uploads directories and their contents.
        Preserves symlinks by creating corresponding symlinks in the sandbox.
        """
        self._upload_item(local_path, sandbox_path)

    def _upload_item(self, local_path: str, sandbox_path: str) -> None:
        """Internal method to upload a single item (file, directory, or symlink)."""
        if os.path.islink(local_path):
            # It's a symlink - read the target and create a symlink in sandbox
            target = os.readlink(local_path)
            self.symlink(target, sandbox_path)
        elif os.path.isdir(local_path):
            # It's a directory - create it and recursively upload contents
            self.mkdir(sandbox_path, {"recursive": True})
            for entry in os.listdir(local_path):
                entry_local_path = os.path.join(local_path, entry)
                entry_sandbox_path = f"{sandbox_path}/{entry}"
                self._upload_item(entry_local_path, entry_sandbox_path)
        elif os.path.isfile(local_path):
            # It's a file - stream it to write_file
            with open(local_path, "rb") as f:
                self.write_file(sandbox_path, f)
        else:
            raise FileNotFoundError(f"Local path does not exist: {local_path}")


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

    def wait(self):
        # FIXME
        pass

    async def kill(self) -> None:
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.kill()
        await self.wait()


class VsCode:
    """Experimental! A VSCode instance running inside the sandbox."""

    def __init__(self, rpc: RpcClient, async_vscode: AsyncVsCode):
        self._rpc = rpc
        self._async = async_vscode

    @property
    def stdout(self):
        # FIXME
        pass

    @property
    def stderr(self):
        # FIXME
        pass

    def wait(self):
        # FIXME
        pass

    async def kill(self) -> None:
        self._rpc._bridge.run(self._async.kill())

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.kill()
        await self.wait()
