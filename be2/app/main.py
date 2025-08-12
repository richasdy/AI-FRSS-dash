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

# Setup absolute Python path for proper imports
current_dir = os.path.dirname(os.path.abspath(__file__))
be2_dir = os.path.dirname(current_dir)  # e:\KP\AI-FRSS-dash\be2
project_root = os.path.dirname(be2_dir)  # e:\KP\AI-FRSS-dash

# Add be2 directory to Python path for app imports
if be2_dir not in sys.path:
    sys.path.insert(0, be2_dir)

# Import services with absolute path context
from app.services.database_service import database_service
from app.services.websocket_service import websocket_service
from app.services.models_service import yolo_service

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management with optimized startup"""
    logger.info("Starting Optimized WebSocket Surveillance API server...")
    logger.info(f"Working directory: {current_dir}")
    logger.info(f"BE2 directory: {be2_dir}")
    logger.info(f"Models path: {os.path.join(be2_dir, 'app', 'yolo_models')}")
    
    # Initialize database connection (optional)
    try:
        await database_service.connect()
        logger.info("✅ Database connected successfully")
    except Exception as e:
        logger.warning(f"⚠️ Database connection failed: {str(e)} - API will run without database")
    
    # Preload YOLO models for better performance
    try:
        logger.info("🔄 Preloading YOLO models...")
        await yolo_service.preload_all_models()
        service_stats = await yolo_service.get_service_stats()
        logger.info(f"✅ YOLO service initialized: {service_stats['service_info']}")
    except Exception as e:
        logger.warning(f"⚠️ YOLO service initialization warning: {str(e)}")
    
    # Server startup complete
    logger.info("🚀 Server startup complete - Ready for connections!")
    
    yield
    
    # Cleanup on shutdown
    try:
        await database_service.disconnect()
        logger.info("Database disconnected")
    except Exception as e:
        logger.warning(f"Database cleanup warning: {str(e)}")
    
    logger.info("Server shutdown complete")

# Create FastAPI application with optimized settings
app = FastAPI(
    title="AI-FRSS Optimized WebSocket Surveillance API",
    description="High-performance Real-time Face Recognition Surveillance System with optimized WebSocket and YOLO detection",
    version="2.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint with comprehensive info
@app.get("/")
async def root():
    """Enhanced API health check with system information"""
    try:
        yolo_stats = await yolo_service.get_service_stats()
        yolo_health = await yolo_service.health_check()
    except Exception as e:
        yolo_stats = {"error": str(e)}
        yolo_health = {"status": "error", "error": str(e)}
    
    return {
        "message": "AI-FRSS Optimized WebSocket Surveillance API is running",
        "version": "2.1.0",
        "status": "healthy",
        "server_info": {
            "current_dir": current_dir,
            "be2_dir": be2_dir,
            "python_path": sys.path[:3],  # First 3 paths for brevity
        },
        "features": [
            "Optimized real-time WebSocket communication",
            "GPU-accelerated YOLO object detection",
            "Multi-model parallel detection support",
            "Real-time alert broadcasting",
            "Performance monitoring & caching",
            "Connection management & health checks"
        ],
        "websocket_endpoints": {
            "main": "/ws/{client_id}",
            "surveillance": "/ws/surveillance/{client_id}",
            "admin": "/ws/admin/{client_id}",
            "attendance": "/ws/attendance/{client_id}"
        },
        "api_endpoints": {
            "health": "/",
            "connections": "/api/connections",
            "connection_details": "/api/connections/details",
            "system_health": "/api/health",
            "yolo_stats": "/api/yolo/stats"
        },
        "connection_stats": websocket_service.manager.get_stats(),
        "yolo_service": yolo_stats,
        "yolo_health": yolo_health
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

# Import WebSocket routers (MVC refined)
from app.api.v1 import auth_ws, users_ws, monitoring_ws, alerts_ws

# Import REST API routers
from app.api.v1 import auth_api, users_api, files_api, mobile_api

# Register WebSocket routers
app.include_router(auth_ws.router, prefix="/ws/auth", tags=["Auth WS"])
app.include_router(users_ws.router, prefix="/ws/users", tags=["Users WS"])
app.include_router(monitoring_ws.router, prefix="/ws/monitoring", tags=["Monitoring WS"])
app.include_router(alerts_ws.router, prefix="/ws/alerts", tags=["Alerts WS"])

# Register REST API routers
app.include_router(auth_api.router, tags=["Authentication REST"])
app.include_router(users_api.router, tags=["Users REST"])  
app.include_router(files_api.router, tags=["Files REST"])
app.include_router(mobile_api.router, tags=["Mobile REST"])

# Enhanced API endpoints for system monitoring
@app.get("/api/health")
async def get_system_health():
    """Comprehensive system health check"""
    try:
        websocket_stats = websocket_service.manager.get_stats()
        yolo_health = await yolo_service.health_check()
        yolo_stats = await yolo_service.get_service_stats()
        
        return {
            "status": "healthy",
            "timestamp": websocket_stats.get("timestamp", "unknown"),
            "services": {
                "websocket": {
                    "status": "healthy",
                    "active_connections": websocket_stats.get("active_connections", 0),
                    "peak_connections": websocket_stats.get("peak_connections", 0)
                },
                "yolo": yolo_health,
                "database": {
                    "status": "optional",
                    "available": database_service is not None
                }
            },
            "performance": yolo_stats.get("performance", {}),
            "uptime": websocket_stats.get("uptime_seconds", 0)
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": "unknown"
        }

@app.get("/api/yolo/stats")
async def get_yolo_statistics():
    """Get detailed YOLO service statistics"""
    try:
        return await yolo_service.get_service_stats()
    except Exception as e:
        return {"error": str(e)}

# Connection management endpoints
@app.get("/api/connections")
async def get_active_connections():
    """Get detailed information about all active WebSocket connections"""
    try:
        stats = websocket_service.manager.get_stats()
        return {
            "total_connections": stats["active_connections"],
            "peak_connections": stats["peak_connections"],
            "connection_details": stats.get("connections", []),
            "groups": stats.get("groups", {}),
            "message_stats": stats.get("messages", {})
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/connections/stats")
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
        await websocket_service.manager.disconnect(client_id)
        return {"message": f"Client {client_id} disconnected successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"Client {client_id} not found")

# Additional API endpoints for monitoring and testing
@app.get("/api/yolo/performance")
async def get_yolo_performance():
    """Get real-time YOLO performance metrics"""
    try:
        stats = await yolo_service.get_service_stats()
        return stats.get("performance", {})
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/system/info")
async def get_system_info():
    """Get comprehensive system information"""
    import platform
    try:
        import psutil
        import torch
        
        return {
            "system": {
                "platform": platform.platform(),
                "python_version": platform.python_version(),
                "architecture": platform.architecture(),
            },
            "hardware": {
                "cpu_count": psutil.cpu_count(),
                "memory_total": f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
                "memory_available": f"{psutil.virtual_memory().available / (1024**3):.2f} GB",
                "cpu_usage": f"{psutil.cpu_percent()}%"
            },
            "gpu": {
                "cuda_available": torch.cuda.is_available(),
                "cuda_version": torch.version.cuda if torch.cuda.is_available() else None,
                "gpu_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
                "gpu_names": [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())] if torch.cuda.is_available() else []
            },
            "services": {
                "websocket_service": "loaded",
                "yolo_service": "loaded",
                "database_service": "loaded" if database_service else "not configured"
            }
        }
    except ImportError as e:
        return {
            "error": f"Missing dependencies: {str(e)}",
            "system": {
                "platform": platform.platform(),
                "python_version": platform.python_version()
            }
        }
    except Exception as e:
        return {"error": str(e), "message": "Failed to gather system information"}

# Development and testing endpoints
@app.get("/api/test/websocket")
async def test_websocket_health():
    """Test WebSocket service health"""
    try:
        stats = websocket_service.manager.get_stats()
        return {
            "websocket_service": "healthy",
            "manager_initialized": websocket_service.manager is not None,
            "stats_available": bool(stats),
            "test_timestamp": stats.get("timestamp", "unknown")
        }
    except Exception as e:
        return {"error": str(e), "websocket_service": "unhealthy"}

@app.get("/api/test/yolo")
async def test_yolo_health():
    """Test YOLO service health with optional test detection"""
    try:
        health = await yolo_service.health_check()
        return {
            "yolo_service": "healthy" if health["status"] == "healthy" else "unhealthy",
            "health_details": health,
            "test_timestamp": health.get("timestamp", "unknown")
        }
    except Exception as e:
        return {"error": str(e), "yolo_service": "unhealthy"}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8080,
        reload=True,
        log_level="info"
    )
