# ATTENTION: This file is auto-generated. Do not edit it manually.

from typing import cast, Any
from typing_extensions import Optional
from deno_sandbox.api_types_generated import (
    App,
    AppListOptions,
    PaginatedList,
    AppInit,
    AppUpdate,
    Timeline,
    Revision,
    RevisionListOptions,
    RevisionWithoutTimelines,
    TimelineListOptions,
    VolumeInit,
    Volume,
    VolumeListOptions,
    ReadFileOptions,
    WriteFileOptions,
    DirEntry,
    RemoveOptions,
    MkdirOptions,
    WalkOptions,
    WalkEntry,
    ExpandGlobOptions,
    MakeTempDirOptions,
    MakeTempFileOptions,
    FsOpenOptions,
    SymlinkOptions,
    DenoRunOptions,
    DenoReplOptions,
    DeployOptions,
)

from deno_sandbox.rpc import RpcClient, AsyncRpcClient
from deno_sandbox.utils import convert_to_camel_case, convert_to_snake_case
from deno_sandbox.console import AsyncConsoleClient, ConsoleClient
from deno_sandbox.wrappers import (
    FileInfo,
    FsFile,
    AsyncFsFile,
    DenoProcess,
    AsyncDenoProcess,
    DenoRepl,
    AsyncDenoRepl,
)


class Apps:
    def __init__(self, client: ConsoleClient):
        self._client = client

    def get(self, id_or_slug: str) -> App:
        """Get an app by its ID or slug."""

        result = self._client._apps_get(id_or_slug)

        raw_result = convert_to_snake_case(result)
        return cast(App, raw_result)

    def list(self, options: Optional[AppListOptions] = None) -> PaginatedList[App]:
        """List apps of an org."""

        result = self._client._apps_list(options)

        raw_result = convert_to_snake_case(result)
        return cast(PaginatedList[App], raw_result)

    def create(self, options: AppInit) -> App:
        """Create a new app."""

        result = self._client._apps_create(options)

        raw_result = convert_to_snake_case(result)
        return cast(App, raw_result)

    def update(self, app: str, update: AppUpdate) -> App:
        """Update an existing app."""

        result = self._client._apps_update(app, update)

        raw_result = convert_to_snake_case(result)
        return cast(App, raw_result)

    def delete(self, app: str) -> None:
        """Delete an app by its ID or slug."""

        self._client._apps_delete(app)


class AsyncApps:
    def __init__(self, client: AsyncConsoleClient):
        self._client = client

    async def get(self, id_or_slug: str) -> App:
        """Get an app by its ID or slug."""

        result = await self._client._apps_get(id_or_slug)

        raw_result = convert_to_snake_case(result)
        return cast(App, raw_result)

    async def list(
        self, options: Optional[AppListOptions] = None
    ) -> PaginatedList[App]:
        """List apps of an org."""

        result = await self._client._apps_list(options)

        raw_result = convert_to_snake_case(result)
        return cast(PaginatedList[App], raw_result)

    async def create(self, options: AppInit) -> App:
        """Create a new app."""

        result = await self._client._apps_create(options)

        raw_result = convert_to_snake_case(result)
        return cast(App, raw_result)

    async def update(self, app: str, update: AppUpdate) -> App:
        """Update an existing app."""

        result = await self._client._apps_update(app, update)

        raw_result = convert_to_snake_case(result)
        return cast(App, raw_result)

    async def delete(self, app: str) -> None:
        """Delete an app by its ID or slug."""

        await self._client._apps_delete(app)


class Revisions:
    def __init__(self, client: ConsoleClient):
        self._client = client

    def get(self, app: str, id: str) -> Revision:
        """Get a revision by its ID for a specific app."""

        result = self._client._revisions_get(app, id)

        raw_result = convert_to_snake_case(result)
        return cast(Revision, raw_result)

    def list(
        self, app: str, options: Optional[RevisionListOptions] = None
    ) -> PaginatedList[RevisionWithoutTimelines]:
        """List revisions for a specific app."""

        result = self._client._revisions_list(app, options)

        raw_result = convert_to_snake_case(result)
        return cast(PaginatedList[RevisionWithoutTimelines], raw_result)


class AsyncRevisions:
    def __init__(self, client: AsyncConsoleClient):
        self._client = client

    async def get(self, app: str, id: str) -> Revision:
        """Get a revision by its ID for a specific app."""

        result = await self._client._revisions_get(app, id)

        raw_result = convert_to_snake_case(result)
        return cast(Revision, raw_result)

    async def list(
        self, app: str, options: Optional[RevisionListOptions] = None
    ) -> PaginatedList[RevisionWithoutTimelines]:
        """List revisions for a specific app."""

        result = await self._client._revisions_list(app, options)

        raw_result = convert_to_snake_case(result)
        return cast(PaginatedList[RevisionWithoutTimelines], raw_result)


