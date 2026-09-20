"""Compare a committed graphify graph against a freshly extracted one.

Only **declaration nodes** are compared: nodes that graphify parsed out of a repository
file. Everything else in ``graph.json`` is rebuild- or environment-volatile and comparing
it produced five consecutive false alarms (issue #26). Usage:

    graphify extract . --code-only
    python scripts/check_graph_drift.py <committed.json> graphify-out/graph.json

Exit 0 when the declarations match, 1 when the committed graph is stale.

A declaration node is one with ``_origin == "ast"`` **and** a ``source_file``, whose id is
not line-number keyed. Each exclusion is there for a measured reason:

- ``_origin == "semantic"`` nodes are unresolved import placeholders. CI resolves imports
  less completely than a local run, so it invents nodes like ``thumbforge_core_errors``
  where a local extract has ``src_thumbforge_core_errors``. This was the entire content of
  the failures on PRs #25, #33 and #35.
- Nodes without a ``source_file`` are external symbols (``json``, ``typer``, ``Self``),
  which depend on what is installed rather than on this repository.
- ``*_rationale_<line>`` ids embed a **line number**, so moving a comment renames the node.
  That is what made the check red on PR #17 after ``ruff format`` ran post-extract.
- Edges are dropped entirely. They cannot be normalised: on PR #30, CI was *missing*
  ``src_…ytdlp imports src_…core_errors_notfounderror`` — an edge between two resolved
  nodes — because it had resolved that import to a module placeholder instead. Filtering
  by endpoint or ignoring the relation label does not recover that, so edge comparison has
  no environment-independent form.

What this still catches is what regeneration is for: a symbol added, removed or renamed
without re-running ``graphify extract``. What it no longer catches is a changed call edge
between unchanged symbols. That is a deliberate trade: per issue #20 the check already
cannot detect the staleness class that actually bites (a stale node present in both the
committed graph and an incremental re-extract cancels out), so buying a readable signal
with that loss is worth it.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

#: `..._rationale_412` — the trailing number is a source line, not an identity.
_LINE_KEYED = re.compile(r"_rationale_\d+$")


def declarations(path: Path) -> set[str]:
    """Ids of the nodes graphify parsed out of a file in this repository."""
    graph = json.loads(path.read_text(encoding="utf-8"))
    return {
        node["id"]
        for node in graph.get("nodes", ())
        if node.get("_origin") == "ast"
        and node.get("source_file")
        and not _LINE_KEYED.search(node["id"])
    }


def main(argv: list[str]) -> int:
    """Report whether the committed graph still describes the current declarations."""
    if len(argv) != 3:
        print(f"usage: {argv[0]} <committed-graph.json> <fresh-graph.json>", file=sys.stderr)
        return 2

    committed = declarations(Path(argv[1]))
    fresh = declarations(Path(argv[2]))

    if committed == fresh:
        print(f"graph is current: {len(fresh)} declarations")
        return 0

    print("committed graph is stale; run `graphify extract . --code-only`")
    for title, names in (
        ("added", sorted(fresh - committed)),
        ("removed", sorted(committed - fresh)),
    ):
        if names:
            print(f"  {title} ({len(names)}):")
            for name in names[:25]:
                print(f"    {name}")
            if len(names) > 25:
                print(f"    … {len(names) - 25} more")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
