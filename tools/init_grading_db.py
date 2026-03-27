#!/usr/bin/env python3
"""
Initialize Grading Databases
=============================
Creates the 과제 제출 현황 and 학기 성적 종합 databases on Notion
and populates them with student rows.

Usage:
    NOTION_TOKEN=... python tools/init_grading_db.py

Options:
    --parent-page-id ID   Override the parent page (default: 03 학생 개인 페이지 운영)
    --dry-run             Show what would be created without calling the API
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from grading_db import (
    WEEKS,
    _load_grading_ids,
    add_grade_row,
    add_submission_row,
    create_grades_db,
    create_submissions_db,
    load_student_roster,
)
from notion_api import get_notion_token

# Parent page: 03 학생 개인 페이지 운영
DEFAULT_PARENT = "31c54d6549718107a864f0dc8d16c45c"


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize grading databases")
    parser.add_argument("--parent-page-id", default=DEFAULT_PARENT)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    token = get_notion_token()
    if not token and not args.dry_run:
        print("ERROR: NOTION_TOKEN not set", file=sys.stderr)
        return 1

    roster = load_student_roster()
    if not roster:
        print("ERROR: No students found in notion-mapping.json", file=sys.stderr)
        return 1

    print(f"Found {len(roster)} students across {len(set(s['class_num'] for s in roster))} classes")

    if args.dry_run:
        print(f"\n[DRY RUN] Would create:")
        print(f"  - 과제 제출 현황 DB: {len(roster)} students x {len(WEEKS)} weeks = {len(roster) * len(WEEKS)} rows")
        print(f"  - 학기 성적 종합 DB: {len(roster)} rows")
        return 0

    # Check if already initialized
    ids = _load_grading_ids()
    if ids.get("submissions_db_id") or ids.get("grades_db_id"):
        print("WARNING: Databases already initialized!")
        print(f"  submissions_db_id: {ids.get('submissions_db_id', 'N/A')}")
        print(f"  grades_db_id: {ids.get('grades_db_id', 'N/A')}")
        answer = input("Re-initialize? This will create NEW databases (old ones remain). [y/N] ")
        if answer.lower() != "y":
            print("Aborted.")
            return 0

    # 1. Create submissions DB
    print("\nCreating submissions database...")
    sub_db_id = create_submissions_db(args.parent_page_id, token=token)
    print(f"  Created: {sub_db_id}")

    # 2. Populate submission rows
    total = len(roster) * len(WEEKS)
    count = 0
    for student in roster:
        for week in WEEKS:
            add_submission_row(sub_db_id, student, week, submitted=False, token=token)
            count += 1
            if count % 25 == 0:
                print(f"  Submissions: {count}/{total} rows created...")
                time.sleep(0.5)  # Notion API rate limit
    print(f"  Done: {count} submission rows created")

    # 3. Create grades DB
    print("\nCreating grades database...")
    grades_db_id = create_grades_db(args.parent_page_id, token=token)
    print(f"  Created: {grades_db_id}")

    # 4. Populate grade rows
    for i, student in enumerate(roster):
        add_grade_row(grades_db_id, student, token=token)
        if (i + 1) % 10 == 0:
            time.sleep(0.3)
    print(f"  Done: {len(roster)} grade rows created")

    print(f"\nInitialization complete!")
    print(f"  Submissions DB: {sub_db_id}")
    print(f"  Grades DB: {grades_db_id}")
    print(f"  IDs saved to: tools/grading-db-ids.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
