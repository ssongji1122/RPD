from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from lecture_notes_sync import LECTURE_SYNC_END, LECTURE_SYNC_START

WEEK_DIR_RE = re.compile(r"week(?P<week>\d+)-")
WEEK_TITLE_RE = re.compile(r"^#\s*Week\s+(?P<week>\d+)\s*:\s*(?P<title>.+?)\s*$", re.MULTILINE)
MANAGED_BLOCK_RE = re.compile(
    rf"{re.escape(LECTURE_SYNC_START)}\n?(?P<body>.*?){re.escape(LECTURE_SYNC_END)}",
    re.DOTALL,
)
CHECKBOX_RE = re.compile(r"^- \[[ xX]\]\s*(.+?)\s*$")
BULLET_RE = re.compile(r"^\s*-\s+(.+?)\s*$")
LINK_RE = re.compile(r"^\s*-\s+\[(?P<title>[^\]]+)\]\((?P<url>[^)]+)\)\s*$")
STEP_RE = re.compile(r"^####\s+(?:\d+\.\s*)?(?P<title>.+?)\s*$")
SHORTCUT_RE = re.compile(r"^- `(?P<keys>[^`]+)`: (?P<action>.+)$")
IMAGE_RE = re.compile(r"^!\[[^\]]*\]\((?P<path>[^)]+)\)$")
ASSIGNMENT_TITLE_RE = re.compile(r"^#\s*(?P<title>.+?)\s*$", re.MULTILINE)
H2_RE = re.compile(r"^##\s+(?P<title>.+?)\s*$", re.MULTILINE)

VIDEO_HOST_TOKENS = (
    "youtube.com",
    "youtu.be",
    "studio.blender.org",
    "vimeo.com",
)


def _week_dirs(weeks_dir: Path) -> list[Path]:
    week_dirs = []
    for path in weeks_dir.iterdir():
        if not path.is_dir():
            continue
        if WEEK_DIR_RE.match(path.name):
            week_dirs.append(path)
    return sorted(week_dirs, key=lambda path: int(WEEK_DIR_RE.match(path.name).group("week")))


def _parse_week_number_from_dir(path: Path) -> int:
    match = WEEK_DIR_RE.match(path.name)
    if not match:
        raise ValueError(f"Invalid week directory name: {path.name}")
    return int(match.group("week"))


def _extract_managed_block(text: str) -> str:
    match = MANAGED_BLOCK_RE.search(text)
    if not match:
        raise ValueError("Managed curriculum block not found in lecture note")
    return match.group("body").strip()


def _strip_managed_block(text: str) -> str:
    return MANAGED_BLOCK_RE.sub("", text)


def _extract_week_title(text: str, fallback_week_num: int) -> tuple[int, str]:
    match = WEEK_TITLE_RE.search(text)
    if match:
        return int(match.group("week")), match.group("title").strip()

    heading = ASSIGNMENT_TITLE_RE.search(text)
    if heading:
        raw_title = heading.group("title").strip()
        if ":" in raw_title:
            return fallback_week_num, raw_title.split(":", 1)[1].strip()
        return fallback_week_num, raw_title

    return fallback_week_num, f"Week {fallback_week_num:02d}"


def _normalize_note_image_path(path: str) -> str:
    cleaned = path.strip()
    if cleaned.startswith("../../course-site/"):
        return cleaned[len("../../course-site/") :]
    if cleaned.startswith("course-site/"):
        return cleaned[len("course-site/") :]
    return cleaned


def _parse_task_bullet(text: str, *, week_num: int, step_index: int, task_index: int, existing_task: dict | None) -> dict[str, str]:
    label = text.strip()
    detail = ""

    if existing_task:
        existing_label = str(existing_task.get("label", "")).strip()
        existing_detail = str(existing_task.get("detail", "")).strip()
        expected = existing_label
        if existing_detail:
            expected = f"{expected} ({existing_detail})"
        if label == expected:
            return {
                "id": str(existing_task.get("id", "")).strip() or f"w{week_num:02d}-s{step_index:02d}-t{task_index:02d}",
                "label": existing_label,
                "detail": existing_detail,
            }

    detail_match = re.match(r"^(?P<label>.+?)\s+\((?P<detail>.+)\)\s*$", label)
    if detail_match:
        label = detail_match.group("label").strip()
        detail = detail_match.group("detail").strip()

    task_id = ""
    if existing_task:
        task_id = str(existing_task.get("id", "")).strip()
    if not task_id:
        task_id = f"w{week_num:02d}-s{step_index:02d}-t{task_index:02d}"

    return {"id": task_id, "label": label, "detail": detail}


