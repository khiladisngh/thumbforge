"""`AntigravityProvider` error mapping and argv, with the CLI replaced (ROADMAP P3.4).

The subprocess is injected so every branch is reachable without the binary, credentials or
quota — including the one that matters most, where a timeout reports success. Live behaviour
is covered by the contract suite's `antigravity` case under `-m integration`.

Every envelope below is the shape spike S6 actually measured, not an invented one.
"""

from __future__ import annotations

import asyncio
import json
import sys
from typing import TYPE_CHECKING, Any, cast

import pytest
from PIL import Image

from thumbforge.core.errors import (
    ProviderAuthError,
    ProviderOutputMissingError,
    ProviderPermanentError,
    ProviderTimeoutError,
    ProviderTransientError,
)
from thumbforge.core.providers import GenerationRequest
from thumbforge.providers import antigravity
from thumbforge.providers.antigravity import AntigravityProvider, _aspect_words, _wrap

if TYPE_CHECKING:
    from pathlib import Path

CONVERSATION = "7e1fba60-8239-4676-8d44-019aabf43362"


def _request(**overrides: object) -> GenerationRequest:
    fields: dict[str, object] = {
        "prompt": "a lighthouse at dusk",
        "width": 1920,
        "height": 1080,
        "idempotency_key": "key01",
    }
    fields.update(overrides)
    return GenerationRequest.model_validate(fields)


def _envelope(**overrides: object) -> dict[str, Any]:
    """The success envelope measured in S2, which callers then mutate."""
    base: dict[str, Any] = {
        "conversation_id": CONVERSATION,
        "status": "SUCCESS",
        "response": "I generated the image.",
        "duration_seconds": 39.9,
        "num_turns": 1,
        "usage": {
            "input_tokens": 62753,
            "output_tokens": 4953,
            "thinking_tokens": 4459,
            "cache_read_tokens": 85548,
            "total_tokens": 67706,
        },
    }
    base.update(overrides)
    return base


class Runner:
    """Stands in for the subprocess, recording the argv it was given."""

    def __init__(self, stdout: str, stderr: str = "", returncode: int = 0) -> None:
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode
        self.argv: list[str] = []

    async def __call__(self, argv: list[str], cwd: Path) -> tuple[str, str, int]:
        self.argv = argv
        return self.stdout, self.stderr, self.returncode


def _provider(tmp_path: Path, runner: Runner, **config: object) -> AntigravityProvider:
    brain = tmp_path / "brain"
    brain.mkdir(exist_ok=True)
    return AntigravityProvider({"brain_dir": str(brain), **config}, run=runner)  # type: ignore[arg-type]


def _plant_image(
    tmp_path: Path,
    name: str = "lighthouse_1789896899337.jpg",
    colour: tuple[int, int, int] = (40, 60, 90),
) -> Path:
    """Put an image where `generate_image` would have written it (S2)."""
    directory = tmp_path / "brain" / CONVERSATION
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / name
    Image.new("RGB", (1376, 768), colour).save(path)
    return path


async def test_success_copies_the_image_out_of_the_brain_directory(tmp_path: Path) -> None:
    """S2: the tool takes no output path, so the adapter finds and copies the result."""
    _plant_image(tmp_path)
    runner = Runner(json.dumps(_envelope()))
    provider = _provider(tmp_path, runner)

    result = await provider.generate(_request(), workdir=tmp_path / "work")

    assert result.image_path == tmp_path / "work" / "key01.jpg"
    assert result.image_path.exists()
    assert result.provider_key == "antigravity"
    assert result.seed_used is None, "generate_image has no seed parameter (S3)"
    assert result.cost is not None
    assert (result.cost.tokens_in, result.cost.tokens_out) == (62753, 4953)
    assert result.cost.credits is None, "S8 measured no monetary field"


