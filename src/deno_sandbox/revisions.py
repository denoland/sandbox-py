from __future__ import annotations

import warnings
from typing import Any, Dict, TypedDict, Union, cast, overload
from typing_extensions import Literal, NotRequired, Optional

from deno_sandbox.apps import Config, EnvVar, LayerRef


class FileAsset(TypedDict):
    kind: Literal["file"]
    encoding: Literal["utf-8", "base64"]
    content: str


class SymlinkAsset(TypedDict):
    kind: Literal["symlink"]
    target: str


Asset = Union[FileAsset, SymlinkAsset]


class EnvVarInputForDeploy(TypedDict):
    key: str
    value: str


from .bridge import AsyncBridge
from .console import (
    AsyncConsoleClient,
    AsyncPaginatedList,
    PaginatedList,
)
from .utils import convert_to_snake_case


class RevisionListItem(TypedDict):
    id: str
    """The unique identifier for the revision."""

    status: Literal["skipped", "queued", "building", "succeeded", "failed"]
    """The current revision lifecycle status."""

    failure_reason: str | None
    """Reason for failure, or null if not failed."""

    created_at: str
    """The ISO 8601 timestamp when the revision was created."""

    cancellation_requested_at: str | None
    """ISO 8601 timestamp when cancellation was requested, or null."""

    build_finished_at: str | None
    """ISO 8601 timestamp when the build completed, or null if still building."""

    deleted_at: str | None
    """ISO 8601 timestamp of deletion, or null if active."""


class Revision(TypedDict):
    id: str
    """The unique identifier for the revision."""

    status: Literal["skipped", "queued", "building", "succeeded", "failed"]
    """The current revision lifecycle status."""

    failure_reason: str | None
    """Reason for failure, or null if not failed."""

    layers: NotRequired[list[LayerRef]]
    """Layers referenced by this revision, in priority order."""

    env_vars: NotRequired[list[EnvVar]]
    """Revision-specific environment variables (immutable once created)."""

    config: NotRequired[Config]
    """Build and runtime configuration used for this revision."""

    created_at: str
    """The ISO 8601 timestamp when the revision was created."""

    cancellation_requested_at: str | None
    """ISO 8601 timestamp when cancellation was requested, or null."""

    build_finished_at: str | None
    """ISO 8601 timestamp when the build completed, or null if still building."""

    deleted_at: str | None
    """ISO 8601 timestamp of deletion, or null if active."""


# Keep old name as alias for backward compatibility
RevisionWithoutTimelines = RevisionListItem


class AsyncRevisions:
    def __init__(self, client: AsyncConsoleClient):
        self._client = client

    @overload
    async def get(self, id: str) -> Revision | None: ...

    @overload
    async def get(self, app: str, id: str) -> Revision | None: ...

    async def get(self, *args: str) -> Revision | None:
        """Get a revision by its ID.

        Args:
            id: The revision ID (globally unique).

        .. deprecated::
            The two-argument form ``get(app, id)`` is deprecated.
            Use ``get(id)`` instead — revision IDs are globally unique.
        """
        if len(args) == 2:
            warnings.warn(
                "revisions.get(app, id) is deprecated. "
                "Use revisions.get(id) instead — revision IDs are globally unique.",
                DeprecationWarning,
                stacklevel=2,
            )
            revision_id = args[1]
        elif len(args) == 1:
            revision_id = args[0]
        else:
            raise TypeError(
                f"get() takes 1 or 2 positional arguments but {len(args)} were given"
            )

        result = await self._client.get_or_none(f"/api/v2/revisions/{revision_id}")
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
    ) -> AsyncPaginatedList[RevisionListItem]:
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

    async def cancel(self, revision: str) -> Revision:
        """Cancel a revision build.

        Cancellation is asynchronous — this returns immediately with the current
        revision state. The ``cancellation_requested_at`` field will be set, but
        the revision may still be in ``building`` status. Poll the revision or use
        the progress endpoint to wait for the ``failed`` state.

        Args:
            revision: The revision ID.
        """
        result = await self._client.post(f"/api/v2/revisions/{revision}/cancel", {})
        return cast(Revision, convert_to_snake_case(result))

    async def deploy(
        self,
        app: str,
        assets: Dict[str, Asset],
        *,
        config: Optional[Config] = None,
        env_vars: Optional[list[EnvVarInputForDeploy]] = None,
        labels: Optional[Dict[str, str]] = None,
    ) -> Revision:
        """Deploy a revision by uploading source files as assets.

        Args:
            app: The app ID or slug.
            assets: Dict mapping file paths to Asset objects.
            config: Optional build/runtime configuration.
            env_vars: Optional environment variables for this revision.
            labels: Optional labels (e.g., git metadata).

        Returns:
            The created Revision (build is async; poll for status).
        """
        body: Dict[str, Any] = {"assets": assets}
        if config is not None:
            body["config"] = config
        if env_vars is not None:
            body["env_vars"] = env_vars
        if labels is not None:
            body["labels"] = labels
        result = await self._client.post(f"/api/v2/apps/{app}/deploy", body)
        return cast(Revision, convert_to_snake_case(result))


class Revisions:
    def __init__(self, client: AsyncConsoleClient, bridge: AsyncBridge):
        self._client = client
        self._bridge = bridge
        self._async = AsyncRevisions(client)

    @overload
    def get(self, id: str) -> Revision | None: ...

    @overload
    def get(self, app: str, id: str) -> Revision | None: ...

    def get(self, *args: str) -> Revision | None:
        """Get a revision by its ID.

        Args:
            id: The revision ID (globally unique).

        .. deprecated::
            The two-argument form ``get(app, id)`` is deprecated.
            Use ``get(id)`` instead — revision IDs are globally unique.
        """
        return self._bridge.run(self._async.get(*args))

    def list(
        self,
        app: str,
        *,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> PaginatedList[RevisionListItem]:
        """List revisions for a specific app.

        Args:
            app: The app ID or slug.
            cursor: The cursor for pagination.
            limit: Limit the number of items to return.
        """
        paginated = self._bridge.run(self._async.list(app, cursor=cursor, limit=limit))
        return PaginatedList(self._bridge, paginated)

    def cancel(self, revision: str) -> Revision:
        """Cancel a revision build.

        Args:
            revision: The revision ID.
        """
        return self._bridge.run(self._async.cancel(revision))

    def deploy(
        self,
        app: str,
        assets: Dict[str, Asset],
        *,
        config: Optional[Config] = None,
        env_vars: Optional[list[EnvVarInputForDeploy]] = None,
        labels: Optional[Dict[str, str]] = None,
    ) -> Revision:
        """Deploy a revision by uploading source files as assets.

        Args:
            app: The app ID or slug.
            assets: Dict mapping file paths to Asset objects.
            config: Optional build/runtime configuration.
            env_vars: Optional environment variables for this revision.
            labels: Optional labels (e.g., git metadata).

        Returns:
            The created Revision (build is async; poll for status).
        """
        return self._bridge.run(
            self._async.deploy(
                app, assets, config=config, env_vars=env_vars, labels=labels
            )
        )
