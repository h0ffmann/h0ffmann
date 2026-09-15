#!/usr/bin/env bash
# Build pdf/cv.pdf, pdf/cv.pt-BR.pdf and pdf/cv.ja.pdf from README.md, README.pt-BR.md and README.ja.md with
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

# build <readme> <header> <output> <lang> <pdftitle> <footer> [extra preamble lines]
build() {
  local readme="$1" header="$2" output="$3" lang="$4" title="$5" footer="$6" extra="${7:-}"
  python3 "$here/cv/prepare.py" "$here/$readme" "$here/cv/$header" > "$tmp/$output.md"
  {
    printf '\\usepackage{graphicx}\\graphicspath{{%s/}}\n' "$tmp"
    printf '\\newcommand{\\cvtitle}{%s}\n' "$title"
    printf '\\newcommand{\\cvfooter}{%s}\n' "$footer"
    printf '%s\n' "$extra"
  } > "$tmp/$output.vars.tex"
  pandoc "$tmp/$output.md" --from markdown+raw_html+emoji --to pdf --pdf-engine=lualatex \
    --lua-filter "$PUBLISHER_FILTERS/shields-badges.lua" -H "$tmp/$output.vars.tex" -H "$here/cv/preamble.tex" \
    --resource-path="$here" -V documentclass=article -V fontsize=10pt -V "lang=$lang" \
    -o "$out/$output"
  echo "cv: $out/$output ($(pdfinfo "$out/$output" | awk '/^Pages/ {print $2}') pages)"
}

build README.md       header.md       cv.pdf       en-US "Matheus Hoffmann — CV" \
  "generated from \\href{https://github.com/h0ffmann/h0ffmann}{github.com/h0ffmann} — the README is the source"
build README.pt-BR.md header.pt-BR.md cv.pt-BR.pdf pt-BR "Matheus Hoffmann — Currículo" \
  "gerado a partir de \\href{https://github.com/h0ffmann/h0ffmann}{github.com/h0ffmann} — o README é a fonte"
# Japanese: luatexja for CJK line breaking, Harano Aji Gothic from publisher's TeX tree
build README.ja.md    header.ja.md    cv.ja.pdf    ja    "Matheus Hoffmann — 履歴書" \
  "\\href{https://github.com/h0ffmann/h0ffmann}{github.com/h0ffmann} から生成 — README が原本です" \
  '\usepackage{luatexja-fontspec}\setmainjfont{HaranoAjiGothic-Regular.otf}[BoldFont=HaranoAjiGothic-Bold.otf,Scale=0.92]\setsansjfont{HaranoAjiGothic-Regular.otf}[BoldFont=HaranoAjiGothic-Bold.otf,Scale=0.92]\ltjdefcharrange{9}{"1F1E6-"1F1FF,"2600-"27BF}\ltjsetparameter{jacharrange={-9}}'