async def test_a_relayed_quota_error_is_retryable(tmp_path: Path) -> None:
    """The second "SUCCESS is not success" trap, found by a live run rather than a spike.

    The image model returned 429 `RESOURCE_EXHAUSTED`; the agent relayed it as prose inside a
    `SUCCESS` envelope with one turn, real token usage and no image. Classified as missing
    output it would be permanent, so a quota reset two hours away would abandon the batch
    item and blame the user's setup. The response text below is the one actually measured.
    """
    runner = Runner(
        json.dumps(
            _envelope(
                response=(
                    "The image generation request was sent with the specified prompt and 16:9 "
                    "aspect ratio, but the service returned a quota exhaustion error:\n\n"
                    "> **429 Too Many Requests**: `RESOURCE_EXHAUSTED` \u2014 You have "
                    "exhausted your capacity on the image model (`gemini-3.1-flash-image`). "
                    "Quota resets in approximately 2 hours and 20 minutes."
                ),
                num_turns=1,
            )
        )
    )

    with pytest.raises(ProviderTransientError) as caught:
        await _provider(tmp_path, runner).generate(_request(), workdir=tmp_path / "work")

    assert "RESOURCE_EXHAUSTED" in str(caught.value)
    assert caught.value.retryable is True


async def test_a_timeout_reporting_success_is_retryable(tmp_path: Path) -> None:
    """The finding that would have shipped a bug (S6c).

    `--print-timeout` expiry returns exit 0 with `status: SUCCESS`, an empty response and
    zero usage. Classified as missing output it would be permanent, and every slow
    generation would abandon its batch item instead of retrying.
    """
    runner = Runner(
        json.dumps(
            _envelope(
                response="",
                duration_seconds=0,
                usage={
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "thinking_tokens": 0,
                    "cache_read_tokens": 0,
                    "total_tokens": 0,
                },
            )
        ),
        stderr="[agy] print timeout after 1s with turn in progress; returning partial output",
    )
    provider = _provider(tmp_path, runner)

    with pytest.raises(ProviderTimeoutError) as caught:
        await provider.generate(_request(), workdir=tmp_path / "work")

    assert caught.value.retryable is True
    assert caught.value.hint is not None


async def test_success_with_no_image_is_permanent(tmp_path: Path) -> None:
    """Real work reported and still nothing produced is not worth retrying.

    Distinguished from the timeout above only by the response and usage being non-empty,
    which is why both tests exist: one flipped classification would be silent.
    """
    runner = Runner(json.dumps(_envelope()))
    provider = _provider(tmp_path, runner)

    with pytest.raises(ProviderOutputMissingError) as caught:
        await provider.generate(_request(), workdir=tmp_path / "work")

    assert caught.value.retryable is False
    assert "brain" in str(caught.value), "the message must name where it looked"


@pytest.mark.parametrize("status", ["CANCELED", "INTERRUPTED"])
async def test_interrupted_runs_are_retryable(tmp_path: Path, status: str) -> None:
    """An interrupted run says nothing about whether a retry would succeed."""
    runner = Runner(json.dumps(_envelope(status=status)))

    with pytest.raises(ProviderTransientError) as caught:
        await _provider(tmp_path, runner).generate(_request(), workdir=tmp_path / "work")

    assert caught.value.retryable is True


async def test_authentication_failure_is_reported_as_such(tmp_path: Path) -> None:
    """Mapped defensively: S6a could not verify this without signing the developer out."""
    runner = Runner(
        json.dumps(_envelope(status="ERROR", response="", error="authentication required")),
        returncode=1,
    )

    with pytest.raises(ProviderAuthError) as caught:
        await _provider(tmp_path, runner).generate(_request(), workdir=tmp_path / "work")

    assert caught.value.hint is not None


async def test_unknown_model_is_permanent(tmp_path: Path) -> None:
    """S6b: a bad `--model` exits 1 with a clean ERROR envelope; retrying cannot help."""
    runner = Runner(
        json.dumps(
            {
                "conversation_id": "",
                "status": "ERROR",
                "response": "",
                "error": 'invalid model selection (--model "does-not-exist")',
            }
        ),
        returncode=1,
    )

    with pytest.raises(ProviderPermanentError) as caught:
        await _provider(tmp_path, runner).generate(_request(), workdir=tmp_path / "work")

    assert "does-not-exist" in str(caught.value)


