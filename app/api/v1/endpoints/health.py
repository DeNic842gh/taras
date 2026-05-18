from fastapi import APIRouter

from app.core.config import settings
from app.schemas.health import HealthResponse
from app.storage.user_memory import user_memory_store

router = APIRouter()


@router.get("", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    if settings.use_memory_store:
        return HealthResponse(
            status="ok",
            app_name=settings.app_name,
            environment=settings.app_env,
            database="memory",
        )

    from app.db.session import check_database_connection

    db_ok = await check_database_connection()
    return HealthResponse(
        status="ok" if db_ok else "degraded",
        app_name=settings.app_name,
        environment=settings.app_env,
        database="connected" if db_ok else "disconnected",
    )
