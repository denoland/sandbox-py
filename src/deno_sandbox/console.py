import httpx
from pydantic import HttpUrl

from deno_sandbox.bridge import AsyncBridge
from deno_sandbox.options import InternalOptions


class AsyncConsoleClient:
    def __init__(self, options: InternalOptions):
        self._options = options

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

    async def post(self, path: str, data: any) -> dict:
        req_url = HttpUrl(self._options["console_url"], path=path)
        response = await self.client.post(req_url, json=data)
        response.raise_for_status()
        return response.json()

    async def get(self, path: str, search: dict | None = None) -> dict:
        req_url = HttpUrl(self._options["console_url"], path=path, search=search)
        response = await self.client.get(req_url)
        response.raise_for_status()
        return response.json()

    async def delete(self, path: str) -> None:
        req_url = HttpUrl(self._options["console_url"], path=path)
        response = await self.client.delete(req_url)
        response.raise_for_status()

    async def aclose(self) -> None:
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aclose()


class ConsoleClient:
    def __init__(self, options: InternalOptions, bridge: AsyncBridge):
        self._async = AsyncConsoleClient(options)
        self._bridge = bridge

    def post(self, path: str, data: any) -> dict:
        return self._bridge.run(self._async.post(path, data))

    def get(self, path: str, search: dict | None = None) -> dict:
        return self._bridge.run(self._async.get(path, search))

    def delete(self, path: str) -> None:
        return self._bridge.run(self._async.delete(path))

    def close(self):
        """Explicitly close the connection pool when the client is no longer needed."""
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._bridge.run(self._async.__aexit__(exc_type, exc_val, exc_tb))


__all__ = ["AsyncConsoleClient", "ConsoleClient"]
