#!/usr/bin/env python3
"""
init_grading_db.py — CLI to create and populate Notion grading databases
=========================================================================
Creates the submissions DB (375 rows: 25 students × 15 weeks) and
grades DB (25 rows) under a given Notion parent page.

Usage::

    python tools/init_grading_db.py                          # live run
    python tools/init_grading_db.py --dry-run                # preview only
    python tools/init_grading_db.py --parent-page-id <id>    # custom parent

Exit codes:
    0: success
    1: error (missing token, API failure, etc.)
    2: aborted by user
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

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_PARENT_PAGE_ID = "31c54d6549718107a864f0dc8d16c45c"

#: Rate-limit: sleep this many seconds every RATE_BATCH rows.
RATE_SLEEP = 0.5
RATE_BATCH = 25


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _print_dry_run_summary(students: list[dict]) -> None:
    n = len(students)
    n_weeks = len(WEEKS)
    submission_rows = n * n_weeks
    grade_rows = n

    print("=== DRY RUN — no API calls will be made ===")
    print(f"  Students loaded   : {n}")
    print(f"  Weeks             : {n_weeks}  ({WEEKS[0]} – {WEEKS[-1]})")
    print(f"  Submission rows   : {submission_rows}  ({n} × {n_weeks})")
    print(f"  Grade rows        : {grade_rows}")
    print()
    print("  Would create:")
    print("    DB 1 → '과제 제출 현황' (submissions)")
    print(f"         → populate {submission_rows} rows")
    print("    DB 2 → '학생별 성적 현황' (grades)")
    print(f"         → populate {grade_rows} rows")
    print()
    print("Run without --dry-run to execute.")


def _confirm_reinit() -> bool:
    """Ask user whether to re-initialize already-existing databases."""
    print("WARNING: grading-db-ids.json already exists — databases may have been created before.")
    answer = input("Re-initialize (create fresh DBs and discard existing IDs)? [y/N] ").strip().lower()
    return answer in ("y", "yes")


def _populate_submissions(db_id: str, students: list[dict], token: str) -> int:
    """Add one row per (student, week) to the submissions DB.

    Returns the total number of rows created.
    """
    total = 0
    for student in students:
        for week in WEEKS:
            add_submission_row(
                db_id=db_id,
                name=student["name"],
                student_id=student["student_id"],
                class_num=student["class_num"],
                week=week,
                submitted=False,
                page_id=student["page_id"],
                token=token,
            )
            total += 1
            if total % RATE_BATCH == 0:
                time.sleep(RATE_SLEEP)
                print(f"  ... {total} rows created", end="\r", flush=True)

    print()  # newline after \r progress
    return total


def _populate_grades(db_id: str, students: list[dict], token: str) -> int:
    """Add one row per student to the grades DB.

    Returns the total number of rows created.
    """
    total = 0
    for student in students:
        add_grade_row(
            db_id=db_id,
            name=student["name"],
            student_id=student["student_id"],
            class_num=student["class_num"],
            submissions_count=0,
            total_weeks=len(WEEKS),
            page_id=student["page_id"],
            token=token,
        )
        total += 1
        if total % RATE_BATCH == 0:
            time.sleep(RATE_SLEEP)

    return total


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create and populate Notion grading databases.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--parent-page-id",
        default=DEFAULT_PARENT_PAGE_ID,
        metavar="PAGE_ID",
        help=f"Notion page that will contain both DBs (default: {DEFAULT_PARENT_PAGE_ID})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be created without making any API calls.",
    )
    args = parser.parse_args()

    # ------------------------------------------------------------------
    # 1. Load student roster
    # ------------------------------------------------------------------
    students = load_student_roster()
    if not students:
        print("Error: No students found in notion-mapping.json.", file=sys.stderr)
        return 1

    # ------------------------------------------------------------------
    # 2. Dry-run: just print and exit
    # ------------------------------------------------------------------
    if args.dry_run:
        _print_dry_run_summary(students)
        return 0

    # ------------------------------------------------------------------
    # 3. Token check (live run only)
    # ------------------------------------------------------------------
    token = get_notion_token()
    if not token:
        print("Error: NOTION_TOKEN environment variable not set.", file=sys.stderr)
        return 1

    # ------------------------------------------------------------------
    # 4. Check if already initialized
    # ------------------------------------------------------------------
    existing_ids = _load_grading_ids()
    if existing_ids:
        if not _confirm_reinit():
            print("Aborted.")
            return 2

    # ------------------------------------------------------------------
    # 5. Create submissions DB and populate
    # ------------------------------------------------------------------
    print(f"Creating submissions DB under parent page {args.parent_page_id!r} …")
    try:
        subs_resp = create_submissions_db(parent_page_id=args.parent_page_id, token=token)
    except Exception as exc:
        print(f"Error creating submissions DB: {exc}", file=sys.stderr)
        return 1

    subs_db_id: str = subs_resp["id"]
    print(f"  submissions DB id: {subs_db_id}")

    print(f"Populating {len(students) * len(WEEKS)} submission rows …")
    try:
        subs_total = _populate_submissions(subs_db_id, students, token)
    except Exception as exc:
        print(f"Error populating submissions DB: {exc}", file=sys.stderr)
        return 1

    print(f"  {subs_total} submission rows created.")

    # ------------------------------------------------------------------
    # 6. Create grades DB and populate
    # ------------------------------------------------------------------
    print(f"Creating grades DB under parent page {args.parent_page_id!r} …")
    try:
        grades_resp = create_grades_db(parent_page_id=args.parent_page_id, token=token)
    except Exception as exc:
        print(f"Error creating grades DB: {exc}", file=sys.stderr)
        return 1

    grades_db_id: str = grades_resp["id"]
    print(f"  grades DB id: {grades_db_id}")

    print(f"Populating {len(students)} grade rows …")
    try:
        grades_total = _populate_grades(grades_db_id, students, token)
    except Exception as exc:
        print(f"Error populating grades DB: {exc}", file=sys.stderr)
        return 1

    print(f"  {grades_total} grade rows created.")

    # ------------------------------------------------------------------
    # 7. Summary
    # ------------------------------------------------------------------
    print()
    print("=== Initialization complete ===")
    print(f"  submissions DB : {subs_db_id}  ({subs_total} rows)")
    print(f"  grades DB      : {grades_db_id}  ({grades_total} rows)")
    print()
    print("IDs are saved in tools/grading-db-ids.json for subsequent scripts.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
