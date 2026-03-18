#!/usr/bin/env python3
"""
notion-sync.py — Notion snapshot fetcher
========================================
Repo-first 운영을 위해 Notion은 읽기 전용 스냅샷으로만 유지합니다.
공개 사이트와 canonical curriculum(`weeks/site-data.json`)은 이 스크립트가 직접 갱신하지 않습니다.

Usage:
    python3 tools/notion-sync.py              # Fetch Notion → curriculum-notion.json
    python3 tools/notion-sync.py --fetch-only # Same as default, kept for CI/backward compatibility

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

sys.path.insert(0, str(Path(__file__).parent))
from notion_api import fetch_notion_to_curriculum, get_notion_token, load_notion_mapping

ROOT = Path(__file__).resolve().parent.parent
NOTION_JSON = ROOT / "course-site" / "data" / "curriculum-notion.json"


def _read_existing_weeks() -> dict[int, dict]:
    if not NOTION_JSON.exists():
        return {}
    try:
        with open(NOTION_JSON, encoding="utf-8") as handle:
            payload = json.load(handle)
    except (json.JSONDecodeError, OSError, TypeError):
        return {}

    existing: dict[int, dict] = {}
    if isinstance(payload, list):
        for week in payload:
            if isinstance(week, dict):
                existing[int(week.get("week", 0) or 0)] = week
    return existing


def _write_json(path: Path, data: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def _file_content(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def fetch_all_weeks(token: str) -> list[dict]:
    mapping = load_notion_mapping()
    if not mapping:
        raise ValueError("notion-mapping.json not found or empty")

    existing_weeks = _read_existing_weeks()
    results: list[dict] = []

    for week_str in sorted(mapping.keys(), key=lambda value: int(value)):
        week_num = int(week_str)
        existing_week = existing_weeks.get(week_num, {"week": week_num})

        try:
            week_data = fetch_notion_to_curriculum(week_num, existing_week, token)
            week_data["week"] = week_num
            results.append(week_data)
            title = week_data.get("title", "(untitled)")
            print(f"✓ Week {week_num:02d}: {title}")
        except Exception as exc:
            print(f"✗ Week {week_num:02d}: {exc}", file=sys.stderr)
            results.append(existing_week)

    results.sort(key=lambda week: week.get("week", 0))
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch Notion snapshot into curriculum-notion.json")
    parser.add_argument(
        "--fetch-only",
        action="store_true",
        help="Deprecated compatibility flag. Snapshot fetch is the default behaviour.",
    )
    args = parser.parse_args()
    if args.fetch_only:
        print("→ --fetch-only is now the default behaviour.")

    token = get_notion_token()
    if not token:
        print("Error: NOTION_TOKEN environment variable not set", file=sys.stderr)
        return 1

    old_content = _file_content(NOTION_JSON)

    try:
        weeks = fetch_all_weeks(token)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if not weeks:
        print("Error: No weeks fetched", file=sys.stderr)
        return 1

    _write_json(NOTION_JSON, weeks)
    new_content = _file_content(NOTION_JSON)

    if new_content != old_content:
        print(f"\nDone — snapshot updated ({len(weeks)} weeks).")
        return 0

    print(f"\nDone — no snapshot changes ({len(weeks)} weeks).")
    return 2


if __name__ == "__main__":
    sys.exit(main())
