import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config, create_async_engine

from alembic import context

from task_motivation_service.task_app.core.config import get_db_url

from task_motivation_service.task_app.models.task_model import Task  # import Task for registry at alembic

from task_motivation_service.task_app.database.database import Base

config = context.config

# Интерпретируем конфигурационный файл для Python логирования.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# добавьте объект MetaData вашей модели здесь
# для поддержки 'autogenerate'
target_metadata = Base.metadata

# Получаем URL базы данных
database_url = get_db_url()

# Устанавливаем основной параметр конфигурации
config.set_main_option("sqlalchemy.url", database_url)

# Проверяем, установлен ли database_url корректно
if not database_url:
    raise ValueError("Database URL is not set. Please check your configuration.")

# Создаем асинхронный движок
connectable = create_async_engine(database_url, echo=False)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    try:
        with context.begin_transaction():
            context.run_migrations()
    except Exception as e:
        print(f"Error during offline migrations: {e}")
        raise


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_async_migrations())
    except Exception as e:
        print(f"Error during online migrations: {e}")
        raise


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
