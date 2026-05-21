import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from tests.helpers import (
    category_create_schema,
    order_create_schema,
    order_item_create_schema,
    product_create_schema,
    user_create_schema,
)


@pytest.mark.asyncio
async def test_order_item_crud(db_session: AsyncSession) -> None:
    from app.schemas.order_item import OrderItemUpdate

    user = await crud.user.create(db_session, obj_in=user_create_schema())
    category = await crud.category.create(db_session, obj_in=category_create_schema())
    product = await crud.product.create(
        db_session,
        obj_in=product_create_schema(category_id=category.id),
    )
    order = await crud.order.create(db_session, obj_in=order_create_schema(user_id=user.id))

    created = await crud.order_item.create(
        db_session,
        obj_in=order_item_create_schema(order_id=order.id, product_id=product.id),
    )
    fetched = await crud.order_item.get(db_session, created.id)
    assert fetched is not None

    updated = await crud.order_item.update(
        db_session,
        db_obj=created,
        obj_in=OrderItemUpdate(quantity=3),
    )
    assert updated.quantity == 3

    listed = await crud.order_item.get_multi(db_session)
    assert len(listed) == 1

    removed = await crud.order_item.remove(db_session, record_id=created.id)
    assert removed is not None
