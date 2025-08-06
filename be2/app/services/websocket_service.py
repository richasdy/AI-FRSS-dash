import json
import logging
from datetime import datetime
from typing import Dict, Any
from fastapi import WebSocket

# Import YOLO service for real detection
from app.services.models_service import yolo_service

logger = logging.getLogger(__name__)

class WebSocketManager:
    """Simple WebSocket connection manager"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.connection_types: Dict[str, str] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str, connection_type: str = "general"):
        """Connect WebSocket client"""
        await websocket.accept()
        self.active_connections[client_id] = websocket
        self.connection_types[client_id] = connection_type
        
        logger.info(f"Client {client_id} connected (type: {connection_type})")
        
        # Send welcome message
        await self.send_message(client_id, {
            "type": "connection_established",
            "client_id": client_id,
            "connection_type": connection_type,
            "timestamp": datetime.now().isoformat()
        })
    
    def disconnect(self, client_id: str):
        """Disconnect WebSocket client"""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            del self.connection_types[client_id]
            logger.info(f"Client {client_id} disconnected")
    
    async def send_message(self, client_id: str, message: Dict[str, Any]):
        """Send message to specific client"""
        if client_id in self.active_connections:
            try:
                await self.active_connections[client_id].send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Error sending message to {client_id}: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get connection statistics"""
        return {
            "total_connections": len(self.active_connections),
            "active_clients": list(self.active_connections.keys()),
            "connection_types": self.connection_types
        }

