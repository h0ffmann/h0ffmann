#!/usr/bin/env python3
"""citation: .zenodo.json is the one citation file edited by hand; CITATION.cff is made from it.

    python3 scripts/citation.py            # validate .zenodo.json, write CITATION.cff
    python3 scripts/citation.py --check    # validate; exit 1 if CITATION.cff is stale
    python3 scripts/citation.py --self-test

Zenodo reads only .zenodo.json. GitHub's "Cite this repository" reads only CITATION.cff. So the
second is generated from the first, and CI fails when they differ.

Three rules come from a release that went wrong (journal/, "the record came out open"):
  - `license` must be there. With none, Zenodo takes the licence that GitHub shows for the
    default branch.
  - `version`, `publication_date` and `doi` must not be there: Zenodo sets them.
  - an ORCID must pass its checksum.

The idea is the citation tool of marola-dev/marola, h0ffmann/picasso and h0ffmann/closed-source.
This file is written for this repository and is much smaller.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORBIDDEN = ("version", "publication_date", "doi", "prereserve_doi")
REQUIRED = ("title", "upload_type", "description", "creators", "license", "access_right", "keywords")


def orcid_ok(orcid: str) -> bool:
    if not re.fullmatch(r"\d{4}-\d{4}-\d{4}-\d{3}[\dX]", orcid):
        return False
    digits = orcid.replace("-", "")
    total = 0
    for c in digits[:-1]:
        total = (total + int(c)) * 2
    check = (12 - total % 11) % 11
    return digits[-1] == ("X" if check == 10 else str(check))


def errors(meta: dict) -> list:
    out = [f"missing {k}" for k in REQUIRED if not meta.get(k)]
    out += [f"{k} is set by Zenodo; remove it" for k in FORBIDDEN if k in meta]
    for i, c in enumerate(meta.get("creators", [])):
        if not re.fullmatch(r"[^,]+, [^,]+", c.get("name", "")):
            out.append(f"creators[{i}]: name is not 'Family, Given'")
        if "orcid" in c and not orcid_ok(c["orcid"]):
            out.append(f"creators[{i}]: the ORCID does not pass its checksum")
    for i, r in enumerate(meta.get("related_identifiers", [])):
        if not r.get("identifier") or not r.get("relation"):
            out.append(f"related_identifiers[{i}]: needs an identifier and a relation")
    return out


def quote(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def cff(meta: dict, doi: str) -> str:
    lines = [
        "# Generated from .zenodo.json by scripts/citation.py; edit that file, then `just citation`.",
        "cff-version: 1.2.0",
        'message: "All rights reserved. Read it and cite it; do not copy it. See REUSE.md."',
        "type: generic",
        "title: " + quote(meta["title"]),
        "authors:",
    ]
    for c in meta["creators"]:
        family, given = [p.strip() for p in c["name"].split(",", 1)]
        lines += ["  - family-names: " + quote(family), "    given-names: " + quote(given)]
        if "orcid" in c:
            lines.append('    orcid: "https://orcid.org/' + c["orcid"] + '"')
        if c.get("affiliation"):
            lines.append("    affiliation: " + quote(c["affiliation"]))
    lines.append('repository-code: "https://github.com/h0ffmann/h0ffmann"')
    lines.append('url: "https://h0ffmann.github.io/h0ffmann/"')
    if doi:
        lines.append("doi: " + doi)
    lines.append("keywords:")
    lines += ["  - " + quote(k) for k in meta["keywords"]]
    return "\n".join(lines) + "\n"


def own_doi() -> str:
    """The repository's own DOI, from site/data/self.tsv; empty before the first release."""
    path = ROOT / "site/data/self.tsv"
    if not path.exists():
        return ""
    for line in path.read_text().splitlines():
        cells = line.split("\t")
        if len(cells) == 2 and cells[0] == "doi":
            return cells[1]
    return ""


def self_test() -> int:
    good = {
        "title": "t", "upload_type": "other", "description": "d", "license": "other-closed",
        "access_right": "closed", "keywords": ["k"],
        "creators": [{"name": "Hoffmann, Matheus", "orcid": "0009-0009-1056-7661"}],
    }
    assert errors(good) == [], errors(good)
    bad = dict(good, version="v1", creators=[{"name": "Matheus Hoffmann", "orcid": "0000-0000-0000-0000"}])
    del bad["license"]
    got = errors(bad)
    assert "missing license" in got and "version is set by Zenodo; remove it" in got, got
    assert any("Family, Given" in e for e in got) and any("checksum" in e for e in got), got
    text = cff(good, "10.5281/zenodo.1")
    assert 'family-names: "Hoffmann"' in text and "doi: 10.5281/zenodo.1" in text, text
    assert orcid_ok("0000-0002-1825-0097") and not orcid_ok("0000-0002-1825-0098")
    print("citation: self-test ok", file=sys.stderr)
    return 0


def main(argv: list) -> int:
    if "--self-test" in argv:
        return self_test()
    meta = json.loads((ROOT / ".zenodo.json").read_text())
    found = errors(meta)
    if found:
        for e in found:
            print("citation: .zenodo.json: " + e, file=sys.stderr)
        return 1
    text = cff(meta, own_doi())
    target = ROOT / "CITATION.cff"
    if "--check" in argv:
        if not target.exists() or target.read_text() != text:
            print("citation: CITATION.cff is stale; run `just citation`", file=sys.stderr)
            return 1
        print("citation: .zenodo.json valid, CITATION.cff current", file=sys.stderr)
        return 0
    target.write_text(text)
    print("citation: wrote CITATION.cff", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
