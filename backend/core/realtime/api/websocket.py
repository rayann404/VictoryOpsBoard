from fastapi import APIRouter, Depends
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from core.realtime.dependencies import (
    get_realtime_service,
)
from core.realtime.services.realtime_service import RealtimeService

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    realtime_service: RealtimeService = Depends(get_realtime_service)
):
    await realtime_service.manager.connect(websocket)

    try:
        while True:
            message = await websocket.receive_json()
            print("LOG | WS MESSAGE RECEIVED RAW: ", message)
            action = message.get("action")

            if action == "subscribe_project":
                await realtime_service.subscribe_to_project(
                    websocket=websocket,
                    project_id=message["project_id"],
                )

    except WebSocketDisconnect:
        realtime_service.manager.disconnect(websocket)