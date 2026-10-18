import re
import unittest
from pathlib import Path

import prepare as p

ROOT = Path(__file__).resolve().parent.parent
READMES = [ROOT / f"README{suffix}.md" for suffix in ("", ".pt-BR", ".ja")]
QR = ('<a href="https://marola.dev" target="_blank"><img src="marola-qr.svg" alt="QR code for marola.dev" '
      'title="scan for marola.dev" align="right" width="120" /></a>\n')
HEADING = re.compile(r"^## ", re.MULTILINE)


class SkipBlocks(unittest.TestCase):
    def test_removes_span_between_markers(self):
        text = "keep 1\n<!-- cv:skip -->\ngone\nalso gone\n<!-- cv:end -->\nkeep 2\n"
        self.assertEqual(p.strip_skipped(text), "keep 1\nkeep 2\n")

    def test_removes_several_spans(self):
        text = "a\n<!-- cv:skip -->\nx\n<!-- cv:end -->\nb\n<!-- cv:skip -->\ny\n<!-- cv:end -->\nc\n"
        self.assertEqual(p.strip_skipped(text), "a\nb\nc\n")

    def test_unmatched_start_raises(self):
        with self.assertRaises(ValueError):
            p.strip_skipped("a\n<!-- cv:skip -->\nb\n")

    def test_unmatched_end_raises(self):
        with self.assertRaises(ValueError):
            p.strip_skipped("a\n<!-- cv:end -->\nb\n")

    def test_nested_raises(self):
        with self.assertRaises(ValueError):
            p.strip_skipped("<!-- cv:skip -->\n<!-- cv:skip -->\nx\n<!-- cv:end -->\n<!-- cv:end -->\n")

    def test_text_without_markers_is_unchanged(self):
        text = "## 👋 me\n\nplain **bold** text\n"
        self.assertEqual(p.strip_skipped(text), text)


class OnlyBlocks(unittest.TestCase):
    """`<!-- cv:only` … `cv:end -->` is an HTML comment on github.com; the CV keeps its inside."""

    def test_block_is_unwrapped(self):
        text = "a\n<!-- cv:only\n## ⚡ research\n\n<p align=\"left\">\n<img src=\"x\" />\n</p>\ncv:end -->\nb\n"
        self.assertEqual(p.strip_skipped(text), "a\n## ⚡ research\n\n<p align=\"left\">\n<img src=\"x\" />\n</p>\nb\n")

    def test_skip_and_only_blocks_mix(self):
        text = "<!-- cv:skip -->\nx\n<!-- cv:end -->\na\n<!-- cv:only\nb\ncv:end -->\n<!-- cv:skip -->\ny\n<!-- cv:end -->\nc\n"
        self.assertEqual(p.strip_skipped(text), "a\nb\nc\n")

    def test_unclosed_only_raises(self):
        with self.assertRaises(ValueError):
            p.strip_skipped("<!-- cv:only\na\n")

    def test_only_end_without_start_raises(self):
        with self.assertRaises(ValueError):
            p.strip_skipped("a\ncv:end -->\n")

    def test_skip_end_does_not_close_only(self):
        with self.assertRaises(ValueError):
            p.strip_skipped("<!-- cv:only\na\n<!-- cv:end -->\n")

    def test_only_end_does_not_close_skip(self):
        with self.assertRaises(ValueError):
            p.strip_skipped("<!-- cv:skip -->\na\ncv:end -->\n")

    def test_only_inside_skip_raises(self):
        with self.assertRaises(ValueError):
            p.strip_skipped("<!-- cv:skip -->\n<!-- cv:only\na\ncv:end -->\n<!-- cv:end -->\n")

    def test_skip_inside_only_raises(self):
        with self.assertRaises(ValueError):
            p.strip_skipped("<!-- cv:only\n<!-- cv:skip -->\na\n<!-- cv:end -->\ncv:end -->\n")


def shown_on_github(text: str) -> str:
    """What the profile page renders: the `cv:only` comments gone, everything else kept."""
    out, hidden = [], False
    for line in text.splitlines(keepends=True):
        if line.strip() == p.ONLY_START:
            hidden = True
        elif line.strip() == p.ONLY_END:
            hidden = False
        elif not hidden:
            out.append(line)
    return "".join(out)


