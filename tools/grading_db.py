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
        update_submission_checkbox,
    )
"""
from __future__ import annotations

import json
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
_RECURSIVE_CONTAINERS = (
    "quote", "toggle", "callout", "column_list", "column",
    "bulleted_list_item", "numbered_list_item", "synced_block",
)


def detect_submission(blocks: list[dict], token: str | None = None) -> bool:
    """Determine if a list of blocks constitutes a submission.

    Returns True if there is at least one meaningful content block
    (image, file, embed, or non-placeholder text). Recurses into
    container blocks (quote, toggle, callout, column) when they have
    children, since students often upload assignments inside these.
    """
    for block in blocks:
        btype = block.get("type", "")

        # Image or file = definitely submitted
        if btype in ("image", "file", "video", "embed", "pdf"):
            return True

        # Text blocks — check if it's a placeholder
        if btype in ("paragraph", "quote", "callout", "bulleted_list_item", "numbered_list_item"):
            rich_text = block.get(btype, {}).get("rich_text", [])
            text = extract_text(rich_text).strip()
            if text and text not in PLACEHOLDERS:
                return True

        # Recurse into containers that may hold submission content
        if block.get("has_children") and btype in _RECURSIVE_CONTAINERS:
            block_id = block.get("id")
            if block_id:
                children = _get_page_blocks(block_id, token=token)
                if detect_submission(children, token=token):
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

    Returns list of dicts: {student_name, student_id, class_num, week, submitted, notion_page_id}
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
