from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate


class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):
    async def get_by_owner(
        self, db: AsyncSession, owner_id: int, *, skip: int = 0, limit: int = 100
    ) -> list[Post]:
        result = await db.execute(
            select(Post).where(Post.owner_id == owner_id).offset(skip).limit(limit)
        )
        return list(result.scalars().all())


post = CRUDPost(Post)
