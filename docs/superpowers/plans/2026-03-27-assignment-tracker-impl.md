# Assignment Tracker Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an automated assignment submission tracker that scans student Notion pages, populates a grading database, and displays a dashboard on the admin site.

**Architecture:** Two Notion databases (과제 제출 DB + 학기 성적 DB) created via init script. A scan script reads student pages and updates submission status. Admin server exposes new API endpoints. Admin UI renders a heatmap dashboard.

**Tech Stack:** Python 3 (stdlib only), Notion API v2022-06-28, existing `notion_api.py` / `admin-server.py` / `runtime_paths.py` patterns, vanilla JS for admin dashboard.

---

## File Structure

| Action | File | Responsibility |
|--------|------|----------------|
| Create | `tools/grading_db.py` | Notion grading DB helpers: create DBs, query, update submissions |
| Create | `tools/init_grading_db.py` | CLI: initialize both Notion databases + populate rows |
| Create | `tools/scan_submissions.py` | CLI: scan student pages, detect submissions, update DB |
| Modify | `tools/notion-mapping.json` | Add `students` section with class/student page IDs |
| Modify | `tools/admin-server.py` | Add `/api/submissions` and `/api/grades` endpoints |
| Modify | `course-site/admin.html` | Add "과제 현황" tab with heatmap UI |
| Modify | `course-site/assets/page-admin.css` | Heatmap table styles |
| Create | `tests/test_grading_db.py` | Unit tests for grading DB helpers |
| Create | `tests/test_scan_submissions.py` | Unit tests for submission detection logic |

---

### Task 1: Add Student Roster to notion-mapping.json

**Files:**
- Modify: `tools/notion-mapping.json`

This task captures the known student page IDs so all scripts can reference them without hardcoding.

- [ ] **Step 1: Update notion-mapping.json with student data**

Add a `students` section to the existing JSON. The page IDs come from the Notion pages we already fetched.

```json
{
  "_comment": "Week number → Notion page ID mapping. Parent page: 03 주차별 강의자료 원본",
  "_parent_page_id": "31d54d6549718101af08ea5812e54677",
  "_students_parent_id": "31c54d6549718107a864f0dc8d16c45c",
  "weeks": { ... },
  "classes": {
    "1": {
      "page_id": "31354d654971814e958ae58303ae8429",
      "title": "1반 (DET3012-001)",
      "students": [
        {"name": "김민서", "student_id": "12243798", "page_id": "31354d65497181d4af1edab059bdcb7d"},
        {"name": "박종민", "student_id": "12234027", "page_id": "31354d65497181339222da6ccd09a6f1"},
        {"name": "신건우", "student_id": "12234032", "page_id": "31354d654971816fb081c078877c16e1"},
        {"name": "엄다현", "student_id": "12233491", "page_id": "31354d6549718126b7dfe7ea94341c86"},
        {"name": "윤서현", "student_id": "12243814", "page_id": "31354d65497181a39a60c2667c438b15"},
        {"name": "이정민", "student_id": "12253488", "page_id": "31354d6549718103b41dcffcab89f8ab"},
        {"name": "이지연", "student_id": "12253489", "page_id": "31354d654971814ca4b0e20280241e8a"},
        {"name": "이채원", "student_id": "12253491", "page_id": "31354d65497181ecaa1afb011a2ee344"},
        {"name": "이태윤", "student_id": "12243082", "page_id": "31354d6549718108944eeb225f65c77f"},
        {"name": "전영훈", "student_id": "12223678", "page_id": "31354d6549718187b0e1d3d00e9d0724"},
        {"name": "제이현", "student_id": "12253494", "page_id": "31354d65497181f0b602ff02dadfd22b"},
        {"name": "조수연", "student_id": "12233499", "page_id": "31354d65497181a1b875e2803614e51e"},
        {"name": "최지율", "student_id": "12214335", "page_id": "31354d65497181029e06db4aa3199b52"},
        {"name": "황은하", "student_id": "12253506", "page_id": "31354d654971816fb081c078877c16e1"}
      ]
    },
    "2": {
      "page_id": "31354d65497181359b62eea0cbe2b0a4",
      "title": "2반 (DET3012-002)",
      "students": [
        {"name": "김민하", "student_id": "12243800", "page_id": "31354d654971811b9326d137769b06ea"},
        {"name": "김성호", "student_id": "12212953", "page_id": "31354d65497181118d60da6149648e35"},
        {"name": "김채원", "student_id": "12242406", "page_id": "31354d6549718174ad23ee49b10dc73a"},
        {"name": "박채린", "student_id": "12243805", "page_id": "31354d6549718152866ec1038ca8c070"},
        {"name": "유다현", "student_id": "12242749", "page_id": "31354d654971818a968ad1df0cb1cd46"},
        {"name": "이가남", "student_id": "12243816", "page_id": "31354d65497181178ee4d4e5eef35704"},
        {"name": "정효린", "student_id": "12224245", "page_id": "31354d6549718179965fe34bf266d874"},
        {"name": "최은녕", "student_id": "12243828", "page_id": "31354d6549718124b9f2fcac976fe727"},
        {"name": "하상민", "student_id": "12223684", "page_id": "31354d6549718131be1afc28806b2952"},
        {"name": "하채민", "student_id": "12243831", "page_id": "31354d65497181b6ab29d55d5f31b670"},
        {"name": "한지예", "student_id": "12221708", "page_id": "31354d6549718189b746f8980d11b33c"}
      ]
    }
  }
}
```

