"""Shared fixtures. Establishes ``tests/`` as the pytest root."""

from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING

import pytest
import structlog

from thumbforge import settings as settings_module

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path


@pytest.fixture(autouse=True)
def isolate_user_environment(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[Path]:
    """Redirect every user directory into ``tmp_path`` and clear ``THUMBFORGE_*``.

    Patching happens at the **platformdirs** level rather than on
    ``settings_module.default_data_dir``: ``GeneralSettings.data_dir`` binds that function as a
    ``default_factory`` at class-definition time, and ``cli/config.py`` imports
    ``default_config_path`` by name, so both would bypass a module-attribute patch. The
    ``user_*_dir`` functions are looked up at call time and cover all of it.

    The teardown closes root logging handlers: a live ``RotatingFileHandler`` holds
    ``state/logs/thumbforge.log`` open, and Windows then refuses to delete the tree.
    """
    root = tmp_path / "home"
    monkeypatch.setattr(settings_module, "user_config_dir", lambda *_a, **_k: str(root / "config"))
    monkeypatch.setattr(settings_module, "user_data_dir", lambda *_a, **_k: str(root / "data"))
    monkeypatch.setattr(settings_module, "user_state_dir", lambda *_a, **_k: str(root / "state"))

    for key in list(os.environ):
        if key.startswith("THUMBFORGE_"):
            monkeypatch.delenv(key, raising=False)

    yield root

    structlog.contextvars.clear_contextvars()
    stdlib_root = logging.getLogger()
    for handler in list(stdlib_root.handlers):
        stdlib_root.removeHandler(handler)
        handler.close()
