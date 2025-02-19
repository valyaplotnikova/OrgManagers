import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from task_motivation_service.task_app.schemas.task_schema import STaskCreate
from task_motivation_service.task_app.services.task_service import TaskService
from task_motivation_service.task_app.services.motivation_service import MotivationService
from task_motivation_service.task_app.schemas.motivation_schema import SMotivationCreate, SMotivationUpdate


@pytest.mark.asyncio
async def test_create_motivation(async_session: AsyncSession, mocked_authenticated_client):
    task_service = TaskService(session=async_session)
    task_data = STaskCreate(title="Test Task",
                            content="This is a test task.",
                            assigned_by=1,
                            assigned_to=2,
                            deadline="2025-10-31T17:00:00",
                            comment="Comment",
                            status="CREATED")

    await task_service.create_task(task_data)
    service = MotivationService(session=async_session)
    motivation_data = SMotivationCreate(task_id=1, rating=5, comment="Well done!")

    await service.create_motivation(motivation_data)

    created_motivation = await service.get_motivation_by_taskid(1)
    assert created_motivation.task_id == motivation_data.task_id
    assert created_motivation.rating == motivation_data.rating

    with pytest.raises(HTTPException):
        await service.create_motivation(motivation_data)


@pytest.mark.asyncio
async def test_get_motivation_by_id(async_session: AsyncSession, mocked_authenticated_client):
    task_service = TaskService(session=async_session)
    task_data = STaskCreate(title="Test Task",
                            content="This is a test task.",
                            assigned_by=1,
                            assigned_to=2,
                            deadline="2025-10-31T17:00:00",
                            comment="Comment",
                            status="CREATED")

    await task_service.create_task(task_data)
    service = MotivationService(session=async_session)
    motivation_data = SMotivationCreate(task_id=2, rating=5, comment="Well done!")
    await service.create_motivation(motivation_data)

    motivation = await service.get_motivation_by_id(2)
    assert motivation.task_id == motivation_data.task_id
    assert motivation.rating == motivation_data.rating

    with pytest.raises(HTTPException):
        await service.get_motivation_by_id(999)


@pytest.mark.asyncio
async def test_update_motivation(async_session: AsyncSession, mocked_authenticated_client):
    task_service = TaskService(session=async_session)
    task_data = STaskCreate(title="Test Task",
                            content="This is a test task.",
                            assigned_by=1,
                            assigned_to=2,
                            deadline="2025-10-31T17:00:00",
                            comment="Comment",
                            status="CREATED")

    await task_service.create_task(task_data)
    service = MotivationService(session=async_session)
    motivation_data = SMotivationCreate(task_id=3, rating=5, comment="Well done!")
    await service.create_motivation(motivation_data)

    update_data = SMotivationUpdate(rating=3, comment="Not done!")
    await service.update_motivation(3, update_data)

    updated_motivation = await service.get_motivation_by_id(3)
    assert updated_motivation.rating == update_data.rating
    assert updated_motivation.comment == update_data.comment

    with pytest.raises(HTTPException):
        await service.update_motivation(999, update_data)


@pytest.mark.asyncio
async def test_delete_motivation(async_session: AsyncSession, mocked_authenticated_client):
    task_service = TaskService(session=async_session)
    task_data = STaskCreate(title="Test Task",
                            content="This is a test task.",
                            assigned_by=1,
                            assigned_to=2,
                            deadline="2025-10-31T17:00:00",
                            comment="Comment",
                            status="CREATED")

    await task_service.create_task(task_data)
    service = MotivationService(session=async_session)
    motivation_data = SMotivationCreate(task_id=4, rating=5, comment="Well done!")
    await service.create_motivation(motivation_data)

    await service.delete_motivation(4)

    with pytest.raises(HTTPException):
        await service.get_motivation_by_id(4)


@pytest.mark.asyncio
async def test_get_all_motivations(async_session: AsyncSession, mocked_authenticated_client):
    task_service = TaskService(session=async_session)
    service = MotivationService(session=async_session)
    task_data1 = STaskCreate(title="Test Task1",
                             content="This is a test task.",
                             assigned_by=1,
                             assigned_to=2,
                             deadline="2025-10-31T17:00:00",
                             comment="Comment",
                             status="CREATED")

    await task_service.create_task(task_data1)
    task_data2 = STaskCreate(title="Test Task2",
                             content="This is a test task.",
                             assigned_by=1,
                             assigned_to=2,
                             deadline="2025-10-31T17:00:00",
                             comment="Comment",
                             status="CREATED")

    await task_service.create_task(task_data2)

    motivation_data1 = SMotivationCreate(task_id=5, rating=5, comment="Well done!")
    motivation_data2 = SMotivationCreate(task_id=6, rating=4, comment="Done!")
    await service.create_motivation(motivation_data1)
    await service.create_motivation(motivation_data2)

    motivations = await service.get_all_motivations()
    assert len(motivations) == 2
