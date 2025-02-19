from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class SstrMembers(BaseModel):
    user_id: int = Field(description="Идентификатор участника структуры")
    structure_id: int = Field(description="Идентификатор структуры")
    manager_id: Optional[int | None] = None
    role: str = Field(description="Роль участника структуры")


class SStructure(BaseModel):
    name: str = Field(description="Название структуры")
    company_id: int = Field(description="Идентификатор компании")
    members: list = Field(description="Список участников структуры")

    model_config = ConfigDict(from_attributes=True)


class SStructureResponse(SStructure):
    id: int = Field(description="Идентификатор структуры")


class SStructureChange(BaseModel):
    id: int = Field(description="Идентификатор структуры")


class SStrMemAll(BaseModel):
    structure_id: int = Field(description="Идентификатор структуры")


class SStrMemID(SstrMembers):
    id: int = Field(description="Идентификатор участника структуры")


class SStrMemResponse(SStrMemID):
    ...


class SStructureUpdate(BaseModel):
    name: str = Field(description="Название структуры")
    company_id: int = Field(description="Идентификатор компании")


class SStrMemFilter(BaseModel):
    id: int = Field(description="Идентификатор участника структуры")