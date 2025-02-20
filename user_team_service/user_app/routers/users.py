from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from user_team_service.user_app.services.task_service import TaskService
from user_team_service.user_app.dependencies.auth_dep import get_current_user, get_current_admin_user
from user_team_service.user_app.dependencies.repository_dep import get_session_with_commit, get_session_without_commit

from user_team_service.user_app.models.user_model import User
from user_team_service.user_app.schemas.auth_schemas import SUserInfo, UserUpdate
from user_team_service.user_app.services.user_service import UserService

router = APIRouter()


@router.get("/get/{user_id}")
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_session_without_commit),
    user_data: User = Depends(get_current_user)
) -> SUserInfo:
    """
    Получение информации о пользователе по его идентификатору.

    :param user_id: Идентификатор пользователя.
    :param session: Асинхронная сессия базы данных.
    :param user_data: Данные текущего администратора.
    :return: Информация о пользователе.
    """
    print(f"Received request for user_id: {user_id}, user_data: {user_data}")
    user_service = UserService(session)
    return await user_service.get_user_by_id(user_id)


@router.put("/update")
async def update_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_session_with_commit)
) -> dict:
    """
    Обновление данных текущего пользователя.

    :param user_data: Данные для обновления пользователя.
    :param current_user: Данные текущего пользователя.
    :param db_session: Асинхронная сессия базы данных.
    :return: Результат обновления пользователя.
    """
    user_service = UserService(db_session)
    return await user_service.update_user(current_user, user_data)


@router.delete("/delete/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db_session: AsyncSession = Depends(get_session_with_commit)
) -> dict:
    """
    Удаление пользователя по его идентификатору.

    :param user_id: Идентификатор пользователя для удаления.
    :param current_user: Данные текущего администратора.
    :param db_session: Асинхронная сессия базы данных.
    :return: Результат удаления пользователя.
    """
    user_service = UserService(db_session)
    return await user_service.delete_user(user_id)


@router.post("/update_status")
async def update_status_user(
    status: str,
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db_session: AsyncSession = Depends(get_session_with_commit)
) -> dict:
    """
    Обновление статуса пользователя.

    :param status: Новый статус пользователя.
    :param user_id: Идентификатор пользователя для обновления статуса.
    :param current_user: Данные текущего администратора.
    :param db_session: Асинхронная сессия базы данных.
    :return: Результат обновления статуса пользователя.
    """
    user_service = UserService(db_session)
    return await user_service.update_user_status(user_id, status)


@router.get("/my_tasks")
async def get_my_tasks(current_user: User = Depends(get_current_user),
                       session: AsyncSession = Depends(get_session_with_commit)
                       ):
    """
    Получение всех задач для пользователя с заданным ID.

    :param current_user: Данные текущего пользователя.
    :param session: Асинхронная сессия базы данных.
    :return: Список задач для указанного пользователя.
    """
    service = TaskService(session)
    tasks = await service.get_tasks_for_user(current_user)
    return tasks


@router.put("/update_my_task")
async def update_my_task(
    task_id: int,
    task_data: dict,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_with_commit)
):
    """
    Обновление задачи по идентификатору.

    :param task_id: Идентификатор задачи для обновления.
    :param task_data: Данные для обновления задачи в формате словаря.
    :param current_user: Текущий пользователь, полученный с помощью зависимости.
    :param session: Сессия базы данных, полученная с помощью зависимости.
    :return: Сообщение об успешном обновлении задачи.
    """
    service = TaskService(session)
    await service.update_my_task(task_id, task_data)
    return {'message': 'Задача успешно обновлена!'}


@router.put("/delete_my_task")
async def delete_my_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_with_commit)
):
    """
    Удаление задачи по идентификатору.

    :param task_id: Идентификатор задачи для удаления.
    :param current_user: Текущий пользователь, полученный с помощью зависимости.
    :param session: Сессия базы данных, полученная с помощью зависимости.
    :return: Сообщение об успешном удалении задачи.
    """
    service = TaskService(session)
    await service.delete_my_task(task_id)
    return {'message': 'Задача успешно удалена!'}


@router.get("/get_my_motivation")
async def get_my_motivation(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_with_commit)
):
    """
    Получение мотивации текущего пользователя.

    :param current_user: Текущий пользователь, полученный с помощью зависимости.
    :param session: Сессия базы данных, полученная с помощью зависимости.
    :return: Мотивация текущего пользователя.
    """
    service = TaskService(session)
    return await service.get_my_motivation(current_user)


@router.get("/get_my_quarterly_motivation")
async def get_my_quarterly_motivation(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_with_commit)
):
    """
    Получение квартальной мотивации текущего пользователя.

    :param current_user: Текущий пользователь, полученный с помощью зависимости.
    :param session: Сессия базы данных, полученная с помощью зависимости.
    :return: Квартальная мотивация текущего пользователя.
    """
    service = TaskService(session)
    return await service.get_my_quarterly_motivation(current_user)
