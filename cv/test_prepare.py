import unittest

import prepare as p

QR = ('<a href="https://marola.dev" target="_blank"><img src="marola-qr.svg" alt="QR code for marola.dev" '
      'title="scan for marola.dev" align="right" width="120" /></a>\n')


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


class QrLine(unittest.TestCase):
    def test_floated_qr_line_is_removed(self):
        self.assertEqual(p.drop_qr("x\n" + QR + "y\n"), "x\ny\n")

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
