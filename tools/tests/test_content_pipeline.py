from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import content_pipeline


class ContentPipelineTest(unittest.TestCase):
    def test_contract_schema_defines_required_contracts(self) -> None:
        contracts_path = ROOT / "weeks" / "contracts.schema.json"
        contracts = json.loads(contracts_path.read_text(encoding="utf-8"))
        defs = contracts.get("$defs", {})

        for required in (
            "CurriculumWeek",
            "CurriculumStep",
            "Assignment",
            "Resource",
            "ShowMeRef",
            "StudentProgress",
            "PublishResult",
        ):
            self.assertIn(required, defs)

    def test_repo_curriculum_is_valid(self) -> None:
        data = content_pipeline.load_canonical_curriculum()
        errors = content_pipeline.validate_curriculum(data)
        self.assertEqual(errors, [])

    def test_compute_curriculum_diff_reports_changed_week(self) -> None:
        current = content_pipeline.load_canonical_curriculum()
        candidate = json.loads(json.dumps(current, ensure_ascii=False))
        candidate[0]["title"] = candidate[0]["title"] + " (updated)"

        diff = content_pipeline.compute_curriculum_diff(current, candidate)

        self.assertEqual(diff["changed_count"], 1)
        self.assertEqual(diff["changed_weeks"][0]["week"], candidate[0]["week"])
        self.assertIn("title", diff["changed_weeks"][0]["changed_fields"])

    def test_public_build_excludes_private_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "public-site"
            build_info = content_pipeline.build_public_site(output_dir)

            self.assertTrue((output_dir / "index.html").exists())
            self.assertTrue((output_dir / "data" / "public-build.json").exists())
            self.assertEqual(build_info["weeks"], len(content_pipeline.load_canonical_curriculum()))
            self.assertFalse((output_dir / "CONTENT_GUIDE.md").exists())
            self.assertFalse((output_dir / "admin.html").exists())
            self.assertFalse((output_dir / "data" / "curriculum-notion.json").exists())
            self.assertFalse((output_dir / "data" / "notion-config.json").exists())
            self.assertFalse((output_dir / "data" / "overrides.json").exists())
            self.assertFalse((output_dir / "data" / "students.js").exists())
            self.assertFalse((output_dir / "data" / "students.json").exists())

    def test_public_build_matches_canonical_golden_data(self) -> None:
        canonical = content_pipeline.load_canonical_curriculum()
        expected_version = content_pipeline.content_version(canonical)

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "public-site"
            build_info = content_pipeline.build_public_site(output_dir)

            public_meta = json.loads((output_dir / "data" / "public-build.json").read_text(encoding="utf-8"))
            public_curriculum = json.loads(
                (output_dir / "data" / "curriculum.json").read_text(encoding="utf-8")
            )

            self.assertEqual(build_info["version"], expected_version)
            self.assertEqual(public_meta["version"], expected_version)
            self.assertEqual(public_meta["weeks"], len(canonical))
            self.assertEqual(public_curriculum, canonical)

    def test_public_scan_rejects_token_marker(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            sample = output_dir / "index.html"
            sample.write_text("secret ntn_1234567890", encoding="utf-8")

            errors = content_pipeline.scan_public_artifact(output_dir)

            self.assertTrue(any("notion-token" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
