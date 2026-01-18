"""Healthcheck route."""

from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health():
    """Return basic service liveness state."""
    return {"status": "ok"}
