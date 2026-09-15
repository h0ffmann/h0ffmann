# CV PDF from the profile README via labs/publisher — design

**Date:** 2026-09-15
**Repos:** h0ffmann/nix-config (`labs/publisher`) and h0ffmann/h0ffmann (profile)
**Status:** approved in chat, awaiting written-spec review

## Goal

Build `pdf/cv.pdf` from `README.md` with the sandboxed toolchain in
`labs/publisher`, keeping the page's colors: every shields.io badge becomes a
colored pill with the badge's own hex color, headings keep their emoji in
color, links and section titles use marola blue. The PDF is committed to the
profile repo by CI whenever the README or the CV sources change, and linked
from the README.

## Non-goals

- No Portuguese PDF (README.pt-BR.md only receives the same markers/badge).
- No photo in the PDF.
- No network at build time: badges are not fetched, they are re-typeset.
- No logos inside the pills.
- No change to any existing publisher output shape (`lib.*.mkPdf`, `tex`,
  `python`, `tools`, `packages.*`, the action's inputs).

## Part 1 — labs/publisher (nix-config)

Everything added is generic "markdown with GitHub-style badges → PDF"
support; nothing knows about the profile.

### 1.1 `filters/shields-badges.lua`

A pandoc Lua filter. Input: any document read with `markdown+raw_html`.

- `RawInline`/`RawBlock` of format `html` are scanned for
  `<img ... src="https://img.shields.io/badge/<path>?...">` tags, optionally
  wrapped in `<a href="URL" ...>…</a>`.
- `<path>` is `label-message-color` or `message-color`. Decoding: `--` → `-`,
  `__` → `_`, `_` → space, then percent-decoding. `color` is a hex string
  (`0077BE`) or one of shields' named colors (`brightgreen`, `green`,
  `yellowgreen`, `yellow`, `orange`, `red`, `blue`, `lightgrey`, `grey`,
  `gray`, `success`, `important`, `critical`, `informational`, `inactive`),
  mapped to hex; unknown names fall back to `9F9F9F`.
