# ATTENTION: This file is auto-generated. Do not edit it manually.


from typing_extensions import TypedDict, NotRequired, Literal
from re import Pattern
from deno_sandbox.wrappers import AbortSignal


class App(TypedDict):
    id: str
    """The unique identifier for the app."""

    slug: str
    """The human readable identifier for the app."""

    created_at: str
    """The ISO 8601 timestamp when the app was created."""

    updated_at: str
    """The ISO 8601 timestamp when the app was last updated."""


class AppListOptions(TypedDict):
    """Pagination options."""

    cursor: NotRequired[str | None]
    """The cursor for pagination."""

    limit: NotRequired[int | None]
    """Limit the number of items to return."""


class AppInit(TypedDict):
    slug: NotRequired[str | None]
    """Human readable identifier for the app."""


class AppUpdate(TypedDict):
    slug: NotRequired[str | None]
    """Human readable identifier for the app."""


class TimelineApp(TypedDict):
    id: str
    """The unique identifier for the app."""

    slug: str
    """The human readable identifier for the app."""


class TimelineContext(TypedDict):
    slug: str


class Domain(TypedDict):
    domain: str
    """The domain name."""


class Timeline(TypedDict):
    slug: str
    """The unique identifier for the timeline."""

    partition: dict[str, str]
    """The partition of the timeline."""

    app: TimelineApp
    context: TimelineContext
    """The context of the timeline."""

    domains: list[Domain]
    """The domains associated with the timeline."""


class Revision(TypedDict):
    id: str
    """The unique identifier for the revision."""

    status: Literal["building", "ready", "error"]
    """The status of the revision."""

    timelines: list[Timeline]
    """The timelines associated with the revision."""

    created_at: str
    """The ISO 8601 timestamp when the revision was created."""

    updated_at: str
    """The ISO 8601 timestamp when the revision was last updated."""


class RevisionListOptions(TypedDict):
    """Pagination options."""

    cursor: NotRequired[str | None]
    """The cursor for pagination."""

    limit: NotRequired[int | None]
    """Limit the number of items to return."""


class RevisionWithoutTimelines(TypedDict):
    id: str
    """The unique identifier for the revision."""

    status: Literal["building", "ready", "error"]
    """The status of the revision."""

    created_at: str
    """The ISO 8601 timestamp when the revision was created."""

    updated_at: str
    """The ISO 8601 timestamp when the revision was last updated."""


class TimelineListOptions(TypedDict):
    """Pagination options."""

    cursor: NotRequired[str | None]
    """The cursor for pagination."""

    limit: NotRequired[int | None]
    """Limit the number of items to return."""


class VolumeInit(TypedDict):
    slug: str
    """Human readable identifier for the volume."""

    region: str
    """The region to create the volume in."""

    capacity: int | str
    """The capacity of the volume in bytes. When passing a string you can use these units too: GB, MB, kB, GiB, MiB, KiB"""


class VolumeSnapshot(TypedDict):
    id: str
    """The unique identifier for the snapshot."""

    slug: str
    """Human readable identifier for the snapshot."""


class Volume(TypedDict):
    id: str
    """The unique identifier for the volume."""

    slug: str
    """Human readable identifier for the volume."""

    region: str
    """The region the volume is located in."""

    capacity: int
    """The capacity of the volume in bytes."""

    estimated_allocated_size: int
    """
  The number of bytes currently allocated specifically for the volume.
  
  Volumes created from snapshots are "copy-on-write", so this size may be
  smaller than the actual size of the file system on the volume, as it does
  not include data shared with any snapshots the volume was created from.
  
  This is an estimate, and may lag real-time usage by multiple minutes.
  """

    estimated_flattened_size: int
    """
  The total size of the file system on the volume, in bytes. This is the size
  the volume would take up if it were fully "flattened" (i.e., if all data
  from any snapshots it was created from were fully copied to the volume).
  
  Volumes created from snapshots are "copy-on-write", so this size may be
  larger than the amount of data actually allocated for the volume.
  
  This is an estimate, and may lag real-time usage by multiple minutes.
  """

    is_bootable: bool
    """Whether the volume is bootable."""

    base_snapshot: VolumeSnapshot
    """The snapshot the volume was created from."""


