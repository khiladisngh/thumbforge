"""Registry behaviour: discovery, duplicate keys, and broken plugins (ADR 0010, P3.1).

`entry_points` is patched rather than a real distribution installed, because the behaviour
under test is how the registry *reacts* to the group's contents — a duplicate key, a plugin
that raises on import, a value that is not a class. Installing a distribution per case would
be slower and would not let the failure cases exist at all.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

import pytest

from thumbforge.core.errors import ExitCode, NotFoundError, ProviderRegistryError
from thumbforge.core.providers import (
    Check,
    GenerationRequest,
    GenerationResult,
    HealthReport,
    ImageProvider,
    ProviderCapabilities,
    ProviderInfo,
)
from thumbforge.providers import registry

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path

    from thumbforge.core.json import JsonValue


class StubProvider:
    """A minimal `ImageProvider`, standing in for a third-party plugin."""

    key: ClassVar[str] = "stub"

    def __init__(self, config: Mapping[str, JsonValue]) -> None:
        """Keep the config so a test can prove it was passed through."""
        self.config = config

    @property
    def capabilities(self) -> ProviderCapabilities:
        """Deliberately unlike Antigravity, so a test cannot pass by coincidence."""
        return ProviderCapabilities(
            supports_reference_image=True,
            supports_seed=True,
            supports_negative_prompt=True,
            supports_aspect_ratio=True,
            max_batch=4,
            max_concurrency=8,
            output_formats=frozenset({"png"}),
        )

    async def info(self) -> ProviderInfo:
        """Identity, with auth reported as unknown."""
        return ProviderInfo(key="stub", name="Stub", version="0", auth="unknown")

    async def healthcheck(self) -> HealthReport:
        """One passing check."""
        return HealthReport(checks=(Check(name="stub", ok=True),))

    async def generate(self, request: GenerationRequest, *, workdir: Path) -> GenerationResult:
        """Return a result pointing at a path inside `workdir`."""
        return GenerationResult(
            image_path=workdir / f"{request.idempotency_key}.png",
            provider_key="stub",
            provider_version="0",
            duration_ms=0,
        )


class _Entry:
    """Stands in for an `importlib.metadata.EntryPoint`."""

    def __init__(self, name: str, value: str, loaded: object, *, raises: bool = False) -> None:
        self.name = name
        self.value = value
        self._loaded = loaded
        self._raises = raises

    def load(self) -> object:
        """Mimic a plugin import, which can fail."""
        if self._raises:
            msg = "boom"
            raise ImportError(msg)
        return self._loaded


@pytest.fixture
def entries(monkeypatch: pytest.MonkeyPatch) -> list[_Entry]:
    """Replace the installed entry-point group with a list the test controls."""
    group: list[_Entry] = []

    def fake_entry_points(*, group: str) -> list[_Entry]:
        assert group == registry.ENTRY_POINT_GROUP
        return entries_list

    entries_list = group
    monkeypatch.setattr(registry, "entry_points", fake_entry_points)
    return group


def test_stub_satisfies_the_provider_protocol() -> None:
    """If the stub drifts from `ImageProvider`, every test here stops meaning anything."""
    assert isinstance(StubProvider({}), ImageProvider)


def test_entry_point_provider_is_discovered_and_constructed(entries: list[_Entry]) -> None:
    """A plugin needs only an entry point: the registry never imports it by name."""
    entries.append(_Entry("stub", "pkg.mod:StubProvider", StubProvider))

    assert registry.keys() == ["stub"]
    provider = registry.get("stub", {"binary": "agy"})

    assert isinstance(provider, StubProvider)
    assert provider.config == {"binary": "agy"}


def test_config_defaults_to_empty_rather_than_none(entries: list[_Entry]) -> None:
    """Providers should not each have to handle `None`."""
    entries.append(_Entry("stub", "pkg.mod:StubProvider", StubProvider))

    provider = registry.get("stub")
    assert isinstance(provider, StubProvider)
    assert provider.config == {}


def test_keys_are_sorted(entries: list[_Entry]) -> None:
    """`provider list` output must not reorder between runs."""
    entries.append(_Entry("zulu", "pkg:Z", StubProvider))
    entries.append(_Entry("alpha", "pkg:A", StubProvider))

    assert registry.keys() == ["alpha", "zulu"]


def test_duplicate_key_is_refused(entries: list[_Entry], monkeypatch: pytest.MonkeyPatch) -> None:
    """Shadowing a provider would make `--provider x` mean different things per machine.

    The failure would otherwise surface as wrong images rather than as a message, so it is
    an error at discovery rather than a precedence rule.
    """
    monkeypatch.setitem(registry.BUILTIN, "stub", StubProvider)
    entries.append(_Entry("stub", "other.pkg:Rival", StubProvider))

    with pytest.raises(ProviderRegistryError) as caught:
        registry.keys()

    assert "claimed twice" in str(caught.value)
    assert "builtin" in str(caught.value)
    assert caught.value.hint is not None


def test_two_plugins_claiming_one_key_are_refused(entries: list[_Entry]) -> None:
    """Same rule when neither side is a builtin."""
    entries.append(_Entry("stub", "first:P", StubProvider))
    entries.append(_Entry("stub", "second:P", StubProvider))

    with pytest.raises(ProviderRegistryError):
        registry.keys()


def test_broken_plugin_is_reported_not_skipped(entries: list[_Entry]) -> None:
    """A skipped plugin looks identical to one that was never installed.

    That is the harder bug to diagnose, so a failed import raises with the entry-point value
    in the message and the underlying error as `__cause__`.
    """
    entries.append(_Entry("stub", "broken.pkg:Boom", None, raises=True))

    with pytest.raises(ProviderRegistryError) as caught:
        registry.keys()

    assert "broken.pkg:Boom" in str(caught.value)
    assert isinstance(caught.value.__cause__, ImportError)


def test_non_callable_entry_point_is_refused(entries: list[_Entry]) -> None:
    """An entry point naming a module or constant cannot be instantiated."""
    entries.append(_Entry("stub", "pkg:NOT_A_CLASS", "just a string"))

    with pytest.raises(ProviderRegistryError) as caught:
        registry.keys()

    assert "not callable" in str(caught.value)


def test_unknown_key_exits_three_and_lists_what_is_available(entries: list[_Entry]) -> None:
    """Spec: unknown provider key → `NotFoundError` → exit 3, with an actionable hint."""
    entries.append(_Entry("stub", "pkg:P", StubProvider))

    with pytest.raises(NotFoundError) as caught:
        registry.get("antigravty")  # typo, the common cause

    assert caught.value.exit_code is ExitCode.NOT_FOUND
    assert caught.value.hint is not None
    assert "stub" in caught.value.hint


def test_unknown_key_with_nothing_installed_says_so(entries: list[_Entry]) -> None:
    """An empty registry must not produce a hint reading `available: `."""
    assert entries == []

    with pytest.raises(NotFoundError) as caught:
        registry.get("fake")

    assert caught.value.hint is not None
    assert "none installed" in caught.value.hint


def test_constructed_object_must_satisfy_the_protocol(entries: list[_Entry]) -> None:
    """`callable()` at discovery says nothing about what the factory returns.

    A plugin that constructs the wrong thing must fail here, not later inside `generate`
    where the traceback names thumbforge rather than the plugin.
    """

    class NotAProvider:
        def __init__(self, config: Mapping[str, JsonValue]) -> None: ...

    entries.append(_Entry("rogue", "pkg:NotAProvider", NotAProvider))

    with pytest.raises(ProviderRegistryError) as caught:
        registry.get("rogue")

    assert "not an ImageProvider" in str(caught.value)
    assert "NotAProvider" in str(caught.value)


def test_provider_key_must_match_its_registered_key(entries: list[_Entry]) -> None:
    """Provenance is recorded from `provider.key` onto every run and iteration.

    A mismatch would attribute generated images to a provider that did not make them, which
    is unrecoverable after the fact — so it is refused at construction.
    """

    class Mislabelled(StubProvider):
        key: ClassVar[str] = "something-else"

    entries.append(_Entry("stub", "pkg:Mislabelled", Mislabelled))

    with pytest.raises(ProviderRegistryError) as caught:
        registry.get("stub")

    assert "reports key 'something-else'" in str(caught.value)
