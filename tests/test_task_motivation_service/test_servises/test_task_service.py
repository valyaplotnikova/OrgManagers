import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from task_motivation_service.task_app.models.task_model import StatusEnum
from task_motivation_service.task_app.services.task_service import TaskService
from task_motivation_service.task_app.schemas.task_schema import STaskCreate, STaskUpdate


@pytest.mark.asyncio
async def test_create_task(async_session: AsyncSession, mocked_authenticated_client):
    service = TaskService(session=async_session)
    task_data = STaskCreate(title="Test Task",
                            content="This is a test task.",
                            assigned_by=1,
                            assigned_to=2,
                            deadline="2025-10-31T17:00:00",
                            comment="Comment",
                            status="CREATED")

    await service.create_task(task_data)

    created_task = await service.get_task_by_id(7)
    assert created_task.title == task_data.title
    assert created_task.content == task_data.content

    with pytest.raises(HTTPException):
        await service.create_task(task_data)


@pytest.mark.asyncio
async def test_get_task_by_id(async_session: AsyncSession, mocked_authenticated_client):
    service = TaskService(session=async_session)
    task_data = STaskCreate(title="Test 2",
                            content="This is a test task.",
                            assigned_by=1,
                            assigned_to=2,
                            deadline="2025-10-31T17:00:00",
                            comment="Comment",
                            status="CREATED")
    await service.create_task(task_data)

    task = await service.get_task_by_id(8)
    assert task.title == task_data.title
    assert task.content == task_data.content

    with pytest.raises(HTTPException):
        await service.get_task_by_id(999)


@pytest.mark.asyncio
async def test_update_task(async_session: AsyncSession, mocked_authenticated_client):
    service = TaskService(session=async_session)
    task_data = STaskCreate(title="Test 3",
                            content="This is a test task.",
                            assigned_by=1,
                            assigned_to=2,
                            deadline="2025-10-31T17:00:00",
                            comment="Comment",
                            status="CREATED")
    await service.create_task(task_data)

    update_data = STaskUpdate(comment="Comment test", status="IN_WORK")
    await service.update_task(9, update_data)

    updated_task = await service.get_task_by_id(9)
    assert updated_task.comment == update_data.comment
    assert updated_task.status == StatusEnum.IN_WORK

    with pytest.raises(HTTPException):
        await service.update_task(999, update_data)


@pytest.mark.asyncio
async def test_delete_task(async_session: AsyncSession, mocked_authenticated_client):
    service = TaskService(session=async_session)
    task_data = STaskCreate(title="Test 4",
                            content="This is a test task.",
                            assigned_by=1,
                            assigned_to=2,
                            deadline="2025-10-31T17:00:00",
                            comment="Comment",
                            status="CREATED")
    await service.create_task(task_data)

    await service.delete_task(10)

    with pytest.raises(HTTPException):
        await service.get_task_by_id(10)


@pytest.mark.asyncio
async def test_get_all_tasks(async_session: AsyncSession, mocked_authenticated_client):
    service = TaskService(session=async_session)
    task1 = STaskCreate(title="Test 5",
                        content="This is a test task.",
                        assigned_by=1,
                        assigned_to=2,
                        deadline="2025-10-31T17:00:00",
                        comment="Comment",
                        status="CREATED")

    task2 = STaskCreate(title="Test 6",
                        content="This is a test task.",
                        assigned_by=1,
                        assigned_to=2,
                        deadline="2025-10-31T17:00:00",
                        comment="Comment",
                        status="CREATED")

    try:
        await service.create_task(task1)
        await service.create_task(task2)

        tasks = await service.get_all_tasks()
    except Exception as e:

        print(f"Произошла ошибка при создании задачи: {e}")
    assert len(tasks) == 2



