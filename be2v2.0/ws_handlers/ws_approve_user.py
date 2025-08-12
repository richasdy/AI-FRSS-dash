from fastapi import WebSocket
from typing import Dict, Any

async def handle_ws_approve_user(websocket: WebSocket, data: Dict[str, Any]):
    """
    Handle APPROVE_USER WebSocket message.
    """
    await websocket.send_json({
        "type": "approve_user_response",
        "status": "not_implemented",
        "message": "Approve user endpoint not implemented yet"
    })
