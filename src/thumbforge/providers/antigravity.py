"""`AntigravityProvider` — drives the Antigravity CLI headlessly (ADR 0013, ROADMAP P3.4).

Every design choice here is a measurement from `docs/spikes/antigravity.md`, not a reading of
the vendor docs. The four that shape the module:

- **`generate_image` takes only `ImageName` and `Prompt`** (S3). There is no path, size,
  seed or reference parameter, so the wrapper prompt states none of them. The one lever on
  output size is the words "16:9 widescreen", which produced 1376x768 in 5 of 5 runs.
- **The image lands in `~/.gemini/antigravity-cli/brain/<conversation_id>/`** (S2), not in
  `--add-dir` and not in `scratch/`. The envelope returns the `conversation_id`, so the path
  is discoverable; it is then copied into the caller's `workdir`.
- **A `--print-timeout` expiry looks like success** (S6c): exit `0`, `status: "SUCCESS"`,
  empty `response`, zero `usage`. It must be classified before "success but no image", or
  every slow generation becomes a permanent failure and its batch item is abandoned.
- **`generate_image` needs no permission grant** (S5, confirmed twice — once with
  `trustedWorkspaces` removed), so `skip_permissions` defaults to `false`.
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import shutil
import time
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, Final, cast

from PIL import Image, UnidentifiedImageError

from thumbforge.core.errors import (
    ProviderAuthError,
    ProviderOutputMissingError,
    ProviderPermanentError,
    ProviderTimeoutError,
    ProviderTransientError,
)
from thumbforge.core.providers import (
    Check,
    Cost,
    GenerationResult,
    HealthReport,
    ProviderCapabilities,
    ProviderInfo,
)
from thumbforge.logging import get_logger

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable, Mapping, Sequence

    from thumbforge.core.json import JsonPayload, JsonValue
    from thumbforge.core.providers import GenerationRequest

    #: `(argv, cwd) -> (stdout, stderr, returncode)`. Tests substitute the subprocess so
    #: every branch of the error mapping is reachable without the binary or quota.
    type CliRunner = Callable[[list[str], Path], Awaitable[tuple[str, str, int]]]

log = get_logger(__name__)

#: Where the CLI keeps its per-conversation working directories (S2).
DEFAULT_BRAIN_DIR: Final = Path.home() / ".gemini" / "antigravity-cli" / "brain"
#: Globally installed plugins, which every headless run inherits (S4).
PLUGINS_DIR: Final = Path.home() / ".gemini" / "config" / "plugins"

#: Extensions `generate_image` is known to emit. JPEG in 7 of 7 runs (S3); PNG is listed
#: only so a future change of format is copied rather than reported as a missing output.
_IMAGE_SUFFIXES: Final = (".jpg", ".jpeg", ".png")

#: Grace added to `--print-timeout` before the process is killed outright. The CLI is
#: expected to return its own timeout envelope first; this is the backstop for a hung child.
_KILL_GRACE_S: Final = 30

_CAPABILITIES: Final = ProviderCapabilities(
    # S4: the agent reads a reference with `view_file` and *describes* it into the prompt.
    # There is no image-to-image conditioning, so two runs from one reference are not
    # pixel-consistent and this must not be advertised as reference support.
    supports_reference_image=False,
    # S3: `generate_image` has no seed parameter, so nothing is reproducible by seed.
    supports_seed=False,
    # Prompt-only: the wrapper folds the negative prompt into the instructions.
    supports_negative_prompt=True,
    # Influence only. The ratio words steer the result; the exact size is never guaranteed.
    supports_aspect_ratio=True,
    max_batch=1,
    # S7: two concurrent runs both succeeded and were faster per run than sequential ones.
    max_concurrency=2,
    output_formats=frozenset({"jpeg"}),
)

#: The wrapper prompt. A module constant rather than the `antigravity_wrapper.j2` the ADR
#: named: it needs no template engine (Jinja2 arrives with Phase 4's *user-authored*
#: templates), and a packaged data file would have to be declared in the wheel, where a
#: constant cannot go missing. Every line earns its place — the negatives exist because a
#: run that calls extra tools or generates twice costs quota and returns an ambiguous
#: `brain/` directory.
_WRAPPER = """\
Use your image generation tool exactly once to create this image.

Subject: {prompt}

