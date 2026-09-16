import unittest

import build_activity as ba


def ev(type_, repo, public=True, action=None, number=None, ref=None, created="2026-09-15T10:00:00Z", extra=None):
    payload = {}
    if action is not None:
        payload["action"] = action
    if type_ == "PullRequestEvent":
        payload["number"] = number
        payload["pull_request"] = {"number": number, "merged": action == "closed", **(extra or {})}
    elif type_ == "IssuesEvent":
        payload["issue"] = {"number": number, "html_url": f"https://github.com/{repo}/issues/{number}"}
    elif type_ == "IssueCommentEvent":
        payload["issue"] = {"number": number, "html_url": f"https://github.com/{repo}/issues/{number}"}
        payload["comment"] = {"html_url": f"https://github.com/{repo}/issues/{number}#issuecomment-1"}
    elif type_ == "PushEvent":
        payload["ref"] = ref or "refs/heads/main"
    elif type_ == "ReleaseEvent":
        payload["release"] = {"tag_name": extra["tag"], "html_url": f"https://github.com/{repo}/releases/tag/{extra['tag']}"}
    return {"type": type_, "repo": {"name": repo}, "public": public, "payload": payload, "created_at": created}


class RepoText(unittest.TestCase):
    def test_public_repo_is_a_link(self):
        self.assertEqual(ba.repo_text("h0ffmann/nix-config", True), "[h0ffmann/nix-config](https://github.com/h0ffmann/nix-config)")

    def test_private_repo_is_plain_name_with_lock(self):
        self.assertEqual(ba.repo_text("h0ffmann/scala-ops", False), "scala-ops 🔒")

    def test_private_repo_with_label(self):
        self.assertEqual(ba.repo_text("h0ffmann/marola", False), "marola 🔒 FOSS soon")


class EventLines(unittest.TestCase):
    def test_public_pr_merged_links_number(self):
        line = ba.event_line(ev("PullRequestEvent", "h0ffmann/h0ffmann", action="closed", number=5, extra={"merged": True}))
        self.assertEqual(line, "✔ Merged PR [#5](https://github.com/h0ffmann/h0ffmann/pull/5) in [h0ffmann/h0ffmann](https://github.com/h0ffmann/h0ffmann)")

    def test_public_pr_opened(self):
        line = ba.event_line(ev("PullRequestEvent", "h0ffmann/h0ffmann", action="opened", number=9))
        self.assertEqual(line, "◆ Opened PR [#9](https://github.com/h0ffmann/h0ffmann/pull/9) in [h0ffmann/h0ffmann](https://github.com/h0ffmann/h0ffmann)")

    def test_private_pr_has_no_number_or_link(self):
        line = ba.event_line(ev("PullRequestEvent", "h0ffmann/marola", public=False, action="closed", number=88, extra={"merged": True}))
        self.assertEqual(line, "✔ Merged a PR in marola 🔒 FOSS soon")

    def test_pr_closed_without_merge(self):
        line = ba.event_line(ev("PullRequestEvent", "h0ffmann/x", action="closed", number=1, extra={"merged": False}))
        self.assertTrue(line.startswith("✕ Closed PR [#1]"))

    def test_issue_opened_public_and_private(self):
        self.assertEqual(ba.event_line(ev("IssuesEvent", "h0ffmann/h0ffmann", action="opened", number=4)),
                         "◇ Opened issue [#4](https://github.com/h0ffmann/h0ffmann/issues/4) in [h0ffmann/h0ffmann](https://github.com/h0ffmann/h0ffmann)")
        self.assertEqual(ba.event_line(ev("IssuesEvent", "h0ffmann/marola", public=False, action="opened", number=4)),
                         "◇ Opened an issue in marola 🔒 FOSS soon")

    def test_comment(self):
        self.assertEqual(ba.event_line(ev("IssueCommentEvent", "h0ffmann/h0ffmann", action="created", number=3)),
                         "✎ Commented on [#3](https://github.com/h0ffmann/h0ffmann/issues/3#issuecomment-1) in [h0ffmann/h0ffmann](https://github.com/h0ffmann/h0ffmann)")

    def test_push_names_branch(self):
        self.assertEqual(ba.event_line(ev("PushEvent", "h0ffmann/marola", public=False, ref="refs/heads/feat/x")),
                         "↑ Pushed to feat/x in marola 🔒 FOSS soon")

    def test_release_published(self):
        self.assertEqual(ba.event_line(ev("ReleaseEvent", "h0ffmann/ww-lab", action="published", extra={"tag": "v1.2"})),
                         "▲ Published release [v1.2](https://github.com/h0ffmann/ww-lab/releases/tag/v1.2) in [h0ffmann/ww-lab](https://github.com/h0ffmann/ww-lab)")

    def test_unknown_or_uninteresting_events_are_skipped(self):
        self.assertIsNone(ba.event_line(ev("WatchEvent", "x/y", action="started")))
        self.assertIsNone(ba.event_line(ev("PullRequestEvent", "x/y", action="synchronize", number=1)))
        self.assertIsNone(ba.event_line(ev("ReleaseEvent", "x/y", action="created", extra={"tag": "v0"})))


