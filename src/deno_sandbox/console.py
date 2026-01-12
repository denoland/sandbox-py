import httpx
from pydantic import HttpUrl

from deno_sandbox.options import Options, get_internal_options


class AsyncConsoleClient:
    def __init__(self, options: Options):
        self._options = get_internal_options(options or Options())

    @property
    def client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self._options.token}",
                }
            )
        return self._client

    async def post(self, path: str, data: any) -> dict:
        req_url = HttpUrl(self._options.console_url, path=path)
        response = await self.client.post(req_url, json=data)
        response.raise_for_status()
        return response.json()

    async def get(self, path: str, search: dict | None = None) -> dict:
        req_url = HttpUrl(self._options.console_url, path=path, search=search)
        response = await self.client.get(req_url)
        response.raise_for_status()
        return response.json()

    async def delete(self, path: str) -> None:
        req_url = HttpUrl(self._options.console_url, path=path)
        response = await self.client.delete(req_url)
        response.raise_for_status()

    async def aclose(self) -> None:
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aclose()


class ConsoleClient:
    def __init__(self, options: Options):
        self._options = get_internal_options(options or Options())

        self.client = httpx.Client(
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._options.token}",
            }
        )

    def post(self, path: str, data: any) -> dict:
        req_url = HttpUrl(self._options.console_url, path=path)
        response = self.client.post(req_url, json=data)
        response.raise_for_status()
        return response.json()

    def get(self, path: str, search: dict | None = None) -> dict:
        req_url = HttpUrl(self._options.console_url, path=path, search=search)
        response = self.client.get(req_url)
        response.raise_for_status()
        return response.json()

    def delete(self, path: str) -> None:
        req_url = HttpUrl(self._options.console_url, path=path)
        response = self.client.delete(req_url)
        response.raise_for_status()

    def close(self):
        """Explicitly close the connection pool when the client is no longer needed."""
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


__all__ = ["AsyncConsoleClient", "ConsoleClient"]
