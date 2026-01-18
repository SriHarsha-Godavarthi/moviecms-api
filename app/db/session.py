"""Async SQLAlchemy session and base configuration."""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import get_settings

settings = get_settings()

engine = create_async_engine(settings.database_url, future=True, echo=False)

class Base(DeclarativeBase):
    """Declarative base for ORM models."""
    pass

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db() -> AsyncSession:
    """FastAPI dependency yielding an AsyncSession."""
    async with async_session() as session:
        yield session
