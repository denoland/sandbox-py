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
    VolumesOptions,
    Volume,
    VolumeListOptions,
    AbortArgs,
    ReadFileArgs,
    ReadTextFileArgs,
    WriteFileArgs,
    WriteTextFileArgs,
    ReadDirArgs,
    ReadDirEntry,
    RemoveArgs,
    MkdirArgs,
    RenameArgs,
    CopyFileArgs,
    LinkArgs,
    LstatArgs,
    FsLstatResult,
    MakeTempDirArgs,
    MakeTempFileArgs,
    ReadLinkArgs,
    RealPathArgs,
    SymlinkArgs,
    TruncateArgs,
    UmaskArgs,
    UtimeArgs,
    OpenArgs,
    FsOpenResult,
    CreateArgs,
    FsCreateResult,
    FileCloseArgs,
    FileLockArgs,
    FileReadArgs,
    FsFileReadResult,
    FileSeekArgs,
    FsFileSeekResult,
    FileStatArgs,
    FileHandleStat,
    FileSyncArgs,
    FileSyncDataArgs,
    FileTruncateArgs,
    FileUnlockArgs,
    FileUtimeArgs,
    FileWriteArgs,
    FsFileWriteResult,
    WalkArgs,
    ExpandGlobArgs,
    SpawnArgs,
    ProcessSpawnResult,
    WaitArgs,
    ProcessWaitResult,
    KillArgs,
    RunArgs,
    DenoRunResult,
    DenoHttpWaitArgs,
    SpawnDenoReplArgs,
    DenoSpawnDenoReplResult,
    DenoReplCloseArgs,
    DenoReplEvalArgs,
    DenoReplCallArgs,
    FetchArgs,
    NetFetchResult,
    ExposeHttpArgs,
    ConnectArgs,
    VscodeConnectResult,
    GetArgs,
    SetArgs,
    DeleteArgs,
)

from deno_sandbox.rpc import AsyncRpcClient, RpcClient
from deno_sandbox.console import AsyncConsoleClient, ConsoleClient


class AppsApi:
    def __init__(self, client: ConsoleClient):
        self._client = client

    def get(self, app_id_or_slug: str) -> App:
        result = self._client.apps_get(app_id_or_slug)
        return cast(App, result)

    def list(self, options: Optional[AppListOptions] = None) -> PaginatedList[App]:
        result = self._client.apps_list(options)
        return cast(PaginatedList[App], result)

    def create(self, options: AppInit) -> App:
        result = self._client.apps_create(options)
        return cast(App, result)

    def update(self, id_or_slug: str, update: AppUpdate) -> App:
        result = self._client.apps_update(id_or_slug, update)
        return cast(App, result)

    def delete(self, id_or_slug: str) -> None:
        self._client.apps_delete(id_or_slug)


class AsyncAppsApi:
    def __init__(self, client: AsyncConsoleClient):
        self._client = client

    async def get(self, app_id_or_slug: str) -> App:
        result = await self._client.apps_get(app_id_or_slug)
        return cast(App, result)

    async def list(
        self, options: Optional[AppListOptions] = None
    ) -> PaginatedList[App]:
        result = await self._client.apps_list(options)
        return cast(PaginatedList[App], result)

    async def create(self, options: AppInit) -> App:
        result = await self._client.apps_create(options)
        return cast(App, result)

    async def update(self, id_or_slug: str, update: AppUpdate) -> App:
        result = await self._client.apps_update(id_or_slug, update)
        return cast(App, result)

    async def delete(self, id_or_slug: str) -> None:
        await self._client.apps_delete(id_or_slug)


class RevisionsApi:
    def __init__(self, client: ConsoleClient):
        self._client = client

    def get(self, app: str) -> Revision:
        result = self._client.revisions_get(app)
        return cast(Revision, result)

    def list(
        self, app_id_or_slug: str, options: Optional[RevisionListOptions] = None
    ) -> PaginatedList[RevisionWithoutTimelines]:
        result = self._client.revisions_list(app_id_or_slug, options)
        return cast(PaginatedList[RevisionWithoutTimelines], result)