- [ ] **Step 2: Commit**

```bash
git add tools/notion-mapping.json
git commit -m "data: add student roster to notion-mapping.json"
```

---

### Task 2: Grading DB Helpers Module

**Files:**
- Create: `tools/grading_db.py`
- Create: `tests/test_grading_db.py`

Core module that wraps Notion API for grading operations. All other scripts import from here.

- [ ] **Step 1: Write tests for student roster loading**

```python
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
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd /Users/ssongji/Developer/Workspace/RPD && python -m pytest tests/test_grading_db.py -v
```

Expected: `ModuleNotFoundError: No module named 'grading_db'`

- [ ] **Step 3: Write tests for submission detection logic**

Add to `tests/test_grading_db.py`:

```python
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
```

- [ ] **Step 4: Write tests for week section parsing**

Add to `tests/test_grading_db.py`:

```python
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
```

- [ ] **Step 5: Implement grading_db.py**

```python
# tools/grading_db.py
"""
Grading DB helpers
==================
Stdlib-only module for managing assignment submission tracking
and grade databases via the Notion API.

Usage:
    from grading_db import (
        load_student_roster,
        parse_student_weeks,
        detect_submission,
        create_submissions_db,
        create_grades_db,
        query_submissions,
        update_submission,
    )
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

from notion_api import (
    NOTION_MAPPING,
    extract_text,
    get_notion_token,
    notion_request,
    _get_page_blocks,
)
from runtime_paths import ROOT

# ---------------------------------------------------------------------------
# Known placeholders that indicate "not submitted"
# ---------------------------------------------------------------------------
PLACEHOLDERS = {
    "여기에 과제를 업로드하세요",
    "여기에 중간 프로젝트를 업로드하세요",
    "여기에 최종 프로젝트를 업로드하세요",
}

WEEKS = [f"{i:02d}" for i in range(1, 16)]

# ---------------------------------------------------------------------------
# DB ID persistence — stored alongside notion-mapping.json
# ---------------------------------------------------------------------------
GRADING_IDS_PATH = ROOT / "tools" / "grading-db-ids.json"


def _load_grading_ids() -> dict:
    if GRADING_IDS_PATH.exists():
        with open(GRADING_IDS_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save_grading_ids(data: dict) -> None:
    with open(GRADING_IDS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Student roster
# ---------------------------------------------------------------------------
def load_student_roster(class_num: str | None = None) -> list[dict]:
    """Load student roster from notion-mapping.json.

    Returns list of dicts: {name, student_id, page_id, class_num, class_title}
    """
    if not NOTION_MAPPING.exists():
        return []
    with open(NOTION_MAPPING, encoding="utf-8") as f:
        data = json.load(f)

    classes = data.get("classes", {})
    roster: list[dict] = []
    for cn, cdata in classes.items():
        if class_num and cn != class_num:
            continue
        for s in cdata.get("students", []):
            roster.append({
                "name": s["name"],
                "student_id": s["student_id"],
                "page_id": s["page_id"],
                "class_num": cn,
                "class_title": cdata.get("title", ""),
            })
    return roster


# ---------------------------------------------------------------------------
# Student page parsing
# ---------------------------------------------------------------------------
def parse_student_weeks(blocks: list[dict]) -> dict[str, list[dict]]:
    """Parse a student page's blocks into week-keyed sections.

    Returns dict mapping week number (e.g. "01") to list of content blocks
    under that heading.
    """
    weeks: dict[str, list[dict]] = {}
    current_week: str | None = None

    for block in blocks:
        btype = block.get("type", "")

        if btype == "heading_3":
            text = extract_text(block["heading_3"].get("rich_text", []))
            m = re.match(r"(?:⭐\s*)?Week\s*(\d+)", text)
            if m:
                current_week = m.group(1).zfill(2)
                weeks[current_week] = []
                continue

        if current_week is not None:
            weeks.setdefault(current_week, []).append(block)

    return weeks


# ---------------------------------------------------------------------------
# Submission detection
# ---------------------------------------------------------------------------
def detect_submission(blocks: list[dict]) -> bool:
    """Determine if a list of blocks constitutes a submission.

    Returns True if there is at least one meaningful content block
    (image, file, embed, or non-placeholder text).
    """
    for block in blocks:
        btype = block.get("type", "")

        # Image or file = definitely submitted
        if btype in ("image", "file", "video", "embed", "pdf"):
            return True

        # Column blocks may contain images
        if btype in ("column_list", "column"):
            return True

        # Text blocks — check if it's a placeholder
        if btype in ("paragraph", "quote", "callout", "bulleted_list_item", "numbered_list_item"):
            text_key = btype
            rich_text = block.get(text_key, {}).get("rich_text", [])
            text = extract_text(rich_text).strip()
            if text and text not in PLACEHOLDERS:
                return True

    return False


# ---------------------------------------------------------------------------
# Notion DB creation
# ---------------------------------------------------------------------------
def create_submissions_db(
    parent_page_id: str, token: str | None = None
) -> str:
    """Create the 과제 제출 현황 database under the given parent page.

    Returns the database ID.
    """
    body = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "title": [{"type": "text", "text": {"content": "📊 과제 제출 현황"}}],
        "properties": {
            "학생명": {"title": {}},
            "학번": {"rich_text": {}},
            "분반": {
                "select": {
                    "options": [
                        {"name": "1반", "color": "blue"},
                        {"name": "2반", "color": "green"},
                    ]
                }
            },
            "주차": {
                "select": {
                    "options": [
                        {"name": f"Week {w}"} for w in WEEKS
                    ]
                }
            },
            "제출": {"checkbox": {}},
            "학생페이지": {"url": {}},
        },
    }
    result = notion_request("POST", "/databases", body, token=token)
    db_id = result["id"]

    ids = _load_grading_ids()
    ids["submissions_db_id"] = db_id
    _save_grading_ids(ids)

    return db_id


def create_grades_db(
    parent_page_id: str, token: str | None = None
) -> str:
    """Create the 학기 성적 종합 database under the given parent page.

    Returns the database ID.
    """
    body = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "title": [{"type": "text", "text": {"content": "📈 학기 성적 종합"}}],
        "properties": {
            "학생명": {"title": {}},
            "학번": {"rich_text": {}},
            "분반": {
                "select": {
                    "options": [
                        {"name": "1반", "color": "blue"},
                        {"name": "2반", "color": "green"},
                    ]
                }
            },
            "출석": {"number": {"format": "number"}},
            "과제제출수": {"number": {"format": "number"}},
            "중간고사": {"number": {"format": "number"}},
            "기말고사": {"number": {"format": "number"}},
            "학생페이지": {"url": {}},
        },
    }
    result = notion_request("POST", "/databases", body, token=token)
    db_id = result["id"]

    ids = _load_grading_ids()
    ids["grades_db_id"] = db_id
    _save_grading_ids(ids)

    return db_id


# ---------------------------------------------------------------------------
# Notion DB row operations
# ---------------------------------------------------------------------------
def add_submission_row(
    db_id: str,
    student: dict,
    week: str,
    submitted: bool = False,
    token: str | None = None,
) -> str:
    """Add a single submission row to the DB. Returns the page ID."""
    class_label = f"{student['class_num']}반"
    page_url = f"https://www.notion.so/{student['page_id'].replace('-', '')}"
    body = {
        "parent": {"database_id": db_id},
        "properties": {
            "학생명": {"title": [{"text": {"content": f"{student['name']} ({student['student_id']})"}}]},
            "학번": {"rich_text": [{"text": {"content": student["student_id"]}}]},
            "분반": {"select": {"name": class_label}},
            "주차": {"select": {"name": f"Week {week}"}},
            "제출": {"checkbox": submitted},
            "학생페이지": {"url": page_url},
        },
    }
    result = notion_request("POST", "/pages", body, token=token)
    return result["id"]


def add_grade_row(
    db_id: str, student: dict, token: str | None = None
) -> str:
    """Add a student row to the grades DB. Returns the page ID."""
    class_label = f"{student['class_num']}반"
    page_url = f"https://www.notion.so/{student['page_id'].replace('-', '')}"
    body = {
        "parent": {"database_id": db_id},
        "properties": {
            "학생명": {"title": [{"text": {"content": f"{student['name']} ({student['student_id']})"}}]},
            "학번": {"rich_text": [{"text": {"content": student["student_id"]}}]},
            "분반": {"select": {"name": class_label}},
            "출석": {"number": 0},
            "과제제출수": {"number": 0},
            "중간고사": {"number": 0},
            "기말고사": {"number": 0},
            "학생페이지": {"url": page_url},
        },
    }
    result = notion_request("POST", "/pages", body, token=token)
    return result["id"]


# ---------------------------------------------------------------------------
# Query helpers
# ---------------------------------------------------------------------------
def query_submissions(
    db_id: str | None = None,
    class_num: str | None = None,
    week: str | None = None,
    token: str | None = None,
) -> list[dict]:
    """Query the submissions DB with optional filters.

    Returns list of dicts: {student_name, student_id, class_num, week, submitted, page_id}
    """
    if db_id is None:
        ids = _load_grading_ids()
        db_id = ids.get("submissions_db_id")
        if not db_id:
            raise RuntimeError("Submissions DB not initialized. Run init_grading_db.py first.")

    filters = []
    if class_num:
        filters.append({
            "property": "분반",
            "select": {"equals": f"{class_num}반"},
        })
    if week:
        filters.append({
            "property": "주차",
            "select": {"equals": f"Week {week}"},
        })

    body: dict = {}
    if len(filters) == 1:
        body["filter"] = filters[0]
    elif len(filters) > 1:
        body["filter"] = {"and": filters}

    all_results: list[dict] = []
    cursor = None
    while True:
        if cursor:
            body["start_cursor"] = cursor
        result = notion_request("POST", f"/databases/{db_id}/query", body, token=token)
        for page in result.get("results", []):
            props = page.get("properties", {})
            title_rt = props.get("학생명", {}).get("title", [])
            student_name = extract_text(title_rt)
            student_id_rt = props.get("학번", {}).get("rich_text", [])
            student_id = extract_text(student_id_rt)
            class_sel = props.get("분반", {}).get("select", {})
            week_sel = props.get("주차", {}).get("select", {})
            submitted = props.get("제출", {}).get("checkbox", False)
            all_results.append({
                "notion_page_id": page["id"],
                "student_name": student_name,
                "student_id": student_id,
                "class_num": class_sel.get("name", ""),
                "week": week_sel.get("name", ""),
                "submitted": submitted,
            })
        if not result.get("has_more"):
            break
        cursor = result.get("next_cursor")

    return all_results


def update_submission_checkbox(
    page_id: str, submitted: bool, token: str | None = None
) -> None:
    """Update the 제출 checkbox on a submission row."""
    notion_request("PATCH", f"/pages/{page_id}", {
        "properties": {"제출": {"checkbox": submitted}},
    }, token=token)


def query_grades(
    db_id: str | None = None,
    class_num: str | None = None,
    token: str | None = None,
) -> list[dict]:
    """Query the grades DB. Returns list of grade dicts."""
    if db_id is None:
        ids = _load_grading_ids()
        db_id = ids.get("grades_db_id")
        if not db_id:
            raise RuntimeError("Grades DB not initialized. Run init_grading_db.py first.")

    body: dict = {}
    if class_num:
        body["filter"] = {
            "property": "분반",
            "select": {"equals": f"{class_num}반"},
        }

    all_results: list[dict] = []
    cursor = None
    while True:
        if cursor:
            body["start_cursor"] = cursor
        result = notion_request("POST", f"/databases/{db_id}/query", body, token=token)
        for page in result.get("results", []):
            props = page.get("properties", {})
            title_rt = props.get("학생명", {}).get("title", [])
            student_id_rt = props.get("학번", {}).get("rich_text", [])
            class_sel = props.get("분반", {}).get("select", {})
            all_results.append({
                "notion_page_id": page["id"],
                "student_name": extract_text(title_rt),
                "student_id": extract_text(student_id_rt),
                "class_num": class_sel.get("name", ""),
                "attendance": props.get("출석", {}).get("number", 0),
                "submissions": props.get("과제제출수", {}).get("number", 0),
                "midterm": props.get("중간고사", {}).get("number", 0),
                "final": props.get("기말고사", {}).get("number", 0),
            })
        if not result.get("has_more"):
            break
        cursor = result.get("next_cursor")

    return all_results


def update_grade_submissions_count(
    page_id: str, count: int, token: str | None = None
) -> None:
    """Update 과제제출수 on a grade row."""
    notion_request("PATCH", f"/pages/{page_id}", {
        "properties": {"과제제출수": {"number": count}},
    }, token=token)
```

