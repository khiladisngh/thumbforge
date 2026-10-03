"""Jinja2 prompt rendering (ROADMAP P4.2, ADR 0006).

A prompt is plain text for an image provider, so the environment is deliberately not HTML:
``autoescape`` is off and ``StrictUndefined`` makes a typo in a template a loud failure rather
than a silently empty gap in the prompt.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import TYPE_CHECKING

from jinja2 import Environment, StrictUndefined, TemplateSyntaxError, UndefinedError
from jinja2 import TemplateError as JinjaTemplateError
from jinja2.utils import missing
from pydantic import BaseModel

from thumbforge.core.errors import TemplateError

if TYPE_CHECKING:
    from thumbforge.core.models import ChannelMeta, PlaylistMeta, VideoMeta


@dataclass(frozen=True, slots=True)
class RenderContext:
    """Everything a prompt template may reference, by these exact field names."""

    video: VideoMeta
    playlist: PlaylistMeta | None
    part_number: int | None
    part_label: str | None
    channel: ChannelMeta | None
    vars: Mapping[str, str]
    negative_space: str
    width: int
    height: int


class _NamedUndefined(StrictUndefined):
    """``StrictUndefined`` whose message carries the dotted path the template asked for.

    Jinja's own message is ``'dict object' has no attribute 'tone'``, which does not say
    which variable to supply. The only mapping in the context is ``vars``; the other
    objects are the ``*Meta`` models, whose class name gives the prefix (``video.genre``).
    Reading an attribute of ``None`` (no playlist, no channel) has no path to report, so it
    says so rather than naming the type.
    """

    @property
    def _undefined_message(self) -> str:
        owner = self._undefined_obj
        name = str(self._undefined_name)
        if self._undefined_hint:
            return self._undefined_hint
        if owner is missing:
            return f"undefined variable {name!r}"
        if isinstance(owner, Mapping):
            return f"undefined variable 'vars.{name}'"
        if isinstance(owner, BaseModel):
            return (
                f"undefined variable '{type(owner).__name__.removesuffix('Meta').lower()}.{name}'"
            )
        return f"undefined variable {name!r} on {'None' if owner is None else type(owner).__name__}"


_ENV = Environment(
    undefined=_NamedUndefined,
    autoescape=False,
    trim_blocks=True,
    lstrip_blocks=True,
)


def render_prompt(prompt_template: str, ctx: RenderContext, *, name: str) -> str:
    """Render ``prompt_template`` with ``ctx``; ``name`` is only used in error messages.

    Raises :class:`~thumbforge.core.errors.TemplateError` for a syntax error or any variable
    the template references that the context does not define.
    """
    try:
        template = _ENV.from_string(prompt_template)
        return template.render(
            video=ctx.video,
            playlist=ctx.playlist,
            part_number=ctx.part_number,
            part_label=ctx.part_label,
            channel=ctx.channel,
            vars=ctx.vars,
            negative_space=ctx.negative_space,
            width=ctx.width,
            height=ctx.height,
        )
    except TemplateSyntaxError as err:
        msg = f"syntax error in {name}, line {err.lineno}: {err.message}"
        raise TemplateError(msg) from err
    except UndefinedError as err:
        msg = f"{err.message} in {name}"
        raise TemplateError(msg) from err
    except (JinjaTemplateError, ArithmeticError, TypeError) as err:
        msg = f"cannot render {name}: {err}"
        raise TemplateError(msg) from err
