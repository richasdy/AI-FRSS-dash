import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# PostgreSQL async configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://root:root123@localhost:5432/sv_fs"
)

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=os.getenv("DEBUG", "false").lower() == "true",
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600
)

# Create session factory
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# For backward compatibility with existing code
database = engine  # Some legacy code might expect this
session_factory = async_session_factory

async def get_async_session():
    """Get async database session"""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Legacy function for compatibility (deprecated - use services.database_service instead)
def get_connection():
    """Deprecated: Use services.database_service.get_session() instead"""
    import warnings
    warnings.warn(
        "get_connection() is deprecated. Use services.database_service.get_session() instead",
        DeprecationWarning,
        stacklevel=2
    )
    return None
