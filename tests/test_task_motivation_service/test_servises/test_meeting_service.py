from datetime import datetime, timezone

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from task_motivation_service.task_app.schemas.meeting_schema import SParticipant
from task_motivation_service.task_app.services.meeting_service import MeetingService, ParticipantService
from task_motivation_service.task_app.schemas.meeting_schema import SMeetingCreate, SMeetingUpdate


@pytest.mark.asyncio
async def test_create_meeting(async_session: AsyncSession, mocked_authenticated_client):
    service = MeetingService(session=async_session)
    meeting_data = SMeetingCreate(organisation_by=1,
                                  start_at=datetime.fromisoformat("2025-10-31T17:00:00").replace(tzinfo=timezone.utc),
                                  end_at=datetime.fromisoformat("2025-10-31T17:30:00").replace(tzinfo=timezone.utc))

    await service.create_meeting(meeting_data)

    created_meeting = await service.get_meeting_by_id(1)

    assert created_meeting.organisation_by == meeting_data.organisation_by
    assert created_meeting.start_at == meeting_data.start_at


@pytest.mark.asyncio
async def test_update_meeting(async_session: AsyncSession, mocked_authenticated_client):
    service = MeetingService(session=async_session)
    meeting_data = SMeetingCreate(organisation_by=1,
                                  start_at=datetime.fromisoformat("2025-10-31T17:00:00").replace(tzinfo=timezone.utc),
                                  end_at=datetime.fromisoformat("2025-10-31T17:30:00").replace(tzinfo=timezone.utc))
    await service.create_meeting(meeting_data)

    update_data = SMeetingUpdate(start_at=datetime.fromisoformat("2025-11-30T17:00:00").replace(tzinfo=timezone.utc),
                                 end_at=datetime.fromisoformat("2025-11-30T17:30:00").replace(tzinfo=timezone.utc))
    await service.update_meeting(2, update_data)

    updated_meeting = await service.get_meeting_by_id(2)
    assert updated_meeting.start_at == update_data.start_at
    assert updated_meeting.end_at == update_data.end_at

    with pytest.raises(HTTPException):
        await service.update_meeting(999, update_data)


@pytest.mark.asyncio
async def test_delete_meeting(async_session: AsyncSession, mocked_authenticated_client):
    service = MeetingService(session=async_session)
    meeting_data = SMeetingCreate(organisation_by=1,
                                  start_at=datetime.fromisoformat("2025-10-31T17:00:00").replace(tzinfo=timezone.utc),
                                  end_at=datetime.fromisoformat("2025-10-31T17:30:00").replace(tzinfo=timezone.utc))
    await service.create_meeting(meeting_data)

    await service.delete_meeting(3)

    with pytest.raises(HTTPException):
        await service.get_meeting_by_id(3)


@pytest.mark.asyncio
async def test_get_all_meetings(async_session: AsyncSession, mocked_authenticated_client):
    service = MeetingService(session=async_session)
    meeting1 = SMeetingCreate(organisation_by=1,
                              start_at=datetime.fromisoformat("2025-10-31T17:00:00").replace(tzinfo=timezone.utc),
                              end_at=datetime.fromisoformat("2025-10-31T17:30:00").replace(tzinfo=timezone.utc))
    meeting2 = SMeetingCreate(organisation_by=1,
                              start_at=datetime.fromisoformat("2025-08-31T17:00:00").replace(tzinfo=timezone.utc),
                              end_at=datetime.fromisoformat("2025-08-31T17:30:00").replace(tzinfo=timezone.utc))

    await service.create_meeting(meeting1)
    await service.create_meeting(meeting2)

    meetings = await service.get_all_meetings()
    assert len(meetings) == 2


@pytest.mark.asyncio
async def test_create_participant(async_session: AsyncSession, mocked_authenticated_client):
    service = ParticipantService(session=async_session)
    meet_service = MeetingService(session=async_session)
    meeting_data = SMeetingCreate(organisation_by=1,
                                  start_at=datetime.fromisoformat("2025-10-31T17:00:00").replace(tzinfo=timezone.utc),
                                  end_at=datetime.fromisoformat("2025-10-31T17:30:00").replace(tzinfo=timezone.utc))
    await meet_service.create_meeting(meeting_data)
    await meet_service.get_meeting_by_id(6)
    participant_data = SParticipant(user_id=1)  # Убираем meeting_id

    # Создание участника
    created_participant = await service.create_participant(participant_data)
    assert created_participant.user_id == participant_data.user_id


@pytest.mark.asyncio
async def test_delete_participant(async_session: AsyncSession, mocked_authenticated_client):
    service = ParticipantService(session=async_session)
    participant_data = SParticipant(user_id=1)
    await service.create_participant(participant_data)

    await service.delete_participant(2)

    with pytest.raises(HTTPException):
        await service.get_participant_by_id(2)


@pytest.mark.asyncio
async def test_get_all_participants(async_session: AsyncSession, mocked_authenticated_client):
    service = ParticipantService(session=async_session)
    participant1 = SParticipant(user_id=1)
    participant2 = SParticipant(user_id=2)

    await service.create_participant(participant1)
    await service.create_participant(participant2)

    participants = await service.get_all_participants()
    assert len(participants) == 2


