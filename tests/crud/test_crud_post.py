import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from tests.helpers import post_create_schema, user_create_schema


@pytest.mark.asyncio
async def test_post_crud(db_session: AsyncSession) -> None:
    from app.schemas.post import PostUpdate

    user = await crud.user.create(db_session, obj_in=user_create_schema())
    created = await crud.post.create(
        db_session,
        obj_in=post_create_schema(title="Log"),
        owner_id=user.id,
    )
    assert created.owner_id == user.id

    fetched = await crud.post.get(db_session, created.id)
    assert fetched is not None

    updated = await crud.post.update(
        db_session,
        db_obj=created,
        obj_in=PostUpdate(title="Updated log"),
    )
    assert updated.title == "Updated log"

    listed = await crud.post.get_multi(db_session)
    assert len(listed) == 1

    removed = await crud.post.remove(db_session, record_id=created.id)
    assert removed is not None
