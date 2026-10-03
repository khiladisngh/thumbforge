"""Shared fixtures. Establishes ``tests/`` as the pytest root."""

from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING

import pytest
import structlog
from PIL import Image, ImageChops

from thumbforge import settings as settings_module
from thumbforge.imaging import fonts as fonts_module

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator
    from pathlib import Path

UPDATE_GOLDEN = "--update-golden"


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        UPDATE_GOLDEN,
        action="store_true",
        default=False,
        help="Write golden images from the current output instead of comparing against them.",
    )


@pytest.fixture
def assert_golden(request: pytest.FixtureRequest) -> Callable[[Image.Image, Path], None]:
    """Compare an image with its committed golden PNG, or rewrite it with ``--update-golden``.

    The comparison is on decoded pixels (size, mode, ``tobytes()``), never on the PNG file:
    zlib output may differ per platform while the pixels are identical.
    """
    update = bool(request.config.getoption(UPDATE_GOLDEN))

    def check(actual: Image.Image, golden_path: Path) -> None:
        if update:
            golden_path.parent.mkdir(parents=True, exist_ok=True)
            actual.save(golden_path, format="PNG")
            return
        if not golden_path.is_file():
            pytest.fail(
                f"golden {golden_path} is missing; create it with "
                f"`uv run pytest -m golden {UPDATE_GOLDEN}` and review it before committing"
            )
        with Image.open(golden_path) as expected:
            expected.load()
            if (actual.size, actual.mode) != (expected.size, expected.mode):
                pytest.fail(
                    f"{golden_path.name}: got {actual.mode} {actual.size}, "
                    f"golden is {expected.mode} {expected.size}"
                )
            if actual.tobytes() != expected.tobytes():
                bbox = ImageChops.difference(actual, expected).getbbox()
                pytest.fail(f"{golden_path.name}: pixels differ inside {bbox}")

    return check


@pytest.fixture(autouse=True)
def isolate_user_environment(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[Path]:
    """Redirect every user directory into ``tmp_path`` and clear ``THUMBFORGE_*``.

    Patching happens at the **platformdirs** level rather than on
    ``settings_module.default_data_dir``: ``GeneralSettings.data_dir`` binds that function as a
    ``default_factory`` at class-definition time, and ``cli/config.py`` imports
    ``default_config_path`` by name, so both would bypass a module-attribute patch. The
    ``user_*_dir`` functions are looked up at call time and cover all of it.
    ``imaging.fonts`` calls platformdirs itself (imaging may not import settings), so its
    ``user_config_dir`` is patched as well.

    The teardown closes root logging handlers: a live ``RotatingFileHandler`` holds
    ``state/logs/thumbforge.log`` open, and Windows then refuses to delete the tree.
    """
    root = tmp_path / "home"
    monkeypatch.setattr(settings_module, "user_config_dir", lambda *_a, **_k: str(root / "config"))
    monkeypatch.setattr(settings_module, "user_data_dir", lambda *_a, **_k: str(root / "data"))
    monkeypatch.setattr(settings_module, "user_state_dir", lambda *_a, **_k: str(root / "state"))
    monkeypatch.setattr(fonts_module, "user_config_dir", lambda *_a, **_k: str(root / "config"))

    for key in list(os.environ):
        if key.startswith("THUMBFORGE_"):
            monkeypatch.delenv(key, raising=False)

    yield root

    structlog.contextvars.clear_contextvars()
    stdlib_root = logging.getLogger()
    for handler in list(stdlib_root.handlers):
        stdlib_root.removeHandler(handler)
        handler.close()
