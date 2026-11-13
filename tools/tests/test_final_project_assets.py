from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import check_final_project_assets as checker


class FinalProjectAssetsTest(unittest.TestCase):
    def test_collects_nested_asset_paths_only(self) -> None:
        data = {
            "projects": [
                {
                    "coverSrc": "assets/final-projects/p/cover.webp",
                    "media": [{"src": "assets/a.webp", "videoSrc": "assets/a.mp4"}],
                    "frames": ["assets/f1.webp"],
                    "links": [{"url": "https://example.com/"}],
                    "title": "Project",
                }
            ]
        }
        self.assertEqual(
            sorted(checker.iter_asset_paths(data)),
            ["assets/a.mp4", "assets/a.webp", "assets/f1.webp", "assets/final-projects/p/cover.webp"],
        )

    def test_reports_untracked_reference(self) -> None:
        data = {"media": [{"src": "assets/a.webp", "videoSrc": "assets/a.mp4"}]}
        tracked = {"course-site/assets/a.webp"}
        self.assertEqual(checker.find_missing(data, tracked), ["assets/a.mp4"])

    def test_repository_data_has_no_untracked_assets(self) -> None:
        data = checker.load_data(checker.DATA_FILE)
        missing = checker.find_missing(data, checker.tracked_files(ROOT))
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
