"""
Database Service
Handles database connections and session management
"""
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class DatabaseService:
    """Database service for async SQLAlchemy operations"""
    
    def __init__(self):
        self.engine = None
        self.session_factory = None
        self._initialize_engine()
    
    def _initialize_engine(self):
        """Initialize the database engine"""
        database_url = os.getenv(
            "DATABASE_URL", 
            "postgresql+asyncpg://root:root123@localhost:5432/sv_fs"
        )
        
        self.engine = create_async_engine(
            database_url,
            echo=os.getenv("DEBUG", "false").lower() == "true",
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            pool_recycle=3600
        )
        
        self.session_factory = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
    
    async def connect(self):
        """Test database connection"""
        try:
            async with self.engine.begin() as conn:
                await conn.execute("SELECT 1")
            logger.info("Database connection established")
        except Exception as e:
            logger.error(f"Database connection failed: {str(e)}")
            raise
    
    async def disconnect(self):
        """Close database connection"""
        if self.engine:
            await self.engine.dispose()
            logger.info("Database connection closed")
    
    async def get_session(self):
        """Get async database session"""
        if not self.session_factory:
            raise RuntimeError("Database not initialized")
        
        async with self.session_factory() as session:
            try:
                yield session
            except SQLAlchemyError:
                await session.rollback()
                raise
            finally:
                await session.close()
    
    async def execute_query(self, query: str, values: dict = None):
        """Execute raw SQL query"""
        async with self.engine.begin() as conn:
            if values:
                result = await conn.execute(query, values)
            else:
                result = await conn.execute(query)
            return result
    
    async def fetch_all(self, query: str, values: dict = None):
        """Execute query and fetch all results"""
        result = await self.execute_query(query, values)
        return [dict(row._mapping) for row in result.fetchall()]
    
    async def fetch_one(self, query: str, values: dict = None):
        """Execute query and fetch one result"""
        result = await self.execute_query(query, values)
        row = result.fetchone()
        return dict(row._mapping) if row else None

# Create global database service instance
database_service = DatabaseService()
