#!/usr/bin/env python3
"""LINKEDIN_PROJECTS.md from FEATURED_REPO.md: one text for each repository, sized for LinkedIn.

    python3 scripts/linkedin-projects.py           # write LINKEDIN_PROJECTS.md
    python3 scripts/linkedin-projects.py --check   # the file is the one FEATURED_REPO.md makes

The rule is DERIVATION.md, "REPO to PROJECT". Nothing is fetched here: every fact of a text is a
cell of FEATURED_REPO.md, so a text can say nothing that the table does not. A text over a limit
fails the build: cut the repository's description at its source, never here.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC, OUT = ROOT / "FEATURED_REPO.md", ROOT / "LINKEDIN_PROJECTS.md"
ME = "h0ffmann"
# The sizes of LinkedIn's "Projects" form. They were not read from LinkedIn in the session that
# wrote this (its pages need a sign-in): check them in the form, and change them here.
NAME_MAX, TEXT_MAX = 255, 2000
# The size this repository asks for: a text that is read in one look.
TEXT_GOAL = 420
AREAS = {"water": "wave modelling and the sea", "ideas": "game theory and tools", "ouroboric": "self-improving apps", "closed": "licences and closed source"}
ROW = re.compile(r"^\| \[(?P<repo>[^\]]+)\]\((?P<url>[^)]+)\) \| (?P<area>\w+) \| (?P<desc>.*?) \| (?P<commits>\d+) \| (?P<mine>\d+) \| "
                 r"\[`(?P<sha>[0-9a-f]{7})`\]\([^)]+\) \| (?P<licence>.*?) \| (?P<doi>.*?) \| (?P<with_>.*?) \|$")


def lower(text: str) -> str:
    """Lower case, as the profile is written; a word with two capitals or more is an acronym and stays."""
    def word(m):
        w = m.group(0)
        return w if sum(c.isupper() for c in w) >= 2 else w.lower()
    return re.sub(r"[^\s]+", word, text)


def read() -> tuple:
    text = SRC.read_text()
    day = re.search(r"read from GitHub on\s+\*\*(.+?)\*\*", text)
    return (day.group(1) if day else ""), [m.groupdict() for m in map(ROW.match, text.splitlines()) if m]


def project(r: dict, day: str) -> tuple:
    owner, name = r["repo"].split("/")
    title = name if owner == ME else f"{name} ({owner})"
    desc = "" if r["desc"] == "—" else lower(r["desc"]).rstrip(".") + ". "
    doi = re.search(r"\[([^\]]+)\]", r["doi"])
    parts = [
        desc + f"research area: {AREAS[r['area']]}.",
        f"{r['commits']} commits, {r['mine']} by {ME}; reviewed at commit {r['sha']} on {day.lower()}.",
        (f"with {lower(r['with_'])}. " if r["with_"] != "—" else "") + f"licence: {r['licence'] if r['licence'].isupper() or '-' in r['licence'] else lower(r['licence'])}."
        + (f" doi: {doi.group(1)}." if doi else ""),
        f"github.com/{r['repo']}",
    ]
    return title, "\n".join(parts)


def build() -> str:
    day, rows = read()
    out = [f"""# LinkedIn projects

One text for each repository of [`FEATURED_REPO.md`](FEATURED_REPO.md), for the "Projects" section
of the LinkedIn profile of `{ME}`. Made by `just linkedin`, by the rule "REPO to PROJECT" of
[`DERIVATION.md`](DERIVATION.md); do not edit it by hand. Each text is in lower case and gives
the repository's own description, its research area, its commits, the commit it was reviewed at,
its licence and its DOI. The numbers are those of FEATURED_REPO.md, read on **{day}**.

Sizes: a name of at most {NAME_MAX} characters and a text of at most {TEXT_MAX} are what the build
allows; {TEXT_GOAL} is what it asks for. The two limits were **not read from LinkedIn** when this
was written: check them in the form.

Paste the first block into "Project name" and the second into "Description". The link goes into
the form's own link field.
"""]
    bad = 0
    for r in rows:
        title, text = project(r, day)
        note = "" if len(text) <= TEXT_GOAL else f", over the goal of {TEXT_GOAL}"
        if len(title) > NAME_MAX or len(text) > TEXT_MAX:
            print(f"linkedin: {r['repo']}: name {len(title)}, text {len(text)}: over the limit", file=sys.stderr)
            bad = 1
        out.append(f"## {r['repo']}\n\nName, {len(title)} characters:\n\n```text\n{title}\n```\n\n"
                   f"Description, {len(text)} characters{note}:\n\n```text\n{text}\n```\n\nLink: <{r['url']}>\n")
    if bad or not rows:
        raise SystemExit("linkedin: no row was read from FEATURED_REPO.md" if not rows else 1)
    return "\n".join(out)


def main(argv) -> int:
    text = build()
    if "--check" in argv:
        if not OUT.is_file() or OUT.read_text() != text:
            print("linkedin: LINKEDIN_PROJECTS.md is not the one FEATURED_REPO.md makes; run `just linkedin`", file=sys.stderr)
            return 1
        print(f"linkedin: LINKEDIN_PROJECTS.md is current ({text.count(chr(10) + '## ')} projects)", file=sys.stderr)
        return 0
    OUT.write_text(text)
    print(f"linkedin: wrote {OUT.name} ({text.count(chr(10) + '## ')} projects)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
