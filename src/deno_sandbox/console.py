from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Generic, Literal, Optional, TypedDict, TypeVar, cast
import httpx

from .api_types_generated import (
    App,
    AppInit,
    AppListOptions,
    AppUpdate,
    RevisionListOptions,
    RevisionWithoutTimelines,
    SandboxListOptions,
    SandboxMeta,
    Snapshot,
    SnapshotInit,
    SnapshotListOptions,
    Timeline,
    TimelineListOptions,
    Volume,
    VolumeInit,
    VolumeListOptions,
)
from .bridge import AsyncBridge
from .options import InternalOptions
from .utils import convert_to_snake_case, parse_link_header

T = TypeVar("T")
O = TypeVar("O")


class Revision(RevisionWithoutTimelines):
    timelines: list[Timeline]
    """The timelines associated with the revision."""


class ExposeSSHResult(TypedDict):
    hostname: str
    username: str
    port: int


class ExposeHTTPResult(TypedDict):
    domain: str


class AsyncPaginatedList(Generic[T, O]):
    def __init__(
        self,
        client: AsyncConsoleClient,
        items: list[T],
        path: str,
        next_cursor: str | None,
        options: Optional[O] = None,
    ):
        self._client = client
        self._options = options
        self._path = path

        self.items = items
        """The items in the current page of the paginated list."""

        self.next_cursor = next_cursor
        """The cursor for pagination."""

    async def get_next_page(self) -> AsyncPaginatedList[T, O] | None:
        if not self.has_more:
            return None

        return await self._client.get_paginated(
            self._path,
            self.next_cursor,
            self._options,
        )

    @property
    def has_more(self) -> bool:
        """Whether there are more items to fetch."""
        return self.next_cursor is not None

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self.has_more:
            raise StopAsyncIteration

        next_page = await self.get_next_page()
        if next_page is None:
            raise StopAsyncIteration

        return next_page


class PaginatedList(Generic[T, O]):
    def __init__(
        self,
        bridge: AsyncBridge,
        async_paginated: AsyncPaginatedList[T, O],
    ):
        self._bridge = bridge
        self._async_paginated = async_paginated

    def get_next_page(self) -> PaginatedList[T, O] | None:
        next_page: AsyncPaginatedList[T, O] | None = self._bridge.run(
            self._async_paginated.get_next_page()
        )
        if next_page is None:
            return None

        return PaginatedList(self._bridge, next_page)

    @property
    def items(self) -> list[T]:
        """The items in the current page of the paginated list."""
        return self._async_paginated.items

    @property
    def next_cursor(self) -> str | None:
        """The cursor for pagination."""
        return self._async_paginated.next_cursor

    @property
    def has_more(self) -> bool:
        """Whether there are more items to fetch."""
        return self._async_paginated.has_more


