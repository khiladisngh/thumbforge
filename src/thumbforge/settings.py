"""Configuration: TOML file, ``THUMBFORGE_*`` environment variables, and defaults.

Precedence, highest first: CLI flags (applied by the caller), environment variables, the TOML
file, then defaults (ADR 0003). Paths come from :mod:`platformdirs` so the tool is XDG-correct on
Linux and uses the right locations on Windows and macOS.

Secrets never live here (ADR 0014): a TOML file containing a secret-looking key is rejected
outright rather than quietly ignored, because a user who put a key there needs to know it is not
being used and is sitting in plaintext.
"""

from __future__ import annotations

import os
import tempfile
import tomllib
from collections.abc import Mapping
from pathlib import Path
from typing import Annotated, Any, Literal, Self, cast

import tomli_w
from platformdirs import user_config_dir, user_data_dir, user_state_dir
from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_settings.sources import EnvSettingsSource, PydanticBaseSettingsSource

from thumbforge.core.errors import SettingsError
from thumbforge.core.redaction import find_secret_keys, is_secret_key

APP_NAME = "thumbforge"

# Secret detection lives in core.redaction so settings and logging share one deny-list.

_SECRET_HINT = (
    "set THUMBFORGE_PROVIDERS__<KEY>__API_KEY in the environment, "
    "or run `thumbforge provider set-key <provider>` to use the system keyring"
)


def default_config_path() -> Path:
    # appauthor=False: on Windows platformdirs otherwise nests under a vendor directory named
    # after the app, giving ...\thumbforge\thumbforge.
    return Path(user_config_dir(APP_NAME, appauthor=False)) / "config.toml"


def default_data_dir() -> Path:
    return Path(user_data_dir(APP_NAME, appauthor=False))


def default_state_dir() -> Path:
    return Path(user_state_dir(APP_NAME, appauthor=False))


class GeneralSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    data_dir: Path = Field(default_factory=default_data_dir)
    default_provider: str = "fake"
    default_template: str = "bold-title"


class OutputSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    width: Annotated[int, Field(ge=1280)] = 1920
    height: Annotated[int, Field(ge=720)] = 1080
    format: Literal["jpeg", "png"] = "jpeg"
    quality: Annotated[int, Field(ge=1, le=100)] = 90
    #: 2 MiB, YouTube's mobile upload limit; the desktop limit of 50 MiB is the hard ceiling.
    max_bytes: Annotated[int, Field(ge=1, le=52_428_800)] = 2_097_152

    @model_validator(mode="after")
    def _check_aspect_ratio(self) -> Self:
        if self.width * 9 != self.height * 16:
            msg = f"output must be 16:9, got {self.width}x{self.height}"
            raise ValueError(msg)
        return self


class BatchSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    concurrency: Annotated[int, Field(ge=1, le=32)] = 1
    max_retries: Annotated[int, Field(ge=0, le=10)] = 2
    stale_after_s: Annotated[int, Field(ge=1)] = 900


class AntigravitySettings(BaseModel):
    """How to invoke the Antigravity CLI (ADR 0013, measured in `docs/spikes/antigravity.md`)."""

    model_config = ConfigDict(extra="forbid")

    binary: str = "agy"
    model: str | None = None
    effort: Literal["low", "medium", "high"] = "low"
    timeout_s: Annotated[int, Field(ge=1)] = 600
    #: Spike S5 measured `generate_image` succeeding with neither this flag nor a
    #: `permissions.allow` rule, and again with `trustedWorkspaces` removed, so the default
    #: does not opt into `--dangerously-skip-permissions`. It stays configurable for users
    #: whose `settings.json` is more restrictive. Supersedes decision D4.
    skip_permissions: bool = False


class ProviderSettings(BaseModel):
    """Per-provider configuration, keyed by provider registry name."""

    model_config = ConfigDict(extra="forbid")

    antigravity: AntigravitySettings = Field(default_factory=AntigravitySettings)


class LoggingSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    format: Literal["console", "json"] = "console"


