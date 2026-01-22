from __future__ import annotations

import base64
import os
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncIterable,
    BinaryIO,
    Iterable,
    Optional,
    Union,
    cast,
)

from .api_types_generated import (
    DirEntry,
    ExpandGlobOptions,
    FileInfo,
    FsFileHandle,
    FsOpenOptions,
    MakeTempDirOptions,
    MakeTempFileOptions,
    MkdirOptions,
    ReadFileOptions,
    RemoveOptions,
    SymlinkOptions,
    WalkEntry,
    WalkOptions,
    WriteFileOptions,
)
from .stream import stream_data
from .utils import convert_to_camel_case, convert_to_snake_case

if TYPE_CHECKING:
    from .console import AsyncConsoleClient, ConsoleClient
    from .rpc import AsyncRpcClient, RpcClient


class AsyncFsFile:
    def __init__(self, rpc: AsyncRpcClient, fd: int):
        self._rpc = rpc
        self._fd = fd

    async def write(self, data: bytes) -> int:
        """Write data to the file. Returns number of bytes written."""

        result = await self._rpc.call(
            "fileWrite",
            {"data": base64.b64encode(data).decode("ascii"), "fileHandleId": self._fd},
        )
        return result["bytes_written"]

    async def truncate(self, size: Optional[int]) -> None:
        """Truncate the file to the given size. If size is None, truncate to 0."""

        await self._rpc.call("fileTruncate", {"size": size, "fileHandleId": self._fd})

    async def read(self, size: int) -> bytes:
        """Read up to size bytes from the file. Returns the data read."""

        result = await self._rpc.call(
            "fileRead", {"length": size, "fileHandleId": self._fd}
        )
        return base64.b64decode(result["data"])

    async def seek(self, offset: int, whence: int) -> int:
        """Seek to a position in the file. Returns the new position."""

        result = await self._rpc.call(
            "fileSeek", {"offset": offset, "whence": whence, "fileHandleId": self._fd}
        )
        return result["position"]

    async def stat(self) -> FileInfo:
        """Get file information."""

        result = await self._rpc.call("fileStat", {"fileHandleId": self._fd})
        return cast(FileInfo, result)

    async def sync(self) -> None:
        """Flushes any pending data and metadata operations of the given file stream to disk."""

        await self._rpc.call("fileSync", {"fileHandleId": self._fd})

    async def sync_data(self) -> None:
        """Sync the file's data to disk."""

        await self._rpc.call("fileSyncData", {"fileHandleId": self._fd})

    async def utime(self, atime: float, mtime: float) -> None:
        """Update the file's access and modification times."""

        await self._rpc.call(
            "fileUtime",
            {"atime": atime, "mtime": mtime, "fileHandleId": self._fd},
        )

    async def lock(self, exclusive: Optional[bool]) -> None:
        """Lock the file. If exclusive is True, acquire an exclusive lock."""

        await self._rpc.call(
            "fileLock", {"exclusive": exclusive, "fileHandleId": self._fd}
        )

    async def unlock(self) -> None:
        """Unlock the file."""

        await self._rpc.call("fileUnlock", {"fileHandleId": self._fd})

    async def close(self) -> None:
        """Close the file."""

        await self._rpc.call("fileClose", {"fileHandleId": self._fd})

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


