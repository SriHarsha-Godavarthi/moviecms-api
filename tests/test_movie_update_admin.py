import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_admin_can_update_movie(async_db_session=None):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Signup admin
        admin_payload = {
            "firstname": "Admin",
            "lastname": "User",
            "email": "admin@example.com",
            "password": "pass123",
            "phonenumber": "1234567890",
            "isPremiumUser": True,
        }
        r = await ac.post("/auth/signup", json=admin_payload)
        assert r.status_code == 200

        # Login admin
        r = await ac.post("/auth/login", params={"email": admin_payload["email"], "password": admin_payload["password"]})
        assert r.status_code == 200
        token = r.json()["access_token"]

        # Create a movie
        movie_payload = {
            "Name": "Initial Name",
            "Image": "img.jpg",
            "CDNImage": "cdnimg.jpg",
            "ReleaseDate": None,
            "ActorsList": "Actor A, Actor B",
            "language": "EN",
            "duration": 120,
            "CDN_VIDEO": "cdnvideo.mp4",
            "description": "desc",
            "createdby": "admin",
            "lastupdated": "2026-01-17",
            "lastupdatedby": "admin",
            "genre": "Action",
            "directedby": "Dir",
            "certificatetype": "PG-13",
            "published": False,
        }
        r = await ac.post("/movies/", json=movie_payload, headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 200
        movie = r.json()

        # Patch update: change name and publish
        update_payload = {"Name": "Updated Name", "published": True}
        r = await ac.patch(f"/movies/{movie['movieid']}", json=update_payload, headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 200
        updated = r.json()
        assert updated["Name"] == "Updated Name"
        assert updated["published"] is True

@pytest.mark.asyncio
async def test_non_admin_forbidden(async_db_session=None):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Signup normal user
        user_payload = {
            "firstname": "Normal",
            "lastname": "User",
            "email": "user@example.com",
            "password": "pass123",
            "phonenumber": "9876543210",
            "isPremiumUser": False,
        }
        r = await ac.post("/auth/signup", json=user_payload)
        assert r.status_code == 200

        # Login normal user
        r = await ac.post("/auth/login", params={"email": user_payload["email"], "password": user_payload["password"]})
        assert r.status_code == 200
        token = r.json()["access_token"]

        # Create a movie as normal user (allowed)
        movie_payload = {
            "Name": "Initial Name",
            "Image": "img.jpg",
            "CDNImage": "cdnimg.jpg",
            "ReleaseDate": None,
            "ActorsList": "Actor A, Actor B",
            "language": "EN",
            "duration": 120,
            "CDN_VIDEO": "cdnvideo.mp4",
            "description": "desc",
            "createdby": "user",
            "lastupdated": "2026-01-17",
            "lastupdatedby": "user",
            "genre": "Action",
            "directedby": "Dir",
            "certificatetype": "PG-13",
            "published": False,
        }
        r = await ac.post("/movies/", json=movie_payload, headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 200
        movie = r.json()

        # Attempt to publish as non-admin
        update_payload = {"published": True}
        r = await ac.patch(f"/movies/{movie['movieid']}", json=update_payload, headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 403
        assert r.json()["detail"] == "Admin privileges required"
