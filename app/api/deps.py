from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import UnauthorizedException
from app.core.security import ALGORITHM
from app.db.session import get_db
from app.schemas.auth import AuthUser
from app.services.auth_service import AuthService

security = HTTPBearer(auto_error=False)
auth_service = AuthService()

SessionDep = Annotated[AsyncSession, Depends(get_db)]
TokenDep = Annotated[HTTPAuthorizationCredentials | None, Depends(security)]


async def get_current_user(db: SessionDep, credentials: TokenDep) -> AuthUser:
    if credentials is None:
        raise UnauthorizedException("Not authenticated")
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.secret_key,
            algorithms=[ALGORITHM],
        )
        user_id = int(payload.get("sub", ""))
    except (JWTError, ValueError) as exc:
        raise UnauthorizedException("Invalid token") from exc
    return await auth_service.get_user_by_id(db, user_id)


CurrentUserDep = Annotated[AuthUser, Depends(get_current_user)]
