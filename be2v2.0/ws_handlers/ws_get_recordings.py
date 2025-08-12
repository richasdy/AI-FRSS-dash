from fastapi import WebSocket
from typing import Dict, Any

async def handle_ws_get_recordings(websocket: WebSocket, data: Dict[str, Any]):
    """
    Handle GET_RECORDINGS WebSocket message.
    """
    await websocket.send_json({
        "type": "get_recordings_response",
        "status": "not_implemented",
        "message": "Get recordings endpoint not implemented yet"
    })
