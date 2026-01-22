from __future__ import annotations

from typing import Any, Union, cast
from typing_extensions import Optional

from .api_types_generated import (
    Volume,
    Snapshot,
)
from .utils import convert_to_snake_case

from .bridge import AsyncBridge
from .console import (
    AsyncConsoleClient,
    AsyncPaginatedList,
    PaginatedList,
)


class AsyncVolumes:
    def __init__(self, client: AsyncConsoleClient):
        self._client = client

    async def create(
        self,
        slug: str,
        region: str,
        capacity: Union[int, str],
        *,
        from_snapshot: Optional[str] = None,
    ) -> Volume:
        """Create a new volume.

        Args:
            slug: Human readable identifier for the volume.
            region: The region to create the volume in.
            capacity: The capacity of the volume in bytes. When passing a string you can use these units too: GB, MB, kB, GiB, MiB, KiB.
            from_snapshot: The ID or slug of the snapshot to create the volume from.
        """
        params: dict[str, Any] = {
            "slug": slug,
            "capacity": capacity,
            "region": region,
        }
        if from_snapshot is not None:
            params["from"] = from_snapshot

        result = await self._client.post("/api/v2/volumes", params)
        raw_result = convert_to_snake_case(result)
        return cast(Volume, raw_result)

    async def get(self, id_or_slug: str) -> Volume | None:
        """Get volume info by ID or slug."""
        result = await self._client.get_or_none(f"/api/v2/volumes/{id_or_slug}")
        if result is None:
            return None
        raw_result = convert_to_snake_case(result)
        return cast(Volume, raw_result)

    async def list(
        self,
        *,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        search: Optional[str] = None,
    ) -> AsyncPaginatedList[Volume]:
        """List volumes.

        Args:
            cursor: The cursor for pagination.
            limit: Limit the number of volumes to return.
            search: The search query to filter volumes by.
        """
        options: dict[str, Any] = {}
        if cursor is not None:
            options["cursor"] = cursor
        if limit is not None:
            options["limit"] = limit
        if search is not None:
            options["search"] = search

        result: AsyncPaginatedList[Volume] = await self._client.get_paginated(
            "/api/v2/volumes", cursor=None, params=options if options else None
        )

        return result

    async def delete(self, id_or_slug: str) -> None:
        """Delete volume by ID or slug."""
        await self._client.delete(f"/api/v2/volumes/{id_or_slug}")

    async def snapshot(
        self,
        id_or_slug: str,
        *,
        slug: str,
    ) -> Snapshot:
        """Create a snapshot of a volume by ID or slug.

        Args:
            id_or_slug: The volume ID or slug to snapshot.
            slug: Human readable identifier for the snapshot.
        """
        params: dict[str, Any] = {"slug": slug}
        result = await self._client.post(
            f"/api/v2/volumes/{id_or_slug}/snapshot", params
        )
        raw_result = convert_to_snake_case(result)
        return cast(Snapshot, raw_result)


class Volumes:
    def __init__(self, client: AsyncConsoleClient, bridge: AsyncBridge):
        self._client = client
        self._bridge = bridge
        self._async = AsyncVolumes(client)

    def create(
        self,
        slug: str,
        region: str,
        capacity: Union[int, str],
        *,
        from_snapshot: Optional[str] = None,
    ) -> Volume:
        """Create a new volume.

        Args:
            slug: Human readable identifier for the volume.
            region: The region to create the volume in.
            capacity: The capacity of the volume in bytes. When passing a string you can use these units too: GB, MB, kB, GiB, MiB, KiB.
            from_snapshot: The ID or slug of the snapshot to create the volume from.
        """
        return self._bridge.run(
            self._async.create(slug, region, capacity, from_snapshot=from_snapshot)
        )

    def get(self, id_or_slug: str) -> Volume | None:
        """Get volume info by ID or slug."""
        return self._bridge.run(self._async.get(id_or_slug))

    def list(
        self,
        *,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        search: Optional[str] = None,
    ) -> PaginatedList[Volume]:
        """List volumes.

        Args:
            cursor: The cursor for pagination.
            limit: Limit the number of volumes to return.
            search: The search query to filter volumes by.
        """
        paginated = self._bridge.run(
            self._async.list(cursor=cursor, limit=limit, search=search)
        )
        return PaginatedList(self._bridge, paginated)

    def delete(self, id_or_slug: str) -> None:
        """Delete volume by ID or slug."""
        self._bridge.run(self._async.delete(id_or_slug))

    def snapshot(
        self,
        id_or_slug: str,
        *,
        slug: str,
    ) -> Snapshot:
        """Create a snapshot of a volume by ID or slug.

        Args:
            id_or_slug: The volume ID or slug to snapshot.
            slug: Human readable identifier for the snapshot.
        """
        return self._bridge.run(self._async.snapshot(id_or_slug, slug=slug))
