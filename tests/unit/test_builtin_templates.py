"""The shipped built-in templates: valid layouts, prompt goldens, overlay fit (ROADMAP P4.3)."""

from __future__ import annotations

import re
from importlib import resources
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from PIL import Image
from structlog.testing import capture_logs

from thumbforge.core.errors import NotFoundError
from thumbforge.core.models import PlaylistMeta, VideoMeta
from thumbforge.imaging.overlay import overlay
from thumbforge.templates.builtins import BUILTIN_NAMES, builtin_files
from thumbforge.templates.render import RenderContext, render_prompt
from thumbforge.templates.schema import load_layout

if TYPE_CHECKING:
    from collections.abc import Callable

    from thumbforge.core.layout import LayoutSpec

TESTS = Path(__file__).parent.parent
GOLDEN = TESTS / "templates" / "golden"
FLAT_GREY = TESTS / "fixtures" / "imaging" / "flat-grey.png"

NAMES = ("bold-title", "minimal", "series-parts")
TITLE = "Ownership explained"
VIDEO_ID = "dQw4w9WgXcQ"
NO_TEXT = "do not draw any text, lettering, numbers or logos"
# The fixture part number: only the series template is about a numbered part.
PART_NUMBER = {"series-parts": 7}


def _layout(name: str) -> LayoutSpec:
    toml_path, _ = builtin_files(name)
    return load_layout(toml_path)


def _prompt_source(name: str) -> str:
    _, j2_path = builtin_files(name)
    return j2_path.read_text(encoding="utf-8")


def _render(name: str, *, bare: bool = False) -> str:
    """Render the built-in prompt for the fixture video; ``bare`` drops every optional field."""
    layout = _layout(name)
    playlist = PlaylistMeta(
        youtube_id="PL" + "r" * 16, title="Rust from scratch", url="https://yt/pl"
    )
    ctx = RenderContext(
        video=VideoMeta(youtube_id=VIDEO_ID, title=TITLE, url=f"https://youtu.be/{VIDEO_ID}"),
        playlist=None if bare else playlist,
        part_number=None if bare else PART_NUMBER.get(name),
        part_label=None,
        channel=None,
        vars={},
        negative_space=layout.negative_space.hint,
        width=layout.canvas.width,
        height=layout.canvas.height,
    )
    return render_prompt(_prompt_source(name), ctx, name=name)


def test_builtin_names_are_exactly_the_three_shipped_templates() -> None:
    assert BUILTIN_NAMES == NAMES


def test_the_builtin_directory_holds_exactly_a_toml_and_j2_per_name() -> None:
    directory = resources.files("thumbforge.templates") / "builtin"
    shipped = {entry.name for entry in directory.iterdir() if entry.is_file()}
    assert shipped == {f"{name}.{ext}" for name in NAMES for ext in ("toml", "j2")}


@pytest.mark.parametrize("name", NAMES)
def test_builtin_layout_loads_under_its_own_name(name: str) -> None:
    toml_path, j2_path = builtin_files(name)
    assert _layout(name).template.name == name
    assert j2_path.is_file()
    assert toml_path.parent == j2_path.parent


def test_an_unknown_builtin_is_not_found_with_a_hint() -> None:
    with pytest.raises(NotFoundError) as raised:
        builtin_files("nope")
    assert "nope" in raised.value.message
    assert raised.value.hint is not None
    assert all(name in raised.value.hint for name in NAMES)


@pytest.mark.golden
@pytest.mark.parametrize("name", NAMES)
def test_builtin_prompt_golden(name: str, assert_golden_text: Callable[[str, Path], None]) -> None:
    prompt = _render(name)
    assert "{{" not in prompt
    assert "{%" not in prompt
    assert_golden_text(prompt, GOLDEN / f"{name}.txt")


def test_series_parts_prompt_names_the_title_the_part_and_the_negative_space() -> None:
    prompt = _render("series-parts")
    assert TITLE in prompt
    assert "Part 7" in prompt
    assert _layout("series-parts").negative_space.hint in prompt
    assert "{{" not in prompt


@pytest.mark.parametrize("name", NAMES)
def test_prompt_states_size_and_negative_space_and_forbids_painted_text(name: str) -> None:
    # ADR 0008: the title and Part badge are overlaid by Pillow, never painted by the model.
    layout = _layout(name)
    prompt = _render(name)
    assert f"{layout.canvas.width}x{layout.canvas.height}" in prompt
    assert layout.negative_space.hint
    assert layout.negative_space.hint in prompt
    assert NO_TEXT in prompt.lower()


@pytest.mark.parametrize("name", NAMES)
def test_prompt_renders_for_a_bare_video_with_no_vars(name: str) -> None:
    prompt = _render(name, bare=True)
    assert TITLE in prompt
    assert "Rust from scratch" not in prompt
    assert re.search(r"Part \d", prompt) is None
    assert NO_TEXT in prompt.lower()


@pytest.mark.parametrize("name", NAMES)
def test_builtin_layout_overlays_the_fixture_title_without_truncating(name: str) -> None:
    with Image.open(FLAT_GREY) as img:
        grey = img.convert("RGB")
    layout = _layout(name)
    with capture_logs() as logs:
        out = overlay(grey, layout, title=TITLE, part_number=PART_NUMBER.get(name), part_label=None)
    assert out.tobytes() != grey.tobytes()
    assert [e for e in logs if e["event"] == "overlay.title_truncated"] == []
