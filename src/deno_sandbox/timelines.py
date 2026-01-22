from __future__ import annotations

from typing import TYPE_CHECKING
from typing_extensions import Optional

from .api_types_generated import (
    Timeline,
    TimelineListOptions,
)

if TYPE_CHECKING:
    from .console import (
        AsyncConsoleClient,
        AsyncPaginatedList,
        ConsoleClient,
        PaginatedList,
    )


class Timelines:
    def __init__(self, client: ConsoleClient):
        self._client = client

    def list(
        self, app: str, options: Optional[TimelineListOptions] = None
    ) -> PaginatedList[Timeline, TimelineListOptions]:
        """List timelines for a specific app."""

        result = self._client._timelines_list(app, options)

        return result


class AsyncTimelines:
    def __init__(self, client: AsyncConsoleClient):
        self._client = client

    async def list(
        self, app: str, options: Optional[TimelineListOptions] = None
    ) -> AsyncPaginatedList[Timeline, TimelineListOptions]:
        """List timelines for a specific app."""

        result = await self._client._timelines_list(app, options)

        return result
