from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.exceptions import ConflictException, UnauthorizedException
from app.core.security import create_access_token, verify_password
from app.models.user import User
from app.schemas.auth import AuthResponse, AuthUser, LoginRequest, RegisterRequest
from app.schemas.user import UserCreate


class AuthService:
    @staticmethod
    def _to_auth_user(user: User) -> AuthUser:
        return AuthUser(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
        )

    def build_auth_response(self, user: User) -> AuthResponse:
        return AuthResponse(
            access_token=create_access_token(user.id),
            user=self._to_auth_user(user),
        )

    async def register(self, db: AsyncSession, data: RegisterRequest) -> AuthResponse:
        if await crud.user.get_by_email(db, str(data.email)):
            raise ConflictException("Email already registered")
        if await crud.user.get_by_username(db, data.username):
            raise ConflictException("Username already taken")

        user = await crud.user.create(
            db,
            obj_in=UserCreate(
                username=data.username,
                email=data.email,
                password=data.password,
                full_name=data.full_name or data.username,
                is_active=True,
            ),
        )
        return self.build_auth_response(user)

    async def login(self, db: AsyncSession, data: LoginRequest) -> AuthResponse:
        user = await crud.user.get_by_username(db, data.username)
        if user is None or not verify_password(data.password, user.hashed_password):
            raise UnauthorizedException("Invalid username or password")
        if not user.is_active:
            raise UnauthorizedException("Account is inactive")
        return self.build_auth_response(user)

    async def get_active_user(self, db: AsyncSession, user_id: int) -> User:
        user = await crud.user.get(db, user_id)
        if user is None or not user.is_active:
            raise UnauthorizedException("User not found or inactive")
        return user
