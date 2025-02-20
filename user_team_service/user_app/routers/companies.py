from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from user_team_service.user_app.dependencies.auth_dep import get_current_user, get_current_admin_user
from user_team_service.user_app.dependencies.repository_dep import get_session_with_commit, get_session_without_commit
from user_team_service.user_app.models import User
from user_team_service.user_app.schemas.company_schemas import SCompanyCreate
from user_team_service.user_app.services.company_service import CompanyUserService

router = APIRouter()


@router.post("/create")
async def create_company(
    company_data: SCompanyCreate,
    current_user: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_session_with_commit)
):
    """
    Создание новой компании.

    :param company_data: Данные для создания компании.
    :param current_user: Данные текущего администратора.
    :param session: Асинхронная сессия базы данных.
    :return: Сообщение об успешном создании компании.
    """
    service = CompanyUserService(session)
    await service.create_company(company_data)
    return {'message': f'Компания {company_data.name} успешно создана!'}


@router.put("/update/{company_id}")
async def update_company(
    company_id: int,
    company_data: SCompanyCreate,
    current_user: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_session_with_commit)
):
    """
    Обновление данных компании по ее идентификатору.

    :param company_id: Идентификатор компании для обновления.
    :param company_data: Новые данные компании.
    :param current_user: Данные текущего администратора.
    :param session: Асинхронная сессия базы данных.
    :return: Сообщение об успешном обновлении данных компании.
    """
    service = CompanyUserService(session)
    await service.update_company(company_id, company_data)
    return {'message': 'Данные компании успешно обновлены!'}


@router.delete("/delete/{company_id}")
async def delete_company(
    company_id: int,
    current_user: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_session_with_commit)
):
    """
    Удаление компании по ее идентификатору.

    :param company_id: Идентификатор компании для удаления.
    :param current_user: Данные текущего администратора.
    :param session: Асинхронная сессия базы данных.
    :return: Сообщение об успешном удалении компании.
    """
    service = CompanyUserService(session)
    await service.delete_company(company_id)
    return {'message': 'Компания успешно удалена!'}


@router.get("/all")
async def get_companies(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_without_commit)
):
    """
    Получение списка всех компаний.

    :param current_user: Данные текущего пользователя.
    :param session: Асинхронная сессия базы данных.
    :return: Список всех компаний.
    """
    service = CompanyUserService(session)
    companies = await service.get_all_companies()
    return companies


@router.get("/get/{company_id}")
async def get_company(
    company_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_without_commit)
):
    """
    Получение информации о компании по ее идентификатору.

    :param company_id: Идентификатор компании.
    :param current_user: Данные текущего пользователя.
    :param session: Асинхронная сессия базы данных.
    :return: Информация о компании.
    """
    service = CompanyUserService(session)
    company = await service.get_company_by_id(company_id)
    return company


@router.post("/add_user/{user_id}/to_company/{company_id}")
async def add_user_to_company(
    user_id: int,
    company_id: int,
    current_user: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_session_with_commit)
):
    """
    Добавление пользователя в компанию.

    :param user_id: Идентификатор пользователя, которого нужно добавить.
    :param company_id: Идентификатор компании, в которую нужно добавить пользователя.
    :param current_user: Данные текущего администратора.
    :param session: Асинхронная сессия базы данных.
    :return: Сообщение об успешном добавлении пользователя в компанию.
    """
    service = CompanyUserService(session)
    await service.add_user_to_company(user_id, company_id)
    return {'message': 'Пользователь успешно добавлен в компанию!'}


@router.delete("/remove_user/{user_id}")
async def remove_user_from_company(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    session: AsyncSession = Depends(get_session_with_commit)
):
    """
    Удаление пользователя из компании.

    :param user_id: Идентификатор пользователя, которого нужно удалить.
    :param current_user: Данные текущего администратора.
    :param session: Асинхронная сессия базы данных.
    :return: Сообщение об успешном удалении пользователя из компании.
    """
    service = CompanyUserService(session)
    await service.remove_user_from_company(user_id)
    return {'message': 'Пользователь успешно удален из компании!'}
