from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.exceptions import NotFoundException
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate


class ProductService:
    async def list_products(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> list[ProductResponse]:
        items = await crud.product.get_multi(db, skip=skip, limit=limit)
        return [ProductResponse.model_validate(p) for p in items]

    async def get_product(self, db: AsyncSession, product_id: int) -> ProductResponse:
        item = await crud.product.get(db, product_id)
        if item is None:
            raise NotFoundException("Product not found")
        return ProductResponse.model_validate(item)

    async def create_product(
        self, db: AsyncSession, product_in: ProductCreate
    ) -> ProductResponse:
        item = await crud.product.create(db, obj_in=product_in)
        return ProductResponse.model_validate(item)

    async def update_product(
        self, db: AsyncSession, product_id: int, product_in: ProductUpdate
    ) -> ProductResponse:
        item = await crud.product.get(db, product_id)
        if item is None:
            raise NotFoundException("Product not found")
        item = await crud.product.update(db, db_obj=item, obj_in=product_in)
        return ProductResponse.model_validate(item)

    async def delete_product(self, db: AsyncSession, product_id: int) -> None:
        item = await crud.product.remove(db, record_id=product_id)
        if item is None:
            raise NotFoundException("Product not found")
