"""Unit tests for ``thumbforge provider`` (ROADMAP P3.5, phase-3 spec Commands table).

No network, no real `agy`, and no real keyring. `antigravity` is driven through a stub
`healthcheck`, and the keyring is replaced, because the keyring on a CI runner has no backend
and a test that wrote to the developer's credential store would be an unpleasant surprise.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest
from typer.testing import CliRunner

from thumbforge import credentials
from thumbforge.cli.app import app
from thumbforge.core.errors import ExitCode
from thumbforge.core.providers import Check, HealthReport
from thumbforge.providers import antigravity

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable
    from pathlib import Path

runner = CliRunner()


@pytest.fixture(autouse=True)
def _no_real_keyring(monkeypatch: pytest.MonkeyPatch) -> dict[tuple[str, str], str]:
    """Replace the OS credential store with a dict for the whole module."""
    store: dict[tuple[str, str], str] = {}

    def get_password(service: str, username: str) -> str | None:
        return store.get((service, username))

    def set_password(service: str, username: str, password: str) -> None:
        store[service, username] = password

    monkeypatch.setattr(credentials.keyring, "get_password", get_password)
    monkeypatch.setattr(credentials.keyring, "set_password", set_password)
    return store


def _healthcheck(
    *checks: Check, models: tuple[str, ...] = ()
) -> Callable[[object], Awaitable[HealthReport]]:
    """A stand-in `AntigravityProvider.healthcheck` returning a fixed report."""

    async def stub(_self: object) -> HealthReport:
        return HealthReport(checks=checks, models=models)

    return stub


def test_list_shows_every_registered_provider() -> None:
    result = runner.invoke(app, ["provider", "list"])

    assert result.exit_code == 0
    assert "fake" in result.stdout
    assert "antigravity" in result.stdout


def test_list_json_reports_capabilities_per_provider() -> None:
    """The JSON contract carries the full capability object, not the display summary."""
    result = runner.invoke(app, ["--json", "provider", "list"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    by_key = {row["key"]: row for row in payload["providers"]}
    assert payload["count"] == len(by_key)
    assert by_key["fake"]["auth"] == "ok"
    assert by_key["fake"]["capabilities"]["supports_seed"] is True
    # Measured in spike S3: the tool has no seed parameter.
    assert by_key["antigravity"]["capabilities"]["supports_seed"] is False
    assert by_key["antigravity"]["capabilities"]["max_concurrency"] == 2


def test_check_passes_for_the_offline_provider() -> None:
    result = runner.invoke(app, ["provider", "check", "fake"])

    assert result.exit_code == 0
    assert "no binary or credentials needed" in result.stdout


def test_check_on_an_unknown_key_exits_not_found() -> None:
    """Exit 3, and the hint lists what is installed, because the cause is usually a typo."""
    result = runner.invoke(app, ["provider", "check", "antigravty"])

    assert result.exit_code == ExitCode.NOT_FOUND
    assert "antigravity" in result.stderr


def test_check_reports_every_check_before_failing(monkeypatch: pytest.MonkeyPatch) -> None:
    """A failing check must not hide the passing ones: the table is printed, then the error."""
    monkeypatch.setattr(
        antigravity.AntigravityProvider,
        "healthcheck",
        _healthcheck(
            Check(name="binary", ok=True, detail="/usr/bin/agy"),
            Check(name="plugins", ok=True, detail="none installed"),
            Check(name="auth", ok=False, detail="could not list models"),
        ),
    )

    result = runner.invoke(app, ["provider", "check", "antigravity"])

    assert result.exit_code == ExitCode.PROVIDER
    assert "/usr/bin/agy" in result.stdout, "the passing checks are still shown"
    assert "FAILED" in result.stdout
    assert "provider_auth" in result.stderr, "a failed auth check is reported as an auth error"


def test_a_non_auth_failure_is_not_reported_as_an_auth_problem(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Both exit 4, but the machine-readable code is what tells the user where to look."""
    monkeypatch.setattr(
        antigravity.AntigravityProvider,
        "healthcheck",
        _healthcheck(Check(name="binary", ok=False, detail="'agy' is not on PATH")),
    )

    result = runner.invoke(app, ["--json", "provider", "check", "antigravity"])

    assert result.exit_code == ExitCode.PROVIDER
    assert json.loads(result.stderr)["error"] == "provider_permanent"


