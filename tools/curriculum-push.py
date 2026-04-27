#!/usr/bin/env python3
"""
curriculum-push.py — canonical curriculum → Notion 단방향 push (DEPRECATED)
==========================================================================
⚠️  Notion이 SoT(Source of Truth)로 결정된 이후(2026-04-06) 이 스크립트의
    파괴적 동작(delete_all_blocks → 단순 구조 재작성)은 금지됩니다.

기본 동작은 **dry-run**: 무엇이 바뀔지만 출력하고 실제 push는 하지 않습니다.
실제 push가 정말 필요한 경우에만 `--confirm-destructive` 플래그를 명시.

Usage:
    python3 tools/curriculum-push.py                                    # dry-run (안전)
    python3 tools/curriculum-push.py --week 3                           # week 3 dry-run
    python3 tools/curriculum-push.py --week 3 --confirm-destructive     # 실제 push (위험)

Exit codes:
    0: 성공 (1개 이상 push) 또는 dry-run 정상 종료
    1: 에러
    2: push할 주차 없음
    3: 안전장치에 의해 차단됨 (--confirm-destructive 누락)
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from content_pipeline import content_version, load_canonical_curriculum
from notion_api import get_notion_token, load_notion_mapping, sync_week_to_notion

ROOT = Path(__file__).resolve().parent.parent


def load_curriculum() -> list[dict]:
    return load_canonical_curriculum()


def push_weeks(weeks: list[dict], token: str, *, dry_run: bool) -> tuple[int, int]:
    mapping = load_notion_mapping()
    ok = 0
    fail = 0
    for week in weeks:
        week_num = str(week.get("week", ""))
        if week_num not in mapping:
            print(f"⚠ Week {week_num}: notion-mapping.json에 매핑 없음, 건너뜀")
            continue
        title = week.get("title", "(untitled)")
        if dry_run:
            print(f"[dry-run] Week {week_num.zfill(2)}: would DELETE all blocks and rewrite — {title}")
            ok += 1
            continue
        try:
            sync_week_to_notion(week, token)
            print(f"✓ Week {week_num.zfill(2)}: {title}")
            ok += 1
        except Exception as exc:
            print(f"✗ Week {week_num}: {exc}", file=sys.stderr)
            fail += 1
    return ok, fail


def main() -> int:
    parser = argparse.ArgumentParser(
        description="weeks/site-data.json → Notion push (DEPRECATED — Notion is SoT)"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--week", type=int, metavar="N", help="특정 주차만 push")
    group.add_argument("--weeks", type=int, nargs="+", metavar="N", help="복수 주차 push")
    parser.add_argument(
        "--confirm-destructive",
        action="store_true",
        help="실제 push를 수행 (각 페이지의 모든 블록을 삭제 후 단순 구조로 재작성). "
             "이 플래그 없으면 dry-run.",
    )
    args = parser.parse_args()

    token = get_notion_token()
    if not token and args.confirm_destructive:
        print("Error: NOTION_TOKEN 환경변수가 설정되지 않음", file=sys.stderr)
        return 1

    try:
        all_weeks = load_curriculum()
    except Exception as exc:
        print(f"Error: canonical curriculum 읽기 실패 — {exc}", file=sys.stderr)
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
            print(f"⚠ Week {n}: canonical curriculum에 없음", file=sys.stderr)
    else:
        weeks_to_push = all_weeks

    if not weeks_to_push:
        print("push할 주차가 없습니다.", file=sys.stderr)
        return 2

    dry_run = not args.confirm_destructive
    if dry_run:
        print("=" * 70, file=sys.stderr)
        print("⚠️  DRY-RUN MODE — Notion이 SoT이므로 기본은 안전 모드입니다.", file=sys.stderr)
        print("    실제 push (각 페이지 전체 블록 삭제 후 재작성) 가 필요하면", file=sys.stderr)
        print("    --confirm-destructive 플래그를 명시하세요.", file=sys.stderr)
        print("=" * 70, file=sys.stderr)
    else:
        print("=" * 70, file=sys.stderr)
        print("🚨 DESTRUCTIVE PUSH — 각 Notion 페이지의 모든 블록을 삭제하고", file=sys.stderr)
        print(f"    {len(weeks_to_push)}개 주차를 단순 구조로 재작성합니다.", file=sys.stderr)
        print("=" * 70, file=sys.stderr)

    print(
        f"Processing {len(weeks_to_push)} week(s) "
        f"(source version {content_version(all_weeks)})..."
    )
    ok, fail = push_weeks(weeks_to_push, token, dry_run=dry_run)
    if dry_run:
        print(f"\n[dry-run] Done — {ok} week(s) would be pushed. Use --confirm-destructive to apply.")
    else:
        print(f"\nDone — {ok} succeeded, {fail} failed.")
    return 0 if ok > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
