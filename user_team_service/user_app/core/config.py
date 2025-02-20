from pydantic import Extra
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """ Класс настроек для работы проекта. """
    POSTGRES_HOST1: str
    POSTGRES_PORT1: int
    POSTGRES_DB1: str
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
    return (
        f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"
        f"{settings.POSTGRES_HOST1}:{settings.POSTGRES_PORT1}/{settings.POSTGRES_DB1}"
    )


def get_auth_data():
    """
    Получает данные аутентификации, включая секретный ключ и алгоритм.

    :return: Словарь с данными аутентификации, содержащий 'secret_key' и 'algorithm'.
    :rtype: dict
    """
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}


database_url = get_db_url()
