from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    categories,
    health,
    order_items,
    orders,
    posts,
    products,
    profiles,
    users,
)

api_v1_router = APIRouter()
api_v1_router.include_router(health.router, prefix="/health", tags=["health"])
api_v1_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_v1_router.include_router(users.router, prefix="/users", tags=["users"])
api_v1_router.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
api_v1_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_v1_router.include_router(products.router, prefix="/products", tags=["products"])
api_v1_router.include_router(posts.router, prefix="/posts", tags=["posts"])
api_v1_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_v1_router.include_router(order_items.router, prefix="/order-items", tags=["order-items"])
