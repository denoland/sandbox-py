import asyncio
import sys
from typing import Any, BinaryIO, Optional, TypedDict, cast
from typing_extensions import Literal
from deno_sandbox.bridge import AsyncBridge
from deno_sandbox.errors import HTTPStatusError, ProcessAlreadyExited
from deno_sandbox.rpc import AsyncRpcClient, RpcClient


class FileInfo(TypedDict):
    is_file: bool
    is_directory: bool
    is_symlink: bool
    size: int
    mtime: str
    atime: str
    birthtime: str
    ctime: str
    dev: int
    ino: int
    mode: int
    nlink: int
    uid: int
    gid: int
    rdev: int
    blksize: int
    blocks: int
    is_block_device: bool
    is_char_device: bool
    is_fifo: bool
    is_socket: bool


class AbortSignal:
    pass


class AsyncFsFile:
    def __init__(self, rpc: AsyncRpcClient, fd: int):
        self._rpc = rpc
        self._fd = fd

    async def write(self, data: bytes) -> int:
        """Write data to the file. Returns number of bytes written."""

        result = await self._rpc.call(
            "fileWrite", {"data": data, "fileHandleId": self.fd}
        )
        return result["bytesWritten"]

    async def truncate(self, size: Optional[int]) -> None:
        """Truncate the file to the given size. If size is None, truncate to 0."""

        await self._rpc.call("fileTruncate", {"size": size, "fileHandleId": self.fd})

    async def read(self, size: int) -> bytes:
        """Read up to size bytes from the file. Returns the data read."""

        result = await self._rpc.call(
            "fileRead", {"length": size, "fileHandleId": self.fd}
        )
        return result

    async def seek(self, offset: int, whence: int) -> int:
        """Seek to a position in the file. Returns the new position."""

        result = await self._rpc.call(
            "fileSeek", {"offset": offset, "whence": whence, "fileHandleId": self.fd}
        )
        return result["position"]

    async def stat(self) -> FileInfo:
        """Get file information."""

        result = await self._rpc.call("fileStat", {"fileHandleId": self.fd})
        return cast(FileInfo, result)

    async def flush(self) -> None:
        """Flush the file's internal buffer."""

        await self._rpc.call("fileFlush", {"fileHandleId": self.fd})

    async def syncData(self) -> None:
        """Sync the file's data to disk."""

        await self._rpc.call("fileSyncData", {"fileHandleId": self.fd})

    async def utime(self, atime: float, mtime: float) -> None:
        """Update the file's access and modification times."""

        await self._rpc.call(
            "fileUtime",
            {"atime": atime, "mtime": mtime, "fileHandleId": self.fd},
        )

    async def lock(self, exclusive: Optional[bool]) -> None:
        """Lock the file. If exclusive is True, acquire an exclusive lock."""

        await self._rpc.call(
            "fileLock", {"exclusive": exclusive, "fileHandleId": self.fd}
        )

    async def unlock(self) -> None:
        """Unlock the file."""

        await self._rpc.call("fileUnlock", {"fileHandleId": self.fd})

    async def close(self) -> None:
        """Close the file."""

        await self._rpc.call("fileClose", {"fileHandleId": self.fd})

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


class FsFile:
    def __init__(self, rpc: RpcClient, fd: int):
        self._rpc = rpc
        self._fd = fd
        self._async = AsyncFsFile(rpc._async_client, fd)

    def write(self, data: bytes) -> int:
        """Write data to the file. Returns number of bytes written."""

        return self._bridge.run(self._async.write(data))

    async def truncate(self, size: Optional[int]) -> None:
        """Truncate the file to the given size. If size is None, truncate to 0."""

        return self._bridge.run(self._async.truncate(size))

    async def read(self, size: int) -> bytes:
        """Read up to size bytes from the file. Returns the data read."""

        return self._bridge.run(self._async.read(size))

    async def seek(self, offset: int, whence: int) -> int:
        """Seek to a position in the file. Returns the new position."""

        return self._bridge.run(self._async.seek(offset, whence))

    async def stat(self) -> FileInfo:
        """Get file information."""

        return self._bridge.run(self._async.stat())

    async def flush(self) -> None:
        """Flush the file's internal buffer."""

        return self._bridge.run(self._async.flush())

    async def syncData(self) -> None:
        """Sync the file's data to disk."""

        return self._bridge.run(self._async.syncData())

    async def utime(self, atime: float, mtime: float) -> None:
        """Update the file's access and modification times."""

        return self._bridge.run(self._async.seek(atime, mtime))

    async def lock(self, exclusive: Optional[bool]) -> None:
        """Lock the file. If exclusive is True, acquire an exclusive lock."""

        return self._bridge.run(self._async.lock(exclusive))

    async def unlock(self) -> None:
        """Unlock the file."""

        return self._bridge.run(self._async.unlock())

    async def close(self) -> None:
        """Close the file."""

        return self._bridge.run(self._async.close())

    async def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class RemoteProcessOptions(TypedDict):
    stdout_inherit: bool
    stderr_inherit: bool


