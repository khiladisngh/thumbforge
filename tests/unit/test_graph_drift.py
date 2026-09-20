"""The drift check's node filter (issue #26).

This is a CI gate, so a silently broken filter produces false *greens*, which is worse than
the false reds it replaced. Each case below pins one of the five exclusions that were
measured from real CI failures — see the module docstring in `scripts/check_graph_drift.py`.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest

if TYPE_CHECKING:
    from types import ModuleType

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "check_graph_drift.py"


def _module() -> ModuleType:
    """Import the script by path; `scripts/` is not a package."""
    spec = importlib.util.spec_from_file_location("check_graph_drift", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


drift = _module()


def _graph(tmp_path: Path, name: str, *nodes: dict[str, Any]) -> Path:
    path = tmp_path / f"{name}.json"
    path.write_text(json.dumps({"nodes": list(nodes), "links": []}), encoding="utf-8")
    return path


def _declaration(node_id: str) -> dict[str, Any]:
    return {"id": node_id, "_origin": "ast", "source_file": "src/thumbforge/x.py"}


def test_declarations_are_kept(tmp_path: Path) -> None:
    """A symbol parsed out of a repository file is the thing being tracked."""
    graph = _graph(tmp_path, "g", _declaration("src_thumbforge_x_thing"))

    assert drift.declarations(graph) == {"src_thumbforge_x_thing"}


@pytest.mark.parametrize(
    ("label", "node"),
    [
        # CI resolves imports less completely than a local run and invents these.
        (
            "unresolved import placeholder",
            {"id": "thumbforge_core_errors", "_origin": "semantic", "source_file": ""},
        ),
        # Depends on what is installed, not on this repository.
        ("external symbol", {"id": "typer", "_origin": "ast", "source_file": ""}),
        # The trailing number is a source line, so moving a comment renames the node.
        (
            "line-keyed rationale",
            {
                "id": "src_thumbforge_x_rationale_412",
                "_origin": "ast",
                "source_file": "src/thumbforge/x.py",
            },
        ),
    ],
)
def test_volatile_nodes_are_excluded(tmp_path: Path, label: str, node: dict[str, Any]) -> None:
    """Each of these varied between CI and a local extract without the source changing."""
    graph = _graph(tmp_path, "g", node)

    assert drift.declarations(graph) == set()


def test_a_renamed_symbol_is_reported(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """The point of the check: a symbol added or removed without regenerating."""
    committed = _graph(tmp_path, "committed", _declaration("src_thumbforge_x_old"))
    fresh = _graph(tmp_path, "fresh", _declaration("src_thumbforge_x_new"))

    exit_code = drift.main(["check", str(committed), str(fresh)])

    assert exit_code == 1
    output = capsys.readouterr().out
    assert "src_thumbforge_x_new" in output
    assert "src_thumbforge_x_old" in output


def test_matching_declarations_pass(tmp_path: Path) -> None:
    """A graph that differs only in volatile nodes must not fail the build."""
    committed = _graph(
        tmp_path,
        "committed",
        _declaration("src_thumbforge_x_thing"),
        {"id": "thumbforge_core_errors", "_origin": "semantic", "source_file": ""},
    )
    fresh = _graph(tmp_path, "fresh", _declaration("src_thumbforge_x_thing"))

    assert drift.main(["check", str(committed), str(fresh)]) == 0


def test_wrong_argument_count_is_a_usage_error(tmp_path: Path) -> None:
    """Exit 2 keeps a misinvocation distinguishable from real drift."""
    assert drift.main(["check"]) == 2
