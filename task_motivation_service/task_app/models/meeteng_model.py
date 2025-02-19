from datetime import datetime, timezone
from sqlalchemy import TIMESTAMP, func
from sqlalchemy import Column, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column

from task_motivation_service.task_app.database.database import Base

# Таблица для связи между встречами и участниками
meeting_participant = Table('meeting_participant', Base.metadata,
                            Column('meeting_id', ForeignKey('meetings.id'), primary_key=True),
                            Column('participant_id', ForeignKey('participants.id'), primary_key=True)
                            )


class Meeting(Base):
    organisation_by: Mapped[int]
    start_at: Mapped[datetime] = mapped_column(DateTime)
    end_at: Mapped[datetime] = mapped_column(DateTime)
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
    participants: Mapped[list] = relationship(
        "Participant",
        secondary=meeting_participant,
        back_populates="meetings"
    )


class Participant(Base):
    user_id: Mapped[int]
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
    meetings: Mapped[list] = relationship("Meeting", secondary=meeting_participant, back_populates="participants")
