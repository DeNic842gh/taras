from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.exceptions import NotFoundException
from app.schemas.order import OrderCreate, OrderResponse, OrderUpdate
from app.schemas.order_item import OrderItemCreate, OrderItemResponse, OrderItemUpdate


class OrderService:
    async def list_orders(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> list[OrderResponse]:
        items = await crud.order.get_multi(db, skip=skip, limit=limit)
        return [OrderResponse.model_validate(o) for o in items]

    async def get_order(self, db: AsyncSession, order_id: int) -> OrderResponse:
        item = await crud.order.get(db, order_id)
        if item is None:
            raise NotFoundException("Order not found")
        return OrderResponse.model_validate(item)

    async def create_order(self, db: AsyncSession, order_in: OrderCreate) -> OrderResponse:
        item = await crud.order.create(db, obj_in=order_in)
        return OrderResponse.model_validate(item)

    async def update_order(
        self, db: AsyncSession, order_id: int, order_in: OrderUpdate
    ) -> OrderResponse:
        item = await crud.order.get(db, order_id)
        if item is None:
            raise NotFoundException("Order not found")
        item = await crud.order.update(db, db_obj=item, obj_in=order_in)
        return OrderResponse.model_validate(item)

    async def delete_order(self, db: AsyncSession, order_id: int) -> None:
        item = await crud.order.remove(db, record_id=order_id)
        if item is None:
            raise NotFoundException("Order not found")

    async def list_order_items(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> list[OrderItemResponse]:
        items = await crud.order_item.get_multi(db, skip=skip, limit=limit)
        return [OrderItemResponse.model_validate(i) for i in items]

    async def create_order_item(
        self, db: AsyncSession, item_in: OrderItemCreate
    ) -> OrderItemResponse:
        item = await crud.order_item.create(db, obj_in=item_in)
        return OrderItemResponse.model_validate(item)

    async def update_order_item(
        self, db: AsyncSession, item_id: int, item_in: OrderItemUpdate
    ) -> OrderItemResponse:
        item = await crud.order_item.get(db, item_id)
        if item is None:
            raise NotFoundException("Order item not found")
        item = await crud.order_item.update(db, db_obj=item, obj_in=item_in)
        return OrderItemResponse.model_validate(item)

    async def delete_order_item(self, db: AsyncSession, item_id: int) -> None:
        item = await crud.order_item.remove(db, record_id=item_id)
        if item is None:
            raise NotFoundException("Order item not found")
