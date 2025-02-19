import pytest
from httpx import AsyncClient, Response
from unittest.mock import AsyncMock, patch

from sqlalchemy.ext.asyncio import AsyncSession

from user_team_service.user_app.services.task_service import TaskService
from user_team_service.user_app.models import User


@pytest.mark.asyncio
async def test_get_tasks_for_user(authenticated_client: AsyncClient, async_session: AsyncSession):
    user_service = TaskService(session=async_session)
    with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:

        mock_response = Response(200, json=[
            {"id": 1, "assigned_by": 1, "title": "Task 1"},
            {"id": 2, "assigned_by": 2, "title": "Task 2"},
        ])
        mock_response.request = mock_get.return_value.request
        mock_get.return_value = mock_response

        user = User(id=1)
        tasks = await user_service.get_tasks_for_user(user)

        assert len(tasks) == 1


@pytest.mark.asyncio
async def test_get_my_motivation(authenticated_client: AsyncClient, async_session: AsyncSession):
    user_service = TaskService(session=async_session)
    user = User(id=1)

    with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:

        mock_response_tasks = Response(200, json=[
            {"id": 1, "assigned_by": 1, "title": "Task 1"},
        ])
        mock_response_tasks.request = mock_get.return_value.request

        mock_response_rating = Response(200, json={"rating": 4})
        mock_response_rating.request = mock_get.return_value.request

        mock_get.side_effect = [mock_response_tasks, mock_response_rating]

        motivation = await user_service.get_my_motivation(user)

        assert "Task ID 1" in motivation
        assert motivation["Task ID 1"] == 4


@pytest.mark.asyncio
async def test_get_my_quarterly_motivation(authenticated_client: AsyncClient, async_session: AsyncSession):
    user_service = TaskService(session=async_session)
    user = User(id=1)

    with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:

        mock_response_tasks = Response(200, json=[
            {"id": 1, "assigned_by": 1, "title": "Task 1"},
            {"id": 2, "assigned_by": 1, "title": "Task 2"},
        ])
        mock_response_tasks.request = mock_get.return_value.request

        mock_response_rating_1 = Response(200, json={"rating": 4})
        mock_response_rating_1.request = mock_get.return_value.request

        mock_response_rating_2 = Response(200, json={"rating": 5})
        mock_response_rating_2.request = mock_get.return_value.request

        mock_get.side_effect = [mock_response_tasks, mock_response_rating_1, mock_response_rating_2]

        quarterly_motivation = await user_service.get_my_quarterly_motivation(user)

        assert "Средняя оценка" in quarterly_motivation
        assert quarterly_motivation["Средняя оценка"] == 4.5
