from fastapi import WebSocket
from typing import Dict, Any

async def handle_ws_get_alert_history(websocket: WebSocket, data: Dict[str, Any]):
    """
    Handle GET_ALERT_HISTORY WebSocket message.
    """
    await websocket.send_json({
        "type": "get_alert_history_response",
        "status": "not_implemented",
        "message": "Get alert history endpoint not implemented yet"
    })
