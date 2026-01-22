from __future__ import annotations

from typing_extensions import Optional

from .api_types_generated import (
    Timeline,
    TimelineListOptions,
)

from .bridge import AsyncBridge
from .console import (
    AsyncConsoleClient,
    AsyncPaginatedList,
    PaginatedList,
)


class AsyncTimelines:
    def __init__(self, client: AsyncConsoleClient):
        self._client = client

    async def list(
        self, app: str, options: Optional[TimelineListOptions] = None
    ) -> AsyncPaginatedList[Timeline, TimelineListOptions]:
        """List timelines for a specific app."""
        return await self._client.get_paginated(
            f"/api/v2/apps/{app}/timelines", cursor=None, params=options
        )


class Timelines:
    def __init__(self, client: AsyncConsoleClient, bridge: AsyncBridge):
        self._client = client
        self._bridge = bridge
        self._async = AsyncTimelines(client)

    def list(
        self, app: str, options: Optional[TimelineListOptions] = None
    ) -> PaginatedList[Timeline, TimelineListOptions]:
        """List timelines for a specific app."""

        paginated = self._bridge.run(self._async.list(app, options))
        return PaginatedList(self._bridge, paginated)
