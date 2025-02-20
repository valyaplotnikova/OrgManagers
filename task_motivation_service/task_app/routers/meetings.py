from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from task_motivation_service.task_app.dependencies.repository_dep import (get_session_with_commit,
                                                                          get_session_without_commit)
from task_motivation_service.task_app.schemas.meeting_schema import SMeetingCreate, SMeetingUpdate
from task_motivation_service.task_app.schemas.meeting_schema import SParticipant
from task_motivation_service.task_app.services.meeting_service import MeetingService

router = APIRouter()


@router.post("/meetings/")
async def create_meeting(meeting: SMeetingCreate, session: AsyncSession = Depends(get_session_with_commit)):
    """
    Создает новую встречу.

    - **meeting**: Данные о встрече, включая название, описание, время начала и окончания.
    - **session**: Сессия базы данных, которая будет использоваться для выполнения операции.

    Возвращает созданную встречу.
    """
    service = MeetingService(session)
    return await service.create_meeting(meeting)


@router.put("/meetings/{meeting_id}")
async def update_meeting(
        meeting_id: int,
        meeting: SMeetingUpdate,
        session: AsyncSession = Depends(get_session_with_commit)
):
    """
    Обновляет существующую встречу по идентификатору.

    - **meeting_id**: Идентификатор встречи для обновления.
    - **meeting**: Обновленные данные о встрече.
    - **session**: Сессия базы данных, которая будет использоваться для выполнения операции.

    Возвращает обновленную встречу.
    """
    service = MeetingService(session)
    await service.update_meeting(meeting_id, meeting)
    return await service.get_meeting_by_id(meeting_id)


@router.delete("/meetings/{meeting_id}")
async def delete_meeting(meeting_id: int, session: AsyncSession = Depends(get_session_with_commit)):
    """
    Удаляет встречу по идентификатору.

    - **meeting_id**: Идентификатор встречи, которую нужно удалить.
    - **session**: Сессия базы данных, которая будет использоваться для выполнения операции.

    Возвращает сообщение об успешном удалении встречи.
    """
    service = MeetingService(session)
    await service.delete_meeting(meeting_id)
    return {"message": "Meeting deleted successfully."}


@router.get("/meetings/{meeting_id}")
async def get_meeting(meeting_id: int, session: AsyncSession = Depends(get_session_without_commit)):
    """
    Получает информацию о встрече по идентификатору.

    - **meeting_id**: Идентификатор встречи, которую нужно получить.
    - **session**: Сессия базы данных, которая будет использоваться для выполнения операции.

    Возвращает данные о встрече.
    """
    service = MeetingService(session)
    return await service.get_meeting_by_id(meeting_id)


@router.get("/meetings/")
async def get_all_meetings(session: AsyncSession = Depends(get_session_without_commit)):
    """
    Получает список всех встреч.

    - **session**: Сессия базы данных, которая будет использоваться для выполнения операции.

    Возвращает список всех встреч.
    """
    service = MeetingService(session)
    return await service.get_all_meetings()
