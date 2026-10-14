#!/usr/bin/env bash
# md-quality: three analysers over every Markdown file of this repository.
#   - markdownlint-cli2: the structure (.markdownlint-cli2.jsonc)
#   - Vale: plain words and no selling (.vale.ini, .vale/styles/profile/)
#   - lychee: links to files and headings that do not exist; with --online, dead web links too
# The tools come from the flake's `md` shell (`just md-quality` enters it), pinned by flake.lock.
# The same three tools and the same shape as marola-dev/marola-research's and
# h0ffmann/closed-source's scripts/md-quality.sh, by the same author.
#   scripts/md-quality.sh              # structure, prose, local links: what CI runs
#   scripts/md-quality.sh --online     # the same, and lychee fetches every web link
#   scripts/md-quality.sh --self-test  # each analyser must refuse a bad file
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

# Google's text beside its emoji is not this repository's.
files() { git ls-files '*.md' | grep -v '^cv/emoji/'; }
# Vale's rules are for English: not the Portuguese and Japanese READMEs, and not the CV's
# headers, which are LaTeX and badges.
prose() { files | grep -Ev '(pt-BR|\.ja\.md$|^cv/header)' || true; }

self_test() {
  local d; d="$(mktemp -d)"; trap 'rm -rf "$d"' RETURN
  fail() { echo "md-quality: self-test: $1" >&2; exit 1; }
  printf '# A page\n\n\n\nTwo blank lines above.\n\n# A second title\n' >"$d/structure.md"
  ! markdownlint-cli2 --config .markdownlint-cli2.jsonc "$d/structure.md" >/dev/null 2>&1 \
    || fail "markdownlint passed two blank lines and two titles"
  printf '# A page\n\nA passionate engineer who can utilize a very good tool.\n' >"$d/prose.md"
  ! vale --config .vale.ini --no-wrap "$d/prose.md" >/dev/null 2>&1 || fail "Vale passed 'passionate', 'utilize' and 'very'"
  printf '# A page\n\nThe source says "a highly concurrent\ntoolkit". It has 3 parts.\n' >"$d/quote.md"
  vale --config .vale.ini --no-wrap "$d/quote.md" >/dev/null 2>&1 || fail "Vale refused a word inside a quotation"
  printf '# A page\n\n[a file that is not there](not-there.md)\n' >"$d/link.md"
  ! lychee --offline --no-progress "$d/link.md" >/dev/null 2>&1 || fail "lychee passed a link to a file that does not exist"
  echo "md-quality: self-test ok: each of the three refused a bad file" >&2
}

online=0
case "${1:-}" in
  --self-test) self_test; exit 0 ;;
  --online) online=1 ;;
  "") ;;
  *) echo "md-quality: usage: scripts/md-quality.sh [--online | --self-test]" >&2; exit 1 ;;
esac

mapfile -t all < <(files)
mapfile -t english < <(prose)
bad=0

echo "md-quality: structure: markdownlint-cli2 on ${#all[@]} files" >&2
log="$(mktemp)"
markdownlint-cli2 "${all[@]}" >/dev/null 2>"$log" || { grep -E ' (error|warning) ' "$log" >&2 || cat "$log" >&2; bad=1; }
rm -f "$log"

echo "md-quality: prose: Vale on ${#english[@]} files (an error fails; a warning is advice)" >&2
vale --no-wrap --output=line "${english[@]}" >&2 || bad=1

# The repository's own published site is not fetched: a page that a pull request adds does not
# exist before the pull request is merged, and `site / build` is the check of what it will be.
pages='^https://h0ffmann\.github\.io/h0ffmann/'
# 403, 405, 429 and LinkedIn's 999 count as an answer: the site is there and refuses a robot, or
# asks it to slow down. A site that is busy for a moment must not fail a pull request, and a
# dead link must: each link is tried five times, and if one still fails lychee runs once more
# after a minute, which fetches only the links that failed (`--cache`).
if [ "$online" = 1 ]; then
  echo "md-quality: links: lychee on ${#all[@]} files, web links too" >&2
  web() {
    # Two requests at a time to one host, half a second apart: this repository has many links to
    # github.com, and github.com answers 500 and 503 to a checker that asks too fast (14 October
    # 2026: three runs failed that way, on links that were alive).
    lychee --no-progress --include-fragments --max-concurrency 6 --max-retries 4 --retry-wait-time 5 \
      --host-concurrency 2 --host-request-interval 500ms \
      --timeout 30 --cache --max-cache-age 1h --accept 200,403,405,429,999 \
      --exclude "$pages" "${all[@]}" >&2
  }
  rm -f .lycheecache
  web || { echo "md-quality: links: a link did not answer; the second and last try in 60 s" >&2; sleep 60; web || bad=1; }
  rm -f .lycheecache
else
  echo "md-quality: links: lychee on ${#all[@]} files, local links (run --online for the web)" >&2
  lychee --offline --no-progress --include-fragments "${all[@]}" >&2 || bad=1
fi

[ "$bad" = 0 ] || { echo "md-quality: failed" >&2; exit 1; }
echo "md-quality: ok" >&2
