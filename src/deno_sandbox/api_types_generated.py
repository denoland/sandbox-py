# ATTENTION: This file is auto-generated. Do not edit it manually.


from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
from typing import Literal, Any


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class App:
    id: str
    slug: str
    created_at: str
    updated_at: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class AppListOptions:
    cursor: str | None = None
    limit: int | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PaginatedList[T]:
    items: list[T]
    has_more: bool
    next_cursor: str | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class AppInit:
    slug: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class AppUpdate:
    slug: str | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TimelineApp:
    id: str
    slug: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TimelineContext:
    slug: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Domain:
    domain: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Timeline:
    slug: str
    partition: dict[str, str]
    app: TimelineApp
    context: TimelineContext
    domains: list[Domain]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Revision:
    id: str
    status: Literal["building", "ready", "error"]
    timelines: list[Timeline]
    created_at: str
    updated_at: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class RevisionListOptions:
    cursor: str | None = None
    limit: int | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class RevisionWithoutTimelines:
    id: str
    status: Literal["building", "ready", "error"]
    created_at: str
    updated_at: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TimelineListOptions:
    cursor: str | None = None
    limit: int | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class SandboxConnectOptions:
    region: str | None = None
    env: dict[str, str] | None = None
    timeout: str | None = None
    memory_db: str | None = None
    debug: bool | None = None
    labels: dict[str, str] | None = None
    volumes: dict[str, str] | None = None
    allow_net: list[str] | None = None
    ssh: bool | None = None
    port: int | None = None
    token: str | None = None
    org: str | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class SandboxListOptions:
    labels: dict[str, str] | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class SandboxMeta:
    id: str
    created_at: str
    region: str
    status: Literal["running", "stopped"]
    stopped_at: str | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class VolumesOptions:
    slug: str
    region: str
    capacity: int | str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Volume:
    id: str
    slug: str
    region: str
    capacity: int
    used: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class AbortArgs:
    abort_id: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ReadFileArgs:
    path: str
    abort_id: int | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ReadTextFileArgs:
    path: str
    abort_id: int | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class WriteFileOptions:
    create: bool | None = None
    append: bool | None = None
    create_new: bool | None = None
    mode: int | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class WriteFileWithContent:
    path: str
    content: str
    abort_id: int | None = None
    options: WriteFileOptions | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class WriteFileWithStream:
    path: str
    content_stream_id: int
    abort_id: int | None = None
    options: WriteFileOptions | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class WriteTextFileWithContent:
    path: str
    content: str
    abort_id: int | None = None
    options: WriteFileOptions | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class WriteTextFileWithStream:
    path: str
    content_stream_id: int
    abort_id: int | None = None
    options: WriteFileOptions | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ReadDirArgs:
    path: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ReadDirEntry:
    name: str
    is_file: bool
    is_directory: bool
    is_symlink: bool


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class RemoveOptions:
    recursive: bool | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class RemoveArgs:
    path: str
    options: RemoveOptions | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class MkdirOptions:
    recursive: bool | None = None
    mode: int | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class MkdirArgs:
    path: str
    options: MkdirOptions | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class RenameArgs:
    old_path: str
    new_path: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class CopyFileArgs:
    from_path: str
    to_path: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class LinkArgs:
    target: str
    path: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class LstatArgs:
    path: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class FsLstatResult:
    is_file: bool
    is_directory: bool
    is_symlink: bool
    size: int
    mtime: str
    atime: str
    birthtime: str
    ctime: str
    mode: int
    dev: int
    ino: int
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


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class MakeTempDirOptions:
    dir: str | None = None
    prefix: str | None = None
    suffix: str | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class MakeTempDirArgs:
    options: MakeTempDirOptions | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class MakeTempFileOptions:
    dir: str | None = None
    prefix: str | None = None
    suffix: str | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class MakeTempFileArgs:
    options: MakeTempFileOptions | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ReadLinkArgs:
    path: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class RealPathArgs:
    path: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class SymlinkOptions:
    type: Literal["file", "dir", "junction"] | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class SymlinkArgs:
    target: str
    path: str
    options: SymlinkOptions | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TruncateArgs:
    name: str
    len: int | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class UmaskArgs:
    mask: int | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class UtimeArgs:
    path: str
    atime: str
    mtime: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class FileOpenOptions:
    read: bool | None = None
    write: bool | None = None
    append: bool | None = None
    truncate: bool | None = None
    create: bool | None = None
    create_new: bool | None = None
    mode: int | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class OpenArgs:
    path: str
    options: FileOpenOptions | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class FsOpenResult:
    file_handle_id: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class CreateArgs:
    path: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class FsCreateResult:
    file_handle_id: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class FileCloseArgs:
    file_handle_id: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class FileLockArgs:
    file_handle_id: int
    exclusive: bool | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class FileReadArgs:
    file_handle_id: int
    length: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class FsFileReadResult:
    data: str | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class FileSeekArgs:
    file_handle_id: int
    offset: int | str
    whence: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class FsFileSeekResult:
    position: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class FileStatArgs:
    file_handle_id: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class FileHandleStat:
    is_file: bool
    is_directory: bool
    is_symlink: bool
    size: int
    mtime: str
    atime: str
    birthtime: str
    ctime: str
    mode: int
    dev: int
    ino: int
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


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class FileSyncArgs:
    file_handle_id: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class FileSyncDataArgs:
    file_handle_id: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class FileTruncateArgs:
    file_handle_id: int
    len: int | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class FileUnlockArgs:
    file_handle_id: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class FileUtimeArgs:
    file_handle_id: int
    atime: str
    mtime: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class FileWriteArgs:
    file_handle_id: int
    data: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class FsFileWriteResult:
    bytes_written: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class WalkArgs:
    path: str
    max_depth: int | None = None
    include_files: bool | None = None
    include_dirs: bool | None = None
    include_symlinks: bool | None = None
    follow_symlinks: bool | None = None
    canonicalize: bool | None = None
    exts: list[str] | None = None
    match: list[str] | None = None
    skip: list[str] | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ExpandGlobArgs:
    glob: str
    extended: bool | None = None
    globstar: bool | None = None
    case_insensitive: bool | None = None
    root: str | None = None
    exclude: list[str] | None = None
    include_dirs: bool | None = None
    follow_symlinks: bool | None = None
    canonicalize: bool | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class SpawnArgs:
    command: str
    stdout: Literal["piped", "null"] = "piped"
    stderr: Literal["piped", "null"] = "piped"
    args: list[str] | None = None
    env: dict[str, str] | None = None
    clear_env: bool | None = None
    cwd: str | None = None
    stdin_stream_id: int | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class ProcessSpawnResult:
    pid: int
    stdout_stream_id: int | None = None
    stderr_stream_id: int | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class WaitArgs:
    pid: int
    vscode: bool | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class ProcessWaitResult:
    success: bool
    code: int
    signal: str | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class KillArgs:
    pid: int
    signal: str | None = None
    vscode: bool | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class SpawnDenoByEntrypoint:
    entrypoint: str
    stdout: Literal["piped", "null"] = "piped"
    stderr: Literal["piped", "null"] = "piped"
    env: dict[str, str] | None = None
    clear_env: bool | None = None
    cwd: str | None = None
    stdin_stream_id: int | None = None
    script_args: list[str] | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class SpawnDenoByCode:
    code: str
    extension: Literal["js", "cjs", "mjs", "ts", "cts", "mts", "jsx", "tsx"]
    stdout: Literal["piped", "null"] = "piped"
    stderr: Literal["piped", "null"] = "piped"
    env: dict[str, str] | None = None
    clear_env: bool | None = None
    cwd: str | None = None
    stdin_stream_id: int | None = None
    script_args: list[str] | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class DenoRunResult:
    pid: int
    stdout_stream_id: int | None = None
    stderr_stream_id: int | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DenoHttpWaitArgs:
    pid: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class SpawnDenoReplArgs:
    stdout: Literal["piped", "null"] = "piped"
    stderr: Literal["piped", "null"] = "piped"
    env: dict[str, str] | None = None
    clear_env: bool | None = None
    cwd: str | None = None
    stdin_stream_id: int | None = None
    script_args: list[str] | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class DenoSpawnDenoReplResult:
    pid: int
    stdout_stream_id: int | None = None
    stderr_stream_id: int | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DenoReplCloseArgs:
    pid: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DenoReplEvalArgs:
    pid: int
    code: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DenoReplCallArgs:
    pid: int
    fn: str
    args: list[Any]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class FetchArgs:
    url: str
    method: str
    headers: dict[str, str]
    redirect: Literal["follow", "manual"]
    abort_id: int | None = None
    body_stream_id: int | None = None
    pid: int | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class NetFetchResult:
    status: int
    status_text: str
    headers: dict[str, str]
    body_stream_id: int | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ExposeHttpByPort:
    domain: str
    port: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ExposeHttpByPid:
    domain: str
    pid: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ConnectArgs:
    path: str
    extensions: list[str]
    env: dict[str, str] | None = None
    preview: str | None = None
    disable_stop_button: bool | None = None
    editor_settings: dict[str, Any] | None = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class VscodeConnectResult:
    pid: int
    port: int
    stdout_stream_id: int
    stderr_stream_id: int


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GetArgs:
    key: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class SetArgs:
    key: str
    value: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DeleteArgs:
    key: str
