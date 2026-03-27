"""Tests for grading_db.py — pure logic functions only (no API calls)."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import mock_open, patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import grading_db


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_paragraph_block(text: str) -> dict:
    return {
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"plain_text": text, "type": "text", "text": {"content": text}}]
        },
    }


def _make_image_block() -> dict:
    return {"type": "image", "image": {"type": "external", "external": {"url": "https://example.com/img.png"}}}


def _make_file_block() -> dict:
    return {"type": "file", "file": {"type": "external", "external": {"url": "https://example.com/file.zip"}}}


def _make_h3_block(text: str) -> dict:
    return {
        "type": "heading_3",
        "heading_3": {
            "rich_text": [{"plain_text": text, "type": "text", "text": {"content": text}}]
        },
    }


# ---------------------------------------------------------------------------
# Student roster tests
# ---------------------------------------------------------------------------

MOCK_MAPPING = {
    "classes": {
        "1": {
            "title": "1반 (DET3012-001)",
            "students": [
                {"name": "홍길동", "student_id": "12345678", "page_id": "page-aaa"},
                {"name": "이순신", "student_id": "87654321", "page_id": "page-bbb"},
            ],
        },
        "2": {
            "title": "2반 (DET3012-002)",
            "students": [
                {"name": "강감찬", "student_id": "11111111", "page_id": "page-ccc"},
            ],
        },
    }
}


def _make_fake_mapping_path(exists: bool):
    """Return a fake Path-like object for mocking NOTION_MAPPING."""

    class _FakePath:
        def exists(self_):  # noqa: N805
            return exists

        def __str__(self_):  # noqa: N805
            return "fake-notion-mapping.json"

    return _FakePath()


class TestLoadStudentRoster(unittest.TestCase):
    def test_load_student_roster(self):
        mapping_json = json.dumps(MOCK_MAPPING, ensure_ascii=False)
        fake_path = _make_fake_mapping_path(exists=True)
        m = mock_open(read_data=mapping_json)
        with patch("builtins.open", m):
            with patch.object(grading_db, "NOTION_MAPPING", fake_path):
                result = grading_db.load_student_roster()

        self.assertEqual(len(result), 3)
        names = [s["name"] for s in result]
        self.assertIn("홍길동", names)
        self.assertIn("이순신", names)
        self.assertIn("강감찬", names)

        # Check dict shape
        first = next(s for s in result if s["name"] == "홍길동")
        self.assertEqual(first["student_id"], "12345678")
        self.assertEqual(first["page_id"], "page-aaa")
        self.assertEqual(first["class_num"], "1")
        self.assertEqual(first["class_title"], "1반 (DET3012-001)")

    def test_load_student_roster_filters_by_class(self):
        mapping_json = json.dumps(MOCK_MAPPING, ensure_ascii=False)
        fake_path = _make_fake_mapping_path(exists=True)
        m = mock_open(read_data=mapping_json)
        with patch("builtins.open", m):
            with patch.object(grading_db, "NOTION_MAPPING", fake_path):
                result = grading_db.load_student_roster(class_num="1")

        self.assertEqual(len(result), 2)
        for s in result:
            self.assertEqual(s["class_num"], "1")

    def test_load_student_roster_returns_empty_when_no_file(self):
        fake_path = _make_fake_mapping_path(exists=False)
        with patch.object(grading_db, "NOTION_MAPPING", fake_path):
            result = grading_db.load_student_roster()
        self.assertEqual(result, [])


# ---------------------------------------------------------------------------
# detect_submission tests
# ---------------------------------------------------------------------------

class TestDetectSubmission(unittest.TestCase):
    def test_detect_submission_empty_blocks(self):
        """Empty list of blocks → no submission."""
        self.assertFalse(grading_db.detect_submission([]))

    def test_detect_submission_empty(self):
        """Blocks containing only placeholder text → no submission."""
        blocks = [_make_paragraph_block("여기에 과제를 업로드하세요")]
        self.assertFalse(grading_db.detect_submission(blocks))

    def test_detect_submission_placeholder_midterm(self):
        blocks = [_make_paragraph_block("여기에 중간 프로젝트를 업로드하세요")]
        self.assertFalse(grading_db.detect_submission(blocks))

    def test_detect_submission_placeholder_final(self):
        blocks = [_make_paragraph_block("여기에 최종 프로젝트를 업로드하세요")]
        self.assertFalse(grading_db.detect_submission(blocks))

    def test_detect_submission_with_image(self):
        """An image block counts as a submission."""
        blocks = [_make_image_block()]
        self.assertTrue(grading_db.detect_submission(blocks))

    def test_detect_submission_with_file(self):
        """A file block counts as a submission."""
        blocks = [_make_file_block()]
        self.assertTrue(grading_db.detect_submission(blocks))

    def test_detect_submission_with_video(self):
        block = {"type": "video", "video": {}}
        self.assertTrue(grading_db.detect_submission([block]))

    def test_detect_submission_with_embed(self):
        block = {"type": "embed", "embed": {"url": "https://example.com"}}
        self.assertTrue(grading_db.detect_submission([block]))

    def test_detect_submission_with_pdf(self):
        block = {"type": "pdf", "pdf": {}}
        self.assertTrue(grading_db.detect_submission([block]))

    def test_detect_submission_with_column_list(self):
        block = {"type": "column_list", "column_list": {}}
        self.assertTrue(grading_db.detect_submission([block]))

    def test_detect_submission_with_text(self):
        """Non-placeholder paragraph text counts as submission."""
        blocks = [_make_paragraph_block("My project is complete.")]
        self.assertTrue(grading_db.detect_submission(blocks))

    def test_detect_submission_empty_rich_text(self):
        """A paragraph with empty rich_text is not a submission."""
        block = {"type": "paragraph", "paragraph": {"rich_text": []}}
        self.assertFalse(grading_db.detect_submission([block]))

    def test_detect_submission_placeholder_with_extra_spaces(self):
        """Placeholder match is exact; extra spaces → treated as real content."""
        blocks = [_make_paragraph_block(" 여기에 과제를 업로드하세요 ")]
        # Trimmed match: the implementation should strip before checking
        # This documents the expected behavior (trimmed comparison)
        result = grading_db.detect_submission(blocks)
        # Trimmed placeholder still recognized as placeholder → False
        self.assertFalse(result)


# ---------------------------------------------------------------------------
# parse_student_weeks tests
# ---------------------------------------------------------------------------

class TestParseStudentWeeks(unittest.TestCase):
    def test_parse_student_weeks_basic(self):
        """h3 heading 'Week 01' groups subsequent blocks."""
        blocks = [
            _make_h3_block("Week 01"),
            _make_paragraph_block("First paragraph"),
            _make_image_block(),
            _make_h3_block("Week 02"),
            _make_paragraph_block("Second paragraph"),
        ]
        result = grading_db.parse_student_weeks(blocks)

        self.assertIn("01", result)
        self.assertIn("02", result)
        self.assertEqual(len(result["01"]), 2)  # paragraph + image
        self.assertEqual(len(result["02"]), 1)  # paragraph

    def test_parse_student_weeks_zero_padded(self):
        """Week numbers should be zero-padded to 2 digits."""
        blocks = [
            _make_h3_block("Week 3"),
            _make_paragraph_block("Content"),
        ]
        result = grading_db.parse_student_weeks(blocks)
        self.assertIn("03", result)

    def test_parse_student_weeks_no_headings(self):
        """No Week headings → empty dict."""
        blocks = [_make_paragraph_block("Some text")]
        result = grading_db.parse_student_weeks(blocks)
        self.assertEqual(result, {})

    def test_parse_student_weeks_ignores_non_week_h3(self):
        """h3 headings not matching 'Week \\d+' are not treated as week markers."""
        blocks = [
            _make_h3_block("소개"),
            _make_paragraph_block("Intro text"),
            _make_h3_block("Week 01"),
            _make_paragraph_block("Week content"),
        ]
        result = grading_db.parse_student_weeks(blocks)
        self.assertEqual(list(result.keys()), ["01"])
        self.assertEqual(len(result["01"]), 1)

    def test_parse_student_weeks_empty_week(self):
        """A week heading with no subsequent blocks has an empty list."""
        blocks = [
            _make_h3_block("Week 05"),
        ]
        result = grading_db.parse_student_weeks(blocks)
        self.assertIn("05", result)
        self.assertEqual(result["05"], [])


if __name__ == "__main__":
    unittest.main()
