import warnings

import pytest
from httpx import AsyncClient
from user_team_service.user_app.schemas.auth_schemas import SUserAuth


@pytest.mark.asyncio
async def test_register_user_success(async_client: AsyncClient):

    user_data = {
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "Testov",
        "password": "password123",
        "confirm_password": "password123"
    }
    response = await async_client.post("/auth/register", json=user_data)

    assert response.status_code == 200
    assert response.json() == {'message': 'Вы успешно зарегистрированы!'}


@pytest.mark.asyncio
async def test_register_user_already_exists(async_client: AsyncClient):

    user_data = {
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "Testov",
        "password": "password123",
        "confirm_password": "password123"
    }
    await async_client.post("/auth/register", json=user_data)
    response = await async_client.post("/auth/register", json=user_data)
    assert response.status_code == 409
    assert response.json() == {'detail': 'Пользователь уже существует'}


@pytest.mark.asyncio
async def test_auth_user_success(async_client: AsyncClient):
    user_data = {
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "Testov",
        "password": "password123",
        "confirm_password": "password123"
    }
    await async_client.post("/auth/register", json=user_data)
    response = await async_client.post("/auth/login", json=SUserAuth(**user_data).model_dump())
    assert response.status_code == 200
    assert response.json() == {'token': True, 'message': 'Авторизация успешна!'}


@pytest.mark.asyncio
async def test_auth_user_incorrect_credentials(async_client: AsyncClient):
    user_data = {
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "Testov",
        "password": "password123",
        "confirm_password": "password123"
    }
    await async_client.post("/auth/register", json=user_data)

    wrong_data = SUserAuth(email="wrong@example.com", password="wrongpassword")
    response = await async_client.post("/auth/login", json=wrong_data.model_dump())

    assert response.status_code == 400
    assert response.json() == {'detail': 'Неверная почта или пароль'}


@pytest.mark.asyncio
async def test_logout_user(async_client: AsyncClient):
    user_data = {
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "Testov",
        "password": "password123",
        "confirm_password": "password123"
    }
    await async_client.post("/auth/register", json=user_data)
    await async_client.post("/auth/login", json=SUserAuth(**user_data).model_dump())
    response = await async_client.post("/auth/logout")

    assert response.status_code == 200
    assert response.json() == {'message': 'Пользователь успешно вышел из системы'}


@pytest.mark.asyncio
async def test_get_me(async_client: AsyncClient):
    user_data = {
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "Testov",
        "password": "password123",
        "confirm_password": "password123"
    }

    login_response = await async_client.post("/auth/login", json=SUserAuth(**user_data).model_dump())
    assert login_response.status_code == 200

    # Извлечение токена из cookies
    access_token = login_response.cookies.get("user_access_token")
    assert access_token is not None, "Access token not found in cookies"

    # Установка токена в клиенте
    async_client.cookies.set("user_access_token", access_token)

    response = await async_client.get("/auth/me")

    print("Response JSON:", response.json())
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_get_all_users(async_client: AsyncClient, create_admin_users):
    user_data = create_admin_users
    await async_client.post("/auth/register", json=user_data)
    login_response = await async_client.post("/auth/login", json=SUserAuth(**user_data).model_dump())
    assert login_response.status_code == 200

    access_token = login_response.cookies.get("user_access_token")
    assert access_token is not None, "Access token not found in cookies"

    async_client.cookies.set("user_access_token", access_token)

    response = await async_client.get("/auth/all_users")
    print((response.json()))

    assert response.status_code == 200
    assert isinstance(response.json(), list)
