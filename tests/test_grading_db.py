# tests/test_grading_db.py
"""Tests for grading_db module."""
import json
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add tools/ to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))


def _sample_mapping():
    return {
        "classes": {
            "1": {
                "page_id": "class1-page-id",
                "title": "1반",
                "students": [
                    {"name": "김민서", "student_id": "12243798", "page_id": "page-1"},
                    {"name": "박종민", "student_id": "12234027", "page_id": "page-2"},
                ],
            }
        }
    }


def test_load_student_roster():
    from grading_db import load_student_roster

    with patch("grading_db.NOTION_MAPPING") as mock_path:
        mock_path.exists.return_value = True
        mock_path.__str__ = lambda self: "/fake/path.json"
        with patch("builtins.open", create=True) as mock_open:
            mock_open.return_value.__enter__ = lambda s: s
            mock_open.return_value.__exit__ = MagicMock(return_value=False)
            mock_open.return_value.read = lambda: json.dumps(_sample_mapping())
            with patch("json.load", return_value=_sample_mapping()):
                roster = load_student_roster()
                assert len(roster) == 2
                assert roster[0]["name"] == "김민서"
                assert roster[0]["class_num"] == "1"


def test_load_student_roster_filters_by_class():
    from grading_db import load_student_roster

    with patch("grading_db.NOTION_MAPPING") as mock_path:
        mock_path.exists.return_value = True
        with patch("builtins.open", create=True):
            with patch("json.load", return_value=_sample_mapping()):
                roster = load_student_roster(class_num="1")
                assert len(roster) == 2
                roster_empty = load_student_roster(class_num="99")
                assert len(roster_empty) == 0


def test_detect_submission_empty():
    """Placeholder-only blocks = not submitted."""
    from grading_db import detect_submission

    blocks = [
        {"type": "quote", "quote": {"rich_text": [{"plain_text": "여기에 과제를 업로드하세요"}]}},
    ]
    assert detect_submission(blocks) is False


def test_detect_submission_with_image():
    """Image block = submitted."""
    from grading_db import detect_submission

    blocks = [
        {"type": "quote", "quote": {"rich_text": [{"plain_text": "여기에 과제를 업로드하세요"}]}},
        {"type": "image", "image": {"type": "file", "file": {"url": "https://example.com/img.png"}}},
    ]
    assert detect_submission(blocks) is True


def test_detect_submission_with_file():
    """File block = submitted."""
    from grading_db import detect_submission

    blocks = [
        {"type": "file", "file": {"type": "file", "file": {"url": "https://example.com/a.zip"}}},
    ]
    assert detect_submission(blocks) is True


def test_detect_submission_with_text():
    """Non-placeholder text = submitted."""
    from grading_db import detect_submission

    blocks = [
        {"type": "paragraph", "paragraph": {"rich_text": [{"plain_text": "스피커의 인간형 로봇화"}]}},
    ]
    assert detect_submission(blocks) is True


def test_detect_submission_empty_blocks():
    """Empty blocks only = not submitted."""
    from grading_db import detect_submission

    blocks = [
        {"type": "paragraph", "paragraph": {"rich_text": []}},
    ]
    assert detect_submission(blocks) is False


def test_parse_student_weeks():
    """Parse student page blocks into week sections."""
    from grading_db import parse_student_weeks

    blocks = [
        {"type": "table", "table": {}},  # student info table
        {"type": "heading_3", "heading_3": {"rich_text": [{"plain_text": "Week 01: 무드보드"}]}},
        {"type": "image", "image": {"type": "file", "file": {"url": "https://example.com/a.png"}}},
        {"type": "heading_3", "heading_3": {"rich_text": [{"plain_text": "Week 02: Blender 기초 + MCP"}]}},
        {"type": "quote", "quote": {"rich_text": [{"plain_text": "여기에 과제를 업로드하세요"}]}},
    ]
    weeks = parse_student_weeks(blocks)
    assert "01" in weeks
    assert "02" in weeks
    assert len(weeks["01"]) == 1  # image block
    assert len(weeks["02"]) == 1  # quote block
