#!/usr/bin/env python3
"""The committed CVs are the ones their sources make.

    python3 scripts/cv-current.py <built dir> [<committed dir>]

For each PDF of the built directory, the words of the committed PDF of the same name must be the
same words (pdftotext). One thing may differ: the commit that the short CV names in its foot,
because a PDF cannot name the commit that it is committed in. The `cv` workflow builds the PDFs
again on main, with that commit. The same check as `just current` of marola-dev/marola-research.
"""
import re
import subprocess
import sys
from pathlib import Path

COMMIT = re.compile(r"\s*built\s+from\s+commit\s+[0-9a-f]{7}\.")


def words(pdf: Path) -> str:
    text = subprocess.run(["pdftotext", str(pdf), "-"], check=True, capture_output=True, text=True).stdout
    return " ".join(COMMIT.sub("", text).split())


def main(argv) -> int:
    built, committed = Path(argv[1]), Path(argv[2] if len(argv) > 2 else "pdf")
    pdfs = sorted(built.glob("*.pdf"))
    if not pdfs:
        print(f"current: no PDF in {built}", file=sys.stderr)
        return 1
    bad = 0
    for pdf in pdfs:
        mine = committed / pdf.name
        if not mine.is_file():
            print(f"current: {mine} is not committed; run `just cv` and commit it", file=sys.stderr)
            bad = 1
        elif words(mine) != words(pdf):
            print(f"current: {mine} was not made from these sources; run `just cv` and commit it", file=sys.stderr)
            bad = 1
    if not bad:
        print(f"current: {len(pdfs)} PDFs of {committed}/ are the ones their sources make", file=sys.stderr)
    return bad


if __name__ == "__main__":
    sys.exit(main(sys.argv))
