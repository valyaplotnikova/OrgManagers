from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from user_team_service.user_app.exceptions.auth_exceptions import UserNotFoundException
from user_team_service.user_app.models import User
from user_team_service.user_app.repositories.auth_repository import UsersRepository
from user_team_service.user_app.schemas.auth_schemas import SUserInfo, UserBase, EmailModel, SUserStatus, UserUpdate, SUserSearch


class UserService:
    def __init__(self, session: AsyncSession):
        """
        Инициализация UserService.

        :param session: Асинхронная сессия базы данных.
        """
        self.session = session
        self.users_repo = UsersRepository(session)

    async def get_user_by_id(self, user_id: int) -> SUserInfo:
        """
        Получение пользователя по его идентификатору.

        :param user_id: Идентификатор пользователя.
        :return: Данные пользователя.
        :raises UserNotFoundException: Если пользователь не найден.
        """
        return await self.users_repo.find_one_or_none_by_id(user_id)

    async def update_user(self, current_user: User, user_data: UserUpdate) -> dict:
        """
        Обновление данных пользователя.

        :param current_user: Текущий пользователь, чьи данные нужно обновить.
        :param user_data: Данные для обновления пользователя.
        :return: Сообщение об успешном обновлении.
        :raises UserNotFoundException: Если текущий пользователь не найден.
        :raises HTTPException: Если email уже используется другим пользователем.
        :raises HTTPException: Если запись не обновлена.
        """
        if not current_user:
            raise UserNotFoundException

        # Проверка на уникальность email, если он был передан
        if user_data.email:
            existing_user = await self.users_repo.find_all(filters=EmailModel(email=user_data.email))
            if existing_user:
                raise HTTPException(status_code=400, detail="Email уже используется другим пользователем.")

        rowcount = await self.users_repo.update(
            filters=EmailModel(email=current_user.email),
            values=user_data
        )
        if rowcount == 0:
            raise HTTPException(status_code=404, detail="Записи не обновлены")

        return {'message': 'Данные успешно обновлены!'}

    async def delete_user(self, user_id: int) -> dict:
        """
        Удаление пользователя по его идентификатору.

        :param user_id: Идентификатор пользователя для удаления.
        :return: Сообщение об успешном удалении.
        :raises UserNotFoundException: Если пользователь не найден.
        :raises HTTPException: Если удаление не выполнено.
        """
        user_data = await self.users_repo.find_one_or_none_by_id(user_id)
        if not user_data:
            raise UserNotFoundException

        rowcount = await self.users_repo.delete(
            filters=SUserSearch(id=user_id),
        )
        if rowcount == 0:
            raise HTTPException(status_code=404, detail="Удаление не выполнено")

        return {'message': 'Данные успешно удалены!'}

    async def update_user_status(self, user_id: int, status: str) -> dict:
        """
        Обновление статуса пользователя.

        :param user_id: Идентификатор пользователя, статус которого нужно обновить.
        :param status: Новый статус пользователя.
        :return: Сообщение об успешном обновлении статуса.
        :raises UserNotFoundException: Если пользователь не найден.
        :raises HTTPException: Если запись не обновлена.
        """
        user_data = await self.users_repo.find_one_or_none_by_id(user_id)
        if user_data is None:
            raise UserNotFoundException

        user_data.status = status
        updated_values = SUserStatus(status=user_data.status)

        rowcount = await self.users_repo.update(
            filters=EmailModel(email=user_data.email),
            values=updated_values
        )
        if rowcount == 0:
            raise HTTPException(status_code=404, detail="Записи не обновлены")

        return {'message': f'Статус пользователя {user_data.email} успешно обновлен!'}
