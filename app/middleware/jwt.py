"""JWT authentication middleware.

Functionality:
- Exempts `/auth/login`, `/auth/signup`, and `/health` from authentication.
- For all other routes, expects an `Authorization: Bearer <token>` header.
- Decodes the JWT and attaches `request.state.user_id` for downstream dependencies.

Failure modes:
- Missing or malformed `Authorization` header → 401
- Invalid or expired JWT → 401 with structured error response
"""

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

from app.core.security import decode_token

EXCLUDED_PATHS = {"/auth/login", "/auth/signup", "/health"}

async def jwt_middleware(request: Request, call_next):
    """Authenticate requests via JWT, skipping exempted paths."""
    # Exemptions: healthcheck and auth routes should be publicly accessible
    if request.url.path in EXCLUDED_PATHS:
        return await call_next(request)

    # Header parsing: expect a Bearer token in Authorization
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = auth_header.split(" ", 1)[1]

    # Decode: extract subject (user id) from JWT; handle invalid tokens
    user_id = decode_token(token)
    if not user_id:
        return JSONResponse(status_code=401, content={"detail": "Invalid or expired token"})

    # Context propagation: attach `user_id` to request state for downstream usage
    request.state.user_id = int(user_id)
    return await call_next(request)
