from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from task_motivation_service.task_app.dependencies.auth_dep import get_current_user_info
from task_motivation_service.task_app.dependencies.repository_dep import (get_session_with_commit,
                                                                          get_session_without_commit)
from task_motivation_service.task_app.schemas.motivation_schema import SMotivationCreate, SMotivationUpdate
from task_motivation_service.task_app.services.motivation_service import MotivationService

router = APIRouter()


@router.post("/create")
async def create_motivation(
    motivation_data: SMotivationCreate,
    session: AsyncSession = Depends(get_session_with_commit),
    current_user: dict = Depends(get_current_user_info),
):
    """
    Создает новую мотивацию для задачи.

    - **motivation_data**: Данные мотивации, которые необходимо создать.
    - **session**: Асинхронная сессия базы данных для выполнения операций.
    - **current_user**: Информация о текущем пользователе, создающем мотивацию.

    Возвращает созданную мотивацию.
    """
    service = MotivationService(session)
    motivation = await service.create_motivation(motivation_data)
    return motivation


@router.put("/update/{motivation_id}")
async def update_motivation(
    motivation_id: int,
    motivation_data: SMotivationUpdate,
    session: AsyncSession = Depends(get_session_with_commit),
):
    """
    Обновляет существующую мотивацию по идентификатору.

    - **motivation_id**: Идентификатор мотивации, которую необходимо обновить.
    - **motivation_data**: Данные для обновления мотивации.
    - **session**: Асинхронная сессия базы данных для выполнения операций.

    Возвращает обновленную мотивацию.
    """
    service = MotivationService(session)
    await service.update_motivation(motivation_id, motivation_data)
    return await service.get_motivation_by_id(motivation_id)


@router.delete("/delete/{motivation_id}")
async def delete_motivation(
    motivation_id: int,
    session: AsyncSession = Depends(get_session_with_commit),
):
    """
    Удаляет мотивацию по идентификатору.

    - **motivation_id**: Идентификатор мотивации, которую необходимо удалить.
    - **session**: Асинхронная сессия базы данных для выполнения операций.

    Возвращает сообщение об успешном удалении.
    """
    service = MotivationService(session)
    await service.delete_motivation(motivation_id)
    return {"detail": "Motivation deleted successfully."}


@router.get("/all")
async def get_all_motivations(
    session: AsyncSession = Depends(get_session_without_commit),
):
    """
    Получает список всех мотиваций.

    - **session**: Асинхронная сессия базы данных для выполнения операций.

    Возвращает список всех мотиваций.
    """
    service = MotivationService(session)
    motivations = await service.get_all_motivations()
    return motivations


@router.get("/{motivation_id}")
async def get_motivation(
    motivation_id: int,
    session: AsyncSession = Depends(get_session_with_commit),
):
    """
    Получает мотивацию по идентификатору.

    - **motivation_id**: Идентификатор мотивации, которую нужно получить.
    - **session**: Асинхронная сессия базы данных для выполнения операций.

    Возвращает мотивацию по указанному идентификатору.
    """
    service = MotivationService(session)
    motivation = await service.get_motivation_by_id(motivation_id)
    return motivation


@router.get("/get_by_taskid/{task_id}")
async def get_motivation(
    task_id: int,
    session: AsyncSession = Depends(get_session_with_commit),
):
    """
    Получает мотивацию по идентификатору.

    - **task_id**: Идентификатор мотивации, которую нужно получить.
    - **session**: Асинхронная сессия базы данных для выполнения операций.

    Возвращает мотивацию по указанному идентификатору.
    """
    service = MotivationService(session)
    motivation = await service.get_motivation_by_taskid(task_id)
    return motivation