class Timelines:
    def __init__(self, client: ConsoleClient):
        self._client = client

    def list(
        self, app: str, options: Optional[TimelineListOptions] = None
    ) -> PaginatedList[Timeline]:
        """List timelines for a specific app."""

        result = self._client._timelines_list(app, options)

        raw_result = convert_to_snake_case(result)
        return cast(PaginatedList[Timeline], raw_result)


class AsyncTimelines:
    def __init__(self, client: AsyncConsoleClient):
        self._client = client

    async def list(
        self, app: str, options: Optional[TimelineListOptions] = None
    ) -> PaginatedList[Timeline]:
        """List timelines for a specific app."""

        result = await self._client._timelines_list(app, options)

        raw_result = convert_to_snake_case(result)
        return cast(PaginatedList[Timeline], raw_result)


class Volumes:
    def __init__(self, client: ConsoleClient):
        self._client = client

    def create(self, options: VolumeInit) -> Volume:
        """Create a new volume."""

        result = self._client._volumes_create(options)

        raw_result = convert_to_snake_case(result)
        return cast(Volume, raw_result)

    def get(self, id_or_slug: str) -> Volume:
        """Get volume info by ID or slug."""

        result = self._client._volumes_get(id_or_slug)

        raw_result = convert_to_snake_case(result)
        return cast(Volume, raw_result)

    def list(
        self, options: Optional[VolumeListOptions] = None
    ) -> PaginatedList[Volume]:
        result = self._client._volumes_list(options)

        raw_result = convert_to_snake_case(result)
        return cast(PaginatedList[Volume], raw_result)

    def delete(self, id_or_slug: str) -> None:
        """Delete volume by ID or slug."""

        self._client._volumes_delete(id_or_slug)


class AsyncVolumes:
    def __init__(self, client: AsyncConsoleClient):
        self._client = client

    async def create(self, options: VolumeInit) -> Volume:
        """Create a new volume."""

        result = await self._client._volumes_create(options)

        raw_result = convert_to_snake_case(result)
        return cast(Volume, raw_result)

    async def get(self, id_or_slug: str) -> Volume:
        """Get volume info by ID or slug."""

        result = await self._client._volumes_get(id_or_slug)

        raw_result = convert_to_snake_case(result)
        return cast(Volume, raw_result)

    async def list(
        self, options: Optional[VolumeListOptions] = None
    ) -> PaginatedList[Volume]:
        result = await self._client._volumes_list(options)

        raw_result = convert_to_snake_case(result)
        return cast(PaginatedList[Volume], raw_result)

    async def delete(self, id_or_slug: str) -> None:
        """Delete volume by ID or slug."""

        await self._client._volumes_delete(id_or_slug)


class SandboxFs:
    def __init__(self, client: ConsoleClient, rpc: RpcClient):
        self._client = client
        self._rpc = rpc

    def read_file(self, path: str, options: Optional[ReadFileOptions] = None) -> bytes:
        """Reads the entire contents of a file as bytes."""

        params = {"path": path}
        if options is not None:
            params["options"] = convert_to_camel_case(options)

        result = self._rpc.call("readFile", params)

        return result

    def write_file(
        self, path: str, data: bytes, options: Optional[WriteFileOptions] = None
    ) -> None:
        """Write bytes to file. Creates a new file if needed. Existing files will be overwritten."""

        params = {"path": path, "data": data}
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

    def create(self, path: str) -> FsFile:
        """Create a new empty file at the specified path."""

        params = {"path": path}
        result = self._rpc.call("create", params)

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

    def open(self, path: str, options: Optional[FsOpenOptions] = None) -> FsFile:
        """Open a file and return a file descriptor."""

        params = {"path": path}
        if options is not None:
            params["options"] = convert_to_camel_case(options)

        result = self._rpc.call("open", params)

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
        """Upload a file or directory to the sandbox."""

        params = {"localPath": local_path, "sandboxPath": sandbox_path}
        self._rpc.call("upload", params)

    def download(self, local_path: str, sandbox_path: str) -> None:
        """Download a file or directory from the sandbox."""

        params = {"localPath": local_path, "sandboxPath": sandbox_path}
        self._rpc.call("download", params)


