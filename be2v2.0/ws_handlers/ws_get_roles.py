from fastapi import WebSocket
from typing import Dict, Any

async def handle_ws_get_roles(websocket: WebSocket, data: Dict[str, Any]):
    """
    Handle GET_ROLES WebSocket message.
    """
    await websocket.send_json({
        "type": "get_roles_response",
        "status": "not_implemented",
        "message": "Get roles endpoint not implemented yet"
    })
