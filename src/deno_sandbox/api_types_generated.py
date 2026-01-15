# ATTENTION: This file is auto-generated. Do not edit it manually.


from typing_extensions import TypedDict, NotRequired, Literal
from re import Pattern
from deno_sandbox.wrappers import AbortSignal


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
    slug: NotRequired[str | None]


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


class VolumeInit(TypedDict):
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


class SecretConfig(TypedDict):
    hosts: list[str]


class SandboxCreateOptions(TypedDict):
    region: NotRequired[str | None]
    env: NotRequired[dict[str, str] | None]
    timeout: NotRequired[str | None]
    memory_db: NotRequired[str | None]
    debug: NotRequired[bool | None]
    labels: NotRequired[dict[str, str] | None]
    volumes: NotRequired[dict[str, str] | None]
    allow_net: NotRequired[list[str] | None]
    secrets: NotRequired[dict[str, SecretConfig] | None]
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


class SpawnOptions(TypedDict):
    args: list[str]
    cwd: NotRequired[str | None]
    clear_env: NotRequired[bool | None]
    env: NotRequired[dict[str, str] | None]
    signal: NotRequired[AbortSignal | None]
    stdin: NotRequired[Literal["piped", "null"] | None]
    stdout: NotRequired[Literal["piped", "null", "inherit"] | None]
    stderr: NotRequired[Literal["piped", "null", "inherit"] | None]


class ReadFileOptions(TypedDict):
    signal: AbortSignal


class WriteFileOptions(TypedDict):
    create: NotRequired[bool | None]
    append: NotRequired[bool | None]
    create_new: NotRequired[bool | None]
    mode: NotRequired[int | None]


class DirEntry(TypedDict):
    name: str
    is_file: bool
    is_directory: bool
    is_symlink: bool


class RemoveOptions(TypedDict):
    recursive: NotRequired[bool | None]


class MkdirOptions(TypedDict):
    recursive: NotRequired[bool | None]
    mode: NotRequired[int | None]


class WalkOptions(TypedDict):
    max_depth: NotRequired[int | None]
    include_files: NotRequired[bool | None]
    include_dirs: NotRequired[bool | None]
    include_symlinks: NotRequired[bool | None]
    follow_symlinks: NotRequired[bool | None]
    canonicalize: NotRequired[bool | None]
    exts: NotRequired[list[str] | None]
    match: NotRequired[list[Pattern] | None]
    skip: NotRequired[list[Pattern] | None]


class WalkEntry(TypedDict):
    path: str
    name: str
    is_file: bool
    is_directory: bool
    is_symlink: bool


class ExpandGlobOptions(TypedDict):
    root: NotRequired[str | None]
    exclude: NotRequired[list[str] | None]
    include_dirs: NotRequired[bool | None]
    follow_symlinks: NotRequired[bool | None]
    canonicalize: NotRequired[bool | None]
    extended: NotRequired[bool | None]
    globstar: NotRequired[bool | None]
    case_insensitive: NotRequired[bool | None]


class MakeTempDirOptions(TypedDict):
    dir: NotRequired[str | None]
    prefix: NotRequired[str | None]
    suffix: NotRequired[str | None]


class MakeTempFileOptions(TypedDict):
    dir: NotRequired[str | None]
    prefix: NotRequired[str | None]
    suffix: NotRequired[str | None]


class FsOpenOptions(TypedDict):
    read: NotRequired[bool | None]
    write: NotRequired[bool | None]
    append: NotRequired[bool | None]
    truncate: NotRequired[bool | None]
    create: NotRequired[bool | None]
    create_new: NotRequired[bool | None]
    mode: NotRequired[int | None]


class SymlinkOptions(TypedDict):
    type: NotRequired[Literal["file", "dir", "junction"] | None]


class DenoRunOptions(TypedDict):
    cwd: NotRequired[str | None]
    clear_env: NotRequired[bool | None]
    env: NotRequired[dict[str, str] | None]
    signal: NotRequired[AbortSignal | None]
    stdin: NotRequired[Literal["piped", "null"] | None]
    stdout: NotRequired[Literal["piped", "null", "inherit"] | None]
    stderr: NotRequired[Literal["piped", "null", "inherit"] | None]
    script_args: NotRequired[list[str] | None]
    entrypoint: NotRequired[str | None]
    code: NotRequired[str | None]
    extension: NotRequired[
        Literal["js", "cjs", "mjs", "ts", "cts", "mts", "jsx", "tsx"] | None
    ]


class DenoReplOptions(TypedDict):
    cwd: NotRequired[str | None]
    clear_env: NotRequired[bool | None]
    env: NotRequired[dict[str, str] | None]
    signal: NotRequired[AbortSignal | None]
    stdin: NotRequired[Literal["piped", "null"] | None]
    stdout: NotRequired[Literal["piped", "null", "inherit"] | None]
    stderr: NotRequired[Literal["piped", "null", "inherit"] | None]
    script_args: NotRequired[list[str] | None]


class DeployBuildOptions(TypedDict):
    mode: NotRequired[Literal["none"] | None]
    entrypoint: NotRequired[str | None]
    args: NotRequired[list[str] | None]


class DeployOptions(TypedDict):
    path: NotRequired[str | None]
    production: NotRequired[bool | None]
    build: NotRequired[DeployBuildOptions | None]
