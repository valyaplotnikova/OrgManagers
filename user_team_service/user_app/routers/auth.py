from typing import List, Optional
from fastapi import APIRouter, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.user_model import User
from ..repositories.teams_repository import CompanyRepository
from ..utils import authenticate_user, set_tokens
from ..dependencies.auth_dep import (get_current_user, get_current_admin_user, check_refresh_token)
from ..dependencies.repository_dep import get_session_with_commit, get_session_without_commit
from ..exceptions.auth_exceptions import (UserAlreadyExistsException, IncorrectEmailOrPasswordException)
from ..repositories.auth_repository import UsersRepository
from ..schemas.auth_schemas import SUserRegister, SUserAuth, EmailModel, SUserAddDB, SUserInfo

router = APIRouter()


@router.post("/register")
async def register_user(user_data: SUserRegister, company_id: Optional[int | None] = None,
                        session: AsyncSession = Depends(get_session_with_commit)) -> dict:
    # Проверка существования пользователя

    existing_user = await UsersRepository(session).find_one_or_none(filters=EmailModel(email=user_data.email))
    if existing_user:
        raise UserAlreadyExistsException

    # Подготовка данных для добавления
    user_data_dict = user_data.model_dump()
    user_data_dict.pop('confirm_password', None)
    if company_id:
        company = await CompanyRepository(session).find_one_or_none_by_id(data_id=company_id)
        if company:
            user_data_dict["company_id"] = company_id
        else:
            raise ValueError("Неправильный код компании.")
    # Добавление пользователя
    await UsersRepository(session).add(values=SUserAddDB(**user_data_dict))

    return {'message': 'Вы успешно зарегистрированы!'}


@router.post("/login")
async def auth_user(
        response: Response,
        user_data: SUserAuth,
        session: AsyncSession = Depends(get_session_without_commit)
) -> dict:
    user = await UsersRepository(session).find_one_or_none(
        filters=EmailModel(email=user_data.email)
    )

    if not (user and await authenticate_user(user=user, password=user_data.password)):
        raise IncorrectEmailOrPasswordException
    set_tokens(response, user.id)
    return {
        'token': True,
        'message': 'Авторизация успешна!'
    }


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("user_access_token")
    response.delete_cookie("user_refresh_token")
    return {'message': 'Пользователь успешно вышел из системы'}


@router.get("/me")
async def get_me(user_data: User = Depends(get_current_user)) -> SUserInfo:
    return SUserInfo.model_validate(user_data)


@router.get("/all_users")
async def get_all_users(session: AsyncSession = Depends(get_session_without_commit),
                        user_data: User = Depends(get_current_admin_user)
                        ) -> List[SUserInfo]:
    return await UsersRepository(session).find_all()


@router.post("/refresh")
async def process_refresh_token(
        response: Response,
        user: User = Depends(check_refresh_token)
):
    set_tokens(response, user.id)
    return {"message": "Токены успешно обновлены"}
