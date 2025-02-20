from pydantic import BaseModel, Field


class SNewsCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100, description="Название новости")
    content: str = Field(min_length=50, max_length=500, description="Контент новости")


class SNews(SNewsCreate):
    author_id: int = Field(description="Идентификатор автора новости")


class SNewsAll(SNews):
    id: int = Field(description="Идентификатор новости")


class SNewsFilter(BaseModel):
    id: int = Field(description="Идентификатор новости")