- Each badge becomes the inline raw LaTeX `\badge{label}{message}{HEX}`,
  wrapped in `\href{URL}{…}` when an `<a>` surrounded it. LaTeX specials in
  label/message (`& % $ # _ { } ~ ^ \`) are escaped.
- A `RawBlock` (a `<p …>…</p>` group) becomes a `Para` of the badges it
  contains, separated by spaces, so pills flow and wrap like the web page.
- HTML `<img>` tags that are not shields badges are left as they were (pandoc
  drops raw HTML in LaTeX output); one warning per dropped image on stderr.
- Non-`html` raw content is untouched. The filter is a no-op for `-t html`.

### 1.2 `tex/publisher-badges.sty`

```latex
\RequirePackage{tikz}\RequirePackage{xcolor}
% \badge{label}{message}{HEX}: a rounded pill; label in a darker left part
% when non-empty, message on the colored part, white bold text.
\newcommand{\badge}[3]{…tikz node(s), baseline aligned, \footnotesize\bfseries…}
```

Label part: `HTML 555555` (shields' default label grey). Message part: `#3`.
Empty label → single pill.

### 1.3 `flake.nix`

- `toolsFor` gains `pkgs.librsvg` (so pandoc's LaTeX writer can convert SVG
  images via `rsvg-convert`) and the font package `pkgs.noto-fonts-color-emoji`.
- A shared `envFor = pkgs: { PUBLISHER_FILTERS = "${self}/filters"; TEXINPUTS = "${self}/tex//:"; OSFONTDIR = "${pkgs.noto-fonts-color-emoji}/share/fonts"; }`
  is exported by `mkPdf` (as derivation env) and by the devShell
  (`shellHook` exports), so local `just` runs and sandbox builds agree.
- `lib.<system>.env` exposes that attrset for consumers that call pandoc
  themselves.
- `example/smoke.md` gains a heading with an emoji and a line with two
  shields badges (one with `<a>`); `example/build.sh` adds a lualatex run with
  `--lua-filter "$PUBLISHER_FILTERS/shields-badges.lua"` and
  `-H` a 6-line preamble that `\usepackage{publisher-badges}` and sets the
  emoji fallback. `checks.smoke` therefore fails if the filter, the style or
  the font wiring breaks.
- A `checks.filters` derivation runs `pandoc -t latex --lua-filter …` on a
  fixture markdown and greps for the expected `\badge{Scala}{}{DC322F}` and
  `\href{https://marola.dev}{\badge{}{marola.dev}{0077BE}}`.

### 1.4 Docs

`labs/publisher/README.md`: a "Badges and emoji" subsection (filter, style,
the three env variables, the lualatex fallback recipe). Root `README.md`
publisher table: pandoc row unchanged, add "badges filter, color emoji".
`AGENTS.md` lab table: publisher "Is" column extended. `lab.json`: summary
unchanged, `headline` gains `librsvg`.

Commit shape: `feat(publisher): shields badges filter, badge style, color
emoji and svg support`, with `Tested:` trailer per AGENTS.md.

## Part 2 — profile repo (h0ffmann/h0ffmann)

### 2.1 README markers and badge

- `<!-- cv:skip -->` … `<!-- cv:end -->` around: the top language-switch
  line (which also holds the new CV badge), the whole `## 📊 stats` section
  (both cards, the activity markers), and the closing `<p align="center">`
  photo. The nix labs table stays.
- The switch line becomes
  `<p align="right"><a href="pdf/cv.pdf">📄 cv (pdf)</a> · <a href="README.pt-BR.md">🇧🇷 português</a></p>`.
- `README.pt-BR.md` gets identical markers and the badge (`📄 cv (pdf)`,
  pointing to the same English PDF).

### 2.2 `cv/`

- `header.md`:
  ```markdown
  # Matheus Hoffmann
  <p align="left">
  <a href="mailto:mhoffmannfs@gmail.com"><img src="https://img.shields.io/badge/email-mhoffmannfs%40gmail.com-0077BE?style=flat-square" /></a>
  <a href="https://www.linkedin.com/in/mhoffmannbr/"><img src="https://img.shields.io/badge/LinkedIn-mhoffmannbr-0A66C2?style=flat-square" /></a>
  <a href="https://github.com/h0ffmann"><img src="https://img.shields.io/badge/GitHub-h0ffmann-181717?style=flat-square" /></a>
  <a href="https://marola.dev"><img src="https://img.shields.io/badge/%F0%9F%8C%8A-marola.dev-0077BE?style=flat-square" /></a>
  </p>
  ```
  (same badge syntax as the README, so the one filter renders everything).
- `prepare.py` (stdlib): `prepare(readme_text, header_text) -> str`:
  1. remove every `<!-- cv:skip -->`…`<!-- cv:end -->` span (multi-line);
     raise `ValueError` on an unmatched or nested marker;
  2. rewrite the QR tag `<a href="https://marola.dev" …><img src="marola-qr.svg" … width="120" /></a>`
     into `[![](marola-qr.svg){width=28mm}](https://marola.dev)` placed
     right after the marola heading (pandoc + rsvg embed it);
  3. demote nothing: the README's `##` become `\section`, `###` `\subsection`;
     the header's `#` becomes the title (`\section*`-styled by the preamble);
  4. return `header + "\n\n" + body`.
  CLI: `python3 cv/prepare.py README.md cv/header.md > out.md`.
- `test_prepare.py` (unittest): skip removal incl. multi-line, unmatched
  marker raises, nested raises, QR rewrite, header first, untouched text
  passes through byte-identical, idempotent on already-prepared input.
- `preamble.tex`: `geometry` a4paper 16mm margins; `fontspec` DejaVu Sans
  10pt with `luaotfload.add_fallback("emoji", {"Noto Color Emoji:mode=harf;"})`;
  `\definecolor{marola}{HTML}{0077BE}`; `titlesec` colored section rules;
  `hyperref` colorlinks in marola; `enumitem` tight lists; blockquote as a
  left marola bar; `\usepackage{publisher-badges}`; `fancyhdr` footer
  "github.com/h0ffmann · built YYYY-MM-DD" (date from `SOURCE_DATE_EPOCH`
  or the build day); no page numbers on a one-pager, numbers from page 2.
- `build.sh`:
  ```bash
  set -euo pipefail
  python3 -m unittest discover -s cv
  python3 cv/prepare.py README.md cv/header.md > "$TMPDIR/cv.md"
  pandoc "$TMPDIR/cv.md" --from markdown+raw_html+emoji --to pdf \
    --pdf-engine=lualatex --lua-filter "$PUBLISHER_FILTERS/shields-badges.lua" \
    -H cv/preamble.tex --resource-path=. -V documentclass=article -V fontsize=10pt \
    -o "$OUT_DIR/cv.pdf"
  ```

### 2.3 `flake.nix`

```nix
inputs.publisher.url = "github:h0ffmann/nix-config?dir=labs/publisher";
outputs = { self, publisher, ... }: let systems = [ "x86_64-linux" "aarch64-linux" "aarch64-darwin" ]; … in {
  packages.<s>.default = publisher.lib.<s>.mkPdf { name = "cv"; src = ./.; command = "bash cv/build.sh"; };
  checks.<s>.cv = self.packages.<s>.default;
  devShells.<s>.default = pkgs.mkShell { packages = publisher.lib.<s>.tools; shellHook = exports of publisher.lib.<s>.env; };
}
```

`src = ./.` means the whole repo (README, cv/, marola-qr.svg). `flake.lock`
is committed. `.gitignore` gains `result`.

### 2.4 `.github/workflows/cv.yml`

```yaml
on:
  push: { branches: [main], paths: [README.md, cv/**, flake.nix, flake.lock, .github/workflows/cv.yml] }
  workflow_dispatch:
permissions: { contents: write }
concurrency: { group: cv, cancel-in-progress: false }
jobs:
  cv:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: h0ffmann/nix-config/labs/publisher@main
        with:
          pdf-dir: pdf
          artifact-name: cv
          commit: "true"
          commit-message: "Update cv.pdf - [Skip GitHub Action]"
```

Bot pushes use the Actions token and never trigger it; only hand edits do.

### 2.5 Docs

AGENTS.md: a "CV PDF" bullet (what builds it, the marker rule, that
`flake.lock` pins publisher and is bumped with `nix flake update publisher`,
`nix build` locally, `pdf/cv.pdf` is generated). The nix-labs spec's
"no flake in this repo" reasoning is superseded; a line there says so.

## Error handling

| Failure | Behaviour |
| --- | --- |
| Unmatched / nested cv markers | `prepare.py` raises; build fails |
| Non-shields `<img>` in README | dropped with a warning; build succeeds |
| Unknown shields color name | grey pill `9F9F9F` |
| Emoji font missing (`OSFONTDIR` unset) | lualatex prints tofu; `checks.smoke` in publisher catches it via `pdffonts` grep for `NotoColorEmoji` |
| publisher input changes shape | `nix flake check` in the profile fails before the action commits anything |

## Testing

- publisher: `nix flake check` (smoke with badges + emoji + lualatex, filters
  fixture check), plus the existing lint gate.
- profile: `python3 -m unittest discover -s cv`; `nix build` locally; page 1
  rasterized with `pdftoppm` and inspected (pills colored, emoji in color,
  QR present, no tofu); `pdffonts` shows `NotoColorEmoji` embedded.
- After merge: one `workflow_dispatch` run of `cv.yml`, `pdf/cv.pdf` committed.

## Sequencing

1. nix-config PR (Part 1), CI green, merged.
2. Profile PR (Part 2) with `flake.lock` pinned to that merge commit.

## Files touched

nix-config: `labs/publisher/{flake.nix,filters/shields-badges.lua,tex/publisher-badges.sty,example/smoke.md,example/build.sh,README.md,lab.json}`, root `README.md`, `AGENTS.md`.

profile: `flake.nix`, `flake.lock`, `cv/{header.md,prepare.py,test_prepare.py,preamble.tex,build.sh}`, `.github/workflows/cv.yml`, `README.md`, `README.pt-BR.md`, `AGENTS.md`, `.gitignore`, this spec, one line in the nix-labs spec.
