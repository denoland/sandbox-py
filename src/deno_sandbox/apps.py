from __future__ import annotations

from typing import Any, cast
from typing_extensions import Optional

from .api_types_generated import (
    App,
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
        self,
        *,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> AsyncPaginatedList[App]:
        """List apps of an org.

        Args:
            cursor: The cursor for pagination.
            limit: Limit the number of items to return.
        """
        options: dict[str, Any] = {}
        if cursor is not None:
            options["cursor"] = cursor
        if limit is not None:
            options["limit"] = limit
        return await self._client.get_paginated(
            "/api/v2/apps", cursor=None, params=options if options else None
        )

    async def create(
        self,
        *,
        slug: Optional[str] = None,
    ) -> App:
        """Create a new app.

        Args:
            slug: Human readable identifier for the app.
        """
        options: dict[str, Any] = {}
        if slug is not None:
            options["slug"] = slug
        result = await self._client.post("/api/v2/apps", options)
        raw_result = convert_to_snake_case(result)
        return cast(App, raw_result)

    async def update(
        self,
        app: str,
        *,
        slug: Optional[str] = None,
    ) -> App:
        """Update an existing app.

        Args:
            app: The app ID or slug to update.
            slug: Human readable identifier for the app.
        """
        update: dict[str, Any] = {}
        if slug is not None:
            update["slug"] = slug
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
        self,
        *,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> PaginatedList[App]:
        """List apps of an org.

        Args:
            cursor: The cursor for pagination.
            limit: Limit the number of items to return.
        """
        paginated = self._bridge.run(self._async.list(cursor=cursor, limit=limit))
        return PaginatedList(self._bridge, paginated)

    def create(
        self,
        *,
        slug: Optional[str] = None,
    ) -> App:
        """Create a new app.

        Args:
            slug: Human readable identifier for the app.
        """
        return self._bridge.run(self._async.create(slug=slug))

    def update(
        self,
        app: str,
        *,
        slug: Optional[str] = None,
    ) -> App:
        """Update an existing app.

        Args:
            app: The app ID or slug to update.
            slug: Human readable identifier for the app.
        """
        return self._bridge.run(self._async.update(app, slug=slug))

    def delete(self, app: str) -> None:
        """Delete an app by its ID or slug."""
        self._bridge.run(self._async.delete(app))
