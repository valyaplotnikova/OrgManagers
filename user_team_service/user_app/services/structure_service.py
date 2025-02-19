from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from user_team_service.user_app.exceptions.exception import StructureNotFoundException, StructureMemberNotFoundException
from user_team_service.user_app.repositories.teams_repository import StructureRepository, StructureMemberRepository
from user_team_service.user_app.schemas.structure_schema import (SStructure, SStructureChange, SStructureResponse,
                                                                 SstrMembers, SStrMemResponse, SStrMemAll,
                                                                 SStructureUpdate, SStrMemFilter)


class StructureService:
    def __init__(self, session: AsyncSession):
        """
        Инициализация сервиса структур.

        :param session: Асинхронная сессия базы данных.
        """
        self.session = session
        self.structure_repo = StructureRepository(session)
        self.member_repo = StructureMemberRepository(session)

    async def create_structure(self, structure_data: SStructure) -> SStructure:
        """
        Создание новой структуры.

        :param structure_data: Данные для создания структуры.
        :return: Созданная структура.
        """
        structure_data_dict = structure_data.model_dump()
        new_structure = SStructure(**structure_data_dict)
        await self.structure_repo.add(values=new_structure)
        return new_structure

    async def update_structure(self, structure_id: int, structure_data: SStructureUpdate) -> dict:
        """
        Обновление существующей структуры.

        :param structure_id: Идентификатор структуры для обновления.
        :param structure_data: Данные для обновления структуры.
        :raises HTTPException: Если запись не обновлена.
        :return: Сообщение об успешном обновлении.
        """
        rowcount = await self.structure_repo.update(
            filters=SStructureChange(id=structure_id),
            values=structure_data
        )
        if rowcount == 0:
            raise HTTPException(status_code=404, detail="Записи не обновлены")
        return {'message': 'Данные успешно обновлены!'}

    async def delete_structure(self, structure_id: int) -> dict:
        """
        Удаление структуры по идентификатору.

        :param structure_id: Идентификатор структуры для удаления.
        :raises HTTPException: Если удаление не выполнено.
        :return: Сообщение об успешном удалении.
        """
        rowcount = await self.structure_repo.delete(
            filters=SStructureChange(id=structure_id),
        )
        if rowcount == 0:
            raise HTTPException(status_code=404, detail="Удаление не выполнено")
        return {'message': 'Данные успешно удалены!'}

    async def get_structure(self, structure_id: int) -> SStructure:
        """
        Получение структуры по идентификатору.

        :param structure_id: Идентификатор структуры.
        :return: Информация о структуре.
        """
        structure = await self.structure_repo.find_one_or_none_by_id(structure_id)
        if not structure:
            raise StructureNotFoundException
        return structure

    async def get_all_structures(self) -> List[SStructureResponse]:
        """
        Получение всех структур.

        :return: Список всех структур.
        """
        return await self.structure_repo.find_all()

    async def create_structure_member(self, structure_data: SstrMembers) -> dict:
        """
        Создание нового участника структуры.

        :param structure_data: Данные для создания участника структуры.
        :return: Сообщение об успешном создании.
        """
        structure_data_dict = structure_data.model_dump()
        new_member = SstrMembers(**structure_data_dict)
        await self.member_repo.add(values=new_member)
        return {'message': 'Участник структуры успешно создан!'}

    async def update_structure_member(self, structure_member_id: int, structure_data: SstrMembers) -> dict:
        """
        Обновление участника структуры.

        :param structure_member_id: Идентификатор участника структуры.
        :param structure_data: Данные для обновления участника структуры.
        :raises HTTPException: Если запись не обновлена.
        :return: Сообщение об успешном обновлении.
        """

        structure_member = await self.member_repo.find_one_or_none_by_id(structure_member_id)
        if not structure_member:
            raise StructureMemberNotFoundException
        rowcount = await self.member_repo.update(
            filters=SStructureChange(id=structure_member_id),
            values=structure_data
        )
        if rowcount == 0:
            raise HTTPException(status_code=404, detail="Записи не обновлены")
        return {'message': 'Данные успешно обновлены!'}

    async def delete_structure_member(self, structure_member_id: int) -> dict:
        """
        Удаление участника структуры по идентификатору.

        :param structure_member_id: Идентификатор участника структуры.
        :raises HTTPException: Если удаление не выполнено.
        :return: Сообщение об успешном удалении.
        """
        rowcount = await self.member_repo.delete(
            filters=SStrMemFilter(id=structure_member_id),
        )
        if rowcount == 0:
            raise HTTPException(status_code=404, detail="Удаление не выполнено")
        return {'message': 'Данные успешно удалены!'}

    async def get_structure_member(self, structure_member_id: int) -> SstrMembers:
        """
        Получение участника структуры по идентификатору.

        :param structure_member_id: Идентификатор участника структуры.
        :raises HTTPException: Если участник не найден.
        :return: Информация об участнике структуры.
        """
        member = await self.member_repo.find_one_or_none_by_id(structure_member_id)
        if not member:
            raise HTTPException(status_code=404, detail="Участник не найден")
        return member

    async def get_structure_members(self, structure_id: int) -> dict:
        """
        Получение всех участников структуры по идентификатору структуры.

        :param structure_id: Идентификатор структуры.
        :raises HTTPException: Если структура не найдена.
        :return: Список участников структуры.
        """
        structure = await self.structure_repo.find_one_or_none_by_id(structure_id)
        if not structure:
            raise HTTPException(status_code=404, detail="Структура не найдена")

        members = await self.member_repo.find_all(filters=SStrMemAll(structure_id=structure_id))
        members_response = [SStrMemResponse(**member.__dict__) for member in members]

        return {"structure_id": structure_id, "members": members_response}

    async def get_all_structure_members(self) -> list[SStrMemResponse]:
        """
        Получение всех участников всех структур.

        :return: Список всех участников структур.
        """
        return await self.member_repo.find_all()
