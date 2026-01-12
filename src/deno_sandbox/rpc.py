import asyncio
import base64
from dataclasses import dataclass
import json
from typing import Any, Dict
from dataclasses_json import dataclass_json
from websockets import ConnectionClosed

from deno_sandbox.bridge import AsyncBridge
from deno_sandbox.transport import WebSocketTransport


@dataclass_json
@dataclass
class RpcRequest:
    id: int
    method: str
    params: dict[str, Any]
    jsonrpc: str = "2.0"


@dataclass_json
@dataclass
class RpcResult[T]:
    ok: T | None = None
    error: Any | None = None


@dataclass_json
@dataclass
class RpcResponse[T]:
    id: int
    jsonrpc: str = "2.0"
    result: RpcResult[T] | None = None
    error: dict[str, Any] | None = None


class AsyncRpcClient:
    def __init__(self, transport: WebSocketTransport):
        self._transport = transport
        self._id = 0
        self._pending_requests: Dict[int, asyncio.Future[Any]] = {}
        self._listen_task: asyncio.Task[Any] | None = None
        self._pending_processes: Dict[int, asyncio.StreamReader] = {}
        self._loop = None

    async def close(self):
        await self._transport.close()

    async def call(self, method: str, params: Dict[str, Any]) -> Any:
        if self._listen_task is None or self._listen_task.done():
            self._loop = asyncio.get_running_loop()
            self._listen_task = self._loop.create_task(self._listener())

        req_id = self._id + 1
        self._id = req_id

        payload = RpcRequest(method=method, params=params, id=req_id)

        future = self._loop.create_future()
        self._pending_requests[req_id] = future

        await self._transport.send(payload.to_json())

        raw_response = await future
        response = RpcResponse[Any].from_json(json.dumps(raw_response))

        if response.error:
            raise Exception(response.error)

        if response.result and response.result.error:
            raise Exception(f"Application Error: {response.result.error}")

        return response.result.ok if response.result else None

    async def _listener(self) -> None:
        try:
            async for raw in self._transport:
                data = json.loads(raw)
                req_id = data.get("id")

                if req_id is not None and req_id in self._pending_requests:
                    future = self._pending_requests.pop(req_id)
                    if not future.done():
                        future.set_result(data)

                elif "method" in data:
                    method = data["method"]
                    params = data.get("params", {})

                    if method == "$sandbox.stream.enqueue":
                        stream_id = params.get("streamId")
                        chunk = base64.b64decode(params.get("data", ""))
                        stream = self._pending_processes.get(stream_id)
                        if stream:
                            stream.feed_data(chunk)
                    elif method == "$sandbox.stream.end":
                        stream_id = params.get("streamId")
                        stream = self._pending_processes.get(stream_id)
                        if stream:
                            stream.feed_eof()
                            del self._pending_processes[stream_id]

        except ConnectionClosed:
            print("Transport connection closed.")  # --- IGNORE ---
            pass
        except Exception as e:
            for future in self._pending_requests.values():
                if not future.done():
                    future.set_exception(e)


class RpcClient:
    def __init__(self, async_client: AsyncRpcClient, bridge: AsyncBridge):
        self._async_client = async_client
        self._bridge = bridge

    def call(self, method: str, params: Dict[str, Any]) -> Any:
        return self._bridge.run(self._async_client.call(method, params))

    def close(self):
        self._bridge.run(self._async_client.close())
