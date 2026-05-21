from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.exceptions import NotFoundException
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate


class CategoryService:
    async def list_categories(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> list[CategoryResponse]:
        items = await crud.category.get_multi(db, skip=skip, limit=limit)
        return [CategoryResponse.model_validate(c) for c in items]

    async def get_category(self, db: AsyncSession, category_id: int) -> CategoryResponse:
        item = await crud.category.get(db, category_id)
        if item is None:
            raise NotFoundException("Category not found")
        return CategoryResponse.model_validate(item)

    async def create_category(
        self, db: AsyncSession, category_in: CategoryCreate
    ) -> CategoryResponse:
        item = await crud.category.create(db, obj_in=category_in)
        return CategoryResponse.model_validate(item)

    async def update_category(
        self, db: AsyncSession, category_id: int, category_in: CategoryUpdate
    ) -> CategoryResponse:
        item = await crud.category.get(db, category_id)
        if item is None:
            raise NotFoundException("Category not found")
        item = await crud.category.update(db, db_obj=item, obj_in=category_in)
        return CategoryResponse.model_validate(item)

    async def delete_category(self, db: AsyncSession, category_id: int) -> None:
        item = await crud.category.remove(db, record_id=category_id)
        if item is None:
            raise NotFoundException("Category not found")
