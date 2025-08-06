"""
FastAPI WebSocket-Based Surveillance API Server
Real-time video detection and monitoring system
"""
import sys
import os
import uuid
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from typing import Optional

# Setup Python path for proper imports
current_dir = os.path.dirname(os.path.abspath(__file__))
be2_dir = os.path.dirname(current_dir)
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
    
    yield
    
    # Cleanup
    try:
        await database_service.disconnect()
        logger.info("Database disconnected")
    except Exception as e:
        logger.warning(f"Database cleanup warning: {str(e)}")

# Create FastAPI application
app = FastAPI(
    title="AI-FRSS WebSocket Surveillance API",
    description="Real-time Face Recognition Surveillance System with WebSocket support",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
async def root():
    """API health check"""
    return {
        "message": "AI-FRSS WebSocket Surveillance API is running",
        "version": "2.0.0",
        "status": "healthy",
        "features": [
            "Real-time WebSocket communication",
            "YOLO object detection via WebSocket",
            "Multi-model detection support",
            "Face recognition (coming soon)",
            "Admin management (coming soon)",
            "Attendance tracking (coming soon)"
        ],
        "websocket_endpoints": {
            "main": "/ws/{client_id}",
            "surveillance": "/ws/surveillance/{client_id}",
            "admin": "/ws/admin/{client_id}",
            "attendance": "/ws/attendance/{client_id}"
        },
        "connection_stats": websocket_service.manager.get_stats(),
    }

# WebSocket connection handler
async def handle_websocket_connection(websocket: WebSocket, client_id: str, connection_type: str = "general"):
    """Generic WebSocket connection handler - Based on be3 pattern"""
    try:
        # Connect client
        await websocket_service.manager.connect(websocket, client_id, connection_type)
        
        # Handle messages (similar to be3 webSocketHandler)
        while True:
            try:
                message = await websocket.receive_text()
                logger.info(f"Received message from client {client_id}: {message}")
                await websocket_service.handle_message(client_id, message)
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

# WebSocket endpoints
@app.websocket("/ws/{client_id}")
async def websocket_main_endpoint(websocket: WebSocket, client_id: str):
    """Main WebSocket endpoint"""
    await handle_websocket_connection(websocket, client_id, "general")

@app.websocket("/ws/surveillance/{client_id}")
async def websocket_surveillance_endpoint(websocket: WebSocket, client_id: str):
    """Surveillance-specific WebSocket endpoint"""
    await handle_websocket_connection(websocket, client_id, "surveillance")

@app.websocket("/ws/admin/{client_id}")
async def websocket_admin_endpoint(websocket: WebSocket, client_id: str):
    """Admin-specific WebSocket endpoint"""
    await handle_websocket_connection(websocket, client_id, "admin")

@app.websocket("/ws/attendance/{client_id}")
async def websocket_attendance_endpoint(websocket: WebSocket, client_id: str):
    """Attendance-specific WebSocket endpoint"""
    await handle_websocket_connection(websocket, client_id, "attendance")

# Connection management endpoints
@app.get("/api/connections")
async def get_connection_stats():
    """Get WebSocket connection statistics"""
    return websocket_service.manager.get_stats()

@app.get("/api/connections/details")
async def get_detailed_connection_info():
    """Get detailed connection information"""
    stats = websocket_service.manager.get_stats()
    detailed_info = []
    
    for client_id in websocket_service.manager.active_connections.keys():
        conn_type = websocket_service.manager.connection_types.get(client_id, "unknown")
        detailed_info.append({
            "client_id": client_id,
            "connection_type": conn_type
        })
    
    return {
        "summary": stats,
        "detailed_connections": detailed_info
    }

@app.delete("/api/connections/{client_id}")
async def disconnect_client(client_id: str):
    """Manually disconnect a specific client"""
    if client_id in websocket_service.manager.active_connections:
        websocket_service.manager.disconnect(client_id)
        return {"message": f"Client {client_id} disconnected successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"Client {client_id} not found")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8080,
        reload=True,
        log_level="info"
    )
