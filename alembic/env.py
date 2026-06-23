from logging.config import fileConfig
import os
import sys

# ensure project root is on sys.path so `app` package can be imported
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# import your app's metadata and models so `autogenerate` works
from app.db import Base
import app.models.resident  # noqa: F401
import app.models.user  # noqa: F401
import app.models.role  # noqa: F401

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging. If the logging sections
# are incomplete, avoid failing: fall back to basic logging.
if config.config_file_name is not None:
    try:
        fileConfig(config.config_file_name)
    except Exception:
        # some alembic.ini files may omit specific logger sections
        # fall back to default logging configuration and continue
        import logging

        logging.basicConfig()

# set sqlalchemy.url from environment if provided
db_url = os.getenv("DATABASE_URL")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)

# set target metadata for 'autogenerate'
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    cfg_section = config.get_section(config.config_ini_section)
    if "sqlalchemy.url" not in cfg_section:
        raise RuntimeError(
            "Database URL not configured. Set DATABASE_URL env var or add 'sqlalchemy.url' to alembic.ini."
        )
    connectable = engine_from_config(
        cfg_section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
