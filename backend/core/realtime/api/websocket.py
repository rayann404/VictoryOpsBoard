from fastapi import APIRouter, Depends
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from realtime.dependencies import (
    get_realtime_service,
)
from realtime.services.realtime_service import RealtimeService

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    realtime_service: RealtimeService = Depends(get_realtime_service)
):
    await realtime_service.manager.connect(
        websocket
    )

    try:
        while True:
            message = await websocket.receive_json()
            action = message.get("action")

            if action == "subscribe_project":
                await realtime_service.subscribe_to_project(
                    websocket=websocket,
                    project_id=message[
                        "project_id"
                    ],
                )

    except WebSocketDisconnect:
        realtime_service.manager.disconnect(
            websocket
        )