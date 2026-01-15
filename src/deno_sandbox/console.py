import json
from typing import Any, Literal, Optional, cast
import httpx
from pydantic import HttpUrl

from deno_sandbox.api_types_generated import (
    App,
    AppInit,
    AppListOptions,
    AppUpdate,
    PaginatedList,
    RevisionListOptions,
    RevisionWithoutTimelines,
    Timeline,
    TimelineListOptions,
    Volume,
    VolumeInit,
    VolumeListOptions,
)
from deno_sandbox.bridge import AsyncBridge
from deno_sandbox.options import InternalOptions


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
        self, method: Literal["POST", "GET"], url: httpx.URL, data: Optional[Any] = None
    ) -> httpx.Response:
        response = await self.client.request(
            method=method, url=url, json=data, timeout=10.0
        )

        response.raise_for_status()
        return response

    async def post(self, path: str, data: any) -> dict:
        req_url = self._options["console_url"].join(path)
        response = await self._request("POST", req_url, data)
        response.raise_for_status()
        return response.json()

    async def get(
        self, path: str, params: Optional[dict[str, str | int]] = None
    ) -> dict:
        req_url = self._options["console_url"].join(path)

        if params is not None:
            req_url = req_url.copy_add_params(params)

        response = await self._request("GET", req_url)
        response.raise_for_status()
        return response.json()

    async def delete(self, path: str) -> None:
        req_url = HttpUrl(self._options["console_url"], path=path)
        response = await self.client.delete(req_url)
        response.raise_for_status()

    async def close(self) -> None:
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    # Proxy methods
    async def _volumes_create(self, data: VolumeInit) -> Volume:
        result = await self.post("/api/v2/volumes", data)
        return cast(Volume, result)

    async def _volumes_get(self, id_or_slug: str) -> Volume:
        return await self.get(f"/api/v2/volumes/{id_or_slug}")

    async def _volumes_list(
        self, options: Optional[VolumeListOptions] = None
    ) -> PaginatedList[Volume]:
        volumes = await self.get("/api/v2/volumes", options)
        print(volumes)
        return volumes


class ConsoleClient:
    def __init__(self, options: InternalOptions, bridge: AsyncBridge):
        self._async = AsyncConsoleClient(options)
        self._bridge = bridge

    def close(self):
        self._bridge.run(self._async.close())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._bridge.run(self._async.__aexit__(exc_type, exc_val, exc_tb))

    # Proxy methods
    def _apps_get(self, id_or_slug: str) -> App:
        return self._bridge.run(self._async._apps_get(id_or_slug))

    def _apps_list(
        self, options: Optional[AppListOptions] = None
    ) -> PaginatedList[App]:
        return self._bridge.run(self._async._apps_list(options))

    def _apps_create(self, options: AppInit) -> App:
        return self._bridge.run(self._async._apps_create(options))

    def _apps_update(self, app: str, update: AppUpdate) -> App:
        return self._bridge.run(self._async._apps_update(app, update))

    def _apps_delete(self, app: str) -> None:
        return self._bridge.run(self._async._apps_delete(app))

    def _revisions_get(self, app: str, id: str) -> None:
        return self._bridge.run(self._async._revisions_get(app, id))

    def _revisions_list(
        self, app: str, options: Optional[RevisionListOptions] = None
    ) -> PaginatedList[RevisionWithoutTimelines]:
        return self._bridge.run(self._async._revisions_list(app, options))

    def _timelines_list(
        self, app: str, options: Optional[TimelineListOptions] = None
    ) -> PaginatedList[Timeline]:
        return self._bridge.run(self._async._timelines_list(app, options))

    def _volumes_create(self, data: VolumeInit) -> Volume:
        return self._bridge.run(self._async._volumes_create(data))

    def _volumes_get(self, id_or_slug: str) -> Volume:
        return self._bridge.run(self._async._volumes_get(id_or_slug))

    def _volumes_list(
        self, options: Optional[VolumeListOptions] = None
    ) -> PaginatedList[Volume]:
        return self._bridge.run(self._async._volumes_list(options))


__all__ = ["AsyncConsoleClient", "ConsoleClient"]
