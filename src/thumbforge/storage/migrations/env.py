"""Alembic environment configuration for thumbforge (ADR 0004)."""

from __future__ import annotations

from alembic import context

from thumbforge.settings import load_settings
from thumbforge.storage.db import get_engine, sqlite_url
from thumbforge.storage.models import Base

config = context.config


target_metadata = Base.metadata


def get_url() -> str:
    """Resolve database URL from config options or active thumbforge settings."""
    url = config.get_main_option("sqlalchemy.url")
    if url:
        return url
    target_path = config.attributes.get("target_db_path")
    if target_path is not None:
        return sqlite_url(target_path)
    settings = load_settings()
    return sqlite_url(settings.db_path)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode with SQL script output."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode against a live database."""
    connection = config.attributes.get("connection")
    if connection is not None:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,
        )
        with context.begin_transaction():
            context.run_migrations()
        return

    connectable = get_engine(get_url())
    try:
        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                render_as_batch=True,
            )
            with context.begin_transaction():
                context.run_migrations()
    finally:
        connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
