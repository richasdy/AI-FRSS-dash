from fastapi import WebSocket
from typing import Dict, Any

async def handle_ws_get_attendance_report(websocket: WebSocket, data: Dict[str, Any]):
    """
    Handle GET_ATTENDANCE_REPORT WebSocket message.
    """
    await websocket.send_json({
        "type": "get_attendance_report_response",
        "status": "not_implemented",
        "message": "Get attendance report endpoint not implemented yet"
    })
