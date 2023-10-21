from fastapi import FastAPI

from app.core.config import settings
from app.domain.enums import AppEnvEnum
from app.resources.example import router as example_router


def get_app():
    app = FastAPI(
        title=settings.app_name,
        redoc_url=None,
        docs_url="/-/docs" if settings.app_env == AppEnvEnum.dev.value else None,
    )
    app.include_router(example_router, prefix="/examples", tags=["examples"])

    return app
