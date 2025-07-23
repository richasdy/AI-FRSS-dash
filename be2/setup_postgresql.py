#!/usr/bin/env python3
"""
Setup script untuk PostgreSQL database
"""
import asyncio
import os
import sys
from pathlib import Path

# Add app directory to Python path
sys.path.append(str(Path(__file__).parent / "app"))

from services.database_service import db_service
from models.database_models import User, DetectionLog, Camera, Alert, SystemConfig
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_database():
    """Create database tables"""
    try:
        logger.info("🗄️ Creating PostgreSQL database tables...")
        await db_service.create_tables()
        logger.info("✅ Database tables created successfully!")
    except Exception as e:
        logger.error(f"❌ Error creating database: {e}")
        raise

async def seed_initial_data():
    """Seed initial system configuration"""
    try:
        from services.database_service import get_db
        
        async for session in get_db():
            # Add default system configurations
            configs = [
                {
                    "config_key": "yolo_default_confidence",
                    "config_value": {"value": 0.5},
                    "description": "Default confidence threshold for YOLO detection"
                },
                {
                    "config_key": "alert_retention_days",
                    "config_value": {"value": 30},
                    "description": "Number of days to retain alerts"
                },
                {
                    "config_key": "max_concurrent_detections",
                    "config_value": {"value": 10},
                    "description": "Maximum concurrent detection processes"
                }
            ]
            
            for config_data in configs:
                config = SystemConfig(**config_data)
                session.add(config)
            
            await session.commit()
            logger.info("✅ Initial system configuration seeded!")
            
    except Exception as e:
        logger.error(f"❌ Error seeding data: {e}")
        raise

async def check_database():
    """Check database connection and tables"""
    try:
        logger.info("🔍 Checking PostgreSQL connection...")
        is_connected = await db_service.check_connection()
        
        if is_connected:
            logger.info("✅ PostgreSQL connection successful!")
            return True
        else:
            logger.error("❌ PostgreSQL connection failed!")
            return False
            
    except Exception as e:
        logger.error(f"❌ Database check error: {e}")
        return False

async def main():
    """Main setup function"""
    logger.info("🚀 Starting PostgreSQL setup for AI-FRSS...")
    
    # Check connection
    if not await check_database():
        logger.error("💥 Cannot proceed without database connection!")
        return False
    
    # Create tables
    await create_database()
    
    # Seed initial data
    await seed_initial_data()
    
    logger.info("🎉 PostgreSQL setup completed successfully!")
    await db_service.close()
    return True

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
