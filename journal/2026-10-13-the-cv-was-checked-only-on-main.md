---
title: "The CV was checked only on main"
date: 2026-10-13
tags: [cv, ci, tooling]
status: open
---

# The CV was checked only on main

## Challenge

The owner asked for two things on the same day: a short CV in English that looks like the site,
with a tip that its links are checked on each merge and the commit it was built from; and the
paper tooling of this repository changed to match marola-dev/marola-research and
h0ffmann/closed-source.

## Context

The CVs were built by one workflow, `cv`, on a push to `main` only, and a bot committed the
PDFs. A change that broke the build was first seen on `main`. In the other two repositories a
paper is rendered by a `just` recipe, committed with its text, and a `pdf` workflow builds it on
each pull request and each push to `main` and compares the committed PDF with the built one.

Two things did not fit that shape as it is:

- The short CV names its commit. A PDF cannot name the commit that it is committed in.
- The other two repositories take their toolchain from picasso's `paper` lab (XeLaTeX). The CVs
  here need lualatex: the Japanese CV uses luatexja and Harano Aji, and the long CVs use the
  badge pills and the filter of nix-config's `publisher` lab. The `paper` lab has none of these.

## Options

1. Leave `cv` as it was and add the new look only.
2. Move everything to the `paper` lab now, and write the Japanese CV and the badges again for
   XeLaTeX.
3. Take the shape and keep the engine: `just cv` and `just current`, a `pdf` workflow on each
   pull request and each push to `main`, the PDFs committed with the change; `publisher` stays
   the toolchain, and `cv` stays on `main` for the one line that only `main` knows.

## Decision

Option 3. `scripts/cv-current.py` compares the words of each committed PDF with the built one
and leaves out the commit in the foot. After a merge, `cv` builds again with the commit of
`main` and commits the PDFs.

## Result

`just cv` renders four PDFs; the short one is one page with 33 links, none of them relative.
`just current` passes on this branch. `pdf / build` runs it on the pull request.

Not done: the toolchain is still `publisher`, not picasso's `paper` lab. To finish the match,
the `paper` lab needs lualatex's packages (luatexja, haranoaji, lua-ul, luacolor, tikz, framed,
titlesec) and the badge filter, and that is a change in h0ffmann/picasso.

## Lessons

- A file cannot hold the name of the commit that holds it. What names a commit is built after
  the commit, or the check leaves that line out.
- A check that runs only on `main` reports a fault after it is merged. The same check on the
  pull request reports it before.
- A relative link in a PDF opens nothing. Write it relative in the source, so that the link
  check reads the file, and make it absolute in the build.
