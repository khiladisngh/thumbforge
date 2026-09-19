"""Error hierarchy and the exit codes it maps to.

Every failure the user can provoke is a :class:`ThumbforgeError` carrying a stable ``code``
(machine-readable), an ``exit_code`` (process status) and an optional ``hint`` (what to do about
it). ``cli/_errors.py`` is the only place allowed to turn these into a process exit.

Exit codes are contract, documented in ``PLAN.md`` §5.1 and relied on by scripts:

===== ==========================================================================
Code  Meaning
===== ==========================================================================
0     success
1     unexpected error (``SourceError``, uncaught exception)
2     usage or validation error (Typer default; ``TemplateError``, ``SettingsError``)
3     not found (video, playlist, run, iteration, template, provider)
4     provider error (auth, permanent, output missing, transient, timeout)
5     compliance failure
6     partial batch: some items failed, the run is resumable
130   interrupted (SIGINT)
===== ==========================================================================
"""

from __future__ import annotations

from enum import IntEnum


class ExitCode(IntEnum):
    """Process exit statuses. Values are a public contract."""

    OK = 0
    UNEXPECTED = 1
    USAGE = 2
    NOT_FOUND = 3
    PROVIDER = 4
    COMPLIANCE = 5
    PARTIAL = 6
    INTERRUPTED = 130


class ThumbforgeError(Exception):
    """Base class for every expected failure.

    Subclasses set ``code`` and ``exit_code`` as class attributes; instances may add a ``hint``.
    """

    code: str = "thumbforge_error"
    exit_code: ExitCode = ExitCode.UNEXPECTED

    def __init__(self, message: str, *, hint: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.hint = hint

    def __str__(self) -> str:
        return self.message


class SettingsError(ThumbforgeError):
    """Configuration is missing, malformed, or contains something it must not."""

    code = "settings"
    exit_code = ExitCode.USAGE


class TemplateError(ThumbforgeError):
    """A template's layout spec or prompt failed to load, validate or render."""

    code = "template"
    exit_code = ExitCode.USAGE


class NotFoundError(ThumbforgeError):
    """A referenced entity does not exist."""

    code = "not_found"
    exit_code = ExitCode.NOT_FOUND


class SourceError(ThumbforgeError):
    """A metadata source failed."""

    code = "source"
    exit_code = ExitCode.UNEXPECTED


class DatabaseError(ThumbforgeError):
    """A database operation failed (e.g. migration, lock, disk failure)."""

    code = "database"
    exit_code = ExitCode.UNEXPECTED


class AssetError(ThumbforgeError):
    """An asset could not be written, verified, or identified."""

    code = "asset"
    exit_code = ExitCode.UNEXPECTED


class ProviderError(ThumbforgeError):
    """Base class for image-provider failures."""

    code = "provider"
    exit_code = ExitCode.PROVIDER

    #: Whether retrying the same request could plausibly succeed.
    retryable: bool = False


class ProviderRegistryError(ProviderError):
    """Provider discovery failed: duplicate key, or a plugin that will not load."""

    code = "provider_registry"


class ProviderAuthError(ProviderError):
    """The provider rejected our credentials, or none were cached."""

    code = "provider_auth"


class ProviderPermanentError(ProviderError):
    """The provider failed in a way that retrying cannot fix."""

    code = "provider_permanent"


class ProviderTransientError(ProviderError):
    """The provider failed in a way that may succeed on retry."""

    code = "provider_transient"
    retryable = True


class ProviderTimeoutError(ProviderError):
    """The provider did not respond within its timeout."""

    code = "provider_timeout"
    retryable = True


class ProviderOutputMissingError(ProviderError):
    """The provider reported success but produced no usable image."""

    code = "provider_output_missing"


class ComplianceError(ThumbforgeError):
    """A generated image violates the YouTube thumbnail requirements."""

    code = "compliance"
    exit_code = ExitCode.COMPLIANCE


class PartialBatchError(ThumbforgeError):
    """A batch finished with some items failed; the run is resumable."""

    code = "partial_batch"
    exit_code = ExitCode.PARTIAL

    def __init__(
        self,
        message: str,
        *,
        hint: str | None = None,
        completed: int = 0,
        failed: int = 0,
        pending: int = 0,
    ) -> None:
        super().__init__(message, hint=hint)
        self.completed = completed
        self.failed = failed
        self.pending = pending
