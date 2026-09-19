"""Database engine, session management, and migration execution (PLAN.md §3, ADR 0004)."""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from alembic import command
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy import URL, Engine, create_engine, event, select, text
from sqlalchemy.orm import Session, sessionmaker

from thumbforge.core.errors import DatabaseError
from thumbforge.storage.models import Asset

if TYPE_CHECKING:
    import sqlite3
    from collections.abc import Generator

    from sqlalchemy.pool import ConnectionPoolEntry


MIGRATIONS_DIR = Path(__file__).resolve().parent / "migrations"


def sqlite_url(db_path: Path) -> str:
    """Format a SQLite connection URL for SQLAlchemy."""
    return URL.create("sqlite+pysqlite", database=str(db_path.resolve())).render_as_string(
        hide_password=False
    )


def _set_sqlite_pragmas(
    dbapi_connection: sqlite3.Connection, _connection_record: ConnectionPoolEntry
) -> None:
    """Apply PRAGMA statements required by ADR 0004 on every SQLite connection."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.execute("PRAGMA busy_timeout=5000;")
    cursor.close()


def get_engine(target: Path | str, *, echo: bool = False) -> Engine:
    """Create a SQLAlchemy engine configured for thumbforge SQLite usage."""
    if isinstance(target, str):
        url = (
            "sqlite+pysqlite:///:memory:"
            if target in (":memory:", "sqlite:///:memory:")
            else target
        )
    else:
        url = sqlite_url(target)
    engine = create_engine(
        url,
        echo=echo,
        connect_args={"check_same_thread": False},
    )
    event.listen(engine, "connect", _set_sqlite_pragmas)
    return engine


def session_factory(engine: Engine) -> sessionmaker[Session]:
    """Create a thread-safe sessionmaker bound to ``engine``."""
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


@contextmanager
def session_scope(
    factory_or_engine: sessionmaker[Session] | Engine,
) -> Generator[Session]:
    """Transactional context manager: commits on clean exit, rolls back on error."""
    factory = (
        factory_or_engine
        if isinstance(factory_or_engine, sessionmaker)
        else session_factory(factory_or_engine)
    )
    session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


@dataclass(frozen=True, slots=True)
class DbStatus:
    """Migration status and storage health metadata."""

    current_revision: str | None
    head_revision: str | None
    pending_count: int
    file_size_bytes: int
    journal_mode: str | None

    @property
    def is_at_head(self) -> bool:
        """Whether the database is fully migrated to the latest revision."""
        return (
            self.current_revision is not None
            and self.head_revision is not None
            and self.current_revision == self.head_revision
        )


def _alembic_config(db_path: Path) -> Config:
    """Build an Alembic configuration targeting ``db_path``."""
    cfg = Config()
    cfg.set_main_option("script_location", str(MIGRATIONS_DIR))
    cfg.set_main_option("sqlalchemy.url", sqlite_url(db_path))
    cfg.attributes["skip_logging_config"] = True
    cfg.attributes["target_db_path"] = db_path
    return cfg


def get_db_status(db_path: Path) -> DbStatus:
    """Inspect migration revision and file metadata for ``db_path``."""
    cfg = _alembic_config(db_path)
    script = ScriptDirectory.from_config(cfg)
    head_rev = script.get_current_head()

    if not db_path.exists():
        pending = len(list(script.walk_revisions())) if head_rev else 0
        return DbStatus(
            current_revision=None,
            head_revision=head_rev,
            pending_count=pending,
            file_size_bytes=0,
            journal_mode=None,
        )

    file_size = db_path.stat().st_size
    engine = get_engine(db_path)
    try:
        with engine.connect() as conn:
            journal_mode = conn.execute(text("PRAGMA journal_mode")).scalar()
            context = MigrationContext.configure(conn)
            current_rev = context.get_current_revision()
    except Exception as exc:
        raise DatabaseError(
            f"Failed to inspect database at {db_path}: {exc}",
            hint="verify database file permissions and disk health",
        ) from exc
    finally:
        engine.dispose()

    pending = 0
    if current_rev != head_rev:
        if current_rev is None:
            pending = len(list(script.walk_revisions()))
        else:
            for rev in script.walk_revisions():
                if rev.revision == current_rev:
                    break
                pending += 1

    return DbStatus(
        current_revision=current_rev,
        head_revision=head_rev,
        pending_count=pending,
        file_size_bytes=file_size,
        journal_mode=str(journal_mode).lower() if journal_mode else None,
    )


def init_db(db_path: Path) -> tuple[str, bool]:
    """Ensure directory exists and upgrade DB to head.

    Returns:
        Tuple of (head_revision, already_at_head).
    """
    db_path.parent.mkdir(parents=True, exist_ok=True)
    status = get_db_status(db_path)
    if status.is_at_head and status.head_revision is not None:
        return status.head_revision, True

    upgrade_db(db_path, "head")
    status_after = get_db_status(db_path)
    return status_after.head_revision or "", False


def upgrade_db(db_path: Path, revision: str = "head") -> str:
    """Run Alembic upgrade to ``revision`` on ``db_path``."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    cfg = _alembic_config(db_path)
    try:
        command.upgrade(cfg, revision)
    except Exception as exc:
        raise DatabaseError(
            f"Database migration failed: {exc}",
            hint="check database locks and migration script syntax",
        ) from exc
    status = get_db_status(db_path)
    return status.current_revision or ""


def vacuum_db(db_path: Path) -> int:
    """Reclaim free space, truncate the WAL, and delete unreferenced asset files.

    `AssetStore.put` publishes a file before inserting its row and never unlinks a
    published path, so a crash in between can leave an orphan. Reclaiming those (and
    stale `tmp/` entries) is this command's job per ADR 0011.

    Returns:
        The number of orphaned files removed from ``assets/`` and ``tmp/``.
    """
    if not db_path.exists():
        raise DatabaseError(
            f"Database file does not exist at {db_path}",
            hint="run 'thumbforge db init' to initialize the database",
        )
    engine = get_engine(db_path)
    try:
        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
            conn.execute(text("VACUUM;"))
            conn.execute(text("PRAGMA wal_checkpoint(TRUNCATE);"))
        reclaimed = _reclaim_orphans(engine, db_path.parent)
    except DatabaseError:
        raise
    except Exception as exc:
        raise DatabaseError(
            f"Failed to vacuum database: {exc}",
            hint="ensure no other processes are actively holding database locks",
        ) from exc
    finally:
        engine.dispose()
    return reclaimed


def _reclaim_orphans(engine: Engine, data_dir: Path) -> int:
    """Delete files under ``assets/`` with no ``asset`` row, plus every ``tmp/`` entry."""
    with session_scope(engine) as session:
        referenced = {
            (data_dir / rel_path).resolve() for rel_path in session.scalars(select(Asset.rel_path))
        }

    removed = 0
    assets_dir = data_dir / "assets"
    if assets_dir.is_dir():
        for candidate in assets_dir.rglob("*"):
            if candidate.is_file() and candidate.resolve() not in referenced:
                candidate.unlink(missing_ok=True)
                removed += 1

    tmp_dir = data_dir / "tmp"
    if tmp_dir.is_dir():
        for leftover in tmp_dir.iterdir():
            if leftover.is_file():
                leftover.unlink(missing_ok=True)
                removed += 1
    return removed