class Render(unittest.TestCase):
    def test_collapses_consecutive_identical_lines_and_limits(self):
        events = [ev("PushEvent", "h0ffmann/marola", public=False)] * 4 + [
            ev("PullRequestEvent", "h0ffmann/h0ffmann", action="opened", number=9),
            ev("PushEvent", "h0ffmann/marola", public=False),
            ev("IssuesEvent", "h0ffmann/h0ffmann", action="opened", number=4),
            ev("IssuesEvent", "h0ffmann/h0ffmann", action="opened", number=3),
            ev("IssuesEvent", "h0ffmann/h0ffmann", action="opened", number=2),
            ev("IssuesEvent", "h0ffmann/h0ffmann", action="opened", number=1),
        ]
        lines = ba.render(events, limit=5)
        self.assertEqual(len(lines), 5)
        self.assertEqual(lines[0], "1. ↑ Pushed to main in marola 🔒 FOSS soon")
        self.assertTrue(lines[1].startswith("2. ◆ Opened PR [#9]"))
        self.assertEqual(lines[2], "3. ↑ Pushed to main in marola 🔒 FOSS soon")
        self.assertTrue(lines[3].startswith("4. ◇ Opened issue [#4]"))
        self.assertTrue(lines[4].startswith("5. ◇ Opened issue [#3]"))

    def test_empty_when_nothing_interesting(self):
        self.assertEqual(ba.render([ev("WatchEvent", "x/y", action="started")], limit=5), [])


class Dispatched(unittest.TestCase):
    PAYLOAD = {"repo": "h0ffmann/nix-config", "number": 59, "private": False, "merged_at": "2026-09-15T12:00:00Z"}

    def test_merge_not_yet_in_the_api_is_added_newest_first(self):
        older = ev("PushEvent", "h0ffmann/marola", public=False, created="2026-09-15T10:00:00Z")
        lines = ba.render(ba.with_dispatched([older], self.PAYLOAD), limit=10)
        self.assertEqual(lines, [
            "1. ✔ Merged PR [#59](https://github.com/h0ffmann/nix-config/pull/59) in [h0ffmann/nix-config](https://github.com/h0ffmann/nix-config)",
            "2. ↑ Pushed to main in marola 🔒 FOSS soon",
        ])

    def test_merge_already_in_the_api_is_not_duplicated(self):
        events = [ev("PullRequestEvent", "h0ffmann/nix-config", action="closed", number=59, created="2026-09-15T12:00:05Z")]
        self.assertEqual(ba.with_dispatched(events, self.PAYLOAD), events)

    def test_private_merge_has_no_number_or_link(self):
        payload = {**self.PAYLOAD, "repo": "h0ffmann/marola", "private": True}
        self.assertEqual(ba.render(ba.with_dispatched([], payload), limit=10), ["1. ✔ Merged a PR in marola 🔒 FOSS soon"])

    def test_malformed_payloads_are_ignored(self):
        for payload in (None, "x", {}, {"repo": "h0ffmann/x", "number": "59"}, {"repo": "](evil)", "number": 1},
                        {"repo": "h0ffmann/x", "number": 0}):
            self.assertEqual(ba.with_dispatched([], payload), [], payload)


class SkipRepos(unittest.TestCase):
    def test_profile_repo_events_are_dropped(self):
        events = [ev("PushEvent", "h0ffmann/h0ffmann"),
                  ev("PullRequestEvent", "h0ffmann/h0ffmann", action="opened", number=7),
                  ev("PushEvent", "h0ffmann/nix-config")]
        lines = ba.render(events, limit=10, skip=["h0ffmann/h0ffmann"])
        self.assertEqual(lines, ["1. ↑ Pushed to main in [h0ffmann/nix-config](https://github.com/h0ffmann/nix-config)"])

    def test_limit_still_fills_from_other_repos(self):
        events = [ev("PushEvent", "h0ffmann/h0ffmann")] * 5 + [
            ev("PushEvent", "h0ffmann/nix-config"), ev("PushEvent", "h0ffmann/ww3-gpu")]
        self.assertEqual(len(ba.render(events, limit=2, skip=["h0ffmann/h0ffmann"])), 2)

    def test_empty_skip_keeps_everything(self):
        events = [ev("PushEvent", "h0ffmann/h0ffmann")]
        self.assertEqual(len(ba.render(events, limit=10, skip=[""])), 1)
        self.assertEqual(len(ba.render(events, limit=10)), 1)


class ReplaceSection(unittest.TestCase):
    def test_replaces_between_activity_markers(self):
        text = "a\n<!--START_SECTION:activity-->\nold\n<!--END_SECTION:activity-->\nb\n"
        self.assertEqual(ba.replace_section(text, ["1. x", "2. y"]),
                         "a\n<!--START_SECTION:activity-->\n1. x\n2. y\n<!--END_SECTION:activity-->\nb\n")

    def test_raises_without_markers(self):
        with self.assertRaises(ValueError):
            ba.replace_section("nothing\n", ["1. x"])


if __name__ == "__main__":
    unittest.main()
