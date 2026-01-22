from __future__ import annotations

from typing import cast
from typing_extensions import Optional

from .api_types_generated import (
    App,
    AppListOptions,
    AppInit,
    AppUpdate,
)
from .utils import convert_to_snake_case
from .bridge import AsyncBridge
from .console import (
    PaginatedList,
    AsyncConsoleClient,
    AsyncPaginatedList,
)


class AsyncApps:
    def __init__(self, client: AsyncConsoleClient):
        self._client = client

    async def get(self, id_or_slug: str) -> App | None:
        """Get an app by its ID or slug."""
        result = await self._client.get_or_none(f"/api/v2/apps/{id_or_slug}")
        if result is None:
            return None
        raw_result = convert_to_snake_case(result)
        return cast(App, raw_result)

    async def list(
        self, options: Optional[AppListOptions] = None
    ) -> AsyncPaginatedList[App, AppListOptions]:
        """List apps of an org."""
        return await self._client.get_paginated(
            "/api/v2/apps", cursor=None, params=options
        )

    async def create(self, options: Optional[AppInit] = None) -> App:
        """Create a new app."""
        result = await self._client.post("/api/v2/apps", options or {})
        raw_result = convert_to_snake_case(result)
        return cast(App, raw_result)

    async def update(self, app: str, update: AppUpdate) -> App:
        """Update an existing app."""
        result = await self._client.patch(f"/api/v2/apps/{app}", update)
        raw_result = convert_to_snake_case(result)
        return cast(App, raw_result)

    async def delete(self, app: str) -> None:
        """Delete an app by its ID or slug."""
        await self._client.delete(f"/api/v2/apps/{app}")


class Apps:
    def __init__(self, client: AsyncConsoleClient, bridge: AsyncBridge):
        self._client = client
        self._bridge = bridge
        self._async = AsyncApps(client)

    def get(self, id_or_slug: str) -> App | None:
        """Get an app by its ID or slug."""
        return self._bridge.run(self._async.get(id_or_slug))

    def list(
        self, options: Optional[AppListOptions] = None
    ) -> PaginatedList[App, AppListOptions]:
        """List apps of an org."""

        paginated = self._bridge.run(self._async.list(options))
        return PaginatedList(self._bridge, paginated)

    def create(self, options: Optional[AppInit] = None) -> App:
        """Create a new app."""
        return self._bridge.run(self._async.create(options))

    def update(self, app: str, update: AppUpdate) -> App:
        """Update an existing app."""
        return self._bridge.run(self._async.update(app, update))

    def delete(self, app: str) -> None:
        """Delete an app by its ID or slug."""
        self._bridge.run(self._async.delete(app))
