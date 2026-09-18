# Branching, protection, labels, releases

## Branches

- `main` is always releasable. Nobody pushes to it directly.
- Work branches: `feat/P3.2-fake-provider`, `infra/P0.5-github`, `fix/<issue>-<slug>`, `spike/S1-agy-image-tool`, `docs/<slug>`.
- Squash-merge only; the squash title is a Conventional Commit.

## Branch protection (`main`)

Applied with the GitHub CLI (requires admin on the repo):

```
gh api -X PUT repos/khiladisngh/thumbforge/branches/main/protection \
  -H "Accept: application/vnd.github+json" \
  --input - <<'JSON'
{
  "required_status_checks": { "strict": true, "contexts": ["test (ubuntu-latest, 3.14)", "test (windows-latest, 3.14)"] },
  "enforce_admins": false,
  "required_pull_request_reviews": { "required_approving_review_count": 0, "dismiss_stale_reviews": true },
  "restrictions": null,
  "required_linear_history": true,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "required_conversation_resolution": true
}
JSON
```

`required_approving_review_count` is `0` while the project has a single maintainer; raise to `1` once a second reviewer exists.

## Labels

Defined in `.github/labels.yml`; applied by:

```
uv run --with pyyaml python - <<'PY'
import subprocess, yaml
for l in yaml.safe_load(open(".github/labels.yml")):
    subprocess.run(["gh", "label", "create", l["name"], "--color", l["color"], "--description", l.get("description", ""), "--force"], check=True)
PY
```

## Releases

1. Bump `[project] version` in `pyproject.toml` on a PR (`chore(release): v0.1.0`).
2. After merge: `git tag v0.1.0 && git push origin v0.1.0`.
3. `release.yml` checks the tag matches the version, runs `uv build`, generates release notes with `git-cliff` from Conventional Commits, creates the GitHub release with the wheel and sdist attached, and publishes to PyPI via trusted publishing (environment `pypi`; configure the publisher on PyPI before the first release).

## Docs

`docs.yml` builds the zensical site and deploys it to GitHub Pages on every push to `main`. Preview locally with `uv run zensical serve`.
