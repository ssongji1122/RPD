#!/usr/bin/env python3
"""
Submission Reminder
===================
해당 반의 현재 주차 제출 여부를 스캔하고,
미제출 학생의 Notion 페이지에 리마인더 댓글을 게시합니다.

Usage:
    NOTION_TOKEN=... python tools/remind_submissions.py --class 1
    NOTION_TOKEN=... python tools/remind_submissions.py --class 2
    NOTION_TOKEN=... python tools/remind_submissions.py --class 1 --week 4
    NOTION_TOKEN=... python tools/remind_submissions.py --class 1 --dry-run
    NOTION_TOKEN=... python tools/remind_submissions.py --class 1 --test-page PAGE_ID
"""
from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from grading_db import (
    load_student_roster,
    parse_student_weeks,
    detect_submission,
    update_submission_checkbox,
    update_grade_submissions_count,
    query_submissions,
    query_grades,
    _load_grading_ids,
)
from notion_api import notion_request, get_notion_token, _get_page_blocks

# ---------------------------------------------------------------------------
# 학기 시작일 (Week 1 화요일 기준)
# ---------------------------------------------------------------------------
SEMESTER_START = date(2026, 3, 4)  # 2026학년도 1학기 Week 1 시작 (화요일)
TOTAL_WEEKS = 15


def current_week_num() -> int:
    """오늘 날짜 기준으로 현재 수업 주차를 계산합니다."""
    today = date.today()
    delta = (today - SEMESTER_START).days
    week = delta // 7 + 1
    return max(1, min(week, TOTAL_WEEKS))


def post_comment(page_id: str, message: str, token: str) -> None:
    """Notion 페이지에 댓글을 게시합니다."""
    notion_request("POST", "/comments", {
        "parent": {"page_id": page_id},
        "rich_text": [{"type": "text", "text": {"content": message}}],
    }, token=token)


def main() -> int:
    parser = argparse.ArgumentParser(description="미제출 학생에게 Notion 댓글 리마인더 발송")
    parser.add_argument("--class", dest="class_num", required=True, choices=["1", "2"],
                        help="분반 번호 (1 또는 2)")
    parser.add_argument("--week", type=int, help="주차 지정 (기본: 자동 계산)")
    parser.add_argument("--dry-run", action="store_true", help="댓글 미전송, 결과만 출력")
    parser.add_argument("--test-page", metavar="PAGE_ID",
                        help="학생 페이지 대신 지정한 페이지에 모든 댓글 전송 (테스트용)")
    args = parser.parse_args()

    token = get_notion_token()
    if not token:
        print("ERROR: NOTION_TOKEN이 설정되지 않았습니다.", file=sys.stderr)
        return 1

    week_num = args.week or current_week_num()
    week_str = f"{week_num:02d}"

    students = load_student_roster(class_num=args.class_num)
    if not students:
        print(f"ERROR: {args.class_num}반 학생 명단을 불러올 수 없습니다.", file=sys.stderr)
        return 1

    print(f"[{args.class_num}반] Week {week_str} 제출 현황 스캔 중... ({len(students)}명)")
    print()

    not_submitted: list[dict] = []
    submitted_count = 0

    for s in students:
        try:
            blocks = _get_page_blocks(s["page_id"], token=token)
            weeks = parse_student_weeks(blocks)
            week_blocks = weeks.get(week_str, [])
            submitted = detect_submission(week_blocks, token=token)
        except Exception as e:
            print(f"  [오류] {s['name']}: {e}", file=sys.stderr)
            continue

        status = "✅ 제출" if submitted else "❌ 미제출"
        print(f"  {s['name']}: {status}")
        if submitted:
            submitted_count += 1
        else:
            not_submitted.append(s)

    print()
    print(f"결과: {submitted_count}명 제출 / {len(not_submitted)}명 미제출")
    print()

    # ── DB 업데이트 ─────────────────────────────────────────────────
    ids = _load_grading_ids()
    submissions_db_id = ids.get("submissions_db_id")
    grades_db_id = ids.get("grades_db_id")

    if submissions_db_id:
        try:
            rows = query_submissions(db_id=submissions_db_id,
                                     class_num=args.class_num,
                                     week=week_str,
                                     token=token)
            name_to_row = {r["student_name"].split(" (")[0]: r for r in rows}
            for s in students:
                row = name_to_row.get(s["name"])
                if row:
                    submitted = s not in not_submitted
                    if not args.dry_run:
                        update_submission_checkbox(row["notion_page_id"], submitted, token=token)
        except Exception as e:
            print(f"[경고] 제출 현황 DB 업데이트 실패: {e}", file=sys.stderr)

    if grades_db_id:
        try:
            grade_rows = query_grades(db_id=grades_db_id,
                                      class_num=args.class_num,
                                      token=token)
            name_to_grade = {r["student_name"].split(" (")[0]: r for r in grade_rows}
            for s in students:
                row = name_to_grade.get(s["name"])
                if row:
                    new_count = row["submissions"] + (1 if s not in not_submitted else 0)
                    if not args.dry_run:
                        update_grade_submissions_count(row["notion_page_id"], new_count, token=token)
        except Exception as e:
            print(f"[경고] 성적 DB 업데이트 실패: {e}", file=sys.stderr)

    # ── 리마인더 댓글 게시 ─────────────────────────────────────────
    if not not_submitted:
        print("모두 제출 완료! 리마인더가 필요하지 않습니다.")
        return 0

    message = (
        f"📌 [Week {week_num} 과제 리마인더]\n"
        f"아직 Week {week_num} 과제가 확인되지 않았어요.\n"
        f"오늘 수업 전까지 이 페이지의 Week {week_num} 섹션에 결과물을 업로드해 주세요 🙏"
    )

    print(f"댓글 리마인더 발송 ({len(not_submitted)}명):")
    errors = 0
    for s in not_submitted:
        if args.dry_run:
            print(f"  [DRY-RUN] {s['name']} → 댓글 전송 예정")
        else:
            target_page = args.test_page or s["page_id"]
            prefix = f"[테스트 → {s['name']}] " if args.test_page else ""
            test_message = prefix + message if args.test_page else message
            try:
                post_comment(target_page, test_message, token=token)
                dest = f"테스트 페이지 ({s['name']})" if args.test_page else s["name"]
                print(f"  ✅ {dest}")
            except Exception as e:
                print(f"  ❌ {s['name']}: {e}", file=sys.stderr)
                errors += 1

    if args.dry_run:
        print()
        print("(--dry-run 모드: 실제 댓글은 전송되지 않았습니다)")

    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
