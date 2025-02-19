from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from user_team_service.user_app.exceptions.auth_exceptions import UserNotFoundException
from user_team_service.user_app.exceptions.exception import CompanyAlreadyExistsException, CompanyNotFoundException
from user_team_service.user_app.repositories.auth_repository import UsersRepository
from user_team_service.user_app.repositories.teams_repository import CompanyRepository
from user_team_service.user_app.schemas.auth_schemas import SUserCompany, SUserSearch
from user_team_service.user_app.schemas.company_schemas import SCompanyCreate, SCompanyDelete


class CompanyUserService:
    def __init__(self, session: AsyncSession):
        """
        Инициализация CompanyUser Service.

        :param session: Асинхронная сессия базы данных.
        """
        self.session = session
        self.company_repo = CompanyRepository(session)
        self.user_repo = UsersRepository(session)

    async def create_company(self, company_data: SCompanyCreate):
        """
        Создание новой компании.

        :param company_data: Данные для создания компании.
        :raises CompanyAlreadyExistsException: Если компания с таким именем уже существует.
        """
        existing_comp = await self.company_repo.find_one_or_none(filters=SCompanyCreate(name=company_data.name))
        if existing_comp:
            raise CompanyAlreadyExistsException

        await self.company_repo.add(values=company_data)
        return {'message': f'Компания {company_data.name} успешно создана!'}

    async def update_company(self, company_id: int, company_data: SCompanyCreate):
        """
        Обновление данных компании по ее идентификатору.

        :param company_id: Идентификатор компании для обновления.
        :param company_data: Новые данные компании.
        :raises CompanyNotFoundException: Если компания не найдена или данные не обновлены.
        """
        rowcount = await self.company_repo.update(filters=SCompanyDelete(id=company_id), values=company_data)
        if rowcount == 0:
            raise CompanyNotFoundException

    async def delete_company(self, company_id: int):
        """
        Удаление компании по ее идентификатору.

        :param company_id: Идентификатор компании для удаления.
        :raises CompanyNotFoundException: Если компания не найдена или не удалена.
        """
        rowcount = await self.company_repo.delete(filters=SCompanyDelete(id=company_id))
        if rowcount == 0:
            raise CompanyNotFoundException

    async def get_all_companies(self):
        """
        Получение списка всех компаний.

        :return: Список всех компаний.
        """
        return await self.company_repo.find_all()

    async def get_company_by_id(self, company_id: int):
        """
        Получение компании по ее идентификатору.

        :param company_id: Идентификатор компании.
        :return: Данные компании.
        :raises CompanyNotFoundException: Если компания не найдена.
        """
        company = await self.company_repo.find_one_or_none_by_id(company_id)
        if not company:
            raise CompanyNotFoundException
        return company

    async def add_user_to_company(self, user_id: int, company_id: int):
        """
        Добавление пользователя в компанию.

        :param user_id: Идентификатор пользователя.
        :param company_id: Идентификатор компании.
        :raises UserNotFoundException: Если пользователь не найден.
        :raises CompanyNotFoundException: Если компания не найдена.
        :raises HTTPException: Если запись не обновлена.
        """
        user_data = await self.user_repo.find_one_or_none_by_id(user_id)
        if not user_data:
            raise UserNotFoundException

        # Проверка на существование компании
        company_data = await self.company_repo.find_one_or_none_by_id(company_id)
        if not company_data:
            raise CompanyNotFoundException

        updated_values = SUserCompany(company_id=company_id)
        rowcount = await self.user_repo.update(filters=SUserSearch(id=user_id), values=updated_values)
        if rowcount == 0:
            raise HTTPException(status_code=404, detail="Записи не обновлены.")

    async def remove_user_from_company(self, user_id: int):
        """
        Удаление пользователя из компании.

        :param user_id: Идентификатор пользователя для удаления.
        :raises HTTPException: Если запись не обновлена.
        """
        updated_values = SUserCompany(company_id=None)
        rowcount = await self.user_repo.update(filters=SUserSearch(id=user_id), values=updated_values)
        if rowcount == 0:
            raise HTTPException(status_code=404, detail="Записи не обновлены.")
