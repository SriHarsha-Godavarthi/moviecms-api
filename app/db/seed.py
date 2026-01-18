import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import async_session
from app.db.models.movie import Movie

async def seed_movies():
    async with async_session() as db:  # type: AsyncSession
        exists = await db.execute(select(Movie).where(Movie.Name == "Seed Movie"))
        if exists.scalar_one_or_none():
            return
        movie = Movie(
            Name="Seed Movie",
            Image="seed.jpg",
            CDNImage="https://cdn/seed.jpg",
            ReleaseDate=None,
            ActorsList="Actor 1, Actor 2",
            language="English",
            duration=90,
            CDN_VIDEO="https://cdn/seed.mp4",
            description="Seed description",
            createdby="Seeder",
            lastupdated="",
            lastupdatedby="Seeder",
            genre="Drama",
            directedby="Director",
            certificatetype="PG",
        )
        db.add(movie)
        await db.commit()
        await db.refresh(movie)
        print("Seeded movie:", movie.movieid)

if __name__ == "__main__":
    asyncio.run(seed_movies())
