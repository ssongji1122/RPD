#!/usr/bin/env python3
"""
curriculum-push.py — curriculum.js → Notion 단방향 push
=========================================================
Usage:
    python3 tools/curriculum-push.py              # 전체 15주
    python3 tools/curriculum-push.py --week 3     # Week 3만
    python3 tools/curriculum-push.py --weeks 1 2 3  # 복수 주차

Exit codes:
    0: 성공 (1개 이상 push)
    1: 에러
    2: push할 주차 없음
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from notion_api import get_notion_token, load_notion_mapping, sync_week_to_notion

ROOT = Path(__file__).resolve().parent.parent
CURRICULUM_JS = ROOT / "course-site" / "data" / "curriculum.js"


def load_curriculum() -> list[dict]:
    text = CURRICULUM_JS.read_text(encoding="utf-8")
    match = re.search(r"const CURRICULUM\s*=\s*(\[.*?\])\s*;", text, re.DOTALL)
    if not match:
        raise ValueError("curriculum.js에서 CURRICULUM 배열을 찾을 수 없음")
    return json.loads(match.group(1))


def push_weeks(weeks: list[dict], token: str) -> tuple[int, int]:
    mapping = load_notion_mapping()
    ok = 0
    fail = 0
    for week in weeks:
        week_num = str(week.get("week", ""))
        if week_num not in mapping:
            print(f"⚠ Week {week_num}: notion-mapping.json에 매핑 없음, 건너뜀")
            continue
        try:
            sync_week_to_notion(week, token)
            title = week.get("title", "(untitled)")
            print(f"✓ Week {week_num.zfill(2)}: {title}")
            ok += 1
        except Exception as exc:
            print(f"✗ Week {week_num}: {exc}", file=sys.stderr)
            fail += 1
    return ok, fail


def main() -> int:
    parser = argparse.ArgumentParser(description="curriculum.js → Notion push")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--week", type=int, metavar="N", help="특정 주차만 push")
    group.add_argument("--weeks", type=int, nargs="+", metavar="N", help="복수 주차 push")
    args = parser.parse_args()

    token = get_notion_token()
    if not token:
        print("Error: NOTION_TOKEN 환경변수가 설정되지 않음", file=sys.stderr)
        return 1

    try:
        all_weeks = load_curriculum()
    except Exception as exc:
        print(f"Error: curriculum.js 읽기 실패 — {exc}", file=sys.stderr)
        return 1

    if args.week is not None:
        target_nums = {args.week}
    elif args.weeks is not None:
        target_nums = set(args.weeks)
    else:
        target_nums = None

    if target_nums is not None:
        weeks_to_push = [w for w in all_weeks if w.get("week") in target_nums]
        missing = target_nums - {w.get("week") for w in weeks_to_push}
        for n in sorted(missing):
            print(f"⚠ Week {n}: curriculum.js에 없음", file=sys.stderr)
    else:
        weeks_to_push = all_weeks

    if not weeks_to_push:
        print("push할 주차가 없습니다.", file=sys.stderr)
        return 2

    print(f"Pushing {len(weeks_to_push)} week(s) to Notion...")
    ok, fail = push_weeks(weeks_to_push, token)
    print(f"\nDone — {ok} succeeded, {fail} failed.")
    return 0 if ok > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
