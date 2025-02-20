
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class STaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=50, description="Заголовок, от 3 до 50 символов")
    content: str = Field(description="Содержание задачи")
    assigned_by: int = Field(description="Постановщик задачи")
    assigned_to: int = Field(description="Исполнитель задачи")
    deadline: datetime = Field(description="Сроки выполнения")
    comment: Optional[str] = Field(default=None, description="Комментарий к задаче")
    status: str = Field(description="Статус задачи")


class STaskSearch(BaseModel):
    title: str = Field(min_length=3, max_length=50, description="Заголовок, от 3 до 50 символов")


class STaskUpdate(BaseModel):
    comment: Optional[str] = Field(default=None, description="Комментарий к задаче")
    status: Optional[str] = Field(description="Статус задачи")


class STaskSearchID(BaseModel):
    id: int
