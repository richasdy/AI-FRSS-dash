from fastapi import WebSocket
from typing import Dict, Any

async def handle_ws_reject_user(websocket: WebSocket, data: Dict[str, Any]):
    """
    Handle REJECT_USER WebSocket message.
    """
    await websocket.send_json({
        "type": "reject_user_response",
        "status": "not_implemented",
        "message": "Reject user endpoint not implemented yet"
    })
