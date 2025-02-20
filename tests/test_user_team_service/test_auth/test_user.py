import pytest

from tests.fixtures.users import USERS


@pytest.mark.asyncio
class TestUser:
    @pytest.fixture(autouse=True)
    async def setup(self, authenticated_client, authenticated_client_admin):
        self.client = authenticated_client
        self.client_admin = authenticated_client_admin

    async def test_get_user_for_id(self, add_results):
        await add_results(USERS)

        response = await self.client.get("/users/get/3")
        assert response.status_code == 200
        assert "user@mail.com" == response.json()["email"]

    async def test_update_user(self):

        update_data = {"first_name": "Name", "last_name": "Surname"}
        response = await self.client.put("/users/update", json=update_data)

        assert response.status_code == 200

    async def test_delete_user_admin(self):
        response = await self.client_admin.delete("/users/delete/2")

        assert response.status_code == 200

    async def test_update_status(self):
        response = await self.client_admin.post("/users/update_status?status=ADMIN_GENERAL&user_id=3")

        assert response.status_code == 200


