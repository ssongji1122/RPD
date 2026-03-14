"""Parse lecture-note.md files into structured LectureNote objects.

The parser understands the consistent structure of RPD lecture notes:
- # Week NN: Title
- ## 학습 목표 (checkboxes)
- ## 이론 (Nmin) → theory sections with ### subsections
- ## 실습 (Nmin) → practice sections with ### Step N: Title (Nmin)
- ## 과제
- ## 참고 자료
"""

from __future__ import annotations

import re
from pathlib import Path

from .models import (
    ActionType,
    LearningObjective,
    LectureNote,
    Section,
    SectionType,
    Step,
    SubSection,
    SubStep,
)

# --- Regex Patterns ---

RE_WEEK_TITLE = re.compile(r"^#\s+Week\s+(\d+):\s*(.+)$", re.MULTILINE)
RE_OBJECTIVE = re.compile(r"^-\s*\[([ x])\]\s*(.+)$", re.MULTILINE)
RE_SECTION_HEADER = re.compile(
    r"^##\s+(이론|실습)\s*\((\d+)분?\)", re.MULTILINE
)
RE_STEP_HEADER = re.compile(
    r"^###\s+Step\s+(\d+):\s*(.+?)\s*\((\d+)분?\)", re.MULTILINE
)
RE_SUBSECTION_HEADER = re.compile(r"^###\s+(.+)$", re.MULTILINE)
RE_SUB_STEP = re.compile(r"^\d+\.\s+(.+)$", re.MULTILINE)
RE_SHORTCUT = re.compile(
    r"(?:^|\s)"
    r"("
    r"(?:Ctrl|Shift|Alt|Cmd|Tab|Numpad)\s*\+?\s*[A-Z0-9]+"
    r"|[A-Z]\s+키"
    r"|[A-Z]\s*\("
    r")"
)
RE_URL = re.compile(r"https?://[^\s)]+")
RE_ASSIGNMENT_SECTION = re.compile(r"^##\s+과제", re.MULTILINE)
RE_REFERENCE_SECTION = re.compile(r"^##\s+참고\s*자료", re.MULTILINE)


def parse_lecture_note(filepath: Path) -> LectureNote:
    """Parse a lecture-note.md file into a structured LectureNote."""
    text = filepath.read_text(encoding="utf-8")
    return _parse_text(text, filepath)


def _parse_text(text: str, source_path: Path | None = None) -> LectureNote:
    """Parse lecture note markdown text."""
    # Extract week number and title
    week_match = RE_WEEK_TITLE.search(text)
    if not week_match:
        # Fallback: try to extract from directory name (e.g., week02-blender-basics)
        week = 0
        title = "Unknown"
        if source_path:
            dir_name = source_path.parent.name
            m = re.match(r"week(\d+)", dir_name)
            if m:
                week = int(m.group(1))
            title = dir_name
    else:
        week = int(week_match.group(1))
        title = week_match.group(2).strip()

    # Extract learning objectives
    objectives = [
        LearningObjective(text=m.group(2).strip(), completed=m.group(1) == "x")
        for m in RE_OBJECTIVE.finditer(text)
    ]

    # Extract sections (theory + practice)
    sections = _parse_sections(text)

    # Extract assignment text
    assignment_text = _extract_section_text(text, RE_ASSIGNMENT_SECTION, RE_REFERENCE_SECTION)

    # Extract reference links
    ref_section = _extract_section_text(text, RE_REFERENCE_SECTION)
    references = RE_URL.findall(ref_section) if ref_section else []

    return LectureNote(
        week=week,
        title=title,
        learning_objectives=objectives,
        sections=sections,
        assignment_text=assignment_text,
        references=references,
        source_path=source_path,
    )


def _parse_sections(text: str) -> list[Section]:
    """Parse ## 이론 and ## 실습 sections."""
    sections: list[Section] = []

    # Find all section headers with their positions
    section_matches = list(RE_SECTION_HEADER.finditer(text))

    for i, match in enumerate(section_matches):
        section_type_str = match.group(1)
        estimated_minutes = int(match.group(2))
        section_type = SectionType.THEORY if section_type_str == "이론" else SectionType.PRACTICE

        # Get section content (from this header to next section header or end markers)
        start = match.end()
        end = _find_section_end(text, start, section_matches, i)
        section_content = text[start:end].strip()

        if section_type == SectionType.PRACTICE:
            steps = _parse_steps(section_content)
            sections.append(
                Section(
                    type=section_type,
                    title=f"{section_type_str} ({estimated_minutes}분)",
                    estimated_minutes=estimated_minutes,
                    content_raw=section_content,
                    steps=steps,
                )
            )
        else:
            subsections = _parse_subsections(section_content)
            sections.append(
                Section(
                    type=section_type,
                    title=f"{section_type_str} ({estimated_minutes}분)",
                    estimated_minutes=estimated_minutes,
                    content_raw=section_content,
                    subsections=subsections,
                )
            )

    return sections


