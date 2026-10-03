#!/usr/bin/env bash
# Reproduces .github/workflows/ci.yml job "test (ubuntu-latest, 3.14)" 1:1.
# Usage: scripts/ci-local.sh [REPO_DIR]  (default: the repo containing this script).
# Fails at the first failing step; prints PASS/FAIL + seconds per step.
set -u
cd "${1:-$(dirname "$0")/..}" || exit 2
export UV_PYTHON=3.14
total=$SECONDS
run_step() {
  local name="$1"; shift
  local t0=$SECONDS
  echo "=== STEP: $name : $*"
  if "$@"; then
    echo "=== PASS $name ($((SECONDS - t0))s)"
  else
    echo "=== FAIL $name ($((SECONDS - t0))s)"
    echo "=== TOTAL $((SECONDS - total))s - FAILED"
    exit 1
  fi
}
run_step sync         uv sync --locked
run_step ruff-check   uv run ruff check .
run_step ruff-fmt     uv run ruff format --check .
run_step pyright      uv run pyright
run_step lint-imports uv run lint-imports
run_step pytest       uv run pytest --cov --cov-fail-under=80
run_step zensical     uv run zensical build
echo "=== TOTAL $((SECONDS - total))s - ALL PASS"
