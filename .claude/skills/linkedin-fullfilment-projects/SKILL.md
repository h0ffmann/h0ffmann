---
name: linkedin-fullfilment-projects
description: "Make the texts that fill the Projects section of the owner's LinkedIn profile, one for each repository of FEATURED_REPO.md: lower case, his id, the commits, the commit it was reviewed at, the research area and the repository's own description, cut to LinkedIn's sizes. Use when asked for LinkedIn project texts, to refresh them after a repository changed, or to add a repository to the featured list."
---

# linkedin-fullfilment-projects

The rule is "REPO to PROJECT" in [`DERIVATION.md`](../../../DERIVATION.md). This page is the
order of work. All rights reserved ([`REUSE.md`](../../../REUSE.md)): this skill is for this
profile and is not a template for another person's.

## Steps

1. **Read every row of [`FEATURED_REPO.md`](../../../FEATURED_REPO.md).** All of them: the
   texts are made for the whole list, never for a part of it.
2. **If a repository is to be added or removed**, change
   [`site/data/featured.tsv`](../../../site/data/featured.tsv): the owner chooses the rows. Give
   the row its area (`water`, `ideas`, `ouroboric` or `closed`) and its source.
3. **Read the numbers again:** `just featured`. It needs `gh`, signed in. It writes the counts,
   the commits and the commit that each repository was reviewed at, with the day.
4. **Derive:** `just linkedin`. It writes [`LINKEDIN_PROJECTS.md`](../../../LINKEDIN_PROJECTS.md):
   for each repository a name and a text, each with its count of characters.
5. **Look at the sizes.** A text "over the goal" is still allowed; a text over the limit stops
   the build. To shorten one, shorten the repository's description on GitHub, then run steps 3
   and 4 again. Do not edit the derived file.
6. **Report** how many projects were written, which are over the goal, and the day of the
   numbers. Say that the two limits of LinkedIn's form were not read from LinkedIn.

## What each text holds

The owner's id (`h0ffmann`), in lower case; the repository's own description; its research
area; its commits and how many are his; the commit it was reviewed at and the day; with whom;
its licence and its DOI; its address.

## Do not

- Do not write a sentence of your own into a text. A text says what its row says.
- Do not type a number. Do not name a person that the row does not name.
- Do not post anything to LinkedIn. The owner fills the form by hand.
- Do not copy this skill or these texts into another repository, or for another person.

## Sources

- [`DERIVATION.md`](../../../DERIVATION.md) and `scripts/linkedin-projects.py`, in this
  repository.
- The owner's request of 14 October 2026, quoted in `DERIVATION.md`.
