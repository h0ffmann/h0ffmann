import contextlib
import io
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

import build_readme as br


def make_lab(root: Path, name: str, rev: str = "eaad089433ca2bb662274377d33df3d0e51ef28b",
             last_modified: int = 1789149629, lab_json=None, with_lock=True):
    lab = root / "labs" / name
    lab.mkdir(parents=True)
    if with_lock:
        lock = {"nodes": {"nixpkgs": {"locked": {"rev": rev, "lastModified": last_modified}}}, "root": "root"}
        (lab / "flake.lock").write_text(json.dumps(lock))
    if lab_json is not None:
        (lab / "lab.json").write_text(lab_json if isinstance(lab_json, str) else json.dumps(lab_json))
    return lab


class AgeText(unittest.TestCase):
    def test_same_day_is_today(self):
        self.assertEqual(br.age_text(date(2026, 9, 15), date(2026, 9, 15)), "today")

    def test_one_day(self):
        self.assertEqual(br.age_text(date(2026, 9, 14), date(2026, 9, 15)), "1 day ago")

    def test_many_days(self):
        self.assertEqual(br.age_text(date(2026, 9, 1), date(2026, 9, 15)), "14 days ago")


class ReadNixpkgsPin(unittest.TestCase):
    def test_parses_rev_and_date(self):
        with tempfile.TemporaryDirectory() as d:
            lab = make_lab(Path(d), "a", rev="abcdef0123456789", last_modified=1789149629)  # 2026-09-11 UTC
            self.assertEqual(br.read_nixpkgs_pin(lab / "flake.lock"), ("abcdef0123456789", date(2026, 9, 11)))

    def test_none_without_nixpkgs_node(self):
        with tempfile.TemporaryDirectory() as d:
            lab = Path(d) / "labs" / "a"
            lab.mkdir(parents=True)
            (lab / "flake.lock").write_text(json.dumps({"nodes": {"root": {}}}))
            self.assertIsNone(br.read_nixpkgs_pin(lab / "flake.lock"))


class ReadLabJson(unittest.TestCase):
    def test_reads_summary_and_headline(self):
        with tempfile.TemporaryDirectory() as d:
            lab = make_lab(Path(d), "a", lab_json={"summary": "x", "headline": ["pandoc"]})
            self.assertEqual(br.read_lab_json(lab), {"summary": "x", "headline": ["pandoc"]})

    def test_missing_file_gives_empty(self):
        with tempfile.TemporaryDirectory() as d:
            lab = make_lab(Path(d), "a")
            self.assertEqual(br.read_lab_json(lab), {})

    def test_malformed_gives_empty(self):
        with tempfile.TemporaryDirectory() as d:
            lab = make_lab(Path(d), "a", lab_json="{not json")
            with contextlib.redirect_stderr(io.StringIO()) as err:
                self.assertEqual(br.read_lab_json(lab), {})
            self.assertIn("warning", err.getvalue())

    def test_wrong_shape_gives_empty(self):
        with tempfile.TemporaryDirectory() as d:
            lab = make_lab(Path(d), "a", lab_json={"summary": 3, "headline": "pandoc"})
            with contextlib.redirect_stderr(io.StringIO()) as err:
                self.assertEqual(br.read_lab_json(lab), {})
            self.assertIn("warning", err.getvalue())


