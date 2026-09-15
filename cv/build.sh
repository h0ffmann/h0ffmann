#!/usr/bin/env bash
# Build pdf/cv.pdf (from README.md) and pdf/cv.pt-BR.pdf (from README.pt-BR.md) with
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

# build <readme> <header> <output> <lang> <pdftitle> <footer>
build() {
  local readme="$1" header="$2" output="$3" lang="$4" title="$5" footer="$6"
  python3 "$here/cv/prepare.py" "$here/$readme" "$here/cv/$header" > "$tmp/$output.md"
  {
    printf '\\usepackage{graphicx}\\graphicspath{{%s/}}\n' "$tmp"
    printf '\\newcommand{\\cvtitle}{%s}\n' "$title"
    printf '\\newcommand{\\cvfooter}{%s}\n' "$footer"
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
