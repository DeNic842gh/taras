from contextlib import asynccontextmanager

import uvicorn
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import api_v1_router
from app.core.config import settings

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MARINE_SITE_DIR = PROJECT_ROOT / "marine-site"
STATIC_DIR = PROJECT_ROOT / "static"


@asynccontextmanager
async def lifespan(_: FastAPI):
    from app.db.session import engine

    yield
    await engine.dispose()


def create_app() -> FastAPI:
    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(api_v1_router, prefix=settings.api_v1_prefix)

    if MARINE_SITE_DIR.is_dir():
        application.mount(
            "/marine",
            StaticFiles(directory=str(MARINE_SITE_DIR), html=True),
            name="marine-site",
        )

    static_path = STATIC_DIR if STATIC_DIR.is_dir() else PROJECT_ROOT
    application.mount("/static", StaticFiles(directory=str(static_path)), name="static")

    @application.get("/", tags=["root"])
    async def root() -> dict[str, str]:
        return {
            "message": f"Welcome to {settings.app_name}",
            "marine_fan_site": "/marine/",
        }

    return application


app = create_app()


def run() -> None:
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
