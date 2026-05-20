from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int = Field(ge=1, default=1)
    unit_price: Decimal = Field(gt=0)


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemUpdate(BaseModel):
    quantity: int | None = Field(default=None, ge=1)
    unit_price: Decimal | None = Field(default=None, gt=0)


class OrderItemResponse(OrderItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
