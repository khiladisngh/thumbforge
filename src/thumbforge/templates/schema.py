"""TOML layout specification loading and validation (ROADMAP P4.1, ADR 0006)."""

from __future__ import annotations

import tomllib
from typing import TYPE_CHECKING

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
