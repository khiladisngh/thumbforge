"""``thumbforge config`` — inspect and edit the configuration file."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Annotated

import tomli_w
import typer
from rich.syntax import Syntax

from thumbforge.cli._errors import handle_errors
from thumbforge.cli._render import AppContext, JsonValue, emit, kv
from thumbforge.core.errors import SettingsError
from thumbforge.settings import (
    default_config_path,
    load_settings,
    set_values,
    write_default_config,
)

app = typer.Typer(
    name="config",
    help="Inspect and edit the configuration file.",
    no_args_is_help=True,
)


def _context(ctx: typer.Context) -> AppContext:
    obj = ctx.obj
    if not isinstance(obj, AppContext):  # pragma: no cover - the root callback always sets it
        msg = "CLI context was not initialised"
        raise SettingsError(msg)
    return obj


def _config_path(app_ctx: AppContext) -> Path:
    return app_ctx.config_path or default_config_path()


@app.command("init")
@handle_errors
def init_(
    ctx: typer.Context,
    force: Annotated[
        bool, typer.Option("--force", help="Overwrite an existing configuration file.")
    ] = False,
) -> None:
    """Write a commented configuration file with every default."""
    app_ctx = _context(ctx)
    path = write_default_config(_config_path(app_ctx), force=force)
    emit(
        app_ctx,
        {"written": str(path)},
        render=lambda: f"[green]wrote[/] {path}",
    )


@app.command("show")
@handle_errors
def show(ctx: typer.Context) -> None:
    """Print the effective configuration: defaults, overlaid by the file, then the environment."""
    app_ctx = _context(ctx)
    settings = load_settings(config_path=app_ctx.config_path, data_dir=app_ctx.data_dir)
    data: JsonValue = settings.model_dump(mode="json")
    emit(
        app_ctx,
        data,
        render=lambda: Syntax(
            _as_toml(settings.model_dump(mode="json")),
            "toml",
            theme="ansi_dark",
            background_color="default",
        ),
    )


@app.command("path")
@handle_errors
def path_(ctx: typer.Context) -> None:
    """Print the paths thumbforge reads and writes."""
    app_ctx = _context(ctx)
    settings = load_settings(config_path=app_ctx.config_path, data_dir=app_ctx.data_dir)
    paths = {
        "config": str(_config_path(app_ctx)),
        "data_dir": str(settings.general.data_dir),
        "state_dir": str(settings.state_dir),
        "db": str(settings.db_path),
        "assets": str(settings.assets_dir),
        "log": str(settings.log_file),
    }
    emit(app_ctx, paths, render=lambda: kv(paths))


@app.command("set")
@handle_errors
def set_(
    ctx: typer.Context,
    assignments: Annotated[
        list[str],
        typer.Argument(
            metavar="KEY=VALUE...",
            help="One or more assignments, for example output.width=1280 output.height=720.",
        ),
    ],
) -> None:
    """Set configuration keys, validating the result before writing.

    Several keys may be set at once, and must be when they are linked: output.width and
    output.height have to change together to keep the 16:9 ratio, because neither halfway
    state is a valid configuration.
    """
    app_ctx = _context(ctx)
    path = _config_path(app_ctx)

    parsed_pairs: dict[str, str] = {}
    for item in assignments:
        key, separator, value = item.partition("=")
        if not separator or not key:
            msg = f"expected KEY=VALUE, got {item!r}"
            raise SettingsError(msg, hint="for example: thumbforge config set output.quality=85")
        parsed_pairs[key.strip()] = value

    written = set_values(path, parsed_pairs)
    summary = ", ".join(f"{k} = {v!r}" for k, v in written.items())
    emit(
        app_ctx,
        {"set": {k: str(v) for k, v in written.items()}, "path": str(path)},
        render=lambda: f"[green]set[/] {summary} in {path}",
    )


def _as_toml(data: Mapping[str, JsonValue], prefix: str = "") -> str:
    """Render effective settings as TOML for display.

    ``tomli_w`` cannot serialise ``None``, which is a legitimate value here (an unset provider
    model), so those keys are shown commented as ``(unset)`` rather than silently dropped.
    """
    scalars = {k: v for k, v in data.items() if v is not None and not isinstance(v, Mapping)}
    unset = [k for k, v in data.items() if v is None]
    tables = {k: v for k, v in data.items() if isinstance(v, Mapping)}

    lines: list[str] = []
    if scalars:
        lines.append(tomli_w.dumps(dict(scalars)).rstrip())
    lines.extend(f"# {key} = (unset)" for key in unset)
    for name, values in tables.items():
        header = f"{prefix}.{name}" if prefix else name
        lines.append(f"\n[{header}]")
        lines.append(_as_toml(values, header).rstrip())
    return "\n".join(lines).strip() + "\n"
