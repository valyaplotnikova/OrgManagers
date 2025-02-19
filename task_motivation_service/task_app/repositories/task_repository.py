from task_motivation_service.task_app.models import Task
from task_motivation_service.task_app.models.meeteng_model import Meeting, Participant
from task_motivation_service.task_app.models.motivation_model import Motivation
from task_motivation_service.task_app.repositories.base_repository import BaseRepository


class TaskRepository(BaseRepository):
    model = Task


class MotivationRepository(BaseRepository):
    model = Motivation


class MeetingRepository(BaseRepository):
    model = Meeting


class ParticipantRepository(BaseRepository):
    model = Participant
