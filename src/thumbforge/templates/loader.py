"""Template references, versioned storage and the built-in sync (ROADMAP P4.4, ADR 0006).

A stored template is immutable. Storing content whose ``spec_hash`` the name already has
returns that row; anything else becomes ``max(version) + 1``. Built-ins follow the same rule
with ``is_builtin=True``, so a package release that changes one adds a version and keeps the
old ones for reproducibility.

``templates`` may not import ``storage``, so the store arrives as the :class:`TemplateStore`
Protocol; ``storage.repositories.TemplateRepository`` satisfies it and ``cli`` wires the two.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

from thumbforge.core.errors import NotFoundError, TemplateError
from thumbforge.core.layout import LayoutSpec, Template, spec_hash
from thumbforge.logging import get_logger
from thumbforge.templates.builtins import BUILTIN_NAMES, builtin_files
from thumbforge.templates.render import check_syntax
from thumbforge.templates.schema import dump_layout, load_layout

if TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path

log = get_logger(__name__)

_VERSION = re.compile(r"[1-9][0-9]*", re.ASCII)
_REF_HINT = "use NAME or NAME@VERSION, where VERSION is a positive integer"


class TemplateStore(Protocol):
    """What the loader needs from persistence."""

    def versions(self, name: str) -> Sequence[int]:
        """Every stored version of ``name``, ascending."""
        ...

    def get(self, name: str, version: int) -> Template | None:
        """The template at exactly ``name@version``."""
        ...

    def find(self, name: str, spec_hash: str) -> Template | None:
        """A stored version of ``name`` with this ``spec_hash``."""
        ...

    def add(self, template: Template) -> Template:
        """Insert a new row."""
        ...


@dataclass(frozen=True, slots=True)
class TemplateRef:
    """``NAME`` (latest version) or ``NAME@VERSION`` (exactly that one)."""

    name: str
    version: int | None = None

    def __str__(self) -> str:
        """The reference as the user writes it."""
        return self.name if self.version is None else f"{self.name}@{self.version}"


def check_name(name: str) -> str:
    """Return ``name`` if it can be both a file stem and the name part of a reference.

    ``@`` separates the version and a path separator would let ``template new`` write outside
    the templates directory, so both are refused with exit ``2``.
    """
    if not name or any(char in name for char in "/\\@"):
        msg = f"invalid template name {name!r}"
        raise TemplateError(msg, hint="a name must be non-empty, without '/', '\\' or '@'")
    return name


def parse_ref(text: str) -> TemplateRef:
    """Parse ``NAME[@VERSION]``; a malformed reference is a :class:`TemplateError` (exit 2)."""
    name, separator, version = text.partition("@")
    if not name or any(char in name for char in "/\\"):
        msg = f"malformed template reference {text!r}"
        raise TemplateError(msg, hint=_REF_HINT)
    if not separator:
        return TemplateRef(name)
    if _VERSION.fullmatch(version) is None:
        msg = f"malformed template reference {text!r}"
        raise TemplateError(msg, hint=_REF_HINT)
    return TemplateRef(name, int(version))


def resolve(store: TemplateStore, ref: TemplateRef) -> Template:
    """The template ``ref`` names; an unknown name or version is :class:`NotFoundError`."""
    versions = store.versions(ref.name)
    if not versions:
        msg = f"template {str(ref)!r}"
        raise NotFoundError(
            msg,
            hint="`thumbforge template list` shows the stored templates",
        )
    version = versions[-1] if ref.version is None else ref.version
    template = store.get(ref.name, version) if version in versions else None
    if template is None:
        msg = f"template {str(ref)!r}"
        stored = ", ".join(f"{ref.name}@{v}" for v in versions)
        raise NotFoundError(msg, hint=f"stored versions: {stored}")
    return template


def locate(path: Path) -> tuple[Path, Path]:
    """Find the ``(toml, j2)`` pair ``path`` names.

    ``path`` is ``X.toml`` (with a sibling ``X.j2``), the stem ``X``, or a directory holding
    exactly one ``.toml`` and its same-stem ``.j2``.
    """
    if path.is_dir():
        layouts = sorted(path.glob("*.toml"))
        prompts = sorted(path.glob("*.j2"))
        if len(layouts) != 1 or len(prompts) != 1:
            msg = f"{path} must hold exactly one .toml and one .j2 file"
            raise TemplateError(
                msg, hint=f"found {len(layouts)} .toml and {len(prompts)} .j2 files"
            )
        toml_path = layouts[0]
    elif path.suffix == ".toml":
        toml_path = path
    else:
        toml_path = path.with_name(f"{path.name}.toml")
    j2_path = toml_path.with_suffix(".j2")
    missing = [p for p in (toml_path, j2_path) if not p.is_file()]
    if missing:
        msg = f"no template at {path}: missing {', '.join(str(p) for p in missing)}"
        raise TemplateError(msg, hint="a template is NAME.toml with a sibling NAME.j2")
    return toml_path, j2_path


def read_pair(toml_path: Path, j2_path: Path) -> tuple[LayoutSpec, str]:
    """Load and validate a layout and its prompt, reporting every problem in both at once.

    The prompt is read in text mode, which translates CRLF to LF, so a checkout on Windows
    hashes the same as one on Linux.
    """
    errors: list[str] = []
    layout: LayoutSpec | None = None
    prompt: str | None = None
    try:
        layout = load_layout(toml_path)
    except TemplateError as err:
        errors.append(err.message)
    try:
        prompt = j2_path.read_text(encoding="utf-8")
        check_syntax(prompt, name=j2_path.name)
    except (OSError, UnicodeDecodeError) as err:
        errors.append(f"Cannot read prompt {j2_path}: {err}")
    except TemplateError as err:
        errors.append(err.message)
    if layout is None or prompt is None or errors:
        raise TemplateError("\n".join(errors))
    return layout, prompt


def validate_files(toml_path: Path) -> tuple[LayoutSpec, Path | None]:
    """``template validate``: the layout, plus a Jinja check of its sibling ``.j2`` if present."""
    j2_path = toml_path.with_suffix(".j2")
    if not j2_path.is_file():
        return load_layout(toml_path), None
    layout, _ = read_pair(toml_path, j2_path)
    return layout, j2_path


def store_template(
    store: TemplateStore, layout: LayoutSpec, prompt: str, *, builtin: bool
) -> tuple[Template, bool]:
    """Store ``prompt`` + ``layout`` under ``layout.template.name``; ``True`` if a row was added.

    Content the name already has (same ``spec_hash``, any version) returns that row instead.
    """
    name = check_name(layout.template.name)
    digest = spec_hash(prompt, layout)
    existing = store.find(name, digest)
    if existing is not None:
        return existing, False
    versions = store.versions(name)
    template = Template(
        name=name,
        version=(versions[-1] if versions else 0) + 1,
        prompt_template=prompt,
        layout=layout,
        spec_hash=digest,
        is_builtin=builtin,
    )
    return store.add(template), True


def import_template(store: TemplateStore, path: Path) -> tuple[Template, bool]:
    """``template import PATH``: locate, validate and store a user template."""
    layout, prompt = read_pair(*locate(path))
    return store_template(store, layout, prompt, builtin=False)


def sync_builtins(store: TemplateStore) -> list[Template]:
    """Store every shipped built-in whose current content is not stored yet; return those added.

    Idempotent: a second call with the same package adds nothing.
    """
    added: list[Template] = []
    for name in BUILTIN_NAMES:
        template, created = store_template(store, *read_pair(*builtin_files(name)), builtin=True)
        if created:
            log.info("builtin template stored", template=template.ref)
            added.append(template)
    return added


def write_copy(template: Template, name: str, directory: Path) -> tuple[Path, Path]:
    """Write ``template`` as ``directory/NAME.toml`` + ``NAME.j2``, renamed to ``name``.

    Refuses (exit ``2``) when either file exists, before writing anything.
    """
    check_name(name)
    toml_path, j2_path = directory / f"{name}.toml", directory / f"{name}.j2"
    existing = [p for p in (toml_path, j2_path) if p.exists()]
    if existing:
        msg = f"refusing to overwrite {', '.join(str(p) for p in existing)}"
        raise TemplateError(msg, hint="choose another NAME or move the existing files away")
    meta = template.layout.template.model_copy(update={"name": name})
    layout = template.layout.model_copy(update={"template": meta})
    try:
        directory.mkdir(parents=True, exist_ok=True)
        # "x" mode: a file appearing between the check above and here is still not clobbered.
        with toml_path.open("x", encoding="utf-8") as handle:
            handle.write(dump_layout(layout))
        with j2_path.open("x", encoding="utf-8") as handle:
            handle.write(template.prompt_template)
    except OSError as err:
        msg = f"cannot write template {name!r} to {directory}: {err}"
        raise TemplateError(msg) from err
    return toml_path, j2_path
