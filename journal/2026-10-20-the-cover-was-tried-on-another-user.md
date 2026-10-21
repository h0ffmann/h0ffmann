---
title: "The cover was tried on another user"
date: 2026-10-20
tags: [cover, rules, tooling]
status: closed
---

# The cover was tried on another user

## Challenge

The owner asked for a LinkedIn cover from the pinned repositories of "any given github
username". To check that claim, the agent ran the first version for one other public GitHub
user. While it worked, the owner set the rule that the cover is for his profile only, and that
it is never tested with another user.

## Context

Hard rule 1 already said that nothing here is used for another person's profile. A cover that
takes any login is that use, and the first version did not say so.

## Options

- Keep the login as an argument and trust the rule in `AGENTS.md`.
- Fix the login to h0ffmann in `just cover`, and test `cover/` with made-up data only.

## Decision

The second. `just cover` takes no login and `_cover` refuses any login but h0ffmann. The rule is
hard rule 5 of `AGENTS.md`, and `REUSE.md` says it too. The other user's output was deleted
from `build/cover/` before any commit; nothing of it was committed.

## Result

`just cover` draws only h0ffmann's pins. `just cover-test` runs on made-up repositories.

## Lessons

When a tool can read another person's data, ask whose data it may read before the first run,
and check that claim on the owner's own data.
