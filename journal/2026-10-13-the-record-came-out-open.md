---
title: "The record came out open"
date: 2026-10-13
tags: [zenodo, licence, release]
status: open
---

# The record came out open

## Challenge

The first release of this repository was meant to make a closed record on Zenodo, under "all
rights reserved". The record that Zenodo made is open, and it names the MIT licence.

## Context

The owner asked for the profile's own DOI in the pull request that changed its licence from MIT
to all rights reserved. `.zenodo.json` said `"access_right": "closed"` and named no licence. The
release was cut at the pull request's commit, before the merge.

Read from Zenodo's record minutes later: the files are public and the rights are `mit`. Zenodo
did not apply the access field to a GitHub release. With no licence in the file it took the one
that GitHub showed for the default branch, and the default branch still had the old MIT
`LICENSE`.

## Options

- Write the DOI into the pages and say nothing.
- Say it at the top of the pull request, ask the owner to restrict the record on zenodo.org, and
  make a check that stops the same thing next time.

## Decision

The second. Only the owner can edit the record, so the pull request leads with the steps.

## Result

Open until the owner edits the record. DOI of the profile: 10.5281/zenodo.23352630; of v0.1.0:
10.5281/zenodo.23352631. `.zenodo.json` now names a licence, and `scripts/citation.py` fails
when it names none. That the field is kept by Zenodo was not tested: a test is another DOI.

## Lessons

- Zenodo's webhook reads the licence that GitHub shows for the default branch. Merge the licence
  first, then release.
- A field in a metadata file is a request. Read the record back at once and compare.
- A step that cannot be undone is tried first on something that can be thrown away.
