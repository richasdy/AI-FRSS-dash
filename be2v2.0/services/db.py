import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# Path absolut ke sv-fs.sqlite di root project
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sqlite_path = os.path.join(project_root, "sv-fs.sqlite")
DATABASE_URL = f"sqlite+aiosqlite:///{sqlite_path}"

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
