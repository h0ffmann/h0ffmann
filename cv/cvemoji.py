#!/usr/bin/env python3
"""Vector artwork for the emoji in the CV.

    python3 cv/cvemoji.py --fetch     # download what the three READMEs use and cv/emoji/ lacks
    python3 cv/cvemoji.py --list      # the emoji the CVs use, with their file names

lualatex can only draw Noto Color Emoji as 136 px bitmaps, and only for characters the text font
lacks (DejaVu Sans has its own black-and-white ⚡ ☁ ❄). So cv/emoji.lua replaces every emoji
with the matching SVG from cv/emoji/, which cv/build.sh converts to PDF: sharp at any zoom.
The SVGs are Noto Emoji's (googlefonts/noto-emoji, Apache-2.0), vendored because the build
sandbox has no network; file names are upstream's (`emoji_u1f30a.svg`, no fe0f).
cv/emoji.lua finds emoji by the same rules as `sequences` here — change both together.
"""
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
NOTO = "https://raw.githubusercontent.com/googlefonts/noto-emoji/v2.051/svg/{name}.svg"

BASE = "☀-➿⬀-⯿\U0001F000-\U0001F1E5\U0001F200-\U0001F3FA\U0001F400-\U0001FAFF"
FLAG = "[\U0001F1E6-\U0001F1FF]{2}"
MODIFIER = "[️\U0001F3FB-\U0001F3FF]"
SEQUENCE = re.compile(f"(?:{FLAG}|[{BASE}]{MODIFIER}*(?:‍[{BASE}]{MODIFIER}*)*)")


def sequences(text: str) -> list:
    """Every emoji in `text`, in order, badge URLs (percent-encoded) included."""
    return SEQUENCE.findall(urllib.parse.unquote(text))


def name(sequence: str) -> str:
    return "emoji_u" + "_".join(f"{ord(c):x}" for c in sequence if c != "️")


def used() -> list:
    import prepare
    root, found = HERE.parent, []
    for suffix in ("", ".pt-BR", ".ja"):
        text = prepare.prepare((root / f"README{suffix}.md").read_text(), (HERE / f"header{suffix}.md").read_text())
        found += sequences(text)
    return list(dict.fromkeys(found))


def main(argv) -> int:
    if argv[1:] not in (["--fetch"], ["--list"]):
        print(__doc__, file=sys.stderr)
        return 2
    for sequence in used():
        target = HERE / "emoji" / f"{name(sequence)}.svg"
        if argv[1] == "--list":
            print(sequence, target.name, "" if target.exists() else "(missing)")
        elif not target.exists():
            with urllib.request.urlopen(NOTO.format(name=name(sequence))) as response:
                target.write_bytes(response.read())
            print(f"fetched {target.relative_to(HERE.parent)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
