import httpx
from task_motivation_service.task_app.dependencies.repository_dep import get_session_without_commit
from task_motivation_service.task_app.exceptions.task_meet_exceptions import ForbiddenException


from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from datetime import datetime, timezone
from task_motivation_service.task_app.core.config import settings
from task_motivation_service.task_app.exceptions.task_meet_exceptions import (TokenNoFound, NoJwtException,
                                                                              TokenExpiredException)


AUTH_SERVICE_URL = "http://127.0.0.1:8000"


def get_access_token(request: Request) -> str:
    """Извлекаем access_token из кук."""
    token = request.cookies.get('user_access_token')
    if not token:
        print("No access token found in cookies")
        raise TokenNoFound
    return token


def get_refresh_token(request: Request) -> str:
    """Извлекаем refresh_token из кук."""
    token = request.cookies.get('user_refresh_token')
    if not token:
        raise TokenNoFound
    return token


async def check_refresh_token(
        token: str = Depends(get_refresh_token),
        session: AsyncSession = Depends(get_session_without_commit)
) -> dict:
    """Проверяем refresh_token и возвращаем минимальную информацию о пользователе."""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload  # Возвращаем полезную нагрузку токена
    except jwt.JWTError:
        raise NoJwtException


async def get_current_user_info(
        token: str = Depends(get_access_token)
) -> dict:
    """Проверяем access_token и возвращаем минимальную информацию о пользователе."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise TokenExpiredException
    except jwt.JWTError:
        raise NoJwtException

    expire: str = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise TokenExpiredException

    user_id = payload.get('sub')

    return {"id": user_id}
