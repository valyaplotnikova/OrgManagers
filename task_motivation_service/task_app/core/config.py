import logging

from pydantic import Extra, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """ Класс настроек для работы проекта. """
    POSTGRES_HOST2: str
    POSTGRES_PORT2: int
    POSTGRES_DB2: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file=(".env", ".test.env"),
        extra=Extra.allow
    )


try:
    settings = Settings()
except ValidationError as e:
    print("Ошибка валидации:", e)

# Проверка на наличие необходимых переменных
required_variables = [
    'POSTGRES_HOST1', 'POSTGRES_PORT1', 'POSTGRES_DB1',
    'POSTGRES_USER', 'POSTGRES_PASSWORD',
    'POSTGRES_HOST2', 'POSTGRES_PORT2', 'POSTGRES_DB2'
]

missing_variables = [var for var in required_variables if not hasattr(settings, var)]

if missing_variables:
    print(f"Отсутствуют обязательные переменные: {', '.join(missing_variables)}")
else:
    print("Все необходимые переменные загружены успешно.")


def get_db_url():
    """
    Формирует строку подключения к базе данных PostgreSQL с использованием asyncpg.

    :return: Строка подключения к базе данных в формате
             'postgresql+asyncpg://<user>:<password>@<host>:<port>/<dbname>'
    :rtype: str
    """
    # Проверка на наличие значений
    if not all([settings.POSTGRES_USER, settings.POSTGRES_PASSWORD, settings.POSTGRES_HOST2, settings.POSTGRES_PORT2,
                settings.POSTGRES_DB2]):
        logger.error("Необходимые параметры для формирования URL базы данных отсутствуют.")
        raise ValueError("Необходимые параметры для формирования URL базы данных отсутствуют.")

    db_url = (
        f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"
        f"{settings.POSTGRES_HOST2}:{settings.POSTGRES_PORT2}/{settings.POSTGRES_DB2}"
    )

    logger.debug("Сформирован URL базы данных: %s", db_url)
    return db_url


def get_auth_data():
    def get_auth_data(log_sensitive=False):
        """
        Получает данные аутентификации, включая секретный ключ и алгоритм.

        :param log_sensitive: Если True, позволяет логировать чувствительные данные.
                              По умолчанию False для защиты конфиденциальной информации.
        :return: Словарь с данными аутентификации, содержащий 'secret_key' и 'algorithm'.
        :rtype: dict
        """
        auth_data = {
            "algorithm": settings.ALGORITHM,
        }

        if log_sensitive:
            # Логируем секретный ключ только в безопасном контексте
            logger.debug("Доступ к секретному ключу: %s", settings.SECRET_KEY)
            auth_data["secret_key"] = settings.SECRET_KEY

        return auth_data


database_url = get_db_url()
