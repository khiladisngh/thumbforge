"""Unit tests for thumbforge.templates.schema (ROADMAP P4.1, phase-4 spec)."""

from __future__ import annotations

from pathlib import Path

import pytest

from thumbforge.core.errors import ExitCode, TemplateError
from thumbforge.core.layout import LayoutSpec
from thumbforge.templates.builtins import BUILTIN_NAMES, builtin_files
from thumbforge.templates.schema import dump_layout, load_layout

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures" / "templates"


def test_load_layout_valid_fixture() -> None:
    path = FIXTURES_DIR / "valid.toml"
    spec = load_layout(path)
    assert isinstance(spec, LayoutSpec)
    assert spec.template.name == "bold-title"
    assert spec.canvas.width == 1920
    assert spec.title.box.x == 64


def test_load_layout_bad_anchor_fixture() -> None:
    path = FIXTURES_DIR / "bad-anchor.toml"
    with pytest.raises(TemplateError) as exc_info:
        load_layout(path)
    err = exc_info.value
    assert err.exit_code == ExitCode.USAGE
    assert "title.anchor" in err.message


def test_load_layout_nonexistent_file(tmp_path: Path) -> None:
    path = tmp_path / "nonexistent.toml"
    with pytest.raises(TemplateError) as exc_info:
        load_layout(path)
    err = exc_info.value
    assert err.exit_code == ExitCode.USAGE
    assert "nonexistent.toml" in err.message


def test_a_directory_is_a_template_error(tmp_path: Path) -> None:
    with pytest.raises(TemplateError):
        load_layout(tmp_path)


def test_a_non_utf8_file_is_a_template_error(tmp_path: Path) -> None:
    latin1 = tmp_path / "latin1.toml"
    latin1.write_bytes('[template]\nname = "café"\n'.encode("latin-1"))
    with pytest.raises(TemplateError) as exc_info:
        load_layout(latin1)
    assert "latin1.toml" in exc_info.value.message


def test_load_layout_malformed_toml(tmp_path: Path) -> None:
    bad_toml = tmp_path / "syntax_error.toml"
    bad_toml.write_text("[template\nname = unclosed string", encoding="utf-8")
    with pytest.raises(TemplateError) as exc_info:
        load_layout(bad_toml)
    err = exc_info.value
    assert err.exit_code == ExitCode.USAGE
    assert "syntax_error.toml" in err.message


def test_load_layout_reports_every_error_at_once(tmp_path: Path) -> None:
    multi_error_toml = tmp_path / "multi_error.toml"
    multi_error_toml.write_text(
        """
[template]
name = ""

[canvas]
width = -100
height = 1080

[title]
enabled = true
font = "Inter"
max_lines = 1
size_px = 50
min_size_px = 100
color = "not-a-color"
stroke_px = 0
stroke_color = "#000000"
anchor = "invalid-anchor"
box = { x = 0, y = 0, w = 100, h = 100 }
case = "invalid-case"

[part]
enabled = false
font = "Inter"
size_px = 10

[negative_space]
hint = ""
""",
        encoding="utf-8",
    )
    with pytest.raises(TemplateError) as exc_info:
        load_layout(multi_error_toml)
    msg = exc_info.value.message
    # Check that multiple dotted locations are reported in the single error message
    assert "template.name" in msg
    assert "canvas.width" in msg
    assert "title.min_size_px" in msg
    assert "title.color" in msg
    assert "title.anchor" in msg
    assert "title.case" in msg


@pytest.mark.parametrize("name", BUILTIN_NAMES)
def test_dump_layout_round_trips_through_load_layout(name: str, tmp_path: Path) -> None:
    original = load_layout(builtin_files(name)[0])
    emitted = tmp_path / "emitted.toml"
    emitted.write_text(dump_layout(original), encoding="utf-8")
    assert load_layout(emitted) == original


def test_dump_layout_omits_unset_optional_blocks() -> None:
    """TOML has no null: an absent badge must be left out, not written as an empty value."""
    layout = load_layout(builtin_files("minimal")[0])
    assert layout.part.badge is None
    assert "badge" not in dump_layout(layout)
