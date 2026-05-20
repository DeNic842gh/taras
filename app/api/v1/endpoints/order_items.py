from fastapi import APIRouter, Response, status

from app import crud
from app.api.deps import SessionDep
from app.core.exceptions import NotFoundException
from app.schemas.order_item import OrderItemCreate, OrderItemResponse, OrderItemUpdate

router = APIRouter()


@router.get("", response_model=list[OrderItemResponse])
async def list_order_items(
    db: SessionDep, skip: int = 0, limit: int = 100
) -> list[OrderItemResponse]:
    items = await crud.order_item.get_multi(db, skip=skip, limit=limit)
    return [OrderItemResponse.model_validate(i) for i in items]


@router.get("/{item_id}", response_model=OrderItemResponse)
async def get_order_item(item_id: int, db: SessionDep) -> OrderItemResponse:
    item = await crud.order_item.get(db, item_id)
    if item is None:
        raise NotFoundException("Order item not found")
    return OrderItemResponse.model_validate(item)


@router.post("", response_model=OrderItemResponse, status_code=status.HTTP_201_CREATED)
async def create_order_item(item_in: OrderItemCreate, db: SessionDep) -> OrderItemResponse:
    item = await crud.order_item.create(db, obj_in=item_in)
    return OrderItemResponse.model_validate(item)


@router.put("/{item_id}", response_model=OrderItemResponse)
async def update_order_item(
    item_id: int, item_in: OrderItemUpdate, db: SessionDep
) -> OrderItemResponse:
    item = await crud.order_item.get(db, item_id)
    if item is None:
        raise NotFoundException("Order item not found")
    item = await crud.order_item.update(db, db_obj=item, obj_in=item_in)
    return OrderItemResponse.model_validate(item)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order_item(item_id: int, db: SessionDep) -> Response:
    item = await crud.order_item.remove(db, record_id=item_id)
    if item is None:
        raise NotFoundException("Order item not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
