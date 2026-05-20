from app.crud.base import CRUDBase
from app.models.order_item import OrderItem
from app.schemas.order_item import OrderItemCreate, OrderItemUpdate


class CRUDOrderItem(CRUDBase[OrderItem, OrderItemCreate, OrderItemUpdate]):
    pass


order_item = CRUDOrderItem(OrderItem)
