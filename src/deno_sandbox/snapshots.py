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

    def get(self, id_or_slug: str) -> Snapshot | None:
        """Get a snapshot by ID or slug."""
        result = self._client._bridge.run(
            self._client._async.get_or_none(f"/api/v2/snapshots/{id_or_slug}")
        )
        if result is None:
            return None
        raw_result = convert_to_snake_case(result)
        return cast(Snapshot, raw_result)

    def list(
        self, options: Optional[SnapshotListOptions] = None
    ) -> PaginatedList[Snapshot, SnapshotListOptions]:
        """List snapshots."""
        from .console import PaginatedList

        paginated = self._client._bridge.run(
            self._client._async.get_paginated("/api/v2/snapshots", cursor=None, params=options)
        )
        return PaginatedList(self._client._bridge, paginated)

    def delete(self, id_or_slug: str) -> None:
        """Delete snapshot by ID or slug."""
        self._client._bridge.run(
            self._client._async.delete(f"/api/v2/snapshots/{id_or_slug}")
        )


class AsyncSnapshots:
    def __init__(self, client: AsyncConsoleClient):
        self._client = client

    async def get(self, id_or_slug: str) -> Snapshot | None:
        """Get a snapshot by ID or slug."""
        result = await self._client.get_or_none(f"/api/v2/snapshots/{id_or_slug}")
        if result is None:
            return None
        raw_result = convert_to_snake_case(result)
        return cast(Snapshot, raw_result)

    async def list(
        self, options: Optional[SnapshotListOptions] = None
    ) -> AsyncPaginatedList[Snapshot, SnapshotListOptions]:
        """List snapshots."""
        return await self._client.get_paginated("/api/v2/snapshots", cursor=None, params=options)

    async def delete(self, id_or_slug: str) -> None:
        """Delete snapshot by ID or slug."""
        await self._client.delete(f"/api/v2/snapshots/{id_or_slug}")
