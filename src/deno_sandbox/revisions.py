from __future__ import annotations

from typing import Any, TypedDict, cast
from typing_extensions import Literal, Optional

from deno_sandbox.timelines import Timeline

from .bridge import AsyncBridge
from .console import (
    AsyncConsoleClient,
    AsyncPaginatedList,
    PaginatedList,
)
from .utils import convert_to_snake_case


class RevisionWithoutTimelines(TypedDict):
    id: str
    """The unique identifier for the revision."""

    status: Literal["building", "ready", "error"]
    """The status of the revision."""

    created_at: str
    """The ISO 8601 timestamp when the revision was created."""

    updated_at: str
    """The ISO 8601 timestamp when the revision was last updated."""


class Revision(RevisionWithoutTimelines):
    timelines: list[Timeline]
    """The timelines associated with the revision."""


class AsyncRevisions:
    def __init__(self, client: AsyncConsoleClient):
        self._client = client

    async def get(self, app: str, id: str) -> Revision | None:
        """Get a revision by its ID for a specific app."""
        result = await self._client.get_or_none(f"/api/v2/apps/{app}/revisions/{id}")
        if result is None:
            return None
        raw_result = convert_to_snake_case(result)
        return cast(Revision, raw_result)

    async def list(
        self,
        app: str,
        *,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> AsyncPaginatedList[RevisionWithoutTimelines]:
        """List revisions for a specific app.

        Args:
            app: The app ID or slug.
            cursor: The cursor for pagination.
            limit: Limit the number of items to return.
        """
        options: dict[str, Any] = {}
        if cursor is not None:
            options["cursor"] = cursor
        if limit is not None:
            options["limit"] = limit
        return await self._client.get_paginated(
            f"/api/v2/apps/{app}/revisions",
            cursor=None,
            params=options if options else None,
        )


class Revisions:
    def __init__(self, client: AsyncConsoleClient, bridge: AsyncBridge):
        self._client = client
        self._bridge = bridge
        self._async = AsyncRevisions(client)

    def get(self, app: str, id: str) -> Revision | None:
        """Get a revision by its ID for a specific app."""
        return self._bridge.run(self._async.get(app, id))

    def list(
        self,
        app: str,
        *,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> PaginatedList[RevisionWithoutTimelines]:
        """List revisions for a specific app.

        Args:
            app: The app ID or slug.
            cursor: The cursor for pagination.
            limit: Limit the number of items to return.
        """
        paginated = self._bridge.run(self._async.list(app, cursor=cursor, limit=limit))
        return PaginatedList(self._bridge, paginated)
