from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from user_team_service.user_app.exceptions.exception import NewsNotFoundException
from user_team_service.user_app.repositories.teams_repository import NewsRepository
from user_team_service.user_app.schemas.news_schema import SNewsCreate, SNews, SNewsAll, SNewsFilter


class NewsService:
    def __init__(self, session: AsyncSession):
        """
        Инициализация сервиса новостей.

        :param session: Асинхронная сессия базы данных.
        """
        self.session = session
        self.repository = NewsRepository(session)

    async def create_news(self, news_data: SNewsCreate, author_id: int) -> SNews:
        """
        Создание новой новости.

        :param news_data: Данные для создания новости.
        :param author_id: Идентификатор автора новости.
        :return: Созданная новость.
        """
        news_data_dict = news_data.model_dump()
        news_data_dict['author_id'] = author_id
        new_news = SNews(**news_data_dict)
        await self.repository.add(values=new_news)
        return new_news

    async def delete_news(self, news_id: int):
        """
        Удаление новости по идентификатору.

        :param news_id: Идентификатор новости для удаления.
        """
        news = await self.repository.find_one_or_none_by_id(news_id)
        if not news:
            raise NewsNotFoundException
        await self.repository.delete(filters=SNewsFilter(id=news_id))

    async def get_one_news(self, news_id: int) -> SNewsAll:
        """
        Получение информации о новости по ее идентификатору.

        :param news_id: Идентификатор новости.
        :return: Информация о новости.
        """
        news = await self.repository.find_one_or_none_by_id(news_id)
        if not news:
            raise NewsNotFoundException
        return news

    async def get_all_news(self) -> List[SNewsAll]:
        """
        Получение списка всех новостей.

        :return: Список всех новостей.
        """
        return await self.repository.find_all()