def _parse_bullet_lines(lines: list[str], start_index: int) -> tuple[list[str], int]:
    bullets: list[str] = []
    index = start_index
    while index < len(lines):
        stripped = lines[index].strip()
        if not stripped:
            index += 1
            continue
        if stripped.startswith("### ") or stripped.startswith("#### "):
            break
        match = BULLET_RE.match(lines[index])
        if not match:
            break
        bullets.append(match.group(1).strip())
        index += 1
    return bullets, index


def parse_learning_goals(text: str) -> list[str]:
    lines = text.splitlines()
    in_section = False
    goals: list[str] = []
    for raw_line in lines:
        stripped = raw_line.strip()
        if stripped.startswith("## ") and "학습 목표" in stripped:
            in_section = True
            continue
        if in_section and stripped.startswith("## "):
            break
        if not in_section:
            continue
        match = CHECKBOX_RE.match(stripped)
        if match:
            goals.append(match.group(1).strip())
    return goals


def _section_body(text: str, titles: tuple[str, ...]) -> str:
    lines = text.splitlines()
    collecting = False
    buffer: list[str] = []
    for raw_line in lines:
        stripped = raw_line.strip()
        if stripped.startswith("## "):
            title = stripped[3:].strip()
            if collecting:
                break
            if title in titles:
                collecting = True
                continue
        if not collecting:
            continue
        buffer.append(raw_line)
    return "\n".join(buffer).strip()


def parse_reference_links(text: str) -> list[dict[str, str]]:
    body = _section_body(_strip_managed_block(text), ("참고 자료", "Notion 참고 자료"))
    resources: list[dict[str, str]] = []
    for line in body.splitlines():
        match = LINK_RE.match(line)
        if match:
            resources.append({"title": match.group("title").strip(), "url": match.group("url").strip()})
    return resources


def _classify_resources(resources: list[dict[str, str]]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    videos: list[dict[str, str]] = []
    docs: list[dict[str, str]] = []
    for item in resources:
        url = item["url"]
        if any(token in url for token in VIDEO_HOST_TOKENS):
            videos.append(item)
        else:
            docs.append(item)
    return videos, docs


def _first_paragraph(body: str) -> str:
    paragraph: list[str] = []
    for raw_line in body.splitlines():
        stripped = raw_line.strip()
        if not stripped:
            if paragraph:
                break
            continue
        if stripped.startswith("#") or stripped.startswith("- ") or stripped.startswith("|"):
            if paragraph:
                break
            continue
        paragraph.append(stripped)
    return " ".join(paragraph).strip()


def parse_assignment_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"title": "", "description": "", "checklist": [], "resources": []}

    text = path.read_text(encoding="utf-8")
    _, title = _extract_week_title(text, 0)
    description = _first_paragraph(_section_body(text, ("과제 내용", "과제 개요")))

    submit_method = _section_body(text, ("제출 방법",))
    checklist: list[str] = []
    for line in submit_method.splitlines():
        match = BULLET_RE.match(line)
        if match:
            checklist.append(match.group(1).strip())

    resources = parse_reference_links(text)
    return {
        "title": title,
        "description": description,
        "checklist": checklist,
        "resources": resources,
    }


def parse_summary(text: str) -> str:
    summary = _first_paragraph(_section_body(_strip_managed_block(text), ("핵심 정리",)))
    if summary:
        return summary
    return _first_paragraph(_section_body(_strip_managed_block(text), ("이론 (30분)", "이론 (20분)", "이론 (40분)")))


