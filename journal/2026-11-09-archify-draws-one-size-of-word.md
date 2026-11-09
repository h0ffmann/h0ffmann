---
title: "Archify draws one size of word"
date: 2026-11-09
tags: [site, topics, tooling]
status: closed
---

# Archify draws one size of word

## Challenge

The owner asked for an index of his most used GitHub topics as a word cloud, where the most used
topic is the biggest word, drawn with Archify. Archify draws boxes and arrows, and every label at
the same size: its schema has no field for the size of a word.

## Context

`vendor/archify` already draws the LinkedIn cover, and `cover/` sets picasso's look over
Archify's geometry in a frame. The repository list (`site/data/repos.tsv`) was from 13 October
2026, without piabrota.

## Options

- Draw the cloud without Archify, as an SVG written by a script.
- Let Archify place and check boxes sized by each topic's count, and set each word's size from
  its box afterwards.
- Edit the SVG in the HTML that Archify writes.

## Decision

The second. Archify keeps the geometry and its four gates (validate, deliver, check,
browser-check). The third option was tried first and did nothing: Archify's viewer draws the
diagram again from its JSON when the page loads, so a change to the written SVG is lost. The
frame (`scripts/topics-frame.py`) adds a script that sizes each word on every drawing.

## Result

`just topics` reads the three accounts again, writes `site/data/repos.tsv` and
`site/data/topics.tsv`, and draws `site/static/topics.png`; the site shows it in "topics, by
size". The colour of a word is the light (`DESIGN.md`) of most of the repositories that carry it.

## Lessons

When a tool redraws from its input, change what it draws in the page that shows it, not in the
file it wrote.
