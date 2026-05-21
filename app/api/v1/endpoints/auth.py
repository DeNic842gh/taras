from fastapi import APIRouter, Response, status

from app.api.auth_cookies import clear_access_token_cookie, set_access_token_cookie
from app.api.deps import CurrentUserDep, SessionDep
from app.schemas.auth import AuthResponse, AuthUser, LoginRequest, RegisterRequest
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService

router = APIRouter()
auth_service = AuthService()


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(
    data: RegisterRequest,
    db: SessionDep,
    response: Response,
) -> AuthResponse:
    """Register a new user. Returns JWT and sets an HttpOnly cookie."""
    result = await auth_service.register(db, data)
    set_access_token_cookie(response, result.access_token)
    return result


@router.post("/login", response_model=AuthResponse)
async def login(
    data: LoginRequest,
    db: SessionDep,
    response: Response,
) -> AuthResponse:
    """Authenticate by username and password. Returns JWT and sets an HttpOnly cookie."""
    result = await auth_service.login(db, data)
    set_access_token_cookie(response, result.access_token)
    return result


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response) -> None:
    """Clear the authentication cookie."""
    clear_access_token_cookie(response)


@router.get("/me", response_model=AuthUser)
async def auth_me(current_user: CurrentUserDep) -> AuthUser:
    """Current authenticated user (JWT header or cookie)."""
    return AuthUser(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
    )
