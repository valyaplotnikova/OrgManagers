import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from user_team_service.user_app.schemas.company_schemas import SCompanyCreate
from user_team_service.user_app.schemas.structure_schema import SStructure, SstrMembers, SStructureUpdate
from user_team_service.user_app.services.company_service import CompanyUserService
from user_team_service.user_app.services.structure_service import StructureService
from fastapi.exceptions import HTTPException


@pytest.mark.asyncio
async def test_create_structure(async_session: AsyncSession, authenticated_client_admin):

    await authenticated_client_admin.post("/auth/register")
    structure_service = StructureService(session=async_session)
    company_service = CompanyUserService(session=async_session)
    company_data = SCompanyCreate(name="Company 1")
    await company_service.create_company(company_data)
    structure_data = SStructure(name="Test Structure", company_id=11, members=[])
    result = await structure_service.create_structure(structure_data)
    assert result.name == "Test Structure"


@pytest.mark.asyncio
async def test_update_structure(async_session: AsyncSession, authenticated_client_admin):

    await authenticated_client_admin.post("/auth/register")
    service = StructureService(session=async_session)
    company_service = CompanyUserService(session=async_session)
    company_data = SCompanyCreate(name="Company 1")
    await company_service.create_company(company_data)
    structure_data = SStructure(name="Test Structure", company_id=12, members=[])
    await service.create_structure(structure_data)

    updated_data = SStructureUpdate(name="Updated Structure", company_id=12)
    response = await service.update_structure(2, updated_data)

    assert response['message'] == 'Данные успешно обновлены!'


@pytest.mark.asyncio
async def test_update_structure_not_found(async_session: AsyncSession, authenticated_client_admin):

    await authenticated_client_admin.post("/auth/register")
    service = StructureService(session=async_session)
    updated_data = SStructureUpdate(name="Updated Structure", company_id=12)

    with pytest.raises(HTTPException):
        await service.update_structure(999, updated_data)


@pytest.mark.asyncio
async def test_delete_structure(async_session: AsyncSession, authenticated_client_admin):

    await authenticated_client_admin.post("/auth/register")
    service = StructureService(session=async_session)
    company_service = CompanyUserService(session=async_session)
    company_data = SCompanyCreate(name="Company 1")
    await company_service.create_company(company_data)

    structure_data = SStructure(name="Test Structure", company_id=13, members=[])
    await service.create_structure(structure_data)

    response = await service.delete_structure(3)

    assert response['message'] == 'Данные успешно удалены!'


@pytest.mark.asyncio
async def test_delete_structure_not_found(async_session: AsyncSession, authenticated_client_admin):

    await authenticated_client_admin.post("/auth/register")
    service = StructureService(session=async_session)

    with pytest.raises(HTTPException):
        await service.delete_structure(999)


@pytest.mark.asyncio
async def test_get_structure(async_session: AsyncSession, authenticated_client_admin):

    await authenticated_client_admin.post("/auth/register")
    service = StructureService(session=async_session)
    company_service = CompanyUserService(session=async_session)
    company_data = SCompanyCreate(name="Company 1")
    await company_service.create_company(company_data)
    structure_data = SStructure(name="Test Structure", company_id=14, members=[])
    await service.create_structure(structure_data)
    structure = await service.get_structure(4)

    assert structure.name == "Test Structure"


@pytest.mark.asyncio
async def test_get_structure_not_found(async_session: AsyncSession, authenticated_client_admin):

    await authenticated_client_admin.post("/auth/register")
    service = StructureService(session=async_session)

    with pytest.raises(HTTPException):
        await service.get_structure(999)


@pytest.mark.asyncio
async def test_get_all_structures(async_session: AsyncSession, authenticated_client_admin):

    await authenticated_client_admin.post("/auth/register")
    service = StructureService(session=async_session)

    company_service = CompanyUserService(session=async_session)
    company_data1 = SCompanyCreate(name="Company 1")
    company_data2 = SCompanyCreate(name="Company 2")
    await company_service.create_company(company_data1)
    await company_service.create_company(company_data2)
    structure_data1 = SStructure(name="Structure 1", company_id=15, members=[])
    structure_data2 = SStructure(name="Structure 2", company_id=16, members=[])

    await service.create_structure(structure_data1)
    await service.create_structure(structure_data2)

    structures = await service.get_all_structures()

    assert len(structures) == 2
    assert structures[0].name == "Structure 1"
    assert structures[1].name == "Structure 2"


