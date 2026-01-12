# ATTENTION: This file is auto-generated. Do not edit it manually.

from typing import Any
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
from deno_sandbox.api_utils import convert_paginated_list_response
from dataclasses import is_dataclass


def parse_args(obj, klass):
    if is_dataclass(obj):
        return obj.to_dict()
    return klass(**obj)


class AppsApi:
    def __init__(self, client: ConsoleClient):
        self._client = client

    def get(self, app_id_or_slug: str) -> App:
        result = self._client.apps_get(app_id_or_slug)
        return App.from_dict(result)

    def list(self, options: AppListOptions | None = None) -> PaginatedList[App]:
        result = self._client.apps_list(AppListOptions(**options).to_dict())
        return convert_paginated_list_response(result, App)

    def create(self, options: AppInit) -> App:
        result = self._client.apps_create(AppInit(**options).to_dict())
        return App.from_dict(result)

    def update(self, id_or_slug: str, update: AppUpdate) -> App:
        result = self._client.apps_update(id_or_slug, AppUpdate(**update).to_dict())
        return App.from_dict(result)

    def delete(self, id_or_slug: str) -> None:
        self._client.apps_delete(id_or_slug)


class AsyncAppsApi:
    def __init__(self, client: AsyncConsoleClient):
        self._client = client

    async def get(self, app_id_or_slug: str) -> App:
        result = await self._client.apps_get(app_id_or_slug)
        return App.from_dict(result)

    async def list(self, options: AppListOptions) -> PaginatedList[App]:
        result = await self._client.apps_list(AppListOptions(**options).to_dict())
        return convert_paginated_list_response(result, App)

    async def create(self, options: AppInit) -> App:
        result = await self._client.apps_create(AppInit(**options).to_dict())
        return App.from_dict(result)

    async def update(self, id_or_slug: str, update: AppUpdate) -> App:
        result = await self._client.apps_update(
            id_or_slug, AppUpdate(**update).to_dict()
        )
        return App.from_dict(result)

    async def delete(self, id_or_slug: str) -> None:
        await self._client.apps_delete(id_or_slug)


class RevisionsApi:
    def __init__(self, client: ConsoleClient):
        self._client = client

    def get(self, app: str) -> Revision:
        result = self._client.revisions_get(app)
        return Revision.from_dict(result)

    def list(
        self, app_id_or_slug: str, options: RevisionListOptions | None = None
    ) -> PaginatedList[RevisionWithoutTimelines]:
        result = self._client.revisions_list(
            app_id_or_slug, RevisionListOptions(**options).to_dict()
        )
        return convert_paginated_list_response(result, RevisionWithoutTimelines)


class AsyncRevisionsApi:
    def __init__(self, client: AsyncConsoleClient):
        self._client = client

    async def get(self, app: str) -> Revision:
        result = await self._client.revisions_get(app)
        return Revision.from_dict(result)

    async def list(
        self, app_id_or_slug: str, options: RevisionListOptions
    ) -> PaginatedList[RevisionWithoutTimelines]:
        result = await self._client.revisions_list(
            app_id_or_slug, RevisionListOptions(**options).to_dict()
        )
        return convert_paginated_list_response(result, RevisionWithoutTimelines)


class TimelinesApi:
    def __init__(self, client: ConsoleClient):
        self._client = client

    def list(
        self, app_id_or_slug: str, options: TimelineListOptions | None = None
    ) -> PaginatedList[Timeline]:
        result = self._client.timelines_list(
            app_id_or_slug, TimelineListOptions(**options).to_dict()
        )
        return convert_paginated_list_response(result, Timeline)


class AsyncTimelinesApi:
    def __init__(self, client: AsyncConsoleClient):
        self._client = client

    async def list(
        self, app_id_or_slug: str, options: TimelineListOptions
    ) -> PaginatedList[Timeline]:
        result = await self._client.timelines_list(
            app_id_or_slug, TimelineListOptions(**options).to_dict()
        )
        return convert_paginated_list_response(result, Timeline)


