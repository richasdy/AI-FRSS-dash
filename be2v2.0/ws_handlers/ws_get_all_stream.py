from fastapi import WebSocket
from typing import Dict, Any

async def handle_ws_get_all_stream(websocket: WebSocket, data: Dict[str, Any]):
    """
    Handle GET_ALL_STREAM WebSocket message.
    """
    await websocket.send_json({
        "type": "get_all_stream_response",
        "status": "not_implemented",
        "message": "Get all stream endpoint not implemented yet"
    })
