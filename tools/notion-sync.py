#!/usr/bin/env python3
"""
notion-sync.py — Notion snapshot fetcher (Notion = SoT)
=======================================================
Notion 페이지를 읽어 두 가지 산출물을 갱신합니다:

  1) `course-site/data/curriculum-notion.json` — 구조화 스냅샷
     (steps, tasks, shortcuts, mistakes, assignment, videos, docs)
  2) `course-site/data/notion-blocks/week{N}.json` — **전체 블록 트리**
     (toggle, callout, image 등 본문 그대로. 웹 미러용. --with-body=on)
  3) `course-site/assets/notion-images/week{N}/...` — Notion-hosted 이미지 캐시
     (서명 URL 만료 대비)

Usage:
    python3 tools/notion-sync.py                       # snapshot + body + images (기본)
    python3 tools/notion-sync.py --fetch-only          # legacy 호환 (기본과 동일)
    python3 tools/notion-sync.py --no-body             # snapshot만, 본문 트리 스킵
    python3 tools/notion-sync.py --apply               # snapshot을 canonical에도 반영
    python3 tools/notion-sync.py --weeks 9             # 특정 주차만

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
from notion_api import (
    download_block_assets,
    fetch_block_tree,
    fetch_notion_to_curriculum,
    get_notion_token,
    load_notion_mapping,
)

ROOT = Path(__file__).resolve().parent.parent
NOTION_JSON = ROOT / "course-site" / "data" / "curriculum-notion.json"
BLOCKS_DIR = ROOT / "course-site" / "data" / "notion-blocks"
IMAGES_DIR = ROOT / "course-site" / "assets" / "notion-images"


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


def _save_block_tree(week_num: int, page_id: str, token: str) -> int:
    """Fetch the full block tree for a week, download Notion-hosted images,
    and persist to course-site/data/notion-blocks/week{N}.json.
    Returns the number of newly downloaded asset files.
    """
    BLOCKS_DIR.mkdir(parents=True, exist_ok=True)
    week_image_dir = IMAGES_DIR / f"week{week_num:02d}"
    public_prefix = f"assets/notion-images/week{week_num:02d}"

    tree = fetch_block_tree(page_id, token=token)
    downloaded = download_block_assets(tree, week_image_dir, public_prefix)

    out_path = BLOCKS_DIR / f"week{week_num:02d}.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(
            {"week": week_num, "page_id": page_id, "blocks": tree},
            handle,
            ensure_ascii=False,
            indent=2,
        )
        handle.write("\n")
    return downloaded


def fetch_all_weeks(token: str, *, weeks_filter: set[int] | None, with_body: bool) -> list[dict]:
    mapping = load_notion_mapping()
    if not mapping:
        raise ValueError("notion-mapping.json not found or empty")

    existing_weeks = _read_existing_weeks()
    results: list[dict] = []

    for week_str in sorted(mapping.keys(), key=lambda value: int(value)):
        week_num = int(week_str)
        if weeks_filter is not None and week_num not in weeks_filter:
            # carry over previous snapshot for this week to keep the file complete
            if week_num in existing_weeks:
                results.append(existing_weeks[week_num])
            continue

        existing_week = existing_weeks.get(week_num, {"week": week_num})
        page_id = mapping[week_str]

        try:
            week_data = fetch_notion_to_curriculum(week_num, existing_week, token)
            week_data["week"] = week_num
            results.append(week_data)
            title = week_data.get("title", "(untitled)")
            line = f"✓ Week {week_num:02d}: {title}"
            if with_body:
                downloaded = _save_block_tree(week_num, page_id, token)
                line += f" — body saved ({downloaded} new asset(s))"
            print(line)
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
    parser.add_argument(
        "--no-body",
        action="store_true",
        help="Skip the per-week full block tree mirror (notion-blocks/week{N}.json).",
    )
    parser.add_argument(
        "--weeks",
        type=int,
        nargs="+",
        metavar="N",
        help="Limit to specific weeks (others keep their existing snapshot).",
    )
    args = parser.parse_args()
    if args.fetch_only:
        print("→ --fetch-only is now the default behaviour.")

    token = get_notion_token()
    if not token:
        print("Error: NOTION_TOKEN environment variable not set", file=sys.stderr)
        return 1

    old_content = _file_content(NOTION_JSON)
    weeks_filter = set(args.weeks) if args.weeks else None
    with_body = not args.no_body

    try:
        weeks = fetch_all_weeks(token, weeks_filter=weeks_filter, with_body=with_body)
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
