"""Routes for creating and listing movie likes.

Detailed behavior:
- `POST /likes/` validates that both the user and movie exist, inserts an entry in the
  `moviesliked` table with a `CreatedAt` timestamp, then returns the created record.
- `GET /likes/user/{userid}` retrieves all likes associated with a user.

Notes:
- Use of async SQLAlchemy keeps DB I/O non-blocking.
- We return ORM entities transformed by FastAPI/Pydantic into response models.
"""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.like import LikeCreate, LikeRead
from app.db.session import get_db
from app.db.models.like import MoviesLiked
from app.db.models.movie import Movie
from app.db.models.user import User

router = APIRouter(prefix="/likes", tags=["likes"])

@router.post("/", response_model=LikeRead)
async def like_movie(payload: LikeCreate, db: AsyncSession = Depends(get_db)):
    """Create a like entry for a user/movie pair. Protected route.

    Steps breakdown:
    1) Validate foreign keys: Ensure `userid` and `movieid` refer to existing rows
    2) Construct entity: Populate `MoviesLiked` with `CreatedAt` timestamp in UTC
    3) Persist: Add and commit the new like, refresh to load PK (`Id`)
    4) Respond: Return the created like as a `LikeRead` model
    """
    # 1) Validate foreign keys: user must exist
    user_exists = (await db.execute(select(User).where(User.userid == payload.userid))).scalar_one_or_none()
    if not user_exists:
        raise HTTPException(status_code=404, detail="User not found")
    # 1) Validate foreign keys: movie must exist
    movie_exists = (await db.execute(select(Movie).where(Movie.movieid == payload.movieid))).scalar_one_or_none()
    if not movie_exists:
        raise HTTPException(status_code=404, detail="Movie not found")

    # 2) Construct entity: build the like record with a precise ISO 8601 timestamp
    like = MoviesLiked(
        userid=payload.userid,
        movieid=payload.movieid,
        CreatedAt=datetime.utcnow().isoformat(),
    )
    # 3) Persist: stage and commit; refresh loads generated fields (e.g., `Id`)
    db.add(like)
    await db.commit()
    await db.refresh(like)
    # 4) Respond: FastAPI + Pydantic handle schema serialization
    return like

@router.get("/user/{userid}")
async def list_user_likes(userid: int, db: AsyncSession = Depends(get_db)):
    """List all likes for the given `userid`. Protected route.

    Internals:
    - Executes a filtered SELECT on `moviesliked.userid`, returning a list of rows.
    - `.scalars().all()` extracts ORM instances from the result to form the response body.
    """
    result = await db.execute(select(MoviesLiked).where(MoviesLiked.userid == userid))
    return result.scalars().all()
