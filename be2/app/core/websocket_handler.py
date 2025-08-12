"""
WebSocket handlers following be2v2.0 pattern
Centralized WebSocket connection handling
"""

from fastapi import WebSocket, WebSocketDisconnect
from app.services.websocket_service import websocket_service
import logging
import json

logger = logging.getLogger(__name__)

async def handle_websocket_connection(websocket: WebSocket, client_id: str, connection_type: str = "general"):
    """Clean WebSocket connection handler (be2v2.0 pattern)"""
    try:
        await websocket_service.manager.connect(websocket, client_id, connection_type)
        
        while True:
            try:
                message_text = await websocket.receive_text()
                await websocket_service.handle_message(client_id, message_text)
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"Error handling message from {client_id}: {str(e)}")
                break
                
    except Exception as e:
        logger.error(f"WebSocket connection error for {client_id}: {str(e)}")
    finally:
        websocket_service.manager.disconnect(client_id)
        logger.info(f"Client {client_id} disconnected")
