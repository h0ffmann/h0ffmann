# Nix labs section — design

**Date:** 2026-09-15
**Repo:** h0ffmann/h0ffmann (GitHub profile README)
**Status:** implemented (PR "Add the generated nix labs section")

## Goal

Show, on the profile README, a self-updating status table for the Nix labs in
`h0ffmann/nix-config`: how fresh each lab's `flake.lock` is and which headline
tool versions it pins. Keeping the locks fresh is out of scope; that belongs
in nix-config.

## Non-goals

- No `update-flake-lock` or any change to nix-config.
- No flake or `flake.lock` in this repo.
- No devShell builds on the runner; versions come from `nix eval` only.
- No change to the existing `metrics.yml` workflow.

## README layout

A new section is inserted between `## 📊 stats` and `## 💼 exp-highlights`:

```markdown
## ❄️ nix labs

[![nix-config ci](https://github.com/h0ffmann/nix-config/actions/workflows/ci.yml/badge.svg)](https://github.com/h0ffmann/nix-config/actions/workflows/ci.yml)

<!-- generated daily by .github/workflows/nix-labs.yml from h0ffmann/nix-config -->
<!-- nix-labs:start -->
| lab | nixpkgs | locked | toolchain |
| --- | --- | --- | --- |
| [pratico](https://github.com/h0ffmann/nix-config/tree/main/labs/pratico) | `eaad089` | 2026-09-11 (4 days ago) | gfortran 15.3.0 · openmpi 5.0.10 · netcdf 4.10.0 · hdf5 1.14.6 · eccodes 2.41.0 |
| [publisher](https://github.com/h0ffmann/nix-config/tree/main/labs/publisher) | `eaad089` | 2026-09-11 (4 days ago) | pandoc 3.7.0.2 · texlive 2025 · python 3.13.7 |
<!-- nix-labs:end -->
```

Version numbers in the example rows are illustrative; the script renders the real ones.

Rules:

- The badge line and the "generated daily" comment are static; only the text
  between the two markers is rewritten.
- One row per directory matching `labs/*/flake.lock` in nix-config, sorted by
  name. New labs appear without any change here.
- `nixpkgs` is the first 7 characters of `nodes.nixpkgs.locked.rev`, in code
  formatting. If a lock has no `nixpkgs` node the cell is `?`.
- `locked` is `nodes.nixpkgs.locked.lastModified` as `YYYY-MM-DD` plus a
  relative age: `today`, `1 day ago`, `N days ago`. If the age exceeds
  90 days the cell is prefixed with `⚠️ `.
