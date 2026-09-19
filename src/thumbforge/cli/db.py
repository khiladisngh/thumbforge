"""``thumbforge db`` — database lifecycle and migration management (ADR 0004)."""

from __future__ import annotations

import typer

from thumbforge.cli._errors import handle_errors
from thumbforge.cli._render import AppContext, emit, kv
from thumbforge.core.errors import SettingsError
from thumbforge.storage.db import (
    get_db_status,
    init_db,
    upgrade_db,
    vacuum_db,
)

app = typer.Typer(
    name="db",
    help="Manage the SQLite database and Alembic migrations.",
    no_args_is_help=True,
)


def _context(ctx: typer.Context) -> AppContext:
    obj = ctx.obj
    if not isinstance(obj, AppContext):  # pragma: no cover
        msg = "CLI context was not initialised"
        raise SettingsError(msg)
    return obj


@app.command("init")
@handle_errors
def init_(ctx: typer.Context) -> None:
    """Create the database file and upgrade schema to Alembic head."""
    app_ctx = _context(ctx)
    settings = app_ctx.require_settings()
    db_path = settings.db_path

    head_rev, already_at_head = init_db(db_path)
    emit(
        app_ctx,
        {
            "status": "ok",
            "path": str(db_path),
            "head_revision": head_rev,
            "already_at_head": already_at_head,
        },
        render=lambda: (
            f"[yellow]database already at head[/] ({head_rev})"
            if already_at_head
            else f"[green]initialized database at[/] {db_path} ([cyan]{head_rev}[/])"
        ),
    )


@app.command("upgrade")
@handle_errors
def upgrade(ctx: typer.Context) -> None:
    """Apply pending Alembic migrations up to head."""
    app_ctx = _context(ctx)
    settings = app_ctx.require_settings()
    db_path = settings.db_path

    current_rev = upgrade_db(db_path, "head")
    emit(
        app_ctx,
        {"status": "ok", "current_revision": current_rev, "path": str(db_path)},
        render=lambda: f"[green]upgraded database to[/] [cyan]{current_rev}[/]",
    )


@app.command("status")
@handle_errors
def status(ctx: typer.Context) -> None:
    """Print current revision, head revision, pending count, file size, and journal mode."""
    app_ctx = _context(ctx)
    settings = app_ctx.require_settings()
    db_path = settings.db_path

    db_status = get_db_status(db_path)
    emit(
        app_ctx,
        {
            "current_revision": db_status.current_revision,
            "head_revision": db_status.head_revision,
            "pending_count": db_status.pending_count,
            "file_size_bytes": db_status.file_size_bytes,
            "journal_mode": db_status.journal_mode,
        },
        render=lambda: kv(
            {
                "Database": str(db_path),
                "Current revision": db_status.current_revision or "none",
                "Head revision": db_status.head_revision or "none",
                "Pending migrations": str(db_status.pending_count),
                "Journal mode": db_status.journal_mode or "none",
                "File size": f"{db_status.file_size_bytes} bytes",
            }
        ),
    )


@app.command("path")
@handle_errors
def path_(ctx: typer.Context) -> None:
    """Print the SQLite database file path."""
    app_ctx = _context(ctx)
    settings = app_ctx.require_settings()
    db_path = settings.db_path

    emit(
        app_ctx,
        {"path": str(db_path)},
        render=lambda: str(db_path),
    )


@app.command("vacuum")
@handle_errors
def vacuum(ctx: typer.Context) -> None:
    """Reclaim unused disk space and checkpoint the Write-Ahead Log (WAL)."""
    app_ctx = _context(ctx)
    settings = app_ctx.require_settings()
    db_path = settings.db_path

    vacuum_db(db_path)
    emit(
        app_ctx,
        {"status": "ok", "path": str(db_path)},
        render=lambda: f"[green]vacuumed and checkpointed[/] {db_path}",
    )