Requirements:
- {aspect} — state this to the image tool, it is the only control over the output shape.
- Leave clear negative space; text will be composited over the art afterwards, so do not
  render any words, letters, numbers or logos in the image.
{negative}{references}
Do not run any shell commands. Do not use any tool other than image generation. Do not
generate more than one image. Do not attempt to save, move or copy the file yourself.
"""


def _wrap(request: GenerationRequest) -> str:
    """Build the prompt sent to `agy -p`.

    The aspect ratio is given in words because S3 measured that as the only thing that
    changes the output shape; stating exact pixels alongside it changed nothing, and
    omitting the words produced 1024x1024 or 1264x848 instead of 1376x768.
    """
    negative = ""
    if request.negative_prompt:
        negative = f"- Avoid entirely: {request.negative_prompt}\n"

    references = ""
    if request.reference_images:
        listed = "\n".join(f"    {path}" for path in request.reference_images)
        references = (
            "- Match the visual style and colour palette of these reference images. View\n"
            "  each one first, then describe its style to the image tool:\n"
            f"{listed}\n"
        )

    return _WRAPPER.format(
        prompt=request.prompt,
        aspect=_aspect_words(request.width, request.height),
        negative=negative,
        references=references,
    )


def _aspect_words(width: int, height: int) -> str:
    """Describe the requested shape in words the image tool responds to.

    16:9 is named explicitly because that is the ratio S3 measured, and thumbforge's own
    output is always 16:9 (`OutputSettings` enforces it). Anything else is described
    generically rather than silently requested as 16:9.
    """
    ratio = width / height
    if abs(ratio - 16 / 9) < 0.02:
        return "16:9 widescreen"
    if abs(ratio - 1.0) < 0.02:
        return "square 1:1"
    orientation = "landscape" if ratio > 1 else "portrait"
    return f"{orientation}, aspect ratio {width}:{height}"


class AntigravityProvider:
    """Generate an image by driving `agy` in headless mode."""

    key: ClassVar[str] = "antigravity"

    def __init__(
        self,
        config: Mapping[str, JsonValue] | None = None,
        *,
        run: CliRunner | None = None,
    ) -> None:
        """Read the provider's own config slice; `run` is injected by tests only.

        `run` replaces the subprocess call so the unit tests can exercise every branch of
        the error mapping — including the timeout that reports success — without the binary,
        credentials or quota. It is not part of the registry contract.
        """
        settings = dict(config or {})
        self._binary = _as_str(settings.get("binary"), "agy")
        self._model = _as_str(settings.get("model"), "") or None
        self._effort = _as_str(settings.get("effort"), "low") or None
        self._timeout_s = _as_int(settings.get("timeout_s"), 600)
        self._skip_permissions = settings.get("skip_permissions") is True
        self._brain_dir = Path(_as_str(settings.get("brain_dir"), str(DEFAULT_BRAIN_DIR)))
        self._run = run
        #: Cached so a batch does not spawn `agy --version` once per image.
        self._version_cache: str | None = None

    @property
    def capabilities(self) -> ProviderCapabilities:
        """Measured in spikes S3, S4 and S7 — see the module docstring."""
        return _CAPABILITIES

    async def info(self) -> ProviderInfo:
        """Report the CLI version, and auth as `unknown` rather than guessing.

        `unknown` is deliberate: proving authentication costs a real generation, and S6a
        could not even isolate an unauthenticated profile. Reporting `missing` on a hunch
        would tell users to fix something that works.
        """
        version = await self._version()
        return ProviderInfo(
            key=self.key,
            name="Antigravity CLI",
            version=version or "unknown",
            auth="unknown" if version else "missing",
        )

    async def healthcheck(self) -> HealthReport:
        """Report every check, so one failure does not hide the others."""
        binary_path = shutil.which(self._binary)
        checks = [
            Check(
                name="binary",
                ok=binary_path is not None,
                detail=binary_path or f"{self._binary!r} is not on PATH",
            )
        ]

        version = await self._version() if binary_path else None
        checks.append(
            Check(name="version", ok=version is not None, detail=version or "could not be read")
        )

        # S4: every headless run inherits these, so generation is not a pure function of
        # thumbforge's inputs. Reported as a passing check with detail rather than a failure
        # — plugins are not broken, but they make a cross-machine difference diagnosable.
        plugins = (
            sorted(entry.name for entry in PLUGINS_DIR.iterdir()) if PLUGINS_DIR.is_dir() else []
        )
        checks.append(
            Check(
                name="plugins",
                ok=True,
                detail=", ".join(plugins) + " (inherited by every run)"
                if plugins
                else "none installed",
            )
        )

        return HealthReport(checks=tuple(checks))

    async def generate(self, request: GenerationRequest, *, workdir: Path) -> GenerationResult:
        """Run one generation and copy its output into `workdir`."""
        started = time.perf_counter()
        workdir.mkdir(parents=True, exist_ok=True)

        argv = self._argv(_wrap(request), workdir, request.reference_images)
        stdout, stderr, returncode = await self._invoke(argv, workdir)
        _write_logs(workdir, request.idempotency_key, stdout, stderr)

        envelope = _parse_envelope(stdout, stderr, returncode)
        _raise_for_envelope(envelope, stderr)

        conversation_id = _as_str(envelope.get("conversation_id"), "")
        produced = self._locate_output(conversation_id, stderr)
        destination = workdir / f"{request.idempotency_key}.jpg"
        shutil.copyfile(produced, destination)
        _verify_image(destination)

        usage = envelope.get("usage")
        return GenerationResult(
            image_path=destination,
            provider_key=self.key,
            # From `agy --version`, not the envelope: the envelope carries no version field
            # (measured — its keys are conversation_id, status, response, duration_seconds,
            # num_turns, usage), so reading it there left every stored row saying "unknown".
            provider_version=await self._version() or "unknown",
            model=self._model,
            # S3: `generate_image` has no seed parameter, so nothing was seeded.
            seed_used=None,
            duration_ms=int((time.perf_counter() - started) * 1000),
            cost=_cost(usage),
            raw_response=_redacted(envelope),
        )

    def _argv(self, prompt: str, workdir: Path, references: Sequence[Path]) -> list[str]:
        """Assemble the command line. Never `--continue`: every image is a fresh run."""
        argv = [
            self._binary,
            "-p",
            prompt,
            "--output-format",
            "json",
            "--add-dir",
            str(workdir),
            "--print-timeout",
            f"{self._timeout_s}s",
        ]
        # The agent can only `view_file` a reference if its directory is granted.
        for directory in dict.fromkeys(str(path.parent) for path in references):
            argv += ["--add-dir", directory]
        if self._skip_permissions:
            argv.append("--dangerously-skip-permissions")
        if self._model:
            argv += ["--model", self._model]
        if self._effort:
            argv += ["--effort", self._effort]
        return argv

    async def _invoke(self, argv: Sequence[str], cwd: Path) -> tuple[str, str, int]:
        """Run the CLI, or the injected stand-in, and return its output."""
        if self._run is not None:
            return await self._run(list(argv), cwd)

        try:
            process = await asyncio.create_subprocess_exec(
                *argv,
                cwd=cwd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        except FileNotFoundError as exc:
            msg = f"{self._binary!r} is not on PATH"
            raise ProviderPermanentError(msg, hint="install the Antigravity CLI") from exc

        try:
            # The CLI should return its own timeout envelope well before this fires; the
            # backstop exists for a child that hangs without honouring --print-timeout.
            out, err = await asyncio.wait_for(
                process.communicate(), timeout=self._timeout_s + _KILL_GRACE_S
            )
        except TimeoutError as exc:
            process.kill()
            with contextlib.suppress(ProcessLookupError):
                await process.wait()
            msg = f"{self._binary} did not exit within {self._timeout_s + _KILL_GRACE_S}s"
            raise ProviderTimeoutError(msg, hint="raise providers.antigravity.timeout_s") from exc

        return out.decode(errors="replace"), err.decode(errors="replace"), process.returncode or 0

    def _locate_output(self, conversation_id: str, stderr: str) -> Path:
        """Find the image `generate_image` wrote, in the conversation's brain directory.

        S2: the tool takes no output path, so the file cannot be predicted by name — only
        the directory, which the envelope's `conversation_id` identifies.
        """
        directory = self._brain_dir / conversation_id if conversation_id else None
        candidates = (
            sorted(
                (path for path in directory.iterdir() if path.suffix.lower() in _IMAGE_SUFFIXES),
                key=lambda path: path.stat().st_mtime,
            )
            if directory is not None and directory.is_dir()
            else []
        )

        if not candidates:
            # No timeout check here: `_raise_for_envelope` already classified that case, so
            # reaching this point means the CLI reported real work and still produced
            # nothing — which is permanent, not worth retrying.
            msg = f"no image in {directory or self._brain_dir}"
            raise ProviderOutputMissingError(
                msg,
                hint="the agent may have skipped its image tool; check the run log",
            )

        if len(candidates) > 1:
            # More than one means the agent generated twice despite being told not to. The
            # newest is the one it settled on, but the run cost double, so say so.
            log.warning(
                "antigravity.multiple_images",
                count=len(candidates),
                conversation_id=conversation_id,
                stderr=stderr[-200:],
            )
        return candidates[-1]

    async def _version(self) -> str | None:
        """Read `agy --version`, or `None` when the binary is absent or unusable."""
        if self._version_cache is not None:
            return self._version_cache
        if self._run is not None:
            return "injected"
        if shutil.which(self._binary) is None:
            return None
        try:
            process = await asyncio.create_subprocess_exec(
                self._binary,
                "--version",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            out, _ = await asyncio.wait_for(process.communicate(), timeout=30)
        except OSError, TimeoutError:
            return None
        self._version_cache = out.decode(errors="replace").strip() or None
        return self._version_cache


def _parse_envelope(stdout: str, stderr: str, returncode: int) -> JsonPayload:
    """Read the single JSON envelope, or explain why there isn't one."""
    text = stdout.strip()
    if not text:
        detail = stderr.strip()[-300:] or f"exit code {returncode}"
        msg = f"the CLI produced no JSON envelope: {detail}"
        raise ProviderPermanentError(msg, hint="run the same command manually to see its output")
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        msg = f"the CLI produced unparseable output: {text[:200]}"
        raise ProviderPermanentError(msg, hint="check for a CLI version change") from exc
    if not isinstance(parsed, dict):
        msg = f"expected a JSON object envelope, got {type(parsed).__name__}"
        raise ProviderPermanentError(msg, hint="check for a CLI version change")
    # `json.loads` is untyped by nature; the isinstance above is the real check and the cast
    # is the boundary. Every field is read back through `_as_str`/`_as_int`, never trusted.
    return cast("JsonPayload", parsed)


