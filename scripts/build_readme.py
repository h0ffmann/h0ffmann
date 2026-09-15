#!/usr/bin/env python3
"""Rewrite the "nix labs" table in the profile README(s) from a nix-config checkout.

For every labs/<lab>/flake.lock in nix-config: the pinned nixpkgs rev and date, and the
versions of the attributes listed in labs/<lab>/lab.json, read with `nix eval` against that
same rev (no lab flake is evaluated, no inputs fetched). Standard library only.

    python3 scripts/build_readme.py --nix-config ../nix-config --dry-run
    python3 scripts/build_readme.py --nix-config nix-config --readme README.md --readme README.pt-BR.md
"""
import argparse
import json
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

LABELS = {"texliveMedium": "texlive"}  # display name when it differs from the attribute
TRIM_AT_DASH = {"texliveMedium"}       # "2025-r78234-final-env" -> "2025"
STALE_DAYS = 90
START, END = "<!-- nix-labs:start -->", "<!-- nix-labs:end -->"
LAB_URL = "https://github.com/h0ffmann/nix-config/tree/main/labs/{name}"
HEADER = "| lab | what | nixpkgs | locked | toolchain |\n| --- | --- | --- | --- | --- |\n"
NIX_TIMEOUT = 120


def discover_labs(nix_config: Path) -> list[Path]:
    labs = nix_config / "labs"
    if not labs.is_dir():
        raise FileNotFoundError(f"{labs} is not a directory")
    return sorted(p for p in labs.iterdir() if p.is_dir() and (p / "flake.lock").is_file())


def read_nixpkgs_pin(lock_path: Path):
    locked = json.loads(lock_path.read_text()).get("nodes", {}).get("nixpkgs", {}).get("locked")
    if not locked or "rev" not in locked or "lastModified" not in locked:
        return None
    return locked["rev"], datetime.fromtimestamp(locked["lastModified"], tz=timezone.utc).date()


def read_lab_json(lab_dir: Path) -> dict:
    path = lab_dir / "lab.json"
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as error:
        print(f"warning: {path}: {error}", file=sys.stderr)
        return {}
    ok = (isinstance(data, dict) and isinstance(data.get("summary"), str)
          and isinstance(data.get("headline"), list) and all(isinstance(a, str) for a in data["headline"]))
    if not ok:
        print(f"warning: {path}: expected {{summary: str, headline: [str]}}", file=sys.stderr)
        return {}
    return {"summary": data["summary"], "headline": data["headline"]}


def age_text(locked: date, today: date) -> str:
    days = (today - locked).days
    if days == 0:
        return "today"
    return f"{days} day{'s' if days != 1 else ''} ago"


def nix_version(rev: str, attr: str):
    try:
        out = subprocess.run(
            ["nix", "eval", "--raw", f"github:NixOS/nixpkgs/{rev}#{attr}.version"],
            capture_output=True, text=True, timeout=NIX_TIMEOUT, check=False)
    except (OSError, subprocess.TimeoutExpired) as error:
        print(f"warning: nix eval {attr}: {error}", file=sys.stderr)
        return None
    if out.returncode != 0 or not out.stdout.strip():
        print(f"warning: nix eval {attr}@{rev[:7]} failed: {out.stderr.strip()[-200:]}", file=sys.stderr)
        return None
    return out.stdout.strip()


def display_version(attr: str, version: str) -> str:
    return version.split("-", 1)[0] if attr in TRIM_AT_DASH else version


def render_table(labs, today: date, evaluate=nix_version) -> str:
    cache = {}

    def version(rev, attr):
        if (rev, attr) not in cache:
            cache[(rev, attr)] = evaluate(rev, attr)
        return cache[(rev, attr)]

    rows = []
    for lab in labs:
        meta = read_lab_json(lab)
        what = meta.get("summary") or "—"
        pin = read_nixpkgs_pin(lab / "flake.lock")
        if pin is None:
            rev_cell, locked_cell, toolchain = "?", "?", "—"
        else:
            rev, locked = pin
            rev_cell = f"`{rev[:7]}`"
            stale = "⚠️ " if (today - locked).days > STALE_DAYS else ""
            locked_cell = f"{stale}{locked.isoformat()} ({age_text(locked, today)})"
            pairs = []
            for attr in meta.get("headline", []):
                v = version(rev, attr)
                pairs.append(f"{LABELS.get(attr, attr)} {display_version(attr, v) if v else '?'}")
            toolchain = " · ".join(pairs) or "—"
        rows.append(f"| [{lab.name}]({LAB_URL.format(name=lab.name)}) | {what} | {rev_cell} | {locked_cell} | {toolchain} |\n")
    return HEADER + "".join(rows)


def replace_section(text: str, section: str) -> str:
    start, end = text.find(START), text.find(END)
    if start < 0 or end < 0 or end < start:
        raise ValueError(f"README lacks the {START} / {END} marker pair")
    return text[:start + len(START)] + "\n" + section + text[end:]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--nix-config", type=Path, default=Path("../nix-config"))
    ap.add_argument("--readme", type=Path, action="append", help="may repeat; default README.md")
    ap.add_argument("--dry-run", action="store_true", help="print the section, write nothing")
    ap.add_argument("--today", type=date.fromisoformat, default=datetime.now(timezone.utc).date())
    args = ap.parse_args(argv)
    readmes = args.readme or [Path("README.md")]
    try:
        labs = discover_labs(args.nix_config)
    except FileNotFoundError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    if not labs:
        print(f"error: no labs with flake.lock under {args.nix_config}/labs", file=sys.stderr)
        return 2
    section = render_table(labs, args.today)
    if args.dry_run:
        print(section, end="")
        return 0
    for readme in readmes:
        try:
            before = readme.read_text()
            after = replace_section(before, section)
        except (OSError, ValueError) as error:
            print(f"error: {readme}: {error}", file=sys.stderr)
            return 2
        if after != before:
            readme.write_text(after)
        print(f"{readme}: {'changed' if after != before else 'unchanged'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
