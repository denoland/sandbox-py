from __future__ import annotations

from typing import Any, TypedDict
from urllib.parse import quote

from typing_extensions import Optional


from .bridge import AsyncBridge
from .console import (
    AsyncConsoleClient,
    AsyncPaginatedList,
    PaginatedList,
)


class TimelineApp(TypedDict):
    id: str
    """The unique identifier for the app."""

    slug: str
    """The human readable identifier for the app."""


class TimelineContext(TypedDict):
    slug: str


class Domain(TypedDict):
    domain: str
    """The domain name."""


class Timeline(TypedDict):
    id: str
    """The identifier that addresses this timeline, e.g. in `pin`.

    For a timeline that exists only once per app this is just its slug
    ("production"). Timelines that are parameterized by their partition — one
    per git branch, say — append those values: "git-branch:main".
    """

    slug: str
    """The slug of the timeline.

    Shared by every timeline built from the same partition config, so it
    identifies a timeline only when that timeline is unparameterized — see
    `Timeline.id`.
    """

    partition: dict[str, str]
    """The partition of the timeline."""

    pinned_revision: Optional[str]
    """The revision this timeline is pinned to.

    None when the timeline serves whichever of its member revisions was created
    most recently.
    """

    app: TimelineApp
    context: TimelineContext
    """The context of the timeline."""

    domains: list[Domain]
    """The domains associated with the timeline."""


class AsyncTimelines:
    def __init__(self, client: AsyncConsoleClient):
        self._client = client

    async def list(
        self,
        app: str,
        *,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> AsyncPaginatedList[Timeline]:
        """List timelines for a specific app.

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
            f"/api/v2/apps/{app}/timelines",
            cursor=None,
            params=options if options else None,
        )

    async def pin(self, app: str, timeline: str, revision: str) -> None:
        """Pin a timeline to one of its revisions.

        An unpinned timeline serves whichever of its member revisions was
        created most recently, so deploying to it makes the new revision live.
        A pinned timeline serves the pinned revision and nothing else: later
        deploys still join the timeline, but they only go live once the pin is
        moved or removed.

        The revision must already be a member of the timeline — pinning never
        changes membership. To make a revision that only exists on its preview
        timeline serve production, use `revisions.promote` instead, which joins
        the default production timeline and then pins it.

        Args:
            app: The app ID or slug.
            timeline: The timeline ID, as returned by `list`.
            revision: The revision ID to pin the timeline to.
        """
        await self._client.put(
            f"/api/v2/apps/{app}/timelines/{quote(timeline, safe='')}/pin",
            {"revision": revision},
        )

    async def unpin(self, app: str, timeline: str) -> None:
        """Remove a timeline's pin.

        The timeline goes back to serving whichever of its member revisions was
        created most recently; the revision that was pinned stays a member. This
        also releases a pin left behind by `revisions.promote`. Unpinning a
        timeline that is not pinned does nothing.

        Args:
            app: The app ID or slug.
            timeline: The timeline ID, as returned by `list`.
        """
        await self._client.delete(
            f"/api/v2/apps/{app}/timelines/{quote(timeline, safe='')}/pin"
        )


class Timelines:
    def __init__(self, client: AsyncConsoleClient, bridge: AsyncBridge):
        self._client = client
        self._bridge = bridge
        self._async = AsyncTimelines(client)

    def list(
        self,
        app: str,
        *,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> PaginatedList[Timeline]:
        """List timelines for a specific app.

        Args:
            app: The app ID or slug.
            cursor: The cursor for pagination.
            limit: Limit the number of items to return.
        """
        paginated = self._bridge.run(self._async.list(app, cursor=cursor, limit=limit))
        return PaginatedList(self._bridge, paginated)

    def pin(self, app: str, timeline: str, revision: str) -> None:
        """Pin a timeline to one of its revisions.

        An unpinned timeline serves whichever of its member revisions was
        created most recently, so deploying to it makes the new revision live.
        A pinned timeline serves the pinned revision and nothing else: later
        deploys still join the timeline, but they only go live once the pin is
        moved or removed.

        The revision must already be a member of the timeline — pinning never
        changes membership. To make a revision that only exists on its preview
        timeline serve production, use `revisions.promote` instead, which joins
        the default production timeline and then pins it.

        Args:
            app: The app ID or slug.
            timeline: The timeline ID, as returned by `list`.
            revision: The revision ID to pin the timeline to.
        """
        self._bridge.run(self._async.pin(app, timeline, revision))

    def unpin(self, app: str, timeline: str) -> None:
        """Remove a timeline's pin.

        The timeline goes back to serving whichever of its member revisions was
        created most recently; the revision that was pinned stays a member. This
        also releases a pin left behind by `revisions.promote`. Unpinning a
        timeline that is not pinned does nothing.

        Args:
            app: The app ID or slug.
            timeline: The timeline ID, as returned by `list`.
        """
        self._bridge.run(self._async.unpin(app, timeline))
