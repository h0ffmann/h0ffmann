# AGENTS.md

Guidance for AI coding agents working in this repository.

## What this repo is

This is the GitHub profile repository for `h0ffmann`. `README.md` is rendered
at https://github.com/h0ffmann as the profile page. There is no application
code, no build, no tests, and no linter. Every change here is either a README
edit or a change to the metrics workflow.

## Files

- `README.md` – the profile page. The only file that is edited by hand
  regularly.
- `.github/workflows/metrics.yml` – runs `lowlighter/metrics` daily at 06:00
  UTC (and on manual dispatch, and on push to `main` when the workflow file
  itself changes). Each of its two steps writes one SVG and commits it back
  to `main` with a `[Skip GitHub Action]` suffix.
- `metrics.base.svg`, `metrics.languages.svg` – **generated**. Never edit these by hand; the next workflow run overwrites
  them. They are committed so the README can embed them by relative path.

## Working on the README

- Headings are lowercase with a leading emoji (`### 🫀 core`, `## 📊 stats`).
  Keep that style for new sections.
- Tech badges use shields.io with `style=flat-square`. Link and cert badges
  use `style=for-the-badge`. Use `logo=<simpleicons-slug>` where a Simple
  Icons logo exists.
- Badge groups live inside `<p align="left">` blocks, one `<img>` per line.
- The stats section embeds the three generated SVGs. If you add a metrics
  step to the workflow, also add the matching `<img>` to the README, or it
  will be generated but never shown.
- Preview: GitHub renders the README, so check the branch on github.com or
  use `gh repo view --web` for the merged result. Relative SVG paths only
  resolve once the SVGs exist on the branch being viewed.

## Working on the workflow

- The workflow needs a `METRICS_TOKEN` repository secret (a PAT with read
  access to the user's repos). Without it every step fails; there is nothing
  to fix in the YAML for that case.
- `lowlighter/metrics` is pinned to a release tag. Bump it deliberately
  rather than reverting to `@latest`.
- Validate YAML before pushing:

  ```sh
  python3 -c "import yaml; yaml.safe_load(open('.github/workflows/metrics.yml'))"
  ```

- Trigger and inspect a run:

  ```sh
  gh workflow run metrics
  gh run list --workflow metrics --limit 5
  gh run view <run-id> --log-failed
  ```

- The workflow commits to `main`. If you are on a feature branch, a manual
  dispatch still targets `main`; to test workflow changes on a branch use
  `gh workflow run metrics --ref <branch>`.
- Plugin options are documented per plugin in the metrics repo, for example
  https://github.com/lowlighter/metrics/blob/master/source/plugins/languages/README.md.

## Git conventions

- Work on a branch and open a PR; do not push straight to `main`.
- Commits made by the metrics bot carry `[Skip GitHub Action]`. Leave that
  suffix off human commits; it exists so the bot's own pushes do not retrigger
  the workflow.
- After a merge, expect three bot commits on `main` within a day. Rebase
  rather than merge if a branch falls behind because of them.
