# Branching and release process

## Branches

- `main` is always releasable. Work lands on it directly: no pull requests, and history stays linear (rebase, never a merge commit, never a force-push).
- One roadmap task is one Conventional Commit. Optional work branches in a worktree: `feat/P3.2-fake-provider`, `infra/P0.5-github`, `fix/<issue>-<slug>`, `spike/S1-agy-image-tool`, `docs/<slug>`; rebase onto `origin/main` and push with `git push origin HEAD:main`.
- Before the push, run both local CI legs (`scripts/ci-local.sh`, `scripts/ci-local.cmd`) and read your own diff. After it, check the remote run.

## Branch protection (`main`)

The repository admin bypasses these rules for the direct push to `main`; they still stop everyone else and force pushes. Applied with the GitHub CLI (requires admin on the repo):

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

1. Bump `[project] version` in `pyproject.toml` and regenerate `CHANGELOG.md` in one commit (`chore(release): v0.1.0`), then push it to `main`. `release.yml` fails when the tag and the version differ, so the bump comes first:

   ```
   uv version 0.1.0
   uvx git-cliff --tag v0.1.0 --output CHANGELOG.md
   ```

2. Once the remote run is green: `git tag v0.1.0 && git push origin v0.1.0`.
3. `release.yml` checks the tag matches the version, runs `uv build`, generates release notes with `git-cliff` from Conventional Commits (`cliff.toml`), creates the GitHub release with the wheel and sdist attached, and publishes to PyPI via trusted publishing (environment `pypi`).

### One-time setup for publishing

Only the repository owner can do these; the workflow cannot. Both are in place for `v0.1.0`; repeat them only for a new project or a new repository:

1. **PyPI:** under Account settings, Publishing, add a pending publisher for a new project: name `thumbforge`, owner `khiladisngh`, repository `thumbforge`, workflow `release.yml`, environment `pypi`.
2. **GitHub:** under Settings, Environments, create the `pypi` environment. Adding yourself as a required reviewer makes every publish wait for an explicit approval. No secret is needed: trusted publishing uses the workflow's OIDC token.

## Docs

`docs.yml` builds the zensical site and deploys it to GitHub Pages on every push to `main`. Preview locally with `uv run zensical serve`.