class FsFile:
    def __init__(self, rpc: RpcClient, fd: int):
        self._rpc = rpc
        self._async = AsyncFsFile(rpc._async_client, fd)

    def write(self, data: bytes) -> int:
        """Write data to the file. Returns number of bytes written."""

        return self._rpc._bridge.run(self._async.write(data))

    def truncate(self, size: Optional[int]) -> None:
        """Truncate the file to the given size. If size is None, truncate to 0."""

        return self._rpc._bridge.run(self._async.truncate(size))

    def read(self, size: int) -> bytes:
        """Read up to size bytes from the file. Returns the data read."""

        return self._rpc._bridge.run(self._async.read(size))

    def seek(self, offset: int, whence: int) -> int:
        """Seek to a position in the file. Returns the new position."""

        return self._rpc._bridge.run(self._async.seek(offset, whence))

    def stat(self) -> FileInfo:
        """Get file information."""

        return self._rpc._bridge.run(self._async.stat())

    def sync(self) -> None:
        """Flushes any pending data and metadata operations of the given file stream to disk."""

        return self._rpc._bridge.run(self._async.sync())

    def sync_data(self) -> None:
        """Sync the file's data to disk."""

        return self._rpc._bridge.run(self._async.sync_data())

    def utime(self, atime: int, mtime: int) -> None:
        """Update the file's access and modification times."""

        return self._rpc._bridge.run(self._async.utime(atime, mtime))

    def lock(self, exclusive: Optional[bool]) -> None:
        """Lock the file. If exclusive is True, acquire an exclusive lock."""

        return self._rpc._bridge.run(self._async.lock(exclusive))

    def unlock(self) -> None:
        """Unlock the file."""

        return self._rpc._bridge.run(self._async.unlock())

    def close(self) -> None:
        """Close the file."""

        return self._rpc._bridge.run(self._async.close())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class AsyncSandboxFs:
    """Filesystem operations inside the sandbox."""

    def __init__(self, client: AsyncConsoleClient, rpc: AsyncRpcClient):
        self._client = client
        self._rpc = rpc

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

    async def read_text_file(
        self, path: str, options: Optional[ReadFileOptions] = None
    ) -> str:
        """Reads the entire contents of a file as an UTF-8 decoded string."""

        params = {"path": path}
        if options is not None:
            params["options"] = convert_to_camel_case(options)

        result = await self._rpc.call("readTextFile", params)

        return result

    async def write_text_file(
        self, path: str, content: str, options: Optional[WriteFileOptions] = None
    ) -> None:
        """Write text to file. Creates a new file if needed. Existing files will be overwritten."""

        params = {"path": path, "content": content}
        if options is not None:
            params["options"] = convert_to_camel_case(options)

        await self._rpc.call("writeTextFile", params)

    async def read_dir(self, path: str) -> list[DirEntry]:
        """Read the directory entries at the given path."""

        params = {"path": path}
        result = await self._rpc.call("readDir", params)

        return result

    async def remove(self, path: str, options: Optional[RemoveOptions] = None) -> None:
        """Remove the file or directory at the given path."""

        params = {"path": path}
        if options is not None:
            params["options"] = convert_to_camel_case(options)

        await self._rpc.call("remove", params)

    async def mkdir(self, path: str, options: Optional[MkdirOptions] = None) -> None:
        """Create a new directory at the specified path."""

        params = {"path": path}
        if options is not None:
            params["options"] = convert_to_camel_case(options)

        await self._rpc.call("mkdir", params)

    async def rename(self, old_path: str, new_path: str) -> None:
        """Rename (move) a file or directory."""

        params = {"oldPath": old_path, "newPath": new_path}
        await self._rpc.call("rename", params)

    async def stat(self, path: str) -> FileInfo:
        """Return file information about a file or directory."""

        params = {"path": path}
        result = await self._rpc.call("stat", params)

        raw_result = convert_to_snake_case(result)
        return cast(FileInfo, raw_result)

    async def chmod(self, path: str, mode: int) -> None:
        """Change the permission mode of a file or directory."""

        params = {"path": path, "mode": mode}
        await self._rpc.call("chmod", params)

    async def chown(
        self, path: str, uid: Optional[int] = None, gid: Optional[int] = None
    ) -> None:
        """Change the owner user ID and group ID of a file or directory."""

        params = {"path": path, "uid": uid, "gid": gid}
        await self._rpc.call("chown", params)

    async def copy_file(self, from_path: str, to_path: str) -> None:
        """Copy a file from a source path to a destination path."""

        params = {"fromPath": from_path, "toPath": to_path}
        await self._rpc.call("copyFile", params)

    async def walk(
        self, path: str, options: Optional[WalkOptions] = None
    ) -> list[WalkEntry]:
        """Recursively walk a directory tree."""

        params = {"path": path}
        if options is not None:
            params["options"] = convert_to_camel_case(options)

        result = await self._rpc.call("walk", params)

        return result

    async def expand_glob(
        self, glob: str, options: Optional[ExpandGlobOptions] = None
    ) -> list[str]:
        """Expand a glob pattern to a list of paths."""

        params = {"glob": glob}
        if options is not None:
            params["options"] = convert_to_camel_case(options)

        result = await self._rpc.call("expandGlob", params)

        return result

    async def link(self, target: str, path: str) -> None:
        """Create a hard link pointing to an existing file."""

        params = {"target": target, "path": path}
        await self._rpc.call("link", params)

    async def lstat(self, path: str) -> FileInfo:
        """Return file information about a file or directory symlink."""

        params = {"path": path}
        result = await self._rpc.call("lstat", params)

        raw_result = convert_to_snake_case(result)
        return cast(FileInfo, raw_result)

    async def make_temp_dir(self, options: Optional[MakeTempDirOptions] = None) -> str:
        """Create a new temporary directory."""

        params = {}
        if options is not None:
            params["options"] = convert_to_camel_case(options)

        result = await self._rpc.call("makeTempDir", params)

        return result

    async def make_temp_file(
        self, options: Optional[MakeTempFileOptions] = None
    ) -> str:
        """Create a new temporary file."""

        params = {}
        if options is not None:
            params["options"] = convert_to_camel_case(options)

        result = await self._rpc.call("makeTempFile", params)

        return result

    async def read_link(self, path: str) -> str:
        """Read the target of a symbolic link."""

        params = {"path": path}
        result = await self._rpc.call("readLink", params)

        return result

    async def real_path(self, path: str) -> str:
        """Return the canonicalized absolute pathname."""

        params = {"path": path}
        result = await self._rpc.call("realPath", params)

        return result

    async def symlink(
        self, target: str, path: str, options: Optional[SymlinkOptions] = None
    ) -> None:
        """Create a symbolic link."""

        params = {"target": target, "path": path}
        if options is not None:
            params["options"] = convert_to_camel_case(options)

        await self._rpc.call("symlink", params)

    async def truncate(self, name: str, length: Optional[int] = None) -> None:
        """Truncate or extend the specified file to reach a given size."""

        params = {"name": name, "length": length}
        await self._rpc.call("truncate", params)

    async def umask(self, mask: Optional[int] = None) -> int:
        """Sets the process's file mode creation mask."""

        params = {"mask": mask}
        result = await self._rpc.call("umask", params)

        return result

    async def utime(self, path: str, atime: str, mtime: str) -> None:
        """Change the access and modification times of a file."""

        params = {"path": path, "atime": atime, "mtime": mtime}
        await self._rpc.call("utime", params)

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

    async def download(self, local_path: str, sandbox_path: str) -> None:
        """Download a file or directory from the sandbox."""

        params = {"localPath": local_path, "sandboxPath": sandbox_path}
        await self._rpc.call("download", params)

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


