"""Layout specification schema for deterministic text overlays (ROADMAP P4.1, ADR 0006).

Defines the Pydantic models that parse and validate a template's TOML layout file.
Lives in ``core`` because both ``imaging`` (Phase 5) and ``core.services`` consume it.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator, model_validator

_HEX_COLOR_PATTERN = r"^#[0-9a-fA-F]{6}$"


class Anchor(StrEnum):
    """The nine standard 2D layout anchor points."""

    TOP_LEFT = "top-left"
    TOP_CENTER = "top-center"
    TOP_RIGHT = "top-right"
    CENTER_LEFT = "center-left"
    CENTER = "center"
    CENTER_RIGHT = "center-right"
    BOTTOM_LEFT = "bottom-left"
    BOTTOM_CENTER = "bottom-center"
    BOTTOM_RIGHT = "bottom-right"


class TextCase(StrEnum):
    """Text casing transformations for rendered titles."""

    NONE = "none"
    UPPER = "upper"
    TITLE = "title"


class TemplateMeta(BaseModel):
    """Template identifier and descriptive metadata."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str = Field(min_length=1)
    description: str = ""


class Canvas(BaseModel):
    """Target canvas dimensions and safe area margins."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    width: int = Field(gt=0)
    height: int = Field(gt=0)
    safe_margin_px: int = Field(default=0, ge=0)


class Box(BaseModel):
    """A rectangular bounding box on the canvas."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    x: int = Field(ge=0)
    y: int = Field(ge=0)
    w: int = Field(gt=0)
    h: int = Field(gt=0)


class BadgeBlock(BaseModel):
    """Visual style for the Part badge."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    fill: str = Field(pattern=_HEX_COLOR_PATTERN)
    padding_px: int = Field(default=0, ge=0)
    radius_px: int = Field(default=0, ge=0)


class TitleBlock(BaseModel):
    """Configuration for rendering the main video title."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    enabled: bool = True
    font: str = Field(min_length=1)
    max_lines: int = Field(default=1, gt=0)
    size_px: int = Field(gt=0)
    min_size_px: int = Field(gt=0)
    color: str = Field(pattern=_HEX_COLOR_PATTERN)
    stroke_px: int = Field(default=0, ge=0)
    stroke_color: str = Field(default="#000000", pattern=_HEX_COLOR_PATTERN)
    anchor: Anchor = Anchor.BOTTOM_LEFT
    box: Box
    case: TextCase = TextCase.NONE

    @field_validator("min_size_px")
    @classmethod
    def _validate_min_size(cls, value: int, info: ValidationInfo) -> int:
        size_px = info.data.get("size_px")
        if isinstance(size_px, int) and value > size_px:
            msg = f"min_size_px ({value}) must not exceed size_px ({size_px})"
            raise ValueError(msg)
        return value


class PartBlock(BaseModel):
    """Configuration for rendering the series Part badge."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    enabled: bool = True
    format: str = "PART {n}"
    font: str = Field(min_length=1)
    size_px: int = Field(gt=0)
    anchor: Anchor = Anchor.TOP_RIGHT
    badge: BadgeBlock | None = None


class NegativeSpace(BaseModel):
    """Region hints injected into provider prompt templates."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    hint: str = ""


class LayoutSpec(BaseModel):
    """Complete layout specification for a thumbnail template."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    template: TemplateMeta
    canvas: Canvas
    title: TitleBlock
    part: PartBlock
    negative_space: NegativeSpace

    @model_validator(mode="after")
    def _box_within_canvas(self) -> Self:
        box = self.title.box
        if box.x + box.w > self.canvas.width or box.y + box.h > self.canvas.height:
            msg = (
                f"title.box ({box.x},{box.y} {box.w}x{box.h}) extends past the "
                f"{self.canvas.width}x{self.canvas.height} canvas"
            )
            raise ValueError(msg)
        return self
