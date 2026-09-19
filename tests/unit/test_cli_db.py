"""Unit tests for ``thumbforge db`` CLI commands (ADR 0004, Phase 1 spec)."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from typer.testing import CliRunner

from thumbforge.cli.app import app

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()


def test_db_path_command(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    result = runner.invoke(app, ["--data-dir", str(data_dir), "db", "path"])
    assert result.exit_code == 0
    expected_path = data_dir / "thumbforge.sqlite3"
    assert str(expected_path) in result.stdout.replace("\n", "").replace("\r", "")


def test_db_path_json_mode(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    result = runner.invoke(app, ["--json", "--data-dir", str(data_dir), "db", "path"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    expected_path = str(data_dir / "thumbforge.sqlite3")
    assert payload["path"] == expected_path


def test_db_init_creates_database_and_is_idempotent(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    # First init: creates DB and runs migrations
    result1 = runner.invoke(app, ["--data-dir", str(data_dir), "db", "init"])
    assert result1.exit_code == 0
    assert "initialized database at" in result1.stdout
    assert (data_dir / "thumbforge.sqlite3").exists()

    # Second init: reports already at head
    result2 = runner.invoke(app, ["--data-dir", str(data_dir), "db", "init"])
    assert result2.exit_code == 0
    assert "already at head" in result2.stdout


def test_db_init_json_mode(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    result = runner.invoke(app, ["--json", "--data-dir", str(data_dir), "db", "init"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["head_revision"] == "0001"
    assert not payload["already_at_head"]

    result2 = runner.invoke(app, ["--json", "--data-dir", str(data_dir), "db", "init"])
    assert result2.exit_code == 0
    payload2 = json.loads(result2.stdout)
    assert payload2["status"] == "ok"
    assert payload2["already_at_head"]


def test_db_status_command(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    # Status before init
    res_pre = runner.invoke(app, ["--data-dir", str(data_dir), "db", "status"])
    assert res_pre.exit_code == 0
    assert "Pending migrations" in res_pre.stdout

    # Init
    runner.invoke(app, ["--data-dir", str(data_dir), "db", "init"])

    # Status after init
    res_post = runner.invoke(app, ["--data-dir", str(data_dir), "db", "status"])
    assert res_post.exit_code == 0
    assert "0001" in res_post.stdout
    assert "wal" in res_post.stdout.lower()


def test_db_status_json_mode(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    runner.invoke(app, ["--data-dir", str(data_dir), "db", "init"])

    result = runner.invoke(app, ["--json", "--data-dir", str(data_dir), "db", "status"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["current_revision"] == "0001"
    assert payload["head_revision"] == "0001"
    assert payload["pending_count"] == 0
    assert payload["journal_mode"] == "wal"
    assert payload["file_size_bytes"] > 0


def test_db_upgrade_command(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    result = runner.invoke(app, ["--data-dir", str(data_dir), "db", "upgrade"])
    assert result.exit_code == 0
    assert "upgraded database to" in result.stdout


def test_db_upgrade_json_mode(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    result = runner.invoke(app, ["--json", "--data-dir", str(data_dir), "db", "upgrade"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["current_revision"] == "0001"


def test_db_vacuum_command(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    runner.invoke(app, ["--data-dir", str(data_dir), "db", "init"])

    result = runner.invoke(app, ["--data-dir", str(data_dir), "db", "vacuum"])
    assert result.exit_code == 0
    assert "vacuumed and checkpointed" in result.stdout


def test_db_vacuum_json_mode(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    runner.invoke(app, ["--data-dir", str(data_dir), "db", "init"])

    result = runner.invoke(app, ["--json", "--data-dir", str(data_dir), "db", "vacuum"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"


def test_db_vacuum_fails_when_db_missing(tmp_path: Path) -> None:
    data_dir = tmp_path / "nonexistent_dir"
    result = runner.invoke(app, ["--data-dir", str(data_dir), "db", "vacuum"])
    assert result.exit_code == 1
