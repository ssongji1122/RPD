#!/usr/bin/env python3
"""
notion-sync.py — Notion → curriculum.js 자동 동기화
====================================================
Usage:
    python3 tools/notion-sync.py              # Full sync (fetch + merge)
    python3 tools/notion-sync.py --fetch-only # Fetch only (update curriculum-notion.json)
    python3 tools/notion-sync.py --merge-only # Merge only (notion + overrides → curriculum.js)

Exit codes:
    0: success, changes detected
    1: error
    2: success, no changes
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Import shared Notion API helpers
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).parent))
from notion_api import (
    fetch_notion_to_curriculum, get_notion_token, load_notion_mapping, merge_curriculum,
)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
NOTION_JSON = ROOT / "course-site" / "data" / "curriculum-notion.json"
OVERRIDES_JSON = ROOT / "course-site" / "data" / "overrides.json"
CURRICULUM_JS = ROOT / "course-site" / "data" / "curriculum.js"

# ---------------------------------------------------------------------------
# curriculum.js template
# ---------------------------------------------------------------------------
CURRICULUM_HEADER = """\
// ============================================================
// 15주 블렌더 수업 커리큘럼 데이터
// 이 파일만 수정하면 메인 페이지와 각 주차 페이지가 자동 반영됨
// ============================================================

const CURRICULUM = """

CURRICULUM_FOOTER = """\
;

// Node.js 환경 대응
if (typeof module !== "undefined") module.exports = CURRICULUM;
"""


# ---------------------------------------------------------------------------
# Fetch
# ---------------------------------------------------------------------------
def fetch_all_weeks(token: str) -> list[dict]:
    """Fetch all mapped weeks from Notion API.

    On per-week failure, the existing data for that week is preserved
    to avoid data loss on transient API errors.
    """
    mapping = load_notion_mapping()
    if not mapping:
        print("✗ notion-mapping.json not found or empty", file=sys.stderr)
        return []

    # Load existing curriculum-notion.json if available
    existing_weeks: dict[int, dict] = {}
    if NOTION_JSON.exists():
        try:
            with open(NOTION_JSON, encoding="utf-8") as f:
                for week in json.load(f):
                    existing_weeks[week.get("week", 0)] = week
        except (json.JSONDecodeError, TypeError):
            pass

    results: list[dict] = []

    for week_str in sorted(mapping.keys(), key=lambda x: int(x)):
        week_num = int(week_str)
        existing_week = existing_weeks.get(week_num, {"week": week_num})

        try:
            week_data = fetch_notion_to_curriculum(week_num, existing_week, token)
            week_data["week"] = week_num
            results.append(week_data)
            title = week_data.get("title", "(untitled)")
            print(f"✓ Week {week_num}: {title}")
        except Exception as exc:
            print(f"✗ Week {week_num}: {exc}", file=sys.stderr)
            # Keep existing data on failure
            results.append(existing_week)

    results.sort(key=lambda w: w.get("week", 0))
    return results


# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Write curriculum.js
# ---------------------------------------------------------------------------
def write_curriculum_js(data: list[dict]) -> None:
    """Write merged curriculum data as curriculum.js."""
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    content = CURRICULUM_HEADER + json_str + CURRICULUM_FOOTER
    CURRICULUM_JS.parent.mkdir(parents=True, exist_ok=True)
    with open(CURRICULUM_JS, "w", encoding="utf-8") as f:
        f.write(content)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _read_json(path: Path) -> list | dict | None:
    """Read a JSON file, return None on failure."""
    if not path.exists():
        return None
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, TypeError):
        return None


def _write_json(path: Path, data: list | dict) -> None:
    """Write data as formatted JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def _file_content(path: Path) -> str:
    """Return file content as string, or empty string if missing."""
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync Notion curriculum data to curriculum.js"
    )
    parser.add_argument(
        "--fetch-only",
        action="store_true",
        help="Fetch from Notion and update curriculum-notion.json only",
    )
    parser.add_argument(
        "--merge-only",
        action="store_true",
        help="Merge curriculum-notion.json + overrides.json → curriculum.js only",
    )
    args = parser.parse_args()

    if args.fetch_only and args.merge_only:
        print("Error: --fetch-only and --merge-only are mutually exclusive", file=sys.stderr)
        return 1

    any_changes = False

    # ---------------------------------------------------------------
    # Phase 1: Fetch from Notion → curriculum-notion.json
    # ---------------------------------------------------------------
    if not args.merge_only:
        token = get_notion_token()
        if not token:
            print("Error: NOTION_TOKEN environment variable not set", file=sys.stderr)
            return 1

        print("Fetching from Notion...")
        old_content = _file_content(NOTION_JSON)

        weeks = fetch_all_weeks(token)
        if not weeks:
            print("Error: No weeks fetched", file=sys.stderr)
            return 1

        _write_json(NOTION_JSON, weeks)
        new_content = _file_content(NOTION_JSON)

        if old_content != new_content:
            print(f"✓ curriculum-notion.json updated ({len(weeks)} weeks)")
            any_changes = True
        else:
            print(f"→ curriculum-notion.json unchanged ({len(weeks)} weeks)")

    # ---------------------------------------------------------------
    # Phase 2: Merge → curriculum.js
    # ---------------------------------------------------------------
    if not args.fetch_only:
        notion_data = _read_json(NOTION_JSON)
        if notion_data is None:
            print("Error: curriculum-notion.json not found or invalid", file=sys.stderr)
            return 1

        overrides = _read_json(OVERRIDES_JSON)
        if overrides is None:
            overrides = {"weeks": {}}

        old_js = _file_content(CURRICULUM_JS)

        merged = merge_curriculum(notion_data, overrides)
        write_curriculum_js(merged)

        new_js = _file_content(CURRICULUM_JS)

        if old_js != new_js:
            print(f"✓ curriculum.js updated ({len(merged)} weeks)")
            any_changes = True
        else:
            print("→ curriculum.js unchanged")

    # ---------------------------------------------------------------
    # Exit code
    # ---------------------------------------------------------------
    if any_changes:
        print("\nDone — changes detected.")
        return 0
    else:
        print("\nDone — no changes.")
        return 2


if __name__ == "__main__":
    sys.exit(main())
