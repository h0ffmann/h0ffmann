# h0ffmann. The CV is built by `nix build` (AGENTS.md). These recipes build the site of site/.
# The tools come from picasso's gleam-website lab through flake.nix, pinned in flake.lock.

set shell := ["bash", "-euo", "pipefail", "-c"]

default:
    @just --list

# Build site/ into site/dist: the content from this repository's files (site/content), the
# tests, the bundle and the first render.
site:
    nix develop --extra-experimental-features 'nix-command flakes' --no-update-lock-file .#site --command just _site

_site:
    # The page names workflows: each one must be a file in .github/workflows/.
    for f in $(grep -oE '"[a-z]+\.yml"' site/src/h0ffmann_site/app.gleam | tr -d '"' | sort -u); do [ -f ".github/workflows/$f" ] || { echo "site: the page names $f, which is not a workflow" >&2; exit 1; }; done
    cd site/content && gleam format --check src test && gleam test && gleam run --no-print-progress
    cd site && gleam format src/h0ffmann_site/content.gleam && gleam format --check src test
    cd site && gleam test
    cd site && rm -rf dist && mkdir -p dist && gleam build \
      && esbuild entry.mjs --bundle --minify --format=esm --outfile=dist/app.js --log-level=warning \
      && gleam run -m h0ffmann_site/prerender --no-print-progress > dist/index.html \
      && cp -R static/. dist/
    @echo "site: site/dist"

# Every logo of the timeline still answers at its owner's address. A logo is never a file here.
logos:
    for u in $(grep -v '^#' site/data/timeline.tsv | cut -f6 | grep -E '^https://' | sort -u); do code="$(curl -s -o /dev/null -L --max-time 30 -A 'Mozilla/5.0' -w '%{http_code}' "$u")"; [ "$code" = 200 ] || { echo "logos: $code $u" >&2; exit 1; }; done
    @echo "logos: every logo answers"

md := "nix develop --extra-experimental-features 'nix-command flakes' --no-update-lock-file .#md --command"

# Three analysers over the Markdown files: markdownlint-cli2, Vale, lychee.
# `just md-quality --online` also fetches every web link; `--self-test` gives each one a bad file.
md-quality *args:
    {{md}} scripts/md-quality.sh {{args}}

# The slip box keeps its rules (NOTES.md).
notes:
    scripts/notes-check.sh

# Every row of the site's tables has its cells and its source.
sources:
    scripts/sources-check.sh

# Write CITATION.cff from .zenodo.json. `just citation --check` fails when it is stale.
citation *args:
    {{md}} python3 scripts/citation.py {{args}}

# Licence and copyright for every file (REUSE.toml).
reuse:
    {{md}} reuse lint

# What CI's `.md / quality` runs. Run it before a pull request.
check:
    just md-quality --self-test
    just md-quality
    just notes
    just sources
    just citation --check
    just reuse

