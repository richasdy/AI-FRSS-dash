"""
FastAPI WebSocket-Based Surveillance API Server
Real-time video detection and monitoring system
"""
import sys
import os
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from typing import Optional

# Setup Python path for proper imports
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = current_dir
be2_dir = os.path.dirname(current_dir)

# Add be2 directory to Python path so 'app' package can be found
if be2_dir not in sys.path:
    sys.path.insert(0, be2_dir)

# Import services
from app.services.database_service import database_service
from app.services.websocket_service import websocket_service

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("Starting WebSocket Surveillance API server...")
    
    # Try to initialize database connection (optional)
    try:
        await database_service.connect()
        logger.info("Database connected successfully")
    except Exception as e:
        logger.warning(f"Database connection failed: {str(e)} - API will run without database")
    
    # Initialize WebSocket service
    logger.info("WebSocket service initialized and ready")
    
    yield
    
    # Cleanup
    logger.info("Shutting down WebSocket Surveillance API server...")
    try:
        await database_service.disconnect()
    except Exception:
        pass

# Create FastAPI application
app = FastAPI(
    title="WebSocket Surveillance API",
    description="Real-time video detection and monitoring system via WebSocket",
    version="2.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "websocket-surveillance-api", "version": "2.0.0"}

@app.get("/")
async def root():
    """Root endpoint with WebSocket connection info"""
    return {
        "message": "WebSocket Surveillance API Server", 
        "version": "2.0.0",
        "websocket_endpoints": {
            "main": "/ws",
            "image_check": "/ws/check-image"
        },
        "http_endpoints": {
            "health": "/health",
            "multi_model_check": "/api/v1/check-image",
            "legacy_apis": "/api/v1/*"
        },
        "connection_stats": websocket_service.connection_manager.get_connection_stats(),
        "available_message_types": [
            "ping", "subscribe", "unsubscribe", "detect", 
            "video_stream", "cctv_control", "get_stats", "get_models"
        ],
        "image_check_message_types": [
            "check_image", "ping", "get_available_models"
        ],
        "supported_models": ["intrusion", "people", "security_threats", "vehicle"]
    }

# Main WebSocket Endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, client_id: Optional[str] = None):
    """
    Main WebSocket endpoint for all real-time surveillance communications
    
    **Connection:** ws://localhost:8000/ws?client_id=optional_id
    
    **Message Format:**
    ```json
    {
        "type": "detect|subscribe|ping|get_stats|get_models",
        "message_id": "unique_id",
        "data": {...},
        "timestamp": "ISO_timestamp"
    }
    ```
    
    **Detection Example:**
    ```json
    {
        "type": "detect",
        "message_id": "det_001",
        "model": "intrusion",
        "data": "base64_image_data",
        "confidence": 0.6,
        "iou_threshold": 0.45
    }
    ```
    
    **Subscribe Example:**
    ```json
    {
        "type": "subscribe",
        "topic": "detections"
    }
    ```
    """
    await websocket_service.handle_client_connection(websocket, client_id)

# Image Check WebSocket Endpoint - Multi-Model Detection
@app.websocket("/ws/check-image")
async def websocket_check_image(websocket: WebSocket, client_id: Optional[str] = None):
    """
    WebSocket endpoint specifically for image checking using all available models
    
    **Connection:** ws://localhost:8000/ws/check-image?client_id=optional_id
    
    **Message Format:**
    ```json
    {
        "type": "check_image",
        "message_id": "unique_id",
        "image_data": "base64_image_data",
        "models": ["intrusion", "people", "security_threats", "vehicle"],
        "confidence": 0.5,
        "iou_threshold": 0.45,
        "return_annotated": true
    }
    ```
    
    **Response Format:**
    ```json
    {
        "type": "multi_detection_result",
        "message_id": "unique_id",
        "results": {
            "intrusion": {...},
            "people": {...},
            "security_threats": {...},
            "vehicle": {...}
        },
        "summary": {
            "total_detections": 5,
            "models_used": ["intrusion", "people"],
            "processing_time": 1.23
        },
        "timestamp": "ISO_timestamp"
    }
    ```
    """
    from app.services.models_service import yolo_service
    import json
    import time
    from datetime import datetime
    
    # Accept connection
    await websocket.accept()
    
    # Generate client ID if not provided
    if not client_id:
        import uuid
        client_id = f"img_check_{uuid.uuid4().hex[:8]}"
    
    logger.info(f"Image check WebSocket client connected: {client_id}")
    
    # Send welcome message
    await websocket.send_text(json.dumps({
        "type": "connection_established",
        "client_id": client_id,
        "server_time": datetime.now().isoformat(),
        "available_models": ["intrusion", "people", "security_threats", "vehicle"],
        "message": "Ready for image checking"
    }))
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "check_image":
                start_time = time.time()
                message_id = message.get("message_id", f"check_{int(time.time())}")
                image_data = message.get("image_data")
                models_to_use = message.get("models", ["intrusion", "people", "security_threats", "vehicle"])
                confidence = message.get("confidence", 0.5)
                iou_threshold = message.get("iou_threshold", 0.45)
                return_annotated = message.get("return_annotated", False)
                
                if not image_data:
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "message_id": message_id,
                        "error": "No image data provided",
                        "timestamp": datetime.now().isoformat()
                    }))
                    continue
                
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
                        
                        logger.info(f"Model {model} processed successfully for client {client_id}")
                        
                    except Exception as e:
                        results[model] = {
                            "error": str(e),
                            "detections": [],
                            "processing_time": 0
                        }
                        logger.error(f"Error running model {model} for client {client_id}: {str(e)}")
                
                processing_time = time.time() - start_time
                
                # Send comprehensive results
                response = {
                    "type": "multi_detection_result",
                    "message_id": message_id,
                    "client_id": client_id,
                    "results": results,
                    "summary": {
                        "total_detections": total_detections,
                        "models_used": successful_models,
                        "models_requested": models_to_use,
                        "processing_time": round(processing_time, 3),
                        "success_rate": f"{len(successful_models)}/{len(models_to_use)}"
                    },
                    "timestamp": datetime.now().isoformat()
                }
                
                await websocket.send_text(json.dumps(response))
                logger.info(f"Multi-model detection completed for client {client_id}: {total_detections} total detections")
                
            elif message.get("type") == "ping":
                await websocket.send_text(json.dumps({
                    "type": "pong",
                    "message_id": message.get("message_id"),
                    "timestamp": datetime.now().isoformat()
                }))
                
            elif message.get("type") == "get_available_models":
                try:
                    models_info = await yolo_service.list_all_models()
                    await websocket.send_text(json.dumps({
                        "type": "available_models",
                        "message_id": message.get("message_id"),
                        "models": models_info,
                        "timestamp": datetime.now().isoformat()
                    }))
                except Exception as e:
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "message_id": message.get("message_id"),
                        "error": f"Failed to get models info: {str(e)}",
                        "timestamp": datetime.now().isoformat()
                    }))
            
            else:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": f"Unknown message type: {message.get('type')}",
                    "supported_types": ["check_image", "ping", "get_available_models"],
                    "timestamp": datetime.now().isoformat()
                }))
                
    except Exception as e:
        logger.error(f"WebSocket error for image check client {client_id}: {str(e)}")
        try:
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": f"Connection error: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }))
        except:
            pass
    finally:
        logger.info(f"Image check WebSocket client disconnected: {client_id}")

