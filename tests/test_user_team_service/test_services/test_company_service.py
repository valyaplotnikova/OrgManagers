import pytest
from fastapi import HTTPException
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from user_team_service.user_app.models import User
from user_team_service.user_app.schemas.company_schemas import SCompanyCreate

from user_team_service.user_app.services.company_service import CompanyUserService


@pytest.mark.asyncio
async def test_create_company(async_session: AsyncSession, authenticated_client_admin):

    await authenticated_client_admin.post("/auth/register")
    service = CompanyUserService(session=async_session)
    company_data = SCompanyCreate(name="Test Company")

    await service.create_company(company_data)

    company = await service.get_company_by_id(1)
    assert company.name == "Test Company"


@pytest.mark.asyncio
async def test_create_company_already_exists(async_session: AsyncSession, authenticated_client_admin):

    await authenticated_client_admin.post("/auth/register")
    service = CompanyUserService(session=async_session)
    company_data = SCompanyCreate(name="Test Company")

    response = await service.create_company(company_data)
    assert response["message"] == 'Компания Test Company успешно создана!'

    with pytest.raises(HTTPException) as exc_info:
        await service.create_company(company_data)


@pytest.mark.asyncio
async def test_update_company(async_session: AsyncSession, authenticated_client_admin):

    await authenticated_client_admin.post("/auth/register")
    service = CompanyUserService(session=async_session)
    company_data = SCompanyCreate(name="Test Company")
    await service.create_company(company_data)

    updated_data = SCompanyCreate(name="Updated Company")
    await service.update_company(3, updated_data)

    company = await service.get_company_by_id(3)
    assert company.name == "Updated Company"


@pytest.mark.asyncio
async def test_update_company_not_found(async_session: AsyncSession, authenticated_client_admin):

    await authenticated_client_admin.post("/auth/register")
    service = CompanyUserService(session=async_session)
    updated_data = SCompanyCreate(name="Updated Company")

    with pytest.raises(HTTPException):
        await service.update_company(999, updated_data)  # ID, который не существует


@pytest.mark.asyncio
async def test_delete_company(async_session: AsyncSession, authenticated_client_admin):

    await authenticated_client_admin.post("/auth/register")
    service = CompanyUserService(session=async_session)
    company_data = SCompanyCreate(name="Test Company")
    await service.create_company(company_data)

    await service.delete_company(4)

    with pytest.raises(HTTPException):
        await service.get_company_by_id(4)


@pytest.mark.asyncio
async def test_delete_company_not_found(async_session: AsyncSession, authenticated_client_admin):

    await authenticated_client_admin.post("/auth/register")
    service = CompanyUserService(session=async_session)

    with pytest.raises(HTTPException):
        await service.delete_company(999)


@pytest.mark.asyncio
async def test_add_user_to_company(async_session: AsyncSession, authenticated_client_admin):

    await authenticated_client_admin.post("/auth/register")
    service = CompanyUserService(session=async_session)
    company_data = SCompanyCreate(name="Test Company")
    await service.create_company(company_data)

    user_data = {
        "email": "user1@mail.com",
        "first_name": "User ",
        "last_name": "User ",
        "password": "zxc123"
    }
    await async_session.execute(insert(User).values(**user_data))
    await service.add_user_to_company(1, 5)

    user = await service.user_repo.find_one_or_none_by_id(1)
    assert user.company_id == 5


@pytest.mark.asyncio
async def test_add_user_to_company_user_not_found(async_session: AsyncSession, authenticated_client_admin):

    await authenticated_client_admin.post("/auth/register")
    service = CompanyUserService(session=async_session)
    company_data = SCompanyCreate(name="Test Company")
    await service.create_company(company_data)

    with pytest.raises(HTTPException):
        await service.add_user_to_company(999, 1)


@pytest.mark.asyncio
async def test_remove_user_from_company(async_session: AsyncSession, authenticated_client_admin):

    await authenticated_client_admin.post("/auth/register")
    service = CompanyUserService(session=async_session)
    company_data = SCompanyCreate(name="Test Company")
    await service.create_company(company_data)

    user_data = {
        "email": "user2@mail.com",
        "first_name": "User ",
        "last_name": "User ",
        "password": "zxc123"
    }
    await async_session.execute(insert(User).values(**user_data))
    await service.add_user_to_company(1, 7)

    await service.remove_user_from_company(1)

    user = await service.user_repo.find_one_or_none_by_id(1)
    assert user.company_id is None


@pytest.mark.asyncio
async def test_remove_user_from_company_not_found(async_session: AsyncSession, authenticated_client_admin):

    await authenticated_client_admin.post("/auth/register")
    service = CompanyUserService(session=async_session)

    with pytest.raises(HTTPException):
        await service.remove_user_from_company(999)


@pytest.mark.asyncio
async def test_get_all_companies(async_session: AsyncSession, authenticated_client_admin):

    await authenticated_client_admin.post("/auth/register")
    service = CompanyUserService(session=async_session)
    company_data1 = SCompanyCreate(name="Company 1")
    company_data2 = SCompanyCreate(name="Company 2")

    await service.create_company(company_data1)
    await service.create_company(company_data2)

    companies = await service.get_all_companies()

    assert len(companies) == 2
    assert companies[0].name == "Company 1"
    assert companies[1].name == "Company 2"


@pytest.mark.asyncio
async def test_get_company_by_id(async_session: AsyncSession, authenticated_client_admin):

    await authenticated_client_admin.post("/auth/register")
    service = CompanyUserService(session=async_session)
    company_data = SCompanyCreate(name="Test Company")
    await service.create_company(company_data)

    company = await service.get_company_by_id(10)

    assert company.name == "Test Company"


@pytest.mark.asyncio
async def test_get_company_by_id_not_found(async_session: AsyncSession, authenticated_client_admin):

    await authenticated_client_admin.post("/auth/register")
    service = CompanyUserService(session=async_session)

    with pytest.raises(HTTPException):
        await service.get_company_by_id(999)
