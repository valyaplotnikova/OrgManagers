import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import func, TIMESTAMP, Integer, inspect
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession
from task_motivation_service.task_app.core.config import database_url


if not database_url:
    raise ValueError("Переменная окружения 'database_url' не загружена корректно.")

engine = create_async_engine(
    url=database_url,
    echo=True,  # Включение логирования SQL-запросов для отладки
    pool_size=20,  # Установка размера пула соединений
    max_overflow=10  # Максимальное количество дополнительных соединений
)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'

    def to_dict(self, exclude_none: bool = False):
        """
        Преобразует объект модели в словарь.

        Args:
            exclude_none (bool): Исключать ли None значения из результата

        Returns:
            dict: Словарь с данными объекта
        """
        result = {}
        for column in inspect(self.__class__).columns:
            value = getattr(self, column.key)

            # Преобразование специальных типов данных
            if isinstance(value, datetime):
                value = value.astimezone().isoformat()
            elif isinstance(value, Decimal):
                value = round(float(value), 2)
            elif isinstance(value, uuid.UUID):
                value = str(value)

            # Добавляем значение в результат
            if exclude_none and value is None:
                continue
            result[column.key] = value

        return result

    def __repr__(self) -> str:
        """Строковое представление объекта для удобства отладки."""
        return (f"<{self.__class__.__name__}(id={self.id if self.id else 'unsaved'}, "
                f"created_at={self.created_at}, updated_at={self.updated_at})>")
