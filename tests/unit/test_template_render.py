"""Prompt rendering: the Jinja environment and ``thumbforge template render`` (ROADMAP P4.2)."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

import pytest
from typer.testing import CliRunner

from thumbforge.cli import fetch as fetch_cli
from thumbforge.cli.app import app
from thumbforge.core.errors import ExitCode, TemplateError
from thumbforge.core.models import (
    ChannelMeta,
    PlaylistItemMeta,
    PlaylistMeta,
    ResolvedUrl,
    VideoMeta,
)
from thumbforge.core.urls import classify_url
from thumbforge.templates.render import RenderContext, render_prompt

if TYPE_CHECKING:
    from typer.testing import Result

runner = CliRunner()
FIXTURES = Path(__file__).parent.parent / "fixtures" / "templates"
VIDEO_ID = "dQw4w9WgXcQ"
OWNER = "UC" + "o" * 22
PLAYLISTS = tuple(f"https://www.youtube.com/playlist?list=PL{c * 16}" for c in "ab")


def _video(title: str = "Me at the zoo") -> VideoMeta:
    return VideoMeta(youtube_id=VIDEO_ID, title=title, url=f"https://youtu.be/{VIDEO_ID}")


def _context(
    *,
    video: VideoMeta | None = None,
    playlist: PlaylistMeta | None = None,
    channel: ChannelMeta | None = None,
    part_number: int | None = None,
    part_label: str | None = None,
    variables: dict[str, str] | None = None,
) -> RenderContext:
    return RenderContext(
        video=video or _video(),
        playlist=playlist,
        part_number=part_number,
        part_label=part_label,
        channel=channel,
        vars=variables or {},
        negative_space="leave the lower-left third uncluttered",
        width=1920,
        height=1080,
    )


def test_render_fills_every_context_field() -> None:
    prompt = "{{ video.title }}|{{ width }}x{{ height }}|{{ negative_space }}|{{ vars.mood }}"
    rendered = render_prompt(prompt, _context(variables={"mood": "calm"}), name="demo")
    assert rendered == "Me at the zoo|1920x1080|leave the lower-left third uncluttered|calm"


def test_render_exposes_playlist_channel_and_part() -> None:
    playlist = PlaylistMeta(youtube_id="PL" + "p" * 16, title="Rust series", url="https://yt/pl")
    channel = ChannelMeta(youtube_id="UC" + "o" * 22, title="Ferris", url="https://yt/c")
    ctx = _context(playlist=playlist, channel=channel, part_number=7, part_label="Finale")
    prompt = "{{ playlist.title }}/{{ channel.title }}/{{ part_number }}/{{ part_label }}"
    assert render_prompt(prompt, ctx, name="demo") == "Rust series/Ferris/7/Finale"


def test_autoescape_is_off_so_prompt_text_stays_verbatim() -> None:
    ctx = _context(video=_video('Q&A <live> "now"'))
    assert render_prompt("{{ video.title }}", ctx, name="demo") == 'Q&A <live> "now"'


def test_blocks_leave_no_stray_blank_lines() -> None:
    prompt = "a\n{% if part_number %}\npart {{ part_number }}\n{% endif %}\nb"
    assert render_prompt(prompt, _context(), name="demo") == "a\nb"
    assert render_prompt(prompt, _context(part_number=2), name="demo") == "a\npart 2\nb"


def test_a_missing_vars_entry_names_the_variable_and_the_template() -> None:
    with pytest.raises(TemplateError) as raised:
        render_prompt("Tone: {{ vars.tone }}", _context(), name="bold-title")
    assert raised.value.exit_code == ExitCode.USAGE
    assert "'vars.tone'" in raised.value.message
    assert "bold-title" in raised.value.message


def test_a_missing_top_level_variable_is_named() -> None:
    with pytest.raises(TemplateError, match=r"undefined variable 'nope' in demo"):
        render_prompt("{{ nope }}", _context(), name="demo")


def test_a_missing_attribute_on_the_video_is_named() -> None:
    with pytest.raises(TemplateError, match=r"undefined variable 'video\.genre' in demo"):
        render_prompt("{{ video.genre }}", _context(), name="demo")


def test_reading_through_a_missing_playlist_says_it_is_none() -> None:
    with pytest.raises(TemplateError, match=r"undefined variable 'title' on None in demo"):
        render_prompt("{{ playlist.title }}", _context(), name="demo")


@pytest.mark.parametrize("source", ['{{ width + "px" }}', "{{ 1 / 0 }}", '{% include "x" %}'])
def test_a_failure_while_rendering_is_a_template_error(source: str) -> None:
    with pytest.raises(TemplateError, match=r"cannot render demo"):
        render_prompt(source, _context(), name="demo")


def test_a_syntax_error_is_a_template_error_with_its_line() -> None:
    with pytest.raises(TemplateError, match=r"demo.*line 2"):
        render_prompt("fine\n{{ video.title ", _context(), name="demo")


class _StubSource:
    """Canned metadata so ``fetch`` stores a video and playlist with no network."""

    key: ClassVar[str] = "ytdlp"

    async def resolve(self, url: str) -> ResolvedUrl:
        return classify_url(url)

    async def fetch_video(self, youtube_id: str) -> VideoMeta:
        return VideoMeta(
            youtube_id=youtube_id,
            title="Me at the zoo",
            url=f"https://youtu.be/{youtube_id}",
            channel_id=OWNER,
        )

    async def fetch_playlist(self, youtube_id: str) -> PlaylistMeta:
        return PlaylistMeta(
            youtube_id=youtube_id,
            title=f"Series {youtube_id[-1]}",
            url=f"https://www.youtube.com/playlist?list={youtube_id}",
            channel_id=OWNER,
            items=(PlaylistItemMeta(video=await self.fetch_video(VIDEO_ID), position=1),),
        )

    async def fetch_channel(self, youtube_id: str) -> ChannelMeta:
        return ChannelMeta(youtube_id=youtube_id, title="Ferris", url="https://yt/c")


@pytest.fixture
def data_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """An initialised database holding one fetched video."""
    monkeypatch.setattr(fetch_cli, "build_source", lambda _source: _StubSource())
    directory = tmp_path / "data"
    assert runner.invoke(app, ["--data-dir", str(directory), "db", "init"]).exit_code == 0
    fetched = runner.invoke(
        app, ["--data-dir", str(directory), "fetch", f"https://youtu.be/{VIDEO_ID}"]
    )
    assert fetched.exit_code == 0, fetched.output
    return directory


@pytest.fixture
def templates_dir(isolate_user_environment: Path) -> Path:
    """The config-dir folder `template render` reads, holding two fixture templates."""
    directory = isolate_user_environment / "config" / "templates"
    directory.mkdir(parents=True)
    for name, prompt in (("demo", "demo.j2"), ("needs-tone", "needs-tone.j2")):
        shutil.copy(FIXTURES / "valid.toml", directory / f"{name}.toml")
        shutil.copy(FIXTURES / prompt, directory / f"{name}.j2")
    return directory


def _render(data_dir: Path, *args: str, json_mode: bool = False) -> Result:
    command = ["--data-dir", str(data_dir)]
    if json_mode:
        command.append("--json")
    return runner.invoke(app, [*command, "template", "render", *args])


def test_cli_prints_the_rendered_prompt(data_dir: Path, templates_dir: Path) -> None:
    result = _render(data_dir, "demo", "--video", VIDEO_ID, "--part", "3", "--var", "mood=calm")
    assert result.exit_code == 0, result.output
    out = result.stdout
    assert 'Background art for "Me at the zoo", 1920x1080.' in out
    assert "Series instalment 3." in out
    assert "Composition: leave the lower-left third uncluttered." in out
    assert "Mood: calm." in out
    assert "{{" not in out


def test_cli_omits_the_part_when_none_is_given(data_dir: Path, templates_dir: Path) -> None:
    result = _render(data_dir, "demo", "--video", VIDEO_ID, "--var", "mood=calm")
    assert result.exit_code == 0, result.output
    assert "Series instalment" not in result.stdout


def test_cli_json_mode_emits_name_and_prompt(data_dir: Path, templates_dir: Path) -> None:
    result = _render(data_dir, "demo", "--video", VIDEO_ID, "--var", "mood=", json_mode=True)
    assert result.exit_code == 0, result.output
    payload = json.loads(result.stdout)
    assert payload["template"] == "demo"
    assert payload["prompt"].endswith("Mood: .")


def test_cli_missing_variable_exits_2_naming_variable_and_template(
    data_dir: Path, templates_dir: Path
) -> None:
    result = _render(data_dir, "needs-tone", "--video", VIDEO_ID, "--var", "mood=")
    assert result.exit_code == ExitCode.USAGE
    assert "vars.tone" in result.stderr
    assert "needs-tone" in result.stderr


def test_cli_supplying_the_variable_fixes_it(data_dir: Path, templates_dir: Path) -> None:
    result = _render(data_dir, "needs-tone", "--video", VIDEO_ID, "--var", "tone=warm")
    assert result.exit_code == 0, result.output
    assert "Tone: warm." in result.stdout


def test_cli_prints_brackets_literally(data_dir: Path, templates_dir: Path) -> None:
    result = _render(data_dir, "demo", "--video", VIDEO_ID, "--var", "mood=[red]hot[/red]")
    assert result.exit_code == 0, result.output
    assert "Mood: [red]hot[/red]." in result.stdout


def test_cli_unknown_template_exits_3(data_dir: Path, templates_dir: Path) -> None:
    result = _render(data_dir, "nope", "--video", VIDEO_ID)
    assert result.exit_code == ExitCode.NOT_FOUND


def test_cli_unknown_video_exits_3(data_dir: Path, templates_dir: Path) -> None:
    result = _render(data_dir, "demo", "--video", "aaaaaaaaaaa", "--var", "mood=x")
    assert result.exit_code == ExitCode.NOT_FOUND


def test_cli_a_var_without_equals_exits_2(data_dir: Path, templates_dir: Path) -> None:
    result = _render(data_dir, "demo", "--video", VIDEO_ID, "--var", "mood")
    assert result.exit_code == ExitCode.USAGE


def test_cli_a_template_name_cannot_escape_the_templates_dir(
    data_dir: Path, templates_dir: Path
) -> None:
    result = _render(data_dir, "../demo", "--video", VIDEO_ID)
    assert result.exit_code == ExitCode.USAGE


def _fetch(data_dir: Path, url: str) -> None:
    fetched = runner.invoke(app, ["--data-dir", str(data_dir), "fetch", url])
    assert fetched.exit_code == 0, fetched.output


def test_cli_a_video_in_one_playlist_supplies_its_part(data_dir: Path, templates_dir: Path) -> None:
    _fetch(data_dir, PLAYLISTS[0])
    result = _render(data_dir, "demo", "--video", VIDEO_ID, "--var", "mood=calm")
    assert result.exit_code == 0, result.output
    assert "Series instalment 1." in result.stdout


def test_cli_the_part_flag_overrides_the_playlist_part(data_dir: Path, templates_dir: Path) -> None:
    _fetch(data_dir, PLAYLISTS[0])
    result = _render(data_dir, "demo", "--video", VIDEO_ID, "--part", "5", "--var", "mood=calm")
    assert result.exit_code == 0, result.output
    assert "Series instalment 5." in result.stdout


def test_cli_a_video_in_two_playlists_supplies_no_part(data_dir: Path, templates_dir: Path) -> None:
    for url in PLAYLISTS:
        _fetch(data_dir, url)
    result = _render(data_dir, "demo", "--video", VIDEO_ID, "--var", "mood=calm")
    assert result.exit_code == 0, result.output
    assert "Series instalment" not in result.stdout
