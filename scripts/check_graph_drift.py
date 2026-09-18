"""Compare a committed graphify graph against a freshly extracted one.

Only the node and edge *sets* are compared. ``built_at_commit``, community ids and
confidence scores are rebuild-volatile, so a byte diff of ``graph.json`` always fails and
tells you nothing. Usage:

    graphify extract . --code-only
    python scripts/check_graph_drift.py <committed.json> graphify-out/graph.json

Exit 0 when the structure matches, 1 when the committed graph is stale.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

Structure = tuple[list[str], list[tuple[str, str, str]]]


def structure(path: Path) -> Structure:
    graph = json.loads(path.read_text(encoding="utf-8"))
    nodes = sorted(str(n.get("label", n.get("id", ""))) for n in graph.get("nodes", []))
    links = sorted(
        (str(link.get("source", "")), str(link.get("relation", "")), str(link.get("target", "")))
        for link in graph.get("links", [])
    )
    return nodes, links


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(f"usage: {argv[0]} <committed-graph.json> <fresh-graph.json>", file=sys.stderr)
        return 2

    want_nodes, want_links = structure(Path(argv[1]))
    have_nodes, have_links = structure(Path(argv[2]))

    if (want_nodes, want_links) == (have_nodes, have_links):
        print(f"graph is current: {len(have_nodes)} nodes, {len(have_links)} edges")
        return 0

    print("committed graph is stale; run `graphify extract . --code-only`")
    for title, missing in (
        ("nodes added", sorted(set(have_nodes) - set(want_nodes))),
        ("nodes removed", sorted(set(want_nodes) - set(have_nodes))),
        ("edges added", [" ".join(e) for e in sorted(set(have_links) - set(want_links))]),
        ("edges removed", [" ".join(e) for e in sorted(set(want_links) - set(have_links))]),
    ):
        if missing:
            print(f"  {title} ({len(missing)}):")
            for item in missing[:20]:
                print(f"    {item}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
