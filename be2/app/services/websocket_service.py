"""
Unified WebSocket Service
Central WebSocket management for real-time surveillance system
"""
import json
import uuid
import asyncio
import logging
import sys
import os
from typing import Dict, List, Any, Optional, Set
from datetime import datetime
from fastapi import WebSocket, WebSocketDisconnect

# Add the parent directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from app.services.models_service import yolo_service
except ImportError:
    # Fallback for direct execution
    from models_service import yolo_service

logger = logging.getLogger(__name__)

class WebSocketConnectionManager:
    """Manages all WebSocket connections and message routing"""
    
    def __init__(self):
        # Connection storage
        self.active_connections: Dict[str, WebSocket] = {}
        self.connection_metadata: Dict[str, Dict] = {}
        
        # Topic subscriptions for pub/sub pattern
        self.subscriptions: Dict[str, Set[str]] = {
            "detections": set(),
            "video_processing": set(),
            "cctv_feeds": set(),
            "system_alerts": set()
        }
        
        # Session statistics
        self.session_stats: Dict[str, Dict] = {}
        
    async def connect(self, websocket: WebSocket, client_id: str = None) -> str:
        """Connect new WebSocket client"""
        await websocket.accept()
        
        # Generate unique client ID if not provided
        if not client_id:
            client_id = f"client_{uuid.uuid4().hex[:8]}"
        
        # Store connection
        self.active_connections[client_id] = websocket
        self.connection_metadata[client_id] = {
            "connected_at": datetime.now().isoformat(),
            "ip_address": websocket.client.host if websocket.client else "unknown",
            "subscriptions": [],
            "last_activity": datetime.now().isoformat()
        }
        self.session_stats[client_id] = {
            "messages_sent": 0,
            "messages_received": 0,
            "detections_processed": 0,
            "errors": 0
        }
        
        logger.info(f"WebSocket client connected: {client_id}")
        
        # Send welcome message
        await self.send_personal_message(client_id, {
            "type": "connection_established",
            "client_id": client_id,
            "server_time": datetime.now().isoformat(),
            "available_topics": list(self.subscriptions.keys())
        })
        
        return client_id
    
    def disconnect(self, client_id: str):
        """Disconnect WebSocket client"""
        if client_id in self.active_connections:
            # Remove from subscriptions
            for topic_subscribers in self.subscriptions.values():
                topic_subscribers.discard(client_id)
            
            # Clean up data
            del self.active_connections[client_id]
            del self.connection_metadata[client_id]
            del self.session_stats[client_id]
            
            logger.info(f"WebSocket client disconnected: {client_id}")
    
    async def send_personal_message(self, client_id: str, message: Dict[str, Any]):
        """Send message to specific client"""
        if client_id in self.active_connections:
            try:
                websocket = self.active_connections[client_id]
                await websocket.send_text(json.dumps(message))
                self.session_stats[client_id]["messages_sent"] += 1
                self.connection_metadata[client_id]["last_activity"] = datetime.now().isoformat()
            except Exception as e:
                logger.error(f"Error sending message to {client_id}: {e}")
                self.session_stats[client_id]["errors"] += 1
    
    async def broadcast_to_topic(self, topic: str, message: Dict[str, Any]):
        """Broadcast message to all subscribers of a topic"""
        if topic in self.subscriptions:
            subscribers = self.subscriptions[topic].copy()
            for client_id in subscribers:
                await self.send_personal_message(client_id, message)
    
    def subscribe_to_topic(self, client_id: str, topic: str):
        """Subscribe client to a topic"""
        if topic in self.subscriptions and client_id in self.active_connections:
            self.subscriptions[topic].add(client_id)
            self.connection_metadata[client_id]["subscriptions"].append(topic)
            logger.info(f"Client {client_id} subscribed to {topic}")
    
    def unsubscribe_from_topic(self, client_id: str, topic: str):
        """Unsubscribe client from a topic"""
        if topic in self.subscriptions:
            self.subscriptions[topic].discard(client_id)
            if client_id in self.connection_metadata:
                self.connection_metadata[client_id]["subscriptions"] = [
                    t for t in self.connection_metadata[client_id]["subscriptions"] if t != topic
                ]
            logger.info(f"Client {client_id} unsubscribed from {topic}")
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get overall connection statistics"""
        return {
            "total_connections": len(self.active_connections),
            "active_clients": list(self.active_connections.keys()),
            "topic_subscriptions": {
                topic: len(subscribers) for topic, subscribers in self.subscriptions.items()
            },
            "server_uptime": datetime.now().isoformat()
        }

class UnifiedWebSocketService:
    """Main WebSocket service handling all real-time communications"""
    
    def __init__(self):
        self.connection_manager = WebSocketConnectionManager()
        self.message_handlers = {
            "ping": self._handle_ping,
            "subscribe": self._handle_subscribe,
            "unsubscribe": self._handle_unsubscribe,
            "detect": self._handle_detection,
            "video_stream": self._handle_video_stream,
            "cctv_control": self._handle_cctv_control,
            "get_stats": self._handle_get_stats,
            "get_models": self._handle_get_models
        }
    
    async def handle_client_connection(self, websocket: WebSocket, client_id: str = None):
        """Handle new WebSocket client connection"""
        client_id = await self.connection_manager.connect(websocket, client_id)
        
        try:
            while True:
                # Receive message from client
                data = await websocket.receive_text()
                await self._process_message(client_id, data)
                
        except WebSocketDisconnect:
            logger.info(f"Client {client_id} disconnected")
        except Exception as e:
            logger.error(f"Error handling client {client_id}: {e}")
            await self.connection_manager.send_personal_message(client_id, {
                "type": "error",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            })
        finally:
            self.connection_manager.disconnect(client_id)
    
    async def _process_message(self, client_id: str, raw_message: str):
        """Process incoming WebSocket message"""
        try:
            message = json.loads(raw_message)
            message_type = message.get("type")
            message_id = message.get("message_id", str(uuid.uuid4()))
            
            # Update client stats
            self.connection_manager.session_stats[client_id]["messages_received"] += 1
            
            if message_type in self.message_handlers:
                await self.message_handlers[message_type](client_id, message, message_id)
            else:
                await self.connection_manager.send_personal_message(client_id, {
                    "type": "error",
                    "message": f"Unknown message type: {message_type}",
                    "message_id": message_id,
                    "timestamp": datetime.now().isoformat()
                })
                
        except json.JSONDecodeError:
            await self.connection_manager.send_personal_message(client_id, {
                "type": "error",
                "message": "Invalid JSON format",
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            logger.error(f"Error processing message from {client_id}: {e}")
            await self.connection_manager.send_personal_message(client_id, {
                "type": "error",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            })
    
    # Message Handlers
    async def _handle_ping(self, client_id: str, message: Dict, message_id: str):
        """Handle ping message"""
        await self.connection_manager.send_personal_message(client_id, {
            "type": "pong",
            "message_id": message_id,
            "timestamp": datetime.now().isoformat()
        })
    
    async def _handle_subscribe(self, client_id: str, message: Dict, message_id: str):
        """Handle topic subscription"""
        topic = message.get("topic")
        if topic:
            self.connection_manager.subscribe_to_topic(client_id, topic)
            await self.connection_manager.send_personal_message(client_id, {
                "type": "subscription_confirmed",
                "topic": topic,
                "message_id": message_id,
                "timestamp": datetime.now().isoformat()
            })
    
    async def _handle_unsubscribe(self, client_id: str, message: Dict, message_id: str):
        """Handle topic unsubscription"""
        topic = message.get("topic")
        if topic:
            self.connection_manager.unsubscribe_from_topic(client_id, topic)
            await self.connection_manager.send_personal_message(client_id, {
                "type": "unsubscription_confirmed",
                "topic": topic,
                "message_id": message_id,
                "timestamp": datetime.now().isoformat()
            })
    
    async def _handle_detection(self, client_id: str, message: Dict, message_id: str):
        """Handle YOLO detection request"""
        try:
            model_type = message.get("model", "intrusion")
            image_data = message.get("data")
            confidence = message.get("confidence", 0.5)
            iou_threshold = message.get("iou_threshold", 0.45)
            
            if not image_data:
                raise ValueError("No image data provided")
            
            # Perform detection
            result = await yolo_service.detect_objects(
                model_type=model_type,
                image_data=image_data,
                confidence=confidence,
                iou_threshold=iou_threshold
            )
            
            # Update stats
            self.connection_manager.session_stats[client_id]["detections_processed"] += 1
            
            # Send result back to client
            response = {
                "type": "detection_result",
                "message_id": message_id,
                "model_type": model_type,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
            
            await self.connection_manager.send_personal_message(client_id, response)
            
            # Broadcast to detection subscribers if enabled
            if result.get("detections"):
                await self.connection_manager.broadcast_to_topic("detections", {
                    "type": "detection_alert",
                    "client_id": client_id,
                    "model_type": model_type,
                    "detections_count": len(result["detections"]),
                    "timestamp": datetime.now().isoformat()
                })
                
        except Exception as e:
            await self.connection_manager.send_personal_message(client_id, {
                "type": "detection_error",
                "message_id": message_id,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
    
    async def _handle_video_stream(self, client_id: str, message: Dict, message_id: str):
        """Handle video streaming (placeholder for future implementation)"""
        await self.connection_manager.send_personal_message(client_id, {
            "type": "video_stream_response",
            "message_id": message_id,
            "status": "received",
            "message": "Video streaming not yet implemented",
            "timestamp": datetime.now().isoformat()
        })
    
    async def _handle_cctv_control(self, client_id: str, message: Dict, message_id: str):
        """Handle CCTV control commands (placeholder for future implementation)"""
        await self.connection_manager.send_personal_message(client_id, {
            "type": "cctv_control_response",
            "message_id": message_id,
            "status": "received",
            "message": "CCTV control not yet implemented",
            "timestamp": datetime.now().isoformat()
        })
    
    async def _handle_get_stats(self, client_id: str, message: Dict, message_id: str):
        """Handle statistics request"""
        stats = {
            "connection_stats": self.connection_manager.get_connection_stats(),
            "client_stats": self.connection_manager.session_stats.get(client_id, {}),
            "client_metadata": self.connection_manager.connection_metadata.get(client_id, {})
        }
        
        await self.connection_manager.send_personal_message(client_id, {
            "type": "stats_response",
            "message_id": message_id,
            "stats": stats,
            "timestamp": datetime.now().isoformat()
        })
    
    async def _handle_get_models(self, client_id: str, message: Dict, message_id: str):
        """Handle available models request"""
        try:
            models_info = await yolo_service.list_all_models()
            await self.connection_manager.send_personal_message(client_id, {
                "type": "models_response",
                "message_id": message_id,
                "models": models_info,
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            await self.connection_manager.send_personal_message(client_id, {
                "type": "models_error",
                "message_id": message_id,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })

# Global service instance
websocket_service = UnifiedWebSocketService()
