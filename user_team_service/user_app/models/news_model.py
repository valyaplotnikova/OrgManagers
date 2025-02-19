from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from user_team_service.user_app.database.database import Base

if TYPE_CHECKING:
    from .user_model import User


class News(Base):
    """
    Модель новостей, представляющая отдельную новость в системе.

    Атрибуты:
        title (str): Заголовок новости.
        content (str): Содержимое новости.
        author_id (int): Идентификатор автора, ссылающийся на пользователя.
        author (User ): Автор новости, связанный с моделью User.
    """

    title: Mapped[str]
    content: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))

    author: Mapped["User"] = relationship("User", lazy="joined")
