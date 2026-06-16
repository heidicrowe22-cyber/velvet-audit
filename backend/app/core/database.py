"""Database setup and session management."""
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine, text
import os

from app.core.config import settings


class Base(DeclarativeBase):
    pass


# Async engine for application use
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    connect_args={"check_same_thread": False},
)

AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncSession:
    """Dependency that provides a database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Create all tables using sync engine (async aiosqlite has issues with create_all)."""
    sync_url = settings.DATABASE_URL.replace("+aiosqlite", "")
    sync_engine = create_engine(sync_url, echo=settings.DEBUG)
    Base.metadata.create_all(sync_engine)
    sync_engine.dispose()


async def close_db():
    """Dispose of the engine connection pool."""
    await async_engine.dispose()