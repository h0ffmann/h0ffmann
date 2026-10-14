---
name: translate-pt-br
description: "Translate a sentence of the site into friendly Brazilian Portuguese and store it in site/data/translations/pt-BR.tsv, with how it was translated and why. Use after any change to a sentence of the page, when `just translations` names an orphan or a sentence with no translation, or when asked to translate, review or improve the Portuguese of the site."
---

# translate-pt-br

The rules are in [`TRANSLATIONS.md`](../../../TRANSLATIONS.md). This page is the order of work.
All rights reserved ([`REUSE.md`](../../../REUSE.md)): this skill is for this profile.

## Before the first sentence

Read the humanizer that this repository uses by link, at its pinned commit:
[mackswendhell/humanizer-pt-br, `SKILL.md` at `ada3599`](https://github.com/mackswendhell/humanizer-pt-br/blob/ada3599ae2732725585f1d93770eeae98c922ff0/SKILL.md)
(MIT, "Copyright (c) 2026 mackswendhell"; pinned in [`../skills.lock`](../skills.lock)). On 14
October 2026 it was the humanizer for Brazilian Portuguese with the most stars on GitHub (46).
Do not copy it into this repository. Its five rules and its 25 patterns are about text that
sounds like a machine wrote it; this page adds what it does not cover, which is translation.

## For each sentence

1. **Take the source exactly**, as the page has it: the string in `site/src/h0ffmann_site/app.gleam`,
   or the cell of a table of `site/data/`. The source is the key. Do not change the English to
   make the Portuguese easier.
2. **Look for the owner's own word first.** `README.pt-BR.md` is his text. If he already said
   it in Portuguese, use his words, and write so in the note.
3. **Say it as a Brazilian would say it out loud**, not word for word. Ask of each sentence:
   would a person in Rio say this to a friend who also writes code?
4. **Check the false friends** of [`site/data/translations/false-friends.tsv`](../../../site/data/translations/false-friends.tsv),
   and add a pair when you meet a new one.
5. **Apply the humanizer**: no filler ("vale destacar que", "com o objetivo de"), no "além
   disso", no dash before a revelation, no closing phrase of effect, short and long sentences
   mixed. Keep the page's lower case.
6. **Keep what stays**: a name, a brand, and a word that Brazilian developers use in English
   (commit, build, fork, stack, port, pull request).
7. **Store the row**: source, translation, `how`, `note`, `status`, `by`, `date`.
   - `plain`: said the same way. `adapted`: a literal translation would be wrong or stiff, and
     the note says why, with the literal form that was avoided. `kept`: left as it is.
   - `status` is `draft` for every row an agent writes. Only the owner makes it `reviewed`.
   - `by` names the agent and the commit of the humanizer.
8. **Run** `just translations`. It must pass, and it prints what is still not translated.
9. **Look at the page**: `just site`, then open `site/dist/index.html?lang=pt-BR`.

## Report

How many rows were added or changed, how many are `adapted` and why for the hard ones, how many
of the page's sentences still have no translation, and that every row is a draft until the
owner reads it.

## Do not

- Do not translate a quotation of the README's history, a repository's own description, or a
  person's name.
- Do not mark a row `reviewed`.
- Do not keep a row whose source changed: translate the new sentence and delete the old row.

## Sources

- [`TRANSLATIONS.md`](../../../TRANSLATIONS.md), written for this repository on 14 October 2026.
- mackswendhell/humanizer-pt-br at `ada3599`, MIT, used by link. It says that it is adapted
  from Wikipedia's "Signs of AI writing".
- The lock by link, and not by copy: the same idea as `.claude/skills/skills.lock` of
  marola-dev/marola-research, by the same author.
