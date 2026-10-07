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
  (pandoc → lualatex; shields badges become colored pills). `cv/prepare.py`
  drops everything between `<!-- cv:skip -->` / `<!-- cv:end -->` (the
  language line, the LinkedIn badge the CV header already has, the live marola badges and the marola-dev repo table, the photo) and prepends `cv/header.md`
  (name + contact). The CV follows the README's section order — me,
  open source (marola-dev), research (ww3-gpu), exp-highlights, certs,
  learning, misc — so reordering the profile
  reorders the CV. `cv/preamble.tex` is the look. The CV is
  one page per language and close to full: check the page count in the
  build output after adding content.
  Emoji are not drawn from a font: `cv/emoji.lua` replaces each one with
  the vector Noto artwork vendored in `cv/emoji/` (Apache-2.0, see its
  README), because lualatex only gets 136 px bitmaps from Noto Color Emoji
  and DejaVu Sans shadows ⚡ ☁ ❄ with black-and-white glyphs. A new emoji
  in a README fails the unit tests until `python3 cv/cvemoji.py --fetch`
  has downloaded its SVG. Apple's emoji (what macOS shows on github.com)
  are proprietary and cannot be used.
  `flake.nix` pins publisher in `flake.lock`; bump with
  `nix flake update publisher` when the lab changes. Build locally with
  `nix build` (result/cv.pdf) and run `python3 -m unittest discover -s cv`.
  Keep the skip-marker pairs balanced and identical in all READMEs.
- `LICENSE` – MIT, plain text with nothing appended: GitHub's licence
  detection reports NOASSERTION when a scope note follows the licence body.
  It covers the scripts and the prose here; the metrics cards are generated
  by a third-party action, the CV PDFs are built from these READMEs and
  `cv/emoji/` is Google's Noto Emoji artwork under Apache-2.0.
- `marola-qr.svg` – static QR code for https://marola.dev, generated once
  with `qrencode -t SVG -l M -m 2` and shown at 120 px beside the marola
  section. Regenerate only if the URL changes.
- `.github/workflows/metrics.yml` – runs `lowlighter/metrics` daily at 06:00
  UTC (and on manual dispatch, and on push to `main` when the workflow file
  itself changes). Each of its two steps writes one SVG and commits it back
  to `main` with a `[Skip GitHub Action]` suffix.
- `metrics.base.svg`, `metrics.languages.svg` – **generated**. Never edit these by hand; the next workflow run overwrites
  them. They are committed so the README can embed them by relative path.

## Working on the README

- Section order is deliberate: the open-source work at
  [marola-dev](https://github.com/marola-dev) comes right after the intro —
  it is what the user is actively working on and the profile leads with
  it — then the ww3-gpu research project, then experience. The profile has
  no tech-stack or stats section; the user removed both. The
  marola-dev repo table lists every public repo of the org; add a row when
  the org gains one. Live badges (last commit, commit activity, CI) sit in a
  `cv:skip` block: they only render on github.com.
- Never leave badge `<img>` lines bare: outside a `<p align="left">` block
  GitHub renders every line as its own paragraph and the badges stack
  vertically (check with `gh api markdown -f mode=gfm -f text=...`). The
  four AWS cert badges also carry `height="24"`: at the native 28 px the
  row is ~919 px, wider than the README column, and the fourth would wrap.
- Headings are lowercase with a leading emoji (`## 👋 me`, `## 💼 exp-highlights`).
  Keep that style for new sections.
- Topic badges use shields.io with `style=flat-square`. Link, DOI and cert
  badges use `style=for-the-badge`. Use `logo=<simpleicons-slug>` where a Simple
  Icons logo exists.
- Badge groups live inside `<p align="left">` blocks, one `<img>` per line.
- The README no longer embeds the two generated metrics SVGs; the metrics
  workflow still refreshes them. Add their `<img>` back to bring the stats
  section back.
- Preview: GitHub renders the README, so check the branch on github.com or
  use `gh repo view --web` for the merged result. Relative SVG paths only
  resolve once the SVGs exist on the branch being viewed.

## Working on the workflow

- The workflow needs a `METRICS_TOKEN` repository secret (a PAT with read
  access to the user's repos). Without it every step fails; there is nothing
  to fix in the YAML for that case.
- `lowlighter/metrics` is pinned to a release tag. Bump it deliberately
  rather than reverting to `@latest`. Upstream is unmaintained (v3.34 is
  from 2023); its activity plugin no longer works with GitHub's events API.
  The profile used to carry a recent-activity list and a nix labs table,
  each rewritten by its own bot; both were removed, so the marola-dev
  section is the place that says what the user is working on.
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
- The `cv` workflow runs in the `readme-bots` concurrency group; give any
  new workflow that commits to `main` the same group so their commit-backs
  queue instead of racing.
- After a merge, expect several bot commits on `main` within a day. Rebase
  rather than merge if a branch falls behind because of them.
