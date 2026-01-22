from __future__ import annotations

from typing import TYPE_CHECKING, cast
from typing_extensions import Optional

from .api_types_generated import (
    VolumeInit,
    Volume,
    VolumeListOptions,
    SnapshotInit,
)
from .utils import convert_to_snake_case

if TYPE_CHECKING:
    from .console import (
        AsyncConsoleClient,
        AsyncPaginatedList,
        ConsoleClient,
        PaginatedList,
    )


class Volumes:
    def __init__(self, client: ConsoleClient):
        self._client = client

    def create(self, options: VolumeInit) -> Volume:
        """Create a new volume."""

        result = self._client._volumes_create(options)

        raw_result = convert_to_snake_case(result)
        return cast(Volume, raw_result)

    def get(self, id_or_slug: str) -> Volume:
        """Get volume info by ID or slug."""

        result = self._client._volumes_get(id_or_slug)

        raw_result = convert_to_snake_case(result)
        return cast(Volume, raw_result)

    def list(
        self, options: Optional[VolumeListOptions] = None
    ) -> PaginatedList[Volume, VolumeListOptions]:
        result = self._client._volumes_list(options)

        return result

    def delete(self, id_or_slug: str) -> None:
        """Delete volume by ID or slug."""

        self._client._volumes_delete(id_or_slug)

    def snapshot(self, id_or_slug: str, init: SnapshotInit) -> None:
        """Create a snapshot of a volume by ID or slug."""

        self._client._volumes_snapshot(id_or_slug, init)


class AsyncVolumes:
    def __init__(self, client: AsyncConsoleClient):
        self._client = client

    async def create(self, options: VolumeInit) -> Volume:
        """Create a new volume."""

        result = await self._client._volumes_create(options)

        raw_result = convert_to_snake_case(result)
        return cast(Volume, raw_result)

    async def get(self, id_or_slug: str) -> Volume:
        """Get volume info by ID or slug."""

        result = await self._client._volumes_get(id_or_slug)

        raw_result = convert_to_snake_case(result)
        return cast(Volume, raw_result)

    async def list(
        self, options: Optional[VolumeListOptions] = None
    ) -> AsyncPaginatedList[Volume, VolumeListOptions]:
        result = await self._client._volumes_list(options)

        return result

    async def delete(self, id_or_slug: str) -> None:
        """Delete volume by ID or slug."""

        await self._client._volumes_delete(id_or_slug)

    async def snapshot(self, id_or_slug: str, init: SnapshotInit) -> None:
        """Create a snapshot of a volume by ID or slug."""

        await self._client._volumes_snapshot(id_or_slug, init)
