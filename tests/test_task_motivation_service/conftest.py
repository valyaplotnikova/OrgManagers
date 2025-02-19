import asyncio
import logging
import warnings
from typing import AsyncGenerator
from unittest.mock import AsyncMock

import pytest
from aiohttp.test_utils import TestClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncEngine

from httpx import AsyncClient, ASGITransport

from user_team_service.user_app.models import User
from user_team_service.user_app.repositories.auth_repository import UsersRepository
from user_team_service.user_app.schemas.auth_schemas import EmailModel, SUserAddDBTest, SUserAuth
from user_team_service.user_app.auth import get_password_hash
from task_motivation_service.task_app.main import app
from task_motivation_service.task_app.database.database import Base
from task_motivation_service.task_app.core.config import database_url
from task_motivation_service.task_app.models import Task, Motivation, Meeting


logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def async_engine() -> AsyncEngine:
    _async_engine = create_async_engine(
        url=database_url,
        echo=False,
        future=True,
        pool_size=50,
        max_overflow=100,
    )
    return _async_engine


@pytest.fixture(scope="session", autouse=True)
async def setup_db(async_engine):
    try:
        async with async_engine.begin() as conn:
            logger.info("Begin database setup")
            await conn.run_sync(Base.metadata.drop_all)
            logger.info("Dropped all tables")
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Created all tables")
    except Exception as e:
        logger.error(f"Error setting up the database: {e}")
        raise
    yield
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            logger.info("Dropped all tables after tests")
    except Exception as e:
        logger.error(f"Error tearing down the database: {e}")


@pytest.fixture(scope="session")
def async_session_maker(async_engine):
    _async_session_maker = async_sessionmaker(bind=async_engine,
                                              class_=AsyncSession,
                                              autoflush=False,
                                              autocommit=False,
                                              expire_on_commit=False,)
    return _async_session_maker


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    logger.info("Creating a new event loop")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    logger.info("Closing the event loop")
    loop.close()


@pytest.fixture(scope="function")
async def async_session(async_session_maker) -> AsyncSession:
    async with async_session_maker() as _async_session:
        yield _async_session


@pytest.fixture(scope="session")
def client() -> TestClient:
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost",
                           cookies={"user_access_token": "your_initial_token"}) as async_client:
        yield async_client


@pytest.fixture(scope="function")
def add_results(async_session_maker):
    async def _add_results(results):
        async with async_session_maker() as session:
            for res_schema in results:
                await session.execute(
                    insert(User).values(**res_schema.model_dump())
                )
            await session.commit()

    return _add_results


@pytest.fixture
async def create_admin_users(async_client: AsyncClient, async_session: AsyncSession):

    test_admin_data = {
        "email": "admin@admin.com",
        "first_name": "Admin",
        "last_name": "Adminov",
        "password": "adminpassword",
        "confirm_password": "adminpassword",
        "status": "ADMIN_GROUP"  # Укажите статус для администратора
    }
    admin_data = {
        "email": "admin@admin.com",
        "first_name": "Admin",
        "last_name": "Adminov",
        "password": "adminpassword",
        "confirm_password": "adminpassword",
        "status": "ADMIN_GROUP"  # Укажите статус для администратора
    }
    hashed_password = get_password_hash(test_admin_data["password"])
    test_admin_data["password"] = hashed_password
    existing_user = await UsersRepository(async_session).find_one_or_none(
        filters=EmailModel(email=test_admin_data["email"]))
    if not existing_user:
        await UsersRepository(async_session).add(values=SUserAddDBTest(**test_admin_data))
        await async_session.commit()

    yield admin_data


@pytest.fixture
async def mocked_authenticated_client(async_client):
    user_data = {
        "email": "user@mail.com",
        "first_name": "User ",
        "last_name": "User ",
        "password": "zxc123",
        "confirm_password": "zxc123"
    }

    # Мокирование ответа от первого сервиса
    async_client.post = AsyncMock(return_value=AsyncMock(status_code=201, cookies={"session_id": "mocked_cookie"}))

    # Регистрация пользователя
    registration_response = await async_client.post("/auth/register", json=user_data)
    assert registration_response.status_code == 201

    # Мокирование ответа на вход в систему
    async_client.post = AsyncMock(return_value=AsyncMock(status_code=200))

    # Вход в систему
    login_response = await async_client.post("/auth/login", json={"email": user_data["email"], "password": user_data["password"]})
    assert login_response.status_code == 200

    return async_client


@pytest.fixture
async def authenticated_client_admin(async_client: AsyncClient, create_admin_users):
    admin_data = create_admin_users
    await async_client.post("/auth/register", json=admin_data)
    login_response = await async_client.post("/auth/login", json=SUserAuth(**admin_data).model_dump())
    assert login_response.status_code == 200

    access_token = login_response.cookies.get("user_access_token")
    assert access_token is not None, "Access token not found in cookies"

    async_client.cookies.set("user_access_token", access_token)

    yield async_client


@pytest.fixture(scope="session", autouse=True)
def ignore_deprecation_warnings():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=DeprecationWarning)
        yield
