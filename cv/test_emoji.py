import unittest
from pathlib import Path

import cvemoji as e
import prepare as p

ROOT = Path(__file__).resolve().parent.parent


class Sequences(unittest.TestCase):
    def test_plain_emoji(self):
        self.assertEqual(e.sequences("## 👋 me and 🌊"), ["👋", "🌊"])

    def test_variation_selector_stays_with_its_base(self):
        self.assertEqual(e.sequences("### ☁️ cloud"), ["☁️"])

    def test_bmp_emoji_without_selector(self):
        self.assertEqual(e.sequences("### ⚡ high-end"), ["⚡"])

    def test_zwj_sequence_is_one_emoji(self):
        self.assertEqual(e.sequences("a 🏊‍♂️ b"), ["🏊‍♂️"])

    def test_flag_is_one_emoji(self):
        self.assertEqual(e.sequences("🇧🇷 português"), ["🇧🇷"])

    def test_percent_encoded_badge_text_is_found(self):
        self.assertEqual(e.sequences("badge/%F0%9F%8C%8A_marola.dev-0077BE"), ["🌊"])

    def test_text_symbols_are_not_emoji(self):
        self.assertEqual(e.sequences("a — b · c ↑ ◆ 日本語 ・"), [])


class Names(unittest.TestCase):
    def test_noto_name_drops_the_variation_selector(self):
        self.assertEqual(e.name("☁️"), "emoji_u2601")

    def test_noto_name_joins_codepoints(self):
        self.assertEqual(e.name("🏊‍♂️"), "emoji_u1f3ca_200d_2642")


class Artwork(unittest.TestCase):
    def test_every_emoji_in_the_three_cvs_has_vendored_artwork(self):
        missing = set()
        for suffix in ("", ".pt-BR", ".ja"):
            text = p.prepare((ROOT / f"README{suffix}.md").read_text(), (ROOT / f"cv/header{suffix}.md").read_text())
            missing |= {s for s in e.sequences(text) if not (ROOT / "cv/emoji" / f"{e.name(s)}.svg").exists()}
        self.assertFalse(missing, f"no artwork for {' '.join(sorted(missing))} — run: python3 cv/cvemoji.py --fetch")


if __name__ == "__main__":
    unittest.main()