class SandboxFs:
    """Filesystem operations inside the sandbox."""

    def __init__(self, client: ConsoleClient, rpc: RpcClient):
        self._client = client
        self._rpc = rpc

    def read_file(self, path: str, options: Optional[ReadFileOptions] = None) -> bytes:
        """Reads the entire contents of a file as bytes."""

        params: dict[str, Any] = {"path": path}
        if options is not None:
            params["options"] = convert_to_camel_case(options)

        result = self._rpc.call("readFile", params)

        # Server returns base64-encoded data
        return base64.b64decode(result)

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

    def read_text_file(
        self, path: str, options: Optional[ReadFileOptions] = None
    ) -> str:
        """Reads the entire contents of a file as an UTF-8 decoded string."""

        params = {"path": path}
        if options is not None:
            params["options"] = convert_to_camel_case(options)

        result = self._rpc.call("readTextFile", params)

        return result

    def write_text_file(
        self, path: str, content: str, options: Optional[WriteFileOptions] = None
    ) -> None:
        """Write text to file. Creates a new file if needed. Existing files will be overwritten."""

        params = {"path": path, "content": content}
        if options is not None:
            params["options"] = convert_to_camel_case(options)

        self._rpc.call("writeTextFile", params)

    def read_dir(self, path: str) -> list[DirEntry]:
        """Read the directory entries at the given path."""

        params = {"path": path}
        result = self._rpc.call("readDir", params)

        return result

    def remove(self, path: str, options: Optional[RemoveOptions] = None) -> None:
        """Remove the file or directory at the given path."""

        params = {"path": path}
        if options is not None:
            params["options"] = convert_to_camel_case(options)

        self._rpc.call("remove", params)

    def mkdir(self, path: str, options: Optional[MkdirOptions] = None) -> None:
        """Create a new directory at the specified path."""

        params = {"path": path}
        if options is not None:
            params["options"] = convert_to_camel_case(options)

        self._rpc.call("mkdir", params)

    def rename(self, old_path: str, new_path: str) -> None:
        """Rename (move) a file or directory."""

        params = {"oldPath": old_path, "newPath": new_path}
        self._rpc.call("rename", params)

    def stat(self, path: str) -> FileInfo:
        """Return file information about a file or directory."""

        params = {"path": path}
        result = self._rpc.call("stat", params)

        raw_result = convert_to_snake_case(result)
        return cast(FileInfo, raw_result)

    def chmod(self, path: str, mode: int) -> None:
        """Change the permission mode of a file or directory."""

        params = {"path": path, "mode": mode}
        self._rpc.call("chmod", params)

    def chown(
        self, path: str, uid: Optional[int] = None, gid: Optional[int] = None
    ) -> None:
        """Change the owner user ID and group ID of a file or directory."""

        params = {"path": path, "uid": uid, "gid": gid}
        self._rpc.call("chown", params)

    def copy_file(self, from_path: str, to_path: str) -> None:
        """Copy a file from a source path to a destination path."""

        params = {"fromPath": from_path, "toPath": to_path}
        self._rpc.call("copyFile", params)

    def walk(self, path: str, options: Optional[WalkOptions] = None) -> list[WalkEntry]:
        """Recursively walk a directory tree."""

        params = {"path": path}
        if options is not None:
            params["options"] = convert_to_camel_case(options)

        result = self._rpc.call("walk", params)

        return result

    def expand_glob(
        self, glob: str, options: Optional[ExpandGlobOptions] = None
    ) -> list[str]:
        """Expand a glob pattern to a list of paths."""

        params = {"glob": glob}
        if options is not None:
            params["options"] = convert_to_camel_case(options)

        result = self._rpc.call("expandGlob", params)

        return result

    def link(self, target: str, path: str) -> None:
        """Create a hard link pointing to an existing file."""

        params = {"target": target, "path": path}
        self._rpc.call("link", params)

    def lstat(self, path: str) -> FileInfo:
        """Return file information about a file or directory symlink."""

        params = {"path": path}
        result = self._rpc.call("lstat", params)

        raw_result = convert_to_snake_case(result)
        return cast(FileInfo, raw_result)

    def make_temp_dir(self, options: Optional[MakeTempDirOptions] = None) -> str:
        """Create a new temporary directory."""

        params = {}
        if options is not None:
            params["options"] = convert_to_camel_case(options)

        result = self._rpc.call("makeTempDir", params)

        return result

    def make_temp_file(self, options: Optional[MakeTempFileOptions] = None) -> str:
        """Create a new temporary file."""

        params = {}
        if options is not None:
            params["options"] = convert_to_camel_case(options)

        result = self._rpc.call("makeTempFile", params)

        return result

    def read_link(self, path: str) -> str:
        """Read the target of a symbolic link."""

        params = {"path": path}
        result = self._rpc.call("readLink", params)

        return result

    def real_path(self, path: str) -> str:
        """Return the canonicalized absolute pathname."""

        params = {"path": path}
        result = self._rpc.call("realPath", params)

        return result

    def symlink(
        self, target: str, path: str, options: Optional[SymlinkOptions] = None
    ) -> None:
        """Create a symbolic link."""

        params = {"target": target, "path": path}
        if options is not None:
            params["options"] = convert_to_camel_case(options)

        self._rpc.call("symlink", params)

    def truncate(self, name: str, length: Optional[int] = None) -> None:
        """Truncate or extend the specified file to reach a given size."""

        params = {"name": name, "length": length}
        self._rpc.call("truncate", params)

    def umask(self, mask: Optional[int] = None) -> int:
        """Sets the process's file mode creation mask."""

        params = {"mask": mask}
        result = self._rpc.call("umask", params)

        return result

    def utime(self, path: str, atime: str, mtime: str) -> None:
        """Change the access and modification times of a file."""

        params = {"path": path, "atime": atime, "mtime": mtime}
        self._rpc.call("utime", params)

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

    def download(self, local_path: str, sandbox_path: str) -> None:
        """Download a file or directory from the sandbox."""

        params = {"localPath": local_path, "sandboxPath": sandbox_path}
        self._rpc.call("download", params)

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