def _looks_like_timeout(envelope: JsonPayload) -> bool:
    """Whether a `SUCCESS` envelope is really agy's print timeout.

    S6c measured the signature: exit 0, `status: "SUCCESS"`, an empty `response`, and an
    all-zero `usage`. Nothing else reports success while having done no work.
    """
    if envelope.get("status") != "SUCCESS":
        return False
    if _as_str(envelope.get("response"), "").strip():
        return False
    usage = envelope.get("usage")
    total = usage.get("total_tokens") if isinstance(usage, dict) else None
    return total in {0, None}


def _raise_for_envelope(envelope: JsonPayload, stderr: str) -> None:
    """Classify a non-success envelope. Order is load-bearing — see the module docstring."""
    status = _as_str(envelope.get("status"), "")

    # FIRST: a print timeout presents as SUCCESS with nothing done. Classified here so it
    # cannot fall through to the non-retryable "no image produced" case below.
    if _looks_like_timeout(envelope):
        msg = "the CLI returned SUCCESS with an empty response, which is its print timeout"
        raise ProviderTimeoutError(msg, hint="raise providers.antigravity.timeout_s")

    if status == "SUCCESS":
        return

    if status in {"CANCELED", "INTERRUPTED"}:
        msg = f"the CLI reported {status}"
        raise ProviderTransientError(msg, hint="the run was interrupted; retrying is safe")

    error = _as_str(envelope.get("error"), "") or stderr.strip()
    if "authentication required" in error.lower():
        # Defensive: S6a could not verify this, because isolating an unauthenticated
        # profile proved impossible without signing the developer out.
        msg = "the CLI is not authenticated"
        raise ProviderAuthError(msg, hint="run the CLI once interactively and sign in")

    msg = f"the CLI reported {status or 'no status'}: {error[:300] or 'no detail'}"
    raise ProviderPermanentError(msg, hint="run the same command manually to see the failure")


