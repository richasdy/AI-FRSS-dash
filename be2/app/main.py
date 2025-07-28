"""
FastAPI Mobile API Server
Clean mobile application backend
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from services.database_service import database_service

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
    from controller.auth_controller import router as auth_router
    app.include_router(auth_router, prefix="/mobile/v1/auth", tags=["authentication"])
    logger.info("Authentication routes loaded successfully")
except ImportError as e:
    logger.warning(f"Auth routes could not be loaded: {str(e)}")

# WebSocket routes disabled for now
logger.info("WebSocket routes disabled - service starting in basic mode")

if __name__ == "__main__":
    logger.info("Starting server on http://localhost:8000")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
