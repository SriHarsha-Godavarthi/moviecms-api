"""Movie routes: create, read, and delete.

These endpoints operate on the `movies` table, adhering to the field names
specified in the README (e.g., `Name`, `CDNImage`, `ReleaseDate`).
"""

from fastapi import APIRouter, Depends, HTTPException,  Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.movie import MovieCreate, MovieRead, MovieUpdate
from app.db.session import get_db
from app.db.models.movie import Movie
from app.deps import require_admin_user, oauth2_scheme

router = APIRouter(prefix="/movies", tags=["movies"])

@router.post("/", response_model=MovieRead)
async def create_movie(
    payload: MovieCreate,
    db: AsyncSession = Depends(get_db),
    Authorization: str = Header(str, alias="Authorization"),
):
    """Create a new movie record. Protected route.

    Steps breakdown:
    1) Build entity: construct `Movie` from the validated payload
    2) Persist: add to session, commit transaction, refresh to load PK
    3) Respond: return created movie in the `MovieRead` schema
    """
    movie = Movie(**payload.model_dump())
    db.add(movie)
    await db.commit()
    await db.refresh(movie)
    return movie

@router.get("/{movieid}", response_model=MovieRead)
async def get_movie(movieid: int, db: AsyncSession = Depends(get_db)):
    """Retrieve a movie by `movieid`.

    Internals:
    - Executes a filtered SELECT on `movies.movieid` and returns the row or 404.
    - FastAPI + Pydantic converts the ORM instance to the `MovieRead` response.
    """
    result = await db.execute(select(Movie).where(Movie.movieid == movieid))
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.delete("/{movieid}")
async def delete_movie(
    movieid: int,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """Delete a movie by `movieid`. Protected route.

    Steps breakdown:
    1) Lookup: find the movie by id
    2) Error handling: 404 if absent
    3) Delete & commit: remove the record and confirm persistence
    4) Response: deletion confirmation object
    """
    result = await db.execute(select(Movie).where(Movie.movieid == movieid))
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    await db.delete(movie)
    await db.commit()
    return {"deleted": True}

@router.patch("/{movieid}", response_model=MovieRead)
async def update_movie(
    movieid: int,
    payload: MovieUpdate,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
    admin_user=Depends(require_admin_user),
):
    """Partially update a movie (admin-only).

    Steps:
    1) Load the target movie or 404
    2) For each provided field in `MovieUpdate`, set the attribute on the entity
    3) Commit and refresh
    4) Return the updated movie in `MovieRead`
    """
    result = await db.execute(select(Movie).where(Movie.movieid == movieid))
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(movie, field, value)

    await db.commit()
    await db.refresh(movie)
    return movie
