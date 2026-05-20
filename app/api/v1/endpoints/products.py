from fastapi import APIRouter, Response, status

from app import crud
from app.api.deps import SessionDep
from app.core.exceptions import NotFoundException
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter()


@router.get("", response_model=list[ProductResponse])
async def list_products(
    db: SessionDep, skip: int = 0, limit: int = 100
) -> list[ProductResponse]:
    items = await crud.product.get_multi(db, skip=skip, limit=limit)
    return [ProductResponse.model_validate(p) for p in items]


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: SessionDep) -> ProductResponse:
    item = await crud.product.get(db, product_id)
    if item is None:
        raise NotFoundException("Product not found")
    return ProductResponse.model_validate(item)


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product_in: ProductCreate, db: SessionDep) -> ProductResponse:
    item = await crud.product.create(db, obj_in=product_in)
    return ProductResponse.model_validate(item)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int, product_in: ProductUpdate, db: SessionDep
) -> ProductResponse:
    item = await crud.product.get(db, product_id)
    if item is None:
        raise NotFoundException("Product not found")
    item = await crud.product.update(db, db_obj=item, obj_in=product_in)
    return ProductResponse.model_validate(item)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: SessionDep) -> Response:
    item = await crud.product.remove(db, record_id=product_id)
    if item is None:
        raise NotFoundException("Product not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
