from fastapi import WebSocket
from typing import Dict, Any

async def handle_ws_get_users(websocket: WebSocket, data: Dict[str, Any]):
    """
    Handle GET_USERS WebSocket message.
    """
    await websocket.send_json({
        "type": "get_users_response",
        "status": "not_implemented",
        "message": "Get users endpoint not implemented yet"
    })
