#!/usr/bin/env python3
"""site/data/stars.tsv: the topics of the repositories that h0ffmann starred, counted.

    python3 scripts/stars.py          # read GitHub again (needs `gh`, signed in) and write the table

GitHub gives each repository the topics its owner set. This counts, over every repository that
h0ffmann starred, how many carry each topic, and keeps the most common. A repository with no
topic counts in the total and in no topic. The day of the reading is written in the table.
"""
import collections
import datetime
import json
import subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "site/data/stars.tsv"
KEEP = 16


def main() -> int:
    pages = subprocess.run(["gh", "api", "users/h0ffmann/starred?per_page=100", "--paginate"],
                           check=True, capture_output=True, text=True).stdout
    repos = []
    for chunk in pages.replace("][", "]\n[").splitlines():
        if chunk.strip():
            repos += json.loads(chunk)
    topics = collections.Counter(t for r in repos for t in set(r.get("topics") or []))
    tagged = sum(1 for r in repos if r.get("topics"))
    day = datetime.datetime.now(datetime.timezone.utc).strftime("%-d %B %Y")
    head = [
        f"# The topics of the repositories that h0ffmann starred, as GitHub gave them on {day}: {len(repos)} stars, {tagged} of them on",
        "# a repository with at least one topic. count: how many starred repositories carry the topic. Made by scripts/stars.py;",
        f"# the {KEEP} most common topics, the most common first. A number here is read, never typed.",
        "# topic\tcount",
    ]
    rows = [f"{t}\t{n}" for t, n in sorted(topics.items(), key=lambda kv: (-kv[1], kv[0]))[:KEEP]]
    OUT.write_text("\n".join(head + rows) + "\n")
    print(f"stars: {len(repos)} stars, {tagged} with topics, {len(topics)} topics; wrote {OUT.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
