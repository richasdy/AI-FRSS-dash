"""
FastAPI Mobile API Server
Clean mobile application backend
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from app.services.database_service import database_service

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("Starting Mobile API server...")
    
    # Try to initialize database connection (optional)
    try:
        await database_service.connect()
        logger.info("Database connected successfully")
    except Exception as e:
        logger.warning(f"Database connection failed: {str(e)} - API will run without database")
    
    yield
    
    # Cleanup
    logger.info("Shutting down Mobile API server...")
    try:
        await database_service.disconnect()
    except Exception:
        pass

# Create FastAPI application
app = FastAPI(
    title="Mobile API",
    description="Clean mobile application backend",
    version="1.0.0",
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
    return {"status": "healthy", "service": "mobile-api"}

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Mobile API Server", "version": "1.0.0"}

# Import and include routers
try:
    from app.controller.auth_controller import router as auth_router
    app.include_router(auth_router, prefix="/mobile/v1/auth", tags=["authentication"])
    logger.info("Authentication routes loaded successfully")
except ImportError as e:
    logger.warning(f"Auth routes could not be loaded: {str(e)}")

# Import YOLO Model APIs
try:
    from app.api.mobile_v1.models.intrusion_api import router as intrusion_router
    app.include_router(intrusion_router, prefix="/mobile/v1/intrusion", tags=["intrusion-detection"])
    logger.info("Intrusion detection routes loaded successfully")
except ImportError as e:
    logger.warning(f"Intrusion routes could not be loaded: {str(e)}")

try:
    from app.api.mobile_v1.models.people_api import router as people_router
    app.include_router(people_router, prefix="/mobile/v1/people", tags=["people-detection"])
    logger.info("People detection routes loaded successfully")
except ImportError as e:
    logger.warning(f"People routes could not be loaded: {str(e)}")

try:
    from app.api.mobile_v1.models.security_api import router as security_router
    app.include_router(security_router, prefix="/mobile/v1/security_threats", tags=["security-detection"])
    logger.info("Security threats detection routes loaded successfully")
except ImportError as e:
    logger.warning(f"Security routes could not be loaded: {str(e)}")

try:
    from app.api.mobile_v1.models.vehicle_api import router as vehicle_router
    app.include_router(vehicle_router, prefix="/mobile/v1/vehicle", tags=["vehicle-detection"])
    logger.info("Vehicle detection routes loaded successfully")
except ImportError as e:
    logger.warning(f"Vehicle routes could not be loaded: {str(e)}")

# Video Processing APIs
try:
    from app.api.mobile_v1.features.video_upload_api import router as video_upload_router
    app.include_router(video_upload_router, prefix="/mobile/v1/video", tags=["video-processing"])
    logger.info("Video upload routes loaded successfully")
except ImportError as e:
    logger.warning(f"Video upload routes could not be loaded: {str(e)}")

try:
    from app.api.mobile_v1.features.realtime_api import router as realtime_router
    app.include_router(realtime_router, prefix="/mobile/v1/realtime", tags=["realtime-detection"])
    logger.info("Real-time detection routes loaded successfully")
except ImportError as e:
    logger.warning(f"Real-time routes could not be loaded: {str(e)}")

try:
    from app.api.mobile_v1.features.cctv_api import router as cctv_router
    app.include_router(cctv_router, prefix="/mobile/v1/cctv", tags=["cctv-monitoring"])
    logger.info("CCTV monitoring routes loaded successfully")
except ImportError as e:
    logger.warning(f"CCTV routes could not be loaded: {str(e)}")

logger.info("All API routes loaded - server ready with complete video detection capabilities")

if __name__ == "__main__":
    logger.info("Starting server on http://localhost:8000")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
