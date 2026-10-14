# Translations

How the website speaks more than one language without having more than one source. All rights
reserved, like the rest of this repository ([`REUSE.md`](REUSE.md)).

## One sentence

The page is written once, in English. A table for each other language holds each sentence of
the page beside the same sentence in that language, and says how it was translated and why.

## The mechanism

| Part | Where | What it does |
|---|---|---|
| the source | `site/src/h0ffmann_site/app.gleam` and the tables of `site/data/` | every sentence, once, in English |
| the table | `site/data/translations/<lang>.tsv` | one row for one sentence: the source **is the key** |
| the build | `site/content` | reads the table into `content.gleam`, as it reads every other table |
| the page | `app.t`, `app.translate` | each sentence is looked up by its source when it is drawn; a sentence with no row is shown in English |
| the switch | two buttons on the cover; `?lang=pt-BR` in the address | the reader's choice is kept in the browser |

Nothing is duplicated: there is no second page, no second copy of a table, and no key that a
person has to invent. When the English of a sentence changes, its old row no longer matches any
sentence, and the check fails until the new sentence is translated.

## A row is indexed like a note

Each row of a table has seven cells, and none may be empty except the note of a plain row.

| Cell | What it holds |
|---|---|
| `source` | the sentence, exactly as the page has it |
| the language | the same sentence in that language |
| `how` | `plain`: said the same way. `adapted`: a literal translation would be wrong or stiff. `kept`: a name or a word that stays |
| `note` | for `adapted`, why, with the literal form that was avoided; for the rest, where the words came from |
| `status` | `draft`: an agent made it and no native reader has read it. `reviewed`: the owner read it, or wrote it |
| `by` | who made the row, and with which skill at which commit |
| `date` | the day |

So a translation says where it came from and how far to trust it, as a note of `notes/` does.

## The quality of the translation, and the quality of its judge

`just translations` (in `just check`, so in CI) judges the tables. It is built so that the judge
itself can be judged:

1. **It can fail.** `just translations --self-test` gives it a bad table with seven faults and
   it must name each one.
2. **It is open.** It is one file, `scripts/translations-check.py`, and its first lines say
   what it checks.
3. **It says what it does not check.** It cannot tell that a translation is right or that it
   reads well. That is the `status` cell, and only a native reader changes it.
4. **It is applied to itself**: the self-test runs in CI beside the check.

What it does check: the seven cells; known words for `how` and `status`; a reason for each
`adapted` row; no source twice; **no orphan** (a row whose sentence is gone from the page); no
false friend of [`site/data/translations/false-friends.tsv`](site/data/translations/false-friends.tsv).
It prints the coverage, which is a measure and not a gate.

## The Portuguese

The Portuguese is Brazilian, friendly and in the page's lower case. It is made with the
`translate-pt-br` skill of this repository, which uses, **by link and at a pinned commit**,
[mackswendhell/humanizer-pt-br](https://github.com/mackswendhell/humanizer-pt-br/blob/ada3599ae2732725585f1d93770eeae98c922ff0/SKILL.md)
(MIT): on 14 October 2026 the humanizer for Brazilian Portuguese with the most stars on GitHub.
No file of it is in this repository ([`.claude/skills/skills.lock`](.claude/skills/skills.lock)).

That skill is about text that sounds like a machine wrote it. It does not speak of translation.
The rules for translation are this repository's own:

- **The owner's own word comes first.** `README.pt-BR.md` is his text.
- **Not word for word.** "built in the open" is "feita às claras"; "the work did not" is "o
  trabalho, não".
- **False friends are a table**, and the check reads it: "record" is "registro" and not
  "recorde"; "trade" is "ofício" and not "comércio".
- **A word that Brazilian developers use in English stays**: commit, build, fork, stack, port.

## The state on 14 October 2026

115 rows in `pt-BR.tsv`. One is `reviewed`: the paragraph about the owner, which is his own text
from `README.pt-BR.md`. The other 114 are **drafts by an agent**. They were not read by a native
reader. The names of companies, the descriptions that repositories give themselves, the
quotations of the README's history and the three "how i work" headings are not translated.

## To add a language

Add `site/data/translations/<lang>.tsv` with the same header, a case for it in `app.translate`
and in `lang_ffi.mjs`, and a button in `tongues`. The check reads every table of the folder.

## Sources

- Written for this repository. The idea that the judge of quality must be judged is the note
  "What is MetaQuality" of h0ffmann/closed-source, by the same author.
- The owner's request of 14 October 2026: "dont duplicate sources, use the same mechanism and
  store the translations", "to avoid false friends or literal translation losing meaning",
  "Translations should be VERY GOODLY indexed, as good as a NOTE".
