from fastapi import APIRouter

from app.core.config import settings
from app.db.session import check_database_connection
from app.schemas.health import HealthResponse

router = APIRouter()


@router.get("", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    db_ok = await check_database_connection()
    return HealthResponse(
        status="ok" if db_ok else "degraded",
        app_name=settings.app_name,
        environment=settings.app_env,
        database="connected" if db_ok else "disconnected",
    )