- `toolchain` is `name version` pairs joined by ` · `. The attribute list
  comes from the lab's own `labs/<lab>/lab.json` in nix-config
  (`"headline": ["gfortran", ...]`, see h0ffmann/nix-config PR "lab.json per
  lab"). A lab without `lab.json`, or with an empty list, renders `—`.
- Version numbers are shown verbatim from nixpkgs except TeX Live, whose
  `texliveMedium.version` string (`2025-r78234-final-env`) is cut at the first
  `-`.

## Script: `scripts/build_readme.py`

Python 3, standard library only (`argparse`, `json`, `subprocess`, `datetime`,
`re`, `pathlib`, `sys`).

### CLI

```
python3 scripts/build_readme.py [--nix-config PATH] [--readme PATH] [--dry-run] [--today YYYY-MM-DD]
```

- `--nix-config` default `../nix-config` (the sibling checkout on the
  workstation; the workflow passes `nix-config`).
- `--readme` default `README.md`. May be given twice; the workflow passes
  `--readme README.md --readme README.pt-BR.md` so both language versions
  get the same table (the table itself is language-neutral).
- `--dry-run` prints the rendered section to stdout and does not touch the
  README.
- `--today` overrides the date used for age calculation (tests, reproducible
  runs). Default: current UTC date.

Exit codes: `0` on success (stdout says `README.md: changed` or
`README.md: unchanged`), `2` if the nix-config path has no `labs/` directory
or the README lacks either marker.

### Structure

```python
LABELS = {"texliveMedium": "texlive"}       # display name when it differs from the attr
STALE_DAYS = 90
START, END = "<!-- nix-labs:start -->", "<!-- nix-labs:end -->"

def discover_labs(nix_config: Path) -> list[Path]            # sorted labs/*/ dirs that hold flake.lock
def read_nixpkgs_pin(lock_path: Path) -> tuple[str, date] | None
def read_headline(lab_dir: Path) -> list[str]                # lab.json "headline"; [] if absent or malformed (warning)
def age_text(locked: date, today: date) -> str
def nix_version(rev: str, attr: str) -> str | None           # subprocess nix eval --raw; None on failure
def render_table(labs, today, evaluate=nix_version) -> str  # evaluate is injectable for tests
def replace_section(readme_text: str, section: str) -> str  # raises ValueError if markers missing
def main(argv) -> int
```

`render_table` memoises `evaluate` per `(rev, attr)` so two labs pinned to the
same nixpkgs do not evaluate twice. `nix_version` runs

```
nix eval --raw github:NixOS/nixpkgs/<rev>#<attr>.version
```

with a 120 s timeout. Any non-zero exit, timeout, or missing `nix` binary
returns `None`; the caller renders `?` for that pair and writes one warning
line to stderr. The run still succeeds.

## Workflow: `.github/workflows/nix-labs.yml`

```yaml
name: nix-labs
on:
  schedule:
    - cron: "30 6 * * *"        # daily, 30 min after metrics.yml
  workflow_dispatch:
  push:
    branches: [main]
    paths:
      - ".github/workflows/nix-labs.yml"
      - "scripts/**"
permissions:
  contents: write
concurrency:
  group: nix-labs
  cancel-in-progress: false
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: actions/checkout@v7
        with:
          repository: h0ffmann/nix-config
          path: nix-config
      - uses: DeterminateSystems/nix-installer-action@v23
      - run: python3 -m unittest discover -s scripts -v
      - run: python3 scripts/build_readme.py --nix-config nix-config
      - name: commit if changed
        run: |
          git config user.name  "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          if git diff --quiet README.md; then echo "no change"; exit 0; fi
          git add README.md
          git commit -m "Update nix labs section - [Skip GitHub Action]"
          git pull --rebase origin main
          git push
```

Notes:

- nix-config is public, so the second checkout needs no token.
- `nix-config/` is added to `.gitignore` so a local run with that path can
  never be committed.
- The `[Skip GitHub Action]` suffix matches the metrics bot's commits. Because
  this workflow's `push` trigger is path-filtered to the script and workflow,
  a README-only commit cannot retrigger it regardless of the suffix.
- The pull-rebase before push covers the case where `metrics.yml` is still
  committing SVGs when this job finishes.
- Action pins match nix-config's `ci.yml` (`checkout@v7`,
  `nix-installer-action@v23`).

## Error handling summary

| Failure | Behaviour |
| --- | --- |
| nix-config checkout fails | Job fails, README untouched |
| Lab has no `nixpkgs` lock node | Row rendered with `?` for rev and locked |
| Lab has no `lab.json`, or it is malformed | `—` in toolchain, warning on stderr, run succeeds |
| `nix eval` fails / times out for an attr | `?` for that pair, warning on stderr, run succeeds |
| README markers missing | Exit 2, nothing written |
| No labs found | Exit 2 |

## Testing

`scripts/test_build_readme.py`, `unittest`, run with
`python3 -m unittest discover -s scripts`:

1. `age_text`: today, 1 day, N days.
2. `render_table` with a fake `evaluate`: two labs, same rev evaluated once
   per attr, TeX Live label and version trimming, `⚠️` past 90 days, `?` when
   the evaluator returns `None`, `—` for an unknown lab.
3. `replace_section`: replaces only between markers, preserves surrounding
   text, raises on missing markers.
4. `discover_labs` on a `tmp_path` fixture tree: finds only directories with
   `flake.lock`, sorted.
5. `read_nixpkgs_pin`: parses a fixture lock; returns `None` without a
   nixpkgs node.
6. `read_headline`: parses a fixture `lab.json`; returns `[]` when the file
   is missing or not the expected shape.

Manual check: `python3 scripts/build_readme.py --nix-config ../nix-config --dry-run`
on the workstation, then one `workflow_dispatch` run after merge.

## Documentation

AGENTS.md gains a "nix labs section" paragraph: what is generated, that the
per-lab attribute list lives in nix-config's `labs/<lab>/lab.json`, that `nix-config/` is a
gitignored checkout path, and the local dry-run and test commands.

## Files touched

- `README.md` — new section with markers (initial table rendered by the script)
- `scripts/build_readme.py` — new
- `scripts/test_build_readme.py` — new
- `.github/workflows/nix-labs.yml` — new
- `.gitignore` — new, contains `nix-config/`
- `AGENTS.md` — updated
