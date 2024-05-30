from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, URL
from config import settings

config = context.config


if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from apps.sender.models import FastModel
from apps.users.models import FastModel
from apps.generator_base.models import FastModel

target_metadata = FastModel.metadata


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    db_config = settings.DATABASES.copy()
    connectable = create_engine(URL.create(**db_config))

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
