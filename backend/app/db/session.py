from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

eengine_kwargs = {}

if not settings.SQLALCHEMY_DATABASE_URI.startswith("sqlite"):
    engine_kwargs = {
        "pool_size": 10,
        "max_overflow": 20,
        "pool_timeout": 30,
    }

engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=False,
    future=True,
    **engine_kwargs
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