class VolumesApi:
    def __init__(self, client: ConsoleClient):
        self._client = client

    def create(self, options: VolumesOptions) -> Volume:
        result = self._client.volumes_create(options)
        return Volume.from_dict(result)

    def get(self, id_or_slug: str) -> Volume:
        result = self._client.volumes_get(id_or_slug)
        return Volume.from_dict(result)

    def list(self, options: VolumesOptions | None = None) -> PaginatedList[Volume]:
        result = self._client.volumes_list(options)
        return convert_paginated_list_response(result, Volume)

    def delete(self, id_or_slug: str) -> None:
        self._client.volumes_delete(id_or_slug)


class AsyncVolumesApi:
    def __init__(self, client: AsyncConsoleClient):
        self._client = client

    async def create(self, options: VolumesOptions) -> Volume:
        result = await self._client.volumes_create(options)
        return Volume.from_dict(result)

    async def get(self, id_or_slug: str) -> Volume:
        result = await self._client.volumes_get(id_or_slug)
        return Volume.from_dict(result)

    async def list(self, options: VolumesOptions) -> PaginatedList[Volume]:
        result = await self._client.volumes_list(options)
        return convert_paginated_list_response(result, Volume)

    async def delete(self, id_or_slug: str) -> None:
        await self._client.volumes_delete(id_or_slug)


class Sandbox:
    def __init__(self, rpc: RpcClient):
        self._rpc = rpc

    def abort(self, args: AbortArgs | dict[str, Any]) -> None:
        self._rpc.call("abort", parse_args(args, AbortArgs))


class AsyncSandbox:
    def __init__(self, rpc: AsyncRpcClient):
        self._rpc = rpc

    async def abort(self, args: AbortArgs | dict[str, Any]) -> None:
        await self._rpc.call("abort", parse_args(args, AbortArgs))


