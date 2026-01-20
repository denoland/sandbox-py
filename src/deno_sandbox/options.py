import os

from typing import NotRequired, Optional, TypedDict

from httpx import URL

from deno_sandbox.errors import MissingApiToken


class Options(TypedDict):
    token: NotRequired[str | None]
    regions: NotRequired[list[str] | None]


class InternalOptions(TypedDict):
    sandbox_ws_url: URL
    sandbox_url: URL
    console_url: URL
    token: str
    regions: list[str]


def get_internal_options(options: Optional[Options] = None) -> InternalOptions:
    sandbox_url = URL(
        os.environ.get("DENO_SANDBOX_ENDPOINT", "https://ams.sandbox-api.deno.net")
    )

    token = (
        options is not None
        and options.get("token")
        or os.environ.get("DENO_DEPLOY_TOKEN", None)
    )

    if token is None:
        raise MissingApiToken({"message": "DENO_DEPLOY_TOKEN is not set"})

    scheme = sandbox_url.scheme.replace("http", "ws")
    sandbox_ws_url = URL(f"{scheme}://{sandbox_url.netloc.decode()}")

    console_url = URL(
        os.environ.get("DENO_DEPLOY_ENDPOINT", "https://console.deno.com")
    )

    regions = (
        options is not None
        and options.get("regions")
        or os.environ.get("DENO_AVAILABLE_REGIONS", "ams1,ord").split(",")
    )

    return InternalOptions(
        console_url=console_url,
        sandbox_ws_url=sandbox_ws_url,
        sandbox_url=sandbox_url,
        token=token,
        regions=regions,
    )
