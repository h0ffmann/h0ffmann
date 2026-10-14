#!/usr/bin/env python3
"""FEATURED_REPO.md from site/data/featured.tsv and GitHub, read today.

    python3 scripts/featured.py            # write FEATURED_REPO.md (needs `gh`, signed in)
    python3 scripts/featured.py --check    # the file has a row for each row of the list

The list is chosen by hand (site/data/featured.tsv). Every number is read from GitHub on the day
and the file says the day: a number is never typed in (DESIGN.md, "Facts"). For each repository:
its own description, its licence, the commits of its default branch, how many of them are the
owner's, and the commit it was reviewed at, which is the head of that branch when it was read.
"""
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIST, OUT, WORKS = ROOT / "site/data/featured.tsv", ROOT / "FEATURED_REPO.md", ROOT / "site/data/works.tsv"
ME = "h0ffmann"
OWNERS = ("h0ffmann", "marola-dev", "ouroboric-dev")
AREAS = {"water": "wave modelling and the sea", "ideas": "game theory and tools", "ouroboric": "self-improving apps", "closed": "licences and closed source"}


def rows(path: Path) -> list:
    return [l.split("\t") for l in path.read_text().splitlines() if l and not l.startswith("#")]


def gh(*args: str) -> str:
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


def commits(repo: str, branch: str, author: str = "") -> tuple:
    """(count, head sha): one request for one commit; the count is the last page of its Link header."""
    q = f"repos/{repo}/commits?per_page=1&sha={branch}" + (f"&author={author}" if author else "")
    out = gh("api", "-i", q)
    head, _, body = out.partition("\r\n\r\n") if "\r\n\r\n" in out else out.partition("\n\n")
    data = json.loads(body)
    if not data:
        return 0, ""
    last = re.search(r'[?&]page=(\d+)>; rel="last"', head)
    return (int(last.group(1)) if last else len(data)), data[0]["sha"]


def counts(owner: str) -> tuple:
    data = json.loads(gh("repo", "list", owner, "--limit", "1000", "--json", "isPrivate,isFork"))
    public = [r for r in data if not r["isPrivate"]]
    return len(data), len(public), len([r for r in public if not r["isFork"]])


def build() -> str:
    today = datetime.datetime.now(datetime.timezone.utc).strftime("%-d %B %Y")
    dois = {w[0]: w[4] for w in rows(WORKS) if len(w) > 4 and w[4]}
    lines = []
    for owner, name, area, with_, _source in rows(LIST):
        repo = f"{owner}/{name}"
        info = json.loads(gh("api", f"repos/{repo}"))
        total, sha = commits(repo, info["default_branch"])
        mine, _ = commits(repo, info["default_branch"], ME)
        licence = (info.get("license") or {}).get("spdx_id") or "none stated"
        licence = "see the repository" if licence == "NOASSERTION" else licence
        doi = dois.get(name, "")
        desc = (info.get("description") or "").strip().replace("|", "/") or "—"
        lines.append(f"| [{repo}](https://github.com/{repo}) | {area} | {desc} | {total} | {mine} | "
                     f"[`{sha[:7]}`](https://github.com/{repo}/commit/{sha}) | {licence} | "
                     f"{f'[{doi}](https://doi.org/{doi})' if doi else '—'} | {with_ or '—'} |")
    count_rows = []
    for owner in OWNERS:
        total, public, source = counts(owner)
        count_rows.append(f"| [{owner}](https://github.com/{owner}) | {total} | {public} | {source} |")
    areas = "\n".join(f"- **{k}**: {v}" for k, v in AREAS.items())
    return f"""# Featured repositories

The repositories that say what Matheus Hoffmann (`h0ffmann`) works on: his own, marola-dev's,
and ouroboric-dev's, which he makes with Bruno Valério. The list is chosen by hand in
[`site/data/featured.tsv`](site/data/featured.tsv). Every number below was read from GitHub on
**{today}** by `just featured`; none was typed in. All rights reserved, like the rest of this
repository ([`REUSE.md`](REUSE.md)); each repository has its own licence, in its own column.

## The counts

| Account | Repositories that this reading could see | Public | Public, not forks |
|---|---:|---:|---:|
{chr(10).join(count_rows)}

The first number is what the owner's own sign-in could see on that day, private ones too; for
an organisation it may leave out a private repository that the sign-in cannot see.

## The repositories

`commits` is the count of the default branch; `his` is how many of them GitHub gives to
`{ME}`; `reviewed at` is the head of that branch when it was read.

| Repository | Area | Description (the repository's own) | Commits | His | Reviewed at | Licence | DOI | With |
|---|---|---|---:|---:|---|---|---|---|
{chr(10).join(lines)}

## The areas

{areas}

The four areas are the four lights of [`DESIGN.md`](DESIGN.md).

## Derived from this file

[`LINKEDIN_PROJECTS.md`](LINKEDIN_PROJECTS.md): one text for each row, sized for the "Projects"
section of a LinkedIn profile. The rule is in [`DERIVATION.md`](DERIVATION.md).
"""


def main(argv) -> int:
    if "--check" in argv:
        text = OUT.read_text() if OUT.is_file() else ""
        missing = [f"{o}/{n}" for o, n, *_ in rows(LIST) if f"[{o}/{n}](" not in text]
        for m in missing:
            print(f"featured: {m} is in the list and not in FEATURED_REPO.md; run `just featured`", file=sys.stderr)
        if not missing:
            print(f"featured: {len(rows(LIST))} repositories of the list are in FEATURED_REPO.md", file=sys.stderr)
        return 1 if missing else 0
    OUT.write_text(build())
    print(f"featured: wrote {OUT.name}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
