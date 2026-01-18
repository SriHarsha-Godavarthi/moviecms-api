from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.db.models.user import User

async def get_current_user_id(user_id: int | None) -> int:
    if user_id is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user_id

async def get_user_by_email(email: str, db: AsyncSession) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)) -> User | None:
    result = await db.execute(select(User).where(User.userid == user_id))
    return result.scalar_one_or_none()