def parse_managed_week(lecture_text: str, week_num: int) -> dict[str, Any]:
    _, title = _extract_week_title(lecture_text, week_num)
    block = _extract_managed_block(lecture_text)
    lines = block.splitlines()
    parsed: dict[str, Any] = {
        "week": week_num,
        "title": title,
        "subtitle": "",
        "duration": "",
        "steps": [],
        "shortcuts": [],
        "assignment": {"title": "", "description": "", "checklist": []},
        "mistakes": [],
        "videos": [],
        "docs": [],
        "topics": parse_learning_goals(_strip_managed_block(lecture_text)),
        "summary": parse_summary(lecture_text),
    }

    index = 0
    while index < len(lines):
        stripped = lines[index].strip()
        if stripped.startswith("- 핵심 키워드:"):
            parsed["subtitle"] = stripped.split(":", 1)[1].strip()
            index += 1
            continue
        if stripped.startswith("- 예상 시간:"):
            parsed["duration"] = stripped.split(":", 1)[1].strip()
            index += 1
            continue

        if stripped == "### 실습 단계":
            index += 1
            step_index = 0
            while index < len(lines):
                stripped = lines[index].strip()
                if stripped.startswith("### "):
                    break
                if not stripped:
                    index += 1
                    continue
                step_match = STEP_RE.match(stripped)
                if not step_match:
                    index += 1
                    continue

                step_index += 1
                step_title = step_match.group("title").strip()
                index += 1
                copy_lines: list[str] = []
                goals: list[str] = []
                task_lines: list[str] = []
                image = ""

                while index < len(lines):
                    stripped = lines[index].strip()
                    if stripped.startswith("#### ") or stripped.startswith("### "):
                        break
                    if not stripped:
                        index += 1
                        continue
                    image_match = IMAGE_RE.match(stripped)
                    if image_match:
                        image = _normalize_note_image_path(image_match.group("path"))
                        index += 1
                        continue
                    if stripped == "배울 것":
                        index += 1
                        goals, index = _parse_bullet_lines(lines, index)
                        continue
                    if stripped == "체크해볼 것":
                        index += 1
                        task_lines, index = _parse_bullet_lines(lines, index)
                        continue
                    copy_lines.append(stripped)
                    index += 1

                step = {
                    "title": step_title,
                    "copy": "\n".join(copy_lines).strip(),
                    "goal": goals,
                    "done": [],
                    "tasks": task_lines,
                }
                if image:
                    step["image"] = image
                parsed["steps"].append(step)
            continue

        if stripped == "### 핵심 단축키":
            index += 1
            while index < len(lines):
                stripped = lines[index].strip()
                if stripped.startswith("### "):
                    break
                if not stripped:
                    index += 1
                    continue
                match = SHORTCUT_RE.match(stripped)
                if match:
                    parsed["shortcuts"].append(
                        {"keys": match.group("keys").strip(), "action": match.group("action").strip()}
                    )
                index += 1
            continue

        if stripped == "### 과제 한눈에 보기":
            index += 1
            while index < len(lines):
                stripped = lines[index].strip()
                if stripped.startswith("### "):
                    break
                if not stripped:
                    index += 1
                    continue
                if stripped.startswith("- 과제명:"):
                    parsed["assignment"]["title"] = stripped.split(":", 1)[1].strip()
                elif stripped.startswith("- 설명:"):
                    parsed["assignment"]["description"] = stripped.split(":", 1)[1].strip()
                elif stripped.startswith("- 제출 체크:"):
                    index += 1
                    checklist, index = _parse_bullet_lines(lines, index)
                    parsed["assignment"]["checklist"] = checklist
                    continue
                index += 1
            continue

        if stripped == "### 자주 막히는 지점":
            index += 1
            mistakes, index = _parse_bullet_lines(lines, index)
            parsed["mistakes"] = mistakes
            continue

        if stripped == "### 공식 영상 튜토리얼":
            index += 1
            while index < len(lines):
                stripped = lines[index].strip()
                if stripped.startswith("### "):
                    break
                if not stripped:
                    index += 1
                    continue
                match = LINK_RE.match(lines[index])
                if match:
                    parsed["videos"].append(
                        {"title": match.group("title").strip(), "url": match.group("url").strip()}
                    )
                index += 1
            continue

        if stripped == "### 공식 문서":
            index += 1
            while index < len(lines):
                stripped = lines[index].strip()
                if stripped.startswith("### "):
                    break
                if not stripped:
                    index += 1
                    continue
                match = LINK_RE.match(lines[index])
                if match:
                    parsed["docs"].append(
                        {"title": match.group("title").strip(), "url": match.group("url").strip()}
                    )
                index += 1
            continue

        index += 1

    return parsed


