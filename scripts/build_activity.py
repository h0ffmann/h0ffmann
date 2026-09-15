#!/usr/bin/env python3
"""Rewrite the recent-activity list in the README(s) from the GitHub events API.

    GITHUB_TOKEN=... python3 scripts/build_activity.py --readme README.md --readme README.pt-BR.md
    python3 scripts/build_activity.py --events-json events.json --dry-run

Reads the authenticated user's own events (private ones included when the token can see them)
and writes the newest interesting ones between <!--START_SECTION:activity--> and
<!--END_SECTION:activity-->. Public repositories and items are linked; a private repository is
shown as its bare name with a lock, plus a label from PRIVATE_LABELS, and its PRs/issues carry
no number or link. Consecutive identical lines (a run of pushes) collapse into one.
Standard library only.
"""
import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path

PRIVATE_LABELS = {"h0ffmann/marola": "FOSS soon"}
START, END = "<!--START_SECTION:activity-->", "<!--END_SECTION:activity-->"
API = "https://api.github.com"


def repo_text(name: str, public: bool) -> str:
    if public:
        return f"[{name}]({'https://github.com/' + name})"
    label = PRIVATE_LABELS.get(name)
    return f"{name.split('/', 1)[-1]} 🔒" + (f" {label}" if label else "")


def _pr_merged(event, fetch):
    pr = event["payload"].get("pull_request", {})
    if "merged" in pr:
        return bool(pr["merged"])
    if fetch is None:
        return False
    data = fetch(f"{API}/repos/{event['repo']['name']}/pulls/{pr.get('number') or event['payload'].get('number')}")
    return bool(data and data.get("merged_at"))


def event_line(event, fetch=None):
    t, repo, public = event["type"], event["repo"]["name"], event.get("public", True)
    p = event.get("payload") or {}
    where = repo_text(repo, public)
    action = p.get("action")
    if t == "PullRequestEvent":
        n = p.get("number") or p.get("pull_request", {}).get("number")
        if action == "opened":
            emoji, verb = "💪", "Opened"
        elif action == "reopened":
            emoji, verb = "🔁", "Reopened"
        elif action == "closed":
            emoji, verb = ("🎉", "Merged") if _pr_merged(event, fetch) else ("❌", "Closed")
        else:
            return None
        what = f"PR [#{n}](https://github.com/{repo}/pull/{n})" if public else "a PR"
        return f"{emoji} {verb} {what} in {where}"
    if t == "IssuesEvent":
        if action not in ("opened", "closed", "reopened"):
            return None
        emoji = {"opened": "❗", "closed": "✅", "reopened": "🔁"}[action]
        issue = p.get("issue", {})
        what = f"issue [#{issue.get('number')}]({issue.get('html_url')})" if public else "an issue"
        return f"{emoji} {action.capitalize()} {what} in {where}"
    if t == "IssueCommentEvent":
        if action != "created":
            return None
        issue, comment = p.get("issue", {}), p.get("comment", {})
        what = f"[#{issue.get('number')}]({comment.get('html_url')})" if public else "an issue"
        return f"🗣 Commented on {what} in {where}"
    if t == "PushEvent":
        branch = (p.get("ref") or "").removeprefix("refs/heads/")
        return f"⬆️ Pushed to {branch} in {where}"
    if t == "ReleaseEvent":
        if action != "published":
            return None
        rel = p.get("release", {})
        what = f"release [{rel.get('tag_name')}]({rel.get('html_url')})" if public else "a release"
        return f"🚀 Published {what} in {where}"
    return None


def render(events, limit: int, fetch=None) -> list:
    lines, last = [], None
    for event in events:
        line = event_line(event, fetch)
        if line and line != last:
            lines.append(line)
            last = line
        if len(lines) == limit:
            break
    return [f"{i}. {line}" for i, line in enumerate(lines, 1)]


def replace_section(text: str, lines: list) -> str:
    start, end = text.find(START), text.find(END)
    if start < 0 or end < 0 or end < start:
        raise ValueError(f"README lacks the {START} / {END} marker pair")
    body = "".join(line + "\n" for line in lines)
    return text[:start + len(START)] + "\n" + body + text[end:]


def github_get(token: str):
    def fetch(url: str):
        req = urllib.request.Request(url, headers={
            "Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "h0ffmann-profile-activity"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.load(resp)
        except (OSError, ValueError) as error:
            print(f"warning: GET {url}: {error}", file=sys.stderr)
            return None
    return fetch


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--login", default="h0ffmann")
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--readme", type=Path, action="append", help="may repeat; default README.md")
    ap.add_argument("--events-json", type=Path, help="read events from a file instead of the API")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    token = os.environ.get("GITHUB_TOKEN", "")
    fetch = github_get(token) if token else None
    if args.events_json:
        events = json.loads(args.events_json.read_text())
    else:
        if not fetch:
            print("error: GITHUB_TOKEN is not set and no --events-json given", file=sys.stderr)
            return 2
        events = fetch(f"{API}/users/{args.login}/events?per_page=100")
        if events is None:
            return 2
    lines = render(events, args.limit, fetch)
    if args.dry_run:
        print("\n".join(lines))
        return 0
    for readme in args.readme or [Path("README.md")]:
        try:
            before = readme.read_text()
            after = replace_section(before, lines)
        except (OSError, ValueError) as error:
            print(f"error: {readme}: {error}", file=sys.stderr)
            return 2
        if after != before:
            readme.write_text(after)
        print(f"{readme}: {'changed' if after != before else 'unchanged'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