class ProcessSpawnResult(TypedDict):
    pid: int
    stdout_stream_id: int
    stderr_stream_id: int


class ProcessWaitResult(TypedDict):
    success: bool
    code: int
    signal: AbortSignal | None


class ChildProcessStatus(TypedDict):
    """Whether the subprocess exited successfully, i.e. with a zero exit code."""

    success: bool
    """The exit code of the subprocess. Negative values indicate that the process was killed by a signal."""
    code: int
    """The signal that caused the process to exit, if any. If the process exited normally, this will be `null`."""
    signal: AbortSignal | None


class AsyncChildProcess:
    def __init__(
        self,
        pid: int,
        stdout: asyncio.StreamReader,
        stderr: asyncio.StreamReader,
        wait_task: asyncio.Task,
        rpc: AsyncRpcClient,
    ):
        self.pid = pid
        self.stdout = stdout
        self.stderr = stderr
        self._wait_task = wait_task
        self.returncode = None
        self._rpc = rpc
        self._stdout_task: Optional[asyncio.Task] = None
        self._stderr_task: Optional[asyncio.Task] = None

    @classmethod
    async def create(
        cls, res: ProcessSpawnResult, rpc: AsyncRpcClient, options: RemoteProcessOptions
    ) -> AsyncChildProcess:
        return create_process_like(cls, res, rpc, options)

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

    async def kill(self) -> None:
        """Kill the process."""

        try:
            await self._rpc.call("processKill", {"pid": self.pid})
        except ProcessAlreadyExited:
            # Process already exited
            pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.kill()


def create_process_like[T](
    cls: T, res: ProcessSpawnResult, rpc: AsyncRpcClient, options: RemoteProcessOptions
) -> T:
    pid = res["pid"]

    stdout = asyncio.StreamReader()
    stderr = asyncio.StreamReader()

    rpc._pending_processes[res["stdout_stream_id"]] = stdout
    rpc._pending_processes[res["stderr_stream_id"]] = stderr

    wait_task = rpc._loop.create_task(rpc.call("processWait", {"pid": pid}))

    instance = cls(pid, stdout, stderr, wait_task, rpc)

    if options.get("stdout_inherit"):
        instance._stdout_task = rpc._loop.create_task(
            instance._pipe_stream(stdout, sys.stdout.buffer)
        )
    if options.get("stderr_inherit"):
        instance._stderr_task = rpc._loop.create_task(
            instance._pipe_stream(stderr, sys.stderr.buffer)
        )

    return instance


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

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._rpc._bridge.run(self._async_proc.__aexit__(exc_type, exc_val, exc_tb))


class AsyncDenoProcess(AsyncChildProcess):
    def __init__(self, pid, stdout, stderr, wait_task, rpc):
        super().__init__(pid, stdout, stderr, wait_task, rpc)
        self._listening_task: asyncio.Task | None = None

    @classmethod
    async def create(
        cls, res: ProcessSpawnResult, rpc: AsyncRpcClient, options: RemoteProcessOptions
    ) -> AsyncDenoProcess:
        p = create_process_like(cls, res, rpc, options)

        p._listening_task = rpc._loop.create_task(
            rpc.call("denoHttpWait", {"pid": p.pid})
        )
        return p

    async def wait_http_ready(self) -> bool:
        """Whether the Deno process is ready to accept HTTP requests."""

        if self._listening_task is not None:
            return await self._listening_task

        return False

    async def fetch(
        self,
        url: str,
        method: Optional[str] = "GET",
        headers: Optional[dict[str, str]] = None,
        redirect: Literal["follow", "manual"] = None,
    ) -> AsyncFetchResponse:
        """Fetch a URL from the Deno process."""

        abort_id = self._rpc.get_next_signal_id()

        params: FetchParams = {
            "method": method,
            "url": url,
            "redirect": redirect or "follow",
            "pid": self.pid,
            "abortId": abort_id,
        }

        if headers is not None:
            params["headers"] = list(headers.items())
        else:
            params["headers"] = []

        response: FetchResponseData = await self._rpc.call("fetch", params)
        return AsyncFetchResponse(rpc=self._rpc, response=response)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._listening_task is not None:
            self._listening_task.cancel()
        await super().__aexit__(exc_type, exc_val, exc_tb)


class DenoProcess(ChildProcess):
    def __init__(
        self,
        rpc: RpcClient,
        async_proc: AsyncChildProcess,
    ):
        super().__init__(rpc, async_proc)

    def wait_http_ready(self) -> bool:
        """Whether the Deno process is ready to accept HTTP requests."""

        return self._rpc._bridge.run(self._async_proc.wait_http_ready())

    def fetch(
        self,
        url: str,
        method: Optional[str] = "GET",
        headers: Optional[dict[str, str]] = None,
        redirect: Literal["follow", "manual"] = None,
    ) -> FetchResponse:
        """Fetch a URL from the Deno process."""

        result = self._rpc._bridge.run(
            self._async_proc.fetch(url, method, headers, redirect)
        )

        return FetchResponse(self._rpc, result)


