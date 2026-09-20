#!/usr/bin/env python3
"""Turn README.md into the markdown the CV PDF is built from.

    python3 cv/prepare.py README.md cv/header.md > cv.md

1. Everything between `<!-- cv:skip -->` and `<!-- cv:end -->` is removed (whole lines);
   an unmatched or nested marker is an error.
2. The floated QR line is removed (the CV header carries the QR instead).
3. Markdown images with remote sources are removed (no network in the sandbox).
4. The header file goes first.
Everything else passes through byte-for-byte; the shields badges are handled later by
labs/publisher's filter and the emoji by cv/emoji.lua.
"""
import re
import sys
from pathlib import Path

START, END = "<!-- cv:skip -->", "<!-- cv:end -->"
QR_TAG = re.compile(r'<a href="(?P<href>https://marola\.dev)"[^>]*><img src="(?P<src>marola-qr\.svg)"[^>]*/></a>\n')


def strip_skipped(text: str) -> str:
    out, skipping = [], False
    for n, line in enumerate(text.splitlines(keepends=True), 1):
        stripped = line.strip()
        if stripped == START:
            if skipping:
                raise ValueError(f"line {n}: nested {START}")
            skipping = True
        elif stripped == END:
            if not skipping:
                raise ValueError(f"line {n}: {END} without {START}")
            skipping = False
        elif not skipping:
            out.append(line)
    if skipping:
        raise ValueError(f"{START} without {END}")
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
