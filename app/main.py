"""Application entrypoint for MovieFlix CMS API.

Initializes FastAPI, registers middlewares and routes, and ensures
database tables exist on startup (for local/dev). Production setups
should use Alembic migrations instead of auto-creation.
"""

import asyncio
import logging

from fastapi import FastAPI
from fastapi.openapi.docs import get_redoc_html

from app.middleware.jwt import jwt_middleware
from app.middleware.logging import logging_middleware
from app.api.routes.health import router as health_router
from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router
from app.api.routes.movies import router as movies_router
from app.api.routes.likes import router as likes_router
from app.api.routes.well_known import router as well_known_router
from app.db.session import Base, engine

app = FastAPI(
    title="MovieFlix CMS API",
    docs_url="/docs",
    redoc_url=None,  # disable built-in Redoc so we can pin JS URL
    openapi_url="/openapi.json",
)

# Order matters: log first, then JWT auth (exemptions within middleware)
app.middleware("http")(logging_middleware)
app.middleware("http")(jwt_middleware)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(movies_router)
app.include_router(likes_router)
app.include_router(well_known_router)

# Custom Redoc that pins a working CDN URL (avoids jsdelivr @next 404s)
@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - ReDoc",
        redoc_js_url="https://unpkg.com/redoc@2.1.2/bundles/redoc.standalone.js",
    )

@app.on_event("startup")
async def on_startup():
    """Create DB schema for dev/local runs."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # Ensure `published` column exists on `movies` for SQLite dev DBs
        def ensure_published_column(sync_conn):
            try:
                rows = sync_conn.execute("PRAGMA table_info('movies')").fetchall()
                cols = {row[1] for row in rows}
                if "published" not in cols:
                    # SQLite uses INTEGER for booleans; default 0 (False)
                    sync_conn.execute(
                        "ALTER TABLE movies ADD COLUMN published INTEGER NOT NULL DEFAULT 0"
                    )
            except Exception as exc:
                logging.getLogger(__name__).warning(
                    "Skipping published column migration: %s", exc
                )

        await conn.run_sync(ensure_published_column)

