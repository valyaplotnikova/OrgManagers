import logging
import os

from pydantic import Extra
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


settings = Settings()


def get_db_url():
    """
    Формирует строку подключения к базе данных PostgreSQL с использованием asyncpg.

    :return: Строка подключения к базе данных в формате
             'postgresql+asyncpg://<user>:<password>@<host>:<port>/<dbname>'
    :rtype: str
    """
    try:
        return (
            f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"
            f"{settings.POSTGRES_HOST2}:{settings.POSTGRES_PORT2}/{settings.POSTGRES_DB2}"
        )
    except Exception as e:
        logger.error("Error constructing database URL: %s", e)
        raise


def get_auth_data():
    """
    Получает данные аутентификации, включая секретный ключ и алгоритм.

    :return: Словарь с данными аутентификации, содержащий 'secret_key' и 'algorithm'.
    :rtype: dict
    """
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}


database_url = get_db_url()
