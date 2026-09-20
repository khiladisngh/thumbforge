"""The JSON shape that crosses every machine-readable boundary.

Defined in `core` because three layers need it and none may import the others': `cli`
emits it under `--json`, `core.providers` carries it in `GenerationRequest.params` and
`GenerationResult.raw_response`, and `storage` persists it into the `*_json` columns.

A leaf module — it imports nothing from `thumbforge`.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

type JsonValue = str | int | float | bool | Sequence[JsonValue] | Mapping[str, JsonValue] | None
"""Any value that survives a round trip through `json.dumps`/`json.loads`.

`Sequence`/`Mapping` rather than `list`/`dict` because the concrete types are invariant: an
ordinary `dict[str, str]` payload would not satisfy `dict[str, JsonValue]`, forcing a cast at
every call site. The looser protocols technically admit `bytes` and `range`, which
`json.dumps` rejects; `cli._render.emit` lets that rejection happen loudly at runtime rather
than coercing, and `tests/unit/test_render.py` pins that behaviour.
"""

#: A mutable JSON object under construction, for code that builds a payload key by key.
type JsonPayload = dict[str, JsonValue]
