"""Unit tests for database engine, pragmas, sessions, and status helpers (ADR 0004)."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from sqlalchemy import text

from thumbforge.core.enums import ChannelSource
from thumbforge.core.errors import DatabaseError
from thumbforge.storage.db import (
    get_db_status,
    get_engine,
    init_db,
    session_factory,
    session_scope,
    sqlite_url,
    upgrade_db,
    vacuum_db,
)
from thumbforge.storage.models import Channel

if TYPE_CHECKING:
    from pathlib import Path


def test_sqlite_url_formats_path(tmp_path: Path) -> None:
    p = tmp_path / "test.sqlite3"
    url = sqlite_url(p)
    assert url.startswith("sqlite+pysqlite:///")
    assert "test.sqlite3" in url


def test_engine_pragmas_on_file(tmp_path: Path) -> None:
    db_file = tmp_path / "pragmas.sqlite3"
    engine = get_engine(db_file)
    try:
        with engine.connect() as conn:
            fk = conn.execute(text("PRAGMA foreign_keys;")).scalar()
            to = conn.execute(text("PRAGMA busy_timeout;")).scalar()
            jm = conn.execute(text("PRAGMA journal_mode;")).scalar()

            assert fk == 1
            assert to == 5000
            assert str(jm).lower() == "wal"
    finally:
        engine.dispose()


def test_engine_pragmas_on_memory() -> None:
    engine = get_engine(":memory:")
    try:
        with engine.connect() as conn:
            fk = conn.execute(text("PRAGMA foreign_keys;")).scalar()
            to = conn.execute(text("PRAGMA busy_timeout;")).scalar()
            jm = conn.execute(text("PRAGMA journal_mode;")).scalar()

            assert fk == 1
            assert to == 5000
            assert str(jm).lower() == "memory"
    finally:
        engine.dispose()


def test_session_scope_commits_on_success(tmp_path: Path) -> None:
    db_file = tmp_path / "commit.sqlite3"
    init_db(db_file)
    engine = get_engine(db_file)
    factory = session_factory(engine)

    try:
        with session_scope(factory) as session:
            channel = Channel(
                youtube_id="UC12345",
                title="Test Channel",
                url="https://youtube.com/@test",
                source=ChannelSource.YTDLP,
            )
            session.add(channel)

        with session_scope(factory) as session:
            saved = session.query(Channel).filter_by(youtube_id="UC12345").one()
            assert saved.title == "Test Channel"
            assert saved.id is not None
    finally:
        engine.dispose()


def test_session_scope_rolls_back_on_error(tmp_path: Path) -> None:
    db_file = tmp_path / "rollback.sqlite3"
    init_db(db_file)
    engine = get_engine(db_file)
    factory = session_factory(engine)

    try:
        with (
            pytest.raises(RuntimeError, match="deliberate failure"),
            session_scope(factory) as session,
        ):
            channel = Channel(
                youtube_id="UC99999",
                title="Rollback Channel",
                url="https://youtube.com/@rollback",
                source=ChannelSource.YTDLP,
            )
            session.add(channel)
            raise RuntimeError("deliberate failure")

        with session_scope(factory) as session:
            assert session.query(Channel).filter_by(youtube_id="UC99999").first() is None
    finally:
        engine.dispose()


def test_init_db_and_idempotence(tmp_path: Path) -> None:
    db_file = tmp_path / "init.sqlite3"

    rev1, already_at_head1 = init_db(db_file)
    assert rev1 == "0001"
    assert not already_at_head1
    assert db_file.exists()

    rev2, already_at_head2 = init_db(db_file)
    assert rev2 == "0001"
    assert already_at_head2


def test_get_db_status_nonexistent_and_initialized(tmp_path: Path) -> None:
    db_file = tmp_path / "status.sqlite3"

    status_pre = get_db_status(db_file)
    assert status_pre.current_revision is None
    assert status_pre.head_revision == "0001"
    assert status_pre.pending_count == 1
    assert status_pre.file_size_bytes == 0
    assert status_pre.journal_mode is None
    assert not status_pre.is_at_head

    init_db(db_file)

    status_post = get_db_status(db_file)
    assert status_post.current_revision == "0001"
    assert status_post.head_revision == "0001"
    assert status_post.pending_count == 0
    assert status_post.file_size_bytes > 0
    assert status_post.journal_mode == "wal"
    assert status_post.is_at_head


def test_upgrade_db_on_fresh_file(tmp_path: Path) -> None:
    db_file = tmp_path / "upgrade.sqlite3"
    rev = upgrade_db(db_file, "head")
    assert rev == "0001"
    status = get_db_status(db_file)
    assert status.is_at_head


def test_vacuum_db_success_and_missing_error(tmp_path: Path) -> None:
    db_file = tmp_path / "vacuum.sqlite3"
    with pytest.raises(DatabaseError, match="does not exist"):
        vacuum_db(db_file)

    init_db(db_file)
    vacuum_db(db_file)
    assert db_file.exists()
