import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi_pagination import add_pagination
from app.api.routers.routers import api_router
from app.core.settings import settings

from app.db.database import engine, Base
from app.models.user import User
from app.models.room import Room
from app.models.booking import Booking
from app.models.outbox import OutboxEvent


def _setup_logging() -> None:
    level = os.getenv("APP_LOG_LEVEL", "INFO").upper()
    fmt = os.getenv("APP_LOG_FORMAT", "%(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(fmt))

    app_logger = logging.getLogger("app.request")
    app_logger.setLevel(level)
    app_logger.handlers = [handler]
    app_logger.propagate = False


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Executa ao iniciar a API (Cria as tabelas de forma assíncrona)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield  # A aplicação roda aqui
    
    # Executa ao desligar a API (Fecha as conexões com o banco)
    await engine.dispose()


def create_app() -> FastAPI:
    _setup_logging()

    fast_api = FastAPI(
        title=f"{settings.SERVICE_NAME.capitalize()} API",
        description="Sistema de gerenciamento de reservas de salas e notificações.",
        version="1.0.0",
        docs_url=f"{settings.PREFIX}/docs" if not settings.PRODUCTION else None,
        openapi_url=f"{settings.PREFIX}/openapi.json" if not settings.PRODUCTION else None,
        swagger_ui_parameters={
            "persistAuthorization": True,
            "displayRequestDuration": True,
        },
        lifespan=lifespan, 
    )

    fast_api.openapi_schema = None

    def custom_openapi() -> dict:
        if fast_api.openapi_schema:
            return fast_api.openapi_schema

        openapi_schema = get_openapi(
            title=fast_api.title,
            version=fast_api.version,
            description=fast_api.description,
            routes=fast_api.routes,
        )

        # Adiciona esquema de segurança JWT no Swagger
        openapi_schema.setdefault("components", {})
        openapi_schema["components"]["securitySchemes"] = {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "Insira apenas o token JWT (sem Bearer)",
            },
        }

        for path in openapi_schema["paths"]:
            for method in openapi_schema["paths"][path]:
                if method.lower() != "options":
                    openapi_schema["paths"][path][method]["security"] = [
                        {"BearerAuth": []},
                    ]

        fast_api.openapi_schema = openapi_schema
        return fast_api.openapi_schema

    fast_api.openapi = custom_openapi


    fast_api.include_router(
        api_router,
        prefix=settings.PREFIX,
    )

    add_pagination(fast_api)

    return fast_api

# Instância que o Uvicorn vai procurar
app = create_app()