@pytest.mark.parametrize(
    ("label", "stdout"),
    [
        ("no output at all", ""),
        ("not json", "Traceback (most recent call last): ..."),
        ("json but not an object", "[1, 2, 3]"),
    ],
)
async def test_unusable_cli_output_is_permanent(tmp_path: Path, label: str, stdout: str) -> None:
    """A CLI change must surface as a diagnosable error, not a crash mid-pipeline."""
    runner = Runner(stdout, stderr="something went wrong", returncode=1)

    with pytest.raises(ProviderPermanentError):
        await _provider(tmp_path, runner).generate(_request(), workdir=tmp_path / "work")


async def test_a_non_image_file_is_not_accepted(tmp_path: Path) -> None:
    """A truncated or bogus file must fail here, not in Phase 5's fit step."""
    directory = tmp_path / "brain" / CONVERSATION
    directory.mkdir(parents=True)
    (directory / "broken.jpg").write_bytes(b"not an image")
    runner = Runner(json.dumps(_envelope()))

    with pytest.raises(ProviderOutputMissingError):
        await _provider(tmp_path, runner).generate(_request(), workdir=tmp_path / "work")


async def test_the_newest_image_wins_when_the_agent_generates_twice(tmp_path: Path) -> None:
    """The prompt forbids it, but the agent can still do it, and the run must not fail."""
    import os

    first = _plant_image(tmp_path, "first_1.jpg")
    second = _plant_image(tmp_path, "second_2.jpg", colour=(3, 4, 5))
    os.utime(second, (first.stat().st_atime + 10, first.stat().st_mtime + 10))
    runner = Runner(json.dumps(_envelope()))

    result = await _provider(tmp_path, runner).generate(_request(), workdir=tmp_path / "work")

    # Not merely "a file exists": a reversed sort would pass that. These bytes are `second`.
    assert result.image_path.read_bytes() == second.read_bytes()
    assert result.image_path.read_bytes() != first.read_bytes()


async def test_logs_are_written_next_to_the_image(tmp_path: Path) -> None:
    """`PLAN.md` §7.3 wants the raw streams kept per iteration for diagnosis."""
    _plant_image(tmp_path)
    runner = Runner(json.dumps(_envelope()), stderr="a warning from the CLI")

    await _provider(tmp_path, runner).generate(_request(), workdir=tmp_path / "work")

    assert (tmp_path / "work" / "key01.out").exists()
    assert (tmp_path / "work" / "key01.err").read_text(encoding="utf-8") == "a warning from the CLI"


async def test_argv_matches_the_measured_contract(tmp_path: Path) -> None:
    """Each flag here was verified in the spikes; `--continue` must never appear."""
    _plant_image(tmp_path)
    runner = Runner(json.dumps(_envelope()))
    provider = _provider(tmp_path, runner, timeout_s=300, model="Gemini 3.1 Pro (High)")

    await provider.generate(_request(), workdir=tmp_path / "work")

    assert runner.argv[0] == "agy"
    assert runner.argv[1] == "-p"
    assert "--output-format" in runner.argv
    assert runner.argv[runner.argv.index("--output-format") + 1] == "json"
    assert runner.argv[runner.argv.index("--print-timeout") + 1] == "300s"
    assert runner.argv[runner.argv.index("--model") + 1] == "Gemini 3.1 Pro (High)"
    assert runner.argv[runner.argv.index("--effort") + 1] == "low"
    assert "--continue" not in runner.argv, "every image is a fresh conversation (ADR 0013)"
    # S5 measured no permission grant being needed, so the dangerous flag is not default.
    assert "--dangerously-skip-permissions" not in runner.argv


