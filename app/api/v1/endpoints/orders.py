from fastapi import APIRouter, Response, status

from app import crud
from app.api.deps import SessionDep
from app.core.exceptions import NotFoundException
from app.schemas.order import OrderCreate, OrderResponse, OrderUpdate

router = APIRouter()


@router.get("", response_model=list[OrderResponse])
async def list_orders(db: SessionDep, skip: int = 0, limit: int = 100) -> list[OrderResponse]:
    items = await crud.order.get_multi(db, skip=skip, limit=limit)
    return [OrderResponse.model_validate(o) for o in items]


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, db: SessionDep) -> OrderResponse:
    item = await crud.order.get(db, order_id)
    if item is None:
        raise NotFoundException("Order not found")
    return OrderResponse.model_validate(item)


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order_in: OrderCreate, db: SessionDep) -> OrderResponse:
    item = await crud.order.create(db, obj_in=order_in)
    return OrderResponse.model_validate(item)


@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(order_id: int, order_in: OrderUpdate, db: SessionDep) -> OrderResponse:
    item = await crud.order.get(db, order_id)
    if item is None:
        raise NotFoundException("Order not found")
    item = await crud.order.update(db, db_obj=item, obj_in=order_in)
    return OrderResponse.model_validate(item)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: int, db: SessionDep) -> Response:
    item = await crud.order.remove(db, record_id=order_id)
    if item is None:
        raise NotFoundException("Order not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
