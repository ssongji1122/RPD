"""
Grading DB Helpers
==================
Stdlib-only module that wraps the Notion API for grading operations.
All grading scripts import from here.

Usage::

    from grading_db import (
        load_student_roster,
        parse_student_weeks,
        detect_submission,
        create_submissions_db,
        create_grades_db,
        add_submission_row,
        add_grade_row,
        query_submissions,
        query_grades,
        update_submission_checkbox,
        update_grade_submissions_count,
    )
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Optional

from runtime_paths import ROOT
from notion_api import NOTION_MAPPING, extract_text, get_notion_token, notion_request, _get_page_blocks

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: Korean placeholder strings that indicate an empty (not submitted) week.
PLACEHOLDERS: frozenset[str] = frozenset(
    {
        "여기에 과제를 업로드하세요",
        "여기에 중간 프로젝트를 업로드하세요",
        "여기에 최종 프로젝트를 업로드하세요",
    }
)

#: All week numbers as zero-padded strings ("01" … "15").
WEEKS: list[str] = [str(n).zfill(2) for n in range(1, 16)]

#: Path to the JSON file that persists created Notion DB IDs across runs.
GRADING_IDS_PATH: Path = ROOT / "tools" / "grading-db-ids.json"

#: Block types that always count as a submission (media / embed).
_MEDIA_TYPES: frozenset[str] = frozenset(
    {"image", "file", "video", "embed", "pdf", "column_list"}
)


# ---------------------------------------------------------------------------
# Grading DB ID persistence
# ---------------------------------------------------------------------------

def _load_grading_ids() -> dict:
    """Load persisted Notion DB IDs from ``tools/grading-db-ids.json``."""
    if not GRADING_IDS_PATH.exists():
        return {}
    with open(GRADING_IDS_PATH, encoding="utf-8") as f:
        return json.load(f)


def _save_grading_ids(data: dict) -> None:
    """Write Notion DB IDs to ``tools/grading-db-ids.json``."""
    GRADING_IDS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(GRADING_IDS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Student roster
# ---------------------------------------------------------------------------

def load_student_roster(class_num: Optional[str] = None) -> list[dict]:
    """Load students from ``notion-mapping.json`` under the ``classes`` key.

    Parameters
    ----------
    class_num : str | None
        When provided, only students from that class are returned.

    Returns
    -------
    list[dict]
        Each element has keys: ``name``, ``student_id``, ``page_id``,
        ``class_num``, ``class_title``.
    """
    if not NOTION_MAPPING.exists():
        return []

    with open(NOTION_MAPPING, encoding="utf-8") as f:
        data = json.load(f)

    classes: dict = data.get("classes", {})
    roster: list[dict] = []

    for cnum, cinfo in classes.items():
        if class_num is not None and cnum != str(class_num):
            continue
        class_title: str = cinfo.get("title", "")
        for student in cinfo.get("students", []):
            roster.append(
                {
                    "name": student.get("name", ""),
                    "student_id": student.get("student_id", ""),
                    "page_id": student.get("page_id", ""),
                    "class_num": cnum,
                    "class_title": class_title,
                }
            )

    return roster


# ---------------------------------------------------------------------------
# Week block parsing
# ---------------------------------------------------------------------------

def parse_student_weeks(blocks: list[dict]) -> dict[str, list[dict]]:
    """Parse Notion page blocks into per-week sections.

    Looks for ``heading_3`` blocks whose text matches ``Week \\d+``.  All
    subsequent blocks up to the next such heading are grouped under that
    week number (zero-padded to 2 digits).

    Parameters
    ----------
    blocks : list[dict]
        Flat list of Notion block objects (top-level).

    Returns
    -------
    dict[str, list[dict]]
        Mapping of week number string (``"01"``, ``"02"``, …) to a list of
        the blocks that belong to that week.
    """
    result: dict[str, list[dict]] = {}
    current_week: Optional[str] = None
    week_pattern = re.compile(r"Week\s+(\d+)", re.IGNORECASE)

    for block in blocks:
        btype = block.get("type", "")

        if btype == "heading_3":
            heading_text = extract_text(block["heading_3"].get("rich_text", []))
            m = week_pattern.search(heading_text)
            if m:
                current_week = str(int(m.group(1))).zfill(2)
                result.setdefault(current_week, [])
                continue  # heading itself is not added to week blocks

        if current_week is not None:
            result[current_week].append(block)

    return result


# ---------------------------------------------------------------------------
# Submission detection
# ---------------------------------------------------------------------------

def detect_submission(blocks: list[dict]) -> bool:
    """Determine whether a list of blocks constitutes a real submission.

    Returns ``True`` when:

    * Any block has a media type (image / file / video / embed / pdf /
      column_list), **or**
    * Any paragraph / heading block contains non-empty, non-placeholder text.

    Parameters
    ----------
    blocks : list[dict]
        Notion block objects for a single week section.

    Returns
    -------
    bool
    """
    for block in blocks:
        btype = block.get("type", "")

        # Media blocks always count as submission
        if btype in _MEDIA_TYPES:
            return True

        # Text blocks: extract plain text and check content
        block_data = block.get(btype, {})
        rich_text = block_data.get("rich_text", [])
        if not rich_text:
            continue

        text = extract_text(rich_text).strip()
        if text and text not in PLACEHOLDERS:
            return True

    return False


# ---------------------------------------------------------------------------
# Notion DB creation
# ---------------------------------------------------------------------------

def create_submissions_db(parent_page_id: str, token: Optional[str] = None) -> dict:
    """Create a Notion database for tracking assignment submissions.

    Schema
    ------
    - Name (title) — student name
    - student_id (rich_text)
    - class_num (select)
    - week (select)
    - submitted (checkbox)
    - page_id (rich_text)

    Parameters
    ----------
    parent_page_id : str
        Notion page that will contain this database.
    token : str | None
        Notion integration token.

    Returns
    -------
    dict
        Raw Notion API response for the created database.
    """
    token = token or get_notion_token()
    body = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "title": [{"type": "text", "text": {"content": "과제 제출 현황"}}],
        "properties": {
            "Name": {"title": {}},
            "student_id": {"rich_text": {}},
            "class_num": {
                "select": {
                    "options": [
                        {"name": "1", "color": "blue"},
                        {"name": "2", "color": "green"},
                    ]
                }
            },
            "week": {
                "select": {
                    "options": [{"name": w} for w in WEEKS]
                }
            },
            "submitted": {"checkbox": {}},
            "page_id": {"rich_text": {}},
        },
    }
    return notion_request("POST", "/databases", body, token=token)


def create_grades_db(parent_page_id: str, token: Optional[str] = None) -> dict:
    """Create a Notion database for tracking grades per student.

    Schema
    ------
    - Name (title) — student name
    - student_id (rich_text)
    - class_num (select)
    - submissions_count (number)
    - total_weeks (number)
    - page_id (rich_text)

    Parameters
    ----------
    parent_page_id : str
        Notion page that will contain this database.
    token : str | None
        Notion integration token.

    Returns
    -------
    dict
        Raw Notion API response for the created database.
    """
    token = token or get_notion_token()
    body = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "title": [{"type": "text", "text": {"content": "학생별 성적 현황"}}],
        "properties": {
            "Name": {"title": {}},
            "student_id": {"rich_text": {}},
            "class_num": {
                "select": {
                    "options": [
                        {"name": "1", "color": "blue"},
                        {"name": "2", "color": "green"},
                    ]
                }
            },
            "submissions_count": {"number": {"format": "number"}},
            "total_weeks": {"number": {"format": "number"}},
            "page_id": {"rich_text": {}},
        },
    }
    return notion_request("POST", "/databases", body, token=token)


# ---------------------------------------------------------------------------
# Row operations
# ---------------------------------------------------------------------------

def add_submission_row(
    db_id: str,
    name: str,
    student_id: str,
    class_num: str,
    week: str,
    submitted: bool,
    page_id: str,
    token: Optional[str] = None,
) -> dict:
    """Add a row to the submissions database.

    Parameters
    ----------
    db_id : str
        Notion database ID.
    name : str
        Student full name.
    student_id : str
        Student ID number string.
    class_num : str
        Class number string ("1", "2", …).
    week : str
        Zero-padded week number ("01" … "15").
    submitted : bool
        Whether the student submitted for this week.
    page_id : str
        Notion page ID of the student page (for reference).
    token : str | None
        Notion integration token.

    Returns
    -------
    dict
        Raw Notion API response.
    """
    token = token or get_notion_token()
    body = {
        "parent": {"database_id": db_id},
        "properties": {
            "Name": {"title": [{"type": "text", "text": {"content": name}}]},
            "student_id": {"rich_text": [{"type": "text", "text": {"content": student_id}}]},
            "class_num": {"select": {"name": class_num}},
            "week": {"select": {"name": week}},
            "submitted": {"checkbox": submitted},
            "page_id": {"rich_text": [{"type": "text", "text": {"content": page_id}}]},
        },
    }
    return notion_request("POST", "/pages", body, token=token)


def add_grade_row(
    db_id: str,
    name: str,
    student_id: str,
    class_num: str,
    submissions_count: int,
    total_weeks: int,
    page_id: str,
    token: Optional[str] = None,
) -> dict:
    """Add a row to the grades database.

    Parameters
    ----------
    db_id : str
        Notion database ID.
    name : str
        Student full name.
    student_id : str
        Student ID number string.
    class_num : str
        Class number string.
    submissions_count : int
        Number of weeks the student submitted work.
    total_weeks : int
        Total number of weeks in the course.
    page_id : str
        Notion page ID of the student page.
    token : str | None
        Notion integration token.

    Returns
    -------
    dict
        Raw Notion API response.
    """
    token = token or get_notion_token()
    body = {
        "parent": {"database_id": db_id},
        "properties": {
            "Name": {"title": [{"type": "text", "text": {"content": name}}]},
            "student_id": {"rich_text": [{"type": "text", "text": {"content": student_id}}]},
            "class_num": {"select": {"name": class_num}},
            "submissions_count": {"number": submissions_count},
            "total_weeks": {"number": total_weeks},
            "page_id": {"rich_text": [{"type": "text", "text": {"content": page_id}}]},
        },
    }
    return notion_request("POST", "/pages", body, token=token)


# ---------------------------------------------------------------------------
# Query helpers
# ---------------------------------------------------------------------------

def query_submissions(
    db_id: str,
    class_num: Optional[str] = None,
    week: Optional[str] = None,
    token: Optional[str] = None,
) -> list[dict]:
    """Query the submissions database with optional filters.

    Parameters
    ----------
    db_id : str
        Submissions database ID.
    class_num : str | None
        Filter to a specific class number.
    week : str | None
        Filter to a specific week (zero-padded, e.g. ``"03"``).
    token : str | None
        Notion integration token.

    Returns
    -------
    list[dict]
        List of Notion page objects matching the filter.
    """
    token = token or get_notion_token()
    filters: list[dict] = []

    if class_num is not None:
        filters.append(
            {
                "property": "class_num",
                "select": {"equals": class_num},
            }
        )
    if week is not None:
        filters.append(
            {
                "property": "week",
                "select": {"equals": week},
            }
        )

    body: dict = {}
    if len(filters) == 1:
        body["filter"] = filters[0]
    elif len(filters) > 1:
        body["filter"] = {"and": filters}

    results: list[dict] = []
    has_more = True
    cursor: Optional[str] = None

    while has_more:
        if cursor:
            body["start_cursor"] = cursor
        resp = notion_request("POST", f"/databases/{db_id}/query", body, token=token)
        results.extend(resp.get("results", []))
        has_more = resp.get("has_more", False)
        cursor = resp.get("next_cursor")

    return results


def query_grades(
    db_id: str,
    class_num: Optional[str] = None,
    token: Optional[str] = None,
) -> list[dict]:
    """Query the grades database with an optional class filter.

    Parameters
    ----------
    db_id : str
        Grades database ID.
    class_num : str | None
        Filter to a specific class number.
    token : str | None
        Notion integration token.

    Returns
    -------
    list[dict]
        List of Notion page objects.
    """
    token = token or get_notion_token()
    body: dict = {}

    if class_num is not None:
        body["filter"] = {
            "property": "class_num",
            "select": {"equals": class_num},
        }

    results: list[dict] = []
    has_more = True
    cursor: Optional[str] = None

    while has_more:
        if cursor:
            body["start_cursor"] = cursor
        resp = notion_request("POST", f"/databases/{db_id}/query", body, token=token)
        results.extend(resp.get("results", []))
        has_more = resp.get("has_more", False)
        cursor = resp.get("next_cursor")

    return results


# ---------------------------------------------------------------------------
# Update helpers
# ---------------------------------------------------------------------------

def update_submission_checkbox(
    page_id: str,
    submitted: bool,
    token: Optional[str] = None,
) -> dict:
    """Update the ``submitted`` checkbox on a submissions DB row.

    Parameters
    ----------
    page_id : str
        Notion page ID of the submission row.
    submitted : bool
        New checkbox value.
    token : str | None
        Notion integration token.

    Returns
    -------
    dict
        Raw Notion API response.
    """
    token = token or get_notion_token()
    body = {
        "properties": {
            "submitted": {"checkbox": submitted},
        }
    }
    return notion_request("PATCH", f"/pages/{page_id}", body, token=token)


def update_grade_submissions_count(
    page_id: str,
    count: int,
    token: Optional[str] = None,
) -> dict:
    """Update the ``submissions_count`` number on a grades DB row.

    Parameters
    ----------
    page_id : str
        Notion page ID of the grade row.
    count : int
        New submissions count value.
    token : str | None
        Notion integration token.

    Returns
    -------
    dict
        Raw Notion API response.
    """
    token = token or get_notion_token()
    body = {
        "properties": {
            "submissions_count": {"number": count},
        }
    }
    return notion_request("PATCH", f"/pages/{page_id}", body, token=token)
