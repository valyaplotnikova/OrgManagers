from sqlalchemy.ext.asyncio import AsyncSession

from task_motivation_service.task_app.exceptions.task_meet_exceptions import (TaskAlreadyExistsException,
                                                                              TaskNotFoundException)
from task_motivation_service.task_app.repositories.task_repository import TaskRepository
from task_motivation_service.task_app.schemas.task_schema import STaskCreate, STaskSearch, STaskUpdate, STaskSearchID


class TaskService:
    def __init__(self, session: AsyncSession):
        """
        Инициализация CompanyUser Service.

        :param session: Асинхронная сессия базы данных.
        """
        self.session = session
        self.task_repo = TaskRepository(session)

    async def create_task(self, task_data: STaskCreate):
        """
        Создание новой задачи.

        :param task_data: Данные для создания задачи.
        :raises TaskAlreadyExistsException: Если задача с таким именем уже существует.
        """
        existing_task = await self.task_repo.find_one_or_none(filters=STaskSearch(title=task_data.title))
        if existing_task:
            raise TaskAlreadyExistsException

        await self.task_repo.add(values=task_data)
        return {"message": "Задача успешно создана"}

    async def update_task(self, task_id: int, task_data: STaskUpdate):
        """
        Обновление данных задачи по ее идентификатору.

        :param task_id: Идентификатор компании для обновления.
        :param task_data: Новые данные компании.
        :raises CompanyNotFoundException: Если компания не найдена или данные не обновлены.
        """
        rowcount = await self.task_repo.update(filters=STaskSearchID(id=task_id), values=task_data)
        if rowcount == 0:
            raise TaskNotFoundException

    async def delete_task(self, task_id: int):
        """
        Удаление задачи по ее идентификатору.

        :param task_id: Идентификатор задачи для удаления.
        :raises TaskNotFoundException: Если задача не найдена или не удалена.
        """
        rowcount = await self.task_repo.delete(filters=STaskSearchID(id=task_id))
        if rowcount == 0:
            raise TaskNotFoundException

    async def get_all_tasks(self):
        """
        Получение списка всех задач.

        :return: Список всех задач.
        """
        tasks = await self.task_repo.find_all()
        return tasks

    async def get_task_by_id(self, task_id: int):
        """
        Получение задачи по ее идентификатору.

        :param task_id: Идентификатор задачи.
        :return: Данные задачи.
        :raises TaskNotFoundException: Если задача не найдена.
        """
        task = await self.task_repo.find_one_or_none_by_id(task_id)
        if not task:
            raise TaskNotFoundException
        return task
