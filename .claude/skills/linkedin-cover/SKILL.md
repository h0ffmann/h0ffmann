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
     and keeps every public one, as GitHub lists them, and a private one that the owner marked
     `lock` in [`site/data/cover.tsv`](../../../site/data/cover.tsv) (Noto Emoji's padlock,
     `cv/emoji/`, beside its name).
   - It writes Archify's input on a small canvas (about 720x180 units), so that Archify's own type
     comes out about 2.2 times larger at 1584x396 and stays readable on LinkedIn's profile page
     without opening the cover. The pins are a grid of 3x2, each with its name and the skills
     that fit on one line: the owner's choice in
     [`site/data/cover.tsv`](../../../site/data/cover.tsv), or else its language, then its GitHub
     topics in GitHub's order. Under them, the commits of its default branch and its contributors
     (GitHub's accounts of type User, less `claude`, whose commits the owner's box counts; no
     bots), read by `just cover`. A pin the owner marked `org` shows its organisation: its name, and
     the commits, the contributors and the stars of all its public source repositories, with a
     pill of its address and its count of repositories. A small pill under each box gives its
     stars, when it has any. The `marks` of `site/data/cover.tsv` add Brazil's flag (`br`, drawn,
     not an emoji) and the DOI of the work of the same name in `site/data/works.tsv` (`doi`).
     There are no lines between boxes.
   - The top-left box: the account's age in whole years, its contributions this year, after the year (GitHub's
     calendar, which counts private ones only if the profile shows them), its commits this year
     with the official trailer "Co-Authored-By: Claude ... <noreply@anthropic.com>" (GitHub's
     commit search: default branches of public repositories only), and the three languages of
     the last 30 days (the files that his commits changed, as GitHub links the commits to his
     account, read from a clone without blobs: a commit counts once for each language; shell,
     Nix, data and documents count for none). A pill on its top edge gives the address on GitHub, in text: no logo is drawn (hard rule 4).
     The cell below it stays empty for the profile photo.
   - `vendor/archify` (its skill is `.claude/skills/archify`, once checked out) draws it and checks it (`finalize`); Chrome takes the
     picture of the drawing cropped to 4:1.
   - The frame sets picasso's look over Archify's geometry (h0ffmann/picasso,
     `site/static/style.css`): its dark palette, one accent for the owner's box only, in the blue of marola's logo
     (`#1BADC5`, the middle stop of its gradient; the owner, 22 October 2026), Fjalla One for
     names and Inter for the rest, both from Google Fonts while Chrome takes the picture, larger
     than Archify's own type.
2. **Look at** `build/cover/h0ffmann/cover.png` before you hand it over, and at a copy shrunk to
   804 px wide, about the size of the profile page. Text that touches a box's edge, or that you
   cannot read at 804 px, is a fault: say so.
3. **Report** the path of the PNG, how many repositories it shows, and the day the pins were read.
   The title of the drawing names that day.

## Do not

- Do not write a repository, a topic, a language or a count by hand. The picture says what GitHub said.
- Do not edit the JSON that `cover/` writes to make it look better; change `cover/` and its tests
  (`just cover-test`).
- Do not run it, test it or try `cover/` with another GitHub login. `just cover-test` uses
  made-up data.
- Do not upload the picture to LinkedIn. The owner does that by hand.

## Sources

- Archify, tt-a1i/archify, MIT, a submodule pinned at v3.0.1 `2ab3cae`, the pin of h0ffmann/ww3-gpu
  (`.claude/skills/skills.lock`).
- LinkedIn's size for a cover, 1584x396, was not read from LinkedIn.