class AsyncRevisionsApi:
    def __init__(self, client: AsyncConsoleClient):
        self._client = client

    async def get(self, app: str) -> Revision:
        result = await self._client.revisions_get(app)
        return cast(Revision, result)

    async def list(
        self, app_id_or_slug: str, options: Optional[RevisionListOptions] = None
    ) -> PaginatedList[RevisionWithoutTimelines]:
        result = await self._client.revisions_list(app_id_or_slug, options)
        return cast(PaginatedList[RevisionWithoutTimelines], result)


class TimelinesApi:
    def __init__(self, client: ConsoleClient):
        self._client = client

    def list(
        self, app_id_or_slug: str, options: Optional[TimelineListOptions] = None
    ) -> PaginatedList[Timeline]:
        result = self._client.timelines_list(app_id_or_slug, options)
        return cast(PaginatedList[Timeline], result)


class AsyncTimelinesApi:
    def __init__(self, client: AsyncConsoleClient):
        self._client = client

    async def list(
        self, app_id_or_slug: str, options: Optional[TimelineListOptions] = None
    ) -> PaginatedList[Timeline]:
        result = await self._client.timelines_list(app_id_or_slug, options)
        return cast(PaginatedList[Timeline], result)


class VolumesApi:
    def __init__(self, client: ConsoleClient):
        self._client = client

    def create(self, options: VolumesOptions) -> Volume:
        result = self._client.volumes_create(options)
        return cast(Volume, result)

    def get(self, id_or_slug: str) -> Volume:
        result = self._client.volumes_get(id_or_slug)
        return cast(Volume, result)

    def list(
        self, options: Optional[VolumeListOptions] = None
    ) -> PaginatedList[Volume]:
        result = self._client.volumes_list(options)
        return cast(PaginatedList[Volume], result)

    def delete(self, id_or_slug: str) -> None:
        self._client.volumes_delete(id_or_slug)


class AsyncVolumesApi:
    def __init__(self, client: AsyncConsoleClient):
        self._client = client

    async def create(self, options: VolumesOptions) -> Volume:
        result = await self._client.volumes_create(options)
        return cast(Volume, result)

    async def get(self, id_or_slug: str) -> Volume:
        result = await self._client.volumes_get(id_or_slug)
        return cast(Volume, result)

    async def list(
        self, options: Optional[VolumeListOptions] = None
    ) -> PaginatedList[Volume]:
        result = await self._client.volumes_list(options)
        return cast(PaginatedList[Volume], result)

    async def delete(self, id_or_slug: str) -> None:
        await self._client.volumes_delete(id_or_slug)


class Sandbox:
    def __init__(self, rpc: RpcClient):
        self._rpc = rpc

    def abort(self, args: AbortArgs) -> None:
        self._rpc.call("abort", args)


class AsyncSandbox:
    def __init__(self, rpc: AsyncRpcClient):
        self._rpc = rpc

    async def abort(self, args: AbortArgs) -> None:
        await self._rpc.call("abort", args)


