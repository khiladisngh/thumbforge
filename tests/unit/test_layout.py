"""Unit tests for LayoutSpec and its block models (ROADMAP P4.1, phase-4 spec)."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from thumbforge.core.layout import (
    Anchor,
    LayoutSpec,
    TextCase,
)


def _valid_spec_dict() -> dict[str, object]:
    """Return a valid layout spec dictionary matching the phase-4 spec TOML."""
    return {
        "template": {
            "name": "bold-title",
            "description": "Large title bottom-left, optional Part badge top-right",
        },
        "canvas": {
            "width": 1920,
            "height": 1080,
            "safe_margin_px": 64,
        },
        "title": {
            "enabled": True,
            "font": "Inter-Bold",
            "max_lines": 3,
            "size_px": 120,
            "min_size_px": 72,
            "color": "#FFFFFF",
            "stroke_px": 6,
            "stroke_color": "#000000",
            "anchor": "bottom-left",
            "box": {"x": 64, "y": 640, "w": 1400, "h": 376},
            "case": "upper",
        },
        "part": {
            "enabled": True,
            "format": "PART {n}",
            "font": "Inter-Bold",
            "size_px": 72,
            "anchor": "top-right",
            "badge": {"fill": "#E53935", "padding_px": 24, "radius_px": 16},
        },
        "negative_space": {
            "hint": "leave the lower-left third uncluttered",
        },
    }


def test_valid_layout_spec_loads() -> None:
    data = _valid_spec_dict()
    spec = LayoutSpec.model_validate(data)
    assert spec.template.name == "bold-title"
    assert spec.canvas.width == 1920
    assert spec.canvas.height == 1080
    assert spec.title.anchor == Anchor.BOTTOM_LEFT
    assert spec.title.case == TextCase.UPPER
    assert spec.title.box.x == 64
    assert spec.part.badge is not None
    assert spec.part.badge.fill == "#E53935"
    assert spec.negative_space.hint == "leave the lower-left third uncluttered"


@pytest.mark.parametrize(
    "bad_anchor",
    ["middle", "middle-center", "center-middle", "top", "left", "random"],
)
def test_invalid_anchor_rejected(bad_anchor: str) -> None:
    data = _valid_spec_dict()
    data["title"]["anchor"] = bad_anchor  # type: ignore[index]
    with pytest.raises(ValidationError) as exc_info:
        LayoutSpec.model_validate(data)
    errors = exc_info.value.errors()
    assert any(e["loc"] == ("title", "anchor") for e in errors)


@pytest.mark.parametrize(
    "bad_color",
    ["red", "#fff", "#12345", "#1234567", "#gggggg", "123456", ""],
)
def test_invalid_hex_color_rejected(bad_color: str) -> None:
    data = _valid_spec_dict()
    data["title"]["color"] = bad_color  # type: ignore[index]
    with pytest.raises(ValidationError) as exc_info:
        LayoutSpec.model_validate(data)
    errors = exc_info.value.errors()
    assert any(e["loc"] == ("title", "color") for e in errors)


def test_box_within_canvas_exact_bounds_valid() -> None:
    data = _valid_spec_dict()
    data["title"]["box"] = {"x": 0, "y": 0, "w": 1920, "h": 1080}  # type: ignore[index]
    spec = LayoutSpec.model_validate(data)
    assert spec.title.box.w == 1920
    assert spec.title.box.h == 1080


@pytest.mark.parametrize(
    "box",
    [
        {"x": 100, "y": 0, "w": 1821, "h": 500},  # right edge 1921 > 1920
        {"x": 0, "y": 200, "w": 500, "h": 881},  # bottom edge 1081 > 1080
    ],
)
def test_box_past_the_canvas_is_rejected(box: dict[str, int]) -> None:
    data = _valid_spec_dict()
    data["title"]["box"] = box  # type: ignore[index]
    with pytest.raises(ValidationError, match=r"title\.box"):
        LayoutSpec.model_validate(data)


def test_min_size_px_equal_to_size_px_valid() -> None:
    data = _valid_spec_dict()
    data["title"]["size_px"] = 72  # type: ignore[index]
    data["title"]["min_size_px"] = 72  # type: ignore[index]
    spec = LayoutSpec.model_validate(data)
    assert spec.title.min_size_px == 72


def test_min_size_px_greater_than_size_px_rejected() -> None:
    data = _valid_spec_dict()
    data["title"]["size_px"] = 72  # type: ignore[index]
    data["title"]["min_size_px"] = 73  # type: ignore[index]
    with pytest.raises(ValidationError) as exc_info:
        LayoutSpec.model_validate(data)
    errors = exc_info.value.errors()
    assert any(e["loc"] == ("title", "min_size_px") for e in errors)


@pytest.mark.parametrize("bad_case", ["lower", "camel", "kebab", "INVALID"])
def test_invalid_text_case_rejected(bad_case: str) -> None:
    data = _valid_spec_dict()
    data["title"]["case"] = bad_case  # type: ignore[index]
    with pytest.raises(ValidationError) as exc_info:
        LayoutSpec.model_validate(data)
    errors = exc_info.value.errors()
    assert any(e["loc"] == ("title", "case") for e in errors)


@pytest.mark.parametrize(
    ("path", "bad_val"),
    [
        (("canvas", "width"), 0),
        (("canvas", "width"), -10),
        (("canvas", "height"), 0),
        (("canvas", "height"), -10),
        (("title", "size_px"), 0),
        (("title", "size_px"), -5),
        (("title", "min_size_px"), 0),
        (("title", "max_lines"), 0),
        (("title", "box", "w"), 0),
        (("title", "box", "h"), 0),
        (("title", "box", "x"), -1),
        (("title", "box", "y"), -1),
        (("part", "size_px"), 0),
    ],
)
def test_positive_sizes_enforced(path: tuple[str, ...], bad_val: int) -> None:
    data = _valid_spec_dict()
    target: dict[str, object] = data  # type: ignore[assignment]
    for seg in path[:-1]:
        target = target[seg]  # type: ignore[assignment]
    target[path[-1]] = bad_val
    with pytest.raises(ValidationError) as exc_info:
        LayoutSpec.model_validate(data)
    errors = exc_info.value.errors()
    assert any(e["loc"] == path for e in errors)


def test_extra_fields_forbidden() -> None:
    data = _valid_spec_dict()
    data["canvas"]["extra_param"] = 123  # type: ignore[index]
    with pytest.raises(ValidationError) as exc_info:
        LayoutSpec.model_validate(data)
    errors = exc_info.value.errors()
    assert any(e["loc"] == ("canvas", "extra_param") for e in errors)
