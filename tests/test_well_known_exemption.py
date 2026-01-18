import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_well_known_path_bypasses_jwt_and_returns_404():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Unknown /.well-known path should not require auth and should 404
        r = await ac.get("/.well-known/appspecific/com.chrome.devtools.json")
        assert r.status_code == 404
