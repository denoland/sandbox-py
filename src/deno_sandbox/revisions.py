from __future__ import annotations

from typing import TYPE_CHECKING, cast
from typing_extensions import Optional

from .api_types_generated import (
    RevisionListOptions,
    RevisionWithoutTimelines,
)
from .console import Revision
from .utils import convert_to_snake_case

if TYPE_CHECKING:
    from .console import (
        AsyncConsoleClient,
        AsyncPaginatedList,
        ConsoleClient,
        PaginatedList,
    )


class Revisions:
    def __init__(self, client: ConsoleClient):
        self._client = client

    def get(self, app: str, id: str) -> Revision | None:
        """Get a revision by its ID for a specific app."""
        result = self._client._bridge.run(
            self._client._async.get_or_none(f"/api/v2/apps/{app}/revisions/{id}")
        )
        if result is None:
            return None
        raw_result = convert_to_snake_case(result)
        return cast(Revision, raw_result)

    def list(
        self, app: str, options: Optional[RevisionListOptions] = None
    ) -> PaginatedList[RevisionWithoutTimelines, RevisionListOptions]:
        """List revisions for a specific app."""
        from .console import PaginatedList

        paginated = self._client._bridge.run(
            self._client._async.get_paginated(
                f"/api/v2/apps/{app}/revisions", cursor=None, params=options
            )
        )
        return PaginatedList(self._client._bridge, paginated)


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
        self, app: str, options: Optional[RevisionListOptions] = None
    ) -> AsyncPaginatedList[RevisionWithoutTimelines, RevisionListOptions]:
        """List revisions for a specific app."""
        return await self._client.get_paginated(
            f"/api/v2/apps/{app}/revisions", cursor=None, params=options
        )
