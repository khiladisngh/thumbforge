"""Database engine, session management, and migration execution (PLAN.md §3, ADR 0004)."""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from alembic import command
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy import Engine, create_engine, event, text
from sqlalchemy.orm import Session, sessionmaker

from thumbforge.core.errors import DatabaseError

if TYPE_CHECKING:
    from collections.abc import Generator

MIGRATIONS_DIR = Path(__file__).resolve().parent / "migrations"


def sqlite_url(db_path: Path | str) -> str:
    """Format a SQLite connection URL for SQLAlchemy."""
    if isinstance(db_path, str):
        if db_path in (":memory:", "sqlite:///:memory:"):
            return "sqlite+pysqlite:///:memory:"
        if db_path.startswith("sqlite"):
            return db_path
        db_path = Path(db_path)
    return f"sqlite+pysqlite:///{db_path.resolve().as_posix()}"


def _set_sqlite_pragmas(dbapi_connection: Any, _connection_record: Any) -> None:
    """Apply PRAGMA statements required by ADR 0004 on every SQLite connection."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.execute("PRAGMA busy_timeout=5000;")
    cursor.close()


def get_engine(db_path: Path | str, *, echo: bool = False) -> Engine:
    """Create a SQLAlchemy engine configured for thumbforge SQLite usage."""
    url = sqlite_url(db_path)
    engine = create_engine(
        url,
        echo=echo,
        future=True,
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
        raise DatabaseError(f"Failed to inspect database at {db_path}: {exc}") from exc
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
        raise DatabaseError(f"Database migration failed: {exc}") from exc
    status = get_db_status(db_path)
    return status.current_revision or ""


def vacuum_db(db_path: Path) -> None:
    """Reclaim free space and truncate the WAL file."""
    if not db_path.exists():
        raise DatabaseError(
            f"Database file does not exist at {db_path}",
            hint="run 'thumbforge db init' to initialize the database",
        )
    engine = get_engine(db_path)
    try:
        with engine.connect() as conn:
            conn.execute(text("VACUUM;"))
            conn.execute(text("PRAGMA wal_checkpoint(TRUNCATE);"))
    except Exception as exc:
        raise DatabaseError(f"Failed to vacuum database: {exc}") from exc
    finally:
        engine.dispose()