def _verify_image(path: Path) -> None:
    """Confirm the copied file really is an image Pillow can read."""
    try:
        with Image.open(path) as image:
            image.verify()
    except (OSError, UnidentifiedImageError) as exc:
        msg = f"the produced file is not a readable image: {path}"
        raise ProviderOutputMissingError(
            msg, hint="the CLI may have written a partial file"
        ) from exc


def _cost(usage: JsonValue) -> Cost | None:
    """Turn the envelope's `usage` into a `Cost`.

    Tokens only: S8 measured no credit, price or currency field, so `credits` stays `None`
    and the Phase 8 report falls back to tokens for this provider.
    """
    if not isinstance(usage, dict):
        return None
    return Cost(
        tokens_in=_as_int(usage.get("input_tokens"), 0),
        tokens_out=_as_int(usage.get("output_tokens"), 0),
    )


def _redacted(envelope: JsonPayload) -> JsonPayload:
    """Keep the envelope for diagnosis, minus anything long or echoed back.

    `response` is the agent's prose and can restate the prompt verbatim; it is truncated
    rather than dropped so a surprising result is still explainable.
    """
    kept: JsonPayload = {key: value for key, value in envelope.items() if key not in {"response"}}
    response = _as_str(envelope.get("response"), "")
    if response:
        kept["response"] = response[:500]
    return kept


def _write_logs(workdir: Path, key: str, stdout: str, stderr: str) -> None:
    """Persist the raw streams next to the image, for the per-iteration logs in PLAN.md §7.3."""
    for suffix, payload in ((".out", stdout), (".err", stderr)):
        if payload:
            (workdir / f"{key}{suffix}").write_text(payload, encoding="utf-8")


def _as_str(value: JsonValue, default: str) -> str:
    """Read a string from untyped JSON, falling back rather than raising."""
    return value if isinstance(value, str) else default


def _as_int(value: JsonValue, default: int) -> int:
    """Read an int from untyped JSON, rejecting bools and non-numbers."""
    if isinstance(value, bool):
        return default
    return int(value) if isinstance(value, (int, float)) else default
