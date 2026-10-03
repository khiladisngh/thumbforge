"""Locate the built-in templates shipped as package data in ``templates/builtin/`` (ROADMAP P4.3).

Each built-in is a ``NAME.toml`` layout spec plus a ``NAME.j2`` prompt. This module only finds
the files; reading them is :func:`thumbforge.templates.schema.load_layout` and
:func:`thumbforge.templates.render.render_prompt`.
"""

from __future__ import annotations

from importlib import resources
from pathlib import Path

from thumbforge.core.errors import NotFoundError

BUILTIN_NAMES: tuple[str, ...] = ("bold-title", "minimal", "series-parts")


def builtin_files(name: str) -> tuple[Path, Path]:
    """Return ``(toml_path, j2_path)`` for the built-in template ``name``.

    Raises :class:`~thumbforge.core.errors.NotFoundError` for a name that is not built in.
    """
    if name not in BUILTIN_NAMES:
        msg = f"no built-in template named {name!r}"
        raise NotFoundError(msg, hint=f"built-in templates: {', '.join(BUILTIN_NAMES)}")
    # The package is installed from a wheel into a directory, never imported from a zip, so
    # its resources are plain files on disk.
    directory = Path(str(resources.files("thumbforge.templates") / "builtin"))
    return directory / f"{name}.toml", directory / f"{name}.j2"
