---
title: "The lit mark was off the screen"
date: 2026-10-14
tags: [site, arc, motion]
status: closed
---

# The lit mark was off the screen

## Challenge

The arc was made to run sideways while the reader scrolls down, as the owner asked, after
sheets.works' "holding up the internet". The first version lit the mark at an even share of the
marks: halfway down, the tenth of nineteen. Halfway down, in a browser, the lit mark was half off
the left edge of the screen, and the next one, dimmed, was in the middle.

## Context

The timeline moves by its extra width, which comes from the pixels of each mark. The share of
the marks counts marks, not pixels. The two agree only when every mark is as wide as the others,
and the big mark (the medal) was wider.

## Options

- Read where every mark is from the browser on each frame, and find the one in view.
- Make every mark the same width, and find the mark from the width.

## Decision

The second. It keeps the decision in Gleam (`app.mark_at`), with a number for each frame and not
a list of boxes. The place that is lit crosses the stage from its left edge to its right one, so
the first mark is lit at the start and the last one at the end.

## Result

Headless Chrome at 1280 × 800 and 390 × 844, at 0, ¼, ½, ¾ and the end: the lit mark is on the
screen at every point, and the page never scrolls sideways. On a phone the screen is a little
wider than one mark, so the lit one can be cut at the left edge as it leaves.

## Lessons

- A scroll effect is checked in a browser, at more than one width, at more than one point of the
  scroll. A unit test of the arithmetic did not see this.
