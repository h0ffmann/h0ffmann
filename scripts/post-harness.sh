#!/usr/bin/env bash
# post-harness.sh — Orchestrates post lifecycle using DSH, OMP and Pi.
# Usage: ./scripts/post-harness.sh <command> [args]
#
# Commands:
#   new <slug>          Create a new post scaffold (front matter + STE skeleton)
#   draft <file>        Open the post in $EDITOR with OMP prompt active
#   check <file>        Run STE + snippets + link checks
#   publish <file>      Mark post as ready and list publish targets (Medium/Substack/Leanpub)
#   list                List all posts and their status

set -euo pipefail

POSTS_DIR="${POSTS_DIR:-posts}"
SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATE_FMT="+%Y-%m-%d"

# --- Tool detection ----------------------------------------------------------
require_tool() {
    local tool="$1" hint="$2"
    if ! command -v "$tool" >/dev/null 2>&1; then
        echo "⚠️  $tool not found. $hint" >&2
        return 1
    fi
    return 0
}

dsh()  { require_tool dsh  "Install DSH to enable shell harness features."; }
omp()  { require_tool omp  "Install OMP (oh-my-posh) for prompt theming."; }
pi()   { require_tool pi   "Install Pi CLI to enable AI-assisted drafting."; }

# --- Commands ----------------------------------------------------------------
cmd_new() {
    local slug="${1:?slug required}"
    local date
    date="$(date "$DATE_FMT")"
    local file="$POSTS_DIR/${date}-${slug}.md"

    mkdir -p "$POSTS_DIR"
    [[ -f "$file" ]] && { echo "❌ $file already exists"; exit 1; }

    cat > "$file" <<MD
---
title: "${slug//-/ }"
date: $date
skill: asd-ste100 v0.4.0 (STE-flavored mode)
tags: []
status: draft
harness: [dsh, omp, pi]
---

<!-- STE skeleton: max 25 words per sentence, max 6 sentences per paragraph. -->
<!-- Use short, direct sentences. One idea per sentence. -->

## What this post is

<!-- One paragraph. -->

## Why it matters

<!-- One paragraph. -->

## Proof

<!-- Facts with sources. -->

## Not checked

<!-- Plain list of what was not verified. -->

peace
MD
    echo "✅ Created $file"
    echo "   Next: just post-draft $file"
}

cmd_draft() {
    local file="${1:?file required}"
    [[ -f "$file" ]] || { echo "❌ $file not found"; exit 1; }

    # Activate OMP theme if available
    if omp; then
        echo "🎨 OMP theme active: $(omp get theme 2>/dev/null || echo 'default')"
    fi

    # Activate DSH shell harness if available
    if dsh; then
        echo "🐚 DSH harness active"
    fi

    # Optional: Pi-assisted STE review
    if pi; then
        echo "🤖 Pi: reviewing STE compliance of $file..."
        pi ste-review "$file" 2>/dev/null || echo "   (Pi ste-review skipped)"
    fi

    ${EDITOR:-vi} "$file"
}

cmd_check() {
    local file="${1:?file required}"
    [[ -f "$file" ]] || { echo "❌ $file not found"; exit 1; }

    echo "🔍 Checking $file"
    echo "---"

    # 1. STE structural check
    echo "[1/3] STE structure"
    python3 "$SCRIPTS_DIR/ste-check.py" "$file" || true

    # 2. Snippet compilation
    echo "[2/3] Snippet compilation"
    python3 "$SCRIPTS_DIR/snippets-check.py" "$file" || true

    # 3. Link check (basic)
    echo "[3/3] Link check"
    python3 "$SCRIPTS_DIR/links-check.py" "$file" || true

    echo "---"
    echo "✅ Check complete"
}

cmd_publish() {
    local file="${1:?file required}"
    [[ -f "$file" ]] || { echo "❌ $file not found"; exit 1; }

    # Flip status to ready
    if grep -q '^status: draft' "$file"; then
        sed -i.bak 's/^status: draft/status: ready/' "$file" && rm -f "${file}.bak"
        echo "📤 Status set to 'ready': $file"
    else
        echo "ℹ️  Status already non-draft"
    fi

    echo ""
    echo "Publish targets:"
    echo "  • Medium   — copy $file body into new story"
    echo "  • Substack — copy $file body into new post"
    echo "  • Leanpub  — for closed-source companion pieces"
    echo ""
    echo "Run 'just post-list' to see all ready posts."
}

cmd_list() {
    echo "📚 Posts in $POSTS_DIR/"
    echo "---"
    for f in "$POSTS_DIR"/*.md; do
        [[ -f "$f" ]] || continue
        local title status date
        title=$(grep -m1 "^title:" "$f" 2>/dev/null | cut -d":" -f2- | tr -d '"' | xargs || echo "(no title)")
        status=$(grep -m1 "^status:" "$f" 2>/dev/null | cut -d":" -f2- | xargs || echo "draft")
        date=$(basename "$f" | grep -oE "^[0-9]{4}-[0-9]{2}-[0-9]{2}" || echo "????-??-??")
        status="${status:-draft}"
        printf "  %s  %-8s  %s\n" "$date" "$status" "$title"
    done
    return 0
}

# --- Dispatch ----------------------------------------------------------------
cmd="${1:-help}"; shift || true
case "$cmd" in
    new)     cmd_new "$@" ;;
    draft)   cmd_draft "$@" ;;
    check)   cmd_check "$@" ;;
    publish) cmd_publish "$@" ;;
    list)    cmd_list ;;
    help|*)
        sed -n '2,10p' "$0"
        ;;
esac
