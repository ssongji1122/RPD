from __future__ import annotations

import re
from pathlib import Path

from runtime_paths import COURSE_SITE, WEEKS_DIR

LECTURE_SYNC_START = "<!-- AUTO:CURRICULUM-SYNC:START -->"
LECTURE_SYNC_END = "<!-- AUTO:CURRICULUM-SYNC:END -->"


def _find_lecture_note_path(week_num: int) -> Path | None:
    matches = sorted(WEEKS_DIR.glob(f"week{week_num:02d}-*/lecture-note.md"))
    return matches[0] if matches else None


def _render_link_list(items: list[dict]) -> list[str]:
    lines: list[str] = []
    for item in items or []:
        title = str(item.get("title", "")).strip()
        url = str(item.get("url", "")).strip()
        if title and url:
            lines.append(f"- [{title}]({url})")
    return lines


def render_curriculum_sync_markdown(week: dict) -> str:
    lines = [
        "## 커리큘럼 연동 요약",
        "",
        "> 이 섹션은 `course-site/data/curriculum.js` 기준으로 자동 갱신됩니다.",
        "",
    ]

    meta = []
    subtitle = str(week.get("subtitle", "")).strip()
    duration = str(week.get("duration", "")).strip()
    if subtitle:
        meta.append(f"- 핵심 키워드: {subtitle}")
    if duration:
        meta.append(f"- 예상 시간: {duration}")
    if meta:
        lines.extend(meta)
        lines.append("")

    steps = week.get("steps", []) or []
    if steps:
        lines.extend(["### 실습 단계", ""])
        for idx, step in enumerate(steps, start=1):
            title = str(step.get("title", "")).strip() or f"Step {idx}"
            copy = str(step.get("copy", "")).strip()
            lines.append(f"#### {idx}. {title}")
            lines.append("")
            if copy:
                lines.append(copy)
                lines.append("")

            image_path = str(step.get("image", "")).strip()
            if image_path:
                note_image_path = f"../../course-site/{image_path.lstrip('/')}"
                lines.append(f"![{title}]({note_image_path})")
                lines.append("")

            goals = [str(goal).strip() for goal in step.get("goal", []) if str(goal).strip()]
            if goals:
                lines.append("배울 것")
                lines.append("")
                lines.extend(f"- {goal}" for goal in goals)
                lines.append("")

            tasks = step.get("tasks", []) or []
            if tasks:
                lines.append("체크해볼 것")
                lines.append("")
                for task in tasks:
                    label = str(task.get("label", "")).strip()
                    detail = str(task.get("detail", "")).strip()
                    if not label:
                        continue
                    task_line = f"- {label}"
                    if detail:
                        task_line += f" ({detail})"
                    lines.append(task_line)
                lines.append("")

    shortcuts = week.get("shortcuts", []) or []
    if shortcuts:
        lines.extend(["### 핵심 단축키", ""])
        for shortcut in shortcuts:
            keys = str(shortcut.get("keys", "")).strip()
            action = str(shortcut.get("action", "")).strip()
            if keys and action:
                lines.append(f"- `{keys}`: {action}")
        lines.append("")

    assignment = week.get("assignment", {}) or {}
    assignment_title = str(assignment.get("title", "")).strip()
    assignment_description = str(assignment.get("description", "")).strip()
    assignment_checklist = [
        str(item).strip() for item in assignment.get("checklist", []) if str(item).strip()
    ]
    if assignment_title or assignment_description or assignment_checklist:
        lines.extend(["### 과제 한눈에 보기", ""])
        if assignment_title:
            lines.append(f"- 과제명: {assignment_title}")
        if assignment_description:
            lines.append(f"- 설명: {assignment_description}")
        if assignment_checklist:
            lines.append("- 제출 체크:")
            lines.extend(f"  - {item}" for item in assignment_checklist)
        lines.append("")

    mistakes = [str(item).strip() for item in week.get("mistakes", []) if str(item).strip()]
    if mistakes:
        lines.extend(["### 자주 막히는 지점", ""])
        lines.extend(f"- {item}" for item in mistakes)
        lines.append("")

    videos = _render_link_list(week.get("videos", []))
    if videos:
        lines.extend(["### 공식 영상 튜토리얼", ""])
        lines.extend(videos)
        lines.append("")

    docs = _render_link_list(week.get("docs", []))
    if docs:
        lines.extend(["### 공식 문서", ""])
        lines.extend(docs)
        lines.append("")

    while lines and lines[-1] == "":
        lines.pop()

    return "\n".join(lines)


def _upsert_lecture_sync_block(text: str, block_markdown: str) -> str:
    managed_block = f"{LECTURE_SYNC_START}\n{block_markdown}\n{LECTURE_SYNC_END}"

    if LECTURE_SYNC_START in text and LECTURE_SYNC_END in text:
        pattern = re.compile(
            rf"{re.escape(LECTURE_SYNC_START)}.*?{re.escape(LECTURE_SYNC_END)}",
            re.DOTALL,
        )
        return pattern.sub(managed_block, text, count=1)

    reference_match = re.search(r"^##\s+.*참고\s*자료.*$", text, re.MULTILINE)
    if reference_match:
        insert_at = reference_match.start()
        prefix = text[:insert_at].rstrip()
        suffix = text[insert_at:].lstrip("\n")
        return f"{prefix}\n\n{managed_block}\n\n{suffix}"

    return text.rstrip() + f"\n\n{managed_block}\n"


def _strip_duplicate_official_reference_sections(text: str) -> str:
    reference_match = re.search(r"^##\s+.*참고\s*자료.*$", text, re.MULTILINE)
    if not reference_match:
        return text

    next_section_match = re.search(r"^##\s+", text[reference_match.end() :], re.MULTILINE)
    section_start = reference_match.start()
    section_end = (
        reference_match.end() + next_section_match.start()
        if next_section_match
        else len(text)
    )
    section = text[section_start:section_end]

    for heading in ("공식 영상 튜토리얼", "공식 문서"):
        section = re.sub(
            rf"\n?^###\s+{heading}\s*$.*?(?=^###\s+|^##\s+|\Z)",
            "",
            section,
            flags=re.MULTILINE | re.DOTALL,
        )

    section = re.sub(r"\n{3,}", "\n\n", section).rstrip() + "\n"

    if re.fullmatch(r"##\s+.*참고\s*자료.*\n?", section.strip()):
        return (text[:section_start].rstrip() + "\n") + text[section_end:].lstrip("\n")

    return text[:section_start] + section + text[section_end:]


def sync_lecture_notes(data: list[dict]) -> list[Path]:
    updated_paths: list[Path] = []

    for week in data:
        week_num = int(week.get("week", 0) or 0)
        if week_num <= 0:
            continue

        lecture_path = _find_lecture_note_path(week_num)
        if not lecture_path or not lecture_path.exists():
            continue

        original = lecture_path.read_text(encoding="utf-8")
        block_markdown = render_curriculum_sync_markdown(week)
        updated = _upsert_lecture_sync_block(original, block_markdown)
        updated = _strip_duplicate_official_reference_sections(updated)
        if updated != original:
            lecture_path.write_text(updated, encoding="utf-8")
            updated_paths.append(lecture_path)

    return updated_paths
