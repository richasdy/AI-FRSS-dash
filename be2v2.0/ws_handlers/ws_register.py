from fastapi import WebSocket
from typing import Dict, Any

async def handle_ws_register(websocket: WebSocket, data: Dict[str, Any]):
    """
    Handle REGISTER_REQUEST WebSocket message.
    """
    await websocket.send_json({
        "type": "register_response",
        "status": "not_implemented",
        "message": "Register endpoint not implemented yet"
    })
