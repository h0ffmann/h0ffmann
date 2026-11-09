#!/usr/bin/env python3
"""site/data/repos.tsv and site/data/topics.tsv: every public source repository of the owner's
accounts, and the GitHub topics they use most.

    python3 scripts/repos.py                    # read GitHub again (needs `gh`, signed in), write both tables
    python3 scripts/repos.py --archify OUT.json # also write the topic cloud as Archify's input
    python3 scripts/repos.py --forks [--forks-archify OUT.json]  # the forks: forks.tsv, fork_topics.tsv
    python3 scripts/repos.py --self-test

The accounts are h0ffmann, marola-dev and piabrota (the owner, 9 November 2026). A repository is
read from GitHub's repository search (`user:<owner> fork:false is:public`), which gives its topics.
The `topic` column of repos.tsv (one of the four lights, DESIGN.md) is set by hand: a row keeps the
one it had, and a new repository gets the light of its account (NEW) until the owner changes it.
topics.tsv counts, over every repository of repos.tsv, how many carry each topic.

The forks (`fork:only`) are read the same way. A fork rarely carries topics of its own, so
fork_topics.tsv counts the topics of each fork's parent. GitHub's search does not give a fork's
parent: a parent already in forks.tsv is kept, and a new one is the repository of the same name,
not a fork, whose description is the fork's (or, when none is, the one with the most stars). The
`parent_read` column says which.
"""
import time
import collections
import datetime
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPOS = ROOT / "site/data/repos.tsv"
TOPICS = ROOT / "site/data/topics.tsv"
FORKS = ROOT / "site/data/forks.tsv"
FORK_TOPICS = ROOT / "site/data/fork_topics.tsv"
OWNERS = ["h0ffmann", "marola-dev", "piabrota"]
NEW = {"h0ffmann": "ideas", "marola-dev": "water", "piabrota": "ideas"}
KEEP = 30
CLOUD = 24


def search(q: str, paginate: bool = True) -> list[dict]:
    # GitHub's search API allows 30 queries a minute.
    time.sleep(2.1)
    out = subprocess.run(
        ["gh", "api", "-X", "GET", "search/repositories", "-f", f"q={q}", "-f", "per_page=100"]
        + (["--paginate"] if paginate else []) + ["--jq", ".items[]"],
        capture_output=True, text=True)
    if out.returncode:
        # A `repo:` qualifier for a repository that was renamed, made private or deleted is refused (422).
        if "repo:" in q:
            return []
        raise RuntimeError(f"search {q!r}: {out.stderr.strip()}")
    return [json.loads(line) for line in out.stdout.splitlines() if line.strip()]


def read_github(kind: str = "fork:false") -> list[dict]:
    return [r for owner in OWNERS for r in search(f"user:{owner} {kind} is:public")]


def old_parents() -> dict[tuple[str, str], tuple[str, str]]:
    keep = {}
    if FORKS.exists():
        header = [l for l in FORKS.read_text().splitlines() if l.startswith("# ")][-1][2:].split("\t")
        for line in FORKS.read_text().splitlines():
            if line and not line.startswith("#"):
                c = dict(zip(header, line.split("\t")))
                key = (c.get("owner", "h0ffmann"), c["name"])
                keep[key] = (c["parent"], c.get("parent_read", "gh repo list h0ffmann --fork, 14 October 2026"))
    return keep


def pick_parent(fork: dict, found: list[dict]) -> tuple[dict | None, str]:
    same = [r for r in found if r["name"].lower() == fork["name"].lower() and r["full_name"] != fork["full_name"]]
    desc = clean(fork.get("description"))
    if desc:
        match = [r for r in same if clean(r.get("description")) == desc]
        if match:
            return max(match, key=lambda r: r["stargazers_count"]), "search: same name and description"
    # He forks his own accounts' work too (h0ffmann/room from piabrota/room): one of them comes first.
    own = [r for r in same if r["owner"]["login"] in OWNERS]
    if own:
        return own[0], "search: same name, one of his accounts"
    if same:
        return max(same, key=lambda r: r["stargazers_count"]), "search: same name, most stars"
    return None, ""


def find_parent(fork: dict, known: tuple[str, str] | None, own: list[dict]) -> tuple[dict | None, str]:
    # His own accounts' repositories are few and rarely starred, so a name search can miss them:
    # they are tried first, from the list read once (h0ffmann/room is a fork of piabrota/room).
    parent, how = pick_parent(fork, own)
    if parent:
        return parent, how
    if known:
        found = search(f"repo:{known[0]}", paginate=False)
        if found:
            return found[0], known[1]
    for kind in ("fork:false", "fork:true"):
        parent, how = pick_parent(fork, search(f"{fork['name']} in:name {kind}", paginate=False))
        if parent:
            return parent, how
    return None, ""


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