class SandboxFs:
    def __init__(self, rpc: RpcClient):
        self._rpc = rpc

    def read_file(self, args: ReadFileArgs | dict[str, Any]) -> None:
        """Reads the entire contents of a file as bytes."""

        self._rpc.call("readFile", parse_args(args, ReadFileArgs))

    def read_text_file(self, args: ReadTextFileArgs | dict[str, Any]) -> str:
        """Reads the entire contents of a file as an UTF-8 decoded string."""

        result = self._rpc.call("readTextFile", parse_args(args, ReadTextFileArgs))
        return result

    def write_file(self, args: WriteFileArgs | dict[str, Any]) -> None:
        """Write bytes to file. Creates a new file if needed. Existing files will be overwritten."""

        self._rpc.call("writeFile", parse_args(args, WriteFileArgs))

    def write_text_file(self, args: WriteTextFileArgs | dict[str, Any]) -> None:
        """Write text to file. Creates a new file if needed. Existing files will be overwritten."""

        self._rpc.call("writeTextFile", parse_args(args, WriteTextFileArgs))

    def read_dir(self, args: ReadDirArgs | dict[str, Any]) -> list[ReadDirEntry]:
        """Read the directory entries at the given path."""

        result = self._rpc.call("readDir", parse_args(args, ReadDirArgs))
        return [ReadDirEntry.from_dict(i) for i in result]

    def remove(self, args: RemoveArgs | dict[str, Any]) -> None:
        """Remove the file or directory at the given path."""

        self._rpc.call("remove", parse_args(args, RemoveArgs))

    def mkdir(self, args: MkdirArgs | dict[str, Any]) -> None:
        """Create a new directory at the specified path."""

        self._rpc.call("mkdir", parse_args(args, MkdirArgs))

    def rename(self, args: RenameArgs | dict[str, Any]) -> None:
        """Rename (move) a file or directory."""

        self._rpc.call("rename", parse_args(args, RenameArgs))

    def copy_file(self, args: CopyFileArgs | dict[str, Any]) -> None:
        """Copy a file from one location to another."""

        self._rpc.call("copyFile", parse_args(args, CopyFileArgs))

    def link(self, args: LinkArgs | dict[str, Any]) -> None:
        """Create a hard link pointing to an existing file."""

        self._rpc.call("link", parse_args(args, LinkArgs))

    def lstat(self, args: LstatArgs | dict[str, Any]) -> FsLstatResult:
        """Return file information about a file or directory symlink."""

        result = self._rpc.call("lstat", parse_args(args, LstatArgs))
        return FsLstatResult.from_dict(result)

    def make_temp_dir(self, args: MakeTempDirArgs | dict[str, Any]) -> str:
        """Create a new temporary directory."""

        result = self._rpc.call("makeTempDir", parse_args(args, MakeTempDirArgs))
        return result

    def make_temp_file(self, args: MakeTempFileArgs | dict[str, Any]) -> str:
        """Create a new temporary file."""

        result = self._rpc.call("makeTempFile", parse_args(args, MakeTempFileArgs))
        return result

    def read_link(self, args: ReadLinkArgs | dict[str, Any]) -> str:
        """Read the target of a symbolic link."""

        result = self._rpc.call("readLink", parse_args(args, ReadLinkArgs))
        return result

    def real_path(self, args: RealPathArgs | dict[str, Any]) -> str:
        """Return the canonicalized absolute pathname."""

        result = self._rpc.call("realPath", parse_args(args, RealPathArgs))
        return result

    def symlink(self, args: SymlinkArgs | dict[str, Any]) -> None:
        """Create a symbolic link."""

        self._rpc.call("symlink", parse_args(args, SymlinkArgs))

    def truncate(self, args: TruncateArgs | dict[str, Any]) -> None:
        """Truncate or extend the specified file to reach a given size."""

        self._rpc.call("truncate", parse_args(args, TruncateArgs))

    def umask(self, args: UmaskArgs | dict[str, Any]) -> int:
        """Sets the process's file mode creation mask."""

        result = self._rpc.call("umask", parse_args(args, UmaskArgs))
        return result

    def utime(self, args: UtimeArgs | dict[str, Any]) -> None:
        """Change the access and modification times of a file."""

        self._rpc.call("utime", parse_args(args, UtimeArgs))

    def open(self, args: OpenArgs | dict[str, Any]) -> FsOpenResult:
        """Open a file and return a file handle id."""

        result = self._rpc.call("open", parse_args(args, OpenArgs))
        return FsOpenResult.from_dict(result)

    def create(self, args: CreateArgs | dict[str, Any]) -> FsCreateResult:
        """Create a new file and return a file handle id."""

        result = self._rpc.call("create", parse_args(args, CreateArgs))
        return FsCreateResult.from_dict(result)

    def file_close(self, args: FileCloseArgs | dict[str, Any]) -> None:
        """Close the specified file handle."""

        self._rpc.call("fileClose", parse_args(args, FileCloseArgs))

    def file_lock(self, args: FileLockArgs | dict[str, Any]) -> None:
        self._rpc.call("fileLock", parse_args(args, FileLockArgs))

    def file_read(self, args: FileReadArgs | dict[str, Any]) -> FsFileReadResult:
        result = self._rpc.call("fileRead", parse_args(args, FileReadArgs))
        return FsFileReadResult.from_dict(result)

    def file_seek(self, args: FileSeekArgs | dict[str, Any]) -> FsFileSeekResult:
        result = self._rpc.call("fileSeek", parse_args(args, FileSeekArgs))
        return FsFileSeekResult.from_dict(result)

    def file_stat(self, args: FileStatArgs | dict[str, Any]) -> FileHandleStat:
        result = self._rpc.call("fileStat", parse_args(args, FileStatArgs))
        return FileHandleStat.from_dict(result)

    def file_sync(self, args: FileSyncArgs | dict[str, Any]) -> None:
        self._rpc.call("fileSync", parse_args(args, FileSyncArgs))

    def file_sync_data(self, args: FileSyncDataArgs | dict[str, Any]) -> None:
        self._rpc.call("fileSyncData", parse_args(args, FileSyncDataArgs))

    def file_truncate(self, args: FileTruncateArgs | dict[str, Any]) -> None:
        self._rpc.call("fileTruncate", parse_args(args, FileTruncateArgs))

    def file_unlock(self, args: FileUnlockArgs | dict[str, Any]) -> None:
        self._rpc.call("fileUnlock", parse_args(args, FileUnlockArgs))

    def file_utime(self, args: FileUtimeArgs | dict[str, Any]) -> None:
        self._rpc.call("fileUtime", parse_args(args, FileUtimeArgs))

    def file_write(self, args: FileWriteArgs | dict[str, Any]) -> FsFileWriteResult:
        result = self._rpc.call("fileWrite", parse_args(args, FileWriteArgs))
        return FsFileWriteResult.from_dict(result)

    def walk(self, args: WalkArgs | dict[str, Any]) -> int:
        result = self._rpc.call("walk", parse_args(args, WalkArgs))
        return result

    def expand_glob(self, args: ExpandGlobArgs | dict[str, Any]) -> int:
        result = self._rpc.call("expandGlob", parse_args(args, ExpandGlobArgs))
        return result


