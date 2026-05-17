from collections import defaultdict
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.channels: dict[str, set[WebSocket]] = defaultdict(set)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()

    def disconnect(self, websocket: WebSocket):
        for connections in self.channels.values():
            connections.discard(websocket)

    async def subscribe(self, websocket: WebSocket, channel: str):
        self.channels[channel].add(websocket)

    async def unsubscribe(self, websocket: WebSocket, channel: str):
        self.channels[channel].discard(websocket)

    async def broadcast(
            self,
            websocket: WebSocket,
            channel: str,
            message: dict
    ):
        dead_connections = []

        for websocket in self.channels[channel]:
            try:
                await websocket.send_json(message)

            except Exception:
                dead_connections.append(websocket)

        for ws in dead_connections:
            self.disconnect(ws)