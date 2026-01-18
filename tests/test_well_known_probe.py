import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_chrome_devtools_probe_returns_200():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/.well-known/appspecific/com.chrome.devtools.json")
        assert r.status_code == 200
        assert r.json() == {}
