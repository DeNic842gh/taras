import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from tests.helpers import category_create_schema


@pytest.mark.asyncio
async def test_category_crud(db_session: AsyncSession) -> None:
    from app.schemas.category import CategoryUpdate

    created = await crud.category.create(
        db_session, obj_in=category_create_schema(name="Music")
    )
    fetched = await crud.category.get(db_session, created.id)
    assert fetched is not None
    assert fetched.name == "Music"

    listed = await crud.category.get_multi(db_session)
    assert len(listed) == 1

    updated = await crud.category.update(
        db_session,
        db_obj=created,
        obj_in=CategoryUpdate(description="Updated desc"),
    )
    assert updated.description == "Updated desc"

    removed = await crud.category.remove(db_session, record_id=created.id)
    assert removed is not None
    assert await crud.category.get(db_session, created.id) is None
