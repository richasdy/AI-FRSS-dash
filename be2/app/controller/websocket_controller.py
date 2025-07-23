from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
import logging
from typing import Dict, List

from services.yolo_service import yolo_manager
from services.image_service import image_processor

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ws", tags=["WebSocket"])

class ConnectionManager:
    """Manager untuk WebSocket connections"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.client_models: Dict[WebSocket, str] = {}
    
    async def connect(self, websocket: WebSocket, model_name: str = "intrusion"):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.client_models[websocket] = model_name
        logger.info(f"Client connected with model: {model_name}")
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            if websocket in self.client_models:
                del self.client_models[websocket]
        logger.info("Client disconnected")
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_text(json.dumps(message))
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except:
                # Remove broken connections
                self.disconnect(connection)

manager = ConnectionManager()

@router.websocket("/detection/{model_name}")
async def websocket_detection(websocket: WebSocket, model_name: str):
    """
    WebSocket endpoint untuk real-time object detection
    
    Expected message format:
    {
        "type": "image",
        "data": "base64_image_string",
        "confidence": 0.5  // optional
    }
    
    Response format:
    {
        "type": "detection_result",
        "model_used": "intrusion",
        "detections": [...],
        "image_with_boxes": "base64_string"  // optional
    }
    """
    
    await manager.connect(websocket, model_name)
    
    try:
        # Send welcome message
        await manager.send_personal_message({
            "type": "connection_established",
            "model": model_name,
            "message": f"Connected to {model_name} detection service"
        }, websocket)
        
        while True:
            # Receive message
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                
                if message.get("type") == "image":
                    # Process image detection
                    base64_image = message.get("data")
                    confidence = message.get("confidence", 0.5)
                    draw_boxes = message.get("draw_boxes", True)
                    
                    if not base64_image:
                        await manager.send_personal_message({
                            "type": "error",
                            "message": "No image data provided"
                        }, websocket)
                        continue
                    
                    # Convert base64 to image
                    image = image_processor.base64_to_image(base64_image)
                    image = image_processor.resize_image(image)
                    
                    # Predict using YOLO
                    detections = yolo_manager.predict(
                        model_name=model_name,
                        image=image,
                        conf=confidence
                    )
                    
                    response = {
                        "type": "detection_result",
                        "model_used": model_name,
                        "image_size": {"width": image.width, "height": image.height},
                        "detections_count": len(detections),
                        "detections": detections,
                        "timestamp": message.get("timestamp")
                    }
                    
                    # Add processed image if requested
                    if draw_boxes and detections:
                        image_with_boxes = image_processor.draw_detections(image, detections)
                        response["image_with_boxes"] = image_processor.image_to_base64(image_with_boxes)
                    
                    await manager.send_personal_message(response, websocket)
                
                elif message.get("type") == "change_model":
                    # Change model for this client
                    new_model = message.get("model")
                    if new_model in yolo_manager.model_configs:
                        manager.client_models[websocket] = new_model
                        model_name = new_model  # Update current model
                        
                        await manager.send_personal_message({
                            "type": "model_changed",
                            "new_model": new_model,
                            "message": f"Model changed to {new_model}"
                        }, websocket)
                    else:
                        await manager.send_personal_message({
                            "type": "error",
                            "message": f"Model {new_model} not available"
                        }, websocket)
                
                elif message.get("type") == "ping":
                    # Health check
                    await manager.send_personal_message({
                        "type": "pong",
                        "timestamp": message.get("timestamp")
                    }, websocket)
                
                else:
                    await manager.send_personal_message({
                        "type": "error",
                        "message": f"Unknown message type: {message.get('type')}"
                    }, websocket)
                    
            except json.JSONDecodeError:
                await manager.send_personal_message({
                    "type": "error",
                    "message": "Invalid JSON format"
                }, websocket)
                
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                await manager.send_personal_message({
                    "type": "error",
                    "message": f"Processing error: {str(e)}"
                }, websocket)
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info(f"Client disconnected from {model_name} detection")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)

@router.websocket("/detection-all")
async def websocket_multi_detection(websocket: WebSocket):
    """
    WebSocket endpoint untuk real-time detection menggunakan semua model
    
    Expected message format:
    {
        "type": "image",
        "data": "base64_image_string",
        "confidence": 0.5,
        "combine_results": true
    }
    """
    
    await manager.connect(websocket, "multi-model")
    
    try:
        # Send welcome message
        await manager.send_personal_message({
            "type": "connection_established",
            "model": "all-models",
            "message": "Connected to multi-model detection service",
            "available_models": list(yolo_manager.model_configs.keys())
        }, websocket)
        
        while True:
            # Receive message
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                
                if message.get("type") == "image":
                    # Process image detection dengan semua model
                    base64_image = message.get("data")
                    confidence = message.get("confidence", 0.5)
                    draw_boxes = message.get("draw_boxes", True)
                    combine_results = message.get("combine_results", False)
                    
                    if not base64_image:
                        await manager.send_personal_message({
                            "type": "error",
                            "message": "No image data provided"
                        }, websocket)
                        continue
                    
                    # Convert base64 to image
                    image = image_processor.base64_to_image(base64_image)
                    image = image_processor.resize_image(image)
                    
                    # Predict menggunakan semua model YOLO
                    multi_results = yolo_manager.predict_multi_model(
                        image=image,
                        conf=confidence
                    )
                    
                    # Hitung total deteksi
                    total_detections = sum(len(detections) for detections in multi_results.values())
                    
                    response = {
                        "type": "multi_detection_result",
                        "models_used": list(multi_results.keys()),
                        "image_size": {"width": image.width, "height": image.height},
                        "total_detections": total_detections,
                        "combined_results": multi_results,
                        "timestamp": message.get("timestamp")
                    }
                    
                    # Jika diminta, gabungkan hasil
                    if combine_results:
                        combined_detections = yolo_manager.get_combined_detections(multi_results)
                        response["combined_detections"] = combined_detections
                    
                    # Add processed image if requested
                    if draw_boxes and total_detections > 0:
                        if combine_results:
                            detections_to_draw = yolo_manager.get_combined_detections(multi_results)
                        else:
                            # Draw dengan warna berbeda per model
                            detections_to_draw = []
                            for model_name, detections in multi_results.items():
                                for detection in detections:
                                    detection["source_model"] = model_name
                                    detections_to_draw.append(detection)
                        
                        image_with_boxes = image_processor.draw_detections(image, detections_to_draw)
                        response["image_with_boxes"] = image_processor.image_to_base64(image_with_boxes)
                    
                    # Debug logging
                    logger.info(f"Multi-model response: models={response['models_used']}, total={response['total_detections']}")
                    for model_name, detections in multi_results.items():
                        logger.info(f"  {model_name}: {len(detections)} detections")
                    
                    await manager.send_personal_message(response, websocket)
                
                elif message.get("type") == "ping":
                    # Health check
                    await manager.send_personal_message({
                        "type": "pong",
                        "timestamp": message.get("timestamp"),
                        "loaded_models": list(yolo_manager.loaded_models.keys())
                    }, websocket)
                
                else:
                    await manager.send_personal_message({
                        "type": "error",
                        "message": f"Unknown message type: {message.get('type')}"
                    }, websocket)
                    
            except json.JSONDecodeError:
                await manager.send_personal_message({
                    "type": "error",
                    "message": "Invalid JSON format"
                }, websocket)
                
            except Exception as e:
                logger.error(f"Error processing multi-model message: {e}")
                await manager.send_personal_message({
                    "type": "error",
                    "message": f"Processing error: {str(e)}"
                }, websocket)
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("Client disconnected from multi-model detection")
    except Exception as e:
        logger.error(f"Multi-model WebSocket error: {e}")
        manager.disconnect(websocket)
