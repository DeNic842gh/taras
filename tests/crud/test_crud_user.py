import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.password import verify_password
from tests.helpers import user_create_schema


@pytest.mark.asyncio
async def test_user_create_hashes_password(db_session: AsyncSession) -> None:
    user = await crud.user.create(
        db_session,
        obj_in=user_create_schema(username="hashuser", email="hash@example.com"),
    )
    assert user.hashed_password != "password99"
    assert verify_password("password99", user.hashed_password)


@pytest.mark.asyncio
async def test_user_get_and_get_multi(db_session: AsyncSession) -> None:
    created = await crud.user.create(db_session, obj_in=user_create_schema())
    fetched = await crud.user.get(db_session, created.id)
    assert fetched is not None
    assert fetched.email == created.email

    users = await crud.user.get_multi(db_session, skip=0, limit=10)
    assert len(users) == 1


@pytest.mark.asyncio
async def test_user_get_by_email_and_username(db_session: AsyncSession) -> None:
    created = await crud.user.create(
        db_session,
        obj_in=user_create_schema(username="findme", email="find@example.com"),
    )
    by_email = await crud.user.get_by_email(db_session, "find@example.com")
    by_username = await crud.user.get_by_username(db_session, "findme")
    assert by_email is not None and by_email.id == created.id
    assert by_username is not None and by_username.id == created.id


@pytest.mark.asyncio
async def test_user_update_and_remove(db_session: AsyncSession) -> None:
    from app.schemas.user import UserUpdate

    user = await crud.user.create(db_session, obj_in=user_create_schema())
    updated = await crud.user.update(
        db_session,
        db_obj=user,
        obj_in=UserUpdate(full_name="Updated", password="newpassword9"),
    )
    assert updated.full_name == "Updated"
    assert verify_password("newpassword9", updated.hashed_password)

    removed = await crud.user.remove(db_session, record_id=user.id)
    assert removed is not None
    assert await crud.user.get(db_session, user.id) is None
