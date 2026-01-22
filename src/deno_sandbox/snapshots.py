from __future__ import annotations

from typing import cast
from typing_extensions import Optional

from .console import (
    AsyncConsoleClient,
    AsyncPaginatedList,
    ConsoleClient,
    PaginatedList,
)

from .api_types_generated import (
    Snapshot,
    SnapshotListOptions,
)
from .utils import convert_to_snake_case


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
        return await self._client.get_paginated(
            "/api/v2/snapshots", cursor=None, params=options
        )

    async def delete(self, id_or_slug: str) -> None:
        """Delete snapshot by ID or slug."""
        await self._client.delete(f"/api/v2/snapshots/{id_or_slug}")


class Snapshots:
    def __init__(self, client: ConsoleClient):
        self._client = client
        self._async = AsyncSnapshots(client._async)

    def get(self, id_or_slug: str) -> Snapshot | None:
        """Get a snapshot by ID or slug."""
        return self._client._bridge.run(self._async.get(id_or_slug))

    def list(
        self, options: Optional[SnapshotListOptions] = None
    ) -> PaginatedList[Snapshot, SnapshotListOptions]:
        """List snapshots."""

        paginated = self._client._bridge.run(self._async.list(options))
        return PaginatedList(self._client._bridge, paginated)

    def delete(self, id_or_slug: str) -> None:
        """Delete snapshot by ID or slug."""
        self._client._bridge.run(self._async.delete(id_or_slug))
