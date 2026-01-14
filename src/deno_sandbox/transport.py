from pydantic_core import Url
from websockets import ConnectionClosed, connect


class WebSocketTransport:
    async def connect(self, url: Url, headers: dict[str, str]) -> None:
        self._ws = await connect(str(url), additional_headers=headers)

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
