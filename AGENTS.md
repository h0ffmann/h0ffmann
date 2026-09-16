# AGENTS.md

Guidance for AI coding agents working in this repository.

## What this repo is

This is the GitHub profile repository for `h0ffmann`. `README.md` is rendered
at https://github.com/h0ffmann as the profile page. There is no application
code, no build, no tests, and no linter. Every change here is either a README
edit or a change to the metrics workflow.

## Files

- `README.md` – the profile page, in English. `README.pt-BR.md` and
  `README.ja.md` are its Portuguese and Japanese mirrors; the three link to
  each other from a flag line at the top. **Every edit to one is made to
  all three in the same commit**: same sections, same badges, same markers,
  only the prose and alt texts differ.
- `pdf/cv.pdf`, `pdf/cv.pt-BR.pdf` and `pdf/cv.ja.pdf` – **generated** CVs,
  built from the three READMEs (headers `cv/header*.md`, footer, PDF title
  and, for Japanese, the luatexja preamble lines per language in
  `cv/build.sh`) by
  `.github/workflows/cv.yml` through nix-config's `labs/publisher` action
  (pandoc → lualatex; shields badges become colored pills, emoji stay in
  color). `cv/prepare.py` drops everything between `<!-- cv:skip -->` /
  `<!-- cv:end -->` (the language line, the stats section, the photo) and
  prepends `cv/header.md` (name + contact). `cv/preamble.tex` is the look.
  `flake.nix` pins publisher in `flake.lock`; bump with
  `nix flake update publisher` when the lab changes. Build locally with
  `nix build` (result/cv.pdf) and run `python3 -m unittest discover -s cv`.
  Keep the skip-marker pairs balanced and identical in all READMEs.
- `marola-qr.svg` – static QR code for https://marola.dev, generated once
  with `qrencode -t SVG -l M -m 2` and shown at 120 px beside the marola
  section. Regenerate only if the URL changes.
- `.github/workflows/metrics.yml` – runs `lowlighter/metrics` daily at 06:00
  UTC (and on manual dispatch, and on push to `main` when the workflow file
  itself changes). Each of its two steps writes one SVG and commits it back
  to `main` with a `[Skip GitHub Action]` suffix.
- `.github/workflows/nix-labs.yml` – daily at 06:30 UTC, checks out
  h0ffmann/nix-config into the gitignored `nix-config/` path and runs
  `scripts/build_readme.py`, which rewrites the table between
  `<!-- nix-labs:start -->` / `<!-- nix-labs:end -->` in both READMEs (also
  on an `activity` dispatch whose payload names h0ffmann/nix-config): per
  lab, the pinned nixpkgs rev and date, and the versions of the attributes
  that lab's `lab.json` lists, read with `nix eval` at that rev. The
  per-lab knowledge lives in nix-config, not here. Never edit inside the
  markers. Locally: `python3 scripts/build_readme.py --nix-config ../nix-config --dry-run`
  and `python3 -m unittest discover -s scripts`.
- `.github/workflows/activity.yml` – daily at 07:00 UTC **and** on every
  `repository_dispatch` of type `activity` (sent by nix-config's reusable
  `profile-ping.yml` after a merged PR in nix-config, marola, ww3-gpu or
  gcp-agentic-architect; each of those holds a `PROFILE_DISPATCH_TOKEN`
  secret), runs
  `scripts/build_activity.py` with `METRICS_TOKEN`, which reads the user's
  own events (private ones included) and rewrites the list between the
  `<!--START_SECTION:activity-->` / `<!--END_SECTION:activity-->` markers
  in all three READMEs, 10 lines. Events in the profile repository itself
  are skipped — its history is README and CV regeneration, which says
  nothing about what the user is working on; `--skip-repo` overrides the
  list and `--skip-repo ""` keeps everything. The dispatch payload (repo, PR number,
  visibility, merge time — nothing else, these logs are public) is passed
  as `--dispatch-json`, and that merge is added when the events API has
  not caught up yet. Private repositories render as a bare name with 🔒 and
  no links; `PRIVATE_LABELS` in the script adds a label (marola: "FOSS
  soon"). Consecutive identical lines collapse. Never edit inside the
  markers; keep the pair intact in both files. Locally:
  `GITHUB_TOKEN=$(gh auth token) python3 scripts/build_activity.py --dry-run`
  and `python3 -m unittest discover -s scripts`.
- `metrics.base.svg`, `metrics.languages.svg` – **generated**. Never edit these by hand; the next workflow run overwrites
  them. They are committed so the README can embed them by relative path.

## Working on the README

- Headings are lowercase with a leading emoji (`### 🫀 core`, `## 📊 stats`).
  Keep that style for new sections.
- Tech badges use shields.io with `style=flat-square`. Link and cert badges
  use `style=for-the-badge`. Use `logo=<simpleicons-slug>` where a Simple
  Icons logo exists.
- Badge groups live inside `<p align="left">` blocks, one `<img>` per line.
- The stats section embeds the two generated SVGs and the activity markers,
  and the nix labs section holds the nix-labs markers, in both READMEs. If you add a metrics
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
  rather than reverting to `@latest`. Upstream is unmaintained (v3.34 is
  from 2023); its activity plugin no longer works with GitHub's events API,
  which is why `activity.yml` uses our own script.
- The languages step runs the in-depth analyzer, which clones every owned
  repository over plain https without a token. Private repositories fail to
  clone silently, so the card covers **public repositories only**. It
  matches commits with `commits_authoring` (login plus the commit email);
  without the email it finds nothing. PostScript, XSLT and JavaScript are
  ignored because they are generated figures and committed bundles, not
  authored code. Back-to-back runs can be throttled and produce an empty
  card; the next scheduled run recovers.
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
- The three README bots (`metrics` excluded) share the `readme-bots`
  concurrency group so their commit-backs queue instead of racing.
- After a merge, expect several bot commits on `main` within a day. Rebase
  rather than merge if a branch falls behind because of them.
