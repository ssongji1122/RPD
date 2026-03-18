from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import content_pipeline


class PublicPagesSmokeTest(unittest.TestCase):
    def test_public_pages_exist_and_stay_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "public-site"
            build_info = content_pipeline.build_public_site(output_dir)

            index_html = (output_dir / "index.html").read_text(encoding="utf-8")
            week_html = (output_dir / "week.html").read_text(encoding="utf-8")
            library_html = (output_dir / "library.html").read_text(encoding="utf-8")
            shortcuts_html = (output_dir / "shortcuts.html").read_text(encoding="utf-8")
            build_meta = json.loads((output_dir / "data" / "public-build.json").read_text(encoding="utf-8"))

            self.assertEqual(build_meta["version"], build_info["version"])
            self.assertTrue((output_dir / "index.html").exists())
            self.assertTrue((output_dir / "week.html").exists())
            self.assertTrue((output_dir / "library.html").exists())
            self.assertTrue((output_dir / "shortcuts.html").exists())

            self.assertIn("assets/i18n.js", index_html)
            self.assertIn("assets/i18n.js", week_html)
            self.assertIn("data/curriculum.js", week_html)
            self.assertIn("Show Me", library_html)
            self.assertIn("Shortcuts", shortcuts_html)

            for html in (index_html, week_html, library_html, shortcuts_html):
                self.assertNotIn("/api/curriculum", html)
                self.assertNotIn("/api/notion-quiz", html)
                self.assertNotIn("Authorization", html)
                self.assertNotIn("rpd-admin-token", html)

            self.assertNotIn("students.js", week_html)
            self.assertNotIn("student-progress.json", week_html)


if __name__ == "__main__":
    unittest.main()