def _find_section_end(
    text: str, start: int, section_matches: list[re.Match], current_idx: int
) -> int:
    """Find where a section ends (next ## section or ## 과제)."""
    # Check for next section header
    if current_idx + 1 < len(section_matches):
        return section_matches[current_idx + 1].start()

    # Check for assignment or reference section
    for pattern in [RE_ASSIGNMENT_SECTION, RE_REFERENCE_SECTION]:
        m = pattern.search(text, start)
        if m:
            return m.start()

    return len(text)


def _parse_steps(content: str) -> list[Step]:
    """Parse ### Step N: Title (Nmin) blocks within a practice section."""
    steps: list[Step] = []
    step_matches = list(RE_STEP_HEADER.finditer(content))

    for i, match in enumerate(step_matches):
        number = int(match.group(1))
        title = match.group(2).strip()
        estimated_minutes = int(match.group(3))

        # Get step content
        start = match.end()
        end = step_matches[i + 1].start() if i + 1 < len(step_matches) else len(content)
        step_content = content[start:end].strip()

        # Parse sub-steps (numbered items)
        sub_steps = _parse_sub_steps(step_content)

        # Extract shortcuts mentioned in the content
        shortcuts = _extract_shortcuts(step_content)

        # Extract URLs
        urls = RE_URL.findall(step_content)

        # Determine action type
        action_type = _classify_action_type(step_content, urls)

        steps.append(
            Step(
                number=number,
                title=title,
                estimated_minutes=estimated_minutes,
                content_raw=step_content,
                sub_steps=sub_steps,
                action_type=action_type,
                shortcuts=shortcuts,
                urls=urls,
            )
        )

    return steps


def _parse_sub_steps(content: str) -> list[SubStep]:
    """Parse numbered sub-steps (1., 2., 3., ...) within a step."""
    sub_steps: list[SubStep] = []
    for i, match in enumerate(RE_SUB_STEP.finditer(content), start=1):
        text = match.group(1).strip()
        shortcuts = _extract_shortcuts(text)
        sub_steps.append(SubStep(number=i, text=text, shortcuts=shortcuts))
    return sub_steps


def _parse_subsections(content: str) -> list[SubSection]:
    """Parse ### subsections within a theory section."""
    subsections: list[SubSection] = []
    matches = list(RE_SUBSECTION_HEADER.finditer(content))

    # Skip if matches look like Step headers (already handled)
    matches = [m for m in matches if not m.group(1).startswith("Step ")]

    for i, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        sub_content = content[start:end].strip()

        subsections.append(
            SubSection(
                title=title,
                content_raw=sub_content,
                has_table="|" in sub_content and "---" in sub_content,
                has_list=bool(re.search(r"^[-*]\s+", sub_content, re.MULTILINE)),
            )
        )

    return subsections


def _extract_shortcuts(text: str) -> list[str]:
    """Extract keyboard shortcuts from text."""
    shortcuts: list[str] = []

    # Pattern: Key combinations like Ctrl+A, Shift+F, G+X
    combo_pattern = re.compile(
        r"\b((?:Ctrl|Shift|Alt|Cmd)\s*\+\s*[A-Z0-9]+(?:\s*\+\s*[A-Z0-9]+)*)\b"
    )
    shortcuts.extend(m.group(1) for m in combo_pattern.finditer(text))

    # Pattern: Single key references like "G (Grab/이동)" or "E 키"
    single_key_pattern = re.compile(
        r"\b([A-Z])\s*(?:\(|키|key\b)"
    )
    shortcuts.extend(m.group(1) for m in single_key_pattern.finditer(text))

    # Pattern: Numpad keys
    numpad_pattern = re.compile(r"Numpad\s+\d+")
    shortcuts.extend(m.group(0) for m in numpad_pattern.finditer(text))

    return list(dict.fromkeys(shortcuts))  # Deduplicate preserving order


def _classify_action_type(content: str, urls: list[str]) -> ActionType:
    """Classify what kind of screen activity a step requires."""
    has_urls = bool(urls)
    has_blender_ops = bool(
        re.search(
            r"(?:Blender|Object Mode|Edit Mode|Sculpt Mode|Viewport|"
            r"Properties Panel|Outliner|Shift\+A|Right-click|Tab 키)",
            content,
        )
    )

    if has_urls and has_blender_ops:
        return ActionType.BLENDER_AND_BROWSER
    elif has_urls:
        return ActionType.BROWSER
    elif has_blender_ops:
        return ActionType.BLENDER
    else:
        return ActionType.NARRATION_ONLY


def _extract_section_text(
    text: str, start_pattern: re.Pattern, end_pattern: re.Pattern | None = None
) -> str:
    """Extract text between two section markers."""
    start_match = start_pattern.search(text)
    if not start_match:
        return ""

    start = start_match.end()

    if end_pattern:
        end_match = end_pattern.search(text, start)
        end = end_match.start() if end_match else len(text)
    else:
        # Find next ## header or end of text
        next_header = re.search(r"^##\s+", text[start:], re.MULTILINE)
        end = start + next_header.start() if next_header else len(text)

    return text[start:end].strip()
