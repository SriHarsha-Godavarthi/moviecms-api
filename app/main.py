"""Application entrypoint for MovieFlix CMS API.

Initializes FastAPI, registers middlewares and routes, and ensures
database tables exist on startup (for local/dev). Production setups
should use Alembic migrations instead of auto-creation.
"""

import asyncio
import logging

from fastapi import FastAPI

from app.middleware.jwt import jwt_middleware
from app.middleware.logging import logging_middleware
from app.api.routes.health import router as health_router
from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router
from app.api.routes.movies import router as movies_router
from app.api.routes.likes import router as likes_router
from app.db.session import Base, engine

app = FastAPI(title="MovieFlix CMS API")

# Order matters: log first, then JWT auth (exemptions within middleware)
app.middleware("http")(logging_middleware)
app.middleware("http")(jwt_middleware)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(movies_router)
app.include_router(likes_router)

@app.on_event("startup")
async def on_startup():
    """Create DB schema for dev/local runs."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

