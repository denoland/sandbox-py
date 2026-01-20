from typing import Optional
from .api_generated import (
    Apps,
    AsyncApps,
    AsyncRevisions,
    AsyncSnapshots,
    AsyncTimelines,
    AsyncVolumes,
    Revisions,
    Snapshots,
    Timelines,
    Volumes,
)
from .bridge import AsyncBridge
from .sandbox import (
    AsyncSandboxApi,
    SandboxApi,
)
from .console import AsyncConsoleClient, ConsoleClient
from .options import Options, get_internal_options

__all__ = ["DenoDeploy", "AsyncDenoDeploy", "Options"]


class DenoDeploy:
    def __init__(self, options: Optional[Options] = None):
        internal_options = get_internal_options(options)
        bridge = AsyncBridge()

        client = ConsoleClient(internal_options, bridge)
        self.apps = Apps(client)
        self.revisions = Revisions(client)
        self.timelines = Timelines(client)
        self.sandbox = SandboxApi(client, bridge)
        self.snapshots = Snapshots(client)
        self.volumes = Volumes(client)


class AsyncDenoDeploy:
    def __init__(self, options: Optional[Options] = None):
        internal_options = get_internal_options(options)
        client = AsyncConsoleClient(internal_options)

        self.apps = AsyncApps(client)
        self.revisions = AsyncRevisions(client)
        self.timelines = AsyncTimelines(client)
        self.sandbox = AsyncSandboxApi(client)
        self.snapshots = AsyncSnapshots(client)
        self.volumes = AsyncVolumes(client)
