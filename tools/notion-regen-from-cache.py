#!/usr/bin/env python3
"""
notion-regen-from-cache.py — Re-parse cached notion-blocks into curriculum-notion.json
======================================================================================
🔴 SSoT 경고: 이 스크립트는 **token-outage 응급용 one-off**다. 평시 워크플로우가 아니다.
   정석은 Notion(SSoT) 편집 → notion-sync.py → 웹. SSoT는 Notion이며 notion-blocks는
   Notion에서 fetch한 단방향 미러다. 이 스크립트를 평시에 쓰면 SSoT 우회를 제도화한다.
   Notion token이 살아있으면 항상 notion-sync.py를 쓸 것.

Token-free counterpart to ``notion-sync.py``. Reads the already-mirrored block trees
in ``course-site/data/notion-blocks/weekNN.json`` and re-runs ``parse_blocks_to_curriculum``
on them. Useful when:

  - The Notion API token is unavailable but the cached body is up-to-date
  - The parser was updated and you want to re-extract from the existing snapshot
  - You only want to regenerate a specific week's entry

Usage:
    python3 tools/notion-regen-from-cache.py                    # all weeks with a cache
    python3 tools/notion-regen-from-cache.py --weeks 13         # only week 13
    python3 tools/notion-regen-from-cache.py --weeks 12 13 14   # several weeks
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from notion_api import parse_blocks_to_curriculum

ROOT = Path(__file__).resolve().parent.parent
NOTION_JSON = ROOT / "course-site" / "data" / "curriculum-notion.json"
BLOCKS_DIR = ROOT / "course-site" / "data" / "notion-blocks"


def load_existing() -> dict[int, dict]:
    if not NOTION_JSON.exists():
        return {}
    with open(NOTION_JSON, encoding="utf-8") as fh:
        payload = json.load(fh)
    if not isinstance(payload, list):
        return {}
    return {int(w.get("week", 0) or 0): w for w in payload if isinstance(w, dict)}


def save_existing(weeks: dict[int, dict]) -> None:
    ordered = [weeks[k] for k in sorted(weeks.keys()) if k > 0]
    with open(NOTION_JSON, "w", encoding="utf-8") as fh:
        json.dump(ordered, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def regenerate_week(week_num: int, existing_week: dict) -> dict | None:
    cache_path = BLOCKS_DIR / f"week{week_num:02d}.json"
    if not cache_path.exists():
        print(f"✗ Week {week_num:02d}: no cache at {cache_path.relative_to(ROOT)}", file=sys.stderr)
        return None
    with open(cache_path, encoding="utf-8") as fh:
        cache = json.load(fh)
    blocks = cache.get("blocks", [])
    if not blocks:
        print(f"✗ Week {week_num:02d}: cache has no blocks", file=sys.stderr)
        return None
    # Preserve existing title (we don't re-fetch page metadata here).
    return parse_blocks_to_curriculum(blocks, week_num, existing_week, title=None)


def main() -> int:
    parser = argparse.ArgumentParser(description="Re-parse cached notion-blocks into curriculum-notion.json")
    parser.add_argument(
        "--weeks",
        type=int,
        nargs="+",
        metavar="N",
        help="Limit to specific weeks (others keep their existing entry).",
    )
    args = parser.parse_args()

    existing = load_existing()

    # Determine target weeks
    if args.weeks:
        targets = set(args.weeks)
    else:
        targets = {
            int(p.stem.removeprefix("week"))
            for p in BLOCKS_DIR.glob("week*.json")
            if p.stem.removeprefix("week").isdigit()
        }

    if not targets:
        print("No weeks to process", file=sys.stderr)
        return 1

    changed = 0
    for week_num in sorted(targets):
        existing_week = existing.get(week_num, {"week": week_num})
        regenerated = regenerate_week(week_num, existing_week)
        if regenerated is None:
            continue
        regenerated["week"] = week_num
        existing[week_num] = regenerated
        steps = len(regenerated.get("steps", []))
        tasks = sum(len(s.get("tasks", []) or []) for s in regenerated.get("steps", []))
        print(f"✓ Week {week_num:02d}: {steps} steps, {tasks} tasks")
        changed += 1

    if changed == 0:
        print("No changes written")
        return 2

    save_existing(existing)
    rel = NOTION_JSON.relative_to(ROOT)
    print(f"\n✓ Wrote {changed} week(s) to {rel}")
    print("Next: python3 tools/content_pipeline.py sync-from-notion --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
