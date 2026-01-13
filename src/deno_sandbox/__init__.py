from typing import Optional
from deno_sandbox.api_generated import (
    AppsApi,
    AsyncAppsApi,
    AsyncRevisionsApi,
    AsyncTimelinesApi,
    AsyncVolumesApi,
    RevisionsApi,
    TimelinesApi,
    VolumesApi,
)
from deno_sandbox.sandbox import (
    AsyncSandboxWrapper,
    SandboxWrapper,
)
from deno_sandbox.console import AsyncConsoleClient, ConsoleClient
from deno_sandbox.options import Options

__all__ = ["DenoDeploy", "AsyncDenoDeploy", "Options"]


class DenoDeploy:
    def __init__(self, options: Optional[Options] = None):
        client = ConsoleClient(options)
        self.apps = AppsApi(client)
        self.revisions = RevisionsApi(client)
        self.timelines = TimelinesApi(client)
        self.sandbox = SandboxWrapper(options)
        self.volumes = VolumesApi(client)


class AsyncDenoDeploy:
    def __init__(self, options: Optional[Options] = None):
        client = AsyncConsoleClient(options)
        self.apps = AsyncAppsApi(client)
        self.revisions = AsyncRevisionsApi(client)
        self.timelines = AsyncTimelinesApi(client)
        self.sandbox = AsyncSandboxWrapper(options)
        self.volumes = AsyncVolumesApi(client)
