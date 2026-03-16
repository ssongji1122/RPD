#!/usr/bin/env python3
"""
migrate-to-overrides.py
=======================
One-time migration script that extracts admin-owned fields from
course-site/data/curriculum.js into course-site/data/overrides.json.

Admin-owned fields:
  Week level  : status, summary, videos, explore
  Step level  : image, done, showme, link

Usage:
    python3 tools/migrate-to-overrides.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CURRICULUM_JS = ROOT / "course-site" / "data" / "curriculum.js"
OVERRIDES_JSON = ROOT / "course-site" / "data" / "overrides.json"

# Admin-owned field names
WEEK_FIELDS = ("status", "summary", "videos", "explore")
STEP_FIELDS = ("image", "done", "showme", "link")


# ---------------------------------------------------------------------------
# JS-to-JSON conversion (adapted from admin-server.py _js_to_json)
# ---------------------------------------------------------------------------
def _js_to_json(text: str) -> str:
    """
    Convert a JS value expression (object/array literal) to valid JSON.

    Handles:
    - Stripping single-line comments (// ...) outside strings
    - Quoting bare (unquoted) object keys
    - Removing trailing commas before } or ]

    Uses a character-level scanner so it never modifies content inside
    double-quoted string literals.
    """
    result: list[str] = []
    i = 0
    length = len(text)

    while i < length:
        ch = text[i]

        # --- Double-quoted string: copy verbatim ---
        if ch == '"':
            j = i + 1
            while j < length:
                if text[j] == "\\":
                    j += 2
                    continue
                if text[j] == '"':
                    j += 1
                    break
                j += 1
            result.append(text[i:j])
            i = j
            continue

        # --- Single-line comment: skip to EOL ---
        if ch == "/" and i + 1 < length and text[i + 1] == "/":
            while i < length and text[i] != "\n":
                i += 1
            continue

        # --- Bare identifier key: quote it ---
        if ch.isalpha() or ch == "_":
            j = i
            while j < length and (text[j].isalnum() or text[j] == "_"):
                j += 1
            k = j
            while k < length and text[k] in " \t":
                k += 1
            if k < length and text[k] == ":":
                preceding = "".join(result).rstrip()
                if preceding and preceding[-1] in "{,[\n":
                    key = text[i:j]
                    result.append(f'"{key}"')
                    i = j
                    continue

            result.append(ch)
            i += 1
            continue

        result.append(ch)
        i += 1

    output = "".join(result)
    output = re.sub(r",\s*([}\]])", r"\1", output)
    return output


def read_curriculum() -> list[dict]:
    """Read curriculum.js and return the parsed array."""
    text = CURRICULUM_JS.read_text(encoding="utf-8")

    start_marker = "const CURRICULUM = "
    start = text.find(start_marker)
    if start == -1:
        raise ValueError("Cannot find 'const CURRICULUM = ' in curriculum.js")
    start += len(start_marker)

    end = text.find("];", start)
    if end == -1:
        raise ValueError("Cannot find closing '];' in curriculum.js")
    array_text = text[start : end + 1]

    json_text = _js_to_json(array_text)
    return json.loads(json_text)


# ---------------------------------------------------------------------------
# Value helpers
# ---------------------------------------------------------------------------
def _is_empty(value: object) -> bool:
    """Return True if value is absent, None, empty string, or empty list."""
    if value is None:
        return True
    if isinstance(value, str) and value.strip() == "":
        return True
    if isinstance(value, list) and len(value) == 0:
        return True
    return False


# ---------------------------------------------------------------------------
# Migration logic
# ---------------------------------------------------------------------------
def build_overrides(weeks: list[dict]) -> dict:
    """Extract admin-owned fields from curriculum data into overrides structure."""
    overrides: dict = {
        "_comment": "어드민 전용 필드. 노션 동기화 시 이 값이 우선함.",
        "weeks": {},
    }

    for week in weeks:
        week_num = week.get("week")
        if week_num is None:
            continue

        week_key = str(week_num)
        week_override: dict = {}

        # Extract week-level admin fields
        for field in WEEK_FIELDS:
            value = week.get(field)
            if not _is_empty(value):
                week_override[field] = value

        # Extract step-level admin fields
        steps = week.get("steps", [])
        if steps:
            steps_override: dict = {}
            for idx, step in enumerate(steps):
                step_override: dict = {}
                for field in STEP_FIELDS:
                    value = step.get(field)
                    if not _is_empty(value):
                        step_override[field] = value
                if step_override:
                    steps_override[str(idx)] = step_override
            if steps_override:
                week_override["steps"] = steps_override

        if week_override:
            overrides["weeks"][week_key] = week_override

    return overrides


NOTION_JSON = ROOT / "course-site" / "data" / "curriculum-notion.json"


def build_notion_snapshot(weeks: list[dict]) -> list[dict]:
    """
    Build Notion-only data by stripping admin-owned fields from each week.
    This is the inverse of build_overrides().
    """
    import copy

    result = []
    for week in weeks:
        w = copy.deepcopy(week)
        # Remove week-level admin fields
        for field in WEEK_FIELDS:
            w.pop(field, None)
        # Remove step-level admin fields
        for step in w.get("steps", []):
            for field in STEP_FIELDS:
                step.pop(field, None)
        result.append(w)
    return result


def print_summary(overrides: dict) -> None:
    """Print a human-readable summary of extracted data."""
    weeks_data = overrides.get("weeks", {})
    print(f"\n{'=' * 60}")
    print(f"  overrides.json Migration Summary")
    print(f"{'=' * 60}")
    print(f"  Total weeks with overrides: {len(weeks_data)}")
    print()

    for week_key in sorted(weeks_data.keys(), key=int):
        week = weeks_data[week_key]
        fields = [k for k in week if k != "steps"]
        step_count = len(week.get("steps", {}))

        step_fields_summary = {}
        for step_data in week.get("steps", {}).values():
            for field in step_data:
                step_fields_summary[field] = step_fields_summary.get(field, 0) + 1

        parts = []
        if fields:
            parts.append(f"week-level: {', '.join(fields)}")
        if step_count:
            step_detail = ", ".join(f"{k}({v})" for k, v in sorted(step_fields_summary.items()))
            parts.append(f"{step_count} steps [{step_detail}]")

        print(f"  Week {week_key:>2}: {' | '.join(parts)}")

    print(f"\n{'=' * 60}\n")


def main() -> int:
    if not CURRICULUM_JS.exists():
        print(f"ERROR: {CURRICULUM_JS} not found", file=sys.stderr)
        return 1

    print(f"Reading {CURRICULUM_JS} ...")
    try:
        weeks = read_curriculum()
    except Exception as exc:
        print(f"ERROR: Failed to parse curriculum.js: {exc}", file=sys.stderr)
        return 1

    print(f"Parsed {len(weeks)} weeks from curriculum.js")

    overrides = build_overrides(weeks)
    print_summary(overrides)

    output = json.dumps(overrides, ensure_ascii=False, indent=2) + "\n"
    OVERRIDES_JSON.write_text(output, encoding="utf-8")
    print(f"Written to {OVERRIDES_JSON}")
    print(f"File size: {len(output):,} bytes")

    # Also generate curriculum-notion.json (Notion-only snapshot)
    notion_data = build_notion_snapshot(weeks)
    notion_output = json.dumps(notion_data, ensure_ascii=False, indent=2) + "\n"
    NOTION_JSON.write_text(notion_output, encoding="utf-8")
    print(f"Written to {NOTION_JSON}")
    print(f"File size: {len(notion_output):,} bytes")

    return 0


if __name__ == "__main__":
    sys.exit(main())
