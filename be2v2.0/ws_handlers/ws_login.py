from fastapi import WebSocket
from typing import Dict, Any

async def handle_ws_login(websocket: WebSocket, data: Dict[str, Any]):
    """
    Handle LOGIN_REQUEST WebSocket message.
    """
    await websocket.send_json({
        "type": "login_response",
        "status": "not_implemented",
        "message": "Login endpoint not implemented yet"
    })
