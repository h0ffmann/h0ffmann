# DESIGN.md

The rules of how this profile looks: the site of `site/`, and what the READMEs borrow from it.
The owner set the meaning of the colours on 13 October 2026; the rest follows from it. An agent
that changes the look reads this page first, and changes this page in the same commit.

All rights reserved, like the rest of this repository ([`REUSE.md`](REUSE.md)): these rules are
for this profile and are not a kit for another one.

## One sentence

A dark sea at night, and four lights on it.

## The four lights

A colour is never decoration here. It says what kind of thing you are looking at, and it says
the same on every part of the page.

| Light | Token | Hex | It means | In the data |
|---|---|---|---|---|
| **blue** | `--water` | `#36B7FF` | **water intuition**: the sea, and what is felt, measured or built for it. marola, ww3-gpu, marola-bench, a race in open water | `water` |
| **green** | `--ideas` | `#3DFF96` | **knowledge**: an idea that was worked out and written down. game theory, tools, notes, a DOI | `ideas` |
| **orange** | `--ouro` | `#FF8A1F` | **Ouroboric ideas**: self-improving apps, work that improves itself, and what is made with those friends. Orange is Ouroboric's own colour | `ouroboric` |
| **red** | `--closed` | `#FF4D62` | **closed source**: the book, the old closed thesis, and this page's own notice that it is not a template | `closed` |

Rules:

1. **Four, and no fifth.** A thing that fits none of them is neutral: `--ink` or `--muted`.
2. **One thing, one light.** A work, a repository or a mark has one `topic`. It is set in
   `site/data/`, by hand, never in the code and never by a guess of the build.
3. **The name is green and the epithet is blue.** `h0ffmann` is knowledge; "the aquatic
   prometheus" is water. Under them one sentence is orange: "i'm always reverse engineering my
   own interests. that is what makes me ouroboric." It is the owner's (14 October 2026), and
   it is orange because it says what makes him Ouroboric. Nothing else on the cover takes a
   light.
4. **Red is rare.** It marks closed source and the notice. It is not an error colour and not an
   accent.
5. **Each area of research has its light and its home.** Wave modelling is blue and links to
   marola-dev; game theory is green; self-improving apps is orange and links to the ouroboric-dev
   organisation. The three stand together above the knowledge graph.
6. **A light is not the only sign.** Where a colour tells something, words tell it too: the
   name of the topic on its button, the word "private", the era under a mark.

## The ground

| Token | Hex | Use |
|---|---|---|
| `--night` | `#05090E` | the page |
| `--deep` | `#0A121B` | the panel of the knowledge graph |
| `--surface` | `#0E1924` | the empty part of a bar |
| `--rule` | `#1C2B38` | a line between two things |
| `--ink` | `#E7F2EF` | words |
| `--muted` | `#8FA3AD` | words that are data or a caption |

The page is dark and has no light theme. White is for the largest headings and for the chip
behind a logo, and for nothing else.

## Glow

A light may glow, like a tube of neon: a soft shadow of its own colour.

- **It may glow:** the name, the epithet, a mark of the timeline, a node of the graph, a counter,
  a pressed button, the bar of a language.
- **It never glows:** a paragraph, a caption, a link in a sentence, a logo.
- One glow has one colour, the colour of the thing. No rainbow, no white glow.
- A gradient is allowed in two places: the wash of the cover, and a language's bar (from blue
  to green). Nowhere else.

## Type

| Role | Face | Where |
|---|---|---|
| the name and the headings | Bricolage Grotesque, 800 or 600 | `h1`, `h2`, the name of a work, a counter |
| the story | Newsreader | every sentence |
| data | JetBrains Mono | a date, a hash, a DOI, a count's label, the labels of the graph |
| a word in its own script | Noto Serif JP | 名残 in the arc, 無 at the centre of the graph |

- **Lower case**, as in picasso's README: headings, buttons, the story. An acronym keeps its
  capitals (DOI, FOSS, MLOps, UFRJ), and so does a name that is written with one (Stone, Broad).
  One word more keeps them: **PUBLIC**, in the section of forks, because the owner asked for it
  (14 October 2026). A fork of a public repository is public, and the capitals say so.
- A sentence is short, and it is the owner's voice or a plain fact. No selling.
- Mono is for data only. A sentence is never in mono.
- **Two languages, one page.** Two small pills on the cover name the languages, each in its
  own language; the pressed one is white. The Portuguese keeps the lower case and the short
  sentences. How a sentence is translated is in [`TRANSLATIONS.md`](TRANSLATIONS.md), not here.

## Shapes

