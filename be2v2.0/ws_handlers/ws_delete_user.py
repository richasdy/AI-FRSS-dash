from fastapi import WebSocket
from typing import Dict, Any

async def handle_ws_delete_user(websocket: WebSocket, data: Dict[str, Any]):
    """
    Handle DELETE_USER WebSocket message.
    """
    await websocket.send_json({
        "type": "delete_user_response",
        "status": "not_implemented",
        "message": "Delete user endpoint not implemented yet"
    })
