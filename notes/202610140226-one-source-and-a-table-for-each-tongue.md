---
id: "202610140226"
title: "One source, and a table for each tongue"
type: permanent
status: partial
source: "Matheus Hoffmann, Claude Code session, 2026-10-14; TRANSLATIONS.md and scripts/translations-check.py of this repository"
tags: [translation, quality, site]
created: 2026-10-14
---

# One source, and a table for each tongue

"dont duplicate sources, use the same mechanism and store the translations."

A page in two languages is usually two pages, and two pages drift. Here the page is written
once. A translation is a row of a table, and the key of the row is the sentence itself. So a
row cannot outlive its sentence: when the English changes, the row matches nothing, and the
check fails.

A row is indexed like a note: it says how it was translated (`plain`, `adapted`, `kept`), why,
by whom and when, and whether a native reader has read it. "Translations should be VERY GOODLY
indexed, as good as a NOTE".

The judge of the translations is judged too: it has a self-test that it must fail, it is one
open file, and it says that it cannot tell whether a translation is right. That is MetaQuality
applied to a translation: the question is not only "is this Portuguese good" but "is the thing
that says so good".

**Status: partial.** The mechanism is verified: it is in the repository and its checks run. The
quality of the Portuguese is not: 114 of 115 rows are drafts by an agent that no native reader
has read.

The rules: `TRANSLATIONS.md`. The look that the two buttons follow: [[202610132300-four-lights]].
