from datetime import datetime, timezone
from sqlalchemy import TIMESTAMP, func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from task_motivation_service.task_app.database.database import Base


class Motivation(Base):

    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'))
    rating: Mapped[int]  # Рейтинг выполнения задачи (например, от 1 до 5)
    comment: Mapped[str]  # Комментарий к оценке
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
        default=lambda: datetime.now(timezone.utc)
    )

    # Связь с моделью Task
    task: Mapped["Task"] = relationship("Task", back_populates="motivations")
