from fastapi.exceptions import HTTPException
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from user_team_service.user_app.dependencies.auth_dep import get_current_user, get_current_admin_user
from user_team_service.user_app.dependencies.repository_dep import get_session_with_commit, get_session_without_commit
from user_team_service.user_app.models import User
from user_team_service.user_app.schemas.news_schema import SNewsCreate, SNewsAll
from user_team_service.user_app.services.news_service import NewsService

router = APIRouter()


@router.post("/create")
async def create_news(
    news: SNewsCreate,
    user_data: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_session_with_commit)
):
    """
    Создание новой новости.

    :param news: Данные для создания новости.
    :param user_data: Данные текущего администратора.
    :param session: Асинхронная сессия базы данных.
    :return: Сообщение об успешном создании новости и идентификатор новости.
    """
    news_service = NewsService(session)
    new_news = await news_service.create_news(news, user_data.id)
    return {'message': 'Новость успешно создана!', 'news_id': new_news.news_id}


@router.delete("/delete/{news_id}")
async def delete_news(
    news_id: int,
    current_user: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_session_with_commit)
):
    """
    Удаление новости по идентификатору.

    :param news_id: Идентификатор новости для удаления.
    :param current_user: Данные текущего администратора.
    :param session: Асинхронная сессия базы данных.
    :return: Сообщение об успешном удалении новости.
    """
    news_service = NewsService(session)
    try:
        await news_service.delete_news(news_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {'message': 'Новость успешно удалена!'}


@router.get("/get/{news_id}")
async def get_one_news(
    news_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_without_commit)
) -> SNewsAll:
    """
    Получение одной новости по идентификатору.

    :param news_id: Идентификатор новости.
    :param current_user: Данные текущего пользователя.
    :param session: Асинхронная сессия базы данных.
    :return: Информация о новости.
    """
    news_service = NewsService(session)
    return await news_service.get_one_news(news_id)


@router.get("/get_all")
async def get_news(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_without_commit)
) -> List[SNewsAll]:
    """
    Получение всех новостей.

    :param current_user: Данные текущего пользователя.
    :param session: Асинхронная сессия базы данных.
    :return: Список всех новостей.
    """
    news_service = NewsService(session)
    return await news_service.get_all_news()
