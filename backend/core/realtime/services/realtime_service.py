from fastapi import WebSocket

from realtime.channels import project_channel
from realtime.infrastructure.manager import (
    ConnectionManager,
)


class RealtimeService:

    def __init__(
        self,
        manager: ConnectionManager,
    ):
        self.manager = manager

    async def subscribe_to_project(
        self,
        websocket: WebSocket,
        project_id: str,
    ):

        channel = project_channel(
            project_id
        )

        await self.manager.subscribe(
            websocket,
            channel,
        )