# Multi-Model Image Check HTTP Endpoint (for non-WebSocket clients)
@app.post("/api/v1/check-image")
async def check_image_all_models(
    request: dict
):
    """
    HTTP endpoint for checking image with multiple models simultaneously
    
    **Request Body:**
    ```json
    {
        "image_data": "base64_image_data",
        "models": ["intrusion", "people", "security_threats", "vehicle"],
        "confidence": 0.5,
        "iou_threshold": 0.45
    }
    ```
    """
    from app.services.models_service import yolo_service
    import time
    from datetime import datetime
    
    image_data = request.get("image_data")
    models = request.get("models", ["intrusion", "people", "security_threats", "vehicle"])
    confidence = request.get("confidence", 0.5)
    iou_threshold = request.get("iou_threshold", 0.45)
    
    if not image_data:
        raise HTTPException(status_code=400, detail="No image data provided")
    
    start_time = time.time()
    results = {}
    total_detections = 0
    successful_models = []
    
    # Run detection on all requested models
    for model in models:
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
                "error": str(e),
                "detections": [],
                "processing_time": 0
            }
            logger.error(f"Error running model {model}: {str(e)}")
    
    processing_time = time.time() - start_time
    
    return {
        "results": results,
        "summary": {
            "total_detections": total_detections,
            "models_used": successful_models,
            "models_requested": models,
            "processing_time": round(processing_time, 3),
            "success_rate": f"{len(successful_models)}/{len(models)}"
        },
        "timestamp": datetime.now().isoformat()
    }

