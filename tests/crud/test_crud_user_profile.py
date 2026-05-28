import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from tests.helpers import profile_create_schema, user_create_schema


@pytest.mark.asyncio
async def test_user_profile_crud(db_session: AsyncSession) -> None:
    user = await crud.user.create(db_session, obj_in=user_create_schema())
    created = await crud.user_profile.create(
        db_session, obj_in=profile_create_schema(user_id=user.id)
    )
    assert created.user_id == user.id

    by_user = await crud.user_profile.get_by_user_id(db_session, user.id)
    assert by_user is not None
    assert by_user.id == created.id

    fetched = await crud.user_profile.get(db_session, created.id)
    assert fetched is not None

    from app.schemas.user_profile import UserProfileUpdate

    updated = await crud.user_profile.update(
        db_session,
        db_obj=created,
        obj_in=UserProfileUpdate(bio="New bio", country="US"),
    )
    assert updated.bio == "New bio"

    profiles = await crud.user_profile.get_multi(db_session)
    assert len(profiles) == 1

    removed = await crud.user_profile.remove(db_session, record_id=created.id)
    assert removed is not None
