from typing import List

from user_team_service.user_app.schemas.auth_schemas import SUserAddDBTest

USERS: List[SUserAddDBTest] = [
    SUserAddDBTest(id=1,
                   first_name="Test User",
                   last_name="Testov",
                   email="test@mail.com",
                   password="123qaz",
                   status="USER"),
    SUserAddDBTest(id=2,
                   first_name="Admin",
                   last_name="Adminov",
                   email="admin@mail.com",
                   password="zxc123",
                   status="ADMIN_GROUP"),
]
