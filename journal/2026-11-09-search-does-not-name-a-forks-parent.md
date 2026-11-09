---
title: "Search does not name a fork's parent"
date: 2026-11-09
tags: [site, topics, forks, tooling]
status: open
---

# Search does not name a fork's parent

## Challenge

The owner asked for a second topic cloud from his public forks, his "indirect interests". A fork
rarely carries topics of its own, so the cloud has to count the topics of each fork's parent. The
session could read GitHub only through its repository search, and a search result does not name a
fork's parent.

## Context

`site/data/forks.tsv` had 37 forks of h0ffmann with their parents, read with `gh repo list` on 14
October 2026. On 9 November 2026 the three accounts had 123 public forks.

## Options

- Read each fork with `gh api repos/<owner>/<name>`, which gives its parent.
- Find the parent by search: a repository of the same name whose description is the fork's.

## Decision

The second, because the session could only search. A parent already in `forks.tsv` is kept. Then
`scripts/repos.py` tries the owner's own accounts first (h0ffmann/room is a fork of
piabrota/room), then the same name and description, then the same name with the most stars. The
`parent_read` column says which one found each parent.

## Result

The first pass named quoroom-ai/room as the parent of h0ffmann/room, because a search for "room"
did not return piabrota/room on its first page. The second pass tries his own accounts first.
Some parents are still found by name alone. The script prints them, and each row says so.

## Lessons

When a source cannot give a fact, record how the fact was guessed beside the fact. A later run
with `gh api` can then replace the guesses.
