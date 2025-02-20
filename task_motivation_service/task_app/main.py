from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from .routers.tasks import router as router_task
from .routers.motivations import router as router_motivation
from .routers.meetings import router as router_meet


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[dict, None]:
    """Управление жизненным циклом приложения."""
    logger.info("Инициализация приложения...")
    yield
    logger.info("Завершение работы приложения...")


def create_app() -> FastAPI:
    """
   Создание и конфигурация FastAPI приложения.

   Returns:
       Сконфигурированное приложение FastAPI
   """
    app = FastAPI(
        title="Микросервис для работы с пользователями, командами, проектами и организационной структурой",
        lifespan=lifespan,
    )

    # Настройка CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    # Регистрация роутеров
    register_routers(app)

    return app


def register_routers(app: FastAPI) -> None:
    """Регистрация роутеров приложения."""
    # Корневой роутер
    root_router = APIRouter()

    @root_router.get("/", tags=["root"])
    def home_page():
        return {
            "message": "Добро пожаловать в систему управления и контроля бизнеса!",
        }

    # Подключение роутеров
    app.include_router(root_router, tags=["root"])
    app.include_router(router_task, prefix='/tasks', tags=['Task'])
    app.include_router(router_motivation, prefix='/motivations', tags=['Motivation'])
    app.include_router(router_meet, prefix='/meetings', tags=['Meeting'])


# Создание экземпляра приложения
app = create_app()
