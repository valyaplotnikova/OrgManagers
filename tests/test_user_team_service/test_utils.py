import pytest
from datetime import datetime, timezone
from fastapi import Response
from jose import jwt

from user_team_service.user_app.auth import get_password_hash
from user_team_service.user_app.core.config import settings
from user_team_service.user_app.utils import create_tokens, authenticate_user, set_tokens, verify_password


@pytest.fixture
def response():
    return Response()


# Тест для функции create_tokens
def test_create_tokens():
    user_data = {"sub": "test_user_id"}
    tokens = create_tokens(user_data)

    assert "access_token" in tokens
    assert "refresh_token" in tokens

    # Проверяем, что токены содержат правильные данные
    access_payload = jwt.decode(tokens["access_token"], settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    refresh_payload = jwt.decode(tokens["refresh_token"], settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    assert access_payload["sub"] == user_data["sub"]
    assert refresh_payload["sub"] == user_data["sub"]

    current_timestamp = int(datetime.now(timezone.utc).timestamp())

    # Проверка, что время истечения токенов больше текущего времени
    assert access_payload["exp"] > current_timestamp
    assert refresh_payload["exp"] > current_timestamp


# Тест для функции authenticate_user
@pytest.mark.asyncio
async def test_authenticate_user():
    user = type('User ', (object,), {'password': get_password_hash("test_password")})()

    # Успешная аутентификация
    authenticated_user = await authenticate_user(user, "test_password")
    assert authenticated_user == user

    # Неуспешная аутентификация
    authenticated_user = await authenticate_user(user, "wrong_password")
    assert authenticated_user is None


# Тест для функции set_tokens
def test_set_tokens(response):
    user_id = 1

    # Вызываем функцию set_tokens
    set_tokens(response, user_id)

    # Проверяем, что заголовок 'set-cookie' установлен
    set_cookie_headers = response.headers.getlist("set-cookie")
    assert set_cookie_headers, "Set-Cookie header is not set"

    access_token = None
    refresh_token = None

    # Ищем куки в заголовках
    for cookie in set_cookie_headers:
        cookie_value = cookie  # Декодируем байтовую строку
        if "user_access_token" in cookie_value:
            access_token = cookie_value.split('=')[1].split(';')[0]  # Извлекаем значение токена
        elif "user_refresh_token" in cookie_value:
            refresh_token = cookie_value.split('=')[1].split(';')[0]  # Извлекаем значение токена

    assert access_token is not None, "Access token is not set in cookies"
    assert refresh_token is not None, "Refresh token is not set in cookies"

    # Декодируем токены для проверки их содержимого
    access_payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    refresh_payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    assert access_payload["sub"] == str(user_id)
    assert refresh_payload["sub"] == str(user_id)


# Тест для функции get_password_hash и verify_password
def test_password_hashing():
    password = "test_password"
    hashed_password = get_password_hash(password)

    assert verify_password(password, hashed_password) is True
    assert verify_password("wrong_password", hashed_password) is False
