"""TOML layout specification loading, validation and writing (ROADMAP P4.1, P4.4, ADR 0006)."""

from __future__ import annotations

import tomllib
from typing import TYPE_CHECKING

import tomli_w
from pydantic import ValidationError

from thumbforge.core.errors import TemplateError
from thumbforge.core.layout import LayoutSpec

if TYPE_CHECKING:
    from pathlib import Path


def load_layout(path: Path) -> LayoutSpec:
    """Load and validate a template layout specification from a TOML file.

    Raises :class:`~thumbforge.core.errors.TemplateError` when the file cannot be read,
    contains malformed TOML, or violates the :class:`LayoutSpec` schema. Every schema
    violation is reported in the error message with its dotted attribute location.
    """
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError) as err:
        msg = f"Cannot read layout spec {path}: {err}"
        raise TemplateError(msg) from err

    try:
        return LayoutSpec.model_validate(data)
    except ValidationError as err:
        messages: list[str] = []
        for e in err.errors():
            loc = ".".join(str(p) for p in e["loc"])
            messages.append(f"{loc}: {e['msg']}" if loc else e["msg"])
        formatted = "\n".join(messages)
        msg = f"Invalid layout spec in {path}:\n{formatted}"
        raise TemplateError(msg) from err


def dump_layout(layout: LayoutSpec) -> str:
    """Render ``layout`` as TOML that :func:`load_layout` reads back to an equal model.

    ``None`` values are omitted because TOML has no null; every optional field defaults to
    ``None`` when absent, so leaving it out round-trips.
    """
    return tomli_w.dumps(layout.model_dump(mode="json", exclude_none=True))
