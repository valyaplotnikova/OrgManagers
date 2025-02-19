from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from task_motivation_service.task_app.dependencies.auth_dep import get_current_user_info
from task_motivation_service.task_app.dependencies.repository_dep import get_session_with_commit
from task_motivation_service.task_app.schemas.task_schema import STaskCreate, STaskUpdate
from task_motivation_service.task_app.services.task_service import TaskService
import logging

logging.basicConfig(level=logging.INFO)

router = APIRouter()


@router.post("/create")
async def create_task(
    task_data: STaskCreate,
    current_user: dict = Depends(get_current_user_info),
    session: AsyncSession = Depends(get_session_with_commit)
):

    """
    Создание новой Задачи.

    :param task_data: Данные для создания задачи.
    :param current_user: Данные текущего пользователя (полученные из первого сервиса).
    :param session: Асинхронная сессия базы данных.
    :return: Сообщение об успешном создании компании.
    """
    service = TaskService(session)
    task_data.assigned_by = int(current_user['id'])
    await service.create_task(task_data)
    return {'message': f'Задача {task_data.title} успешно создана!'}


@router.put("/update")
async def update_task(
        task_id: int,
        task_data: STaskUpdate,
        session: AsyncSession = Depends(get_session_with_commit)
):

    """
    Обновление Задачи.

    :param task_id: Идентификатор задачи.
    :param task_data: Данные для обновления задачи.
    :param session: Асинхронная сессия базы данных.
    :return: Сообщение об успешном обновлении задачи.
    """
    service = TaskService(session)
    await service.update_task(task_id, task_data)
    return {'message': f'Задача  успешно обновлена!'}


@router.delete("/delete/{task_id}")
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(get_session_with_commit)
):
    """
    Удаление задачи по идентификатору.

    :param task_id: Идентификатор задачи для удаления.
    :param session: Асинхронная сессия базы данных.
    :return: Сообщение об успешном удалении задачи.
    """
    service = TaskService(session)
    await service.delete_task(task_id)
    return {'message': 'Задача успешно удалена!'}


@router.get("/all")
async def get_all_tasks(

    session: AsyncSession = Depends(get_session_with_commit)
):
    """
    Получение списка всех задач.
    :param session: Асинхронная сессия базы данных.
    :return: Список всех задач.
    """
    logging.info("Получен запрос на получение всех задач.")
    service = TaskService(session)
    tasks = await service.get_all_tasks()
    return tasks


@router.get("/{task_id}")
async def get_task_by_id(
    task_id: int,
    session: AsyncSession = Depends(get_session_with_commit)
):
    """
    Получение задачи по идентификатору.

    :param task_id: Идентификатор задачи.
    :param session: Асинхронная сессия базы данных.
    :return: Данные задачи.
    """
    service = TaskService(session)
    task = await service.get_task_by_id(task_id)
    return task