class ConfigSchema(BaseModel):
    """The shape of ``config.toml``, with no environment involvement.

    Kept separate from :class:`Settings` so a file can be validated on its own. Validating
    through ``Settings`` would overlay ``THUMBFORGE_*`` values, letting an environment variable
    mask an invalid value in the file — which would then be written to disk and fail later,
    once that variable is gone.
    """

    model_config = ConfigDict(extra="forbid")

    general: GeneralSettings = Field(default_factory=GeneralSettings)
    output: OutputSettings = Field(default_factory=OutputSettings)
    batch: BatchSettings = Field(default_factory=BatchSettings)
    providers: ProviderSettings = Field(default_factory=ProviderSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)


class _SecretFreeEnvSource(EnvSettingsSource):
    """Environment source that drops secret-looking variables before validation.

    The same deny-list that makes settings *refuse* a config file containing a secret makes
    the environment source *ignore* one, because the environment is exactly where a secret is
    supposed to live. `thumbforge.credentials` is the only reader.
    """

    def __call__(self) -> dict[str, Any]:
        return _drop_secrets(super().__call__())


def _drop_secrets(values: dict[str, Any]) -> dict[str, Any]:
    """Recursively remove secret-looking keys, and any section left empty by their removal.

    Emptied sections must go too: `providers.fake` surviving as `{}` is still an extra input
    under `extra="forbid"`, so dropping only the leaf would fix nothing for a provider that
    has no settings section of its own.
    """
    cleaned: dict[str, Any] = {}
    for key, value in values.items():
        if is_secret_key(key):
            continue
        if isinstance(value, dict):
            nested = _drop_secrets(cast("dict[str, Any]", value))
            if not nested:
                continue
            cleaned[key] = nested
            continue
        cleaned[key] = value
    return cleaned


