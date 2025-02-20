import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from user_team_service.user_app.schemas.news_schema import SNewsCreate

from user_team_service.user_app.services.news_service import NewsService


@pytest.mark.asyncio
async def test_create_news(async_session: AsyncSession, authenticated_client_admin):

    await authenticated_client_admin.post("/auth/register")
    service = NewsService(session=async_session)
    news_data = SNewsCreate(title="Test title",
                            content='Test content!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    await service.create_news(news_data, author_id=1)


async def test_get_one_news(async_session: AsyncSession, authenticated_client_admin):

    await authenticated_client_admin.post("/auth/register")
    service = NewsService(session=async_session)
    news_data = SNewsCreate(title="Test title",
                            content='Test content!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    await service.create_news(news_data, author_id=1)
    await service.get_one_news(2)


async def test_delete_news(async_session: AsyncSession, authenticated_client_admin):

    await authenticated_client_admin.post("/auth/register")
    service = NewsService(session=async_session)
    news_data = SNewsCreate(title="Test title",
                            content='Test content!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    await service.create_news(news_data, author_id=1)

    await service.delete_news(3)
    with pytest.raises(HTTPException):
        await service.get_one_news(3)


async def test_get_all_news(async_session: AsyncSession, authenticated_client_admin):

    await authenticated_client_admin.post("/auth/register")
    service = NewsService(session=async_session)
    news_data = SNewsCreate(title="Test title",
                            content='Test content!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    await service.create_news(news_data, author_id=1)
    news_data = SNewsCreate(title="Test title1",
                            content='Test content11111111111111111111111111111111111111111111111111111111111111111111')

    await service.create_news(news_data, author_id=1)

    response = await service.get_all_news()
    assert len(response) == 2
