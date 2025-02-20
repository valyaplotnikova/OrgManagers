from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from user_team_service.user_app.database.database import Base

if TYPE_CHECKING:
    from .user_model import User
    from .structure_model import Structure


class Company(Base):
    """
    Модель компании, представляющая организацию в системе.

    Атрибуты:
        name (str): Название компании, уникальное и обязательное поле.
        users (list[User ]): Список пользователей, связанных с компанией.
        structures (list[Structure]): Список структур, связанных с компанией.
    """

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    users: Mapped[list["User"]] = relationship("User", back_populates="company")
    structures: Mapped[list["Structure"]] = relationship("Structure", back_populates="company")
