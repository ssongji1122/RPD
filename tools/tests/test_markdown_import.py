from __future__ import annotations

import unittest
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import content_pipeline
from markdown_import import build_curriculum_from_markdown


class MarkdownImportTest(unittest.TestCase):
    def test_markdown_import_builds_all_weeks(self) -> None:
        merged = build_curriculum_from_markdown(ROOT / "weeks", [])

        self.assertEqual(len(merged), 15)
        week1 = next(week for week in merged if week["week"] == 1)
        self.assertIn("오리엔테이션", week1["title"])
        self.assertGreaterEqual(len(week1["steps"]), 1)
        self.assertTrue(week1["assignment"]["title"])

    def test_markdown_import_preserves_existing_step_extras(self) -> None:
        existing = content_pipeline.load_canonical_curriculum()
        merged = build_curriculum_from_markdown(ROOT / "weeks", existing)

        existing_week2 = next(week for week in existing if week["week"] == 2)
        merged_week2 = next(week for week in merged if week["week"] == 2)

        self.assertEqual(
            merged_week2["steps"][0].get("showme"),
            existing_week2["steps"][0].get("showme"),
        )
        self.assertEqual(
            merged_week2["steps"][0].get("image"),
            existing_week2["steps"][0].get("image"),
        )

    def test_markdown_import_parses_reference_links(self) -> None:
        existing = content_pipeline.load_canonical_curriculum()
        merged = build_curriculum_from_markdown(ROOT / "weeks", existing)

        week1 = next(week for week in merged if week["week"] == 1)
        doc_titles = {item["title"] for item in week1["docs"]}

        self.assertIn("Blender 설치 가이드", doc_titles)
        self.assertTrue(week1["videos"])


if __name__ == "__main__":
    unittest.main()
