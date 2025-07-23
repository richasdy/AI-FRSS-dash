from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData
import os
from typing import AsyncGenerator
import logging

logger = logging.getLogger(__name__)

# Database configuration from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://root:root123@localhost:5432/sv_fs"
)

# SQLAlchemy setup
engine = create_async_engine(
    DATABASE_URL,
    echo=os.getenv("DEBUG", "false").lower() == "true",  # Use DEBUG from .env
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600
)

# Session factory
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models
Base = declarative_base()

# Metadata for migrations
metadata = MetaData()

class DatabaseService:
    """Database service untuk PostgreSQL"""
    
    def __init__(self):
        self.engine = engine
        self.session_factory = async_session_factory
    
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session"""
        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    
    async def create_tables(self):
        """Create all tables"""
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("✅ Database tables created successfully")
    
    async def drop_tables(self):
        """Drop all tables (use with caution!)"""
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            logger.info("🗑️ Database tables dropped")
    
    async def check_connection(self) -> bool:
        """Check database connection"""
        try:
            async with engine.begin() as conn:
                await conn.execute("SELECT 1")
            logger.info("✅ Database connection successful")
            return True
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            return False
    
    async def close(self):
        """Close database connections"""
        await engine.dispose()
        logger.info("🔒 Database connections closed")

# Global database service instance
db_service = DatabaseService()

# Dependency untuk FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency untuk database session"""
    async for session in db_service.get_session():
        yield session