class VolumeListOptions(TypedDict):
    cursor: NotRequired[str | None]
    """The cursor for pagination."""

    limit: NotRequired[int | None]
    """Limit the number of volumes to return."""

    search: NotRequired[str | None]
    """The search query to filter volumes by."""


class SecretConfig(TypedDict):
    hosts: list[str]
    """
  List of hostnames where this secret can be used. Must have at least one host.
  
  Examples:
  - ["api.openai.com"]
  - ["api.github.com", "github.com"]
  """


class SandboxCreateOptions(TypedDict):
    region: NotRequired[str | None]
    """If the sandbox was created in a non-default region, the region where the sandbox is running. If this is set incorrectly, connection will fail."""

    env: NotRequired[dict[str, str] | None]
    """Environment variables to start the sandbox with, in addition to the default environment variables such as `DENO_DEPLOY_ORGANIZATION_ID`."""

    timeout: NotRequired[str | None]
    """
  The timeout of the sandbox. When not specified, it defaults to "session".
  
  "session" means the sandbox will be destroyed when the primary client disconnects. "Primary" client is the client that created the sandbox with .create() as opposed to secondary clients that connect with .connect().
  
  Other possible values are durations like "30s" (30 Seconds) or "2m" (2 minutes), after which the sandbox will be automatically destroyed.
  """

    memory_db: NotRequired[str | None]
    """
  The memory size in MiB of the sandbox. When not specified, it defaults to the default value (1280). Example values: 1024, 4096
                
  """

    debug: NotRequired[bool | None]
    """Enable debug logging for the sandbox connection."""

    labels: NotRequired[dict[str, str] | None]
    """Labels to set on the sandbox. Up to 5 labels can be specified. Each label key must be at most 64 bytes, and each label value must be at most 128 bytes."""

    volumes: NotRequired[dict[str, str] | None]
    """
  Volumes to mount on the sandbox.
                
                The key is the mount path inside the sandbox, and the value is the volume ID or slug.
  """

    allow_net: NotRequired[list[str] | None]
    """
  List of hostnames / IP addresses with optional port numbers that the sandbox can make outbound network requests to.
  
  If not specified, no network restrictions are applied.
  
  Examples:
  - "example.com"
  - "*.example.com"
  - "example.com:443"
  - "203.0.113.110"
  - "[2001:db8::1]:80"
  """

    secrets: NotRequired[dict[str, SecretConfig] | None]
    """Secret environment variables that are never exposed to sandbox code. The real secret values are injected on the wire when the sandbox makes HTTPS requests to the specified hosts. The key is the environment variable name."""

    ssh: NotRequired[bool | None]
    """Whether to expose SSH access to the sandbox. If true, the `ssh` property will be populated once the sandbox is ready."""

    port: NotRequired[int | None]
    """The port number to expose for HTTP access. If specified, `url` property will be populated once the sandbox is ready, and can be used to access the sandbox over HTTP."""

    token: NotRequired[str | None]
    """
  The Deno Deploy access token that should be used to authenticate requests.
  
  - When passing an organization token (starts with `ddo_`), no further organization information is required.
  - When passing a personal token (starts with `ddp_`), the `org` option must also be provided.
  """

    org: NotRequired[str | None]
    """
  The Deno Deploy organization slug to operate within. This is required when
  using a personal access token.
  
  If not provided, the `DENO_DEPLOY_ORG` environment variable will be used.
  """


class SandboxConnectOptions(TypedDict):
    id: str
    """The unique id of the sandbox to connect to."""

    region: NotRequired[str | None]
    """If the sandbox was created in a non-default region, the region where the sandbox is running. If this is set incorrectly, connection will fail."""

    debug: NotRequired[bool | None]
    """Enable debug logging for the sandbox connection."""

    ssh: NotRequired[bool | None]
    """Whether to expose SSH access to the sandbox. If true, the `ssh` property will be populated once the sandbox is ready."""

    token: NotRequired[str | None]
    """
  The Deno Deploy access token that should be used to authenticate requests.
  
  - When passing an organization token (starts with `ddo_`), no further organization information is required.
  - When passing a personal token (starts with `ddp_`), the `org` option must also be provided.
  """

    org: NotRequired[str | None]
    """
  The Deno Deploy organization slug to operate within. This is required when
  using a personal access token.
  
  If not provided, the `DENO_DEPLOY_ORG` environment variable will be used.
  """