class AsyncDenoRepl(AsyncChildProcess):
    @classmethod
    async def create(
        cls, res: ProcessSpawnResult, rpc: AsyncRpcClient, options: RemoteProcessOptions
    ) -> AsyncDenoRepl:
        return create_process_like(cls, res, rpc, options)

    async def eval(self, code: str) -> str:
        """Evaluate code in the REPL and return the output."""

        result = await self._rpc.call("denoReplEval", {"code": code, "pid": self.pid})

        return result

    async def call(self, fn: str, args: list[Any]) -> Any:
        """Call a function in the REPL process."""

        result = await self._rpc.call(
            "denoReplCall", {"pid": self.pid, "fn": fn, "args": args}
        )

        return result

    async def close(self) -> None:
        """Close the REPL process."""

        await self._rpc.call("denoReplClose", {"pid": self.pid})
        self._wait_task.cancel()
        self._stdout_task.cancel()
        self._stderr_task.cancel()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


class DenoRepl:
    def __init__(
        self,
        rpc: RpcClient,
        async_proc: AsyncDenoRepl,
    ):
        self._rpc = rpc

        self._async = async_proc
        self.stdout = SyncStreamReader(rpc._bridge, self._async.stdout)
        self.stderr = SyncStreamReader(rpc._bridge, self._async.stderr)
        self.returncode: int | None = None

    def eval(self, code: str) -> str:
        """Evaluate code in the REPL and return the output."""

        return self._rpc._bridge.run(self._async.eval(code))

    def call(self, fn: str, args: list[Any]) -> Any:
        """Call a function in the REPL process."""

        return self._rpc._bridge.run(self._async.call(fn, args))

    def close(self) -> None:
        """Close the REPL process."""

        self._rpc._bridge.run(self._async.close())

    @property
    def pid(self) -> int:
        return self._async.pid

    @property
    def status(self) -> ChildProcessStatus:
        return self._rpc._bridge.run(self._async.status)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._rpc._bridge.run(self._async.__aexit__(exc_type, exc_val, exc_tb))


class FetchParams(TypedDict):
    method: str
    url: str
    headers: list[tuple[str, str]]
    redirect: str
    pid: int
    abortId: int


class FetchResponseData(TypedDict):
    status: int
    status_text: str
    headers: list[tuple[str, str]]
    body_stream_id: int


class AsyncFetchResponse:
    def __init__(self, rpc: AsyncRpcClient, response: FetchResponseData):
        self._rpc = rpc
        self._response = response

    def raise_for_status(self) -> HTTPStatusError | None:
        if self.is_success:
            return

        message = "{self} resulted in a {error_type} (status code: {self.status})"
        status_class = self.status // 100
        error_types = {
            1: "Informational response",
            3: "Redirect response",
            4: "Client error",
            5: "Server error",
        }
        error_type = error_types.get(status_class, "Invalid status code")
        message = message.format(self, error_type=error_type)

        return HTTPStatusError(self.status, message)

    @property
    def headers(self) -> dict[str, str]:
        return {k: v for k, v in self._response["headers"]}

    @property
    def status_code(self) -> int:
        return self._response["status"]

    @property
    def is_informational(self) -> int:
        return 100 <= self.status_code <= 199

    @property
    def is_success(self) -> int:
        return 200 <= self.status_code <= 299

    @property
    def is_redirect(self) -> int:
        return 300 <= self.status_code <= 399

    @property
    def is_client_error(self) -> int:
        return 400 <= self.status_code <= 499

    @property
    def is_server_error(self) -> int:
        return 500 <= self.status_code <= 599

    @property
    def is_error(self) -> int:
        return 400 <= self.status_code <= 599

    @property
    def has_redirect_location(self) -> bool:
        return (
            self.status_code in (301, 302, 303, 307, 308)
            and "location" in self._response["headers"]
        )

    async def cancel(self) -> None:
        await self._rpc.call("abort", {"abortId": self._response["abortId"]})

    def __repr__(self) -> str:
        return f"<Response [{self.status_code}]>"


class FetchResponse(AsyncFetchResponse):
    def __init__(self, rpc: AsyncRpcClient, async_res: AsyncFetchResponse):
        self._rpc = rpc
        self._async = async_res

    def raise_for_status(self) -> HTTPStatusError | None:
        return self._async.raise_for_status()

    @property
    def status_code(self) -> int:
        return self._async.status_code

    @property
    def is_informational(self) -> int:
        return self._async.is_informational

    @property
    def is_success(self) -> int:
        return self._async.is_success

    @property
    def is_redirect(self) -> int:
        return self._async.is_redirect

    @property
    def is_client_error(self) -> int:
        return self._async.is_client_error

    @property
    def is_server_error(self) -> int:
        return self._async.is_server_error

    @property
    def is_error(self) -> int:
        return self._async.is_error

    @property
    def has_redirect_location(self) -> bool:
        return self._async.has_redirect_location

    def cancel(self) -> None:
        self._rpc._bridge.run(self._async.cancel())

    def __repr__(self) -> str:
        return f"<Response [{self.status_code}]>"
