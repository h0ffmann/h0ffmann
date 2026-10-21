---
name: linkedin-cover
description: "Make the owner's LinkedIn cover (1584x396 PNG): the public repositories that h0ffmann pins on GitHub, drawn with the vendored Archify. Use when asked for his LinkedIn cover, a banner of his pinned repositories, or to draw it again after his pins changed. For h0ffmann only."
---

# linkedin-cover

The owner asked for it on 20 October 2026: a cover for LinkedIn from his pinned repositories,
drawn with Archify as in h0ffmann/ww3-gpu, and the code in Rust. It is for h0ffmann only, and is
never run or tested with another GitHub user ([`AGENTS.md`](../../../AGENTS.md), hard rule 5).
All rights reserved ([`REUSE.md`](../../../REUSE.md)).

## Steps

1. **Run** `just cover`. It needs `gh`, signed in, and Chrome (`CHROME` names another).
   - [`cover/`](../../../cover/src/main.rs), in Rust, reads his pins with `gh api graphql`
     and keeps every public one, as GitHub lists them.
   - It writes Archify's input: the user in the middle, the pins in two columns, each with its
     description and five skills at most: its language, then its GitHub topics in GitHub's order.
     A description longer than 72 characters is cut with "…".
   - [`vendor/archify`](../archify/SKILL.md) draws it and checks it (`finalize`); Chrome takes the
     picture. The left quarter stays empty, because LinkedIn's profile photo covers it.
2. **Look at** `build/cover/h0ffmann/cover.png` before you hand it over. A label cut short or a
   line through a box is a fault: say so.
3. **Report** the path of the PNG, how many repositories it shows, and the day the pins were read.
   The title of the drawing names that day.

## Do not

- Do not write a repository, a topic or a language by hand. The picture says what GitHub said.
- Do not edit the JSON that `cover/` writes to make it look better; change `cover/` and its tests
  (`just cover-test`).
- Do not run it, test it or try `cover/` with another GitHub login. `just cover-test` uses
  made-up data.
- Do not upload the picture to LinkedIn. The owner does that by hand.

## Sources

- Archify, tt-a1i/archify, MIT, a submodule pinned at v3.0.1 `2ab3cae`, the pin of h0ffmann/ww3-gpu
  (`.claude/skills/skills.lock`).
- LinkedIn's size for a cover, 1584x396, was not read from LinkedIn.
