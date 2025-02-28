from datetime import datetime
from sqlalchemy import TIMESTAMP
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column

from task_motivation_service.task_app.database.database import Base

# Таблица для связи между встречами и участниками
meeting_participant = Table('meeting_participant', Base.metadata,
                            Column('meeting_id', ForeignKey('meetings.id'), primary_key=True),
                            Column('participant_id', ForeignKey('participants.id'), primary_key=True)
                            )


class Meeting(Base):
    organisation_by: Mapped[int]
    start_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True)  # Использует TIMESTAMP WITH TIME ZONE
    )
    end_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True)  # Использует TIMESTAMP WITH TIME ZONE
    )

    participants: Mapped[list] = relationship(
        "Participant",
        secondary=meeting_participant,
        back_populates="meetings"
    )


class Participant(Base):
    user_id: Mapped[int]

    meetings: Mapped[list] = relationship("Meeting", secondary=meeting_participant, back_populates="participants")
