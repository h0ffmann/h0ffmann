#!/usr/bin/env python3
"""Turn README.md into the markdown the CV PDF is built from.

    python3 cv/prepare.py README.md cv/header.md > cv.md

1. Everything between `<!-- cv:skip -->` and `<!-- cv:end -->` is removed (whole lines);
   an unmatched or nested marker is an error.
2. Everything between `<!-- cv:bottom -->` and `<!-- cv:end -->` moves to the end of the CV
   (the profile keeps it where it is) and its first heading goes up one level.
3. The floated QR line is removed (the CV header carries the QR instead).
4. Markdown images with remote sources are removed (no network in the sandbox).
5. The header file goes first.
Everything else passes through byte-for-byte; the shields badges are handled later by
labs/publisher's filter and the emoji by cv/emoji.lua.
"""
import re
import sys
from pathlib import Path

START, BOTTOM, END = "<!-- cv:skip -->", "<!-- cv:bottom -->", "<!-- cv:end -->"
QR_TAG = re.compile(r'<a href="(?P<href>https://marola\.dev)"[^>]*><img src="(?P<src>marola-qr\.svg)"[^>]*/></a>\n')
HEADING = re.compile(r"^#(#+ )")


def scan(text: str):
    """(marker the line sits in or None, is the line a marker, line) for every line; blocks
    do not nest, and both kinds close with the same END."""
    inside = None
    for n, line in enumerate(text.splitlines(keepends=True), 1):
        stripped = line.strip()
        if stripped in (START, BOTTOM):
            if inside:
                raise ValueError(f"line {n}: {stripped} inside {inside}")
            inside = stripped
            yield inside, True, line
        elif stripped == END:
            if not inside:
                raise ValueError(f"line {n}: {END} without {START} or {BOTTOM}")
            yield inside, True, line
            inside = None
        else:
            yield inside, False, line
    if inside:
        raise ValueError(f"{inside} without {END}")


def strip_skipped(text: str) -> str:
    return "".join(line for inside, _, line in scan(text) if inside != START)


def move_bottom(text: str) -> str:
    """BOTTOM blocks go after everything else, in order, each after a blank line. On the profile
    such a block sits under another section (marola under "me"); at the end of the CV it stands
    alone, so its first heading moves up one level."""
    body, blocks = [], []
    for inside, marker, line in scan(text):
        if inside != BOTTOM:
            body.append(line)
        elif marker and line.strip() == BOTTOM:
            blocks.append([])
        elif not marker:
            blocks[-1].append(line)
    for block in blocks:
        for i, line in enumerate(block):
            if HEADING.match(line):
                block[i] = HEADING.sub(r"\1", line, count=1)
                break
    return "".join(body) + "".join("\n" + "".join(block) for block in blocks)


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
    body = unremote_images(drop_qr(move_bottom(strip_skipped(readme))))
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
