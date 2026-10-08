from dotenv import load_dotenv
import os

# .env faylidagi ma'lumotlarni yuklaymiz
load_dotenv()


from logging.config import fileConfig

from sqlalchemy import create_engine
from sqlalchemy import pool

from alembic import context

# O'zimiz yaratgan database Base
from app.database import Base

# O'zimiz yaratgan modellar
from app.models import User


# Alembic konfiguratsiya obyekti
config = context.config


# Logging konfiguratsiyasini yuklaymiz
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Alembic bizning modellarimizni ko'rishi uchun
# Base.metadata ni beramiz
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Database bilan to'g'ridan-to'g'ri ulanmasdan
    migration yaratish rejimi.
    """

    # .env faylidan database manzilini olamiz
    url = os.getenv("DATABASE_URL")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    # Migrationni boshlaymiz
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    PostgreSQL database bilan ulanib,
    migrationlarni ishga tushirish.
    """

    # .env faylidan PostgreSQL manzilini olamiz
    database_url = os.getenv("DATABASE_URL")

    # PostgreSQL bilan ulanish yaratamiz
    connectable = create_engine(
        database_url,
        poolclass=pool.NullPool,
    )

    # Database bilan ulanib olamiz
    with connectable.connect() as connection:

        # Alembic'ga database va modellar haqida ma'lumot beramiz
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        # Migrationni ishga tushiramiz
        with context.begin_transaction():
            context.run_migrations()


# Agar offline rejim bo'lsa
# offline migration ishlaydi
if context.is_offline_mode():
    run_migrations_offline()

# Aks holda online migration ishlaydi
else:
    run_migrations_online()