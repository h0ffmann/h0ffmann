---
title: "A CV for a reader that is not named"
date: 2026-10-14
tags: [cv, facts, tooling]
status: open
---

# A CV for a reader that is not named

## Challenge

The owner asked for a formal English CV and a one-page presentation letter, written for the
directors and researchers of one ocean-research institute, with the suffix `en.OCEAN`. The two
documents may not name the institute. They must keep the skill set of his general CV whole, cite
his ocean works by DOI with a badge to each repository, and come out of this repository's CV
pipeline.

## Context

Three things did not line up.

- The pipeline builds CVs from the READMEs: `cv/prepare.py` strips the profile's markers and
  prepends a header, and `cv/build.sh` renders each with the badge filter and `cv/preamble.tex`.
  A hand-written Markdown file had never gone through it.
- The sources of the facts disagree in two places. The general CV (the owner's job-search
  workspace, at the commit that merged its Markdown form) says Stone was October 2017 to April
  2019 and the instrumentation laboratory September 2015 to October 2017; the README's arc says
  2017–2018 and 2016–2017.
- Hard rule 2 says every text about him cites all six DOIs. The task names three ocean works and
  one book. A one-page letter has little room for six DOIs.

## Options

1. A second pipeline for the pair (pandoc's default template, as the general CV's export uses):
   no badges, a different look, one more thing to keep.
2. The same pipeline: a hand-written Markdown file goes through `prepare.py` unchanged (it has
   no markers), with its own letterhead, and `build()` gets two more calls. The letter's size and
   margins are set after the preamble with `\AtBeginDocument`, so the preamble is not touched.
3. For the dates: the README's arc, the general CV, or ask.

## Decision

Option 2: two `build()` calls, one letterhead (`cv/header.en.OCEAN.md`, the contact details of
`cv/header.md` without the QR), and the build fails when the CV passes two pages or the letter
one. The dates are the general CV's, which names the month, and the pull request lists each
difference as a question for the owner. The six DOIs: the three ocean works in full in the CV,
the other three in one small line; in the letter, one small line under the signature.

## Result

`cv.en.OCEAN.pdf` is two pages and `letter.en.OCEAN.pdf` one, in the same build as the four CVs
of the profile. Neither names the institute (`pdftotext`, searched). The unit tests cover the
pair's emoji (there are none). What the owner has to decide is in the pull request: the dates,
the city on the letterhead, the title of the laboratory position, the phone number that the
general CV shows and this public repository does not.

## Lessons

- A pipeline that prepends a header and passes the rest through takes a hand-written file for
  free. Reuse it before writing another.
- When two of the owner's own sources disagree, the document takes the more precise one and the
  pull request asks; the document does not pick in silence.
- A rule of the repository (cite all six) holds in a tailored document too. The room it takes is
  one small line.
