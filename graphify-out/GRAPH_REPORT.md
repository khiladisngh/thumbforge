# Graph Report - yt-thumbnail-generator  (2026-09-19)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 363 nodes · 650 edges · 28 communities (11 shown, 17 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 30 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `191d1243`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Community 0
- Community 1
- Community 2
- Community 3
- Community 4
- Community 5
- Community 6
- Community 7
- Community 8
- Community 9
- Community 10
- Community 11
- Community 12
- Community 13
- Community 14
- Community 15
- Community 16
- Community 17
- Community 18
- Community 19
- Community 20
- Community 21
- Community 22
- Community 23
- Community 24
- Community 25
- Community 26
- Community 27

## God Nodes (most connected - your core abstractions)
1. `load_settings()` - 22 edges
2. `set_values()` - 18 edges
3. `configure_logging()` - 18 edges
4. `get_logger()` - 17 edges
5. `root()` - 17 edges
6. `Settings` - 14 edges
7. `emit()` - 13 edges
8. `ThumbforgeError` - 12 edges
9. `set_()` - 12 edges
10. `SettingsError` - 11 edges

## Surprising Connections (you probably didn't know these)
- `root()` --calls--> `AppContext`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/cli/_render.py
- `root()` --calls--> `AppContext`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/cli/_render.py
- `test_non_16_9_output_is_rejected()` --uses--> `ConfigSchema`  [INFERRED]
  tests/unit/test_settings.py → src/thumbforge/settings.py
- `boom()` --calls--> `ComplianceError`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/core/errors.py
- `boom()` --calls--> `NotFoundError`  [INFERRED]
  tests/unit/test_errors.py → src/thumbforge/core/errors.py

## Import Cycles
- None detected.

## Communities (28 total, 17 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.08
Nodes (50): Any, BaseSettings, Configuration is missing, malformed, or contains something it must not., SettingsError, _atomic_write(), _deep_merge(), default_config_path(), default_state_dir() (+42 more)

### Community 1 - "Community 1"
Cohesion: 0.07
Nodes (36): AppContext, dataclasses, functools, json, P, R, rich_console, rich_panel (+28 more)

### Community 2 - "Community 2"
Cohesion: 0.08
Nodes (38): Argument, command, Console, JsonValue, metavar, RenderableType, rich_syntax, _as_toml() (+30 more)

### Community 3 - "Community 3"
Cohesion: 0.07
Nodes (36): enum, Exception, IntEnum, ComplianceError, ExitCode, NotFoundError, PartialBatchError, ProviderAuthError (+28 more)

### Community 4 - "Community 4"
Cohesion: 0.09
Nodes (29): collections_abc, logging_handlers, parametrize, re, find_secret_keys(), is_secret_key(), Secret detection shared by configuration loading and logging (ADR 0014, ADR…, Split a key into lowercase words across separators and camelCase boundaries. (+21 more)

### Community 5 - "Community 5"
Cohesion: 0.08
Nodes (26): fixture, hashlib, MonkeyPatch, os, Path, pathlib, pytest, new_id() (+18 more)

### Community 6 - "Community 6"
Cohesion: 0.15
Nodes (28): BoundLogger, CaptureFixture, LogFormat, bind(), configure_logging(), get_logger(), Path, Return a bound logger. Use ``get_logger(__name__)``. (+20 more)

### Community 7 - "Community 7"
Cohesion: 0.10
Nodes (24): BaseModel, model_validator, platformdirs, pydantic, pydantic_settings, Self, AntigravitySettings, BatchSettings (+16 more)

### Community 8 - "Community 8"
Cohesion: 0.12
Nodes (17): callback, Context, count, envvar, is_eager, handle_errors, help, Option (+9 more)

### Community 9 - "Community 9"
Cohesion: 0.16
Nodes (12): Path, Root application behaviour: version, exit codes, and diagnostics from the…, The failure happens inside the root callback, before ctx.obj is assigned. The…, The hint tells users to run `config init --force`; that must actually be…, `config set` still needs a parseable file, but must fail cleanly rather than…, test_broken_config_reports_json_when_json_mode_is_set(), test_broken_config_reports_rich_without_json_mode(), test_config_set_also_works_against_a_broken_config() (+4 more)

### Community 10 - "Community 10"
Cohesion: 0.18
Nodes (9): AppContext, Per-invocation state built by the root callback and stored on ``ctx.obj``., Return the settings, or re-raise the failure that prevented loading them.…, Machine mode contract: stdout carries command output, stderr carries the…, Ctrl-C during a batch must still leave machine mode with parseable output., test_json_mode_emits_one_parseable_line_on_stderr_and_nothing_on_stdout(), root(), test_keyboard_interrupt_in_json_mode_emits_one_line_on_stderr() (+1 more)

## Knowledge Gaps
- **1 isolated node(s):** `thumbforge`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 169 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SettingsError` connect `Community 0` to `Community 3`, `Community 2`, `Community 10`?**
  _High betweenness centrality (0.145) - this node is a cross-community bridge._
- **Why does `load_settings()` connect `Community 0` to `Community 8`, `Community 1`, `Community 7`?**
  _High betweenness centrality (0.095) - this node is a cross-community bridge._
- **Why does `root()` connect `Community 8` to `Community 0`, `Community 1`, `Community 6`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **What connects `thumbforge` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.07857142857142857 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.06666666666666667 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.08205128205128205 - nodes in this community are weakly interconnected._