- [ ] **Step 6: Run tests to verify they pass**

```bash
cd /Users/ssongji/Developer/Workspace/RPD && python -m pytest tests/test_grading_db.py -v
```

Expected: All 7 tests PASS.

- [ ] **Step 7: Commit**

```bash
git add tools/grading_db.py tests/test_grading_db.py
git commit -m "feat: add grading DB helpers module with submission detection"
```

---

### Task 3: DB Initialization Script

**Files:**
- Create: `tools/init_grading_db.py`

CLI that creates both Notion databases and populates all rows.

- [ ] **Step 1: Write init_grading_db.py**

```python
#!/usr/bin/env python3
"""
Initialize Grading Databases
=============================
Creates the 과제 제출 현황 and 학기 성적 종합 databases on Notion
and populates them with student rows.

Usage:
    NOTION_TOKEN=... python tools/init_grading_db.py

Options:
    --parent-page-id ID   Override the parent page (default: 03 학생 개인 페이지 운영)
    --dry-run             Show what would be created without calling the API
"""
from __future__ import annotations

import argparse
import sys
import time

from grading_db import (
    WEEKS,
    _load_grading_ids,
    add_grade_row,
    add_submission_row,
    create_grades_db,
    create_submissions_db,
    load_student_roster,
)
from notion_api import get_notion_token

# Parent page: 03 학생 개인 페이지 운영
DEFAULT_PARENT = "31c54d6549718107a864f0dc8d16c45c"


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize grading databases")
    parser.add_argument("--parent-page-id", default=DEFAULT_PARENT)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    token = get_notion_token()
    if not token and not args.dry_run:
        print("ERROR: NOTION_TOKEN not set", file=sys.stderr)
        return 1

    roster = load_student_roster()
    if not roster:
        print("ERROR: No students found in notion-mapping.json", file=sys.stderr)
        return 1

    print(f"Found {len(roster)} students across {len(set(s['class_num'] for s in roster))} classes")

    if args.dry_run:
        print(f"\n[DRY RUN] Would create:")
        print(f"  - 과제 제출 현황 DB: {len(roster)} students x {len(WEEKS)} weeks = {len(roster) * len(WEEKS)} rows")
        print(f"  - 학기 성적 종합 DB: {len(roster)} rows")
        return 0

    # Check if already initialized
    ids = _load_grading_ids()
    if ids.get("submissions_db_id") or ids.get("grades_db_id"):
        print("WARNING: Databases already initialized!")
        print(f"  submissions_db_id: {ids.get('submissions_db_id', 'N/A')}")
        print(f"  grades_db_id: {ids.get('grades_db_id', 'N/A')}")
        answer = input("Re-initialize? This will create NEW databases (old ones remain). [y/N] ")
        if answer.lower() != "y":
            print("Aborted.")
            return 0

    # 1. Create submissions DB
    print("\nCreating submissions database...")
    sub_db_id = create_submissions_db(args.parent_page_id, token=token)
    print(f"  Created: {sub_db_id}")

    # 2. Populate submission rows
    total = len(roster) * len(WEEKS)
    count = 0
    for student in roster:
        for week in WEEKS:
            add_submission_row(sub_db_id, student, week, submitted=False, token=token)
            count += 1
            if count % 25 == 0:
                print(f"  Submissions: {count}/{total} rows created...")
                time.sleep(0.5)  # Notion API rate limit
    print(f"  Done: {count} submission rows created")

    # 3. Create grades DB
    print("\nCreating grades database...")
    grades_db_id = create_grades_db(args.parent_page_id, token=token)
    print(f"  Created: {grades_db_id}")

    # 4. Populate grade rows
    for i, student in enumerate(roster):
        add_grade_row(grades_db_id, student, token=token)
        if (i + 1) % 10 == 0:
            time.sleep(0.3)
    print(f"  Done: {len(roster)} grade rows created")

    print(f"\nInitialization complete!")
    print(f"  Submissions DB: {sub_db_id}")
    print(f"  Grades DB: {grades_db_id}")
    print(f"  IDs saved to: tools/grading-db-ids.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Test dry-run mode**

```bash
cd /Users/ssongji/Developer/Workspace/RPD && python tools/init_grading_db.py --dry-run
```

Expected output:
```
Found 25 students across 2 classes

