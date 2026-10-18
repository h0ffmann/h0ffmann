"""The short CV (cv/summary.md) says nothing that the profile does not say.

A fact about the owner needs a source (AGENTS.md, hard rule 3). The short CV is written by hand,
so these tests tie it to what is already sourced: the README, the long CV's header, me/ and
the site's tables.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUMMARY = (ROOT / "cv" / "summary.md").read_text()
LINK = re.compile(r"\]\(([^)\s]+)\)")


def sources() -> str:
    files = [ROOT / "README.md", ROOT / "cv" / "header.md", *sorted((ROOT / "me").glob("*.md")), *sorted((ROOT / "site" / "data").glob("*.tsv"))]
    return "\n".join(f.read_text() for f in files)


class Summary(unittest.TestCase):
    def test_every_web_link_is_one_the_profile_already_has(self):
        known = sources()
        for target in LINK.findall(SUMMARY):
            if target.startswith(("http://", "https://", "mailto:")):
                # a DOI link counts as known when site/data/works.tsv names its DOI
                doi = target.removeprefix("https://doi.org/")
                self.assertTrue(target.rstrip("/") in known or (doi != target and doi in known),
                                f"{target} is in no README, CV header, me/ page or site table")

    def test_every_link_to_a_file_is_a_file(self):
        for target in LINK.findall(SUMMARY):
            if not re.match(r"^[a-z][a-z0-9+.-]*:", target):
                path = (ROOT / "cv" / target.split("#")[0]).resolve()
                # pdf/cv.full.pdf is made by the build; the rest must be in the repository
                self.assertTrue(path.is_file() or path.name == "cv.full.pdf", f"{target} is not a file")

    def test_every_work_with_a_doi_is_named(self):
        rows = [r.split("\t") for r in (ROOT / "site" / "data" / "works.tsv").read_text().splitlines() if r and not r.startswith("#")]
        for row in rows:
            if row[4]:
                self.assertIn(f"https://doi.org/{row[4]}", SUMMARY, f"{row[1]} has a DOI and is not in the short CV")

    def test_the_tip_says_where_the_links_are_checked(self):
        self.assertIn("::: tip", SUMMARY)
        self.assertIn("../.github/workflows/links.yml", SUMMARY)
        self.assertTrue((ROOT / ".github" / "workflows" / "links.yml").is_file())

    def test_a_heading_of_ways_of_working_that_is_linked_exists(self):
        page = (ROOT / "me" / "ways-of-working.md").read_text()
        slugs = {re.sub(r"[^a-z0-9 -]", "", h.lower()).strip().replace(" ", "-") for h in re.findall(r"^#+ (.+)$", page, re.M)}
        for frag in re.findall(r"ways-of-working\.md#([a-z0-9-]+)", SUMMARY):
            self.assertIn(frag, slugs)


if __name__ == "__main__":
    unittest.main()
