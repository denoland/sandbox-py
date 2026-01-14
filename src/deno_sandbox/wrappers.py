from typing import Optional, cast
from deno_sandbox.api_types_generated import FileInfo
from deno_sandbox.rpc import AsyncRpcClient, RpcClient


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


class DenoProcess:
    pass


class AsyncDenoProcess:
    pass


class DenoRepl:
    pass


class AsyncDenoRepl:
    pass