class AsyncConsoleClient:
    def __init__(self, options: InternalOptions):
        self._options = options
        self._client: httpx.AsyncClient | None = None

    @property
    def client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self._options['token']}",
                }
            )
        return self._client

    async def _request(
        self,
        method: Literal["POST", "GET", "PATCH", "PUT", "DELETE"],
        url: httpx.URL,
        data: Optional[Any] = None,
    ) -> httpx.Response:
        response = await self.client.request(
            method=method, url=url, json=data, timeout=10.0
        )

        response.raise_for_status()
        return response

    async def post(self, path: str, data: Any) -> dict:
        req_url = self._options["console_url"].join(path)
        response = await self._request("POST", req_url, data)
        return response.json()

    async def patch(self, path: str, data: Any) -> dict:
        req_url = self._options["console_url"].join(path)
        response = await self._request("PATCH", req_url, data)
        return response.json()

    async def get(
        self, path: str, params: Optional[dict[str, str | int]] = None
    ) -> dict:
        req_url = self._options["console_url"].join(path)

        if params is not None:
            req_url = req_url.copy_merge_params(params)

        response = await self._request("GET", req_url)
        return response.json()

    async def get_or_none(
        self, path: str, params: Optional[dict[str, str | int]] = None
    ) -> dict | None:
        try:
            return await self.get(path, params)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

    async def delete(self, path: str) -> httpx.Response:
        req_url = self._options["console_url"].join(path)
        response = await self._request("DELETE", req_url)
        return response

    async def get_paginated(
        self,
        path: str,
        cursor: Optional[str],
        params: Optional[O] = None,
    ) -> AsyncPaginatedList[T, O]:
        req_url = self._options["console_url"].join(path)

        if params is not None:
            url_params = cast(dict, params)
            req_url = req_url.copy_merge_params(url_params)

        if cursor is not None:
            req_url = req_url.copy_add_param("cursor", cursor)

        response = await self._request("GET", req_url)
        response.raise_for_status()
        data = response.json()

        next_cursor: str | None = None
        link_header = response.headers.get("link")
        if link_header is not None:
            parsed = parse_link_header(link_header)
            next_cursor = parsed.get("next", None)

        items = [cast(T, convert_to_snake_case(item)) for item in data]

        return AsyncPaginatedList(self, items, path, next_cursor, params)

    async def close(self) -> None:
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    # Proxy methods
    async def _apps_create(self, data: Optional[AppInit] = None) -> App:
        result = await self.post("/api/v2/apps", data or {})
        return cast(App, result)

    async def _apps_get(self, id_or_slug: str) -> App | None:
        result = await self.get_or_none(f"/api/v2/apps/{id_or_slug}")
        if result is None:
            return None
        return cast(App, result)

    async def _apps_update(self, app: str, update: AppUpdate) -> App:
        result = await self.patch(f"/api/v2/apps/{app}", update)
        return cast(App, result)

    async def _apps_delete(self, app: str) -> None:
        await self.delete(f"/api/v2/apps/{app}")

    async def _apps_list(
        self, options: Optional[AppListOptions] = None
    ) -> AsyncPaginatedList[App, AppListOptions]:
        apps: AsyncPaginatedList[App, AppListOptions] = await self.get_paginated(
            path="/api/v2/apps", cursor=None, params=options
        )
        return apps

    async def _revisions_get(self, app: str, id_or_slug: str) -> Revision | None:
        result = await self.get_or_none(f"/api/v2/apps/{app}/revisions/{id_or_slug}")
        if result is None:
            return None
        return cast(Revision, result)

    async def _revisions_list(
        self, app: str, options: Optional[RevisionListOptions] = None
    ) -> AsyncPaginatedList[RevisionWithoutTimelines, RevisionListOptions]:
        revisions: AsyncPaginatedList[
            RevisionWithoutTimelines, RevisionListOptions
        ] = await self.get_paginated(
            path=f"/api/v2/apps/{app}/revisions", cursor=None, params=options
        )

        return revisions

    async def _snapshots_get(self, id_or_slug: str) -> Snapshot | None:
        result = await self.get_or_none(f"/api/v2/snapshots/{id_or_slug}")
        if result is None:
            return None
        return cast(Snapshot, result)

    async def _snapshots_list(
        self, options: Optional[SnapshotListOptions] = None
    ) -> AsyncPaginatedList[Snapshot, SnapshotListOptions]:
        snapshots: AsyncPaginatedList[
            Snapshot, SnapshotListOptions
        ] = await self.get_paginated("/api/v2/snapshots", cursor=None, params=options)

        return snapshots

    async def _snapshots_delete(self, id_or_slug: str) -> None:
        await self.delete(f"/api/v2/snapshots/{id_or_slug}")

    async def _timelines_list(
        self, app: str, options: Optional[TimelineListOptions] = None
    ) -> AsyncPaginatedList[Timeline, TimelineListOptions]:
        timelines: AsyncPaginatedList[
            Timeline, TimelineListOptions
        ] = await self.get_paginated(
            path=f"/api/v2/apps/{app}/timelines", cursor=None, params=options
        )

        return timelines

    async def _volumes_create(self, data: VolumeInit) -> Volume:
        params = {
            "slug": data["slug"],
            "capacity": data["capacity"],
            "region": data["region"],
        }
        if data.get("from_snapshot") is not None:
            params["from"] = data["from_snapshot"]

        result = await self.post("/api/v2/volumes", params)
        return cast(Volume, result)

    async def _volumes_get(self, id_or_slug: str) -> Volume | None:
        result = await self.get_or_none(f"/api/v2/volumes/{id_or_slug}")
        if result is None:
            return None
        return cast(Volume, result)

    async def _volumes_delete(self, id_or_slug: str) -> None:
        await self.delete(f"/api/v2/volumes/{id_or_slug}")

    async def _volumes_list(
        self, options: Optional[VolumeListOptions] = None
    ) -> AsyncPaginatedList[Volume, VolumeListOptions]:
        volumes: AsyncPaginatedList[
            Volume, VolumeListOptions
        ] = await self.get_paginated(
            path="/api/v2/volumes", cursor=None, params=options
        )
        return volumes

    async def _volumes_snapshot(self, id_or_slug: str, init: SnapshotInit) -> Snapshot:
        result = await self.post(f"/api/v2/volumes/{id_or_slug}/snapshot", init)
        return cast(Snapshot, result)

    # FIXME test
    async def _sandboxes_list(
        self, options: Optional[SandboxListOptions] = None
    ) -> AsyncPaginatedList[SandboxMeta, SandboxListOptions]:
        sandboxes: AsyncPaginatedList[
            SandboxMeta, SandboxListOptions
        ] = await self.get_paginated(
            path="/api/v3/sandboxes", cursor=None, params=options
        )
        return sandboxes

    async def _kill_sandbox(self, sandbox_id: str) -> None:
        await self.delete(f"/api/v3/sandboxes/{sandbox_id}")

    async def _extend_timeout(self, sandbox_id: str, stop_at_ms: int) -> datetime:
        url = self._options["sandbox_url"].join(f"/api/v3/sandbox/{sandbox_id}")

        result = await self._request("PATCH", url, {"stop_at_ms": stop_at_ms})

        data = result.json()

        return datetime.fromtimestamp(data["stop_at_ms"] / 1000, tz=timezone.utc)

    async def _expose_http(self, sandbox_id: str, params: dict[str, int]) -> str:
        url = self._options["sandbox_url"].join(
            f"/api/v3/sandbox/{sandbox_id}/expose/http"
        )

        result = await self._request("POST", url, params)

        data = cast(ExposeHTTPResult, result.json())
        return data["domain"]

    async def _expose_ssh(self, sandbox_id: str) -> ExposeSSHResult:
        url = self._options["sandbox_url"].join(
            f"/api/v3/sandbox/{sandbox_id}/expose/ssh"
        )
        response = await self._request("POST", url, {})

        return cast(ExposeSSHResult, response.json())


