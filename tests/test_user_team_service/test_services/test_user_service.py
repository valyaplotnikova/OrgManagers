import pytest
from fastapi import HTTPException

from user_team_service.user_app.models.user_model import StatusEnum
from user_team_service.user_app.schemas.auth_schemas import UserUpdate, SUserAddDBTest, UserBase
from user_team_service.user_app.services.user_service import UserService


@pytest.mark.asyncio
async def test_get_user_by_id(async_session, add_results):

    user_data = dict(email="testuser@example.com",
                     first_name="Test",
                     last_name="User",
                     password="password",
                     status="USER")
    await add_results([SUserAddDBTest(**user_data)])

    user_service = UserService(session=async_session)
    response = await user_service.users_repo.find_all()
    user_info = await user_service.get_user_by_id(9)

    assert user_info.email == user_data["email"]
    assert user_info.first_name == user_data["first_name"]


@pytest.mark.asyncio
async def test_update_user(async_session, authenticated_client):

    await authenticated_client.post("/auth/register")

    user_service = UserService(session=async_session)
    updated_data = UserUpdate(email="newemail@example.com", first_name="NewName")

    response = await user_service.update_user(current_user=await user_service.get_user_by_id(1), user_data=updated_data)

    assert response["message"] == "Данные успешно обновлены!"
    updated_user = await user_service.get_user_by_id(1)
    assert updated_user.email == updated_data.email
    assert updated_user.first_name == updated_data.first_name


@pytest.mark.asyncio
async def test_delete_user(async_session, authenticated_client_admin):

    await authenticated_client_admin.post("/auth/register")

    user_service = UserService(session=async_session)

    response = await user_service.delete_user(user_id=1)

    assert response["message"] == "Данные успешно удалены!"

    answer = await user_service.get_user_by_id(1)
    assert answer is None


@pytest.mark.asyncio
async def test_update_user_status(async_session, authenticated_client_admin):

    await authenticated_client_admin.post("/auth/register")

    user_service = UserService(session=async_session)

    response = await user_service.update_user_status(user_id=4, status="ADMIN_GROUP")

    assert response["message"] == "Статус пользователя test@mail.com успешно обновлен!"
    updated_user = await user_service.get_user_by_id(4)
    assert updated_user.status == StatusEnum.ADMIN_GROUP


@pytest.mark.asyncio
async def test_update_user_email_already_exists(async_session, create_admin_users, authenticated_client_admin):

    await authenticated_client_admin.post("/auth/register")

    user_service = UserService(session=async_session)

    updated_data = UserUpdate(**{"email": "testuser@example.com"})
    current_user = UserBase(**create_admin_users)

    with pytest.raises(HTTPException) as exc_info:
        await user_service.update_user(current_user=current_user, user_data=updated_data)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Email уже используется другим пользователем."

