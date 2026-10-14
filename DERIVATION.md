# Derivation: from a repository to a project

How one thing of this repository is made from another, with no fact added on the way. The idea
and the word are from h0ffmann/closed-source's `DERIVATION.md`, by the same author, where a note
becomes an essay. Here a repository becomes a project: a text for the "Projects" section of a
LinkedIn profile. All rights reserved, like the rest of this repository ([`REUSE.md`](REUSE.md)).

## The rule that makes it short

**Nothing new is written at the last step.** The slow work is done once, at the source: a
repository's description is written in the repository, its numbers are read from GitHub, its
area is set by hand in one table. The last step only chooses, orders and cuts to size.

## REPO to PROJECT

| Step | From | To | Who does it |
|---|---|---|---|
| 1. choose | every repository of `h0ffmann`, `marola-dev` and `ouroboric-dev` | a row of [`site/data/featured.tsv`](site/data/featured.tsv): owner, name, area, with whom | the owner, by hand |
| 2. read | the row, and GitHub on that day | a row of [`FEATURED_REPO.md`](FEATURED_REPO.md): the repository's own description, its commits, his commits, the commit it was reviewed at, its licence, its DOI | `just featured` |
| 3. derive | the row of `FEATURED_REPO.md`, and nothing else | a name and a text in [`LINKEDIN_PROJECTS.md`](LINKEDIN_PROJECTS.md) | `just linkedin` |
| 4. fill | the two blocks of the text | the form on LinkedIn | the owner, by hand |

## The shape of a project text

In this order, in lower case, one fact for each part:

1. **the description**: the repository's own, word for word. A word with two capitals or more is
   an acronym and keeps them (GPU, WAVEWATCH).
2. **the research area**: one of the four of [`DESIGN.md`](DESIGN.md).
3. **the commits**: all of the default branch, and how many are `h0ffmann`'s.
4. **the commit it was reviewed at**, seven characters, and the day.
5. **with whom**, when the work is not his alone.
6. **the licence** and **the DOI**, when there is one.
7. **the address**, with no `https://`, so that it reads as a name.

The name is the repository's name; a repository of an organisation has the organisation after
it, in brackets.

## Size

LinkedIn's form cuts what is too long, so size is a rule and the build checks it.

- The build refuses a name over 255 characters or a text over 2,000. Those two numbers were
  **not read from LinkedIn** when this was written: its pages need a sign-in. Check them in the
  form and change them in `scripts/linkedin-projects.py`.
- The build asks for a text of 420 characters or fewer, which is read in one look, and says
  which texts are over it.
- **A text that is too long is cut at its source**: shorten the repository's description on
  GitHub and run the two recipes again. Never edit `LINKEDIN_PROJECTS.md` by hand.

## What a derived text may not do

- Say a thing that its row does not say. No adjective, no "leading", no "passionate".
- Give a number that was typed in.
- Name a person that the row does not name.
- Be older than its table: `just linkedin --check` fails when it is.

## Sources

- h0ffmann/closed-source, `DERIVATION.md` (note to essay), by the same author, 14 October 2026.
- The owner's request of 14 October 2026: "It should use my id. lower case, Showing number of
  commits, last review commit sha, research areas, and the DESCRIPTION field. respecting
  PROJECTS fillment of linkedin. So size is important".
