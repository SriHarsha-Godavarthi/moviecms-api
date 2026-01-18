import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_signup_and_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        signup_payload = {
            "firstname": "John",
            "lastname": "Doe",
            "email": "john@example.com",
            "password": "secret123",
            "phonenumber": "1234567890",
            "isPremiumUser": False,
        }
        r = await ac.post("/auth/signup", json=signup_payload)
        assert r.status_code == 200
        user_id = r.json()["userid"]

        r = await ac.post("/auth/login", params={"email": "john@example.com", "password": "secret123"})
        assert r.status_code == 200
        token = r.json()["access_token"]
        assert token

        # Protected route should require token
        r = await ac.get(f"/users/{user_id}")
        assert r.status_code == 401

        r = await ac.get(f"/users/{user_id}", headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 200
