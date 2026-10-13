#!/usr/bin/env bash
# sources-check: every fact of the site's tables says where it was read (AGENTS.md, hard rule 3).
# For each site/data/*.tsv: the last comment line names the columns; every row has that many
# cells; and when a column is named `source`, no row leaves it empty.
#   scripts/sources-check.sh
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
bad=0
for f in site/data/*.tsv; do
  header="$(grep '^# ' "$f" | tail -1 | sed 's/^# //')"
  n="$(awk -F'\t' '{print NF}' <<<"$header")"
  src="$(tr '\t' '\n' <<<"$header" | grep -nx 'source' | cut -d: -f1 || true)"
  rows=0
  while IFS= read -r line; do
    case "$line" in "" | \#*) continue ;; esac
    rows=$((rows + 1))
    cells="$(awk -F'\t' '{print NF}' <<<"$line")"
    [ "$cells" = "$n" ] || { echo "sources-check: $f: a row has $cells cells, the header has $n: ${line:0:60}" >&2; bad=1; }
    if [ -n "$src" ]; then
      [ -n "$(cut -f"$src" <<<"$line" | tr -d '[:space:]')" ] || { echo "sources-check: $f: a row has no source: ${line:0:60}" >&2; bad=1; }
    fi
  done <"$f"
  [ "$rows" -gt 0 ] || { echo "sources-check: $f has no row" >&2; bad=1; }
done
[ "$bad" = 0 ] || exit 1
echo "sources-check: every row of site/data has its cells and its source" >&2
