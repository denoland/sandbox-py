# ATTENTION: This file is auto-generated. Do not edit it manually.

from __future__ import annotations

from typing_extensions import TypedDict, NotRequired, Literal


class App(TypedDict):
    id: str
    """The unique identifier for the app."""

    slug: str
    """The human readable identifier for the app."""

    created_at: str
    """The ISO 8601 timestamp when the app was created."""

    updated_at: str
    """The ISO 8601 timestamp when the app was last updated."""


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


class RevisionWithoutTimelines(TypedDict):
    id: str
    """The unique identifier for the revision."""

    status: Literal["building", "ready", "error"]
    """The status of the revision."""

    created_at: str
    """The ISO 8601 timestamp when the revision was created."""

    updated_at: str
    """The ISO 8601 timestamp when the revision was last updated."""


class BaseSnapshot(TypedDict):
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

    base_snapshot: NotRequired[BaseSnapshot | None]
    """The snapshot the volume was created from."""


class Snapshot(TypedDict):
    id: str
    """The unique identifier for the snapshot."""

    slug: str
    """The human readable identifier for the snapshot."""

    region: str
    """The region the snapshot is located in."""

    allocated_size: int
    """
  The number of bytes currently allocated specifically for the snapshot.

  Snapshots created from other snapshots only store data that is different
  from their base snapshot, so this size may be smaller than the actual size
  of the file system on the snapshot.
  This is not the total size of the snapshot.
  """

    flattened_size: int
    """
  The total size of the file system on the snapshot, in bytes. This is the size the snapshot would take up if it were fully "flattened" (i.e., if all data from any snapshots it was created from were fully stored in this snapshot).

  Snapshots created from other snapshots only store data that is different from their base snapshot, so this size may be larger than the amount of data actually allocated for the snapshot.
  """

    is_bootable: bool
    """Whether the snapshot is bootable."""

    base_snapshot: BaseSnapshot
    """The snapshot the volume was created from."""


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


class DirEntry(TypedDict):
    name: str
    """The file or directory name."""

    is_file: bool
    """Whether the entry is a file."""

    is_directory: bool
    """Whether the entry is a directory."""

    is_symlink: bool
    """Whether the entry is a symbolic link."""


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


class FsFileHandle(TypedDict):
    file_handle_id: int
