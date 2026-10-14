#!/usr/bin/env python3
"""The translations of the site are whole, current and marked (TRANSLATIONS.md).

    python3 scripts/translations-check.py              # what `just check` runs
    python3 scripts/translations-check.py --self-test  # a bad table must be refused

For each site/data/translations/<lang>.tsv:
1. every row has its seven cells; `how` and `status` are known words; an `adapted` row says why;
2. no source is there twice;
3. no row is an orphan: its source is still a sentence of the page (a string of the page's code,
   a cell of site/data/*.tsv, or the README's paragraph). When the English changes, the old row
   fails here, so a translation can never stay beside a sentence it no longer translates;
4. no false friend of false-friends.tsv is in a translation;
5. the coverage is counted and printed. It is a measure, not a gate.

What this cannot tell: that a translation is right, or that it reads well. That is the `status`
column, and only a native reader moves a row from `draft` to `reviewed`.
"""
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOW, STATUS = {"plain", "adapted", "kept"}, {"draft", "reviewed"}


def rows(path: Path) -> list:
    return [l.split("\t") for l in path.read_text().split("\n") if l and not l.startswith("#")]


def page_strings(root: Path) -> set:
    """Every string the page can show: its code's literals, the tables' cells, the README's paragraphs."""
    app = (root / "site/src/h0ffmann_site/app.gleam").read_text()
    found = {m.replace('\\"', '"') for m in re.findall(r'"((?:[^"\\]|\\.)*)"', app)}
    for tsv in sorted((root / "site/data").glob("*.tsv")):
        for row in rows(tsv):
            found.update(row)
    readme = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", (root / "README.md").read_text())
    found.update(l.replace("**", "").replace("`", "").strip() for l in readme.split("\n") if l.strip())
    return found


def shown(root: Path) -> set:
    """The sentences that the page's code writes itself: the ones a translation is owed for."""
    app = (root / "site/src/h0ffmann_site/app.gleam").read_text()
    lits = {m.replace('\\"', '"') for m in re.findall(r'tx\(\s*"((?:[^"\\]|\\.)*)"', app)}
    for name, cols in (("timeline", (4, 5)), ("works", (9,))):
        for row in rows(root / f"site/data/{name}.tsv"):
            lits.update(row[c] for c in cols if c < len(row) and row[c])
    return {l for l in lits if re.search(r"[a-z]{3}", l)}


def check(root: Path) -> list:
    errors, strings = [], page_strings(root)
    friends = rows(root / "site/data/translations/false-friends.tsv")
    for table in sorted((root / "site/data/translations").glob("*.tsv")):
        if table.name == "false-friends.tsv":
            continue
        lang, seen = table.stem, set()
        for row in rows(table):
            where = f"{table.name}: {row[0][:50]!r}"
            if len(row) != 7:
                errors.append(f"{where}: {len(row)} cells, and a row has 7"); continue
            source, target, how, note, status, by, date = row
            if how not in HOW: errors.append(f"{where}: how is {how!r}")
            if status not in STATUS: errors.append(f"{where}: status is {status!r}")
            if how == "adapted" and not note.strip(): errors.append(f"{where}: adapted, and the note does not say why")
            if not target.strip() or not by.strip() or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
                errors.append(f"{where}: no translation, no translator or no date")
            if source in seen: errors.append(f"{where}: the source is there twice")
            seen.add(source)
            if source not in strings and source.strip() not in strings:
                errors.append(f"{where}: an orphan: the page has no such sentence now. Translate the new sentence and delete this row")
            for english, wrong, right, *_ in friends:
                if re.search(rf"\b{re.escape(english)}", source, re.I) and re.search(rf"\b{re.escape(wrong)}\b", target, re.I):
                    errors.append(f"{where}: false friend: {english!r} is {right!r} here, not {wrong!r}")
        owed = shown(root)
        done = len(owed & seen)
        drafts = sum(1 for r in rows(table) if len(r) == 7 and r[4] == "draft")
        print(f"translations: {lang}: {len(seen)} rows; {done} of {len(owed)} sentences of the page's own text have one; "
              f"{drafts} rows are drafts that no native reader has reviewed", file=sys.stderr)
        for missing in sorted(owed - seen)[:8]:
            print(f"translations: {lang}: not translated yet: {missing[:70]!r}", file=sys.stderr)
    return errors


def self_test() -> int:
    """The judge is judged: a table with one fault of each kind must be refused for each."""
    import shutil
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        for rel in ("site/src/h0ffmann_site/app.gleam", "README.md"):
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(ROOT / rel, root / rel)
        shutil.copytree(ROOT / "site/data", root / "site/data")
        bad = root / "site/data/translations/pt-BR.tsv"
        bad.write_text("# source\tpt-BR\thow\tnote\tstatus\tby\tdate\n"
                       "the arc\ta trajetória\tadapted\t\tdraft\tx\t2026-10-14\n"
                       "the arc\to arco\tplain\t\tdraft\tx\t2026-10-14\n"
                       "a sentence the page does not have\tuma frase\tplain\t\tdraft\tx\t2026-10-14\n"
                       "the works\tos trabalhos\tguessed\t\tdone\tx\t2026-10-14\n"
                       "its record names all six\to recorde nomeia os seis\tplain\t\tdraft\tx\t2026-10-14\n"
                       "three cells\tonly\n")
        found = " | ".join(check(root))
    for fault in ("does not say why", "there twice", "an orphan", "how is 'guessed'", "status is 'done'", "false friend", "cells"):
        if fault not in found:
            print(f"translations: self-test: a bad table passed: {fault}", file=sys.stderr)
            return 1
    print("translations: self-test ok: the check refused a bad table for each of seven faults", file=sys.stderr)
    return 0


def main(argv) -> int:
    if "--self-test" in argv:
        return self_test()
    errors = check(ROOT)
    for e in errors:
        print(f"translations: {e}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
