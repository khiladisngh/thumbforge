"""Which keys count as secret, and that redaction never mutates the caller's data."""

from __future__ import annotations

import pytest

from thumbforge.core.redaction import REDACTED, find_secret_keys, is_secret_key, redact


@pytest.mark.parametrize(
    "key",
    [
        "api_key",
        "apiKey",
        "X-API-KEY",
        "ApiKey",
        "access_token",
        "refreshToken",
        "client_secret",
        "password",
        "db_password",
        "credentials",
        "Authorization",
        "Cookie",
        "Set-Cookie",
    ],
)
def test_credential_names_are_secret(key: str) -> None:
    assert is_secret_key(key)


@pytest.mark.parametrize(
    "key",
    [
        "monkey",
        "turkey",
        "keyboard",
        "width",
        "data_dir",
        "default_template",
        "tokenizer",
        "",
        # A bare trailing `key` is not a credential. These two matter concretely:
        # idempotency_key is logged on every batch iteration (PLAN.md 6), and the same
        # deny-list decides what config.toml may contain, so over-matching breaks settings.
        "idempotency_key",
        "primary_key",
        "key",
        "sort_key",
    ],
)
def test_ordinary_names_are_not_secret(key: str) -> None:
    """Word-boundary matching, and a trailing `key` alone does not make a field secret."""
    assert not is_secret_key(key)


@pytest.mark.parametrize("key", ["api_key", "apiKey", "private_key", "access_key", "secret_key"])
def test_key_is_secret_when_qualified_as_a_credential(key: str) -> None:
    assert is_secret_key(key)


def test_idempotency_key_survives_a_log_record() -> None:
    """The batch resume identifier must stay readable in logs, or debugging a run is blind."""
    event = {"idempotency_key": "abc123", "api_key": "sk-live"}
    assert redact(event) == {"idempotency_key": "abc123", "api_key": REDACTED}


def test_redaction_does_not_mutate_the_caller_structure() -> None:
    """Logging observes data; it must never alter a caller's dict."""
    original = {"providers": {"openai": {"api_key": "sk-live"}}, "width": 1920}
    result = redact(original)

    assert original["providers"] == {"openai": {"api_key": "sk-live"}}
    assert result == {"providers": {"openai": {"api_key": REDACTED}}, "width": 1920}


def test_find_secret_keys_reports_dotted_paths() -> None:
    found = find_secret_keys(
        {"providers": {"openai": {"api_key": "x"}}, "items": [{"access_token": "y"}]}
    )
    assert "providers.openai.api_key" in found
    assert "items[0].access_token" in found
