#!/usr/bin/env python3
"""
Scan Student Submissions
========================
Reads each student's Notion page, detects which weeks have
submissions, and updates the submissions database.

Usage:
    NOTION_TOKEN=... python tools/scan_submissions.py
    NOTION_TOKEN=... python tools/scan_submissions.py --week 3
    NOTION_TOKEN=... python tools/scan_submissions.py --class 1
    NOTION_TOKEN=... python tools/scan_submissions.py --dry-run
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from grading_db import (
    detect_submission,
    load_student_roster,
    parse_student_weeks,
    query_submissions,
    update_submission_checkbox,
    update_grade_submissions_count,
    query_grades,
    _load_grading_ids,
)
from notion_api import _get_page_blocks, get_notion_token


def scan_student(student: dict, week_filter: str | None, token: str) -> dict[str, bool]:
    """Scan a student page and return {week_num: submitted} dict."""
    blocks = _get_page_blocks(student["page_id"], token=token)
    weeks = parse_student_weeks(blocks)

    results: dict[str, bool] = {}
    for week_num, week_blocks in weeks.items():
        if week_filter and week_num != week_filter:
            continue
        results[week_num] = detect_submission(week_blocks)

    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan student submissions")
    parser.add_argument("--week", type=int, help="Scan specific week only (e.g. 3)")
    parser.add_argument("--class", dest="class_num", help="Scan specific class only (1 or 2)")
    parser.add_argument("--dry-run", action="store_true", help="Show results without updating DB")
    args = parser.parse_args()

    token = get_notion_token()
    if not token:
        print("ERROR: NOTION_TOKEN not set", file=sys.stderr)
        return 1

    ids = _load_grading_ids()
    sub_db_id = ids.get("submissions_db_id")
    if not sub_db_id and not args.dry_run:
        print("ERROR: Submissions DB not initialized. Run init_grading_db.py first.", file=sys.stderr)
        return 1

    week_filter = f"{args.week:02d}" if args.week else None
    roster = load_student_roster(class_num=args.class_num)

    if not roster:
        print("No students found.", file=sys.stderr)
        return 1

    week_msg = f" for Week {week_filter}" if week_filter else ""
    print(f"Scanning {len(roster)} students{week_msg}...")

    # Scan all students
    all_results: list[dict] = []
    for i, student in enumerate(roster):
        results = scan_student(student, week_filter, token)
        for wk, submitted in results.items():
            all_results.append({
                "student": student,
                "week": wk,
                "submitted": submitted,
            })
        status_parts = []
        for w, s in sorted(results.items()):
            mark = "V" if s else "X"
            status_parts.append(f"W{w}={mark}")
        print(f"  [{i+1}/{len(roster)}] {student['name']}: {', '.join(status_parts)}")
        if (i + 1) % 5 == 0:
            time.sleep(0.3)  # Rate limit

    # Summary
    submitted_count = sum(1 for r in all_results if r["submitted"])
    total = len(all_results)
    pct = submitted_count / total * 100 if total else 0
    print(f"\nSummary: {submitted_count}/{total} submitted ({pct:.0f}%)")

    # Print not submitted
    not_submitted = [r for r in all_results if not r["submitted"]]
    if not_submitted:
        print(f"\nNot submitted ({len(not_submitted)}):")
        for r in sorted(not_submitted, key=lambda x: (x["week"], x["student"]["name"])):
            print(f"  Week {r['week']} - {r['student']['name']} ({r['student']['class_num']}반)")

    if args.dry_run:
        print("\n[DRY RUN] No database updates made.")
        return 0

    # Update submissions DB
    print("\nUpdating submissions database...")
    existing = query_submissions(sub_db_id, token=token)

    # Build lookup: (student_id, week) -> notion_page_id
    lookup: dict[tuple[str, str], str] = {}
    for row in existing:
        sid = row["student_id"]
        week = row["week"]  # "Week 03" format
        lookup[(sid, week)] = row["notion_page_id"]

    updated = 0
    for r in all_results:
        sid = r["student"]["student_id"]
        week_label = f"Week {r['week']}"
        page_id = lookup.get((sid, week_label))
        if page_id:
            update_submission_checkbox(page_id, r["submitted"], token=token)
            updated += 1
            if updated % 25 == 0:
                time.sleep(0.3)

    print(f"  Updated {updated} rows")

    # Update grade submission counts
    grades_db_id = ids.get("grades_db_id")
    if grades_db_id:
        print("Updating grade submission counts...")
        grades = query_grades(grades_db_id, token=token)
        # Count submissions per student
        sub_counts: dict[str, int] = {}
        for r in all_results:
            sid = r["student"]["student_id"]
            if r["submitted"]:
                sub_counts[sid] = sub_counts.get(sid, 0) + 1

        for grade in grades:
            sid = grade["student_id"]
            count = sub_counts.get(sid, 0)
            if count != grade["submissions"]:
                update_grade_submissions_count(grade["notion_page_id"], count, token=token)
        print("  Done")

    print("\nScan complete!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