class SandboxListOptions(TypedDict):
    labels: NotRequired[dict[str, str] | None]
    """Filter sandboxes by labels."""


class SandboxMeta(TypedDict):
    id: str
    """The unique identifier for the sandbox."""

    created_at: str
    """The ISO 8601 timestamp when the sandbox was created."""

    region: str
    """The region the sandbox is located in."""

    status: Literal["running", "stopped"]
    """The status of the sandbox."""

    stopped_at: NotRequired[str | None]
    """The ISO 8601 timestamp when the sandbox was stopped."""


class SpawnOptions(TypedDict):
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
    """Create file if it doesn't already exist."""

    append: NotRequired[bool | None]
    """Append content instead of overwriting existing contents."""

    create_new: NotRequired[bool | None]
    mode: NotRequired[int | None]
    """Set the file permission mode."""


class DirEntry(TypedDict):
    name: str
    """The file or directory name."""

    is_file: bool
    """Whether the entry is a file."""

    is_directory: bool
    """Whether the entry is a directory."""

    is_symlink: bool
    """Whether the entry is a symbolic link."""


class RemoveOptions(TypedDict):
    recursive: NotRequired[bool | None]
    """Whether to remove directories recursively. Default: false."""


class MkdirOptions(TypedDict):
    recursive: NotRequired[bool | None]
    """If true, parent directories will be created if they do not already exist."""

    mode: NotRequired[int | None]
    """Permissions to use for the new directory."""


class FileInfo(TypedDict):
    is_file: bool
    """Whether the path is a file."""

    is_directory: bool
    """Whether the path is a directory."""

    is_symlink: bool
    """Whether the path is a symbolic link."""

    size: int
    """The size of the file in bytes."""

    mtime: str
    """The last modification time of the file."""

    atime: str
    """The last access time of the file."""

    birthtime: str
    """The creation time of the file."""

    ctime: str
    """The last status change time of the file."""

    dev: int
    """The device ID."""

    ino: int
    """The inode number."""

    mode: int
    """The file mode."""

    nlink: int
    """The number of hard links pointing to this file."""

    uid: int
    """The user ID of the owner."""

    gid: int
    """The group ID of the owner."""

    rdev: int
    """The device ID of this file."""

    blksize: int
    """The block size for filesystem I/O."""

    blocks: int
    """The number of blocks allocated in 512-byte units"""

    is_block_device: bool
    """Whether the path is a block device."""

    is_char_device: bool
    """Whether the path is a character device."""

    is_fifo: bool
    """Whether the path is a FIFO."""

    is_socket: bool
    """Whether the path is a socket."""


class WalkOptions(TypedDict):
    max_depth: NotRequired[int | None]
    """The maximum depth to traverse. Default: Infinity."""

    include_files: NotRequired[bool | None]
    """Whether to include files in the results. Default: true."""

    include_dirs: NotRequired[bool | None]
    """Whether to include directories in the results. Default: true."""

    include_symlinks: NotRequired[bool | None]
    """Whether to include symbolic links in the results. Default: true."""

    follow_symlinks: NotRequired[bool | None]
    """Whether to follow symbolic links. Default: false."""

    canonicalize: NotRequired[bool | None]
    """Whether to return canonicalized paths. This option works only if `followSymlinks` is not `false`. Default: false."""

    exts: NotRequired[list[str] | None]
    """If provided, only files with the specified extensions will be included. Example: ['.ts', '.js']"""

    match: NotRequired[list[Pattern] | None]
    """List of regular expression patterns used to filter entries. If specified, entries that do not match the patterns specified by this option are excluded."""

    skip: NotRequired[list[Pattern] | None]
    """List of regular expression patterns used to filter entries. If specified, entries that match the patterns specified by this option are excluded."""


