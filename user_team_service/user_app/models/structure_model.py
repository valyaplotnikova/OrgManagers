import enum
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from user_team_service.user_app.database.database import Base

if TYPE_CHECKING:
    from .user_model import User
    from .company_model import Company


class RoleEnum(enum.Enum):
    """
    Перечисление для ролей участников структур.

    Роли:
        ADMIN: Администратор структуры.
        MANAGER: Менеджер структуры.
        EMPLOYEE: Сотрудник структуры.
    """

    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"


class Structure(Base):
    """
    Модель структуры, представляющая организационную единицу компании.

    Атрибуты:
        name (str): Название структуры, уникальное и обязательное.
        company_id (int): Идентификатор компании, к которой принадлежит структура.
        members (list[StructureMember]): Список участников структуры.
        company (Company): Связь с моделью Company, представляющая компанию, к которой принадлежит структура.
    """

    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    company_id: Mapped[int] = mapped_column(ForeignKey("companys.id", ondelete='CASCADE'), nullable=False)
    members: Mapped[list["StructureMember"]] = relationship(
        "StructureMember",
        back_populates="structure",
    )

    company: Mapped["Company"] = relationship(
        "Company",
        foreign_keys=[company_id],
        back_populates="structures",
      )


class StructureMember(Base):
    """
    Модель участника структуры, представляющая отдельного пользователя в рамках структуры.

    Атрибуты:
        user_id (int): Идентификатор пользователя, который является участником структуры (может быть NULL).
        structure_id (int): Идентификатор структуры, к которой принадлежит участник.
        manager_id (int): Идентификатор менеджера, который курирует участника (может быть NULL).
        role (RoleEnum): Роль участника в структуре.
        user (User ): Связь с моделью User, представляющая участника.
        structure (Structure): Связь с моделью Structure, представляющая структуру, к которой принадлежит участник.
        manager (StructureMember): Связь с менеджером, который курирует участника.
    """

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    structure_id: Mapped[str] = mapped_column(ForeignKey("structures.id", ondelete="CASCADE"), nullable=False)
    manager_id: Mapped[int] = mapped_column(ForeignKey("structuremembers.id", ondelete="SET NULL"), nullable=True)
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum, name='roleenum', create_type=True),
                                           default=RoleEnum.EMPLOYEE)
    user: Mapped["User"] = relationship("User", lazy="joined")  # Связь с пользователем
    structure: Mapped["Structure"] = relationship("Structure", back_populates="members")
    manager: Mapped["StructureMember"] = relationship(
        "StructureMember",
        remote_side="StructureMember.id",
        backref="subordinates",
        lazy="joined")
