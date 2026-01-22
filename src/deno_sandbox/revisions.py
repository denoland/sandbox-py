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

    def get(self, app: str, id: str) -> Revision:
        """Get a revision by its ID for a specific app."""

        result = self._client._revisions_get(app, id)

        raw_result = convert_to_snake_case(result)
        return cast(Revision, raw_result)

    def list(
        self, app: str, options: Optional[RevisionListOptions] = None
    ) -> PaginatedList[RevisionWithoutTimelines, RevisionListOptions]:
        """List revisions for a specific app."""

        result = self._client._revisions_list(app, options)

        return result


class AsyncRevisions:
    def __init__(self, client: AsyncConsoleClient):
        self._client = client

    async def get(self, app: str, id: str) -> Revision:
        """Get a revision by its ID for a specific app."""

        result = await self._client._revisions_get(app, id)

        raw_result = convert_to_snake_case(result)
        return cast(Revision, raw_result)

    async def list(
        self, app: str, options: Optional[RevisionListOptions] = None
    ) -> AsyncPaginatedList[RevisionWithoutTimelines, RevisionListOptions]:
        """List revisions for a specific app."""

        result = await self._client._revisions_list(app, options)

        return result
