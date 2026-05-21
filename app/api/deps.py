from typing import Annotated

from fastapi import Cookie, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import UnauthorizedException
from app.core.security import ALGORITHM
from app.db.session import get_db
from app.models.user import User
from app.services.auth_service import AuthService

security = HTTPBearer(auto_error=False)
auth_service = AuthService()

SessionDep = Annotated[AsyncSession, Depends(get_db)]
TokenDep = Annotated[HTTPAuthorizationCredentials | None, Depends(security)]


async def get_access_token(
    credentials: TokenDep,
    access_token: Annotated[
        str | None,
        Cookie(alias=settings.access_token_cookie_name, include_in_schema=False),
    ] = None,
) -> str:
    if credentials is not None:
        return credentials.credentials
    if access_token:
        return access_token
    raise UnauthorizedException("Not authenticated")


async def get_current_user(
    db: SessionDep,
    token: Annotated[str, Depends(get_access_token)],
) -> User:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub", ""))
    except (JWTError, ValueError) as exc:
        raise UnauthorizedException("Invalid or expired token") from exc
    return await auth_service.get_active_user(db, user_id)


CurrentUserDep = Annotated[User, Depends(get_current_user)]
