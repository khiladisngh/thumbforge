"""Logging contracts: stream separation, renderer choice, the stdlib bridge, bound context."""

from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING

import pytest

from thumbforge.logging import (
    bind,
    clear_context,
    configure_logging,
    get_logger,
    level_from_flags,
)

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.parametrize(
    ("verbose", "quiet", "configured", "expected"),
    [
        (0, False, "INFO", "INFO"),
        (0, False, "WARNING", "WARNING"),
        (1, False, "WARNING", "INFO"),
        (2, False, "WARNING", "DEBUG"),
        (3, False, "WARNING", "DEBUG"),
        (0, True, "DEBUG", "ERROR"),
        (2, True, "DEBUG", "ERROR"),
    ],
)
def test_flag_to_level_mapping(verbose: int, quiet: bool, configured: str, expected: str) -> None:
    """--quiet outranks -v: an explicit request for silence beats a scripted -v."""
    assert level_from_flags(verbose=verbose, quiet=quiet, configured=configured) == expected


def test_logs_go_to_stderr_never_stdout(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging(level="INFO", fmt="json")
    get_logger("thumbforge.test").info("hello")
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "hello" in captured.err


def test_json_format_emits_parseable_records(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging(level="INFO", fmt="json")
    get_logger("thumbforge.test").warning("disk almost full", free_bytes=17)
    payload = json.loads(capsys.readouterr().err.strip())
    assert payload["event"] == "disk almost full"
    assert payload["level"] == "warning"
    assert payload["free_bytes"] == 17
    assert "timestamp" in payload


def test_level_filters_quieter_records(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging(level="ERROR", fmt="json")
    log = get_logger("thumbforge.test")
    log.info("ignored")
    log.error("reported")
    err = capsys.readouterr().err
    assert "ignored" not in err
    assert "reported" in err


def test_third_party_stdlib_loggers_flow_through_the_pipeline(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """yt_dlp and sqlalchemy use stdlib logging; their records must not bypass our format."""
    configure_logging(level="INFO", fmt="json")
    logging.getLogger("sqlalchemy.engine").warning("SELECT 1")
    payload = json.loads(capsys.readouterr().err.strip())
    assert payload["event"] == "SELECT 1"
    assert payload["logger"] == "sqlalchemy.engine"


def test_bound_context_appears_and_can_be_cleared(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging(level="INFO", fmt="json")
    log = get_logger("thumbforge.test")

    bind(run_id="01J9", provider="fake")
    log.info("started")
    bound = json.loads(capsys.readouterr().err.strip())
    assert bound["run_id"] == "01J9"
    assert bound["provider"] == "fake"

    clear_context()
    log.info("finished")
    unbound = json.loads(capsys.readouterr().err.strip())
    assert "run_id" not in unbound


def test_file_handler_records_debug_regardless_of_console_level(tmp_path: Path) -> None:
    """A failure report should not require the user to reproduce the run with -vv."""
    log_file = tmp_path / "logs" / "thumbforge.log"
    configure_logging(level="ERROR", fmt="console", log_file=log_file)
    get_logger("thumbforge.test").debug("low level detail", step=3)

    lines = [line for line in log_file.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(lines) == 1
    payload = json.loads(lines[0])
    assert payload["event"] == "low level detail"
    assert payload["level"] == "debug"
    assert payload["step"] == 3


def test_reconfiguring_does_not_duplicate_records(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging(level="INFO", fmt="json")
    configure_logging(level="INFO", fmt="json")
    get_logger("thumbforge.test").info("once")
    lines = [line for line in capsys.readouterr().err.splitlines() if line.strip()]
    assert len(lines) == 1


def test_unusable_log_file_degrades_to_console_instead_of_failing(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A read-only state directory must not take the command down."""
    blocker = tmp_path / "logs"
    blocker.write_text("not a directory", encoding="utf-8")  # mkdir here will fail

    configure_logging(level="INFO", fmt="json", log_file=blocker / "thumbforge.log")

    records = [json.loads(line) for line in capsys.readouterr().err.splitlines() if line.strip()]
    assert any(r["event"] == "file logging disabled" for r in records)

    # Console logging still works after the failure.
    get_logger("thumbforge.test").info("still alive")
    assert "still alive" in capsys.readouterr().err


def test_secret_looking_fields_are_redacted(capsys: pytest.CaptureFixture[str]) -> None:
    """Logs land on disk and in bug reports; a key must never survive to a renderer."""
    configure_logging(level="INFO", fmt="json")
    get_logger("thumbforge.test").info(
        "provider call",
        api_key="sk-live-123",
        access_token="tok-abc",
        client_secret="shh",
        db_password="hunter2",
        provider="antigravity",
    )
    payload = json.loads(capsys.readouterr().err.strip())

    assert payload["provider"] == "antigravity"  # ordinary fields survive
    for field in ("api_key", "access_token", "client_secret", "db_password"):
        assert payload[field] == "***redacted***"
    assert "sk-live-123" not in json.dumps(payload)


def test_redaction_also_covers_bound_context(capsys: pytest.CaptureFixture[str]) -> None:
    configure_logging(level="INFO", fmt="json")
    bind(api_key="sk-bound")
    get_logger("thumbforge.test").info("started")
    payload = json.loads(capsys.readouterr().err.strip())
    assert payload["api_key"] == "***redacted***"


def test_redaction_reaches_nested_structures(capsys: pytest.CaptureFixture[str]) -> None:
    """A secret is as likely to arrive inside a settings dump as at the top level."""
    configure_logging(level="INFO", fmt="json")
    get_logger("thumbforge.test").info(
        "provider configured",
        settings={"providers": {"openai": {"api_key": "sk-nested"}}, "width": 1920},
        candidates=[{"access_token": "tok-in-list"}],
    )
    rendered = capsys.readouterr().err
    payload = json.loads(rendered)

    assert "sk-nested" not in rendered
    assert "tok-in-list" not in rendered
    assert payload["settings"]["providers"]["openai"]["api_key"] == "***redacted***"
    assert payload["candidates"][0]["access_token"] == "***redacted***"
    assert payload["settings"]["width"] == 1920
