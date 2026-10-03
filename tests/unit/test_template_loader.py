"""Template versioning, reference resolution and the built-in sync (ROADMAP P4.4).

Runs against the real `TemplateRepository` over a migrated SQLite file: the loader's rules
and the `UNIQUE(name, version)` constraint are tested together.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from thumbforge.core.errors import ExitCode, NotFoundError, TemplateError
from thumbforge.core.json import canonical_json
from thumbforge.core.layout import spec_hash
from thumbforge.storage.db import get_engine, init_db, session_factory, session_scope
from thumbforge.storage.repositories import Repositories, TemplateRepository
from thumbforge.templates import loader
from thumbforge.templates.builtins import BUILTIN_NAMES, builtin_files
from thumbforge.templates.loader import (
    TemplateRef,
    import_template,
    locate,
    parse_ref,
    read_pair,
    resolve,
    sync_builtins,
    write_copy,
)
from thumbforge.templates.schema import load_layout

if TYPE_CHECKING:
    from collections.abc import Iterator

FIXTURES = Path(__file__).parent.parent / "fixtures" / "templates"


@pytest.fixture
def store(tmp_path: Path) -> Iterator[TemplateRepository]:
    db_file = tmp_path / "templates.sqlite3"
    init_db(db_file)
    engine = get_engine(db_file)
    with session_scope(session_factory(engine)) as session:
        yield Repositories(session).templates
    engine.dispose()


def _pair(directory: Path, name: str = "demo", prompt: str = "Art for {{ video.title }}.") -> Path:
    """Write `name.toml` (the valid fixture renamed) and `name.j2`; return the `.toml`."""
    directory.mkdir(parents=True, exist_ok=True)
    layout = (FIXTURES / "valid.toml").read_text(encoding="utf-8")
    toml_path = directory / f"{name}.toml"
    toml_path.write_text(
        layout.replace('name = "bold-title"', f'name = "{name}"'), encoding="utf-8"
    )
    (directory / f"{name}.j2").write_text(prompt, encoding="utf-8")
    return toml_path


@pytest.mark.parametrize(
    ("text", "expected"),
    [("bold-title", TemplateRef("bold-title")), ("bold-title@12", TemplateRef("bold-title", 12))],
)
def test_a_reference_is_a_name_and_an_optional_version(text: str, expected: TemplateRef) -> None:
    assert parse_ref(text) == expected
    assert str(parse_ref(text)) == text


@pytest.mark.parametrize(
    "text", ["", "@1", "name@", "name@x", "name@0", "name@-1", "name@01", "a@1@2", "a/b", r"a\b"]
)
def test_a_malformed_reference_is_a_usage_error(text: str) -> None:
    with pytest.raises(TemplateError) as raised:
        parse_ref(text)
    assert raised.value.exit_code == ExitCode.USAGE


def test_canonical_json_sorts_keys_and_drops_whitespace() -> None:
    assert (
        canonical_json({"b": 1, "a": [1, {"d": 2, "c": "é"}]}) == '{"a":[1,{"c":"é","d":2}],"b":1}'
    )


def test_spec_hash_ignores_toml_key_and_table_order(tmp_path: Path) -> None:
    original = load_layout(FIXTURES / "valid.toml")
    text = (FIXTURES / "valid.toml").read_text(encoding="utf-8")
    sections = text.split("\n\n")
    # Reverse the tables, and the keys inside each table after its header.
    shuffled = "\n\n".join(
        "\n".join([lines[0], *reversed(lines[1:])])
        for lines in (section.strip().splitlines() for section in reversed(sections))
    )
    reordered = tmp_path / "reordered.toml"
    reordered.write_text(shuffled + "\n", encoding="utf-8")
    assert reordered.read_text(encoding="utf-8") != text
    assert spec_hash("p", load_layout(reordered)) == spec_hash("p", original)


def test_spec_hash_covers_the_prompt_and_the_layout() -> None:
    layout = load_layout(FIXTURES / "valid.toml")
    moved = layout.model_copy(update={"canvas": layout.canvas.model_copy(update={"width": 3840})})
    assert spec_hash("a", layout) != spec_hash("b", layout)
    assert spec_hash("a", layout) != spec_hash("a", moved)


def test_crlf_and_lf_prompts_hash_the_same(tmp_path: Path) -> None:
    lf = _pair(tmp_path / "lf", prompt="line one\nline two\n")
    crlf = _pair(tmp_path / "crlf", prompt="")
    crlf.with_suffix(".j2").write_bytes(b"line one\r\nline two\r\n")
    lf_layout, lf_prompt = read_pair(lf, lf.with_suffix(".j2"))
    crlf_layout, crlf_prompt = read_pair(crlf, crlf.with_suffix(".j2"))
    assert crlf_prompt == lf_prompt == "line one\nline two\n"
    assert spec_hash(crlf_prompt, crlf_layout) == spec_hash(lf_prompt, lf_layout)


def test_importing_the_same_pair_twice_stores_one_row(
    tmp_path: Path, store: TemplateRepository
) -> None:
    path = _pair(tmp_path)
    first, created = import_template(store, path)
    again, created_again = import_template(store, path)
    assert (first.name, first.version, first.is_builtin, created) == ("demo", 1, False, True)
    assert (again, created_again) == (first, False)
    assert list(store.versions("demo")) == [1]


def test_a_one_character_prompt_change_is_a_new_version(
    tmp_path: Path, store: TemplateRepository
) -> None:
    path = _pair(tmp_path, prompt="Art for {{ video.title }}.")
    first, _ = import_template(store, path)
    path.with_suffix(".j2").write_text("Art for {{ video.title }}!", encoding="utf-8")
    second, created = import_template(store, path)
    assert created
    assert second.version == first.version + 1
    assert second.spec_hash != first.spec_hash
    assert list(store.versions("demo")) == [1, 2]
    assert store.get("demo", 1) == first


def test_a_crlf_copy_of_a_stored_pair_is_not_a_new_version(
    tmp_path: Path, store: TemplateRepository
) -> None:
    import_template(store, _pair(tmp_path / "lf", prompt="a\nb\n"))
    crlf = _pair(tmp_path / "crlf", prompt="")
    crlf.with_suffix(".j2").write_bytes(b"a\r\nb\r\n")
    _, created = import_template(store, crlf)
    assert not created


@pytest.mark.parametrize("form", ["toml", "stem", "directory"])
def test_import_accepts_the_toml_its_stem_or_its_directory(
    tmp_path: Path, store: TemplateRepository, form: str
) -> None:
    toml_path = _pair(tmp_path / "pair")
    argument = {
        "toml": toml_path,
        "stem": toml_path.with_suffix(""),
        "directory": toml_path.parent,
    }[form]
    assert locate(argument) == (toml_path, toml_path.with_suffix(".j2"))
    template, _ = import_template(store, argument)
    assert template.name == "demo"


def test_a_directory_with_two_layouts_is_ambiguous(tmp_path: Path) -> None:
    _pair(tmp_path, "one")
    _pair(tmp_path, "two")
    with pytest.raises(TemplateError, match="exactly one"):
        locate(tmp_path)


def test_a_layout_without_its_prompt_is_a_usage_error(tmp_path: Path) -> None:
    toml_path = _pair(tmp_path)
    toml_path.with_suffix(".j2").unlink()
    with pytest.raises(TemplateError) as raised:
        locate(toml_path)
    assert raised.value.exit_code == ExitCode.USAGE
    assert "demo.j2" in raised.value.message


def test_read_pair_reports_layout_and_prompt_errors_together(tmp_path: Path) -> None:
    bad = tmp_path / "bad.toml"
    shutil.copy(FIXTURES / "bad-anchor.toml", bad)
    text = bad.read_text(encoding="utf-8").replace("size_px = 120", "size_px = -1")
    bad.write_text(text, encoding="utf-8")
    bad.with_suffix(".j2").write_text("fine\n{{ video.title ", encoding="utf-8")
    with pytest.raises(TemplateError) as raised:
        read_pair(bad, bad.with_suffix(".j2"))
    message = raised.value.message
    assert "title.anchor" in message
    assert "title.size_px" in message
    assert "line 2" in message


def test_an_imported_name_must_be_referenceable(tmp_path: Path, store: TemplateRepository) -> None:
    with pytest.raises(TemplateError) as raised:
        import_template(store, _pair(tmp_path, "a@b"))
    assert raised.value.exit_code == ExitCode.USAGE


def test_sync_builtins_stores_each_builtin_once_at_version_1(store: TemplateRepository) -> None:
    added = sync_builtins(store)
    assert [(t.name, t.version, t.is_builtin) for t in added] == [
        (name, 1, True) for name in BUILTIN_NAMES
    ]
    assert sync_builtins(store) == []
    assert [(t.name, t.version) for t in store.list()] == [(name, 1) for name in BUILTIN_NAMES]


def test_a_changed_builtin_is_stored_as_the_next_version(
    tmp_path: Path, store: TemplateRepository, monkeypatch: pytest.MonkeyPatch
) -> None:
    sync_builtins(store)
    toml_path, j2_path = builtin_files("minimal")
    changed = tmp_path / "minimal.j2"
    changed.write_text(j2_path.read_text(encoding="utf-8") + "Extra.\n", encoding="utf-8")

    def patched(name: str) -> tuple[Path, Path]:
        return (toml_path, changed) if name == "minimal" else builtin_files(name)

    monkeypatch.setattr(loader, "builtin_files", patched)
    [added] = sync_builtins(store)
    assert (added.name, added.version, added.is_builtin) == ("minimal", 2, True)
    assert list(store.versions("minimal")) == [1, 2]
    assert sync_builtins(store) == []


def test_a_bare_name_resolves_to_the_highest_version(
    tmp_path: Path, store: TemplateRepository
) -> None:
    path = _pair(tmp_path, prompt="one")
    import_template(store, path)
    path.with_suffix(".j2").write_text("two", encoding="utf-8")
    import_template(store, path)
    assert resolve(store, parse_ref("demo")).prompt_template == "two"
    assert resolve(store, parse_ref("demo@1")).prompt_template == "one"


def test_an_unknown_name_is_not_found(store: TemplateRepository) -> None:
    with pytest.raises(NotFoundError) as raised:
        resolve(store, parse_ref("nope"))
    assert raised.value.exit_code == ExitCode.NOT_FOUND
    assert raised.value.hint


def test_an_unknown_version_is_not_found_and_lists_the_versions(
    store: TemplateRepository,
) -> None:
    sync_builtins(store)
    with pytest.raises(NotFoundError) as raised:
        resolve(store, parse_ref("minimal@7"))
    assert raised.value.exit_code == ExitCode.NOT_FOUND
    assert "minimal@7" in raised.value.message
    assert raised.value.hint is not None
    assert "1" in raised.value.hint


def test_write_copy_renames_the_template_and_round_trips(
    tmp_path: Path, store: TemplateRepository
) -> None:
    sync_builtins(store)
    source = resolve(store, parse_ref("series-parts"))
    toml_path, j2_path = write_copy(source, "my-series", tmp_path / "templates")
    assert (toml_path.name, j2_path.name) == ("my-series.toml", "my-series.j2")
    layout, prompt = read_pair(toml_path, j2_path)
    assert layout.template.name == "my-series"
    assert layout.model_copy(update={"template": source.layout.template}) == source.layout
    assert prompt == source.prompt_template
    copied, created = import_template(store, toml_path)
    assert (copied.name, copied.version, created) == ("my-series", 1, True)


@pytest.mark.parametrize("existing", ["toml", "j2"])
def test_write_copy_refuses_to_overwrite_either_file(
    tmp_path: Path, store: TemplateRepository, existing: str
) -> None:
    sync_builtins(store)
    directory = tmp_path / "templates"
    directory.mkdir()
    (directory / f"mine.{existing}").write_text("keep me", encoding="utf-8")
    with pytest.raises(TemplateError) as raised:
        write_copy(resolve(store, parse_ref("minimal")), "mine", directory)
    assert raised.value.exit_code == ExitCode.USAGE
    assert sorted(p.name for p in directory.iterdir()) == [f"mine.{existing}"]
    assert (directory / f"mine.{existing}").read_text(encoding="utf-8") == "keep me"


@pytest.mark.parametrize("name", ["", "a/b", r"a\b", "a@1"])
def test_write_copy_rejects_a_name_that_is_a_path_or_a_reference(
    tmp_path: Path, store: TemplateRepository, name: str
) -> None:
    sync_builtins(store)
    with pytest.raises(TemplateError):
        write_copy(resolve(store, parse_ref("minimal")), name, tmp_path)
    assert not any(p.suffix in {".toml", ".j2"} for p in tmp_path.rglob("*"))
