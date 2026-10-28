---
title: "The cover could not read the pins"
date: 2026-10-28
tags: [cover, tooling]
status: open
---

# The cover could not read the pins

## Challenge

The owner asked for a new cover: zettelkasten in place of picasso, alerts in place of
smart-notes, and a small padlock beside ww3-gpu. Three things stood in the way. `cover/` reads the
pins with GitHub's GraphQL API, which a cloud session cannot call. ww3-gpu is now private, and
`cover/` dropped every private pin. zettelkasten belongs to ouroboric-dev and alerts to piabrota,
and `cover/` drew any pin of an organisation as the organisation, so the boxes would have said
"ouroboric-dev" and "piabrota".

## Options

- Write the pins, the counts and the topics into the drawing by hand.
- Change `cover/` so that the owner's marks decide: `lock` keeps a private pin and draws the
  padlock, `org` makes a box stand for its organisation; and leave the drawing to `just cover`.

## Decision

The second. The skill forbids a count written by hand. The pins themselves are set on the owner's
GitHub profile, which no agent changes.

## Result

`site/data/cover.tsv` carries the marks. A drawing from made-up counts checked the layout; it was
not committed. The real cover waits for the owner to swap the pins and run `just cover`.

## Lessons

A choice that was implicit in the code (every organisation's pin is the organisation) breaks on
the second case. Make it a mark the owner sets.