def _merge_resources(primary: list[dict[str, str]], *fallback_sets: list[dict[str, str]]) -> list[dict[str, str]]:
    if primary:
        return primary
    seen: set[tuple[str, str]] = set()
    merged: list[dict[str, str]] = []
    for fallback in fallback_sets:
        for item in fallback:
            key = (item["title"], item["url"])
            if key in seen:
                continue
            seen.add(key)
            merged.append(item)
    return merged


def _merge_step(parsed_step: dict[str, Any], existing_step: dict[str, Any], week_num: int, step_index: int) -> dict[str, Any]:
    merged = {
        "title": existing_step.get("title", "") or parsed_step.get("title", ""),
        "copy": existing_step.get("copy", "") or parsed_step.get("copy", ""),
        "goal": existing_step.get("goal", []) or parsed_step.get("goal", []),
        "done": existing_step.get("done", []) or parsed_step.get("done", []),
        "tasks": [],
    }

    if existing_step.get("image") or parsed_step.get("image"):
        merged["image"] = existing_step.get("image") or parsed_step.get("image")

    for key in ("showme", "widgets", "link", "images", "downloads", "clips", "video", "sectionTitle"):
        if existing_step.get(key):
            merged[key] = existing_step.get(key)

    existing_tasks = existing_step.get("tasks", []) if isinstance(existing_step.get("tasks"), list) else []
    parsed_tasks = parsed_step.get("tasks", [])
    if existing_tasks:
        merged["tasks"] = existing_tasks
        return merged

    for task_index, task_line in enumerate(parsed_tasks, start=1):
        existing_task = existing_tasks[task_index - 1] if task_index - 1 < len(existing_tasks) else None
        merged["tasks"].append(
            _parse_task_bullet(
                task_line,
                week_num=week_num,
                step_index=step_index,
                task_index=task_index,
                existing_task=existing_task,
            )
        )

    if not merged["tasks"] and existing_tasks:
        merged["tasks"] = existing_tasks

    return merged


def _default_week(week_num: int) -> dict[str, Any]:
    return {
        "week": week_num,
        "status": "upcoming",
        "title": f"Week {week_num:02d}",
        "subtitle": "",
        "summary": "",
        "duration": "",
        "topics": [],
        "steps": [],
        "shortcuts": [],
        "explore": [],
        "assignment": {"title": "", "description": "", "checklist": []},
        "mistakes": [],
        "videos": [],
        "docs": [],
    }


