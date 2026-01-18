from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.core.security import decode_claims
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
    """Ensure the current user is an admin via JWT claim.

    Checks the `Authorization: Bearer <token>` header for a `role` claim set to `admin`.
    Uses the token's `sub` to load and return the `User` entity.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = auth_header.split(" ", 1)[1].strip()

    claims = decode_claims(token)
    if not claims:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    if claims.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")

    sub = claims.get("sub")
    if not sub:
        raise HTTPException(status_code=401, detail="Not authenticated")

    result = await db.execute(select(User).where(User.userid == int(sub)))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# OAuth2 bearer token dependency to make Swagger show the Authorize button.
# tokenUrl points to our login route; Swagger will let you paste the JWT.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
