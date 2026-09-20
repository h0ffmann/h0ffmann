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


class BottomBlocks(unittest.TestCase):
    def test_block_moves_to_the_end_and_its_heading_is_promoted(self):
        text = "## me\n\nbio\n<!-- cv:bottom -->\n### building marola\n\npitch\n<!-- cv:end -->\n\n## certs\n\nlist\n"
        self.assertEqual(p.move_bottom(text), "## me\n\nbio\n\n## certs\n\nlist\n\n## building marola\n\npitch\n")

    def test_only_the_first_heading_of_the_block_is_promoted(self):
        text = "<!-- cv:bottom -->\n### a\n### b\n<!-- cv:end -->\nrest\n"
        self.assertEqual(p.move_bottom(text), "rest\n\n## a\n### b\n")

    def test_several_blocks_keep_their_order(self):
        text = "<!-- cv:bottom -->\nx\n<!-- cv:end -->\nmid\n<!-- cv:bottom -->\ny\n<!-- cv:end -->\n"
        self.assertEqual(p.move_bottom(text), "mid\n\nx\n\ny\n")

    def test_text_without_markers_is_unchanged(self):
        self.assertEqual(p.move_bottom("## me\n\nbio\n"), "## me\n\nbio\n")

    def test_unmatched_start_raises(self):
        with self.assertRaises(ValueError):
            p.move_bottom("<!-- cv:bottom -->\nx\n")

    def test_skip_inside_bottom_raises(self):
        with self.assertRaises(ValueError):
            p.strip_skipped("<!-- cv:bottom -->\n<!-- cv:skip -->\nx\n<!-- cv:end -->\n<!-- cv:end -->\n")

    def test_skip_leaves_bottom_blocks_alone(self):
        text = "<!-- cv:bottom -->\nx\n<!-- cv:end -->\n"
        self.assertEqual(p.strip_skipped(text), text)


class Prepare(unittest.TestCase):
    def test_bottom_block_lands_after_everything_else(self):
        readme = "## me\n<!-- cv:bottom -->\n### marola\n" + QR + "pitch\n<!-- cv:end -->\n## misc\n<!-- cv:skip -->\nphoto\n<!-- cv:end -->\n"
        self.assertEqual(p.prepare(readme, ""), "## me\n## misc\n\n## marola\npitch\n")

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