def merge_markdown_week(
    parsed_week: dict[str, Any],
    assignment_data: dict[str, Any],
    lecture_refs: list[dict[str, str]],
    existing_week: dict[str, Any] | None,
) -> dict[str, Any]:
    week_num = parsed_week["week"]
    base = dict(_default_week(week_num))
    if existing_week:
        base.update(existing_week)
    existing_payload = existing_week or {}

    lecture_videos, lecture_docs = _classify_resources(lecture_refs)
    assignment_videos, assignment_docs = _classify_resources(assignment_data.get("resources", []))
    existing_assignment = (
        existing_week.get("assignment", {})
        if existing_week and isinstance(existing_week.get("assignment"), dict)
        else {}
    )

    merged: dict[str, Any] = dict(base)
    merged["title"] = existing_payload.get("title") or parsed_week.get("title") or f"Week {week_num:02d}"
    merged["subtitle"] = existing_payload.get("subtitle", "") or parsed_week.get("subtitle")
    merged["summary"] = existing_payload.get("summary") or parsed_week.get("summary") or merged["subtitle"]
    merged["duration"] = existing_payload.get("duration", "") or parsed_week.get("duration")
    merged["topics"] = existing_payload.get("topics") or parsed_week.get("topics") or [merged["title"]]
    merged["shortcuts"] = existing_payload.get("shortcuts", []) or parsed_week.get("shortcuts")
    merged["explore"] = existing_payload.get("explore", [])
    merged["mistakes"] = existing_payload.get("mistakes", []) or parsed_week.get("mistakes")
    merged["videos"] = _merge_resources(
        existing_payload.get("videos", []),
        parsed_week.get("videos", []),
        lecture_videos,
        assignment_videos,
    )
    merged["docs"] = _merge_resources(
        existing_payload.get("docs", []),
        parsed_week.get("docs", []),
        lecture_docs,
        assignment_docs,
    )
    merged["assignment"] = {
        "title": (
            existing_assignment.get("title", "")
            or parsed_week.get("assignment", {}).get("title")
            or assignment_data.get("title")
        ),
        "description": (
            existing_assignment.get("description", "")
            or parsed_week.get("assignment", {}).get("description")
            or assignment_data.get("description")
        ),
        "checklist": (
            existing_assignment.get("checklist", [])
            or assignment_data.get("checklist")
            or parsed_week.get("assignment", {}).get("checklist")
        ),
    }

    parsed_steps = parsed_week.get("steps", [])
    existing_steps = existing_payload.get("steps", []) if isinstance(existing_payload.get("steps"), list) else []
    merged_steps: list[dict[str, Any]] = []
    for step_index, parsed_step in enumerate(parsed_steps, start=1):
        existing_step = existing_steps[step_index - 1] if step_index - 1 < len(existing_steps) else {}
        merged_steps.append(_merge_step(parsed_step, existing_step, week_num, step_index))
    merged["steps"] = merged_steps or existing_steps

    return merged


def build_curriculum_from_markdown(weeks_dir: Path, existing_curriculum: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    existing_by_week = {
        int(week.get("week", 0)): week for week in (existing_curriculum or []) if isinstance(week, dict)
    }
    merged_weeks: list[dict[str, Any]] = []
    seen_weeks: set[int] = set()

    for week_dir in _week_dirs(weeks_dir):
        week_num = _parse_week_number_from_dir(week_dir)
        lecture_path = week_dir / "lecture-note.md"
        lecture_text = lecture_path.read_text(encoding="utf-8") if lecture_path.exists() else ""
        assignment_data = parse_assignment_file(week_dir / "assignment.md")
        lecture_refs = parse_reference_links(lecture_text) if lecture_text else []

        if lecture_text:
            try:
                parsed_week = parse_managed_week(lecture_text, week_num)
            except ValueError:
                _, title = _extract_week_title(lecture_text, week_num)
                parsed_week = {
                    "week": week_num,
                    "title": title,
                    "subtitle": "",
                    "duration": "",
                    "steps": [],
                    "shortcuts": [],
                    "assignment": {"title": "", "description": "", "checklist": []},
                    "mistakes": [],
                    "videos": [],
                    "docs": [],
                    "topics": parse_learning_goals(_strip_managed_block(lecture_text)),
                    "summary": parse_summary(lecture_text),
                }
        else:
            parsed_week = {
                "week": week_num,
                "title": f"Week {week_num:02d}",
                "subtitle": "",
                "duration": "",
                "steps": [],
                "shortcuts": [],
                "assignment": {"title": "", "description": "", "checklist": []},
                "mistakes": [],
                "videos": [],
                "docs": [],
                "topics": [],
                "summary": "",
            }

        merged_weeks.append(
            merge_markdown_week(
                parsed_week,
                assignment_data,
                lecture_refs,
                existing_by_week.get(week_num),
            )
        )
        seen_weeks.add(week_num)

    for week_num, existing_week in existing_by_week.items():
        if week_num not in seen_weeks:
            merged_weeks.append(existing_week)

    return sorted(merged_weeks, key=lambda week: int(week.get("week", 0)))