class Readmes(unittest.TestCase):
    """The three READMEs are edited together: same markers, same sections, in the same order."""

    def test_marker_lines_are_identical_in_the_three_readmes(self):
        lists = [p.markers(path.read_text()) for path in READMES]
        self.assertTrue(lists[0], "no cv markers in README.md")
        self.assertEqual(lists[0], lists[1], "README.pt-BR.md markers differ from README.md")
        self.assertEqual(lists[0], lists[2], "README.ja.md markers differ from README.md")

    def test_profile_shows_five_sections_and_cv_seven(self):
        for path in READMES:
            text = path.read_text()
            with self.subTest(readme=path.name):
                # me, marola, closed-source, certs, misc. The arc is on the site only.
                self.assertEqual(len(HEADING.findall(shown_on_github(text))), 5)
                self.assertEqual(len(HEADING.findall(p.prepare(text, ""))), 7)

    def test_no_line_inside_an_only_block_closes_the_html_comment_early(self):
        for path in READMES:
            hidden = False
            for n, line in enumerate(path.read_text().splitlines(), 1):
                if line.strip() == p.ONLY_START:
                    hidden = True
                elif line.strip() == p.ONLY_END:
                    hidden = False
                elif hidden:
                    self.assertNotIn("-->", line, f"{path.name}:{n} ends the cv:only comment early")


class QrLine(unittest.TestCase):
    def test_floated_qr_line_is_removed(self):
        self.assertEqual(p.drop_qr("x\n" + QR + "y\n"), "x\ny\n")

    def test_portuguese_qr_line_is_removed_too(self):
        qr_pt = ('<a href="https://marola.dev" target="_blank"><img src="marola-qr.svg" alt="QR code para marola.dev" '
                 'title="escaneie para abrir marola.dev" align="right" width="120" /></a>\n')
        self.assertEqual(p.drop_qr("x\n" + qr_pt + "y\n"), "x\ny\n")

    def test_japanese_qr_line_is_removed_too(self):
        qr_ja = ('<a href="https://marola.dev" target="_blank"><img src="marola-qr.svg" alt="marola.dev の QR コード" '
                 'title="スキャンして marola.dev を開く" align="right" width="120" /></a>\n')
        self.assertEqual(p.drop_qr("x\n" + qr_ja + "y\n"), "x\ny\n")

    def test_no_qr_is_unchanged(self):
        self.assertEqual(p.drop_qr("nothing here\n"), "nothing here\n")


class RemoteImages(unittest.TestCase):
    def test_linked_remote_markdown_image_is_dropped(self):
        text = "intro\n\n[![nix-config ci](https://github.com/h0ffmann/nix-config/actions/workflows/ci.yml/badge.svg)](https://github.com/h0ffmann/nix-config/actions/workflows/ci.yml)\n\nnext\n"
        self.assertEqual(p.unremote_images(text), "intro\n\n\n\nnext\n")

    def test_bare_remote_markdown_image_is_dropped(self):
        self.assertEqual(p.unremote_images("see ![a chart](https://x.example/c.png) here\n"), "see  here\n")

    def test_local_markdown_image_is_kept(self):
        text = "[![](marola-qr.svg){width=28mm}](https://marola.dev)\n"
        self.assertEqual(p.unremote_images(text), text)


class Prepare(unittest.TestCase):
    def test_header_first_then_body_with_skips_and_qr_removed(self):
        header = "# Matheus Hoffmann\n\ncontact\n"
        readme = "<!-- cv:skip -->\nswitch line\n<!-- cv:end -->\n\n## 👋 me\n\n" + QR + "bio\n"
        out = p.prepare(readme, header)
        self.assertEqual(out, "# Matheus Hoffmann\n\ncontact\n\n\n## 👋 me\n\nbio\n")

    def test_idempotent_on_prepared_output(self):
        header = "# H\n"
        readme = "a\n<!-- cv:skip -->\nb\n<!-- cv:end -->\n" + QR
        once = p.prepare(readme, header)
        self.assertEqual(p.prepare(once, ""), once)


if __name__ == "__main__":
    unittest.main()
