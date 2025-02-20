from user_team_service.user_app.models import Company, StructureMember, Structure, News
from user_team_service.user_app.repositories.base_repository import BaseRepository


class CompanyRepository(BaseRepository):
    model = Company


class StructureRepository(BaseRepository):
    model = Structure


class StructureMemberRepository(BaseRepository):
    model = StructureMember


class NewsRepository(BaseRepository):
    model = News
