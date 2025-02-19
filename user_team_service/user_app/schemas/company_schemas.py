from pydantic import BaseModel, Field, ConfigDict


class SCompanyCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50, description="Название, от 3 до 50 символов")


class SCompanyResponse(SCompanyCreate):
    id: int = Field(description="Идентификатор компании")
    users: list = Field(description="Список работников компании")

    model_config = ConfigDict(from_attributes=True)


class SCompanyDelete(BaseModel):
    id: int = Field(description="Идентификатор компании")


class SCompanyList(SCompanyDelete, SCompanyCreate):
    ...
