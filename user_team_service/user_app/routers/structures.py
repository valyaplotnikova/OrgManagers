from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from user_team_service.user_app.dependencies.auth_dep import get_current_admin_user, get_current_user
from user_team_service.user_app.dependencies.repository_dep import get_session_with_commit, get_session_without_commit
from user_team_service.user_app.models import User
from user_team_service.user_app.schemas.structure_schema import SStructure, SstrMembers, SStructureResponse, SStrMemResponse
from user_team_service.user_app.services.structure_service import StructureService

router = APIRouter()


@router.post("/create")
async def create_structure(structure_data: SStructure,
                           current_user: User = Depends(get_current_admin_user),
                           session: AsyncSession = Depends(get_session_with_commit)) -> dict:
    service = StructureService(session)
    await service.create_structure(structure_data)
    return {'message': 'Структура успешно создана!'}


@router.put("/update/{structure_id}")
async def update_structure(structure_id: int,
                           structure_data: SStructure,
                           current_user: User = Depends(get_current_admin_user),
                           session: AsyncSession = Depends(get_session_with_commit)):
    service = StructureService(session)
    return await service.update_structure(structure_id, structure_data)


@router.delete("/delete/{structure_id}")
async def delete_structure(structure_id: int,
                           current_user: User = Depends(get_current_admin_user),
                           session: AsyncSession = Depends(get_session_with_commit)):
    service = StructureService(session)
    return await service.delete_structure(structure_id)


@router.get("/get/{structure_id}")
async def get_structure(structure_id: int,
                        current_user: User = Depends(get_current_user),
                        session: AsyncSession = Depends(get_session_without_commit)) -> SStructureResponse:
    service = StructureService(session)
    return await service.get_structure(structure_id)


@router.get("/all")
async def get_structures(current_user: User = Depends(get_current_user),
                         session: AsyncSession = Depends(get_session_without_commit)) -> List[SStructureResponse]:
    service = StructureService(session)
    return await service.get_all_structures()


@router.post("/create_member")
async def create_structure_member(structure_data: SstrMembers,
                                  current_user: User = Depends(get_current_admin_user),
                                  session: AsyncSession = Depends(get_session_with_commit)) -> dict:
    service = StructureService(session)
    return await service.create_structure_member(structure_data)


@router.put("/update_member/{structure_member_id}")
async def update_structure_member(structure_member_id: int,
                                  structure_data: SstrMembers,
                                  current_user: User = Depends(get_current_admin_user),
                                  session: AsyncSession = Depends(get_session_with_commit)) -> dict:
    service = StructureService(session)
    return await service.update_structure_member(structure_member_id, structure_data)


@router.delete("/delete_member/{structure_member_id}")
async def delete_structure_member(structure_member_id: int,
                                  current_user: User = Depends(get_current_admin_user),
                                  session: AsyncSession = Depends(get_session_with_commit)):
    service = StructureService(session)
    return await service.delete_structure_member(structure_member_id)


@router.get("/get_member/{structure_member_id}")
async def get_structure_member(structure_member_id: int,
                               current_user: User = Depends(get_current_user),
                               session: AsyncSession = Depends(get_session_without_commit)):
    """
    Получение участника структуры по его идентификатору.
    """
    service = StructureService(session)
    return await service.get_structure_member(structure_member_id)


@router.get("/members/{structure_id}")
async def get_structure_members(structure_id: int,
                                current_user: User = Depends(get_current_user),
                                session: AsyncSession = Depends(get_session_without_commit)) -> dict:
    """
    Получение всех участников структуры по идентификатору структуры.
    """
    service = StructureService(session)
    return await service.get_structure_members(structure_id)


@router.get("/all_members")
async def get_all_structure_members(current_user: User = Depends(get_current_user),
                                    session: AsyncSession = Depends(get_session_without_commit)
                                    ) -> list[SStrMemResponse]:
    """
    Получение всех участников всех структур.
    """
    service = StructureService(session)
    return await service.get_all_structure_members()