class DiscoverLabs(unittest.TestCase):
    def test_only_dirs_with_flake_lock_sorted(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            make_lab(root, "zeta")
            make_lab(root, "alpha")
            make_lab(root, "nolock", with_lock=False)
            (root / "labs" / "afile").write_text("")
            self.assertEqual([p.name for p in br.discover_labs(root)], ["alpha", "zeta"])

    def test_missing_labs_dir_raises(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(FileNotFoundError):
                br.discover_labs(Path(d))


class RenderTable(unittest.TestCase):
    TODAY = date(2026, 9, 15)

    def test_row_links_lab_and_shows_summary_rev_age_and_versions(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            make_lab(root, "publisher", rev="eaad089433ca2bb662274377d33df3d0e51ef28b", last_modified=1789149629,
                     lab_json={"summary": "pandoc + TeX Live", "headline": ["pandoc"]})
            out = br.render_table(br.discover_labs(root), self.TODAY, evaluate=lambda rev, attr: "3.7.0.2")
            self.assertIn("| lab | what | nixpkgs | locked | toolchain |", out)
            self.assertIn("[publisher](https://github.com/h0ffmann/nix-config/tree/main/labs/publisher)", out)
            self.assertIn("| pandoc + TeX Live |", out)
            self.assertIn("| `eaad089` |", out)
            self.assertIn("| 2026-09-11 (4 days ago) |", out)
            self.assertIn("| pandoc 3.7.0.2 |", out)

    def test_same_rev_evaluated_once_per_attr(self):
        calls = []
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            make_lab(root, "a", lab_json={"summary": "a", "headline": ["python3"]})
            make_lab(root, "b", lab_json={"summary": "b", "headline": ["python3", "pandoc"]})
            br.render_table(br.discover_labs(root), self.TODAY,
                            evaluate=lambda rev, attr: calls.append((rev, attr)) or "1.0")
            self.assertEqual(sorted(calls), sorted({("eaad089433ca2bb662274377d33df3d0e51ef28b", "python3"),
                                                    ("eaad089433ca2bb662274377d33df3d0e51ef28b", "pandoc")}))

    def test_texlive_label_and_version_trimmed(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            make_lab(root, "a", lab_json={"summary": "a", "headline": ["texliveMedium"]})
            out = br.render_table(br.discover_labs(root), self.TODAY, evaluate=lambda rev, attr: "2025-r78234-final-env")
            self.assertIn("| texlive 2025 |", out)

    def test_stale_marker_past_90_days(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            make_lab(root, "a", last_modified=1780000000, lab_json={"summary": "a", "headline": []})  # 2026-05-28
            out = br.render_table(br.discover_labs(root), self.TODAY, evaluate=lambda rev, attr: "1")
            self.assertIn("| ⚠️ 2026-05-28 (110 days ago) |", out)

    def test_question_mark_when_evaluate_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            make_lab(root, "a", lab_json={"summary": "a", "headline": ["gone", "pandoc"]})
            out = br.render_table(br.discover_labs(root), self.TODAY,
                                  evaluate=lambda rev, attr: None if attr == "gone" else "3.7")
            self.assertIn("| gone ? · pandoc 3.7 |", out)

    def test_dash_without_lab_json(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            make_lab(root, "a")
            out = br.render_table(br.discover_labs(root), self.TODAY, evaluate=lambda rev, attr: "1")
            self.assertIn("| [a](https://github.com/h0ffmann/nix-config/tree/main/labs/a) | — | `eaad089` |", out)
            self.assertTrue(out.rstrip().endswith("| — |"))

    def test_question_marks_without_nixpkgs_node(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            lab = Path(d) / "labs" / "a"
            lab.mkdir(parents=True)
            (lab / "flake.lock").write_text(json.dumps({"nodes": {"root": {}}}))
            out = br.render_table(br.discover_labs(root), self.TODAY, evaluate=lambda rev, attr: "1")
            self.assertIn("| — | ? | ? | — |", out)


class ReplaceSection(unittest.TestCase):
    def test_replaces_only_between_markers(self):
        text = "before\n<!-- nix-labs:start -->\nold\n<!-- nix-labs:end -->\nafter\n"
        out = br.replace_section(text, "| new |\n")
        self.assertEqual(out, "before\n<!-- nix-labs:start -->\n| new |\n<!-- nix-labs:end -->\nafter\n")

    def test_idempotent(self):
        text = "<!-- nix-labs:start -->\n<!-- nix-labs:end -->\n"
        once = br.replace_section(text, "x\n")
        self.assertEqual(br.replace_section(once, "x\n"), once)

    def test_raises_without_markers(self):
        with self.assertRaises(ValueError):
            br.replace_section("no markers here\n", "x\n")


if __name__ == "__main__":
    unittest.main()
