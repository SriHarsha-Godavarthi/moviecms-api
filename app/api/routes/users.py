"""User-related routes: retrieve and delete.

Both endpoints are protected by the JWT middleware and operate using async
SQLAlchemy queries to avoid blocking the event loop.
"""

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.user import UserRead
from app.db.session import get_db
from app.db.models.user import User
from app.deps import oauth2_scheme

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{userid}", response_model=UserRead)
async def get_user(
    userid: int,
    db: AsyncSession = Depends(get_db),
    Authorization: str = Header(str, alias="Authorization"),
):
    """Retrieve a user by `userid`. Protected route.

    Steps breakdown:
    1) Lookup by primary key: filter users on `userid`
    2) Error handling: raise 404 if user is absent
    3) Response: return ORM instance serialized via `UserRead`
    """
    result = await db.execute(select(User).where(User.userid == userid))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{userid}")
async def delete_user(
    userid: int,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """Delete a user by `userid`. Protected route.

    Steps breakdown:
    1) Lookup: retrieve user by id
    2) Error handling: return 404 if absent
    3) Delete & commit: remove record and persist transaction
    4) Response: confirmation payload
    """
    result = await db.execute(select(User).where(User.userid == userid))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
    return {"deleted": True}
