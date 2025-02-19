import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from user_team_service.user_app.models import User


class TaskService:
    def __init__(self, session: AsyncSession):
        """
        Инициализация сервиса задач.

        :param session: Асинхронная сессия базы данных.
        """
        self.session = session
        self.base_url = "http://service2:8002"

    async def get_tasks_for_user(self, current_user: User):
        """
        Получение задач для текущего пользователя.

        :param current_user: Текущий пользователь, для которого нужно получить задачи.
        :return: Список задач, назначенных текущему пользователю.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/tasks/all")
            response.raise_for_status()
            tasks = response.json()
            user_tasks = [task for task in tasks if task["assigned_by"] == current_user.id]

            return user_tasks

    async def update_my_task(self, task_id: int, task_data: dict):
        """
        Обновление задачи по идентификатору.

        :param task_id: Идентификатор задачи, которую нужно обновить.
        :param task_data: Данные для обновления задачи в формате словаря.
        :return: Сообщение об успешном обновлении задачи.
        """
        async with httpx.AsyncClient() as client:
            await client.put(f"{self.base_url}/tasks/update?task_id={task_id}", json=task_data)

            return {'message': 'Задача успешно обновлена!'}

    async def delete_my_task(self, task_id: int):
        """
        Удаление задачи по идентификатору.

        :param task_id: Идентификатор задачи, которую нужно удалить.
        """
        async with httpx.AsyncClient() as client:
            await client.delete(f"{self.base_url}/tasks/delete/{task_id}")

    async def get_my_motivation(self, current_user: User):
        """
        Получение мотивации текущего пользователя на основе его задач.

        :param current_user: Текущий пользователь, для которого нужно получить мотивацию.
        :return: Словарь с оценками мотивации по задачам текущего пользователя.
        """
        res = {}
        my_tasks = await self.get_tasks_for_user(current_user)
        for task in my_tasks:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/motivations/get_by_taskid/{task['id']}")
                if response.status_code == 200:
                    res[f"Task ID {task['id']}"] = response.json()["rating"]

        return res

    async def get_my_quarterly_motivation(self, current_user: User):
        """
        Получение средней оценки мотивации текущего пользователя за квартал.

        :param current_user: Текущий пользователь, для которого нужно получить квартальную мотивацию.
        :return: Словарь с средней оценкой мотивации.
        """
        my_grades = await self.get_my_motivation(current_user)
        if len(my_grades) == 1:
            average = my_grades["Task ID 1"]
        else:
            average = sum(my_grades.values()) / len(my_grades) if my_grades else 0
        return {"Средняя оценка": average}
