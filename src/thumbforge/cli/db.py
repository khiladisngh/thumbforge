"""``thumbforge db`` — database lifecycle and migration management (ADR 0004)."""

from __future__ import annotations

from typing import Annotated

import typer

from thumbforge.cli._errors import handle_errors
from thumbforge.cli._render import emit, get_app_context, kv
from thumbforge.storage.db import (
    ORPHAN_GRACE_SECONDS,
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


_context = get_app_context


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
            "path": str(db_path),
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
                "Status": "current == head" if db_status.is_at_head else "pending upgrades",
                "Pending migrations": f"pending: {db_status.pending_count}",
                "Journal mode": f"journal_mode = {db_status.journal_mode or 'none'}",
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
        soft_wrap=True,
    )


@app.command("vacuum")
@handle_errors
def vacuum(
    ctx: typer.Context,
    grace_seconds: Annotated[
        float,
        typer.Option(
            "--grace-seconds",
            help="Only reclaim unreferenced files untouched for this long (seconds).",
        ),
    ] = ORPHAN_GRACE_SECONDS,
) -> None:
    """Reclaim unused disk space, checkpoint the WAL, and delete orphaned asset files."""
    app_ctx = _context(ctx)
    settings = app_ctx.require_settings()
    db_path = settings.db_path

    reclaimed = vacuum_db(db_path, grace_seconds=grace_seconds)
    emit(
        app_ctx,
        {"status": "ok", "path": str(db_path), "reclaimed_files": reclaimed},
        render=lambda: (
            f"[green]vacuumed and checkpointed[/] {db_path} "
            f"([cyan]{reclaimed}[/] reclaimed file(s))"
        ),
    )
