import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from tests.helpers import order_create_schema, user_create_schema


@pytest.mark.asyncio
async def test_order_crud(db_session: AsyncSession) -> None:
    from decimal import Decimal

    from app.schemas.order import OrderUpdate

    user = await crud.user.create(db_session, obj_in=user_create_schema())
    created = await crud.order.create(db_session, obj_in=order_create_schema(user_id=user.id))
    assert created.user_id == user.id

    fetched = await crud.order.get(db_session, created.id)
    assert fetched is not None

    updated = await crud.order.update(
        db_session,
        db_obj=created,
        obj_in=OrderUpdate(status="paid", total_amount=Decimal("50.00")),
    )
    assert updated.status == "paid"

    listed = await crud.order.get_multi(db_session)
    assert len(listed) == 1

    removed = await crud.order.remove(db_session, record_id=created.id)
    assert removed is not None
