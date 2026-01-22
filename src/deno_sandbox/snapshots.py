from __future__ import annotations

from typing import TYPE_CHECKING, cast
from typing_extensions import Optional

from .api_types_generated import (
    Snapshot,
    SnapshotListOptions,
)
from .utils import convert_to_snake_case

if TYPE_CHECKING:
    from .console import (
        AsyncConsoleClient,
        AsyncPaginatedList,
        ConsoleClient,
        PaginatedList,
    )


class Snapshots:
    def __init__(self, client: ConsoleClient):
        self._client = client

    def get(self, id_or_slug: str) -> Snapshot:
        """Get a snapshot by ID or slug."""

        result = self._client._snapshots_get(id_or_slug)

        raw_result = convert_to_snake_case(result)
        return cast(Snapshot, raw_result)

    def list(
        self, options: Optional[SnapshotListOptions] = None
    ) -> PaginatedList[Snapshot, SnapshotListOptions]:
        """List snapshots."""

        result = self._client._snapshots_list(options)

        return result

    def delete(self, id_or_slug: str) -> None:
        """Delete snapshot by ID or slug."""

        self._client._snapshots_delete(id_or_slug)


class AsyncSnapshots:
    def __init__(self, client: AsyncConsoleClient):
        self._client = client

    async def get(self, id_or_slug: str) -> Snapshot:
        """Get a snapshot by ID or slug."""

        result = await self._client._snapshots_get(id_or_slug)

        raw_result = convert_to_snake_case(result)
        return cast(Snapshot, raw_result)

    async def list(
        self, options: Optional[SnapshotListOptions] = None
    ) -> AsyncPaginatedList[Snapshot, SnapshotListOptions]:
        """List snapshots."""

        result = await self._client._snapshots_list(options)

        return result

    async def delete(self, id_or_slug: str) -> None:
        """Delete snapshot by ID or slug."""

        await self._client._snapshots_delete(id_or_slug)
