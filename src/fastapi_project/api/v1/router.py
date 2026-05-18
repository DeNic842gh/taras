from fastapi import APIRouter

from fastapi_project.api.v1.endpoints import health

api_v1_router = APIRouter()
api_v1_router.include_router(health.router, prefix="/health", tags=["health"])