class SandboxFs:
    def __init__(self, rpc: RpcClient):
        self._rpc = rpc

    def read_file(self, args: ReadFileArgs) -> None:
        """Reads the entire contents of a file as bytes."""

        self._rpc.call("readFile", args)

    def read_text_file(self, args: ReadTextFileArgs) -> str:
        """Reads the entire contents of a file as an UTF-8 decoded string."""

        result = self._rpc.call("readTextFile", args)
        return result

    def write_file(self, args: WriteFileArgs) -> None:
        """Write bytes to file. Creates a new file if needed. Existing files will be overwritten."""

        self._rpc.call("writeFile", args)

    def write_text_file(self, args: WriteTextFileArgs) -> None:
        """Write text to file. Creates a new file if needed. Existing files will be overwritten."""

        self._rpc.call("writeTextFile", args)

    def read_dir(self, args: ReadDirArgs) -> list[ReadDirEntry]:
        """Read the directory entries at the given path."""

        result = self._rpc.call("readDir", args)
        return [cast(ReadDirEntry, i) for i in result]

    def remove(self, args: RemoveArgs) -> None:
        """Remove the file or directory at the given path."""

        self._rpc.call("remove", args)

    def mkdir(self, args: MkdirArgs) -> None:
        """Create a new directory at the specified path."""

        self._rpc.call("mkdir", args)

    def rename(self, args: RenameArgs) -> None:
        """Rename (move) a file or directory."""

        self._rpc.call("rename", args)

    def copy_file(self, args: CopyFileArgs) -> None:
        """Copy a file from one location to another."""

        self._rpc.call("copyFile", args)

    def link(self, args: LinkArgs) -> None:
        """Create a hard link pointing to an existing file."""

        self._rpc.call("link", args)

    def lstat(self, args: LstatArgs) -> FsLstatResult:
        """Return file information about a file or directory symlink."""

        result = self._rpc.call("lstat", args)
        return cast(FsLstatResult, result)

    def make_temp_dir(self, args: MakeTempDirArgs) -> str:
        """Create a new temporary directory."""

        result = self._rpc.call("makeTempDir", args)
        return result

    def make_temp_file(self, args: MakeTempFileArgs) -> str:
        """Create a new temporary file."""

        result = self._rpc.call("makeTempFile", args)
        return result

    def read_link(self, args: ReadLinkArgs) -> str:
        """Read the target of a symbolic link."""

        result = self._rpc.call("readLink", args)
        return result

    def real_path(self, args: RealPathArgs) -> str:
        """Return the canonicalized absolute pathname."""

        result = self._rpc.call("realPath", args)
        return result

    def symlink(self, args: SymlinkArgs) -> None:
        """Create a symbolic link."""

        self._rpc.call("symlink", args)

    def truncate(self, args: TruncateArgs) -> None:
        """Truncate or extend the specified file to reach a given size."""

        self._rpc.call("truncate", args)

    def umask(self, args: UmaskArgs) -> int:
        """Sets the process's file mode creation mask."""

        result = self._rpc.call("umask", args)
        return result

    def utime(self, args: UtimeArgs) -> None:
        """Change the access and modification times of a file."""

        self._rpc.call("utime", args)

    def open(self, args: OpenArgs) -> FsOpenResult:
        """Open a file and return a file handle id."""

        result = self._rpc.call("open", args)
        return cast(FsOpenResult, result)

    def create(self, args: CreateArgs) -> FsCreateResult:
        """Create a new file and return a file handle id."""

        result = self._rpc.call("create", args)
        return cast(FsCreateResult, result)

    def file_close(self, args: FileCloseArgs) -> None:
        """Close the specified file handle."""

        self._rpc.call("fileClose", args)

    def file_lock(self, args: FileLockArgs) -> None:
        self._rpc.call("fileLock", args)

    def file_read(self, args: FileReadArgs) -> FsFileReadResult:
        result = self._rpc.call("fileRead", args)
        return cast(FsFileReadResult, result)

    def file_seek(self, args: FileSeekArgs) -> FsFileSeekResult:
        result = self._rpc.call("fileSeek", args)
        return cast(FsFileSeekResult, result)

    def file_stat(self, args: FileStatArgs) -> FileHandleStat:
        result = self._rpc.call("fileStat", args)
        return cast(FileHandleStat, result)

    def file_sync(self, args: FileSyncArgs) -> None:
        self._rpc.call("fileSync", args)

    def file_sync_data(self, args: FileSyncDataArgs) -> None:
        self._rpc.call("fileSyncData", args)

    def file_truncate(self, args: FileTruncateArgs) -> None:
        self._rpc.call("fileTruncate", args)

    def file_unlock(self, args: FileUnlockArgs) -> None:
        self._rpc.call("fileUnlock", args)

    def file_utime(self, args: FileUtimeArgs) -> None:
        self._rpc.call("fileUtime", args)

    def file_write(self, args: FileWriteArgs) -> FsFileWriteResult:
        result = self._rpc.call("fileWrite", args)
        return cast(FsFileWriteResult, result)

    def walk(self, args: WalkArgs) -> int:
        result = self._rpc.call("walk", args)
        return result

    def expand_glob(self, args: ExpandGlobArgs) -> int:
        result = self._rpc.call("expandGlob", args)
        return result