# Connection Management Endpoints
@app.get("/ws/stats")
async def get_websocket_stats():
    """Get WebSocket connection statistics"""
    return websocket_service.connection_manager.get_connection_stats()

@app.get("/ws/clients")
async def list_connected_clients():
    """List all connected WebSocket clients"""
    stats = websocket_service.connection_manager.get_connection_stats()
    clients_info = []
    
    for client_id in websocket_service.connection_manager.active_connections.keys():
        metadata = websocket_service.connection_manager.connection_metadata.get(client_id, {})
        session_stats = websocket_service.connection_manager.session_stats.get(client_id, {})
        
        clients_info.append({
            "client_id": client_id,
            "metadata": metadata,
            "stats": session_stats
        })
    
    return {
        "total_clients": len(clients_info),
        "clients": clients_info
    }

@app.delete("/ws/clients/{client_id}")
async def disconnect_client(client_id: str):
    """Force disconnect a WebSocket client"""
    if client_id in websocket_service.connection_manager.active_connections:
        websocket_service.connection_manager.disconnect(client_id)
        return {"message": f"Client {client_id} disconnected"}
    else:
        raise HTTPException(status_code=404, detail="Client not found")

# Authentication (keep as HTTP for security)
try:
    from app.controller.auth_controller import router as auth_router
    app.include_router(auth_router, prefix="/api/v1/auth", tags=["authentication"])
    logger.info("Authentication routes loaded successfully (HTTP)")
except ImportError as e:
    logger.warning(f"Auth routes could not be loaded: {str(e)}")

# Legacy HTTP Model APIs (for backward compatibility)
try:
    from app.api.mobile_v1.models.intrusion_api import router as intrusion_router
    app.include_router(intrusion_router, prefix="/api/v1/intrusion", tags=["intrusion-detection-legacy"])
    logger.info("Legacy intrusion detection routes loaded (HTTP)")
except ImportError as e:
    logger.warning(f"Legacy intrusion routes could not be loaded: {str(e)}")

try:
    from app.api.mobile_v1.models.people_api import router as people_router
    app.include_router(people_router, prefix="/api/v1/people", tags=["people-detection-legacy"])
    logger.info("Legacy people detection routes loaded (HTTP)")
except ImportError as e:
    logger.warning(f"Legacy people routes could not be loaded: {str(e)}")

try:
    from app.api.mobile_v1.models.security_api import router as security_router
    app.include_router(security_router, prefix="/api/v1/security_threats", tags=["security-detection-legacy"])
    logger.info("Legacy security threats detection routes loaded (HTTP)")
except ImportError as e:
    logger.warning(f"Legacy security routes could not be loaded: {str(e)}")

try:
    from app.api.mobile_v1.models.vehicle_api import router as vehicle_router
    app.include_router(vehicle_router, prefix="/api/v1/vehicle", tags=["vehicle-detection-legacy"])
    logger.info("Legacy vehicle detection routes loaded (HTTP)")
except ImportError as e:
    logger.warning(f"Legacy vehicle routes could not be loaded: {str(e)}")

logger.info("🚀 WebSocket Surveillance API server ready!")
logger.info("📡 Main WebSocket Endpoint: ws://localhost:8000/ws")
logger.info("�️  Image Check WebSocket: ws://localhost:8000/ws/check-image")
logger.info("🔄 Multi-Model HTTP API: http://localhost:8000/api/v1/check-image")
logger.info("�🔄 Legacy HTTP APIs available at: /api/v1/*")
logger.info("📊 WebSocket Stats: http://localhost:8000/ws/stats")

if __name__ == "__main__":
    logger.info("🚀 Starting WebSocket Surveillance API server on http://localhost:8000")
    logger.info("📡 WebSocket endpoint: ws://localhost:8000/ws")
    uvicorn.run(
        app,  # Use the app instance directly instead of string reference
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
