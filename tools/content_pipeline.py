#!/usr/bin/env python3
"""
Canonical curriculum pipeline for RPD.

Source of truth:
    weeks/site-data.json

Generated outputs:
    course-site/data/curriculum.json
    course-site/data/curriculum.js
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

from lecture_notes_sync import sync_lecture_notes
from markdown_import import build_curriculum_from_markdown
from runtime_paths import (
    CANONICAL_JSON,
    COURSE_SITE,
    GENERATED_JS,
    GENERATED_JSON,
    NOTION_JSON,
    OVERRIDES_JSON,
    ROOT,
    SCHEMA_JSON,
    WEEKS_DIR,
)

CURRICULUM_HEADER = """\
// ============================================================
// 15주 블렌더 수업 커리큘럼 데이터
// 이 파일은 weeks/site-data.json 에서 자동 생성됩니다.
// ============================================================

const CURRICULUM = """

CURRICULUM_FOOTER = """\
;

// Node.js 환경 대응
if (typeof module !== "undefined") module.exports = CURRICULUM;
"""

PUBLIC_EXCLUDED_RELATIVE_PATHS = {
    "CONTENT_GUIDE.md",
    "admin.html",
    "data/curriculum-notion.json",
    "data/notion-config.json",
    "data/notion-config.local.json",
    "data/overrides.json",
    "data/students.js",
    "data/students.json",
    "data/curriculum.js.bak",
}

TEXT_SCAN_SUFFIXES = {
    ".css",
    ".html",
    ".js",
    ".json",
    ".md",
    ".svg",
    ".txt",
}

SENSITIVE_CONTENT_PATTERNS = {
    "notion-token": re.compile(r"ntn_[A-Za-z0-9]+"),
    "client-secret": re.compile(r"client_secret", re.IGNORECASE),
    "auth-header": re.compile(r"\bAuthorization\b"),
    "admin-session-storage": re.compile(r"rpd-admin-token"),
    "student-roster": re.compile(r"\bSTUDENTS\s*="),
}


def _read_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content)


def _read_generated_js() -> list[dict[str, Any]]:
    text = GENERATED_JS.read_text(encoding="utf-8")
    match = re.search(r"const\s+CURRICULUM\s*=\s*(\[.*\])\s*;", text, re.DOTALL)
    if not match:
        raise ValueError(f"Could not find CURRICULUM array in {GENERATED_JS}")
    return json.loads(match.group(1))


def _string(value: Any, *, default: str = "") -> str:
    if value is None:
        return default
    return str(value)


def _normalize_string_list(values: Any) -> list[str]:
    if not isinstance(values, list):
        return []
    return [_string(value).strip() for value in values if _string(value).strip()]


def _normalize_resource_list(values: Any) -> list[dict[str, str]]:
    if not isinstance(values, list):
        return []
    normalized: list[dict[str, str]] = []
    for item in values:
        if not isinstance(item, dict):
            continue
        title = _string(item.get("title")).strip()
        url = _string(item.get("url")).strip()
        if title or url:
            normalized.append({"title": title, "url": url})
    return normalized


def _normalize_shortcuts(values: Any) -> list[dict[str, str]]:
    if not isinstance(values, list):
        return []
    normalized: list[dict[str, str]] = []
    for item in values:
        if not isinstance(item, dict):
            continue
        normalized.append(
            {
                "keys": _string(item.get("keys")).strip(),
                "action": _string(item.get("action")).strip(),
            }
        )
    return [item for item in normalized if item["keys"] or item["action"]]


def _normalize_explore(values: Any) -> list[dict[str, str]]:
    if not isinstance(values, list):
        return []
    normalized: list[dict[str, str]] = []
    for item in values:
        if not isinstance(item, dict):
            continue
        normalized.append(
            {
                "title": _string(item.get("title")).strip(),
                "hint": _string(item.get("hint")).strip(),
            }
        )
    return [item for item in normalized if item["title"] or item["hint"]]


def _normalize_downloads(values: Any) -> list[dict[str, str]]:
    if not isinstance(values, list):
        return []
    normalized: list[dict[str, str]] = []
    for item in values:
        if not isinstance(item, dict):
            continue
        normalized.append(
            {
                "label": _string(item.get("label")).strip(),
                "url": _string(item.get("url")).strip(),
            }
        )
    return [item for item in normalized if item["label"] or item["url"]]


def _normalize_showme(value: Any) -> str | list[str] | None:
    if value is None:
        return None
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    if isinstance(value, list):
        normalized = [_string(item).strip() for item in value if _string(item).strip()]
        return normalized or None
    return None


def _normalize_widgets(values: Any) -> list[dict[str, str]]:
    if not isinstance(values, list):
        return []
    normalized: list[dict[str, str]] = []
    for item in values:
        if not isinstance(item, dict):
            continue
        widget_type = _string(item.get("type")).strip()
        widget_id = _string(item.get("id")).strip()
        if widget_type or widget_id:
            normalized.append({"type": widget_type, "id": widget_id})
    return [item for item in normalized if item["type"] and item["id"]]


def _normalize_tasks(values: Any) -> list[dict[str, str]]:
    if not isinstance(values, list):
        return []
    normalized: list[dict[str, str]] = []
    for index, item in enumerate(values, start=1):
        if not isinstance(item, dict):
            continue
        task_id = _string(item.get("id")).strip() or f"task-{index}"
        normalized.append(
            {
                "id": task_id,
                "label": _string(item.get("label")).strip(),
                "detail": _string(item.get("detail")).strip(),
            }
        )
    return normalized


def _normalize_step(step: Any) -> dict[str, Any]:
    if not isinstance(step, dict):
        step = {}
    normalized: dict[str, Any] = {
        "title": _string(step.get("title")).strip(),
        "copy": _string(step.get("copy")).strip(),
        "goal": _normalize_string_list(step.get("goal")),
        "done": _normalize_string_list(step.get("done")),
        "tasks": _normalize_tasks(step.get("tasks")),
    }

    optional_text_fields = ("image", "link", "video", "sectionTitle")
    for field in optional_text_fields:
        value = _string(step.get(field)).strip()
        if value:
            normalized[field] = value

    images = _normalize_string_list(step.get("images"))
    if images:
        normalized["images"] = images

    downloads = _normalize_downloads(step.get("downloads"))
    if downloads:
        normalized["downloads"] = downloads

    clips = []
    if isinstance(step.get("clips"), list):
        for clip in step["clips"]:
            if not isinstance(clip, dict):
                continue
            label = _string(clip.get("label")).strip()
            src = _string(clip.get("src")).strip()
            if label or src:
                clips.append({"label": label, "src": src})
    if clips:
        normalized["clips"] = clips

    showme = _normalize_showme(step.get("showme"))
    if showme is not None:
        normalized["showme"] = showme

    widgets = _normalize_widgets(step.get("widgets"))
    if widgets:
        normalized["widgets"] = widgets

    return normalized


def _normalize_assignment(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        value = {}
    return {
        "title": _string(value.get("title")).strip(),
        "description": _string(value.get("description")).strip(),
        "checklist": _normalize_string_list(value.get("checklist")),
    }


def normalize_week(week: Any) -> dict[str, Any]:
    if not isinstance(week, dict):
        week = {}

    normalized_steps = [_normalize_step(step) for step in week.get("steps", []) or []]

    seen_task_ids: dict[str, int] = {}
    for step in normalized_steps:
        for task in step["tasks"]:
            base_id = task["id"] or "task"
            next_count = seen_task_ids.get(base_id, 0) + 1
            seen_task_ids[base_id] = next_count
            if next_count > 1:
                task["id"] = f"{base_id}-{next_count}"

    normalized: dict[str, Any] = {
        "week": int(week.get("week", 0) or 0),
        "status": _string(week.get("status"), default="upcoming").strip() or "upcoming",
        "title": _string(week.get("title")).strip(),
        "subtitle": _string(week.get("subtitle")).strip(),
        "duration": _string(week.get("duration")).strip(),
        "topics": _normalize_string_list(week.get("topics")),
        "steps": normalized_steps,
        "shortcuts": _normalize_shortcuts(week.get("shortcuts")),
        "explore": _normalize_explore(week.get("explore")),
        "assignment": _normalize_assignment(week.get("assignment")),
        "mistakes": _normalize_string_list(week.get("mistakes")),
        "videos": _normalize_resource_list(week.get("videos")),
        "docs": _normalize_resource_list(week.get("docs")),
    }

    summary = _string(week.get("summary")).strip()
    if summary:
        normalized["summary"] = summary

    return normalized


def normalize_curriculum(data: Any) -> list[dict[str, Any]]:
    if not isinstance(data, list):
        raise ValueError("Curriculum payload must be a list")
    normalized = [normalize_week(week) for week in data]
    return sorted(normalized, key=lambda week: week["week"])


def _find_lecture_note(week_num: int) -> Path | None:
    matches = sorted(WEEKS_DIR.glob(f"week{week_num:02d}-*/lecture-note.md"))
    return matches[0] if matches else None


def validate_curriculum(data: Any) -> list[str]:
    errors: list[str] = []
    try:
        weeks = normalize_curriculum(data)
    except Exception as exc:  # pragma: no cover - defensive guard
        return [str(exc)]

    seen_weeks: set[int] = set()
    allowed_status = {"done", "active", "upcoming"}

    for week in weeks:
        week_num = week["week"]
        prefix = f"Week {week_num:02d}"

        if week_num <= 0:
            errors.append(f"{prefix}: week must be a positive integer")
        if week_num in seen_weeks:
            errors.append(f"{prefix}: duplicate week number")
        seen_weeks.add(week_num)

        if week["status"] not in allowed_status:
            errors.append(f"{prefix}: status must be one of {sorted(allowed_status)}")
        if not week["title"]:
            errors.append(f"{prefix}: title is required")
        if not week["duration"]:
            errors.append(f"{prefix}: duration is required")
        if not week["topics"]:
            errors.append(f"{prefix}: topics must contain at least one item")
        if not week["steps"]:
            errors.append(f"{prefix}: steps must contain at least one item")

        lecture_note = _find_lecture_note(week_num)
        if lecture_note is None:
            errors.append(f"{prefix}: missing lecture-note.md in weeks/")

        assignment = week["assignment"]
        if not assignment["title"]:
            errors.append(f"{prefix}: assignment.title is required")
        if not assignment["description"]:
            errors.append(f"{prefix}: assignment.description is required")
        if not assignment["checklist"]:
            errors.append(f"{prefix}: assignment.checklist must contain at least one item")

        week_task_ids: set[str] = set()

        for resource_group in ("videos", "docs"):
            for index, item in enumerate(week[resource_group], start=1):
                if not item["title"] or not item["url"]:
                    errors.append(f"{prefix}: {resource_group}[{index}] requires title and url")

        for step_index, step in enumerate(week["steps"], start=1):
            step_prefix = f"{prefix} Step {step_index}"
            if not step["title"]:
                errors.append(f"{step_prefix}: title is required")
            if not step["copy"]:
                errors.append(f"{step_prefix}: copy is required")
            if not step["tasks"]:
                errors.append(f"{step_prefix}: tasks must contain at least one item")
            showme = step.get("showme")
            if showme is not None and not isinstance(showme, (str, list)):
                errors.append(f"{step_prefix}: showme must be a string or string list")
            widgets = step.get("widgets", [])
            if widgets and not isinstance(widgets, list):
                errors.append(f"{step_prefix}: widgets must be a list")
            for widget_index, widget in enumerate(widgets, start=1):
                if not isinstance(widget, dict):
                    errors.append(f"{step_prefix}: widgets[{widget_index}] must be an object")
                    continue
                if not widget.get("type"):
                    errors.append(f"{step_prefix}: widgets[{widget_index}].type is required")
                if not widget.get("id"):
                    errors.append(f"{step_prefix}: widgets[{widget_index}].id is required")

            for task_index, task in enumerate(step["tasks"], start=1):
                task_prefix = f"{step_prefix} Task {task_index}"
                if not task["id"]:
                    errors.append(f"{task_prefix}: id is required")
                if not task["label"]:
                    errors.append(f"{task_prefix}: label is required")
                if task["id"] in week_task_ids:
                    errors.append(f"{task_prefix}: duplicate task id '{task['id']}'")
                week_task_ids.add(task["id"])

    return errors


def load_canonical_curriculum() -> list[dict[str, Any]]:
    if CANONICAL_JSON.exists():
        return normalize_curriculum(_read_json(CANONICAL_JSON))
    return normalize_curriculum(_read_generated_js())


def load_notion_snapshot() -> list[dict[str, Any]]:
    if not NOTION_JSON.exists():
        raise FileNotFoundError(f"Notion snapshot not found: {NOTION_JSON}")
    return normalize_curriculum(_read_json(NOTION_JSON))


def load_overrides() -> dict[str, Any]:
    if not OVERRIDES_JSON.exists():
        return {}
    payload = _read_json(OVERRIDES_JSON)
    return payload if isinstance(payload, dict) else {}


def _merge_week_with_base(
    base_week: dict[str, Any] | None,
    notion_week: dict[str, Any],
) -> dict[str, Any]:
    def should_override(value: Any) -> bool:
        if value is None:
            return False
        if isinstance(value, str):
            return bool(value.strip())
        if isinstance(value, (list, dict)):
            return bool(value)
        return True

    if not base_week:
        return copy.deepcopy(notion_week)

    merged = copy.deepcopy(base_week)

    for key, value in notion_week.items():
        if key in {"steps", "assignment"}:
            continue
        if should_override(value) or key not in merged:
            merged[key] = copy.deepcopy(value)

    if "assignment" in notion_week:
        merged_assignment = copy.deepcopy(base_week.get("assignment", {}) or {})
        notion_assignment = notion_week.get("assignment", {}) or {}
        if isinstance(notion_assignment, dict):
            for key, value in notion_assignment.items():
                if should_override(value) or key not in merged_assignment:
                    merged_assignment[key] = copy.deepcopy(value)
        merged["assignment"] = merged_assignment

    if "steps" in notion_week:
        base_steps = base_week.get("steps", []) or []
        notion_steps = notion_week.get("steps", []) or []
        step_count = max(len(base_steps), len(notion_steps))
        merged_steps: list[dict[str, Any]] = []
        for idx in range(step_count):
            base_step = base_steps[idx] if idx < len(base_steps) else {}
            notion_step = notion_steps[idx] if idx < len(notion_steps) else {}
            merged_step = copy.deepcopy(base_step)
            if isinstance(notion_step, dict):
                for key, value in notion_step.items():
                    if should_override(value) or key not in merged_step:
                        merged_step[key] = copy.deepcopy(value)
            if merged_step:
                merged_steps.append(merged_step)
        merged["steps"] = merged_steps

    return merged


def load_notion_first_curriculum_with_report() -> tuple[list[dict[str, Any]], list[int]]:
    from notion_api import merge_curriculum

    base_data = {week["week"]: week for week in load_canonical_curriculum()}
    notion_snapshot = load_notion_snapshot()
    notion_data: list[dict[str, Any]] = []
    fallback_weeks: list[int] = []
    for week in notion_snapshot:
        week_num = int(week["week"])
        candidate = _merge_week_with_base(base_data.get(week_num), week)
        candidate_errors = validate_curriculum([candidate])
        if candidate_errors and week_num in base_data:
            notion_data.append(copy.deepcopy(base_data[week_num]))
            fallback_weeks.append(week_num)
            continue
        notion_data.append(candidate)
    overrides = load_overrides()
    return normalize_curriculum(merge_curriculum(notion_data, overrides)), fallback_weeks


def load_notion_first_curriculum() -> list[dict[str, Any]]:
    curriculum, _fallback_weeks = load_notion_first_curriculum_with_report()
    return curriculum


def write_canonical_curriculum(data: Any) -> list[dict[str, Any]]:
    normalized = normalize_curriculum(data)
    errors = validate_curriculum(normalized)
    if errors:
        raise ValueError("\n".join(errors))
    _write_json(CANONICAL_JSON, normalized)
    return normalized


def render_curriculum_js(data: Any) -> str:
    normalized = normalize_curriculum(data)
    return CURRICULUM_HEADER + json.dumps(normalized, ensure_ascii=False, indent=2) + CURRICULUM_FOOTER


def content_version(data: Any) -> str:
    normalized = normalize_curriculum(data)
    payload = json.dumps(normalized, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]


def write_generated_outputs(data: Any) -> dict[str, Any]:
    normalized = normalize_curriculum(data)
    errors = validate_curriculum(normalized)
    if errors:
        raise ValueError("\n".join(errors))

    _write_json(GENERATED_JSON, normalized)
    _write_text(GENERATED_JS, render_curriculum_js(normalized))
    sync_lecture_notes(normalized)
    return {"version": content_version(normalized), "weeks": len(normalized)}


def summarize_week_diff(current_week: dict[str, Any], candidate_week: dict[str, Any]) -> dict[str, Any] | None:
    changed_fields: list[str] = []
    for field in (
        "status",
        "title",
        "subtitle",
        "duration",
        "topics",
        "shortcuts",
        "explore",
        "assignment",
        "mistakes",
        "videos",
        "docs",
        "summary",
    ):
        if current_week.get(field) != candidate_week.get(field):
            changed_fields.append(field)

    if current_week.get("steps") != candidate_week.get("steps"):
        changed_fields.append("steps")

    if not changed_fields:
        return None

    return {
        "week": candidate_week["week"],
        "title": candidate_week["title"],
        "changed_fields": changed_fields,
        "step_count": len(candidate_week.get("steps", [])),
    }


def compute_curriculum_diff(current: Any, candidate: Any) -> dict[str, Any]:
    current_weeks = {week["week"]: week for week in normalize_curriculum(current)}
    candidate_weeks = {week["week"]: week for week in normalize_curriculum(candidate)}

    changed_weeks: list[dict[str, Any]] = []
    for week_num in sorted(set(current_weeks) | set(candidate_weeks)):
        current_week = current_weeks.get(week_num)
        candidate_week = candidate_weeks.get(week_num)

        if current_week is None and candidate_week is not None:
            changed_weeks.append(
                {
                    "week": week_num,
                    "title": candidate_week["title"],
                    "changed_fields": ["created"],
                    "step_count": len(candidate_week.get("steps", [])),
                }
            )
            continue

        if candidate_week is None and current_week is not None:
            changed_weeks.append(
                {
                    "week": week_num,
                    "title": current_week["title"],
                    "changed_fields": ["deleted"],
                    "step_count": len(current_week.get("steps", [])),
                }
            )
            continue

        diff = summarize_week_diff(current_week, candidate_week)
        if diff:
            changed_weeks.append(diff)

    return {
        "version_from": content_version(list(current_weeks.values())),
        "version_to": content_version(list(candidate_weeks.values())),
        "changed_count": len(changed_weeks),
        "changed_weeks": changed_weeks,
        "unchanged_count": max(len(candidate_weeks) - len(changed_weeks), 0),
    }


def _ignore_public_copy(directory: str, names: list[str]) -> set[str]:
    ignored: set[str] = set()
    relative_dir = Path(directory).resolve().relative_to(COURSE_SITE.resolve())

    for name in names:
        rel_path = (relative_dir / name).as_posix()
        if rel_path in PUBLIC_EXCLUDED_RELATIVE_PATHS:
            ignored.add(name)
            continue
        if rel_path.startswith("data/") and name.endswith(".bak"):
            ignored.add(name)
    return ignored


def scan_public_artifact(output_dir: Path) -> list[str]:
    errors: list[str] = []

    for relative_path in sorted(PUBLIC_EXCLUDED_RELATIVE_PATHS):
        if (output_dir / relative_path).exists():
            errors.append(f"Public artifact contains excluded file: {relative_path}")

    for path in output_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in TEXT_SCAN_SUFFIXES:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in SENSITIVE_CONTENT_PATTERNS.items():
            if pattern.search(content):
                errors.append(f"{path.relative_to(output_dir)} contains sensitive marker: {label}")

    return errors


def build_public_site(output_dir: Path) -> dict[str, Any]:
    data = load_canonical_curriculum()
    build_meta = write_generated_outputs(data)

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(COURSE_SITE, output_dir, ignore=_ignore_public_copy)

    errors = scan_public_artifact(output_dir)
    if errors:
        raise ValueError("\n".join(errors))

    build_info = {
        "version": build_meta["version"],
        "weeks": build_meta["weeks"],
        "source": str(CANONICAL_JSON.relative_to(ROOT)),
    }
    _write_json(output_dir / "data" / "public-build.json", build_info)
    return build_info


def bootstrap_from_generated(*, force: bool = False) -> list[dict[str, Any]]:
    if CANONICAL_JSON.exists() and not force:
        raise FileExistsError(f"{CANONICAL_JSON} already exists")
    generated = _read_generated_js()
    normalized = write_canonical_curriculum(generated)
    write_generated_outputs(normalized)
    return normalized


def _print_errors(errors: list[str]) -> int:
    for error in errors:
        print(f"✗ {error}", file=sys.stderr)
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="RPD canonical curriculum pipeline")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("check", help="Validate canonical curriculum and generated outputs")
    subparsers.add_parser("build", help="Generate course-site curriculum assets from canonical data")

    build_public = subparsers.add_parser("build-public", help="Build public deployment artifact")
    build_public.add_argument("--output", required=True, help="Output directory for public site")

    bootstrap = subparsers.add_parser("bootstrap", help="Create canonical data from current curriculum.js")
    bootstrap.add_argument("--force", action="store_true", help="Overwrite existing canonical data")

    markdown_sync = subparsers.add_parser(
        "sync-from-markdown",
        help="Rebuild canonical curriculum by merging lecture-note markdown into site-data.json",
    )
    markdown_sync.add_argument(
        "--write",
        action="store_true",
        help="Persist merged curriculum into weeks/site-data.json and regenerate outputs",
    )

    notion_sync = subparsers.add_parser(
        "sync-from-notion",
        help="Rebuild canonical curriculum from curriculum-notion.json + overrides.json",
    )
    notion_sync.add_argument(
        "--write",
        action="store_true",
        help="Persist merged curriculum into weeks/site-data.json and regenerate outputs",
    )

    args = parser.parse_args()

    if args.command == "bootstrap":
        normalized = bootstrap_from_generated(force=args.force)
        print(f"✓ Bootstrapped {len(normalized)} weeks into {CANONICAL_JSON.relative_to(ROOT)}")
        return 0

    if args.command == "sync-from-markdown":
        existing = load_canonical_curriculum()
        merged = normalize_curriculum(build_curriculum_from_markdown(WEEKS_DIR, existing))
        errors = validate_curriculum(merged)
        if errors:
            return _print_errors(errors)

        diff = compute_curriculum_diff(existing, merged)
        if args.write:
            write_canonical_curriculum(merged)
            result = write_generated_outputs(merged)
            print(
                f"✓ Synced canonical curriculum from markdown "
                f"({diff['changed_count']} changed weeks, version {result['version']})"
            )
        else:
            print(
                f"✓ Markdown import validated "
                f"({diff['changed_count']} changed weeks, next version {diff['version_to']})"
            )
        return 0

    if args.command == "sync-from-notion":
        existing = load_canonical_curriculum()
        merged, fallback_weeks = load_notion_first_curriculum_with_report()
        errors = validate_curriculum(merged)
        if errors:
            return _print_errors(errors)

        diff = compute_curriculum_diff(existing, merged)
        if fallback_weeks:
            fallback_list = ", ".join(f"Week {week:02d}" for week in fallback_weeks)
            print(
                "⚠ Notion snapshot is incomplete for "
                f"{fallback_list}; kept existing canonical data for those weeks."
            )
        if args.write:
            write_canonical_curriculum(merged)
            result = write_generated_outputs(merged)
            print(
                f"✓ Synced canonical curriculum from Notion "
                f"({diff['changed_count']} changed weeks, version {result['version']})"
            )
        else:
            print(
                f"✓ Notion snapshot validated "
                f"({diff['changed_count']} changed weeks, next version {diff['version_to']})"
            )
        return 0

    data = load_canonical_curriculum()
    errors = validate_curriculum(data)
    if errors:
        return _print_errors(errors)

    if args.command == "check":
        version = content_version(data)
        print(f"✓ Curriculum valid ({len(data)} weeks, version {version})")
        return 0

    if args.command == "build":
        result = write_generated_outputs(data)
        print(f"✓ Generated curriculum assets ({result['weeks']} weeks, version {result['version']})")
        return 0

    if args.command == "build-public":
        result = build_public_site(Path(args.output))
        print(f"✓ Built public site ({result['weeks']} weeks, version {result['version']})")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
