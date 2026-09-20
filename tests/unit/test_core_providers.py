"""Invariants the provider boundary models enforce (ADR 0010, ROADMAP P3.1/P3.2)."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from thumbforge.core.providers import Check, GenerationRequest, HealthReport


def _request(**overrides: object) -> GenerationRequest:
    fields: dict[str, object] = {
        "prompt": "a red bicycle",
        "width": 1280,
        "height": 720,
        "idempotency_key": "contract",
    }
    fields.update(overrides)
    return GenerationRequest.model_validate(fields)


@pytest.mark.parametrize(
    ("label", "key"),
    [
        ("parent traversal", "../../escaped"),
        ("absolute posix", "/etc/passwd"),
        ("absolute windows", "C:/windows/system32"),
        ("nested posix separator", "sub/evil"),
        ("nested windows separator", "sub\\evil"),
        ("bare parent", ".."),
        ("bare dot", "."),
        ("only dots", "...."),
        ("null byte", "ok\x00bad"),
        ("empty", ""),
    ],
)
def test_path_unsafe_idempotency_keys_are_rejected(label: str, key: str) -> None:
    """Providers join this onto a path, so it must not be able to leave the workdir.

    Measured before the constraint existed: `idempotency_key="../../escaped"` made
    `workdir / f"{key}.png"` resolve to `D:\\escaped.png`, and the provider then created the
    parent directory and wrote there. Validating on the model fixes it for every provider
    rather than asking each one to guard its own join.
    """
    with pytest.raises(ValidationError):
        _request(idempotency_key=key)


@pytest.mark.parametrize(
    "key",
    [
        "contract",
        "k1",
        "det-a",
        "run.01J9",
        "a" * 32,  # the sha256(...)[:32] that PLAN.md §6 actually supplies
    ],
)
def test_legitimate_idempotency_keys_are_accepted(key: str) -> None:
    """The constraint must not reject what `PLAN.md` §6 and the test suites really use."""
    assert _request(idempotency_key=key).idempotency_key == key


def test_over_long_key_is_rejected() -> None:
    """A filename has a length limit even when every character is safe."""
    with pytest.raises(ValidationError):
        _request(idempotency_key="a" * 65)


def test_health_report_ok_cannot_disagree_with_its_checks() -> None:
    """`ok` is derived, so a report cannot claim health while carrying a failure."""
    assert HealthReport().ok is True
    assert HealthReport(checks=(Check(name="a", ok=True),)).ok is True
    assert HealthReport(checks=(Check(name="a", ok=True), Check(name="b", ok=False))).ok is False


def test_health_report_rejects_a_supplied_ok() -> None:
    """`extra="forbid"` stops a caller asserting health that the checks contradict."""
    with pytest.raises(ValidationError):
        HealthReport.model_validate({"checks": [], "ok": True})


def test_requests_are_frozen() -> None:
    """A request is a value; mutating one after dispatch would desync it from its key."""
    request = _request()
    with pytest.raises(ValidationError):
        request.prompt = "changed"  # type: ignore[misc]