[DRY RUN] Would create:
  - 과제 제출 현황 DB: 25 students x 15 weeks = 375 rows
  - 학기 성적 종합 DB: 25 rows
```

- [ ] **Step 3: Commit**

```bash
git add tools/init_grading_db.py
git commit -m "feat: add grading DB initialization script"
```

---

### Task 4: Submission Scanner Script

**Files:**
- Create: `tools/scan_submissions.py`
- Create: `tests/test_scan_submissions.py`

Scans student pages and updates the submissions DB.

- [ ] **Step 1: Write test for scan orchestration**

```python
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
```

- [ ] **Step 2: Run tests**

```bash
cd /Users/ssongji/Developer/Workspace/RPD && python -m pytest tests/test_scan_submissions.py -v
```

Expected: All PASS.

- [ ] **Step 3: Write scan_submissions.py**

```python
#!/usr/bin/env python3
"""
Scan Student Submissions
========================
Reads each student's Notion page, detects which weeks have
submissions, and updates the submissions database.

Usage:
    NOTION_TOKEN=... python tools/scan_submissions.py
    NOTION_TOKEN=... python tools/scan_submissions.py --week 3
    NOTION_TOKEN=... python tools/scan_submissions.py --class 1
    NOTION_TOKEN=... python tools/scan_submissions.py --dry-run
"""
from __future__ import annotations

