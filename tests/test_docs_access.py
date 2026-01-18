import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_docs_and_redoc_access():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Swagger UI
        r = await ac.get("/docs")
        assert r.status_code == 200
        # Redoc UI
        r = await ac.get("/redoc")
        assert r.status_code == 200
        # OpenAPI schema
        r = await ac.get("/openapi.json")
        assert r.status_code == 200
