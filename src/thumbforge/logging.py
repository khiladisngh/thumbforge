"""structlog configuration (ADR 0015).

One pipeline for everything. Application code calls :func:`get_logger`; third-party libraries
(``yt_dlp``, ``sqlalchemy``, ``alembic``) keep using stdlib ``logging`` and are routed through the
same processors by :class:`structlog.stdlib.ProcessorFormatter`, so a run produces one coherent
stream rather than two competing formats.

Streams are strictly separated: **logs go to stderr**, command output goes to stdout. That is what
makes ``thumbforge --json ... > data.json`` safe to parse while diagnostics stay visible.

The file handler is always JSON and always at DEBUG, independent of console verbosity: when
something fails, the log already contains the detail, without asking the user to reproduce with
``-vv``.
"""

from __future__ import annotations

import logging
import logging.handlers
from typing import TYPE_CHECKING, Literal

import structlog

from thumbforge.core.redaction import REDACTED, is_secret_key, redact

if TYPE_CHECKING:
    from collections.abc import MutableMapping
    from pathlib import Path

    from structlog.stdlib import BoundLogger

LogFormat = Literal["console", "json"]

#: Rotating file handler size and count: 5 files x 5 MiB.
_LOG_BYTES = 5 * 1024 * 1024
_LOG_BACKUPS = 5


def redact_secrets(
    _logger: object,
    _method: str,
    event_dict: MutableMapping[str, object],
) -> MutableMapping[str, object]:
    """Replace secret-looking values anywhere in the event dict (ADR 0017).

    Logs reach disk and bug reports, so a provider key must never survive to a renderer. A
    secret is as likely to arrive nested — ``settings={"api_key": ...}`` — as at the top level,
    so the walk is recursive. The deny-list is shared with the settings loader via
    :mod:`thumbforge.core.redaction`.
    """
    for key in event_dict:
        event_dict[key] = REDACTED if is_secret_key(key) else redact(event_dict[key])
    return event_dict


#: Processors applied to every event, whatever its origin, before rendering.
_SHARED_PROCESSORS: list[structlog.typing.Processor] = [
    structlog.contextvars.merge_contextvars,
    structlog.stdlib.add_log_level,
    structlog.stdlib.add_logger_name,
    structlog.processors.TimeStamper(fmt="iso", utc=True),
    structlog.processors.StackInfoRenderer(),
    structlog.processors.format_exc_info,
    redact_secrets,
]


def level_from_flags(*, verbose: int = 0, quiet: bool = False, configured: str = "INFO") -> str:
    """Resolve the console level from the global flags.

    ``--quiet`` wins over ``-v`` because it is the more explicit instruction: a user who asks for
    silence while a script adds ``-v`` should get silence.
    """
    if quiet:
        return "ERROR"
    if verbose >= 2:  # -vv
        return "DEBUG"
    if verbose == 1:
        return "INFO"
    return configured


def configure_logging(
    *,
    level: str = "INFO",
    fmt: LogFormat = "console",
    log_file: Path | None = None,
    color: bool = True,
) -> None:
    """Configure structlog and the stdlib root logger. Safe to call more than once."""
    timestamped: structlog.typing.Processor = structlog.stdlib.ProcessorFormatter.wrap_for_formatter

    structlog.configure(
        processors=[*_SHARED_PROCESSORS, timestamped],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    console_renderer: structlog.typing.Processor = (
        structlog.processors.JSONRenderer()
        if fmt == "json"
        else structlog.dev.ConsoleRenderer(colors=color)
    )

    root = logging.getLogger()
    for handler in list(root.handlers):
        root.removeHandler(handler)
        handler.close()

    # stderr, never stdout: stdout belongs to command output.
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            processor=console_renderer,
            foreign_pre_chain=_SHARED_PROCESSORS,
        )
    )
    stream_handler.setLevel(level.upper())
    root.addHandler(stream_handler)

    file_error: OSError | None = None
    if log_file is not None:
        try:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=_LOG_BYTES,
                backupCount=_LOG_BACKUPS,
                encoding="utf-8",
            )
        except OSError as error:
            # A read-only or full state directory must not take the command down: logging is
            # support infrastructure, not the user's goal. Degrade to console and say so once.
            file_error = error
        else:
            file_handler.setFormatter(
                structlog.stdlib.ProcessorFormatter(
                    processor=structlog.processors.JSONRenderer(),
                    foreign_pre_chain=_SHARED_PROCESSORS,
                )
            )
            file_handler.setLevel(logging.DEBUG)
            root.addHandler(file_handler)

    # The root stays at DEBUG so the file handler can record everything; each handler filters.
    root.setLevel(logging.DEBUG)

    if file_error is not None:
        get_logger(__name__).warning(
            "file logging disabled",
            log_file=str(log_file),
            error=str(file_error),
            hint="console logging continues; check permissions on the state directory",
        )


def get_logger(name: str) -> BoundLogger:
    """Return a bound logger. Use ``get_logger(__name__)``."""
    return structlog.stdlib.get_logger(name)


def bind(**values: object) -> None:
    """Bind context onto every subsequent log record in this task (run id, provider, ...)."""
    structlog.contextvars.bind_contextvars(**values)


def clear_context() -> None:
    """Drop all bound context."""
    structlog.contextvars.clear_contextvars()
