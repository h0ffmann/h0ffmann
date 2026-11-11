---
title: "The site read headings the README dropped"
date: 2026-11-11
tags: [site, readme, tooling]
status: closed
---

# The site read headings the README dropped

## Challenge

The owner asked for the site to match the new README, with the new repositories, and for every
index to be read again. On `main` at `bd00944`, `just site` failed: two of its tests found the
sentence about the owner empty.

## Context

`site/content` read the sentence under `## 👋 me` and the line under `## 🏅 certs`. The README
was written again by hand in November 2026, with bold headings ("**Piabrota AI Studio**",
"**Research**", "**Misc**") and no `##` heading. The generator found nothing and wrote two empty
strings, and the page had no text where the README had its new sections. CI is off since 29
October 2026, so no check ran on those commits.

## Options

- Put the old headings back in the README.
- Read the README as it is now: its first bold line, the lists under its bold headings, its
  badges, the CVs of its first line and the picture of its library.

## Decision

The second. The README is the owner's text; the generator follows it. Each new reader of the
README has a test in `site/content`, and the page has a test for each list it shows.

## Result

The site shows a "now" section (the headline, the studio and its sites, the research, the
badges) and a "how i read" section with the picture of `media/`, which `just site` copies.

## Lessons

A generator that reads a hand-written file by its headings breaks silently when the file is
written again. A test that the text it reads is not empty is what found it.
