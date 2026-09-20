"""`emit` is the machine boundary: what it prints must always be parseable JSON."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, cast

import pytest
from rich.console import Console

from thumbforge.cli._render import AppContext, emit, kv

if TYPE_CHECKING:
    from thumbforge.core.json import JsonValue


def _json_context() -> tuple[AppContext, Console]:
    console = Console(no_color=True, highlight=False, width=200)
    return AppContext(console=console, json_mode=True), console


def test_json_mode_output_round_trips() -> None:
    ctx, console = _json_context()
    with console.capture() as captured:
        emit(ctx, {"revision": "head", "pending": 0, "ok": True, "note": None})
    assert json.loads(captured.get()) == {
        "revision": "head",
        "pending": 0,
        "ok": True,
        "note": None,
    }


def test_non_json_payload_raises_instead_of_being_stringified() -> None:
    ctx, _ = _json_context()
    with pytest.raises(TypeError):
        emit(ctx, cast("JsonValue", {"path": Path("/tmp/x")}))


def test_non_finite_floats_are_rejected() -> None:
    ctx, _ = _json_context()
    with pytest.raises(ValueError, match="Out of range float"):
        emit(ctx, {"ratio": float("inf")})


def test_rich_mode_uses_the_renderer_and_prints_no_json() -> None:
    console = Console(no_color=True, highlight=False, width=200)
    ctx = AppContext(console=console, json_mode=False)
    with console.capture() as captured:
        emit(ctx, {"revision": "head"}, render=lambda: kv({"revision": "head"}))
    output = captured.get()
    assert "revision" in output
    with pytest.raises(json.JSONDecodeError):
        json.loads(output)
