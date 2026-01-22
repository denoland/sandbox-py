from __future__ import annotations

from typing import cast
from typing_extensions import Optional

from .api_types_generated import (
    VolumeInit,
    Volume,
    VolumeListOptions,
    SnapshotInit,
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

    async def create(self, options: VolumeInit) -> Volume:
        """Create a new volume."""
        params = {
            "slug": options["slug"],
            "capacity": options["capacity"],
            "region": options["region"],
        }
        if options.get("from_snapshot") is not None:
            params["from"] = options["from_snapshot"]

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
        self, options: Optional[VolumeListOptions] = None
    ) -> AsyncPaginatedList[Volume, VolumeListOptions]:
        """List volumes."""
        return await self._client.get_paginated(
            "/api/v2/volumes", cursor=None, params=options
        )

    async def delete(self, id_or_slug: str) -> None:
        """Delete volume by ID or slug."""
        await self._client.delete(f"/api/v2/volumes/{id_or_slug}")

    async def snapshot(self, id_or_slug: str, init: SnapshotInit) -> Snapshot:
        """Create a snapshot of a volume by ID or slug."""
        result = await self._client.post(f"/api/v2/volumes/{id_or_slug}/snapshot", init)
        raw_result = convert_to_snake_case(result)
        return cast(Snapshot, raw_result)


class Volumes:
    def __init__(self, client: AsyncConsoleClient, bridge: AsyncBridge):
        self._client = client
        self._bridge = bridge
        self._async = AsyncVolumes(client)

    def create(self, options: VolumeInit) -> Volume:
        """Create a new volume."""
        return self._bridge.run(self._async.create(options))

    def get(self, id_or_slug: str) -> Volume | None:
        """Get volume info by ID or slug."""
        return self._bridge.run(self._async.get(id_or_slug))

    def list(
        self, options: Optional[VolumeListOptions] = None
    ) -> PaginatedList[Volume, VolumeListOptions]:
        """List volumes."""

        paginated = self._bridge.run(self._async.list(options))
        return PaginatedList(self._bridge, paginated)

    def delete(self, id_or_slug: str) -> None:
        """Delete volume by ID or slug."""
        self._bridge.run(self._async.delete(id_or_slug))

    def snapshot(self, id_or_slug: str, init: SnapshotInit) -> Snapshot:
        """Create a snapshot of a volume by ID or slug."""
        return self._bridge.run(self._async.snapshot(id_or_slug, init))
