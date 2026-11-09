#!/usr/bin/env python3
"""site/data/repos.tsv and site/data/topics.tsv: every public source repository of the owner's
accounts, and the GitHub topics they use most.

    python3 scripts/repos.py                    # read GitHub again (needs `gh`, signed in), write both tables
    python3 scripts/repos.py --archify OUT.json # also write the topic cloud as Archify's input
    python3 scripts/repos.py --self-test

The accounts are h0ffmann, marola-dev and piabrota (the owner, 9 November 2026). A repository is
read from GitHub's repository search (`user:<owner> fork:false is:public`), which gives its topics.
The `topic` column of repos.tsv (one of the four lights, DESIGN.md) is set by hand: a row keeps the
one it had, and a new repository gets the light of its account (NEW) until the owner changes it.
topics.tsv counts, over every repository of repos.tsv, how many carry each topic.
"""
import collections
import datetime
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPOS = ROOT / "site/data/repos.tsv"
TOPICS = ROOT / "site/data/topics.tsv"
OWNERS = ["h0ffmann", "marola-dev", "piabrota"]
NEW = {"h0ffmann": "ideas", "marola-dev": "water", "piabrota": "ideas"}
KEEP = 30
CLOUD = 24


def read_github() -> list[dict]:
    repos = []
    for owner in OWNERS:
        out = subprocess.run(
            ["gh", "api", "-X", "GET", "search/repositories", "-f",
             f"q=user:{owner} fork:false is:public", "-f", "per_page=100", "--paginate",
             "--jq", ".items[]"],
            check=True, capture_output=True, text=True).stdout
        repos += [json.loads(line) for line in out.splitlines() if line.strip()]
    return repos


def old_topics() -> dict[tuple[str, str], str]:
    keep = {}
    if REPOS.exists():
        for line in REPOS.read_text().splitlines():
            if line and not line.startswith("#"):
                c = line.split("\t")
                keep[(c[0], c[1])] = c[2]
    return keep


def clean(text: str) -> str:
    return " ".join((text or "").replace("\t", " ").split())


def repo_rows(repos: list[dict], keep: dict) -> list[list[str]]:
    rows = []
    for r in sorted(repos, key=lambda r: (r["pushed_at"], r["created_at"]), reverse=True):
        owner, name = r["owner"]["login"], r["name"]
        rows.append([owner, name, keep.get((owner, name), NEW[owner]), r["pushed_at"][:4],
                     clean(r.get("description")), r["html_url"]])
    return rows


def topic_rows(repos: list[dict]) -> list[list[str]]:
    seen = collections.defaultdict(list)
    for r in sorted(repos, key=lambda r: (r["owner"]["login"], r["name"])):
        for t in sorted(set(r.get("topics") or [])):
            seen[t].append(f'{r["owner"]["login"]}/{r["name"]}')
    top = sorted(seen.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:KEEP]
    return [[t, str(len(names)), ", ".join(names)] for t, names in top]


def cloud(topics: list[list[str]], lights: dict[str, str], day: str, total: int, tagged: int) -> dict:
    """The topic cloud as Archify's architecture input: one box per topic, its size by its count.

    Archify's type is one size; the frame (scripts/topics-frame.py) sets each word's size from its
    box, so the most used topic is the biggest word. The boxes are packed in rows, the most used in
    the middle row, and each row centred.
    """
    rows = topics[:CLOUD]
    top = int(rows[0][1])
    words = []
    for t, n, names in rows:
        n = int(n)
        h = round(34 * (0.5 + 1.6 * n / top))
        # The frame sets the word at 0.42 of the box's height; a monospace letter is 0.6 of that.
        w = round(len(t) * 0.6 * 0.42 * h + 30)
        # The light of the topic (DESIGN.md, the four lights): the one most of its repositories have.
        light = collections.Counter(lights[x] for x in names.split(", ")).most_common(1)[0][0]
        words.append((t, n, w, h, light))
    width = 980
    lines, line, used = [], [], 0
    for wd in words:
        if line and used + wd[2] + 14 > width:
            lines.append(line)
            line, used = [], 0
        line.append(wd)
        used += wd[2] + 14
    lines.append(line)
    # The line of the most used topics goes in the middle; the others alternate above and below.
    order = []
    for i, ln in enumerate(lines):
        order.insert(0, ln) if i % 2 else order.append(ln)
    # Archify's kinds whose colours are nearest the four lights: blue, green, orange, red.
    kind = {"water": "frontend", "ideas": "backend", "ouroboric": "cloud", "closed": "security"}
    comps, y = [], 40
    for ln in order:
        rowh = max(wd[3] for wd in ln)
        x = 40 + (width - sum(wd[2] + 14 for wd in ln) + 14) / 2
        # Inside a line, the biggest word in the middle too.
        mid = []
        for i, wd in enumerate(ln):
            mid.insert(0, wd) if i % 2 else mid.append(wd)
        for t, n, w, h, light in mid:
            comps.append({
                "id": "t-" + "".join(ch if ch.isalnum() else "-" for ch in t),
                "type": kind[light], "label": t,
                "sublabel": f"{n} repos" if n > 1 else "1 repo",
                "pos": [round(x), round(y + (rowh - h) / 2)], "size": [w, h],
            })
            x += w + 14
        y += rowh + 16
    return {
        "schema_version": 1,
        "diagram_type": "architecture",
        "meta": {
            "title": "h0ffmann: the GitHub topics of his repositories",
            "subtitle": f"read from GitHub on {day}: {total} public source repositories of h0ffmann, marola-dev and piabrota, {tagged} with topics",
            "output": "topics.html",
            "quality_profile": "showcase",
            "viewBox": [1060, y + 30],
            "legend": {"mode": "hidden"},
        },
        "components": comps,
        "cards": [
            {"dot": "cyan", "title": "the size", "items": [
                "a bigger word: more repositories carry the topic",
                f"the {len(rows)} most used topics of site/data/topics.tsv"]},
            {"dot": "emerald", "title": "the colour", "items": [
                "the light of most of the repositories that carry it: blue water, green ideas",
                "orange ouroboric, red closed source (site/data/repos.tsv)"]},
        ],
    }


