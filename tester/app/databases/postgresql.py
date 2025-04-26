import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.core.config import config

logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# Create engine
engine = create_async_engine(
    config.DATABASE_URL,
)

# Create session factory
SessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# Base class for app.models
class Base(AsyncAttrs, DeclarativeBase):
    pass


# Dependency function for FastAPI routes
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
