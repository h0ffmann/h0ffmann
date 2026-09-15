#!/usr/bin/env bash
# Build pdf/cv.pdf from README.md with labs/publisher's toolchain (run by mkPdf in the sandbox,
# or from `nix develop` locally). OUT_DIR is where mkPdf collects PDFs; defaults to ./pdf.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
out="${OUT_DIR:-$here/pdf}"
tmp="${TMPDIR:-/tmp}"
mkdir -p "$out"
python3 -m unittest discover -s "$here/cv"
python3 "$here/cv/prepare.py" "$here/README.md" "$here/cv/header.md" > "$tmp/cv.md"
# the QR goes into the header as a PDF (raw \includegraphics; pandoc only converts SVG in image nodes)
rsvg-convert -f pdf -o "$tmp/marola-qr.pdf" "$here/marola-qr.svg"
printf '\\graphicspath{{%s/}}\n' "$tmp" > "$tmp/paths.tex"
pandoc "$tmp/cv.md" --from markdown+raw_html+emoji --to pdf --pdf-engine=lualatex \
  --lua-filter "$PUBLISHER_FILTERS/shields-badges.lua" -H "$here/cv/preamble.tex" -H "$tmp/paths.tex" \
  --resource-path="$here" -V documentclass=article -V fontsize=10pt \
  -o "$out/cv.pdf"
echo "cv: $out/cv.pdf ($(pdfinfo "$out/cv.pdf" | awk '/^Pages/ {print $2}') pages)"