class Settings(BaseSettings):
    """Effective configuration for one invocation: defaults, then file, then environment.

    The sections are redeclared rather than inherited from :class:`ConfigSchema`: pydantic
    requires a different ``model_config`` here (a ``SettingsConfigDict`` carrying the env
    prefix), and inheriting one while overriding the other is an incompatible override.
    """

    model_config = SettingsConfigDict(
        env_prefix="THUMBFORGE_",
        env_nested_delimiter="__",
        extra="forbid",
    )

    general: GeneralSettings = Field(default_factory=GeneralSettings)
    output: OutputSettings = Field(default_factory=OutputSettings)
    batch: BatchSettings = Field(default_factory=BatchSettings)
    providers: ProviderSettings = Field(default_factory=ProviderSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Default source order, with the environment source filtered of secrets.

        ``THUMBFORGE_PROVIDERS__<KEY>__API_KEY`` is the documented place to put a provider's
        key (ADR 0014), but ``env_nested_delimiter`` reads it as ``providers.<key>.api_key``,
        which ``extra="forbid"`` then rejects — so simply following the documentation made
        *every* command exit 2 with "Extra inputs are not permitted". Filtering here rather
        than declaring the field keeps the secret out of the settings model entirely, which
        matters because those sections are dumped into provider config and snapshotted into
        ``provider_profile.params_json``.
        """
        return (
            init_settings,
            _SecretFreeEnvSource(settings_cls),
            dotenv_settings,
            file_secret_settings,
        )

    @classmethod
    def from_sources(cls, file_values: Mapping[str, Any]) -> Settings:
        """Build settings where the environment outranks the TOML file.

        File values cannot simply be passed to ``Settings(**file_values)``: constructor
        arguments are the *highest* priority source in pydantic-settings, which would let the
        file silently beat ``THUMBFORGE_*`` variables. Instead the file is merged underneath
        whatever the environment supplies.
        """
        from_env = cls()
        merged = _deep_merge(dict(file_values), from_env.model_dump(exclude_unset=True))
        return cls(**merged)

    @property
    def db_path(self) -> Path:
        return self.general.data_dir / "thumbforge.sqlite3"

    @property
    def assets_dir(self) -> Path:
        return self.general.data_dir / "assets"

    @property
    def state_dir(self) -> Path:
        return default_state_dir()

    @property
    def log_file(self) -> Path:
        return self.state_dir / "logs" / "thumbforge.log"


def _deep_merge(base: dict[str, Any], override: Mapping[str, Any]) -> dict[str, Any]:
    """Merge ``override`` into ``base``, recursing into nested tables."""
    for key, value in override.items():
        existing = base.get(key)
        if isinstance(existing, dict) and isinstance(value, Mapping):
            base[key] = _deep_merge(
                cast("dict[str, Any]", existing),
                cast("Mapping[str, Any]", value),
            )
        else:
            base[key] = value
    return base


def _read_toml(path: Path) -> dict[str, Any]:
    try:
        with path.open("rb") as handle:
            return tomllib.load(handle)
    except tomllib.TOMLDecodeError as error:
        msg = f"{path} is not valid TOML: {error}"
        hint = "run `thumbforge config init --force` to rewrite it"
        raise SettingsError(msg, hint=hint) from error
    except OSError as error:
        msg = f"cannot read {path}: {error}"
        raise SettingsError(msg) from error


def _reject_secrets(data: dict[str, Any], path: Path) -> None:
    secrets = find_secret_keys(data)
    if not secrets:
        return
    msg = f"{path} contains secret-looking keys: {', '.join(sorted(secrets))}"
    raise SettingsError(msg, hint=_SECRET_HINT)


def load_settings(
    *,
    config_path: Path | None = None,
    data_dir: Path | None = None,
) -> Settings:
    """Build the effective settings.

    ``config_path`` and ``data_dir`` are the CLI overrides and win over everything else. A
    missing config file is not an error: defaults plus environment are a valid configuration.
    """
    resolved_config = config_path or default_config_path()
    file_values: dict[str, Any] = {}
    if resolved_config.is_file():
        file_values = _read_toml(resolved_config)
        _reject_secrets(file_values, resolved_config)

    try:
        settings = Settings.from_sources(file_values)
    except ValidationError as error:
        # The failing value may have come from the file or from THUMBFORGE_*; naming only the
        # file sends users to edit something that may not even exist.
        source = str(resolved_config) if resolved_config.is_file() else "built-in defaults"
        msg = (
            f"invalid configuration ({source}, overlaid with THUMBFORGE_* environment "
            f"variables): {_format_validation_error(error)}"
        )
        raise SettingsError(msg) from error

    if data_dir is not None:
        settings = settings.model_copy(
            update={"general": settings.general.model_copy(update={"data_dir": data_dir})}
        )
    return settings


def _format_validation_error(error: ValidationError) -> str:
    parts = [f"{'.'.join(str(p) for p in item['loc'])}: {item['msg']}" for item in error.errors()]
    return "; ".join(parts)


def _atomic_write(path: Path, payload: bytes) -> None:
    """Replace ``path`` atomically: write a sibling temp file, fsync, then rename.

    A direct write leaves a truncated file visible if the process dies mid-write, and a
    concurrent reader can observe a partial document. ``os.replace`` is atomic on POSIX and
    Windows when source and destination share a directory.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temp_name = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    temp_path = Path(temp_name)
    try:
        with os.fdopen(handle, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_path, path)
    except BaseException:
        temp_path.unlink(missing_ok=True)
        raise


def write_default_config(config_path: Path, *, force: bool = False) -> Path:
    """Write the commented default configuration, refusing to clobber unless ``force``."""
    if config_path.exists() and not force:
        msg = f"{config_path} already exists"
        raise SettingsError(msg, hint="pass --force to overwrite it")
    _atomic_write(config_path, default_config_toml().encode("utf-8"))
    return config_path


def default_config_toml() -> str:
    """Render the default configuration as commented TOML for ``config init``."""
    # ConfigSchema, not Settings: `Settings()` would read THUMBFORGE_* and bake the current
    # shell's overrides into the file as if they were defaults.
    defaults = ConfigSchema()
    return f"""\
# thumbforge configuration
# Every value below is a default; delete a line to keep following the default.
# Environment variables override this file: THUMBFORGE_OUTPUT__WIDTH=1280
# Secrets do NOT belong here - use the environment or `thumbforge provider set-key`.

[general]
data_dir = {_toml_value(str(defaults.general.data_dir))}
default_provider = {_toml_value(defaults.general.default_provider)}
default_template = {_toml_value(defaults.general.default_template)}

[output]
width = {defaults.output.width}
height = {defaults.output.height}
format = {_toml_value(defaults.output.format)}      # "jpeg" | "png"
quality = {defaults.output.quality}
max_bytes = {defaults.output.max_bytes}   # 2 MiB; YouTube allows up to 50 MiB from desktop

[batch]
concurrency = {defaults.batch.concurrency}
max_retries = {defaults.batch.max_retries}
stale_after_s = {defaults.batch.stale_after_s}

[providers.antigravity]
binary = {_toml_value(defaults.providers.antigravity.binary)}
# model = "gemini-3.1-pro-high"   # slug from `agy models`; omit for the provider default
effort = {_toml_value(defaults.providers.antigravity.effort)}          # low | medium | high
timeout_s = {defaults.providers.antigravity.timeout_s}
skip_permissions = {str(defaults.providers.antigravity.skip_permissions).lower()}

[logging]
level = {_toml_value(defaults.logging.level)}
format = {_toml_value(defaults.logging.format)}   # console | json
"""


def _toml_value(value: str) -> str:
    return tomli_w.dumps({"v": value}).split("=", 1)[1].strip()


def set_values(config_path: Path, assignments: Mapping[str, str]) -> dict[str, object]:
    """Apply several dotted keys to the TOML file, validating the result once.

    All assignments are applied together and the file is written only if the resulting
    configuration validates, so a rejected edit leaves the previous file untouched. Applying
    them together is required, not a convenience: cross-field invariants such as the 16:9
    output ratio cannot be satisfied by changing ``output.width`` and ``output.height`` one at
    a time, since neither intermediate state is valid.
    """
    data = _read_toml(config_path) if config_path.is_file() else {}
    parsed_values: dict[str, object] = {}

    for dotted_key, raw in assignments.items():
        segments = dotted_key.split(".")
        if len(segments) < 2 or any(not segment for segment in segments):
            msg = f"expected a dotted key such as output.width, got {dotted_key!r}"
            raise SettingsError(msg, hint="see `thumbforge config show` for available keys")

        parsed = _parse_scalar(raw)
        parsed_values[dotted_key] = parsed

        cursor: dict[str, Any] = data
        for segment in segments[:-1]:
            existing = cursor.get(segment)
            if existing is None:
                existing = {}
                cursor[segment] = existing
            elif not isinstance(existing, dict):
                msg = f"{dotted_key} conflicts with the existing value at {segment!r}"
                raise SettingsError(msg)
            cursor = cast("dict[str, Any]", existing)
        cursor[segments[-1]] = parsed

    _reject_secrets(data, config_path)
    try:
        # ConfigSchema, not Settings: the file must stand on its own, or a THUMBFORGE_*
        # override could mask an invalid value and we would persist a file that breaks the
        # next run without that variable set.
        ConfigSchema.model_validate(data)
    except ValidationError as error:
        shown = ", ".join(f"{k}={v!r}" for k, v in assignments.items())
        msg = f"{shown} is invalid: {_format_validation_error(error)}"
        raise SettingsError(msg) from error

    config_path.parent.mkdir(parents=True, exist_ok=True)
    _atomic_write(config_path, tomli_w.dumps(data).encode("utf-8"))
    return parsed_values


def _parse_scalar(raw: str) -> object:
    """Parse a CLI value using TOML scalar rules, falling back to a bare string.

    ``config set output.width 1280`` must store an integer, not ``"1280"``, or the schema
    rejects it.
    """
    try:
        return tomllib.loads(f"v = {raw}")["v"]
    except tomllib.TOMLDecodeError:
        return raw
