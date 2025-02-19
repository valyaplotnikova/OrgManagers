from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from task_motivation_service.task_app.exceptions.task_meet_exceptions import MeetingNotFoundException, \
    ParticipantNotFoundException
from task_motivation_service.task_app.models import Meeting
from task_motivation_service.task_app.models.meeteng_model import Participant
from task_motivation_service.task_app.repositories.task_repository import MeetingRepository, ParticipantRepository
from task_motivation_service.task_app.schemas.meeting_schema import SMeetingCreate, SMeetingUpdate, SMeetingSearch
from task_motivation_service.task_app.schemas.meeting_schema import SParticipantSearch, SParticipant


class MeetingService:
    def __init__(self, session: AsyncSession):
        """
        Инициализирует MeetingService с заданной сессией базы данных.

        - **session**: Сессия базы данных, используемая для взаимодействия с репозиторием.
        """
        self.repository = MeetingRepository(session)
        self.participant_repository = ParticipantRepository(session)

    async def create_meeting(self, meeting_data: SMeetingCreate):
        """
        Создает новую встречу в базе данных.

        - **meeting_data**: Данные о встрече, которые будут добавлены.

        Возвращает созданную встречу.
        """

        meeting = await self.repository.add(values=meeting_data)
        return meeting

    async def update_meeting(self, meeting_id: int, meeting_data: SMeetingUpdate) -> None:
        """
        Обновляет существующую встречу по идентификатору.

        - **meeting_id**: Идентификатор встречи, которую нужно обновить.
        - **meeting_data**: Новые данные о встрече.

        Вызывает исключение NoResultFound, если встреча с данным идентификатором не найдена.
        """

        updated_count = await self.repository.update(filters=SMeetingSearch(id=meeting_id), values=meeting_data)
        if updated_count == 0:
            raise MeetingNotFoundException

    async def delete_meeting(self, meeting_id: int) -> None:
        """
        Удаляет встречу по идентификатору.

        - **meeting_id**: Идентификатор встречи, которую нужно удалить.

        Вызывает исключение NoResultFound, если встреча с данным идентификатором не найдена.
        """
        deleted_count = await self.repository.delete(filters=SMeetingSearch(id=meeting_id))
        if deleted_count == 0:
            raise MeetingNotFoundException

    async def get_meeting_by_id(self, meeting_id: int) -> Meeting:
        """
        Получает информацию о встрече по идентификатору.

        - **meeting_id**: Идентификатор встречи, которую нужно получить.

        Возвращает объект Meeting, если встреча найдена.
        Вызывает исключение NoResultFound, если встреча не найдена.
        """
        meeting = await self.repository.find_one_or_none_by_id(meeting_id)
        if not meeting:
            raise MeetingNotFoundException
        return meeting

    async def get_all_meetings(self) -> list[Meeting]:
        """
        Получает список всех встреч.

        Возвращает список объектов Meeting.
        """
        return await self.repository.find_all()


class ParticipantService:
    def __init__(self, session: AsyncSession):
        self.repository = ParticipantRepository(session)

    async def create_participant(self, participant_data: SParticipant):
        """
        Создает нового участника в базе данных.

        - **participant_data**: Данные о участнике, которые будут добавлены.

        Возвращает созданного участника.
        """
        participant = await self.repository.add(values=participant_data)
        return participant

    async def delete_participant(self, participant_id: int) -> None:
        """
        Удаляет участника по идентификатору.

        - **participant_id**: Идентификатор участника, которого нужно удалить.

        Вызывает исключение NoResultFound, если участник с данным идентификатором не найден.
        """
        deleted_count = await self.repository.delete(filters=SParticipantSearch(id=participant_id))
        if deleted_count == 0:
            raise ParticipantNotFoundException

    async def get_participant_by_id(self, participant_id: int) -> Participant:
        """
        Получает информацию об участнике по идентификатору.

        - **participant_id**: Идентификатор участника, которого нужно получить.

        Возвращает объект Participant, если участник найден.
        Вызывает исключение NoResultFound, если участник не найден.
        """
        participant = await self.repository.find_one_or_none_by_id(participant_id)
        if not participant:
            raise ParticipantNotFoundException
        return participant

    async def get_all_participants(self):
        """
        Получает список всех участников.

        Возвращает список объектов Participant.
        """
        return await self.repository.find_all()