- **無 (mu, "nothing") is the centre of the graph** (the owner, 14 October 2026), in kanji and
  drawn as the arc draws 名残: green, in a rounded square. A dashed muted line, labelled "no DOI",
  goes from it to each work of `site/data/works.tsv` that has no DOI; when a work gets one, its
  line goes away by itself.
- **Round.** Buttons, the nodes of the graph and the chips of an era are pills. A panel has a
  large radius. There is no sharp card.
- **A line, not a box.** A list is set apart by a rule or by a light on its left edge, not by a
  card with a shadow.
- **Dashed means not his, or not yet.** A friend's work, a private work, a prophecy.
- **One-line drawings**, in picasso's manner: a few lines and curves, a broken frame, round
  caps, no fill. Each is drawn here, is a file in `site/static/drawings/`, and is used as a mask
  so that it takes a light. Never trace a drawing by Pablo Picasso.

## The favicon

A dark square with three small one-line drawings, one for each light that the name stands on: a
green flame (the knowledge that Prometheus carries), an orange boat, and the blue sea under
both. The boat is orange because the owner asked for it; it is the one place where orange is
not Ouroboric.

## Logos

- A logo is its owner's. It is never a file here, never recoloured and never given a glow.
- It sits on a white chip with round corners, so that it keeps its own colours on the dark
  page.
- A logo that its owner drew in light colours, for a dark ground, sits on a dark chip with a
  rule around it, and is larger (`mark: wide`). It is still not recoloured. LIOC's is the one.
- Where an owner's page cannot be loaded by a secure page, the logo loads from the Internet
  Archive's copy of the owner's own file, at a fixed date. Where there is no such copy, the
  row has no logo and shows a plain mark. Do not draw a look-alike.

## Motion

None that starts by itself. Two things answer the reader:

- A press on a colour lights its works and dims the rest, at once.
- The arc runs sideways while the reader scrolls down (the owner, 14 October 2026, after
  sheets.works' "holding up the internet"). Its stage stays on the screen, a pixel down is a pixel
  sideways, the reader's mark is lit, the others are dimmed, and so is the name of its era. It
  stops when the reader stops. With no JavaScript, or with reduced motion, the arc is a list.

## Facts

The look serves the facts and not the other way.

- Every fact on the page comes from `README.md`, `me/` or a table of `site/data/`, and every row
  of a table says where it was read ([`AGENTS.md`](AGENTS.md), hard rule 3).
- A number is read from a metrics card at build. It is never typed in.
- What has not happened is marked as such: a dashed mark and the word "prophecy".

## A phone

- One column. The arc runs sideways as on a wide screen, one mark at a time; as a list (no
  JavaScript, or reduced motion), its marks go to the left edge. The graph keeps its shape and
  its labels grow.
- No sideways scroll of the page. A word that is too long breaks.

## The CV

The short CV in English (`pdf/cv.pdf`, from `cv/summary.md`) is a page of the site on paper: the
same ground, the same four lights with the same meanings, the same three faces.

- **One page.** It is a summary for somebody who has a minute. What does not fit goes to the
  long form and to the site, and the page links to both.
- **The name is green and the epithet is blue**, as on the cover. A work has a light on its
  left edge, the light of its topic in `site/data/works.tsv`.
- **A link is the words with a line under them**, never a colour: a light is for meaning. Every
  place, work, DOI and way of working that the page names is a link.
- **The foot is a tip, in small muted words:** the links are checked on each pull request and
  each merge to `main`, and the commit that the PDF was built from, as a link.
- **No glow, no gradient, no logo.** Paper does not glow, and a logo is never a file here.
- The long CVs in three languages keep the older, light look of `cv/preamble.tex`.

## Before a change to the look

1. `just site`, then open `site/dist/index.html` at 1280 px and at 500 px wide.
2. Check each light against this page: is the thing really water, knowledge, Ouroboric or
   closed source?
3. Check the keyboard: Tab reaches every link and button, and the ring is visible on the dark
   ground.
4. Make the pictures of `site/preview/` again, for the pull request.

## Sources

Written for this repository.

- The manner (lower case, one-line drawings, few things, nothing that moves by itself) is
  h0ffmann/picasso's README and site.
- "Spend the boldness in one place", "structure is information" and "motion only as an answer
  to the reader's action" are read from Anthropic's `frontend-design` skill (Apache-2.0).
- The meaning of the four colours is the owner's: "ideas are in green, water related topics are
  in blue, and ouroboric ideas in yellow. Closed source ideas in red", and "Ouroboric ideas,
  water intuition, green knowledge". Later the same day he asked for "the ouroboric orange", so
  the Ouroboric light is orange and there is no yellow on the page.
