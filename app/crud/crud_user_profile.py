from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.user_profile import UserProfile
from app.schemas.user_profile import UserProfileCreate, UserProfileUpdate


class CRUDUserProfile(CRUDBase[UserProfile, UserProfileCreate, UserProfileUpdate]):
    async def get_by_user_id(self, db: AsyncSession, user_id: int) -> UserProfile | None:
        result = await db.execute(select(UserProfile).where(UserProfile.user_id == user_id))
        return result.scalar_one_or_none()


user_profile = CRUDUserProfile(UserProfile)
