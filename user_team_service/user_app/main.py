from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from sqladmin import Admin

from .admin import UserAdmin, CompanyAdmin, StructureAdmin, StructureMemberAdmin, NewsAdmin
from .database.database import engine
from .routers.auth import router as router_auth
from .routers.users import router as router_user
from .routers.companies import router as router_companies
from .routers.structures import router as router_structures
from .routers.news import router as router_news


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
    app.include_router(router_auth, prefix='/auth', tags=['Auth'])
    app.include_router(router_user, prefix='/users', tags=['Users'])
    app.include_router(router_companies, prefix='/companies', tags=['Companies'])
    app.include_router(router_structures, prefix='/structures', tags=['Structures'])
    app.include_router(router_news, prefix='/news', tags=['News'])


# Создание экземпляра приложения
app = create_app()
admin = Admin(app, engine, title="Admin Panel")
admin.add_view(UserAdmin)
admin.add_view(CompanyAdmin)
admin.add_view(StructureAdmin)
admin.add_view(StructureMemberAdmin)
admin.add_view(NewsAdmin)
