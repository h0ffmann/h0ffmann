#!/usr/bin/env bash
# Build pdf/cv.pdf from cv/summary.md, and pdf/cv.full.pdf, pdf/cv.pt-BR.pdf and pdf/cv.ja.pdf from README.md, README.pt-BR.md and README.ja.md, with
# labs/publisher's toolchain — run by mkPdf in the sandbox, or from `nix develop` locally.
# OUT_DIR is where mkPdf collects PDFs; defaults to ./pdf.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
out="${OUT_DIR:-$here/pdf}"
tmp="${TMPDIR:-/tmp}"
mkdir -p "$out"
python3 -m unittest discover -s "$here/cv"
# the QR goes into the header as a PDF (raw \includegraphics; pandoc only converts SVG in image nodes)
rsvg-convert -f pdf -o "$tmp/marola-qr.pdf" "$here/marola-qr.svg"
# emoji are drawn from vector artwork, not from a font (cv/cvemoji.py, cv/emoji.lua)
mkdir -p "$tmp/emoji"
for svg in "$here"/cv/emoji/*.svg; do
  rsvg-convert -f pdf -o "$tmp/emoji/$(basename "$svg" .svg).pdf" "$svg"
done

# build <readme> <header> <output> <lang> <pdftitle> <footer> [extra preamble lines]
build() {
  local readme="$1" header="$2" output="$3" lang="$4" title="$5" footer="$6" extra="${7:-}"
  python3 "$here/cv/prepare.py" "$here/$readme" "$here/cv/$header" > "$tmp/$output.md"
  {
    printf '\\usepackage{graphicx}\\graphicspath{{%s/}{%s/emoji/}}\n' "$tmp" "$tmp"
    printf '\\newcommand{\\cvtitle}{%s}\n' "$title"
    printf '\\newcommand{\\cvfooter}{%s}\n' "$footer"
    printf '%s\n' "$extra"
  } > "$tmp/$output.vars.tex"
  pandoc "$tmp/$output.md" --from markdown+raw_html+emoji --to pdf --pdf-engine=lualatex \
    --lua-filter "$here/cv/links.lua" --lua-filter "$PUBLISHER_FILTERS/shields-badges.lua" --lua-filter "$here/cv/emoji.lua" -H "$tmp/$output.vars.tex" -H "$here/cv/preamble.tex" \
    --resource-path="$here" -V documentclass=article -V fontsize=10pt -V "lang=$lang" \
    -o "$out/$output"
  echo "cv: $out/$output ($(pdfinfo "$out/$output" | awk '/^Pages/ {print $2}') pages)"
}

# The short CV in English: cv/summary.md, in the look of the site (cv/site.tex, cv/site.lua,
# DESIGN.md). The faces are the site's three, from the flake (CV_FONTS, CV_MONO); a variable
# font's file has brackets in its name, so each is copied to a plain name. CV_COMMIT is the
# commit the flake was built from: empty when the tree has changes that are not committed.
mkdir -p "$tmp/fonts"
cp "$CV_FONTS/Newsreader[opsz,wght].ttf" "$tmp/fonts/Newsreader.ttf"
cp "$CV_FONTS/Newsreader-Italic[opsz,wght].ttf" "$tmp/fonts/Newsreader-Italic.ttf"
cp "$CV_FONTS/BricolageGrotesque[opsz,wdth,wght].ttf" "$tmp/fonts/Bricolage.ttf"
cp "$(find "$CV_MONO" -name 'JetBrainsMono-Regular.ttf' | head -1)" "$tmp/fonts/JetBrainsMono-Regular.ttf"
{
  printf '\\newcommand{\\cvtitle}{Matheus Hoffmann — CV}\n'
  printf '\\newcommand{\\cvfonts}{%s/fonts}\n' "$tmp"
} > "$tmp/cv.vars.tex"
pandoc "$here/cv/summary.md" --from markdown --to pdf --pdf-engine=lualatex \
  --lua-filter "$here/cv/site.lua" -H "$tmp/cv.vars.tex" -H "$here/cv/site.tex" \
  -V documentclass=article -V fontsize=10pt -V lang=en-US -o "$out/cv.pdf"
echo "cv: $out/cv.pdf ($(pdfinfo "$out/cv.pdf" | awk '/^Pages/ {print $2}') pages)"
# The short CV is one page (DESIGN.md, "The CV"). A second page is a fault of the summary.
[ "$(pdfinfo "$out/cv.pdf" | awk '/^Pages/ {print $2}')" = 1 ] || { echo "cv: the short CV must be one page; shorten cv/summary.md" >&2; exit 1; }

# The long CVs: each README, in the look of cv/preamble.tex.
build README.md       header.md       cv.full.pdf  en-US "Matheus Hoffmann — CV, the long form" \
  "generated from \\href{https://github.com/h0ffmann/h0ffmann}{github.com/h0ffmann} — the README is the source"
build README.pt-BR.md header.pt-BR.md cv.pt-BR.pdf pt-BR "Matheus Hoffmann — Currículo" \
  "gerado a partir de \\href{https://github.com/h0ffmann/h0ffmann}{github.com/h0ffmann} — o README é a fonte"
# Japanese: luatexja for CJK line breaking, Harano Aji Gothic from publisher's TeX tree
build README.ja.md    header.ja.md    cv.ja.pdf    ja    "Matheus Hoffmann — 履歴書" \
  "\\href{https://github.com/h0ffmann/h0ffmann}{github.com/h0ffmann} から生成 — README が原本です" \
  '\usepackage{luatexja-fontspec}\setmainjfont{HaranoAjiGothic-Regular.otf}[BoldFont=HaranoAjiGothic-Bold.otf,Scale=0.92]\setsansjfont{HaranoAjiGothic-Regular.otf}[BoldFont=HaranoAjiGothic-Bold.otf,Scale=0.92]\ltjdefcharrange{9}{"1F1E6-"1F1FF,"2600-"27BF}\ltjsetparameter{jacharrange={-9}}'

# en.OCEAN: a formal English CV (two pages at most) and a one-page presentation letter for an
# ocean-research audience, written by hand in cv/*.en.OCEAN.md (not from a README), with the
# letterhead cv/header.en.OCEAN.md and the look of cv/preamble.tex. The letter is set larger and
# with wider margins than the CV: \AtBeginDocument runs after the preamble, so it overrides it.
build cv/cv.en.OCEAN.md     header.en.OCEAN.md cv.en.OCEAN.pdf     en-US "Matheus Hoffmann — Curriculum Vitae" \
  "Matheus Hoffmann — curriculum vitae — \\href{https://github.com/h0ffmann/h0ffmann}{github.com/h0ffmann}" \
  '\AtBeginDocument{\newgeometry{margin=16mm,top=12mm,bottom=14mm}\setmainfont{DejaVu Sans}[Scale=0.92]\setlength{\parskip}{3pt}}'
build cv/letter.en.OCEAN.md header.en.OCEAN.md letter.en.OCEAN.pdf en-US "Matheus Hoffmann — Presentation letter" \
  "Matheus Hoffmann — presentation letter" \
  '\AtBeginDocument{\newgeometry{margin=22mm,top=16mm,bottom=18mm}\setmainfont{DejaVu Sans}[Scale=1.0]\setlength{\parskip}{8pt}}'
# pt-BR.OCEAN: the same formal CV in Portuguese, written by hand in cv/cv.pt-BR.OCEAN.md, with its
# own research section (ww3-gpu only) and the letterhead cv/header.pt-BR.OCEAN.md.
build cv/cv.pt-BR.OCEAN.md  header.pt-BR.OCEAN.md cv.pt-BR.OCEAN.pdf  pt-BR "Matheus Hoffmann — Currículo" \
  "Matheus Hoffmann — currículo — \\href{https://github.com/h0ffmann/h0ffmann}{github.com/h0ffmann}" \
  '\AtBeginDocument{\newgeometry{margin=16mm,top=12mm,bottom=14mm}\setmainfont{DejaVu Sans}[Scale=0.92]\setlength{\parskip}{3pt}}'
pages="$(pdfinfo "$out/cv.en.OCEAN.pdf" | awk '/^Pages/ {print $2}')"
[ "$pages" -le 2 ] || { echo "cv: cv.en.OCEAN.pdf must be two pages at most; shorten cv/cv.en.OCEAN.md" >&2; exit 1; }
[ "$(pdfinfo "$out/letter.en.OCEAN.pdf" | awk '/^Pages/ {print $2}')" = 1 ] || { echo "cv: letter.en.OCEAN.pdf must be one page; shorten cv/letter.en.OCEAN.md" >&2; exit 1; }
[ "$(pdfinfo "$out/cv.pt-BR.OCEAN.pdf" | awk '/^Pages/ {print $2}')" -le 2 ] || { echo "cv: cv.pt-BR.OCEAN.pdf must be two pages at most; shorten cv/cv.pt-BR.OCEAN.md" >&2; exit 1; }
