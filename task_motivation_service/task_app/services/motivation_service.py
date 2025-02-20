from sqlalchemy.ext.asyncio import AsyncSession

from task_motivation_service.task_app.exceptions.task_meet_exceptions import (MotivationNotFoundException,
                                                                              MotivationAlreadyExistsException)
from task_motivation_service.task_app.repositories.task_repository import MotivationRepository
from task_motivation_service.task_app.schemas.motivation_schema import (SMotivationCreate, SMotivationSearch,
                                                                        SMotivationUpdate, SMotivationSearchID)


class MotivationService:
    def __init__(self, session: AsyncSession):
        """
        Инициализация Motivation Service.

        :param session: Асинхронная сессия базы данных.
        """
        self.session = session
        self.motivation_repo = MotivationRepository(session)

    async def create_motivation(self, motivation_data: SMotivationCreate):
        """
        Создание новой мотивации.

        :param motivation_data: Данные для создания мотивации.
        :raises MotivationAlreadyExistsException: Если мотивация для данной задачи уже существует.
        """
        existing_motivation = await self.motivation_repo.find_one_or_none(
            filters=SMotivationSearch(task_id=motivation_data.task_id)
        )
        if existing_motivation:
            raise MotivationAlreadyExistsException

        await self.motivation_repo.add(values=motivation_data)
        return {'message': 'Оценка успешно создана'}

    async def update_motivation(self, motivation_id: int, motivation_data: SMotivationUpdate):
        """
        Обновление данных мотивации по ее идентификатору.

        :param motivation_id: Идентификатор мотивации для обновления.
        :param motivation_data: Новые данные мотивации.
        :raises MotivationNotFoundException: Если мотивация не найдена или данные не обновлены.
        """
        rowcount = await self.motivation_repo.update(filters=SMotivationSearchID(id=motivation_id),
                                                     values=motivation_data)
        if rowcount == 0:
            raise MotivationNotFoundException

    async def delete_motivation(self, motivation_id: int):
        """
        Удаление мотивации по ее идентификатору.

        :param motivation_id: Идентификатор мотивации для удаления.
        :raises MotivationNotFoundException: Если мотивация не найдена или не удалена.
        """
        rowcount = await self.motivation_repo.delete(filters=SMotivationSearchID(id=motivation_id))
        if rowcount == 0:
            raise MotivationNotFoundException

    async def get_all_motivations(self):
        """
        Получение списка всех мотиваций.

        :return: Список всех мотиваций.
        """
        return await self.motivation_repo.find_all()

    async def get_motivation_by_id(self, motivation_id: int):
        """
        Получение мотивации по ее идентификатору.

        :param motivation_id: Идентификатор мотивации.
        :return: Данные мотивации.
        :raises MotivationNotFoundException: Если мотивация не найдена.
        """
        motivation = await self.motivation_repo.find_one_or_none_by_id(motivation_id)
        if not motivation:
            raise MotivationNotFoundException
        return motivation

    async def get_motivation_by_taskid(self, task_id: int):
        """
        Получение мотивации по ее идентификатору.

        :param task_id: Идентификатор задачи.
        :return: Данные мотивации.
        :raises MotivationNotFoundException: Если мотивация не найдена.
        """
        motivation = await self.motivation_repo.find_one_or_none(
            filters=SMotivationSearch(task_id=task_id)
        )
        if not motivation:
            raise MotivationNotFoundException
        return motivation