@pytest.mark.asyncio
async def test_create_structure_member(async_session: AsyncSession, authenticated_client_admin):

    await authenticated_client_admin.post("/auth/register")
    service = StructureService(session=async_session)
    company_service = CompanyUserService(session=async_session)
    company_data = SCompanyCreate(name="Company 1")
    await company_service.create_company(company_data)
    structure_data = SStructure(name="Test Structure", company_id=17, members=[])
    await service.create_structure(structure_data)

    member_data = SstrMembers(name="Member 1", user_id=1, role="EMPLOYEE", structure_id=7)
    result = await service.create_structure_member(member_data)

    assert result['message'] == 'Участник структуры успешно создан!'


@pytest.mark.asyncio
async def test_update_structure_member(async_session: AsyncSession, authenticated_client_admin):

    await authenticated_client_admin.post("/auth/register")
    service = StructureService(session=async_session)
    company_service = CompanyUserService(session=async_session)
    company_data = SCompanyCreate(name="Company 1")
    await company_service.create_company(company_data)
    structure_data = SStructure(name="Test Structure", company_id=18, members=[])
    await service.create_structure(structure_data)

    member_data = SstrMembers(name="Member 1", user_id=1, role="EMPLOYEE", structure_id=8)
    await service.create_structure_member(member_data)

    updated_member_data = SstrMembers(name="Updated Member", user_id=1, role="EMPLOYEE", structure_id=8)
    response = await service.update_structure_member(2, updated_member_data)

    assert response['message'] == 'Данные успешно обновлены!'


@pytest.mark.asyncio
async def test_delete_structure_member(async_session: AsyncSession, authenticated_client_admin):

    await authenticated_client_admin.post("/auth/register")
    service = StructureService(session=async_session)
    company_service = CompanyUserService(session=async_session)
    company_data = SCompanyCreate(name="Company 1")
    await company_service.create_company(company_data)
    structure_data = SStructure(name="Test Structure", company_id=19, members=[])
    await service.create_structure(structure_data)

    member_data = SstrMembers(name="Member 1", user_id=1, role="EMPLOYEE", structure_id=9)
    await service.create_structure_member(member_data)

    response = await service.delete_structure_member(3)

    assert response['message'] == 'Данные успешно удалены!'


@pytest.mark.asyncio
async def test_get_structure_member(async_session, authenticated_client_admin):
    await authenticated_client_admin.post("/auth/register")
    service = StructureService(session=async_session)
    company_service = CompanyUserService(session=async_session)
    company_data = SCompanyCreate(name="Company 1")
    await company_service.create_company(company_data)
    structure_data = SStructure(name="Test Structure", company_id=20, members=[])
    await service.create_structure(structure_data)

    member_data = SstrMembers(name="Member 1", user_id=1, role="EMPLOYEE", structure_id=10)
    await service.create_structure_member(member_data)
    response = await service.get_structure_member(4)
    assert response.id == 4


@pytest.mark.asyncio
async def test_get_structure_members(add_results, async_session, authenticated_client_admin):

    await authenticated_client_admin.post("/auth/register")
    service = StructureService(session=async_session)
    company_service = CompanyUserService(session=async_session)
    company_data = SCompanyCreate(name="Company 1")
    await company_service.create_company(company_data)
    structure_data = SStructure(name="Test Structure", company_id=21, members=[])
    await service.create_structure(structure_data)

    member_data = SstrMembers(name="Member 1", user_id=1, role="EMPLOYEE", structure_id=11)
    await service.create_structure_member(member_data)
    member_data = SstrMembers(name="Member 2", user_id=3, role="EMPLOYEE", structure_id=11)
    await service.create_structure_member(member_data)
    response = await service.get_structure_members(11)
    assert len(response["members"]) == 2


@pytest.mark.asyncio
async def test_get_all_structure_members(add_results, async_session, authenticated_client_admin):

    await authenticated_client_admin.post("/auth/register")
    service = StructureService(session=async_session)
    company_service = CompanyUserService(session=async_session)
    company_data = SCompanyCreate(name="Company 1")
    await company_service.create_company(company_data)
    structure_data = SStructure(name="Test Structure1", company_id=22, members=[])
    await service.create_structure(structure_data)
    structure_data = SStructure(name="Test Structure2", company_id=22, members=[])
    await service.create_structure(structure_data)

    member_data = SstrMembers(name="Member 1", user_id=1, role="EMPLOYEE", structure_id=12)
    await service.create_structure_member(member_data)
    member_data = SstrMembers(name="Member 2", user_id=3, role="EMPLOYEE", structure_id=13)
    await service.create_structure_member(member_data)
    response = await service.get_all_structure_members()
    assert len(response) == 2