class AsyncSandboxFs:
    def __init__(self, client: AsyncConsoleClient, rpc: AsyncRpcClient):
        self._client = client
        self._rpc = rpc

    async def read_file(
        self, path: str, options: Optional[ReadFileOptions] = None
    ) -> bytes:
        """Reads the entire contents of a file as bytes."""

        params = {"path": path}
        if options is not None:
            params["options"] = convert_to_camel_case(options)

        result = await self._rpc.call("readFile", params)

        return result

    async def write_file(
        self, path: str, data: bytes, options: Optional[WriteFileOptions] = None
    ) -> None:
        """Write bytes to file. Creates a new file if needed. Existing files will be overwritten."""

        params = {"path": path, "data": data}
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

    async def create(self, path: str) -> AsyncFsFile:
        """Create a new empty file at the specified path."""

        params = {"path": path}
        result = await self._rpc.call("create", params)

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

    async def open(
        self, path: str, options: Optional[FsOpenOptions] = None
    ) -> AsyncFsFile:
        """Open a file and return a file descriptor."""

        params = {"path": path}
        if options is not None:
            params["options"] = convert_to_camel_case(options)

        result = await self._rpc.call("open", params)

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
        """Upload a file or directory to the sandbox."""

        params = {"localPath": local_path, "sandboxPath": sandbox_path}
        await self._rpc.call("upload", params)

    async def download(self, local_path: str, sandbox_path: str) -> None:
        """Download a file or directory from the sandbox."""

        params = {"localPath": local_path, "sandboxPath": sandbox_path}
        await self._rpc.call("download", params)


class SandboxDeno:
    def __init__(self, client: ConsoleClient, rpc: RpcClient):
        self._client = client
        self._rpc = rpc

    def run(self, options: DenoRunOptions) -> DenoProcess:
        """Create a new Deno process from the specified entrypoint file or code. The runtime will execute the given code to completion, and then exit."""

        params = {}
        if options is not None:
            params["options"] = convert_to_camel_case(options)

        result = self._rpc.call("spawnDeno", params)

        return result

    def eval(self, code: str) -> Any:
        result = self._client._sandbox_deno_eval(code)

        return result

    def repl(self, options: Optional[DenoReplOptions] = None) -> DenoRepl:
        params = {}
        if options is not None:
            params["options"] = convert_to_camel_case(options)

        result = self._rpc.call("spawnDenoRepl", params)

        return result

    def deploy(self, app: str, options: Optional[DeployOptions] = None) -> None:
        self._client._sandbox_deno_deploy(app, options)


class AsyncSandboxDeno:
    def __init__(self, client: AsyncConsoleClient, rpc: AsyncRpcClient):
        self._client = client
        self._rpc = rpc

    async def run(self, options: DenoRunOptions) -> AsyncDenoProcess:
        """Create a new Deno process from the specified entrypoint file or code. The runtime will execute the given code to completion, and then exit."""

        params = {}
        if options is not None:
            params["options"] = convert_to_camel_case(options)

        result = await self._rpc.call("spawnDeno", params)

        return result

    async def eval(self, code: str) -> Any:
        result = await self._client._sandbox_deno_eval(code)

        return result

    async def repl(self, options: Optional[DenoReplOptions] = None) -> AsyncDenoRepl:
        params = {}
        if options is not None:
            params["options"] = convert_to_camel_case(options)

        result = await self._rpc.call("spawnDenoRepl", params)

        return result

    async def deploy(self, app: str, options: Optional[DeployOptions] = None) -> None:
        await self._client._sandbox_deno_deploy(app, options)


class SandboxEnv:
    def __init__(self, client: ConsoleClient, rpc: RpcClient):
        self._client = client
        self._rpc = rpc

    def get(self, key: str) -> str:
        """Get the value of an environment variable."""

        params = {"key": key}
        result = self._rpc.call("envGet", params)

        return result

    def set(self, key: str, value: str) -> None:
        """Set the value of an environment variable."""

        params = {"key": key, "value": value}
        self._rpc.call("envSet", params)

    def to_object(self) -> dict[str, str]:
        """Get all environment variables."""

        params = {}
        result = self._rpc.call("envToObject", params)

        return result

    def delete(self, key: str) -> None:
        """Delete an environment variable."""

        params = {"key": key}
        self._rpc.call("envDelete", params)


class AsyncSandboxEnv:
    def __init__(self, client: AsyncConsoleClient, rpc: AsyncRpcClient):
        self._client = client
        self._rpc = rpc

    async def get(self, key: str) -> str:
        """Get the value of an environment variable."""

        params = {"key": key}
        result = await self._rpc.call("envGet", params)

        return result

    async def set(self, key: str, value: str) -> None:
        """Set the value of an environment variable."""

        params = {"key": key, "value": value}
        await self._rpc.call("envSet", params)

    async def to_object(self) -> dict[str, str]:
        """Get all environment variables."""

        params = {}
        result = await self._rpc.call("envToObject", params)

        return result

    async def delete(self, key: str) -> None:
        """Delete an environment variable."""

        params = {"key": key}
        await self._rpc.call("envDelete", params)
