# Notes and journal

This repository keeps two records beside its pages. Both are plain Markdown that Obsidian reads
when you open the repository as a vault. They are the discipline of h0ffmann/closed-source and
marola-dev/marola-research, brought here.

## Notes: `notes/`

A slip box, in the Zettelkasten way: one idea in one note, linked to other notes. A sentence on
the profile or a rule of the design can be followed back to a note.

1. **One idea, one note.**
2. **Own words.** Quote only what must stay exact, in quotation marks, with its source.
3. **A permanent name.** `notes/<id>-<slug>.md`. The id is the UTC time the note was made,
   `YYYYMMDDHHMM`, and it never changes.
4. **Front matter:**

   ```yaml
   ---
   id: "202610132300"
   title: "Four lights"
   type: fleeting | literature | permanent
   status: unverified | partial | verified | open-question | approved
   source: "who or what the idea came from, with the date"
   tags: [design]
   created: 2026-10-13
   ---
   ```

   - *fleeting*: an idea as it came. *literature*: what one source says. *permanent*: a claim of
     this repository, built from other notes.
   - *verified*: the source was read and says it. For a rule or a definition of the owner, the
     source is his message, quoted with its date. *approved*: the owner read the note and
     approved it; only he gives it.
5. **Links.** Every note links to another note with `[[<id>-<slug>]]`, and `notes/index.md`
   links to every note.
6. **Truth.** Never invent a source, a quotation or a number.

`just notes` checks the front matter, the ids and the links.

## Journal: `journal/`

One entry for each challenge met, `journal/<date>-<slug>.md`, with six headings: Challenge,
Context, Options, Decision, Result, Lessons. What went wrong is an entry too. An entry is
appended and not rewritten: a later entry corrects an earlier one. No secret, no private name,
no raw transcript.

## Sources

- The slip box and its rules: h0ffmann/closed-source's `SMART_NOTE_POLICY.md`, which follows
  Luhmann's slip box as Sönke Ahrens describes it in *How to Take Smart Notes*.
- The six headings of a journal entry: the Ouroboric journal format.
- "Append, never rewrite" and "negative results included": h0ffmann/ww3-gpu's lab notebook.
