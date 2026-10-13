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