# Topics that say the same thing count as one (the owner, 9 November 2026: "reduce redundant
# topics like awesome, and awesome-*"). A repository counts once for the merged topic.
ALIASES = {
    "rust-lang": "rust",
    "second-brain": "2nd-brain",
    "zettelkasten-method": "zettelkasten",
    "zettelkasten-methodology": "zettelkasten",
    "nix-flake": "nix",
    "nix-flakes": "nix",
    "nix-lang": "nix",
    "nix-language": "nix",
    "nixos": "nix",
    "nix-os": "nix",
    "claude-code-plugin": "claude-code",
    "claude-code-skill": "claude-code",
    "claude-code-skills": "claude-code",
    "claude-skills": "claude-code",
    "neuro-symbolic": "neurosymbolic-ai",
    "neuro-symbolic-ai": "neurosymbolic-ai",
    "ocean-science": "ocean-sciences",
    "llms": "llm",
}


def merge(topic: str) -> str:
    return "awesome" if topic.startswith("awesome") else ALIASES.get(topic, topic)


def topic_rows(repos: list[dict]) -> list[list[str]]:
    seen = collections.defaultdict(list)
    for r in sorted(repos, key=lambda r: (r["owner"]["login"], r["name"])):
        for t in sorted({merge(t) for t in r.get("topics") or []}):
            seen[t].append(f'{r["owner"]["login"]}/{r["name"]}')
    top = sorted(seen.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:KEEP]
    return [[t, str(len(names)), ", ".join(names)] for t, names in top]


def cloud(topics: list[list[str]], lights: dict[str, str] | None, title: str, subtitle: str,
          cards: list[dict], unit: str = "repo") -> dict:
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
        # A fork is somebody else's work and has no light: it is neutral.
        light = (collections.Counter(lights[x] for x in names.split(", ")).most_common(1)[0][0]
                 if lights else "none")
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
    kind = {"water": "frontend", "ideas": "backend", "ouroboric": "cloud", "closed": "security",
            "none": "external"}
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
                "sublabel": f"{n} {unit}s" if n > 1 else f"1 {unit}",
                "pos": [round(x), round(y + (rowh - h) / 2)], "size": [w, h],
            })
            x += w + 14
        y += rowh + 16
    return {
        "schema_version": 1,
        "diagram_type": "architecture",
        "meta": {
            "title": title,
            "subtitle": subtitle,
            "output": "topics.html",
            "quality_profile": "showcase",
            "viewBox": [1060, y + 30],
            "legend": {"mode": "hidden"},
        },
        "components": comps,
        "cards": cards,
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
        "# most used topics, the most used first. Topics that say the same thing are merged (awesome-*, rust-lang: ALIASES in",
        "# scripts/repos.py). A number here is read, never typed.",
        "# topic\tcount\trepos",
    ] + ["\t".join(r) for r in topics]) + "\n")
    print(f"repos: {len(repos)} repositories ({dict(counts)}), {tagged} with topics; wrote {REPOS.name}, {TOPICS.name}")
    if archify:
        archify.parent.mkdir(parents=True, exist_ok=True)
        lights = {f"{r[0]}/{r[1]}": r[2] for r in rows}
        cards = [
            {"dot": "cyan", "title": "the size", "items": [
                "a bigger word: more repositories carry the topic",
                f"the {min(CLOUD, len(topics))} most used topics of site/data/topics.tsv"]},
            {"dot": "emerald", "title": "the colour", "items": [
                "the light of most of the repositories that carry it: blue water, green ideas",
                "orange ouroboric, red closed source (site/data/repos.tsv)"]},
        ]
        # The two titles are the owner's (9 November 2026).
        c = cloud(topics, lights, "h0ffmann - how I fork, how I play",
                  f"direct interests: the GitHub topics of my {len(repos)} public repositories (h0ffmann, marola-dev, piabrota), {tagged} with topics, read on {day}",
                  cards)
        archify.write_text(json.dumps(c, indent=1) + "\n")
        print(f"repos: wrote {archify}")


