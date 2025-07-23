from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
import os
from contextlib import asynccontextmanager

# Load environment variables
from dotenv import load_dotenv
load_dotenv(dotenv_path="../.env")  # Load from be2/.env

# Import routers
from controller.detection_controller import router as detection_router
from controller.websocket_controller import router as websocket_router
from controller.auth_controller import router as auth_router
from controller.faces_controller import router as faces_router

# Import services untuk pre-loading
from services.yolo_service import yolo_manager
from services.database_service import db_service

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("🚀 Starting AI-FRSS YOLO Detection Service...")
    
    # Check database connection
    try:
        logger.info("Checking PostgreSQL connection...")
        db_connected = await db_service.check_connection()
        if db_connected:
            logger.info("✅ PostgreSQL connected successfully")
            # Create tables if they don't exist
            await db_service.create_tables()
        else:
            logger.error("❌ PostgreSQL connection failed")
    except Exception as e:
        logger.error(f"❌ Database initialization error: {e}")
    
    # Pre-load default models
    try:
        logger.info("Loading default YOLO models...")
        # Pre-load semua model untuk performa optimal
        models_to_load = ["intrusion", "people", "security_threats", "vehicle"]
        for model_name in models_to_load:
            try:
                yolo_manager.load_model(model_name)
                logger.info(f"✅ Model {model_name} loaded successfully")
            except Exception as e:
                logger.error(f"❌ Failed to load model {model_name}: {e}")
        
        loaded_count = len(yolo_manager.loaded_models)
        logger.info(f"✅ {loaded_count}/{len(models_to_load)} models loaded successfully")
    except Exception as e:
        logger.error(f"❌ Error loading default models: {e}")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down AI-FRSS service...")
    await db_service.close()

# Create FastAPI app with lifespan
app = FastAPI(
    title="AI-FRSS YOLO Detection API",
    description="API untuk deteksi objek menggunakan YOLO models pada sistem surveillance",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Health check endpoint"""
    return {
        "message": "🎥 AI-FRSS YOLO Detection Service is running!",
        "version": "2.0.0",
        "status": "active",
        "available_endpoints": {
            "docs": "/docs",
            "detection": "/detection",
            "websocket": "/ws",
            "health": "/health"
        }
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check"""
    try:
        # Check YOLO models
        available_models = yolo_manager.get_available_models()
        loaded_models = list(yolo_manager.loaded_models.keys())
        
        # Check database connection
        db_status = await db_service.check_connection()
        
        return {
            "status": "healthy" if db_status else "degraded",
            "timestamp": "2025-07-18",
            "database": {
                "status": "connected" if db_status else "disconnected",
                "type": "PostgreSQL"
            },
            "models": {
                "available": len(available_models),
                "loaded": len(loaded_models),
                "available_models": list(available_models.keys()),
                "loaded_models": loaded_models
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Service unhealthy: {str(e)}")

# Include routers
app.include_router(detection_router)
app.include_router(websocket_router)
app.include_router(auth_router)
app.include_router(faces_router)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )

# Run the application
if __name__ == "__main__":
    # Get configuration from environment
    PORT = int(os.getenv("PORT", "8000"))
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=PORT,
        reload=DEBUG,
        log_level="info"
    )