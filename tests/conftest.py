"""Shared fixtures. Establishes ``tests/`` as the pytest root."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

import pytest

from thumbforge import settings as settings_module

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture(autouse=True)
def isolate_user_environment(
    tmp_path_factory: pytest.TempPathFactory,
    monkeypatch: pytest.MonkeyPatch,
) -> Path:
    """Point platformdirs at a temp directory and drop stray ``THUMBFORGE_*`` variables.

    Without this, anything that exercises the root callback writes ``thumbforge.log`` into the
    developer's or CI runner's real state directory, and a ``config.toml`` or exported
    ``THUMBFORGE_*`` on the machine silently changes test results.
    """
    root = tmp_path_factory.mktemp("thumbforge-home")
    config_dir = root / "config"

    monkeypatch.setattr(settings_module, "default_config_path", lambda: config_dir / "config.toml")
    monkeypatch.setattr(settings_module, "default_data_dir", lambda: root / "data")
    monkeypatch.setattr(settings_module, "default_state_dir", lambda: root / "state")

    for name in [key for key in os.environ if key.startswith("THUMBFORGE_")]:
        monkeypatch.delenv(name, raising=False)

    return root
