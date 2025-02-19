import enum
from datetime import datetime

from sqlalchemy import Enum, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from task_motivation_service.task_app.database.database import Base


class StatusEnum(enum.Enum):
    """
    Перечисление для статусов задачи.

    Статусы:
        CREATED: создана.
        IN_WORK: в работе.
        DONE: завершена.
    """
    CREATED = "created"
    IN_WORK = "in_work"
    DONE = "done"


class Task(Base):

    title: Mapped[str]
    content: Mapped[str]
    assigned_by: Mapped[int]
    assigned_to: Mapped[int]
    deadline: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    comment: Mapped[str]
    status: Mapped[StatusEnum] = mapped_column(Enum(StatusEnum, name='statusenum', create_type=True),
                                               default=StatusEnum.CREATED)

    # Связь с моделью Motivation
    motivations: Mapped[list] = relationship("Motivation", back_populates="task")