class AsyncSandboxFs:
    def __init__(self, rpc: AsyncRpcClient):
        self._rpc = rpc

    async def read_file(self, args: ReadFileArgs | dict[str, Any]) -> None:
        """Reads the entire contents of a file as bytes."""

        await self._rpc.call("readFile", parse_args(args, ReadFileArgs))

    async def read_text_file(self, args: ReadTextFileArgs | dict[str, Any]) -> str:
        """Reads the entire contents of a file as an UTF-8 decoded string."""

        result = await self._rpc.call(
            "readTextFile", parse_args(args, ReadTextFileArgs)
        )
        return result

    async def write_file(self, args: WriteFileArgs | dict[str, Any]) -> None:
        """Write bytes to file. Creates a new file if needed. Existing files will be overwritten."""

        await self._rpc.call("writeFile", parse_args(args, WriteFileArgs))

    async def write_text_file(self, args: WriteTextFileArgs | dict[str, Any]) -> None:
        """Write text to file. Creates a new file if needed. Existing files will be overwritten."""

        await self._rpc.call("writeTextFile", parse_args(args, WriteTextFileArgs))

    async def read_dir(self, args: ReadDirArgs | dict[str, Any]) -> list[ReadDirEntry]:
        """Read the directory entries at the given path."""

        result = await self._rpc.call("readDir", parse_args(args, ReadDirArgs))
        return [ReadDirEntry.from_dict(i) for i in result]

    async def remove(self, args: RemoveArgs | dict[str, Any]) -> None:
        """Remove the file or directory at the given path."""

        await self._rpc.call("remove", parse_args(args, RemoveArgs))

    async def mkdir(self, args: MkdirArgs | dict[str, Any]) -> None:
        """Create a new directory at the specified path."""

        await self._rpc.call("mkdir", parse_args(args, MkdirArgs))

    async def rename(self, args: RenameArgs | dict[str, Any]) -> None:
        """Rename (move) a file or directory."""

        await self._rpc.call("rename", parse_args(args, RenameArgs))

    async def copy_file(self, args: CopyFileArgs | dict[str, Any]) -> None:
        """Copy a file from one location to another."""

        await self._rpc.call("copyFile", parse_args(args, CopyFileArgs))

    async def link(self, args: LinkArgs | dict[str, Any]) -> None:
        """Create a hard link pointing to an existing file."""

        await self._rpc.call("link", parse_args(args, LinkArgs))

    async def lstat(self, args: LstatArgs | dict[str, Any]) -> FsLstatResult:
        """Return file information about a file or directory symlink."""

        result = await self._rpc.call("lstat", parse_args(args, LstatArgs))
        return FsLstatResult.from_dict(result)

    async def make_temp_dir(self, args: MakeTempDirArgs | dict[str, Any]) -> str:
        """Create a new temporary directory."""

        result = await self._rpc.call("makeTempDir", parse_args(args, MakeTempDirArgs))
        return result

    async def make_temp_file(self, args: MakeTempFileArgs | dict[str, Any]) -> str:
        """Create a new temporary file."""

        result = await self._rpc.call(
            "makeTempFile", parse_args(args, MakeTempFileArgs)
        )
        return result

    async def read_link(self, args: ReadLinkArgs | dict[str, Any]) -> str:
        """Read the target of a symbolic link."""

        result = await self._rpc.call("readLink", parse_args(args, ReadLinkArgs))
        return result

    async def real_path(self, args: RealPathArgs | dict[str, Any]) -> str:
        """Return the canonicalized absolute pathname."""

        result = await self._rpc.call("realPath", parse_args(args, RealPathArgs))
        return result

    async def symlink(self, args: SymlinkArgs | dict[str, Any]) -> None:
        """Create a symbolic link."""

        await self._rpc.call("symlink", parse_args(args, SymlinkArgs))

    async def truncate(self, args: TruncateArgs | dict[str, Any]) -> None:
        """Truncate or extend the specified file to reach a given size."""

        await self._rpc.call("truncate", parse_args(args, TruncateArgs))

    async def umask(self, args: UmaskArgs | dict[str, Any]) -> int:
        """Sets the process's file mode creation mask."""

        result = await self._rpc.call("umask", parse_args(args, UmaskArgs))
        return result

    async def utime(self, args: UtimeArgs | dict[str, Any]) -> None:
        """Change the access and modification times of a file."""

        await self._rpc.call("utime", parse_args(args, UtimeArgs))

    async def open(self, args: OpenArgs | dict[str, Any]) -> FsOpenResult:
        """Open a file and return a file handle id."""

        result = await self._rpc.call("open", parse_args(args, OpenArgs))
        return FsOpenResult.from_dict(result)

    async def create(self, args: CreateArgs | dict[str, Any]) -> FsCreateResult:
        """Create a new file and return a file handle id."""

        result = await self._rpc.call("create", parse_args(args, CreateArgs))
        return FsCreateResult.from_dict(result)

    async def file_close(self, args: FileCloseArgs | dict[str, Any]) -> None:
        """Close the specified file handle."""

        await self._rpc.call("fileClose", parse_args(args, FileCloseArgs))

    async def file_lock(self, args: FileLockArgs | dict[str, Any]) -> None:
        await self._rpc.call("fileLock", parse_args(args, FileLockArgs))

    async def file_read(self, args: FileReadArgs | dict[str, Any]) -> FsFileReadResult:
        result = await self._rpc.call("fileRead", parse_args(args, FileReadArgs))
        return FsFileReadResult.from_dict(result)

    async def file_seek(self, args: FileSeekArgs | dict[str, Any]) -> FsFileSeekResult:
        result = await self._rpc.call("fileSeek", parse_args(args, FileSeekArgs))
        return FsFileSeekResult.from_dict(result)

    async def file_stat(self, args: FileStatArgs | dict[str, Any]) -> FileHandleStat:
        result = await self._rpc.call("fileStat", parse_args(args, FileStatArgs))
        return FileHandleStat.from_dict(result)

    async def file_sync(self, args: FileSyncArgs | dict[str, Any]) -> None:
        await self._rpc.call("fileSync", parse_args(args, FileSyncArgs))

    async def file_sync_data(self, args: FileSyncDataArgs | dict[str, Any]) -> None:
        await self._rpc.call("fileSyncData", parse_args(args, FileSyncDataArgs))

    async def file_truncate(self, args: FileTruncateArgs | dict[str, Any]) -> None:
        await self._rpc.call("fileTruncate", parse_args(args, FileTruncateArgs))

    async def file_unlock(self, args: FileUnlockArgs | dict[str, Any]) -> None:
        await self._rpc.call("fileUnlock", parse_args(args, FileUnlockArgs))

    async def file_utime(self, args: FileUtimeArgs | dict[str, Any]) -> None:
        await self._rpc.call("fileUtime", parse_args(args, FileUtimeArgs))

    async def file_write(
        self, args: FileWriteArgs | dict[str, Any]
    ) -> FsFileWriteResult:
        result = await self._rpc.call("fileWrite", parse_args(args, FileWriteArgs))
        return FsFileWriteResult.from_dict(result)

    async def walk(self, args: WalkArgs | dict[str, Any]) -> int:
        result = await self._rpc.call("walk", parse_args(args, WalkArgs))
        return result

    async def expand_glob(self, args: ExpandGlobArgs | dict[str, Any]) -> int:
        result = await self._rpc.call("expandGlob", parse_args(args, ExpandGlobArgs))
        return result