class WebSocketService:
    """WebSocket message handler service - Based on be3 pattern"""
    
    def __init__(self):
        self.manager = WebSocketManager()
    
    async def handle_message(self, client_id: str, message_text: str):
        """Handle incoming WebSocket message"""
        try:
            message = json.loads(message_text)
            message_type = message.get("type")
            
            # Route messages based on type (similar to be3 webSocketController)
            if message_type == "ping":
                await self._handle_ping(client_id, message)
            elif message_type == "recognize_face":
                await self._handle_recognize_face(client_id, message)
            elif message_type == "insert_face":
                await self._handle_insert_face(client_id, message)
            elif message_type == "insert_admin":
                await self._handle_insert_admin(client_id, message)
            elif message_type == "LOGIN_REQUEST":
                await self._handle_login(client_id, message)
            elif message_type == "GET_PROFILE_REQUEST":
                await self._handle_get_profile(client_id, message)
            elif message_type == "UPDATE_PROFILE_REQUEST":
                await self._handle_update_profile(client_id, message)
            elif message_type == "INSERT_ATTENDANCE":
                await self._handle_insert_attendance(client_id, message)
            elif message_type == "check_image":
                await self._handle_check_image(client_id, message)
            elif message_type == "multi_model_detection":
                await self._handle_multi_model_detection(client_id, message)
            elif message_type == "get_available_models":
                await self._handle_get_available_models(client_id, message)
            else:
                await self.manager.send_message(client_id, {
                    "type": "error",
                    "message": f"Unknown message type: {message_type}",
                    "timestamp": datetime.now().isoformat()
                })
                
        except json.JSONDecodeError:
            await self.manager.send_message(client_id, {
                "type": "error",
                "message": "Invalid JSON format",
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            logger.error(f"Error handling message from {client_id}: {str(e)}")
            await self.manager.send_message(client_id, {
                "type": "error",
                "message": f"Internal server error: {str(e)}",
                "timestamp": datetime.now().isoformat()
            })
    
    # Message handlers (placeholder implementations)
    async def _handle_ping(self, client_id: str, message: dict):
        await self.manager.send_message(client_id, {
            "type": "pong",
            "timestamp": datetime.now().isoformat()
        })
    
    async def _handle_recognize_face(self, client_id: str, message: dict):
        await self.manager.send_message(client_id, {
            "type": "face_recognition_result",
            "status": "not_implemented",
            "message": "Face recognition coming soon",
            "timestamp": datetime.now().isoformat()
        })
    
    async def _handle_insert_face(self, client_id: str, message: dict):
        await self.manager.send_message(client_id, {
            "type": "face_insert_result",
            "status": "not_implemented",
            "message": "Face insertion coming soon",
            "timestamp": datetime.now().isoformat()
        })
    
    async def _handle_insert_admin(self, client_id: str, message: dict):
        await self.manager.send_message(client_id, {
            "type": "admin_insert_result",
            "status": "not_implemented",
            "message": "Admin management coming soon",
            "timestamp": datetime.now().isoformat()
        })
    
    async def _handle_login(self, client_id: str, message: dict):
        await self.manager.send_message(client_id, {
            "type": "login_response",
            "status": "not_implemented",
            "message": "Authentication coming soon",
            "timestamp": datetime.now().isoformat()
        })
    
    async def _handle_get_profile(self, client_id: str, message: dict):
        await self.manager.send_message(client_id, {
            "type": "profile_response",
            "status": "not_implemented",
            "message": "Profile system coming soon",
            "timestamp": datetime.now().isoformat()
        })
    
    async def _handle_update_profile(self, client_id: str, message: dict):
        await self.manager.send_message(client_id, {
            "type": "profile_update_result",
            "status": "not_implemented",
            "message": "Profile update coming soon",
            "timestamp": datetime.now().isoformat()
        })
    
    async def _handle_insert_attendance(self, client_id: str, message: dict):
        await self.manager.send_message(client_id, {
            "type": "attendance_result",
            "status": "not_implemented",
            "message": "Attendance system coming soon",
            "timestamp": datetime.now().isoformat()
        })
    
    async def _handle_check_image(self, client_id: str, message: dict):
        """Handle real image detection using YOLO"""
        message_id = message.get("message_id", f"detection_{int(datetime.now().timestamp())}")
        
        try:
            # Extract parameters
            image_data = message.get("image_data")
            model_type = message.get("model", "intrusion")
            confidence = message.get("confidence", 0.5)
            iou_threshold = message.get("iou_threshold", 0.45)
            
            if not image_data:
                await self.manager.send_message(client_id, {
                    "type": "error",
                    "message_id": message_id,
                    "error": "No image data provided",
                    "timestamp": datetime.now().isoformat()
                })
                return
            
            # Perform real YOLO detection
            result = await yolo_service.detect_objects(
                model_type=model_type,
                image_data=image_data,
                confidence=confidence,
                iou_threshold=iou_threshold
            )
            
            # Send successful result
            await self.manager.send_message(client_id, {
                "type": "detection_result",
                "message_id": message_id,
                "model_type": model_type,
                "success": result.get("success", True),
                "detections": result.get("detections", []),
                "total_detections": result.get("total_detections", 0),
                "processing_time": result.get("processing_time", 0),
                "image_size": result.get("image_size", []),
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            await self.manager.send_message(client_id, {
                "type": "error",
                "message_id": message_id,
                "error": f"Detection failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            })
    
    async def _handle_multi_model_detection(self, client_id: str, message: dict):
        """Handle multi-model detection"""
        message_id = message.get("message_id", f"multi_detection_{int(datetime.now().timestamp())}")
        
        try:
            # Extract parameters
            image_data = message.get("image_data")
            models_to_use = message.get("models", ["intrusion", "people", "security_threats", "vehicle"])
            confidence = message.get("confidence", 0.5)
            iou_threshold = message.get("iou_threshold", 0.45)
            
            if not image_data:
                await self.manager.send_message(client_id, {
                    "type": "error",
                    "message_id": message_id,
                    "error": "No image data provided",
                    "timestamp": datetime.now().isoformat()
                })
                return
            
            # Run detection on all requested models
            results = {}
            total_detections = 0
            successful_models = []
            
            for model in models_to_use:
                try:
                    result = await yolo_service.detect_objects(
                        model_type=model,
                        image_data=image_data,
                        confidence=confidence,
                        iou_threshold=iou_threshold
                    )
                    results[model] = result
                    if result.get("detections"):
                        total_detections += len(result["detections"])
                        successful_models.append(model)
                except Exception as e:
                    results[model] = {
                        "success": False,
                        "error": str(e),
                        "detections": [],
                        "processing_time": 0
                    }
            
            # Send results
            await self.manager.send_message(client_id, {
                "type": "multi_detection_result",
                "message_id": message_id,
                "results": results,
                "summary": {
                    "total_detections": total_detections,
                    "models_used": successful_models,
                    "models_requested": models_to_use,
                    "success_rate": f"{len(successful_models)}/{len(models_to_use)}"
                },
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            await self.manager.send_message(client_id, {
                "type": "error",
                "message_id": message_id,
                "error": f"Multi-model detection failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            })
    
    async def _handle_get_available_models(self, client_id: str, message: dict):
        """Handle get available models request"""
        message_id = message.get("message_id", f"models_{int(datetime.now().timestamp())}")
        
        try:
            models_info = await yolo_service.list_all_models()
            await self.manager.send_message(client_id, {
                "type": "available_models",
                "message_id": message_id,
                "models": models_info,
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            await self.manager.send_message(client_id, {
                "type": "error",
                "message_id": message_id,
                "error": f"Failed to get models info: {str(e)}",
                "timestamp": datetime.now().isoformat()
            })

# Global instance
websocket_service = WebSocketService()
