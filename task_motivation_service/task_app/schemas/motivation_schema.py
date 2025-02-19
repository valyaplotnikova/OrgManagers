from pydantic import BaseModel, Field


class SMotivationCreate(BaseModel):
    task_id: int = Field(description="Идентификатор задачи")
    rating: int = Field(description="Оценка за выполнение задачи по пятибальной шкале")
    comment: str = Field(min_length=3, max_length=250, description="Комментарий к задаче")


class SMotivationUpdate(BaseModel):
    rating: int = Field(description="Оценка за выполнение задачи по пятибальной шкале")
    comment: str = Field(min_length=3, max_length=250, description="Комментарий к задаче")


class SMotivationSearch(BaseModel):
    task_id: int = Field(description="Идентификатор задачи")


class SMotivationSearchID(BaseModel):
    id: int = Field(description="Идентификатор оценки задачи")