class SandboxProcess:
    def __init__(self, rpc: RpcClient):
        self._rpc = rpc

    def spawn(self, args: SpawnArgs | dict[str, Any]) -> ProcessSpawnResult:
        result = self._rpc.call("spawn", parse_args(args, SpawnArgs))
        return ProcessSpawnResult.from_dict(result)

    def wait(self, args: WaitArgs | dict[str, Any]) -> ProcessWaitResult:
        result = self._rpc.call("processWait", parse_args(args, WaitArgs))
        return ProcessWaitResult.from_dict(result)

    def kill(self, args: KillArgs | dict[str, Any]) -> None:
        self._rpc.call("processKill", parse_args(args, KillArgs))


class AsyncSandboxProcess:
    def __init__(self, rpc: AsyncRpcClient):
        self._rpc = rpc

    async def spawn(self, args: SpawnArgs | dict[str, Any]) -> ProcessSpawnResult:
        result = await self._rpc.call("spawn", parse_args(args, SpawnArgs))
        return ProcessSpawnResult.from_dict(result)

    async def wait(self, args: WaitArgs | dict[str, Any]) -> ProcessWaitResult:
        result = await self._rpc.call("processWait", parse_args(args, WaitArgs))
        return ProcessWaitResult.from_dict(result)

    async def kill(self, args: KillArgs | dict[str, Any]) -> None:
        await self._rpc.call("processKill", parse_args(args, KillArgs))


