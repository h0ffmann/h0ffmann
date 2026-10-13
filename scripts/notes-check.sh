#!/usr/bin/env bash
# notes-check: the slip box of this repository keeps its rules (NOTES.md).
#   - every notes/<id>-<slug>.md has front matter with id, title, type, status, source, created;
#   - the id is the file name's and is unique; type and status are known values;
#   - every [[link]] points to a note that exists; every note links to another note;
#   - notes/index.md links to every note.
# The same check as marola-dev/marola-research's scripts/notes-check.sh, by the same author; the
# rules are h0ffmann/closed-source's `tools/fabric notes-check`.
#   scripts/notes-check.sh
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
dir="notes"
[ -d "$dir" ] || { echo "notes-check: no notes/; nothing to check" >&2; exit 0; }
bad=0
err() { echo "notes-check: $1" >&2; bad=1; }
[ -f "$dir/index.md" ] || err "$dir/index.md is missing"
n=0
for f in "$dir"/*.md; do
  base="$(basename "$f" .md)"
  [ "$base" = index ] && continue
  n=$((n + 1))
  [[ "$base" =~ ^([0-9]{12})-[a-z0-9-]+$ ]] || { err "$f: the name is not <12 digits>-<slug>"; continue; }
  id="${BASH_REMATCH[1]}"
  fm="$(awk 'NR==1 && $0=="---" {on=1; next} on && $0=="---" {exit} on' "$f")"
  for k in id title type status source created; do
    grep -qE "^$k: " <<<"$fm" || err "$f: front matter has no $k"
  done
  grep -qE "^id: \"$id\"$" <<<"$fm" || err "$f: the id in the front matter is not $id"
  grep -qE '^type: (fleeting|literature|permanent)$' <<<"$fm" || err "$f: type is not fleeting, literature or permanent"
  grep -qE '^status: (unverified|partial|verified|open-question|approved)$' <<<"$fm" || err "$f: status is not a known value"
  links="$(grep -oE '\[\[[^]]+\]\]' "$f" | tr -d '[]' | sort -u || true)"
  [ -n "$links" ] || err "$f: links to no other note"
  for l in $links; do [ -f "$dir/$l.md" ] || err "$f: [[${l}]] is not a note"; done
  grep -qF "[[$base]]" "$dir/index.md" 2>/dev/null || err "$dir/index.md does not link to $base"
done
dup="$(ls "$dir" | grep -oE '^[0-9]{12}' | sort | uniq -d || true)"
[ -z "$dup" ] || err "two notes share the id $dup"
[ "$bad" = 0 ] || exit 1
echo "notes-check: $n notes, all linked" >&2
