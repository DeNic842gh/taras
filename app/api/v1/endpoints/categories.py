from fastapi import APIRouter, Response, status

from app import crud
from app.api.deps import SessionDep
from app.core.exceptions import NotFoundException
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate

router = APIRouter()


@router.get("", response_model=list[CategoryResponse])
async def list_categories(
    db: SessionDep, skip: int = 0, limit: int = 100
) -> list[CategoryResponse]:
    items = await crud.category.get_multi(db, skip=skip, limit=limit)
    return [CategoryResponse.model_validate(c) for c in items]


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, db: SessionDep) -> CategoryResponse:
    item = await crud.category.get(db, category_id)
    if item is None:
        raise NotFoundException("Category not found")
    return CategoryResponse.model_validate(item)


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(category_in: CategoryCreate, db: SessionDep) -> CategoryResponse:
    item = await crud.category.create(db, obj_in=category_in)
    return CategoryResponse.model_validate(item)


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int, category_in: CategoryUpdate, db: SessionDep
) -> CategoryResponse:
    item = await crud.category.get(db, category_id)
    if item is None:
        raise NotFoundException("Category not found")
    item = await crud.category.update(db, db_obj=item, obj_in=category_in)
    return CategoryResponse.model_validate(item)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, db: SessionDep) -> Response:
    item = await crud.category.remove(db, record_id=category_id)
    if item is None:
        raise NotFoundException("Category not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
