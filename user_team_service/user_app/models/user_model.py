from typing import TYPE_CHECKING
from ..database.database import Base
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

if TYPE_CHECKING:
    from .company_model import Company
    from .news_model import News


class StatusEnum(enum.Enum):
    """
    Перечисление для статусов пользователей.

    Статусы:
        ADMIN_GROUP: Администратор группы.
        ADMIN_GENERAL: Генеральный администратор.
        USER: Обычный пользователь.
    """
    ADMIN_GROUP = "admin_group"
    ADMIN_GENERAL = "admin_general"
    USER = "user"


class User(Base):
    """
    Модель пользователя, представляющая отдельного пользователя в системе.

    Атрибуты:
        first_name (str): Имя пользователя.
        last_name (str): Фамилия пользователя.
        email (str): Электронная почта пользователя, уникальная для каждого пользователя.
        password (str): Пароль пользователя.
        status (StatusEnum): Статус пользователя, определяющий его уровень доступа.
        company_id (int): Идентификатор компании, к которой принадлежит пользователь (может быть NULL).
        company (Company): Связь с моделью Company, представляющая компанию пользователя.
        news (list[News]): Список новостей, созданных пользователем.
    """

    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    status: Mapped[StatusEnum] = mapped_column(Enum(StatusEnum, name='statusenum', create_type=True),
                                               default=StatusEnum.USER)
    company_id: Mapped[int] = mapped_column(ForeignKey('companys.id', ondelete="SET NULL"), nullable=True)

    company: Mapped["Company"] = relationship(back_populates="users", uselist=True)
    news: Mapped[list["News"]] = relationship(back_populates="author")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, status={self.status.value})"
