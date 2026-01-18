import pytest
from httpx import AsyncClient
from app.main import app
from datetime import date

@pytest.mark.asyncio
async def test_movie_create_and_like():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Create user and login
        payload = {
            "firstname": "Alice",
            "lastname": "Smith",
            "email": "alice@example.com",
            "password": "secret123",
            "phonenumber": "9876543210",
            "isPremiumUser": True,
        }
        r = await ac.post("/auth/signup", json=payload)
        user_id = r.json()["userid"]
        r = await ac.post("/auth/login", params={"email": "alice@example.com", "password": "secret123"})
        token = r.json()["access_token"]

        movie_payload = {
            "Name": "Sample Movie",
            "Image": "img.jpg",
            "CDNImage": "https://cdn/img.jpg",
            "ReleaseDate": date.today().isoformat(),
            "ActorsList": "Actor A, Actor B",
            "language": "English",
            "duration": 120,
            "CDN_VIDEO": "https://cdn/video.mp4",
            "description": "Desc",
            "createdby": "Alice",
            "lastupdated": "today",
            "lastupdatedby": "Alice",
            "genre": "Action",
            "directedby": "Director",
            "certificatetype": "PG-13",
        }
        r = await ac.post("/movies/", json=movie_payload, headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 200
        movie_id = r.json()["movieid"]

        like_payload = {"userid": user_id, "movieid": movie_id}
        r = await ac.post("/likes/", json=like_payload, headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 200
        assert r.json()["userid"] == user_id

        r = await ac.get(f"/likes/user/{user_id}", headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 200
        assert len(r.json()) >= 1
