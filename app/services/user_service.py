from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.exceptions import NotFoundException
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.schemas.user_profile import UserProfileCreate, UserProfileResponse, UserProfileUpdate


class UserService:
    async def list_users(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> list[UserResponse]:
        users = await crud.user.get_multi(db, skip=skip, limit=limit)
        return [UserResponse.model_validate(u) for u in users]

    async def get_user(self, db: AsyncSession, user_id: int) -> UserResponse:
        user = await crud.user.get(db, user_id)
        if user is None:
            raise NotFoundException("User not found")
        return UserResponse.model_validate(user)

    async def create_user(self, db: AsyncSession, user_in: UserCreate) -> UserResponse:
        user = await crud.user.create(db, obj_in=user_in)
        return UserResponse.model_validate(user)

    async def update_user(
        self, db: AsyncSession, user_id: int, user_in: UserUpdate
    ) -> UserResponse:
        user = await crud.user.get(db, user_id)
        if user is None:
            raise NotFoundException("User not found")
        user = await crud.user.update(db, db_obj=user, obj_in=user_in)
        return UserResponse.model_validate(user)

    async def delete_user(self, db: AsyncSession, user_id: int) -> None:
        user = await crud.user.remove(db, record_id=user_id)
        if user is None:
            raise NotFoundException("User not found")

    async def get_profile_by_user(
        self, db: AsyncSession, user_id: int
    ) -> UserProfileResponse:
        profile = await crud.user_profile.get_by_user_id(db, user_id)
        if profile is None:
            raise NotFoundException("Profile not found")
        return UserProfileResponse.model_validate(profile)

    async def create_profile(
        self, db: AsyncSession, profile_in: UserProfileCreate
    ) -> UserProfileResponse:
        profile = await crud.user_profile.create(db, obj_in=profile_in)
        return UserProfileResponse.model_validate(profile)

    async def update_profile(
        self, db: AsyncSession, profile_id: int, profile_in: UserProfileUpdate
    ) -> UserProfileResponse:
        profile = await crud.user_profile.get(db, profile_id)
        if profile is None:
            raise NotFoundException("Profile not found")
        profile = await crud.user_profile.update(db, db_obj=profile, obj_in=profile_in)
        return UserProfileResponse.model_validate(profile)