async def test_skip_permissions_is_opt_in(tmp_path: Path) -> None:
    """It stays configurable for a restrictive `settings.json`, but off by default (S5)."""
    _plant_image(tmp_path)
    runner = Runner(json.dumps(_envelope()))

    await _provider(tmp_path, runner, skip_permissions=True).generate(
        _request(), workdir=tmp_path / "work"
    )

    assert "--dangerously-skip-permissions" in runner.argv


async def test_reference_directories_are_granted(tmp_path: Path) -> None:
    """The agent can only `view_file` a reference whose directory was added (S4)."""
    _plant_image(tmp_path)
    refs = tmp_path / "refs"
    refs.mkdir()
    reference = refs / "ref.png"
    Image.new("RGB", (8, 8), (1, 2, 3)).save(reference)
    runner = Runner(json.dumps(_envelope()))

    await _provider(tmp_path, runner).generate(
        _request(reference_images=(reference,)), workdir=tmp_path / "work"
    )

    assert str(refs) in runner.argv


async def test_missing_binary_is_reported_with_an_install_hint(tmp_path: Path) -> None:
    """Without the injected runner the real subprocess call is attempted."""
    provider = AntigravityProvider({"binary": "thumbforge-no-such-binary"})

    with pytest.raises(ProviderPermanentError) as caught:
        await provider.generate(_request(), workdir=tmp_path / "work")

    assert caught.value.hint is not None
    assert "Antigravity" in caught.value.hint


@pytest.mark.parametrize(
    ("width", "height", "expected"),
    [
        (1920, 1080, "16:9 widescreen"),
        (1280, 720, "16:9 widescreen"),
        (1024, 1024, "square 1:1"),
        (1080, 1920, "portrait"),
    ],
)
def test_aspect_is_described_in_words(width: int, height: int, expected: str) -> None:
    """S3: the ratio words are the only lever on output size, so they must be right."""
    assert expected in _aspect_words(width, height)


def test_the_wrapper_states_no_output_path() -> None:
    """S2: `generate_image` has no path parameter, so asking wastes a turn.

    The original ADR design instructed an exact absolute path; the agent replied explaining
    it could not comply and apologising, which is a turn of quota for nothing.
    """
    prompt = _wrap(_request(negative_prompt="people"))

    assert "16:9 widescreen" in prompt
    assert "exactly once" in prompt
    assert "people" in prompt
    assert ".jpg" not in prompt
    assert "save" in prompt.lower(), "it must still forbid the agent saving the file itself"


async def test_reap_tolerates_a_child_that_already_exited() -> None:
    """The kill can land after the child has gone, and that must not mask the timeout.

    `Process.kill()` on a reaped child raises `ProcessLookupError`; letting it escape would
    replace the timeout diagnosis with an unrelated traceback.
    """

    class Gone:
        waited = False

        def kill(self) -> None:
            raise ProcessLookupError

        async def wait(self) -> int:
            Gone.waited = True
            return 0

    await antigravity._reap(cast("Any", Gone()))

    assert Gone.waited is False, "wait() is unreachable once kill() raises"


async def test_reap_actually_kills_a_running_child() -> None:
    """The spec's acceptance criterion: after a timeout the child is gone.

    Uses a real process, because suppressing `ProcessLookupError` around a `kill()` that
    never happens would pass a stub-only test while leaking a subprocess per timeout.
    """
    process = await asyncio.create_subprocess_exec(
        sys.executable, "-c", "import time; time.sleep(30)"
    )

    await antigravity._reap(process)

    assert process.returncode is not None, "the child outlived the call"


