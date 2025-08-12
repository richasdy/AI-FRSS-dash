from fastapi import WebSocket
from typing import Dict, Any

async def handle_ws_get_dashboard_data(websocket: WebSocket, data: Dict[str, Any]):
    """
    Handle GET_DASHBOARD_DATA WebSocket message.
    """
    await websocket.send_json({
        "type": "get_dashboard_data_response",
        "status": "not_implemented",
        "message": "Get dashboard data endpoint not implemented yet"
    })