class SandboxDenoCli:
    def __init__(self, rpc: RpcClient):
        self._rpc = rpc

    def run(self, args: RunArgs | dict[str, Any]) -> DenoRunResult:
        result = self._rpc.call("spawnDeno", parse_args(args, RunArgs))
        return DenoRunResult.from_dict(result)

    def deno_http_wait(self, args: DenoHttpWaitArgs | dict[str, Any]) -> bool:
        result = self._rpc.call("denoHttpWait", parse_args(args, DenoHttpWaitArgs))
        return result

    def spawn_deno_repl(
        self, args: SpawnDenoReplArgs | dict[str, Any]
    ) -> DenoSpawnDenoReplResult:
        result = self._rpc.call("spawnDenoRepl", parse_args(args, SpawnDenoReplArgs))
        return DenoSpawnDenoReplResult.from_dict(result)

    def deno_repl_close(self, args: DenoReplCloseArgs | dict[str, Any]) -> None:
        self._rpc.call("denoReplClose", parse_args(args, DenoReplCloseArgs))

    def deno_repl_eval(self, args: DenoReplEvalArgs | dict[str, Any]) -> Any:
        result = self._rpc.call("denoReplEval", parse_args(args, DenoReplEvalArgs))
        return result

    def deno_repl_call(self, args: DenoReplCallArgs | dict[str, Any]) -> Any:
        result = self._rpc.call("denoReplCall", parse_args(args, DenoReplCallArgs))
        return result


