from fastapi import WebSocket
from typing import Dict, Any

async def handle_ws_reset_user_password(websocket: WebSocket, data: Dict[str, Any]):
    """
    Handle RESET_USER_PASSWORD WebSocket message.
    """
    await websocket.send_json({
        "type": "reset_user_password_response",
        "status": "not_implemented",
        "message": "Reset user password endpoint not implemented yet"
    })