def write_forks(archify: Path | None) -> None:
    day = datetime.datetime.now(datetime.timezone.utc).strftime("%-d %B %Y")
    known = old_parents()
    own = read_github()
    forks = read_github("fork:only")
    rows, parents, lost = [], [], []
    for f in sorted(forks, key=lambda f: (f["created_at"], f["full_name"]), reverse=True):
        owner = f["owner"]["login"]
        parent, how = find_parent(f, known.get((owner, f["name"])), own)
        if not parent:
            lost.append(f["full_name"])
            continue
        parents.append({**parent, "owner": {"login": owner}, "name": f["name"]})
        rows.append([owner, f["name"], parent["full_name"], parent["created_at"][:4], f["created_at"][:10],
                     clean(f.get("description")), f["html_url"], how])
    counts = collections.Counter(r[0] for r in rows)
    FORKS.write_text("\n".join([
        f"# Every public fork of h0ffmann, marola-dev and piabrota, as GitHub listed them on {day} (GitHub's repository",
        "# search, `user:<owner> fork:only is:public`; made by scripts/repos.py): "
        + ", ".join(f"{counts[o]} of {o}" for o in OWNERS) + ". Each one is PUBLIC, because GitHub keeps",
        "# a fork of a public repository public. forked: the day the fork was made. started: the year its parent was created on",
        "# GitHub, the closest record of when that project began. parent: the repository it was forked from; parent_read: how the",
        "# parent was found (scripts/repos.py). The description is the fork's own, which GitHub usually copies from its parent.",
        "# owner\tname\tparent\tstarted\tforked\tdescription\thref\tparent_read",
    ] + ["\t".join(r) for r in rows]) + "\n")
    topics = topic_rows(parents)
    tagged = sum(1 for p in parents if p.get("topics"))
    FORK_TOPICS.write_text("\n".join([
        f"# The GitHub topics of the parents of the {len(rows)} forks of site/data/forks.tsv, as GitHub gave them on {day}: {tagged}",
        "# parents carry at least one topic. A fork rarely has topics of its own, so its parent's stand for it. count: how many",
        f"# forks carry the topic; forks: which. Made by scripts/repos.py --forks; the {KEEP} most used, the most used first;",
        "# topics that say the same thing are merged (ALIASES in scripts/repos.py).",
        "# topic\tcount\tforks",
    ] + ["\t".join(r) for r in topics]) + "\n")
    print(f"forks: {len(rows)} forks ({dict(counts)}), {tagged} parents with topics; wrote {FORKS.name}, {FORK_TOPICS.name}")
    for name in lost:
        print(f"forks: no parent found for {name}; it is left out", file=sys.stderr)
    for r in rows:
        if r[7].startswith("search: same name, most stars"):
            print(f"forks: {r[0]}/{r[1]}: parent {r[2]} by name only", file=sys.stderr)
    if archify:
        archify.parent.mkdir(parents=True, exist_ok=True)
        cards = [
            {"dot": "cyan", "title": "the size", "items": [
                "a bigger word: more of his forks come from a repository with the topic",
                f"the {min(CLOUD, len(topics))} most used topics of site/data/fork_topics.tsv"]},
            {"dot": "slate", "title": "the colour", "items": [
                "none: a fork is somebody else's work, so it takes no light (DESIGN.md)"]},
        ]
        c = cloud(topics, None, "h0ffmann - indirect interests",
                  f"the GitHub topics of the repositories behind my {len(rows)} public forks (h0ffmann, marola-dev, piabrota), {tagged} with topics, read on {day}",
                  cards, unit="fork")
        archify.write_text(json.dumps(c, indent=1) + "\n")
        print(f"forks: wrote {archify}")


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
    assert merge("awesome-list") == "awesome" and merge("rust-lang") == "rust"
    tops = topic_rows(fake)
    assert tops[0] == ["nix", "2", "h0ffmann/a, piabrota/b"], tops
    c = cloud(tops, {"h0ffmann/a": "water", "piabrota/b": "ideas"}, "t", "s", [])
    size = {x["label"]: x["size"][1] for x in c["components"]}
    assert size["nix"] > size["rust"], size
    fork = {"name": "x", "full_name": "h0ffmann/x", "description": "the x"}
    found = [
        {"name": "x", "full_name": "big/x", "description": "other", "stargazers_count": 90, "owner": {"login": "big"}},
        {"name": "x", "full_name": "real/x", "description": "the x", "stargazers_count": 3, "owner": {"login": "real"}},
        {"name": "x", "full_name": "h0ffmann/x", "description": "the x", "stargazers_count": 0, "owner": {"login": "h0ffmann"}},
    ]
    assert pick_parent(fork, found)[0]["full_name"] == "real/x"
    assert pick_parent({**fork, "description": None}, found)[0]["full_name"] == "big/x"
    assert pick_parent({**fork, "name": "y"}, found) == (None, "")
    mine = found + [{"name": "x", "full_name": "piabrota/x", "description": "", "stargazers_count": 1, "owner": {"login": "piabrota"}}]
    assert pick_parent({**fork, "description": None}, mine)[0]["full_name"] == "piabrota/x"
    print("repos: self-test passed")
    return 0


def main(argv: list[str]) -> int:
    if argv[:1] == ["--self-test"]:
        return self_test()
    if "--forks" in argv:
        out = Path(argv[argv.index("--forks-archify") + 1]) if "--forks-archify" in argv else None
        write_forks(out)
        return 0
    archify = Path(argv[argv.index("--archify") + 1]) if "--archify" in argv else None
    write(read_github(), archify)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
