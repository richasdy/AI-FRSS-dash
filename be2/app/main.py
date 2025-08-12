"""
AI-FRSS Modular WebSocket Surveillance API v2.0
Simple and clean main entry point following be2v2.0 pattern
"""
import os
import sys
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

# Setup paths
current_dir = os.path.dirname(os.path.abspath(__file__))
be2_dir = os.path.dirname(current_dir)

if be2_dir not in sys.path:
    sys.path.insert(0, be2_dir)

# Import core components
from app.core.config import settings
from app.core.websocket_handler import handle_websocket_connection

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME, 
    version=settings.VERSION
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": f"{settings.PROJECT_NAME} is running",
        "version": settings.VERSION,
        "status": "healthy"
    }

# WebSocket endpoints
@app.websocket("/ws/{client_id}")
async def websocket_main_endpoint(websocket: WebSocket, client_id: str):
    await handle_websocket_connection(websocket, client_id, "general")

@app.websocket("/ws/surveillance/{client_id}")
async def websocket_surveillance_endpoint(websocket: WebSocket, client_id: str):
    await handle_websocket_connection(websocket, client_id, "surveillance")

@app.websocket("/ws/admin/{client_id}")
async def websocket_admin_endpoint(websocket: WebSocket, client_id: str):
    await handle_websocket_connection(websocket, client_id, "admin")

# Import and register routers
from app.api.v1 import auth_ws, users_ws, monitoring_ws, alerts_ws
from app.api.v1 import auth_api, users_api, files_api, mobile_api
from app.api.system import router as system_router

# WebSocket routers
app.include_router(auth_ws.router, prefix="/ws/auth", tags=["Auth WS"])
app.include_router(users_ws.router, prefix="/ws/users", tags=["Users WS"]) 
app.include_router(monitoring_ws.router, prefix="/ws/monitoring", tags=["Monitoring WS"])
app.include_router(alerts_ws.router, prefix="/ws/alerts", tags=["Alerts WS"])

# REST API routers
app.include_router(auth_api.router, tags=["Authentication REST"])
app.include_router(users_api.router, tags=["Users REST"])
app.include_router(files_api.router, tags=["Files REST"])
app.include_router(mobile_api.router, tags=["Mobile REST"])
app.include_router(system_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.RELOAD
    )
