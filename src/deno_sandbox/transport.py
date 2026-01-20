from typing import Any
from websockets import ClientConnection, ConnectionClosed, connect
from httpx import URL

from deno_sandbox.errors import AuthenticationError


class WebSocketTransport:
    def __init__(self) -> None:
        self._ws: ClientConnection | None = None
        self._closed = False

    @property
    def closed(self) -> bool:
        return self._closed

    async def connect(self, url: URL, headers: dict[str, str]) -> ClientConnection:
        try:
            ws = await connect(str(url), additional_headers=headers)
            self._ws = ws
            return ws
        except Exception as e:
            if "HTTP 401" in str(e):
                raise AuthenticationError(
                    "Authentication failed, invalid API token"
                ) from e

            raise e

    async def send(self, data: str) -> None:
        if self._ws is None:
            raise RuntimeError("WebSocket is not connected")
        await self._ws.send(data)

    async def close(self) -> None:
        self._closed = True

        if self._ws is not None:
            await self._ws.close()

    async def __aexit__(self):
        await self.close()

    async def __aiter__(self):
        if self._ws is None:
            raise RuntimeError("WebSocket is not connected")

        try:
            async for message in self._ws:
                yield message
        except ConnectionClosed:
            return
