"""The CLI never crashes on non-ASCII text when stdout and stderr are not a console.

Python encodes a redirected stream with the locale code page (cp1252 on Windows), and Rich writes
text to it unchanged, so a Devanagari title or the ``✔`` of a run table used to end in a
``UnicodeEncodeError`` traceback after the work had already completed. These tests run the real
CLI as a subprocess with both streams piped and the encoding forced to a narrow one, which is the
same failure class on every OS, and read back the raw bytes.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from typing import TYPE_CHECKING

import pytest
from typer.testing import CliRunner

from thumbforge.cli._youtube import open_repositories
from thumbforge.cli.app import app
from thumbforge.core.errors import ExitCode
from thumbforge.core.models import VideoMeta

if TYPE_CHECKING:
    from pathlib import Path

runner = CliRunner()
VIDEO = "HiNdI123456"
TITLE = "हिंदी में थंबनेल"
ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
NARROW = ["ascii", "cp1252"]


@pytest.fixture
def data_dir(tmp_path: Path) -> Path:
    directory = tmp_path / "data"
    assert runner.invoke(app, ["--data-dir", str(directory), "db", "init"]).exit_code == 0
    with open_repositories(directory / "thumbforge.sqlite3") as repos:
        repos.store_video(
            VideoMeta(
                youtube_id=VIDEO,
                title=TITLE,
                url=f"https://www.youtube.com/watch?v={VIDEO}",
            )
        )
    return directory


def _cli(
    tmp_path: Path, data_dir: Path, *args: str, encoding: str = "cp1252"
) -> subprocess.CompletedProcess[bytes]:
    """Run the real CLI with stdout and stderr piped through a stream of ``encoding``.

    User directories are redirected into ``tmp_path`` so the child never reads or writes the
    developer's own configuration, logs or database.
    """
    home = tmp_path / "child-home"
    home.mkdir(exist_ok=True)
    config = home / "config.toml"
    config.write_text("", encoding="utf-8")
    env = {key: value for key, value in os.environ.items() if not key.startswith("THUMBFORGE_")}
    env.update(
        HOME=str(home),
        USERPROFILE=str(home),
        WIN_PD_OVERRIDE_APPDATA=str(home / "appdata"),
        WIN_PD_OVERRIDE_LOCAL_APPDATA=str(home / "localappdata"),
        XDG_CONFIG_HOME=str(home / "xdg-config"),
        XDG_DATA_HOME=str(home / "xdg-data"),
        XDG_STATE_HOME=str(home / "xdg-state"),
        PYTHONIOENCODING=encoding,
        PYTHONUTF8="0",
    )
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "thumbforge",
            "--config",
            str(config),
            "--data-dir",
            str(data_dir),
            *args,
        ],
        capture_output=True,
        env=env,
        check=False,
        timeout=180,
    )


def _text(raw: bytes) -> str:
    """Decode captured bytes as UTF-8 (strictly) and drop colour codes."""
    return ANSI.sub("", raw.decode("utf-8"))


@pytest.mark.parametrize("encoding", NARROW)
def test_generate_prints_the_run_table_as_utf8(
    tmp_path: Path, data_dir: Path, encoding: str
) -> None:
    result = _cli(
        tmp_path,
        data_dir,
        "-v",
        "thumb",
        "generate",
        VIDEO,
        "--provider",
        "fake",
        "--n",
        "2",
        encoding=encoding,
    )

    assert result.returncode == ExitCode.OK, result.stderr.decode("utf-8", "replace")
    assert b"Traceback" not in result.stderr
    stdout = _text(result.stdout)
    assert stdout.count("✔") == 2
    assert "✔".encode() in result.stdout
    assert "Pick one with: thumbforge thumb pick" in stdout


@pytest.mark.parametrize("encoding", NARROW)
def test_a_listing_round_trips_the_title_as_utf8(
    tmp_path: Path, data_dir: Path, encoding: str
) -> None:
    result = _cli(tmp_path, data_dir, "video", "list", encoding=encoding)

    assert result.returncode == ExitCode.OK, result.stderr.decode("utf-8", "replace")
    assert result.stderr == b""
    assert TITLE in _text(result.stdout)
    assert TITLE.encode() in result.stdout


@pytest.mark.parametrize("encoding", NARROW)
def test_json_output_stays_valid_json_with_the_title(
    tmp_path: Path, data_dir: Path, encoding: str
) -> None:
    result = _cli(tmp_path, data_dir, "--json", "video", "list", encoding=encoding)

    assert result.returncode == ExitCode.OK, result.stderr.decode("utf-8", "replace")
    payload = json.loads(result.stdout.decode("utf-8"))
    assert [video["title"] for video in payload["videos"]] == [TITLE]


@pytest.mark.parametrize("encoding", NARROW)
def test_an_error_naming_non_ascii_text_keeps_its_exit_code(
    tmp_path: Path, data_dir: Path, encoding: str
) -> None:
    result = _cli(
        tmp_path, data_dir, "thumb", "generate", VIDEO, "--template", TITLE, encoding=encoding
    )

    assert result.returncode == ExitCode.NOT_FOUND
    assert b"Traceback" not in result.stderr
    assert TITLE in _text(result.stderr)


def test_help_and_version_survive_a_narrow_pipe(tmp_path: Path, data_dir: Path) -> None:
    for args in (["--help"], ["--version"], ["thumb", "--help"]):
        result = _cli(tmp_path, data_dir, *args, encoding="ascii")

        assert result.returncode == ExitCode.OK, (args, result.stderr.decode("utf-8", "replace"))
        assert b"Traceback" not in result.stderr


def test_a_utf8_environment_prints_the_same_bytes(tmp_path: Path, data_dir: Path) -> None:
    narrow = _cli(tmp_path, data_dir, "video", "list", encoding="ascii")
    utf8 = _cli(tmp_path, data_dir, "video", "list", encoding="utf-8")

    assert narrow.returncode == utf8.returncode == ExitCode.OK
    assert narrow.stdout == utf8.stdout
