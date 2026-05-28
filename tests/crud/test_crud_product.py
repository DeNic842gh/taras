import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.models.category import Category
from tests.helpers import product_create_schema


@pytest.mark.asyncio
async def test_product_crud(db_session: AsyncSession, sample_category: Category) -> None:
    from app.schemas.product import ProductUpdate

    created = await crud.product.create(
        db_session,
        obj_in=product_create_schema(category_id=sample_category.id, name="Coat"),
    )
    fetched = await crud.product.get(db_session, created.id)
    assert fetched is not None
    assert fetched.name == "Coat"

    updated = await crud.product.update(
        db_session,
        db_obj=created,
        obj_in=ProductUpdate(stock=5),
    )
    assert updated.stock == 5

    listed = await crud.product.get_multi(db_session)
    assert len(listed) == 1

    removed = await crud.product.remove(db_session, record_id=created.id)
    assert removed is not None
