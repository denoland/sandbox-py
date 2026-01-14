from pydantic_core import Url
from websockets import ConnectionClosed, connect

from deno_sandbox.errors import AuthenticationError


class WebSocketTransport:
    async def connect(self, url: Url, headers: dict[str, str]) -> None:
        try:
            self._ws = await connect(str(url), additional_headers=headers)
        except Exception as e:
            if "HTTP 401" in str(e):
                raise AuthenticationError(
                    "Authentication failed, invalid API token"
                ) from e

            raise e

    async def send(self, data: str) -> None:
        await self._ws.send(data)

    async def receive(self) -> dict[str, any]:
        return await self._ws.recv()

    async def close(self) -> None:
        await self._ws.close()

    async def __aexit__(self):
        await self.close()

    async def __aiter__(self):
        try:
            async for message in self._ws:
                yield message
        except ConnectionClosed:
            return
