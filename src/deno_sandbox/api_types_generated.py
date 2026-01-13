# ATTENTION: This file is auto-generated. Do not edit it manually.


from typing_extensions import TypedDict, NotRequired, Literal, Any


class App(TypedDict):
    id: str
    slug: str
    created_at: str
    updated_at: str


class AppListOptions(TypedDict):
    cursor: NotRequired[str | None]
    limit: NotRequired[int | None]


class PaginatedList[T](TypedDict):
    items: list[T]
    has_more: bool
    next_cursor: NotRequired[str | None]


class AppInit(TypedDict):
    slug: str


class AppUpdate(TypedDict):
    slug: NotRequired[str | None]


class TimelineApp(TypedDict):
    id: str
    slug: str


class TimelineContext(TypedDict):
    slug: str


class Domain(TypedDict):
    domain: str


class Timeline(TypedDict):
    slug: str
    partition: dict[str, str]
    app: TimelineApp
    context: TimelineContext
    domains: list[Domain]


class Revision(TypedDict):
    id: str
    status: Literal["building", "ready", "error"]
    timelines: list[Timeline]
    created_at: str
    updated_at: str


class RevisionListOptions(TypedDict):
    cursor: NotRequired[str | None]
    limit: NotRequired[int | None]


class RevisionWithoutTimelines(TypedDict):
    id: str
    status: Literal["building", "ready", "error"]
    created_at: str
    updated_at: str


class TimelineListOptions(TypedDict):
    cursor: NotRequired[str | None]
    limit: NotRequired[int | None]


class SandboxCreateOptions(TypedDict):
    region: NotRequired[str | None]
    env: NotRequired[dict[str, str] | None]
    timeout: NotRequired[str | None]
    memory_db: NotRequired[str | None]
    debug: NotRequired[bool | None]
    labels: NotRequired[dict[str, str] | None]
    volumes: NotRequired[dict[str, str] | None]
    allow_net: NotRequired[list[str] | None]
    ssh: NotRequired[bool | None]
    port: NotRequired[int | None]
    token: NotRequired[str | None]
    org: NotRequired[str | None]


class SandboxConnectOptions(TypedDict):
    id: str
    region: NotRequired[str | None]
    debug: NotRequired[bool | None]
    ssh: NotRequired[bool | None]
    token: NotRequired[str | None]
    org: NotRequired[str | None]


class SandboxListOptions(TypedDict):
    labels: NotRequired[dict[str, str] | None]


class SandboxMeta(TypedDict):
    id: str
    created_at: str
    region: str
    status: Literal["running", "stopped"]
    stopped_at: NotRequired[str | None]


class VolumesOptions(TypedDict):
    slug: str
    region: str
    capacity: int | str


class Volume(TypedDict):
    id: str
    slug: str
    region: str
    capacity: int
    used: int


class VolumeListOptions(TypedDict):
    cursor: NotRequired[str | None]
    limit: NotRequired[int | None]
    search: NotRequired[str | None]


class AbortArgs(TypedDict):
    abort_id: int


class ReadFileArgs(TypedDict):
    path: str
    abort_id: NotRequired[int | None]


class ReadTextFileArgs(TypedDict):
    path: str
    abort_id: NotRequired[int | None]


class WriteFileOptions(TypedDict):
    create: NotRequired[bool | None]
    append: NotRequired[bool | None]
    create_new: NotRequired[bool | None]
    mode: NotRequired[int | None]


class WriteFileArgs(TypedDict):
    path: str
    abort_id: NotRequired[int | None]
    options: NotRequired[WriteFileOptions | None]
    content: NotRequired[str | None]
    content_stream_id: NotRequired[int | None]


class WriteTextFileArgs(TypedDict):
    path: str
    abort_id: NotRequired[int | None]
    options: NotRequired[WriteFileOptions | None]
    content: NotRequired[str | None]
    content_stream_id: NotRequired[int | None]


class ReadDirArgs(TypedDict):
    path: str


class ReadDirEntry(TypedDict):
    name: str
    is_file: bool
    is_directory: bool
    is_symlink: bool


class RemoveOptions(TypedDict):
    recursive: NotRequired[bool | None]


