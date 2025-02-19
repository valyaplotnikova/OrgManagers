from select import select

from user_team_service.user_app.models.user_model import User
from user_team_service.user_app.repositories.base_repository import BaseRepository


class UsersRepository(BaseRepository):
    model = User
