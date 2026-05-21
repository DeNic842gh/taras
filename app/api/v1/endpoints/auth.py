from fastapi import APIRouter, status

from app.api.deps import CurrentUserDep, SessionDep
from app.schemas.auth import AuthResponse, AuthUser, LoginRequest, RegisterRequest
from app.services.auth_service import AuthService

router = APIRouter()
auth_service = AuthService()


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest, db: SessionDep) -> AuthResponse:
    return await auth_service.register(db, data)


@router.post("/login", response_model=AuthResponse)
async def login(data: LoginRequest, db: SessionDep) -> AuthResponse:
    return await auth_service.login(db, data)


@router.get("/me", response_model=AuthUser)
async def me(current_user: CurrentUserDep) -> AuthUser:
    return current_user
