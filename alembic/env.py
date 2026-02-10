from logging.config import fileConfig
import os

from sqlalchemy import engine_from_config, pool
from alembic import context

# ------------------------------------------------------------------
# Alembic Config
# ------------------------------------------------------------------
config = context.config

# DATABASE_URL aus docker-compose / env
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise RuntimeError("DATABASE_URL environment variable is not set")

config.set_main_option("sqlalchemy.url", database_url)

# Logging konfigurieren
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ------------------------------------------------------------------
# Models / Metadata
# ------------------------------------------------------------------
# WICHTIG:
# - Base importieren
# - ALLE ORM-Models importieren, damit Alembic sie kennt
from app.db.base import Base  # noqa: E402
from app.models.user import User  # noqa: F401, E402

target_metadata = Base.metadata

# ------------------------------------------------------------------
# Offline migrations
# ------------------------------------------------------------------
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# ------------------------------------------------------------------
# Online migrations
# ------------------------------------------------------------------
def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# ------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()