class AsyncSandboxDenoCli:
    def __init__(self, rpc: AsyncRpcClient):
        self._rpc = rpc

    async def run(self, args: RunArgs | dict[str, Any]) -> DenoRunResult:
        result = await self._rpc.call("spawnDeno", parse_args(args, RunArgs))
        return DenoRunResult.from_dict(result)

    async def deno_http_wait(self, args: DenoHttpWaitArgs | dict[str, Any]) -> bool:
        result = await self._rpc.call(
            "denoHttpWait", parse_args(args, DenoHttpWaitArgs)
        )
        return result

    async def spawn_deno_repl(
        self, args: SpawnDenoReplArgs | dict[str, Any]
    ) -> DenoSpawnDenoReplResult:
        result = await self._rpc.call(
            "spawnDenoRepl", parse_args(args, SpawnDenoReplArgs)
        )
        return DenoSpawnDenoReplResult.from_dict(result)

    async def deno_repl_close(self, args: DenoReplCloseArgs | dict[str, Any]) -> None:
        await self._rpc.call("denoReplClose", parse_args(args, DenoReplCloseArgs))

    async def deno_repl_eval(self, args: DenoReplEvalArgs | dict[str, Any]) -> Any:
        result = await self._rpc.call(
            "denoReplEval", parse_args(args, DenoReplEvalArgs)
        )
        return result

    async def deno_repl_call(self, args: DenoReplCallArgs | dict[str, Any]) -> Any:
        result = await self._rpc.call(
            "denoReplCall", parse_args(args, DenoReplCallArgs)
        )
        return result


class SandboxNet:
    def __init__(self, rpc: RpcClient):
        self._rpc = rpc

    def fetch(self, args: FetchArgs | dict[str, Any]) -> NetFetchResult:
        result = self._rpc.call("fetch", parse_args(args, FetchArgs))
        return NetFetchResult.from_dict(result)

    def expose_http(self, args: ExposeHttpArgs | dict[str, Any]) -> None:
        self._rpc.call("exposeHttp", parse_args(args, ExposeHttpArgs))


class AsyncSandboxNet:
    def __init__(self, rpc: AsyncRpcClient):
        self._rpc = rpc

    async def fetch(self, args: FetchArgs | dict[str, Any]) -> NetFetchResult:
        result = await self._rpc.call("fetch", parse_args(args, FetchArgs))
        return NetFetchResult.from_dict(result)

    async def expose_http(self, args: ExposeHttpArgs | dict[str, Any]) -> None:
        await self._rpc.call("exposeHttp", parse_args(args, ExposeHttpArgs))


class SandboxVSCode:
    def __init__(self, rpc: RpcClient):
        self._rpc = rpc

    def connect(self, args: ConnectArgs | dict[str, Any]) -> VscodeConnectResult:
        result = self._rpc.call("connect", parse_args(args, ConnectArgs))
        return VscodeConnectResult.from_dict(result)


class AsyncSandboxVSCode:
    def __init__(self, rpc: AsyncRpcClient):
        self._rpc = rpc

    async def connect(self, args: ConnectArgs | dict[str, Any]) -> VscodeConnectResult:
        result = await self._rpc.call("connect", parse_args(args, ConnectArgs))
        return VscodeConnectResult.from_dict(result)


class SandboxEnv:
    def __init__(self, rpc: RpcClient):
        self._rpc = rpc

    def get(self, args: GetArgs | dict[str, Any]) -> str:
        result = self._rpc.call("envGet", parse_args(args, GetArgs))
        return result

    def set(self, args: SetArgs | dict[str, Any]) -> None:
        self._rpc.call("envSet", parse_args(args, SetArgs))

    def to_object(self, args: None | dict[str, Any]) -> dict[str, str]:
        result = self._rpc.call("envToObject", {})
        return result

    def delete(self, args: DeleteArgs | dict[str, Any]) -> None:
        self._rpc.call("envDelete", parse_args(args, DeleteArgs))


class AsyncSandboxEnv:
    def __init__(self, rpc: AsyncRpcClient):
        self._rpc = rpc

    async def get(self, args: GetArgs | dict[str, Any]) -> str:
        result = await self._rpc.call("envGet", parse_args(args, GetArgs))
        return result

    async def set(self, args: SetArgs | dict[str, Any]) -> None:
        await self._rpc.call("envSet", parse_args(args, SetArgs))

    async def to_object(self, args: None | dict[str, Any]) -> dict[str, str]:
        result = await self._rpc.call("envToObject", {})
        return result

    async def delete(self, args: DeleteArgs | dict[str, Any]) -> None:
        await self._rpc.call("envDelete", parse_args(args, DeleteArgs))