def test_models_lists_the_slugs_from_the_health_report(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        antigravity.AntigravityProvider,
        "healthcheck",
        _healthcheck(
            Check(name="auth", ok=True, detail="2 models available"),
            models=("gemini-3.1-pro-high", "claude-sonnet-4-6"),
        ),
    )

    result = runner.invoke(app, ["--json", "provider", "models", "antigravity"])

    assert result.exit_code == 0
    assert json.loads(result.stdout)["models"] == [
        "gemini-3.1-pro-high",
        "claude-sonnet-4-6",
    ]


def test_models_fails_rather_than_reporting_an_empty_list(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """ "No models" and "not signed in" look identical in output and must not be conflated."""
    monkeypatch.setattr(
        antigravity.AntigravityProvider,
        "healthcheck",
        _healthcheck(Check(name="auth", ok=False, detail="could not list models")),
    )

    result = runner.invoke(app, ["provider", "models", "antigravity"])

    assert result.exit_code == ExitCode.PROVIDER


def test_models_says_so_when_a_provider_has_no_model_selection() -> None:
    """`fake` is healthy and offers nothing; that is a 0, not a failure."""
    result = runner.invoke(app, ["provider", "models", "fake"])

    assert result.exit_code == 0
    assert "no model selection" in result.stdout


def test_set_key_stores_in_the_keyring(
    _no_real_keyring: dict[tuple[str, str], str],
) -> None:
    """Spec behaviour 5: works for `fake` even though it ignores keys, so the path is testable."""
    result = runner.invoke(app, ["provider", "set-key", "fake"], input="s3cret\n")

    assert result.exit_code == 0
    assert _no_real_keyring == {(credentials.SERVICE, "fake"): "s3cret"}
    assert "s3cret" not in result.stdout, "the secret must never be echoed back"


def test_set_key_rejects_an_unknown_provider_before_prompting(
    _no_real_keyring: dict[tuple[str, str], str],
) -> None:
    """A typo must cost a message, not a typed-out secret."""
    result = runner.invoke(app, ["provider", "set-key", "nope"], input="s3cret\n")

    assert result.exit_code == ExitCode.NOT_FOUND
    assert _no_real_keyring == {}
    assert "API key for" not in result.stdout


def test_set_key_refuses_an_empty_value(
    _no_real_keyring: dict[tuple[str, str], str],
) -> None:
    """A stored empty string reads back as "no key" while occupying a credential entry."""
    result = runner.invoke(app, ["provider", "set-key", "fake"], input="   \n")

    assert result.exit_code == ExitCode.PROVIDER
    assert _no_real_keyring == {}


def test_the_environment_beats_the_keyring(
    monkeypatch: pytest.MonkeyPatch, _no_real_keyring: dict[tuple[str, str], str]
) -> None:
    """`PLAN.md` §8 lookup order: the environment variable wins."""
    _no_real_keyring[credentials.SERVICE, "fake"] = "from-keyring"
    monkeypatch.setenv(credentials.env_var("fake"), "from-env")

    assert credentials.api_key("fake") == "from-env"

    monkeypatch.delenv(credentials.env_var("fake"))

    assert credentials.api_key("fake") == "from-keyring"


@pytest.mark.parametrize("blank", ["", "   ", "\t\n"])
def test_a_blank_environment_variable_falls_through_to_the_keyring(
    monkeypatch: pytest.MonkeyPatch, _no_real_keyring: dict[tuple[str, str], str], blank: str
) -> None:
    """An exported-but-empty variable is how shells leave unset values; it must not win.

    Whitespace-only is included because `""` alone is falsy and passes a plain truthiness
    check, leaving the real case — a variable holding a stray space — masking a good keyring
    entry. `store_api_key` rejects the same input.
    """
    _no_real_keyring[credentials.SERVICE, "fake"] = "from-keyring"
    monkeypatch.setenv(credentials.env_var("fake"), blank)

    assert credentials.api_key("fake") == "from-keyring"
    assert "keyring" in credentials.describe("fake"), "and `check` must not claim the env wins"


def test_an_unusable_keyring_reports_no_key_rather_than_failing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Reading is a question, not a demand: a CI runner has no backend at all."""
    from keyring.errors import NoKeyringError

    def explode(_service: str, _username: str) -> str | None:
        raise NoKeyringError

    monkeypatch.setattr(credentials.keyring, "get_password", explode)

    assert credentials.api_key("fake") is None


def test_an_unusable_keyring_is_fatal_when_storing(monkeypatch: pytest.MonkeyPatch) -> None:
    """Writing is a demand, and the hint has to name the fallback that needs no keyring."""
    from keyring.errors import NoKeyringError

    def explode(_service: str, _username: str, _password: str) -> None:
        raise NoKeyringError

    monkeypatch.setattr(credentials.keyring, "set_password", explode)

    result = runner.invoke(app, ["provider", "set-key", "fake"], input="s3cret\n")

    assert result.exit_code == ExitCode.PROVIDER
    assert "THUMBFORGE_PROVIDERS__FAKE__API_KEY" in result.stderr


def test_env_var_name_matches_the_settings_convention() -> None:
    """The variable that authenticates a provider follows pydantic-settings' nesting."""
    assert credentials.env_var("antigravity") == "THUMBFORGE_PROVIDERS__ANTIGRAVITY__API_KEY"


def test_provider_settings_reach_the_provider(tmp_path: Path) -> None:
    """`providers.antigravity.*` must actually configure the instance `provider list` builds.

    Asserted through the version the CLI reports: pointing `binary` at a path that cannot
    exist proves the section was passed through rather than defaulted.
    """
    config = tmp_path / "config.toml"
    config.write_text(
        '[providers.antigravity]\nbinary = "definitely-not-installed-agy"\n',
        encoding="utf-8",
    )

    result = runner.invoke(app, ["--json", "--config", str(config), "provider", "list"])

    assert result.exit_code == 0
    rows = {row["key"]: row for row in json.loads(result.stdout)["providers"]}
    assert rows["antigravity"]["version"] == "unknown"
    assert rows["antigravity"]["auth"] == "missing"


def test_check_names_the_keyring_backend_without_printing_the_key(
    monkeypatch: pytest.MonkeyPatch, _no_real_keyring: dict[tuple[str, str], str]
) -> None:
    """ADR 0014: a backend that stores nothing must be distinguishable from an empty one."""
    _no_real_keyring[credentials.SERVICE, "fake"] = "s3cret"
    monkeypatch.delenv(credentials.env_var("fake"), raising=False)

    result = runner.invoke(app, ["--json", "provider", "check", "fake"])

    assert result.exit_code == 0
    state = json.loads(result.stdout)["credentials"]
    assert "key in keyring" in state
    assert "backend:" in state
    assert "s3cret" not in result.stdout


def test_check_reports_the_environment_as_the_key_source(monkeypatch: pytest.MonkeyPatch) -> None:
    """The variable name is useful; its value is not, and must not be echoed."""
    monkeypatch.setenv(credentials.env_var("fake"), "s3cret")

    result = runner.invoke(app, ["--json", "provider", "check", "fake"])

    assert result.exit_code == 0
    assert json.loads(result.stdout)["credentials"] == (
        "key from THUMBFORGE_PROVIDERS__FAKE__API_KEY"
    )
    assert "s3cret" not in result.stdout


def test_a_missing_key_does_not_fail_a_healthy_provider() -> None:
    """No provider needs an API key yet, so the credential row is informational only."""
    result = runner.invoke(app, ["provider", "check", "fake"])

    assert result.exit_code == 0
    assert "no key stored" in result.stdout
