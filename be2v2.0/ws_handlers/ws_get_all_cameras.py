from fastapi import WebSocket
from typing import Dict, Any

async def handle_ws_get_all_cameras(websocket: WebSocket, data: Dict[str, Any]):
    """
    Handle GET_ALL_CAMERAS WebSocket message.
    """
    await websocket.send_json({
        "type": "get_all_cameras_response",
        "status": "not_implemented",
        "message": "Get all cameras endpoint not implemented yet"
    })
