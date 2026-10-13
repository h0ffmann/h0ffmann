#!/usr/bin/env python3
"""Turn README.md into the markdown the CV PDF is built from.

    python3 cv/prepare.py README.md cv/header.md > cv.md

1. Everything between `<!-- cv:skip -->` and `<!-- cv:end -->` is removed (whole lines).
2. Everything between a line `<!-- cv:only` and a line `cv:end -->` is kept and the two marker
   lines are dropped: on github.com that span is one HTML comment, so the profile hides it and
   only the CV shows it. The two kinds of block cannot nest; an unmatched marker is an error.
3. The floated QR line is removed (the CV header carries the QR instead).
4. Markdown images with remote sources are removed (no network in the sandbox).
5. The header file goes first.
Everything else passes through byte-for-byte; the shields badges are handled later by
labs/publisher's filter and the emoji by cv/emoji.lua.
"""
import re
import sys
from pathlib import Path

START, END = "<!-- cv:skip -->", "<!-- cv:end -->"
ONLY_START, ONLY_END = "<!-- cv:only", "cv:end -->"
MARKERS = (START, END, ONLY_START, ONLY_END)
QR_TAG = re.compile(r'<a href="(?P<href>https://marola\.dev)"[^>]*><img src="(?P<src>marola-qr\.svg)"[^>]*/></a>\n')


def markers(text: str) -> list:
    """The marker lines of a README, in order: the three READMEs must have the same list."""
    return [line.strip() for line in text.splitlines() if line.strip() in MARKERS]


def strip_skipped(text: str) -> str:
    """Drop the `cv:skip` blocks, unwrap the `cv:only` blocks, pass the rest through."""
    out, block = [], None  # block: None, "skip" or "only"
    for n, line in enumerate(text.splitlines(keepends=True), 1):
        stripped = line.strip()
        if stripped in (START, ONLY_START):
            if block:
                raise ValueError(f"line {n}: {stripped} inside a cv:{block} block")
            block = "skip" if stripped == START else "only"
        elif stripped in (END, ONLY_END):
            closes = "skip" if stripped == END else "only"
            if block != closes:
                raise ValueError(f"line {n}: {stripped} without its cv:{closes} start")
            block = None
        elif block != "skip":
            out.append(line)
    if block:
        raise ValueError(f"cv:{block} block never closed")
    return "".join(out)


def drop_qr(text: str) -> str:
    """The README floats the QR beside the marola section; the CV shows it in the header instead."""
    return QR_TAG.sub("", text)


LINKED_REMOTE_IMG = re.compile(r"\[!\[(?P<alt>[^\]]*)\]\((?P<img>https?://[^)\s]+)(?:\s+\"[^\"]*\")?\)\]\((?P<href>[^)]+)\)")
REMOTE_IMG = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<img>https?://[^)\s]+)(?:\s+\"[^\"]*\")?\)")


def unremote_images(text: str) -> str:
    """Markdown images with http(s) sources cannot be fetched in the sandbox and carry nothing on
    a CV (status badges); they are removed, linked or not. Local images are untouched."""
    return REMOTE_IMG.sub("", LINKED_REMOTE_IMG.sub("", text))


def prepare(readme: str, header: str) -> str:
    body = unremote_images(drop_qr(strip_skipped(readme)))
    return header + "\n" + body if header else body


def main(argv) -> int:
    if len(argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    readme, header = Path(argv[1]).read_text(), Path(argv[2]).read_text()
    try:
        sys.stdout.write(prepare(readme, header))
    except ValueError as error:
        print(f"error: {argv[1]}: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
