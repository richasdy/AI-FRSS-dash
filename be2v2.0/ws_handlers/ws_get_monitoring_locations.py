from fastapi import WebSocket
from typing import Dict, Any

async def handle_ws_get_monitoring_locations(websocket: WebSocket, data: Dict[str, Any]):
    """
    Handle GET_MONITORING_LOCATIONS WebSocket message.
    """
    await websocket.send_json({
        "type": "get_monitoring_locations_response",
        "status": "not_implemented",
        "message": "Get monitoring locations endpoint not implemented yet"
    })