class AsyncSandboxFs:
    def __init__(self, rpc: AsyncRpcClient):
        self._rpc = rpc

    async def read_file(self, args: ReadFileArgs) -> None:
        """Reads the entire contents of a file as bytes."""

        await self._rpc.call("readFile", args)

    async def read_text_file(self, args: ReadTextFileArgs) -> str:
        """Reads the entire contents of a file as an UTF-8 decoded string."""

        result = await self._rpc.call("readTextFile", args)
        return result

    async def write_file(self, args: WriteFileArgs) -> None:
        """Write bytes to file. Creates a new file if needed. Existing files will be overwritten."""

        await self._rpc.call("writeFile", args)

    async def write_text_file(self, args: WriteTextFileArgs) -> None:
        """Write text to file. Creates a new file if needed. Existing files will be overwritten."""

        await self._rpc.call("writeTextFile", args)

    async def read_dir(self, args: ReadDirArgs) -> list[ReadDirEntry]:
        """Read the directory entries at the given path."""

        result = await self._rpc.call("readDir", args)
        return [cast(ReadDirEntry, i) for i in result]

    async def remove(self, args: RemoveArgs) -> None:
        """Remove the file or directory at the given path."""

        await self._rpc.call("remove", args)

    async def mkdir(self, args: MkdirArgs) -> None:
        """Create a new directory at the specified path."""

        await self._rpc.call("mkdir", args)

    async def rename(self, args: RenameArgs) -> None:
        """Rename (move) a file or directory."""

        await self._rpc.call("rename", args)

    async def copy_file(self, args: CopyFileArgs) -> None:
        """Copy a file from one location to another."""

        await self._rpc.call("copyFile", args)

    async def link(self, args: LinkArgs) -> None:
        """Create a hard link pointing to an existing file."""

        await self._rpc.call("link", args)

    async def lstat(self, args: LstatArgs) -> FsLstatResult:
        """Return file information about a file or directory symlink."""

        result = await self._rpc.call("lstat", args)
        return cast(FsLstatResult, result)

    async def make_temp_dir(self, args: MakeTempDirArgs) -> str:
        """Create a new temporary directory."""

        result = await self._rpc.call("makeTempDir", args)
        return result

    async def make_temp_file(self, args: MakeTempFileArgs) -> str:
        """Create a new temporary file."""

        result = await self._rpc.call("makeTempFile", args)
        return result

    async def read_link(self, args: ReadLinkArgs) -> str:
        """Read the target of a symbolic link."""

        result = await self._rpc.call("readLink", args)
        return result

    async def real_path(self, args: RealPathArgs) -> str:
        """Return the canonicalized absolute pathname."""

        result = await self._rpc.call("realPath", args)
        return result

    async def symlink(self, args: SymlinkArgs) -> None:
        """Create a symbolic link."""

        await self._rpc.call("symlink", args)

    async def truncate(self, args: TruncateArgs) -> None:
        """Truncate or extend the specified file to reach a given size."""

        await self._rpc.call("truncate", args)

    async def umask(self, args: UmaskArgs) -> int:
        """Sets the process's file mode creation mask."""

        result = await self._rpc.call("umask", args)
        return result

    async def utime(self, args: UtimeArgs) -> None:
        """Change the access and modification times of a file."""

        await self._rpc.call("utime", args)

    async def open(self, args: OpenArgs) -> FsOpenResult:
        """Open a file and return a file handle id."""

        result = await self._rpc.call("open", args)
        return cast(FsOpenResult, result)

    async def create(self, args: CreateArgs) -> FsCreateResult:
        """Create a new file and return a file handle id."""

        result = await self._rpc.call("create", args)
        return cast(FsCreateResult, result)

    async def file_close(self, args: FileCloseArgs) -> None:
        """Close the specified file handle."""

        await self._rpc.call("fileClose", args)

    async def file_lock(self, args: FileLockArgs) -> None:
        await self._rpc.call("fileLock", args)

    async def file_read(self, args: FileReadArgs) -> FsFileReadResult:
        result = await self._rpc.call("fileRead", args)
        return cast(FsFileReadResult, result)

    async def file_seek(self, args: FileSeekArgs) -> FsFileSeekResult:
        result = await self._rpc.call("fileSeek", args)
        return cast(FsFileSeekResult, result)

    async def file_stat(self, args: FileStatArgs) -> FileHandleStat:
        result = await self._rpc.call("fileStat", args)
        return cast(FileHandleStat, result)

    async def file_sync(self, args: FileSyncArgs) -> None:
        await self._rpc.call("fileSync", args)

    async def file_sync_data(self, args: FileSyncDataArgs) -> None:
        await self._rpc.call("fileSyncData", args)

    async def file_truncate(self, args: FileTruncateArgs) -> None:
        await self._rpc.call("fileTruncate", args)

    async def file_unlock(self, args: FileUnlockArgs) -> None:
        await self._rpc.call("fileUnlock", args)

    async def file_utime(self, args: FileUtimeArgs) -> None:
        await self._rpc.call("fileUtime", args)

    async def file_write(self, args: FileWriteArgs) -> FsFileWriteResult:
        result = await self._rpc.call("fileWrite", args)
        return cast(FsFileWriteResult, result)

    async def walk(self, args: WalkArgs) -> int:
        result = await self._rpc.call("walk", args)
        return result

    async def expand_glob(self, args: ExpandGlobArgs) -> int:
        result = await self._rpc.call("expandGlob", args)
        return result