class RemoveArgs(TypedDict):
    path: str
    options: NotRequired[RemoveOptions | None]


class MkdirOptions(TypedDict):
    recursive: NotRequired[bool | None]
    mode: NotRequired[int | None]


class MkdirArgs(TypedDict):
    path: str
    options: NotRequired[MkdirOptions | None]


class RenameArgs(TypedDict):
    old_path: str
    new_path: str


class CopyFileArgs(TypedDict):
    from_path: str
    to_path: str


class LinkArgs(TypedDict):
    target: str
    path: str


class LstatArgs(TypedDict):
    path: str


class FsLstatResult(TypedDict):
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


class MakeTempDirOptions(TypedDict):
    dir: NotRequired[str | None]
    prefix: NotRequired[str | None]
    suffix: NotRequired[str | None]


class MakeTempDirArgs(TypedDict):
    options: NotRequired[MakeTempDirOptions | None]


class MakeTempFileOptions(TypedDict):
    dir: NotRequired[str | None]
    prefix: NotRequired[str | None]
    suffix: NotRequired[str | None]


class MakeTempFileArgs(TypedDict):
    options: NotRequired[MakeTempFileOptions | None]


class ReadLinkArgs(TypedDict):
    path: str


class RealPathArgs(TypedDict):
    path: str


class SymlinkOptions(TypedDict):
    type: NotRequired[Literal["file", "dir", "junction"] | None]


class SymlinkArgs(TypedDict):
    target: str
    path: str
    options: NotRequired[SymlinkOptions | None]


class TruncateArgs(TypedDict):
    name: str
    len: NotRequired[int | None]


class UmaskArgs(TypedDict):
    mask: NotRequired[int | None]


class UtimeArgs(TypedDict):
    path: str
    atime: str
    mtime: str


class FileOpenOptions(TypedDict):
    read: NotRequired[bool | None]
    write: NotRequired[bool | None]
    append: NotRequired[bool | None]
    truncate: NotRequired[bool | None]
    create: NotRequired[bool | None]
    create_new: NotRequired[bool | None]
    mode: NotRequired[int | None]


class OpenArgs(TypedDict):
    path: str
    options: NotRequired[FileOpenOptions | None]


class FsOpenResult(TypedDict):
    file_handle_id: int


class CreateArgs(TypedDict):
    path: str


class FsCreateResult(TypedDict):
    file_handle_id: int


class FileCloseArgs(TypedDict):
    file_handle_id: int


class FileLockArgs(TypedDict):
    file_handle_id: int
    exclusive: NotRequired[bool | None]


class FileReadArgs(TypedDict):
    file_handle_id: int
    length: int


class FsFileReadResult(TypedDict):
    data: NotRequired[str | None]


class FileSeekArgs(TypedDict):
    file_handle_id: int
    offset: int | str
    whence: int


class FsFileSeekResult(TypedDict):
    position: int


class FileStatArgs(TypedDict):
    file_handle_id: int


class FileHandleStat(TypedDict):
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


class FileSyncArgs(TypedDict):
    file_handle_id: int


class FileSyncDataArgs(TypedDict):
    file_handle_id: int


class FileTruncateArgs(TypedDict):
    file_handle_id: int
    len: NotRequired[int | None]


class FileUnlockArgs(TypedDict):
    file_handle_id: int


class FileUtimeArgs(TypedDict):
    file_handle_id: int
    atime: str
    mtime: str


class FileWriteArgs(TypedDict):
    file_handle_id: int
    data: str


class FsFileWriteResult(TypedDict):
    bytes_written: int


class WalkArgs(TypedDict):
    path: str
    max_depth: NotRequired[int | None]
    include_files: NotRequired[bool | None]
    include_dirs: NotRequired[bool | None]
    include_symlinks: NotRequired[bool | None]
    follow_symlinks: NotRequired[bool | None]
    canonicalize: NotRequired[bool | None]
    exts: NotRequired[list[str] | None]
    match: NotRequired[list[str] | None]
    skip: NotRequired[list[str] | None]


