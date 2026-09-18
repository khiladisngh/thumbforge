# ADR 0004: SQLite via SQLAlchemy 2.0 with Alembic migrations

## Status

`Accepted` — 2026-09-19

## Context

The tool must remember channels, playlists, videos, templates (versioned), provider profiles, runs, iterations and assets across invocations, support resumable batch runs (ADR 0012) and answer queries such as "which iteration of run X is picked". It is a single-user local tool: zero operational burden matters more than throughput, and the schema will evolve across phases.

## Decision

- **SQLite** is the only database. File location: `<data_dir>/thumbforge.db` (ADR 0003).
- Engine in `storage/db.py`: `sqlite+pysqlite`, with `PRAGMA journal_mode=WAL` and `PRAGMA foreign_keys=ON` set on every connection via a `connect` event listener. `check_same_thread=False` so the async batch loop can use a thread-pool session.
- **SQLAlchemy 2.0** declarative ORM in `storage/models.py` (`Mapped[...]` / `mapped_column`, typed). One repository class per aggregate in `storage/repositories.py`; services never touch the session directly.
- Primary keys are `TEXT` ULIDs; every table has `created_at`, `updated_at` as ISO-8601 UTC text; JSON columns are `TEXT`. Enumerations use `CHECK` constraints (`run.kind`, `run.status`, `asset.kind`) as listed in `PLAN.md` §3.
- Referential integrity that encodes business rules lives in the schema: `ON DELETE RESTRICT` on `run.parent_run_id` and `run.reference_asset_id`, `UNIQUE(playlist_id, video_id)` and `UNIQUE(playlist_id, position)` on `playlist_item`, `UNIQUE(name, version)` on `template`, `iteration.idempotency_key UNIQUE`.
- **Alembic** owns schema changes: `storage/migrations/` holds `env.py` and `versions/`; new revisions via `uv run alembic revision --autogenerate -m "…"`. `thumbforge db init` creates the file and upgrades to head; `db upgrade`, `db status`, `db path`, `db vacuum` wrap Alembic and `VACUUM`.
- A migration is required for every ORM change; CI fails when `alembic check` reports drift.

## Consequences

- No server, no credentials, no network; the database file is portable together with `data_dir`.
- WAL allows the CLI to read (`runs show`) while a batch is writing.
- Write concurrency is single-process; that matches the semaphore design in ADR 0012.
- Alembic autogenerate has limits with SQLite `ALTER`; batch-mode (`render_as_batch=True`) is enabled in `env.py`.

## Alternatives considered

- **SQLModel** — rejected: lags SQLAlchemy and Pydantic releases and conflates the persistence model with the boundary model; the project keeps Pydantic models in `core/` and ORM models in `storage/`.
- **Raw `sqlite3` + hand-written SQL** — rejected: no migration tooling, and the nine-table schema with several FKs is error-prone to keep in sync by hand.
- **PostgreSQL / DuckDB** — rejected: a server is unacceptable for a local CLI; DuckDB is analytics-oriented and has no Alembic support.
- **JSON files on disk** — rejected: idempotent resume needs unique constraints and transactional updates.