class SandboxProcess:
    def __init__(self, rpc: RpcClient):
        self._rpc = rpc

    def spawn(self, args: SpawnArgs) -> ProcessSpawnResult:
        result = self._rpc.call("spawn", args)
        return cast(ProcessSpawnResult, result)

    def wait(self, args: WaitArgs) -> ProcessWaitResult:
        result = self._rpc.call("processWait", args)
        return cast(ProcessWaitResult, result)

    def kill(self, args: KillArgs) -> None:
        self._rpc.call("processKill", args)


class AsyncSandboxProcess:
    def __init__(self, rpc: AsyncRpcClient):
        self._rpc = rpc

    async def spawn(self, args: SpawnArgs) -> ProcessSpawnResult:
        result = await self._rpc.call("spawn", args)
        return cast(ProcessSpawnResult, result)

    async def wait(self, args: WaitArgs) -> ProcessWaitResult:
        result = await self._rpc.call("processWait", args)
        return cast(ProcessWaitResult, result)

    async def kill(self, args: KillArgs) -> None:
        await self._rpc.call("processKill", args)


class SandboxDenoCli:
    def __init__(self, rpc: RpcClient):
        self._rpc = rpc

    def run(self, args: RunArgs) -> DenoRunResult:
        result = self._rpc.call("spawnDeno", args)
        return cast(DenoRunResult, result)

    def deno_http_wait(self, args: DenoHttpWaitArgs) -> bool:
        result = self._rpc.call("denoHttpWait", args)
        return result

    def spawn_deno_repl(self, args: SpawnDenoReplArgs) -> DenoSpawnDenoReplResult:
        result = self._rpc.call("spawnDenoRepl", args)
        return cast(DenoSpawnDenoReplResult, result)

    def deno_repl_close(self, args: DenoReplCloseArgs) -> None:
        self._rpc.call("denoReplClose", args)

    def deno_repl_eval(self, args: DenoReplEvalArgs) -> Any:
        result = self._rpc.call("denoReplEval", args)
        return result

    def deno_repl_call(self, args: DenoReplCallArgs) -> Any:
        result = self._rpc.call("denoReplCall", args)
        return result


