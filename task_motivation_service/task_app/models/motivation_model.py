from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from task_motivation_service.task_app.database.database import Base


class Motivation(Base):

    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'))
    rating: Mapped[int]  # Рейтинг выполнения задачи (например, от 1 до 5)
    comment: Mapped[str]  # Комментарий к оценке

    # Связь с моделью Task
    task: Mapped["Task"] = relationship("Task", back_populates="motivations")