async def test_a_hung_child_is_killed_and_reported_as_a_timeout(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The real subprocess path, which the injected runner bypasses everywhere else.

    Exercises `create_subprocess_exec`, the `wait_for` backstop for a child that ignores
    `--print-timeout`, and `_reap`. The grace period is patched to keep it fast; without
    that the floor is `_KILL_GRACE_S` seconds.
    """
    monkeypatch.setattr(antigravity, "_KILL_GRACE_S", 0)
    brain = tmp_path / "brain"
    brain.mkdir()
    provider = AntigravityProvider(
        {
            "brain_dir": str(brain),
            "binary": sys.executable,
            "timeout_s": 1,
        }
    )

    with pytest.raises(ProviderTimeoutError) as caught:
        await provider._invoke([sys.executable, "-c", "import time; time.sleep(30)"], tmp_path)

    assert "did not exit within" in str(caught.value)
    assert caught.value.retryable is True


async def test_a_models_timeout_is_not_reported_as_an_auth_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """An unanswered call is no evidence about credentials.

    Reported as `auth` it would tell a signed-in user to sign in. The check is named `models`
    instead and says the credentials could not be checked.
    """

    async def never_answers(_self: object, *_args: str, timeout: float) -> object:
        return antigravity.TIMED_OUT

    monkeypatch.setattr(antigravity.AntigravityProvider, "_capture", never_answers)
    monkeypatch.setattr(antigravity.shutil, "which", lambda _binary: "/usr/bin/agy")
    brain = tmp_path / "brain"
    brain.mkdir()

    report = await AntigravityProvider({"brain_dir": str(brain)}).healthcheck()

    named = {check.name: check for check in report.checks}
    assert "auth" not in named, "a timeout must not masquerade as an auth verdict"
    assert named["models"].ok is False
    assert "could not be checked" in named["models"].detail
    assert report.models == ()
    # The other checks survive: one failure must not hide the rest.
    assert {"binary", "version", "plugins"} <= set(named)


async def test_a_clean_models_failure_is_an_auth_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A non-zero exit from `agy models` is the one signal that the CLI is not signed in."""

    async def fails(_self: object, *_args: str, timeout: float) -> object:
        return None

    monkeypatch.setattr(antigravity.AntigravityProvider, "_capture", fails)
    monkeypatch.setattr(antigravity.shutil, "which", lambda _binary: "/usr/bin/agy")
    brain = tmp_path / "brain"
    brain.mkdir()

    report = await AntigravityProvider({"brain_dir": str(brain)}).healthcheck()

    named = {check.name: check for check in report.checks}
    assert named["auth"].ok is False
    assert "may not be signed in" in named["auth"].detail


def test_models_output_is_parsed_by_its_tab_not_its_banner() -> None:
    """`agy models` prefixes a progress line; keying off the tab ignores it by construction."""
    measured = (
        "Fetching available models...\n"
        "gemini-3.1-pro-high\tGemini 3.1 Pro (High)\n"
        "claude-sonnet-4-6\tClaude Sonnet 4.6 (Thinking)\n"
        # Not the measured banner: any future untabbed line must be ignored too. Filtering on
        # the banner text instead would turn this one into a model named after it.
        "Catalogue refreshed 2 seconds ago\n"
        "\n"
    )

    assert antigravity._parse_models(measured) == (
        "gemini-3.1-pro-high",
        "claude-sonnet-4-6",
    )


async def test_capture_classifies_a_real_timeout_rather_than_a_failure(tmp_path: Path) -> None:
    """Drives the actual `wait_for` expiry, which the healthcheck tests stub past.

    Without this, collapsing `TIMED_OUT` back into `None` goes unnoticed — and keeping a
    timeout out of the auth verdict is the entire reason the distinction exists.
    """
    brain = tmp_path / "brain"
    brain.mkdir()
    provider = AntigravityProvider({"brain_dir": str(brain), "binary": sys.executable})

    result = await provider._capture("-c", "import time; time.sleep(30)", timeout=0.25)

    assert result is antigravity.TIMED_OUT


async def test_capture_returns_none_for_a_clean_failure(tmp_path: Path) -> None:
    """A non-zero exit is the signal `_models` reads as "not signed in"."""
    brain = tmp_path / "brain"
    brain.mkdir()
    provider = AntigravityProvider({"brain_dir": str(brain), "binary": sys.executable})

    result = await provider._capture("-c", "raise SystemExit(3)", timeout=30)

    assert result is None