class AsyncSandboxDenoCli:
    def __init__(self, rpc: AsyncRpcClient):
        self._rpc = rpc

    async def run(self, args: RunArgs) -> DenoRunResult:
        result = await self._rpc.call("spawnDeno", args)
        return cast(DenoRunResult, result)

    async def deno_http_wait(self, args: DenoHttpWaitArgs) -> bool:
        result = await self._rpc.call("denoHttpWait", args)
        return result

    async def spawn_deno_repl(self, args: SpawnDenoReplArgs) -> DenoSpawnDenoReplResult:
        result = await self._rpc.call("spawnDenoRepl", args)
        return cast(DenoSpawnDenoReplResult, result)

    async def deno_repl_close(self, args: DenoReplCloseArgs) -> None:
        await self._rpc.call("denoReplClose", args)

    async def deno_repl_eval(self, args: DenoReplEvalArgs) -> Any:
        result = await self._rpc.call("denoReplEval", args)
        return result

    async def deno_repl_call(self, args: DenoReplCallArgs) -> Any:
        result = await self._rpc.call("denoReplCall", args)
        return result


class SandboxNet:
    def __init__(self, rpc: RpcClient):
        self._rpc = rpc

    def fetch(self, args: FetchArgs) -> NetFetchResult:
        result = self._rpc.call("fetch", args)
        return cast(NetFetchResult, result)

    def expose_http(self, args: ExposeHttpArgs) -> None:
        self._rpc.call("exposeHttp", args)


class AsyncSandboxNet:
    def __init__(self, rpc: AsyncRpcClient):
        self._rpc = rpc

    async def fetch(self, args: FetchArgs) -> NetFetchResult:
        result = await self._rpc.call("fetch", args)
        return cast(NetFetchResult, result)

    async def expose_http(self, args: ExposeHttpArgs) -> None:
        await self._rpc.call("exposeHttp", args)


class SandboxVSCode:
    def __init__(self, rpc: RpcClient):
        self._rpc = rpc

    def connect(self, args: ConnectArgs) -> VscodeConnectResult:
        result = self._rpc.call("connect", args)
        return cast(VscodeConnectResult, result)


class AsyncSandboxVSCode:
    def __init__(self, rpc: AsyncRpcClient):
        self._rpc = rpc

    async def connect(self, args: ConnectArgs) -> VscodeConnectResult:
        result = await self._rpc.call("connect", args)
        return cast(VscodeConnectResult, result)


class SandboxEnv:
    def __init__(self, rpc: RpcClient):
        self._rpc = rpc

    def get(self, args: GetArgs) -> str:
        result = self._rpc.call("envGet", args)
        return result

    def set(self, args: SetArgs) -> None:
        self._rpc.call("envSet", args)

    def to_object(self, args: None) -> dict[str, str]:
        result = self._rpc.call("envToObject", {})
        return result

    def delete(self, args: DeleteArgs) -> None:
        self._rpc.call("envDelete", args)


class AsyncSandboxEnv:
    def __init__(self, rpc: AsyncRpcClient):
        self._rpc = rpc

    async def get(self, args: GetArgs) -> str:
        result = await self._rpc.call("envGet", args)
        return result

    async def set(self, args: SetArgs) -> None:
        await self._rpc.call("envSet", args)

    async def to_object(self, args: None) -> dict[str, str]:
        result = await self._rpc.call("envToObject", {})
        return result

    async def delete(self, args: DeleteArgs) -> None:
        await self._rpc.call("envDelete", args)