class ConsoleClient:
    def __init__(self, options: InternalOptions, bridge: AsyncBridge):
        self._async = AsyncConsoleClient(options)
        self._bridge = bridge

    def get_paginated(
        self, path: str, cursor: Optional[str], params: Optional[O] = None
    ) -> PaginatedList[T, O]:
        async_paginated = self._bridge.run(
            self._async.get_paginated(path, cursor, params)
        )

        return PaginatedList(self._bridge, async_paginated)

    def close(self):
        self._bridge.run(self._async.close())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._bridge.run(self._async.__aexit__(exc_type, exc_val, exc_tb))

    # Proxy methods
    def _apps_get(self, id_or_slug: str) -> App | None:
        return self._bridge.run(self._async._apps_get(id_or_slug))

    def _apps_list(
        self, options: Optional[AppListOptions] = None
    ) -> PaginatedList[App, AppListOptions]:
        paginated: AsyncPaginatedList[App, AppListOptions] = self._bridge.run(
            self._async._apps_list(options)
        )
        return PaginatedList(self._bridge, paginated)

    def _apps_create(self, options: Optional[AppInit] = None) -> App:
        return self._bridge.run(self._async._apps_create(options))

    def _apps_update(self, app: str, update: AppUpdate) -> App:
        return self._bridge.run(self._async._apps_update(app, update))

    def _apps_delete(self, app: str) -> None:
        self._bridge.run(self._async._apps_delete(app))

    def _revisions_get(self, app: str, id_or_slug: str) -> Revision | None:
        return self._bridge.run(self._async._revisions_get(app, id_or_slug))

    def _revisions_list(
        self, app: str, options: Optional[RevisionListOptions] = None
    ) -> PaginatedList[RevisionWithoutTimelines, RevisionListOptions]:
        paginated: AsyncPaginatedList[RevisionWithoutTimelines, RevisionListOptions] = (
            self._bridge.run(self._async._revisions_list(app, options))
        )
        return PaginatedList(self._bridge, paginated)

    def _snapshots_get(self, id_or_slug: str) -> Snapshot | None:
        return self._bridge.run(self._async._snapshots_get(id_or_slug))

    def _snapshots_list(
        self, options: Optional[SnapshotListOptions] = None
    ) -> PaginatedList[Snapshot, SnapshotListOptions]:
        result = self._bridge.run(self._async._snapshots_list(options))

        return PaginatedList(self._bridge, result)

    def _snapshots_delete(self, id_or_slug: str) -> None:
        self._bridge.run(self._async._snapshots_delete(id_or_slug))

    def _timelines_list(
        self, app: str, options: Optional[TimelineListOptions] = None
    ) -> PaginatedList[Timeline, TimelineListOptions]:
        paginated: AsyncPaginatedList[Timeline, TimelineListOptions] = self._bridge.run(
            self._async._timelines_list(app, options)
        )
        return PaginatedList(self._bridge, paginated)

    def _volumes_create(self, data: VolumeInit) -> Volume:
        return self._bridge.run(self._async._volumes_create(data))

    def _volumes_get(self, id_or_slug: str) -> Volume | None:
        return self._bridge.run(self._async._volumes_get(id_or_slug))

    def _volumes_delete(self, id_or_slug: str) -> None:
        self._bridge.run(self._async._volumes_delete(id_or_slug))

    def _volumes_list(
        self, options: Optional[VolumeListOptions] = None
    ) -> PaginatedList[Volume, VolumeListOptions]:
        paginated: AsyncPaginatedList[Volume, VolumeListOptions] = self._bridge.run(
            self._async._volumes_list(options)
        )
        return PaginatedList(self._bridge, paginated)

    def _volumes_snapshot(self, id_or_slug: str, init: SnapshotInit) -> Snapshot:
        return self._bridge.run(self._async._volumes_snapshot(id_or_slug, init))

    def _sandboxes_list(
        self, options: Optional[SandboxListOptions] = None
    ) -> PaginatedList[SandboxMeta, SandboxListOptions]:
        paginated: AsyncPaginatedList[SandboxMeta, SandboxListOptions] = (
            self._bridge.run(self._async._sandboxes_list(options))
        )
        return PaginatedList(self._bridge, paginated)

    def _kill_sandbox(self, sandbox_id: str) -> None:
        self._bridge.run(self._async._kill_sandbox(sandbox_id))

    def _extend_timeout(self, sandbox_id: str, stop_at_ms: int) -> None:
        self._bridge.run(self._async._extend_timeout(sandbox_id, stop_at_ms))

    def _expose_http(self, sandbox_id: str, params: dict[str, int]) -> str:
        return self._bridge.run(self._async._expose_http(sandbox_id, params))

    def _expose_ssh(self, sandbox_id: str) -> ExposeSSHResult:
        return self._bridge.run(self._async._expose_ssh(sandbox_id))


__all__ = ["AsyncConsoleClient", "ConsoleClient"]
