import asyncio
import base64
import json
from typing import Any, Dict, TypedDict, cast
from websockets import ConnectionClosed

from deno_sandbox.bridge import AsyncBridge
from deno_sandbox.errors import (
    ProcessAlreadyExited,
    RpcValidationError,
    UnknownRpcMethod,
    ZodErrorRaw,
)
from deno_sandbox.transport import WebSocketTransport
from deno_sandbox.utils import (
    convert_to_camel_case,
    convert_to_snake_case,
    to_snake_case,
)


class RpcRequest(TypedDict):
    id: int
    method: str
    params: dict[str, Any]
    jsonrpc: str = "2.0"


class RpcResult[T](TypedDict):
    ok: T | None = None
    error: Any | None = None


class RpcResponse[T](TypedDict):
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
        self._loop: asyncio.AbstractEventLoop | None = None
        self._signal_id = 0

    def get_next_signal_id(self) -> int:
        self._signal_id += 1
        return self._signal_id

    async def close(self):
        await self._transport.close()

    async def call(self, method: str, params: Dict[str, Any]) -> Any:
        if self._loop is None:
            self._loop = asyncio.get_running_loop()

        if self._listen_task is None or self._listen_task.done():
            self._listen_task = self._loop.create_task(self._listener())

        req_id = self._id + 1
        self._id = req_id

        camel_params = convert_to_camel_case(params)
        payload = RpcRequest(
            method=method, params=camel_params, id=req_id, jsonrpc="2.0"
        )

        future = self._loop.create_future()
        self._pending_requests[req_id] = future

        await self._transport.send(json.dumps(payload))

        raw_response = await future
        response = cast(RpcResponse[Any], raw_response)

        if response.get("error") is not None:
            if response["error"].get("message") == "Method not found":
                raise UnknownRpcMethod("RPC method not found")

            if response["error"].get("data") is not None:
                data = response["error"]["data"]
                if data.get("constructor_name") == "ZodError":
                    # For some reason ZodError data is serialized as
                    # json inside json ¯\_(ツ)_/¯
                    zod_errors: list[ZodErrorRaw] = []
                    for e in json.loads(data["message"]):
                        value = cast(ZodErrorRaw, e)

                        value["path"] = [to_snake_case(p) for p in value["path"]]
                        zod_errors.append(value)

                    raise RpcValidationError(zod_errors)

            raise Exception(response["error"])

        if response.get("result") and response["result"].get("error"):
            err = response["result"]["error"]
            if (
                "constructor_name" in err
                and err["constructor_name"] == "TypeError"
                and "code" in err
                and err["code"] == "ENOENT"
            ):
                raise ProcessAlreadyExited("Process has already exited")

            raise Exception(f"Application Error: {err}")
        return response["result"]["ok"] if response.get("result") else None

    async def _listener(self) -> None:
        try:
            async for raw in self._transport:
                data = json.loads(raw)
                req_id = data.get("id")

                if req_id is not None and req_id in self._pending_requests:
                    future = self._pending_requests.pop(req_id)
                    if not future.done():
                        converted_data = convert_to_snake_case(data)
                        future.set_result(converted_data)

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
            pass
        except Exception as e:
            for future in self._pending_requests.values():
                if not future.done():
                    future.set_exception(e)


class RpcClient:
    def __init__(self, async_client: AsyncRpcClient, bridge: AsyncBridge):
        self._async_client = async_client
        self._bridge = bridge

    def get_next_signal_id(self) -> int:
        return self._async_client.get_next_signal_id()

    def call(self, method: str, params: Dict[str, Any]) -> Any:
        return self._bridge.run(self._async_client.call(method, params))

    def close(self):
        self._bridge.run(self._async_client.close())
