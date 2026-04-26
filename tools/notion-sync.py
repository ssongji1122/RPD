#!/usr/bin/env python3
"""
notion-sync.py — Notion snapshot fetcher
========================================
기본 동작은 Notion 내용을 읽어서 `curriculum-notion.json` 스냅샷만 갱신합니다.
옵션으로 Notion 스냅샷 + overrides를 canonical curriculum(`weeks/site-data.json`)에 반영할 수 있습니다.

Usage:
    python3 tools/notion-sync.py              # Fetch Notion → curriculum-notion.json
    python3 tools/notion-sync.py --fetch-only # Same as default, kept for CI/backward compatibility
    python3 tools/notion-sync.py --apply      # Fetch Notion → canonical + generated outputs 갱신

Exit codes:
    0: success, changes detected
    1: error
    2: success, no changes
"""

from __future__ import annotations

import argparse
import json
import subprocess
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
    parser.add_argument(
        "--apply",
        action="store_true",
        help="After fetching, merge curriculum-notion.json + overrides.json into canonical/generated outputs.",
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

    if args.apply:
        command = [sys.executable, str(ROOT / "tools" / "content_pipeline.py"), "sync-from-notion", "--write"]
        completed = subprocess.run(command, cwd=ROOT)
        if completed.returncode != 0:
            return completed.returncode

    if new_content != old_content:
        if args.apply:
            print(f"\nDone — snapshot updated and applied ({len(weeks)} weeks).")
        else:
            print(f"\nDone — snapshot updated ({len(weeks)} weeks).")
        return 0

    if args.apply:
        print(f"\nDone — no snapshot changes, apply completed ({len(weeks)} weeks).")
    else:
        print(f"\nDone — no snapshot changes ({len(weeks)} weeks).")
    return 2


if __name__ == "__main__":
    sys.exit(main())
