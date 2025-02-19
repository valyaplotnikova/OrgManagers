from fastapi import Depends, HTTPException
from sqladmin import ModelView

from user_team_service.user_app.dependencies.auth_dep import get_current_admin_user, get_current_user
from user_team_service.user_app.models import User, Company, Structure, StructureMember, News
from user_team_service.user_app.models.user_model import StatusEnum


class SecureModelView(ModelView):
    async def is_accessible(self, current_user: User = Depends(get_current_admin_user)):
        """Проверяем доступ к админ-панели."""
        if current_user:
            return True
        raise HTTPException(status_code=403, detail="Access forbidden")

    async def inaccessible_callback(self):
        """Обработка недоступности."""
        return {"detail": "Access forbidden"}, 403


class UserAdmin(SecureModelView, model=User):
    column_list = [
        User.first_name,
        User.last_name,
        User.email,
        User.status,
        User.company_id,
        User.news
    ]
    column_searchable_list = [User.email]


class CompanyAdmin(SecureModelView, model=Company):
    column_list = [
        Company.id,
        Company.name,
        Company.users,
        Company.structures
    ]
    column_searchable_list = [Company.name]


class StructureAdmin(SecureModelView, model=Structure):
    column_list = [
        Structure.id,
        Structure.name,
        Structure.company_id,
        Structure.members
    ]


class StructureMemberAdmin(SecureModelView, model=StructureMember):
    column_list = [
        StructureMember.id,
        StructureMember.user_id,
        StructureMember.structure_id,
        StructureMember.role
    ]


class NewsAdmin(SecureModelView, model=News):
    column_list = [
        News.id,
        News.title,
        News.content,
        News.author_id
    ]
    column_searchable_list = [News.title]


