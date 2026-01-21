from __future__ import annotations

import base64
from typing import TYPE_CHECKING, AsyncIterable, BinaryIO, Iterable, Union

if TYPE_CHECKING:
    from .rpc import AsyncRpcClient

Streamable = Union[AsyncIterable[bytes], Iterable[bytes], BinaryIO]


class AsyncStreamWriter:
    """Manages writing a stream to the server."""

    def __init__(self, rpc: AsyncRpcClient, stream_id: int):
        self._rpc = rpc
        self._stream_id = stream_id

    async def start(self) -> None:
        """Send $sandbox.stream.start message."""
        await self._rpc.send_notification(
            "$sandbox.stream.start", {"streamId": self._stream_id}
        )

    async def enqueue(self, data: bytes) -> None:
        """Send $sandbox.stream.enqueue message with base64-encoded data."""
        await self._rpc.send_notification(
            "$sandbox.stream.enqueue",
            {
                "streamId": self._stream_id,
                "data": base64.b64encode(data).decode("ascii"),
            },
        )

    async def end(self) -> None:
        """Send $sandbox.stream.end message."""
        await self._rpc.send_notification(
            "$sandbox.stream.end", {"streamId": self._stream_id}
        )

    async def error(self, message: str) -> None:
        """Send $sandbox.stream.error message."""
        await self._rpc.send_notification(
            "$sandbox.stream.error", {"streamId": self._stream_id, "error": message}
        )


async def stream_data(
    rpc: AsyncRpcClient, data: Streamable, chunk_size: int = 64 * 1024
) -> int:
    """
    Stream data to server. Returns stream_id.

    Sends: start → enqueue(s) → end
    On error: sends error message then re-raises
    """
    stream_id = rpc.next_stream_id()
    writer = AsyncStreamWriter(rpc, stream_id)

    try:
        await writer.start()

        if hasattr(data, "read"):
            # File-like object
            while True:
                chunk = data.read(chunk_size)  # type: ignore[union-attr]
                if not chunk:
                    break
                await writer.enqueue(chunk)
        elif hasattr(data, "__aiter__"):
            # Async iterable
            async for chunk in data:  # type: ignore[union-attr]
                await writer.enqueue(chunk)
        else:
            # Sync iterable
            for chunk in data:  # type: ignore[union-attr]
                await writer.enqueue(chunk)

        await writer.end()
        return stream_id

    except Exception as e:
        await writer.error(str(e))
        raise


def is_streamable(obj: object) -> bool:
    """Check if object is streamable (not bytes)."""
    return (
        hasattr(obj, "read")
        or hasattr(obj, "__aiter__")
        or (hasattr(obj, "__iter__") and not isinstance(obj, (bytes, str, dict, list)))
    )