def write(repos: list[dict], archify: Path | None) -> None:
    day = datetime.datetime.now(datetime.timezone.utc).strftime("%-d %B %Y")
    rows = repo_rows(repos, old_topics())
    counts = collections.Counter(r[0] for r in rows)
    REPOS.write_text("\n".join([
        f"# Every public source repository of h0ffmann, marola-dev and piabrota (no forks), as GitHub listed them on {day}",
        "# (GitHub's repository search, `user:<owner> fork:false is:public`; made by scripts/repos.py): "
        + ", ".join(f"{counts[o]} of {o}" for o in OWNERS) + ".",
        "# year: the year of the last push. The description is the repository's own; empty when it has none.",
        "# topic: water | ideas | ouroboric | closed, set by hand (a new repository gets its account's until the owner sets it).",
        "# owner\tname\ttopic\tyear\tdescription\thref",
    ] + ["\t".join(r) for r in rows]) + "\n")
    topics = topic_rows(repos)
    tagged = sum(1 for r in repos if r.get("topics"))
    TOPICS.write_text("\n".join([
        f"# The GitHub topics of the {len(repos)} repositories of site/data/repos.tsv, as GitHub gave them on {day}: {tagged} of them",
        f"# carry at least one topic. count: how many of them carry the topic; repos: which. Made by scripts/repos.py; the {KEEP}",
        "# most used topics, the most used first. A number here is read, never typed.",
        "# topic\tcount\trepos",
    ] + ["\t".join(r) for r in topics]) + "\n")
    print(f"repos: {len(repos)} repositories ({dict(counts)}), {tagged} with topics; wrote {REPOS.name}, {TOPICS.name}")
    if archify:
        archify.parent.mkdir(parents=True, exist_ok=True)
        lights = {f"{r[0]}/{r[1]}": r[2] for r in rows}
        archify.write_text(json.dumps(cloud(topics, lights, day, len(repos), tagged), indent=1) + "\n")
        print(f"repos: wrote {archify}")


def self_test() -> int:
    fake = [
        {"owner": {"login": "h0ffmann"}, "name": "a", "pushed_at": "2026-01-01", "created_at": "2025-01-01",
         "description": "one\ttwo", "html_url": "https://github.com/h0ffmann/a", "topics": ["nix", "rust"]},
        {"owner": {"login": "piabrota"}, "name": "b", "pushed_at": "2026-02-01", "created_at": "2025-01-01",
         "description": None, "html_url": "https://github.com/piabrota/b", "topics": ["nix"]},
    ]
    rows = repo_rows(fake, {("h0ffmann", "a"): "water"})
    assert rows[0][:4] == ["piabrota", "b", "ideas", "2026"], rows
    assert rows[1][2] == "water" and rows[1][4] == "one two", rows
    tops = topic_rows(fake)
    assert tops[0] == ["nix", "2", "h0ffmann/a, piabrota/b"], tops
    c = cloud(tops, {"h0ffmann/a": "water", "piabrota/b": "ideas"}, "1 January 2026", 2, 2)
    size = {x["label"]: x["size"][1] for x in c["components"]}
    assert size["nix"] > size["rust"], size
    print("repos: self-test passed")
    return 0


def main(argv: list[str]) -> int:
    if argv[:1] == ["--self-test"]:
        return self_test()
    archify = Path(argv[argv.index("--archify") + 1]) if "--archify" in argv else None
    write(read_github(), archify)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