import argparse
import sys
import time

from grading_db import (
    detect_submission,
    load_student_roster,
    parse_student_weeks,
    query_submissions,
    update_submission_checkbox,
    update_grade_submissions_count,
    query_grades,
    _load_grading_ids,
)
from notion_api import _get_page_blocks, get_notion_token


def scan_student(student: dict, week_filter: str | None, token: str) -> dict[str, bool]:
    """Scan a student page and return {week_num: submitted} dict."""
    blocks = _get_page_blocks(student["page_id"], token=token)
    weeks = parse_student_weeks(blocks)

    results: dict[str, bool] = {}
    for week_num, week_blocks in weeks.items():
        if week_filter and week_num != week_filter:
            continue
        results[week_num] = detect_submission(week_blocks)

    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan student submissions")
    parser.add_argument("--week", type=int, help="Scan specific week only (e.g. 3)")
    parser.add_argument("--class", dest="class_num", help="Scan specific class only (1 or 2)")
    parser.add_argument("--dry-run", action="store_true", help="Show results without updating DB")
    args = parser.parse_args()

    token = get_notion_token()
    if not token:
        print("ERROR: NOTION_TOKEN not set", file=sys.stderr)
        return 1

    ids = _load_grading_ids()
    sub_db_id = ids.get("submissions_db_id")
    if not sub_db_id and not args.dry_run:
        print("ERROR: Submissions DB not initialized. Run init_grading_db.py first.", file=sys.stderr)
        return 1

    week_filter = f"{args.week:02d}" if args.week else None
    roster = load_student_roster(class_num=args.class_num)

    if not roster:
        print("No students found.", file=sys.stderr)
        return 1

    week_msg = f" for Week {week_filter}" if week_filter else ""
    print(f"Scanning {len(roster)} students{week_msg}...")

    # Scan all students
    all_results: list[dict] = []
    for i, student in enumerate(roster):
        results = scan_student(student, week_filter, token)
        for wk, submitted in results.items():
            all_results.append({
                "student": student,
                "week": wk,
                "submitted": submitted,
            })
        status_parts = []
        for w, s in sorted(results.items()):
            mark = "V" if s else "X"
            status_parts.append(f"W{w}={mark}")
        print(f"  [{i+1}/{len(roster)}] {student['name']}: {', '.join(status_parts)}")
        if (i + 1) % 5 == 0:
            time.sleep(0.3)  # Rate limit

    # Summary
    submitted_count = sum(1 for r in all_results if r["submitted"])
    total = len(all_results)
    pct = submitted_count / total * 100 if total else 0
    print(f"\nSummary: {submitted_count}/{total} submitted ({pct:.0f}%)")

    # Print not submitted
    not_submitted = [r for r in all_results if not r["submitted"]]
    if not_submitted:
        print(f"\nNot submitted ({len(not_submitted)}):")
        for r in sorted(not_submitted, key=lambda x: (x["week"], x["student"]["name"])):
            print(f"  Week {r['week']} - {r['student']['name']} ({r['student']['class_num']}ban)")

    if args.dry_run:
        print("\n[DRY RUN] No database updates made.")
        return 0

    # Update submissions DB
    print("\nUpdating submissions database...")
    existing = query_submissions(sub_db_id, token=token)

    # Build lookup: (student_id, week) -> notion_page_id
    lookup: dict[tuple[str, str], str] = {}
    for row in existing:
        sid = row["student_id"]
        week = row["week"]  # "Week 03" format
        lookup[(sid, week)] = row["notion_page_id"]

    updated = 0
    for r in all_results:
        sid = r["student"]["student_id"]
        week_label = f"Week {r['week']}"
        page_id = lookup.get((sid, week_label))
        if page_id:
            update_submission_checkbox(page_id, r["submitted"], token=token)
            updated += 1
            if updated % 25 == 0:
                time.sleep(0.3)

    print(f"  Updated {updated} rows")

    # Update grade submission counts
    grades_db_id = ids.get("grades_db_id")
    if grades_db_id:
        print("Updating grade submission counts...")
        grades = query_grades(grades_db_id, token=token)
        # Count submissions per student
        sub_counts: dict[str, int] = {}
        for r in all_results:
            sid = r["student"]["student_id"]
            if r["submitted"]:
                sub_counts[sid] = sub_counts.get(sid, 0) + 1

        for grade in grades:
            sid = grade["student_id"]
            count = sub_counts.get(sid, 0)
            if count != grade["submissions"]:
                update_grade_submissions_count(grade["notion_page_id"], count, token=token)
        print("  Done")

    print("\nScan complete!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Commit**

```bash
git add tools/scan_submissions.py tests/test_scan_submissions.py
git commit -m "feat: add submission scanner script with dry-run mode"
```

---

### Task 5: Admin Server API Endpoints

**Files:**
- Modify: `tools/admin-server.py`

Add two new API endpoints for the dashboard to consume.

- [ ] **Step 1: Add import at top of admin-server.py**

After the existing `from notion_api import ...` line, add:

```python
from grading_db import (
    query_submissions,
    query_grades,
    _load_grading_ids,
)
```

- [ ] **Step 2: Add API route handlers**

Find the route dispatch section in `admin-server.py` (the `do_GET` method) and add these handlers before the static file fallback:

```python
# --- Grading API ---
if path == "/api/submissions":
    self._require_auth()
    params = dict(urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query))
    class_num = params.get("class", [None])[0]
    week = params.get("week", [None])[0]
    try:
        data = query_submissions(class_num=class_num, week=week)
        self._json_response(data)
    except RuntimeError as e:
        self._json_error(str(e), 500)
    return

if path == "/api/grades":
    self._require_auth()
    params = dict(urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query))
    class_num = params.get("class", [None])[0]
    try:
        data = query_grades(class_num=class_num)
        self._json_response(data)
    except RuntimeError as e:
        self._json_error(str(e), 500)
    return
```

- [ ] **Step 3: Commit**

```bash
git add tools/admin-server.py
git commit -m "feat: add /api/submissions and /api/grades endpoints"
```

---

### Task 6: Admin Dashboard UI

**Files:**
- Modify: `course-site/admin.html`
- Modify: `course-site/assets/page-admin.css`

Add the "과제 현황" tab with heatmap visualization. Uses safe DOM construction (no innerHTML with untrusted data).

- [ ] **Step 1: Add the tab button in admin.html**

In the tab bar section, add a new tab button:

```html
<button class="tab-btn" data-tab="grading" aria-controls="panel-grading">과제 현황</button>
```

- [ ] **Step 2: Add the grading panel HTML**

Add the panel container (alongside existing panels):

```html
<section id="panel-grading" class="tab-panel" role="tabpanel" hidden>
  <div class="grading-controls">
    <select id="grading-class-filter" aria-label="분반 선택">
      <option value="">전체</option>
      <option value="1">1반</option>
      <option value="2">2반</option>
    </select>
    <button id="grading-refresh-btn" class="btn-secondary">새로고침</button>
  </div>
  <div class="grading-summary" id="grading-summary"></div>
  <div class="grading-heatmap-wrap">
    <table class="grading-heatmap" id="grading-heatmap">
      <thead><tr><th>학생</th></tr></thead>
      <tbody></tbody>
    </table>
  </div>
  <h3 style="margin-top:var(--space-6)">학기 성적 종합</h3>
  <div class="grading-grades-wrap">
    <table class="grading-grades" id="grading-grades">
      <thead>
        <tr>
          <th>학생</th><th>분반</th><th>출석(10%)</th>
          <th>과제(20%)</th><th>중간(35%)</th><th>기말(35%)</th>
          <th>총점</th><th>등급</th>
        </tr>
      </thead>
      <tbody></tbody>
    </table>
  </div>
</section>
```

- [ ] **Step 3: Add JavaScript for the grading panel (safe DOM construction)**

Add before the closing `</body>` tag. This script uses `document.createElement` and `textContent` instead of innerHTML to prevent XSS:

```html
<script>
(function() {
  var WEEKS = [];
  for (var i = 1; i <= 15; i++) WEEKS.push(String(i).padStart(2, '0'));

  function calcGrade(total) {
    if (total >= 95) return 'A+';
    if (total >= 90) return 'A';
    if (total >= 85) return 'B+';
    if (total >= 80) return 'B';
    if (total >= 75) return 'C+';
    if (total >= 70) return 'C';
    if (total >= 65) return 'D+';
    if (total >= 60) return 'D';
    return 'F';
  }

  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function(k) {
      if (k === 'className') node.className = attrs[k];
      else if (k === 'textContent') node.textContent = attrs[k];
      else node.setAttribute(k, attrs[k]);
    });
    if (children) children.forEach(function(c) { node.appendChild(c); });
    return node;
  }

  function clearChildren(node) {
    while (node.firstChild) node.removeChild(node.firstChild);
  }

  async function fetchJSON(url) {
    var res = await fetch(url);
    if (!res.ok) throw new Error('fetch failed');
    return res.json();
  }

  function renderHeatmap(submissions) {
    var thead = document.querySelector('#grading-heatmap thead tr');
    var tbody = document.querySelector('#grading-heatmap tbody');
    clearChildren(thead);
    clearChildren(tbody);

    // Header
    thead.appendChild(el('th', {className: 'heatmap-student', textContent: '학생'}));
    WEEKS.forEach(function(w) {
      thead.appendChild(el('th', {className: 'heatmap-week', textContent: 'W' + parseInt(w)}));
    });

    // Group by student
    var byStudent = {};
    submissions.forEach(function(s) {
      if (!byStudent[s.student_id]) byStudent[s.student_id] = {name: s.student_name, weeks: {}};
      var wn = s.week.replace('Week ', '');
      byStudent[s.student_id].weeks[wn] = s.submitted;
    });

    Object.keys(byStudent).forEach(function(sid) {
      var student = byStudent[sid];
      var cells = [el('td', {className: 'heatmap-student', textContent: student.name})];
      WEEKS.forEach(function(w) {
        var sub = student.weeks[w];
        var cls = sub === true ? 'hm-yes' : sub === false ? 'hm-no' : 'hm-na';
        cells.push(el('td', {className: cls}));
      });
      tbody.appendChild(el('tr', null, cells));
    });

    // Summary
    var total = submissions.length;
    var submitted = submissions.filter(function(s) { return s.submitted; }).length;
    var pct = total ? Math.round(submitted / total * 100) : 0;
    var summary = document.getElementById('grading-summary');
    clearChildren(summary);
    var span = el('span', {className: 'grading-stat'});
    span.textContent = 'Total: ' + pct + '% (' + submitted + '/' + total + ')';
    summary.appendChild(span);
  }

  function renderGrades(grades) {
    var tbody = document.querySelector('#grading-grades tbody');
    clearChildren(tbody);

    grades.forEach(function(g) {
      var assignPct = g.submissions / 15 * 100;
      var total = (g.attendance || 0) * 0.1 + assignPct * 0.2 + (g.midterm || 0) * 0.35 + (g.final || 0) * 0.35;
      var grade = calcGrade(total);
      var cells = [
        el('td', {textContent: g.student_name}),
        el('td', {textContent: g.class_num}),
        el('td', {textContent: String(g.attendance || 0)}),
        el('td', {textContent: g.submissions + '/15'}),
        el('td', {textContent: String(g.midterm || 0)}),
        el('td', {textContent: String(g.final || 0)}),
        el('td', null, [el('strong', {textContent: total.toFixed(1)})]),
        el('td', null, [el('strong', {textContent: grade})]),
      ];
      tbody.appendChild(el('tr', null, cells));
    });
  }

  async function loadGradingPanel() {
    var classNum = document.getElementById('grading-class-filter').value;
    var params = classNum ? '?class=' + encodeURIComponent(classNum) : '';
    try {
      var results = await Promise.all([
        fetchJSON('/api/submissions' + params),
        fetchJSON('/api/grades' + params),
      ]);
      renderHeatmap(results[0]);
      renderGrades(results[1]);
    } catch (e) {
      var summary = document.getElementById('grading-summary');
      clearChildren(summary);
      summary.appendChild(el('span', {
        className: 'grading-error',
        textContent: 'Data unavailable. Run init_grading_db.py first.',
      }));
    }
  }

  var classFilter = document.getElementById('grading-class-filter');
  if (classFilter) classFilter.addEventListener('change', loadGradingPanel);

  var refreshBtn = document.getElementById('grading-refresh-btn');
  if (refreshBtn) refreshBtn.addEventListener('click', loadGradingPanel);

  var gradingTab = document.querySelector('[data-tab="grading"]');
  if (gradingTab) gradingTab.addEventListener('click', function() {
    setTimeout(loadGradingPanel, 100);
  });
})();
</script>
```

- [ ] **Step 4: Add heatmap CSS to page-admin.css**

```css
/* --- Grading Heatmap --- */
.grading-controls {
  display: flex;
  gap: var(--space-3);
  align-items: center;
  margin-bottom: var(--space-4);
}
.grading-summary {
  margin-bottom: var(--space-4);
}
.grading-stat {
  font-size: var(--fs-body);
}
.grading-error {
  color: var(--clr-danger, #e53e3e);
}
.grading-heatmap-wrap,
.grading-grades-wrap {
  overflow-x: auto;
}
.grading-heatmap,
.grading-grades {
  border-collapse: collapse;
  font-size: var(--fs-sm);
  width: 100%;
}
.grading-heatmap th,
.grading-heatmap td,
.grading-grades th,
.grading-grades td {
  padding: var(--space-1) var(--space-2);
  border: 1px solid var(--clr-border, #e2e8f0);
  text-align: center;
  white-space: nowrap;
}
.heatmap-student {
  text-align: left !important;
  min-width: 100px;
}
.heatmap-week {
  min-width: 36px;
}
.hm-yes { background: #c6f6d5; }
.hm-no  { background: #fed7d7; }
.hm-na  { background: #edf2f7; }
```

- [ ] **Step 5: Commit**

```bash
git add course-site/admin.html course-site/assets/page-admin.css
git commit -m "feat: add grading heatmap dashboard to admin panel"
```

---

### Task 7: Add grading-db-ids.json to .gitignore

**Files:**
- Modify: `.gitignore`

The grading DB IDs file contains Notion database IDs that are environment-specific.

- [ ] **Step 1: Add to .gitignore**

```
# Grading DB IDs (environment-specific)
tools/grading-db-ids.json
```

- [ ] **Step 2: Commit**

```bash
git add .gitignore
git commit -m "chore: gitignore grading-db-ids.json"
```

---

### Task 8: Integration Test — Dry Run End-to-End

**Files:** (no new files)

Verify the full pipeline works without hitting the Notion API.

- [ ] **Step 1: Run all unit tests**

```bash
cd /Users/ssongji/Developer/Workspace/RPD && python -m pytest tests/test_grading_db.py tests/test_scan_submissions.py -v
```

Expected: All tests PASS.

- [ ] **Step 2: Test init dry-run**

```bash
cd /Users/ssongji/Developer/Workspace/RPD && python tools/init_grading_db.py --dry-run
```

Expected: Shows student count and row count without errors.

- [ ] **Step 3: Test scan help**

```bash
cd /Users/ssongji/Developer/Workspace/RPD && python tools/scan_submissions.py --help
```

Expected: Shows usage with --week, --class, --dry-run options.

---

### Task 9: Live Initialization (requires NOTION_TOKEN)

**Files:** (no new files)

Actually create the Notion databases and populate them.

- [ ] **Step 1: Initialize databases**

```bash
cd /Users/ssongji/Developer/Workspace/RPD && NOTION_TOKEN=$NOTION_TOKEN python tools/init_grading_db.py
```

Expected: Creates two databases, 375 + 25 rows, saves IDs to `tools/grading-db-ids.json`.

- [ ] **Step 2: Run first scan**

```bash
cd /Users/ssongji/Developer/Workspace/RPD && NOTION_TOKEN=$NOTION_TOKEN python tools/scan_submissions.py
```

Expected: Scans 25 students, updates submission checkboxes, updates grade counts.

- [ ] **Step 3: Verify in Notion**

Open the `03 학생 개인 페이지 운영` page in Notion and confirm:
- Submissions database exists with 375 rows
- Grades database exists with 25 rows
- Submission checkboxes reflect actual student submissions

- [ ] **Step 4: Test admin dashboard**

```bash
cd /Users/ssongji/Developer/Workspace/RPD && ADMIN_KEY=test NOTION_TOKEN=$NOTION_TOKEN python tools/admin-server.py
```

Open admin page, click the grading tab, verify heatmap renders.