class WalkEntry(TypedDict):
    path: str
    """The full path of the entry."""

    name: str
    """The file or directory name."""

    is_file: bool
    """Whether the entry is a file."""

    is_directory: bool
    """Whether the entry is a directory."""

    is_symlink: bool
    """Whether the entry is a symbolic link."""


class ExpandGlobOptions(TypedDict):
    root: NotRequired[str | None]
    """The root directory from which to expand the glob pattern. Default is the current working directory."""

    exclude: NotRequired[list[str] | None]
    """An array of glob patterns to exclude from the results."""

    include_dirs: NotRequired[bool | None]
    """Whether to include directories in the results. Default: true."""

    follow_symlinks: NotRequired[bool | None]
    """Whether to follow symbolic links. Default: false."""

    canonicalize: NotRequired[bool | None]
    """Whether to return canonicalized paths. This option works only if `followSymlinks` is not `false`. Default: true."""

    extended: NotRequired[bool | None]
    """Whether to enable extended glob syntax, see https://www.linuxjournal.com/content/bash-extended-globbing . Default: true."""

    globstar: NotRequired[bool | None]
    """Globstar syntax. See https://www.linuxjournal.com/content/globstar-new-bash-globbing-option. If false, `**` is treated like `*`. Default: true."""

    case_insensitive: NotRequired[bool | None]
    """Whether the glob matching should be case insensitive. Default: false."""


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
    """Sets the option for read access. This option, when `true`, means that the file should be read-able if opened. Default: true."""

    write: NotRequired[bool | None]
    """Sets the option for write access. This option, when `true`, means that the file should be write-able if opened. Default: false."""

    append: NotRequired[bool | None]
    """Sets the option for append mode. This option, when `true`, means that writes to the file will always append to the end. Default: false."""

    truncate: NotRequired[bool | None]
    """If `true`, and the file already exists and is a regular file, it will be truncated to length 0 when opened. Default: false."""

    create: NotRequired[bool | None]
    """If `true`, the file will be created if it does not already exist. Default: false."""

    create_new: NotRequired[bool | None]
    """If `true`, the file will be created if it does not already exist. Default: false."""

    mode: NotRequired[int | None]
    """The permission mode to use when creating the file."""


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
    """Arguments to pass to the Deno runtime, after the entrypoint. This entire array will be available to the script as `process.args` and `Deno.args`"""

    entrypoint: NotRequired[str | None]
    """A module to read from disk and execute as the entrypoint of the Deno runtime. If this is specified, `code` must not be specified."""

    code: NotRequired[str | None]
    """Deno code to execute as the entrypoint of the Deno runtime. If this is specified, `entrypoint` must not be specified."""

    extension: NotRequired[
        Literal["js", "cjs", "mjs", "ts", "cts", "mts", "jsx", "tsx"] | None
    ]
    """Which file extension to use when executing the code. If no extension is specified, the default is `ts`."""


class DenoReplOptions(TypedDict):
    cwd: NotRequired[str | None]
    clear_env: NotRequired[bool | None]
    env: NotRequired[dict[str, str] | None]
    signal: NotRequired[AbortSignal | None]
    stdin: NotRequired[Literal["piped", "null"] | None]
    stdout: NotRequired[Literal["piped", "null", "inherit"] | None]
    stderr: NotRequired[Literal["piped", "null", "inherit"] | None]
    script_args: NotRequired[list[str] | None]
    """Arguments to pass to the Deno runtime, after the entrypoint. This entire array will be available to the script as `process.args` and `Deno.args`"""


class DeployBuildOptions(TypedDict):
    mode: NotRequired[Literal["none"] | None]
    """The build mode to use. Currently only `none` is supported. Default: `none`."""

    entrypoint: NotRequired[str | None]
    """The entrypoint file path relative to the `path` option. Default: main.ts"""

    args: NotRequired[list[str] | None]
    """Arguments to pass to the entrypoint script."""


class DeployOptions(TypedDict):
    path: NotRequired[str | None]
    """The path to the directory to deploy. If the path is relative, it is relative to /app. If the path is absolute, it is used as is. Default: ."""

    production: NotRequired[bool | None]
    """Whether to deploy in production mode. Default: false."""

    build: NotRequired[DeployBuildOptions | None]
    """Build options to use."""