class ExpandGlobArgs(TypedDict):
    glob: str
    extended: NotRequired[bool | None]
    globstar: NotRequired[bool | None]
    case_insensitive: NotRequired[bool | None]
    root: NotRequired[str | None]
    exclude: NotRequired[list[str] | None]
    include_dirs: NotRequired[bool | None]
    follow_symlinks: NotRequired[bool | None]
    canonicalize: NotRequired[bool | None]


class SpawnArgs(TypedDict):
    command: str
    args: NotRequired[list[str] | None]
    env: NotRequired[dict[str, str] | None]
    clear_env: NotRequired[bool | None]
    cwd: NotRequired[str | None]
    stdin_stream_id: NotRequired[int | None]
    stdout: NotRequired[Literal["piped", "null", "inherit"] | None]
    stderr: NotRequired[Literal["piped", "null", "inherit"] | None]


class ProcessSpawnResult(TypedDict):
    pid: int
    stdout_stream_id: NotRequired[int | None]
    stderr_stream_id: NotRequired[int | None]


class WaitArgs(TypedDict):
    pid: int
    vscode: NotRequired[bool | None]


class ProcessWaitResult(TypedDict):
    success: bool
    code: int
    signal: NotRequired[str | None]


class KillArgs(TypedDict):
    pid: int
    signal: NotRequired[str | None]
    vscode: NotRequired[bool | None]


class RunArgs(TypedDict):
    code: str
    extension: Literal["js", "cjs", "mjs", "ts", "cts", "mts", "jsx", "tsx"]
    env: NotRequired[dict[str, str] | None]
    clear_env: NotRequired[bool | None]
    cwd: NotRequired[str | None]
    stdin_stream_id: NotRequired[int | None]
    stdout: NotRequired[Literal["piped", "null", "inherit"] | None]
    stderr: NotRequired[Literal["piped", "null", "inherit"] | None]
    script_args: NotRequired[list[str] | None]
    entrypoint: NotRequired[str | None]


class DenoRunResult(TypedDict):
    pid: int
    stdout_stream_id: NotRequired[int | None]
    stderr_stream_id: NotRequired[int | None]


class DenoHttpWaitArgs(TypedDict):
    pid: int


class SpawnDenoReplArgs(TypedDict):
    env: NotRequired[dict[str, str] | None]
    clear_env: NotRequired[bool | None]
    cwd: NotRequired[str | None]
    stdin_stream_id: NotRequired[int | None]
    stdout: NotRequired[Literal["piped", "null", "inherit"] | None]
    stderr: NotRequired[Literal["piped", "null", "inherit"] | None]
    script_args: NotRequired[list[str] | None]


class DenoSpawnDenoReplResult(TypedDict):
    pid: int
    stdout_stream_id: NotRequired[int | None]
    stderr_stream_id: NotRequired[int | None]


class DenoReplCloseArgs(TypedDict):
    pid: int


class DenoReplEvalArgs(TypedDict):
    pid: int
    code: str


class DenoReplCallArgs(TypedDict):
    pid: int
    fn: str
    args: list[Any]


class FetchArgs(TypedDict):
    url: str
    method: str
    headers: dict[str, str]
    redirect: Literal["follow", "manual"]
    abort_id: NotRequired[int | None]
    body_stream_id: NotRequired[int | None]
    pid: NotRequired[int | None]


class NetFetchResult(TypedDict):
    status: int
    status_text: str
    headers: dict[str, str]
    body_stream_id: NotRequired[int | None]


class ExposeHttpArgs(TypedDict):
    domain: str
    port: NotRequired[int | None]
    pid: NotRequired[int | None]


class ConnectArgs(TypedDict):
    path: str
    extensions: list[str]
    env: NotRequired[dict[str, str] | None]
    preview: NotRequired[str | None]
    disable_stop_button: NotRequired[bool | None]
    editor_settings: NotRequired[dict[str, Any] | None]


class VscodeConnectResult(TypedDict):
    pid: int
    port: int
    stdout_stream_id: int
    stderr_stream_id: int


class GetArgs(TypedDict):
    key: str


class SetArgs(TypedDict):
    key: str
    value: str


class DeleteArgs(TypedDict):
    key: str
