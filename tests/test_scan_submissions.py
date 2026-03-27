# tests/test_scan_submissions.py
"""Tests for scan_submissions module."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))


def test_scan_single_student():
    """Scan one student page and detect submissions."""
    from grading_db import parse_student_weeks, detect_submission

    # Simulate a student page with Week 01 submitted and Week 02 not
    blocks = [
        {"type": "heading_3", "heading_3": {"rich_text": [{"plain_text": "Week 01: 무드보드"}]}},
        {"type": "image", "image": {"type": "file", "file": {"url": "https://example.com/a.png"}}},
        {"type": "heading_3", "heading_3": {"rich_text": [{"plain_text": "Week 02: Blender 기초 + MCP"}]}},
        {"type": "quote", "quote": {"rich_text": [{"plain_text": "여기에 과제를 업로드하세요"}]}},
        {"type": "heading_3", "heading_3": {"rich_text": [{"plain_text": "Week 03: 기초 모델링 1"}]}},
        {"type": "column_list", "column_list": {}},
    ]
    weeks = parse_student_weeks(blocks)
    assert detect_submission(weeks["01"]) is True
    assert detect_submission(weeks["02"]) is False
    assert detect_submission(weeks["03"]) is True


def test_scan_midterm_placeholder():
    """Midterm/final placeholders are also detected."""
    from grading_db import parse_student_weeks, detect_submission

    blocks = [
        {"type": "heading_3", "heading_3": {"rich_text": [{"plain_text": "⭐ Week 08: 중간고사"}]}},
        {"type": "quote", "quote": {"rich_text": [{"plain_text": "여기에 중간 프로젝트를 업로드하세요"}]}},
    ]
    weeks = parse_student_weeks(blocks)
    assert detect_submission(weeks["08"]) is False
