from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
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

async def require_admin_user(request: Request, db: AsyncSession = Depends(get_db)) -> User:
    """Dependency that ensures the current user is an admin (premium).

    Uses `request.state.user_id` set by JWT middleware, loads the `User`, and checks
    `isPremiumUser`. Adjust this check if a dedicated admin flag is introduced later.
    """
    user_id = getattr(request.state, "user_id", None)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    result = await db.execute(select(User).where(User.userid == int(user_id)))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if not user.isPremiumUser:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return user

# OAuth2 bearer token dependency to make Swagger show the Authorize button.
# tokenUrl points to our login route; Swagger will let you paste the JWT.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
