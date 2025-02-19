from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class SMeetingBase(BaseModel):

    organisation_by: int = Field(description="Организатор встречи")
    start_at: datetime = Field(description="Начало встречи")
    end_at: datetime = Field(description="Окончание встречи")


class SMeetingCreate(SMeetingBase):
    pass


class SMeetingUpdate(BaseModel):
    start_at: Optional[datetime] = Field(description="Начало встречи")
    end_at: Optional[datetime] = Field(description="Окончание встречи")


class SMeeting(SMeetingBase):
    id: int = Field(description="Идентификатор встречи")
    participants: list

    model_config = ConfigDict(from_attributes=True)


class SMeetingSearch(BaseModel):
    id: int = Field(description="Идентификатор встречи")


class SParticipant(BaseModel):
    user_id: int = Field(description="Идентификатор участника встречи")
    model_config = ConfigDict(from_attributes=True)


class SParticipantSearch(BaseModel):
    id: int = Field(description="Идентификатор участника встречи")
