from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class OrderBase(BaseModel):
    user_id: int
    status: str = Field(default="pending", max_length=50)
    total_amount: Decimal = Field(default=Decimal("0.00"), ge=0)


class OrderCreate(BaseModel):
    user_id: int
    status: str = Field(default="pending", max_length=50)


class OrderUpdate(BaseModel):
    status: str | None = Field(default=None, max_length=50)
    total_amount: Decimal | None = Field(default=None, ge=0)


class OrderResponse(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
