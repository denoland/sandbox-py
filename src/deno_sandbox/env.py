from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .rpc import AsyncRpcClient, RpcClient


class AsyncSandboxEnv:
    def __init__(self, rpc: AsyncRpcClient):
        self._rpc = rpc

    async def get(self, key: str) -> str:
        """Get the value of an environment variable."""

        params = {"key": key}
        result = await self._rpc.call("envGet", params)

        return result

    async def set(self, key: str, value: str) -> None:
        """Set the value of an environment variable."""

        params = {"key": key, "value": value}
        await self._rpc.call("envSet", params)

    async def to_object(self) -> dict[str, str]:
        """Get all environment variables."""

        params = {}
        result = await self._rpc.call("envToObject", params)

        return result

    async def delete(self, key: str) -> None:
        """Delete an environment variable."""

        params = {"key": key}
        await self._rpc.call("envDelete", params)


class SandboxEnv:
    def __init__(self, rpc: RpcClient):
        self._rpc = rpc

    def get(self, key: str) -> str:
        """Get the value of an environment variable."""

        params = {"key": key}
        result = self._rpc.call("envGet", params)

        return result

    def set(self, key: str, value: str) -> None:
        """Set the value of an environment variable."""

        params = {"key": key, "value": value}
        self._rpc.call("envSet", params)

    def to_object(self) -> dict[str, str]:
        """Get all environment variables."""

        params = {}
        result = self._rpc.call("envToObject", params)

        return result

    def delete(self, key: str) -> None:
        """Delete an environment variable."""

        params = {"key": key}
        self._rpc.call("envDelete", params)
