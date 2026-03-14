"""Generate natural Korean narration scripts from parsed lecture notes.

Transforms structured lecture content into conversational narration suitable
for video voiceover. Can use Claude API for high-quality generation, or fall
back to a simpler template-based approach.
"""

from __future__ import annotations

import re

from .models import (
    ActionType,
    LectureNote,
    NarrationBlock,
    Section,
    SectionType,
    SegmentSection,
    Step,
    VideoSegment,
    VisualType,
)

# Average Korean speech rate: ~3.5 syllables/second → ~250 chars/minute
CHARS_PER_MINUTE = 250
CHARS_PER_SECOND = CHARS_PER_MINUTE / 60


def generate_segments(lecture: LectureNote) -> list[VideoSegment]:
    """Split a lecture into 2-3 video segments and generate narration scripts."""
    segments: list[VideoSegment] = []

    # Segment 1: Theory + early practice steps
    # Segment 2+: Remaining practice steps
    theory_sections = lecture.theory_sections
    practice_sections = lecture.practice_sections

    all_steps: list[Step] = []
    for ps in practice_sections:
        all_steps.extend(ps.steps)

    # Split steps into segments of ~20-30min each
    step_groups = _split_steps_by_time(all_steps, target_minutes=25)

    seg_num = 1

    # First segment: Theory + first group of steps
    if theory_sections:
        first_group = step_groups[0] if step_groups else []
        seg = _build_segment(
            lecture, seg_num, theory_sections, first_group
        )
        segments.append(seg)
        seg_num += 1
        step_groups = step_groups[1:]  # Remove first group

    # Additional segments for remaining step groups
    for group in step_groups:
        seg = _build_segment(lecture, seg_num, [], group)
        segments.append(seg)
        seg_num += 1

    # If no segments created, create one with all content
    if not segments:
        seg = _build_segment(lecture, 1, theory_sections, all_steps)
        segments.append(seg)

    return segments


def _split_steps_by_time(
    steps: list[Step], target_minutes: int = 25
) -> list[list[Step]]:
    """Group steps so each group is ~target_minutes."""
    if not steps:
        return []

    groups: list[list[Step]] = []
    current_group: list[Step] = []
    current_time = 0

    for step in steps:
        step_time = step.estimated_minutes or 10
        if current_time + step_time > target_minutes * 1.3 and current_group:
            groups.append(current_group)
            current_group = [step]
            current_time = step_time
        else:
            current_group.append(step)
            current_time += step_time

    if current_group:
        groups.append(current_group)

    return groups


def _build_segment(
    lecture: LectureNote,
    seg_num: int,
    theory_sections: list[Section],
    steps: list[Step],
) -> VideoSegment:
    """Build a VideoSegment with narration blocks."""
    segment_id = f"week{lecture.week:02d}-seg{seg_num:02d}"

    # Build title from content
    if theory_sections and steps:
        title = f"{lecture.title} - 이론 & 실습 Part {seg_num}"
    elif theory_sections:
        title = f"{lecture.title} - 이론"
    elif steps:
        step_titles = [s.title for s in steps[:2]]
        title = f"{lecture.title} - " + ", ".join(step_titles)
    else:
        title = lecture.title

    # Generate narration blocks
    blocks: list[NarrationBlock] = []
    seg_sections: list[SegmentSection] = []
    block_counter = 0

    # Intro block
    block_counter += 1
    blocks.append(
        NarrationBlock(
            id=f"{segment_id}-intro",
            text=_generate_intro(lecture, seg_num),
            timing_hint_seconds=8.0,
            visual_type=VisualType.OVERLAY,
            visual_ref="title_card",
            pause_after_seconds=1.0,
        )
    )

    # Theory narration
    for section in theory_sections:
        section_blocks = _generate_theory_narration(segment_id, section, block_counter)
        blocks.extend(section_blocks)
        block_counter += len(section_blocks)
        seg_sections.append(
            SegmentSection(
                title=section.title,
                section_type=SectionType.THEORY,
                narration_blocks=section_blocks,
            )
        )

    # Practice steps narration
    if steps:
        step_blocks = _generate_practice_narration(segment_id, steps, block_counter)
        blocks.extend(step_blocks)
        seg_sections.append(
            SegmentSection(
                title="실습",
                section_type=SectionType.PRACTICE,
                narration_blocks=step_blocks,
                action_type=_dominant_action_type(steps),
            )
        )

    # Outro block
    blocks.append(
        NarrationBlock(
            id=f"{segment_id}-outro",
            text=_generate_outro(lecture, seg_num, steps),
            timing_hint_seconds=6.0,
            visual_type=VisualType.OVERLAY,
            visual_ref="outro_card",
            pause_after_seconds=0.5,
        )
    )

    # Calculate target duration from narration text length
    total_chars = sum(len(b.text) for b in blocks)
    target_seconds = int(total_chars / CHARS_PER_SECOND) + len(blocks) * 2  # + pauses

    return VideoSegment(
        segment_id=segment_id,
        week=lecture.week,
        segment_number=seg_num,
        title=title,
        sections=seg_sections,
        target_duration_seconds=target_seconds,
        narration_blocks=blocks,
    )


def _generate_intro(lecture: LectureNote, seg_num: int) -> str:
    """Generate intro narration."""
    if seg_num == 1:
        objectives = " ".join(
            f"{i+1}. {obj.text}" for i, obj in enumerate(lecture.learning_objectives[:3])
        )
        return (
            f"안녕하세요, 로봇 프로덕트 디자인 {lecture.week}주차 수업을 시작하겠습니다. "
            f"오늘의 주제는 '{lecture.title}'입니다. "
            f"오늘 수업에서 다룰 내용은 다음과 같습니다. {objectives}"
        )
    else:
        return (
            f"{lecture.week}주차 수업의 Part {seg_num}를 이어서 진행하겠습니다. "
            f"이번 파트에서는 실습을 진행합니다."
        )


def _generate_theory_narration(
    segment_id: str, section: Section, start_counter: int
) -> list[NarrationBlock]:
    """Generate narration blocks for a theory section."""
    blocks: list[NarrationBlock] = []
    counter = start_counter

    # Section transition
    blocks.append(
        NarrationBlock(
            id=f"{segment_id}-theory-header",
            text="먼저 이론 부분을 살펴보겠습니다.",
            timing_hint_seconds=3.0,
            visual_type=VisualType.OVERLAY,
            visual_ref="section_header:이론",
            pause_after_seconds=0.5,
        )
    )
    counter += 1

    # Process subsections
    for subsection in section.subsections:
        narration_text = _markdown_to_narration(subsection.content_raw, subsection.title)

        visual = VisualType.SLIDE
        if subsection.has_table:
            visual = VisualType.OVERLAY  # Animated table

        est_seconds = len(narration_text) / CHARS_PER_SECOND

        blocks.append(
            NarrationBlock(
                id=f"{segment_id}-theory-{counter:03d}",
                text=narration_text,
                timing_hint_seconds=est_seconds,
                visual_type=visual,
                visual_ref=f"slide:{subsection.title}",
                pause_after_seconds=0.8,
            )
        )
        counter += 1

    # Fallback: if no subsections, use raw content
    if not section.subsections and section.content_raw:
        narration_text = _markdown_to_narration(section.content_raw, section.title)
        blocks.append(
            NarrationBlock(
                id=f"{segment_id}-theory-{counter:03d}",
                text=narration_text,
                timing_hint_seconds=len(narration_text) / CHARS_PER_SECOND,
                visual_type=VisualType.SLIDE,
                visual_ref="slide:theory",
            )
        )

    return blocks


def _generate_practice_narration(
    segment_id: str, steps: list[Step], start_counter: int
) -> list[NarrationBlock]:
    """Generate narration blocks for practice steps."""
    blocks: list[NarrationBlock] = []
    counter = start_counter

    # Section transition
    blocks.append(
        NarrationBlock(
            id=f"{segment_id}-practice-header",
            text="이제 실습을 진행하겠습니다. 함께 따라해 보세요.",
            timing_hint_seconds=4.0,
            visual_type=VisualType.OVERLAY,
            visual_ref="section_header:실습",
            pause_after_seconds=1.0,
        )
    )
    counter += 1

    for step in steps:
        # Step intro
        blocks.append(
            NarrationBlock(
                id=f"{segment_id}-step{step.number}-intro",
                text=f"Step {step.number}, {step.title}입니다.",
                timing_hint_seconds=3.0,
                visual_type=VisualType.OVERLAY,
                visual_ref=f"step_indicator:{step.number}:{step.title}",
                pause_after_seconds=0.5,
            )
        )
        counter += 1

        # Sub-step narrations
        visual = (
            VisualType.SCREEN_RECORDING
            if step.action_type != ActionType.NARRATION_ONLY
            else VisualType.SLIDE
        )

        for sub_step in step.sub_steps:
            narration = _sub_step_to_narration(sub_step.text)
            est_seconds = max(len(narration) / CHARS_PER_SECOND, 3.0)

            blocks.append(
                NarrationBlock(
                    id=f"{segment_id}-step{step.number}-{counter:03d}",
                    text=narration,
                    timing_hint_seconds=est_seconds,
                    visual_type=visual,
                    visual_ref=f"recording:step{step.number}",
                    pause_after_seconds=1.0,
                )
            )
            counter += 1

        # If no sub-steps, create narration from raw content
        if not step.sub_steps and step.content_raw:
            narration = _markdown_to_narration(step.content_raw, step.title)
            blocks.append(
                NarrationBlock(
                    id=f"{segment_id}-step{step.number}-content",
                    text=narration,
                    timing_hint_seconds=len(narration) / CHARS_PER_SECOND,
                    visual_type=visual,
                    visual_ref=f"recording:step{step.number}",
                    pause_after_seconds=1.0,
                )
            )
            counter += 1

    return blocks


def _generate_outro(lecture: LectureNote, seg_num: int, steps: list[Step]) -> str:
    """Generate outro narration."""
    if lecture.assignment_text and seg_num == 1:
        return (
            f"오늘 {lecture.week}주차 수업의 첫 번째 파트를 마치겠습니다. "
            f"과제는 Discord 채널에 제출해 주세요. "
            f"다음 파트에서 이어서 진행하겠습니다. 수고하셨습니다."
        )
    elif steps:
        return (
            f"이번 파트에서 다룬 내용을 잘 복습해 주세요. "
            f"수고하셨습니다."
        )
    else:
        return "오늘 수업을 마치겠습니다. 수고하셨습니다."


def _markdown_to_narration(content: str, title: str = "") -> str:
    """Convert markdown content to natural Korean narration text."""
    text = content

    # Remove markdown formatting
    text = re.sub(r"#{1,4}\s*", "", text)  # Headers
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)  # Bold
    text = re.sub(r"\*(.+?)\*", r"\1", text)  # Italic
    text = re.sub(r"`(.+?)`", r"\1", text)  # Inline code
    text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)  # Links
    text = re.sub(r"^\s*[-*]\s+", "", text, flags=re.MULTILINE)  # List markers
    text = re.sub(r"^\s*\d+\.\s+", "", text, flags=re.MULTILINE)  # Numbered lists
    text = re.sub(r"\|.+\|", "", text)  # Table rows
    text = re.sub(r"---+", "", text)  # Horizontal rules
    text = re.sub(r">\s*", "", text)  # Blockquotes

    # Clean up whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"  +", " ", text)
    text = text.strip()

    # Add title context
    if title and not text.startswith(title):
        text = f"{title}에 대해 알아보겠습니다. {text}"

    return text


def _sub_step_to_narration(text: str) -> str:
    """Convert a numbered sub-step to natural narration."""
    # Remove markdown
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)
    text = text.strip()

    # If it's already a natural sentence, keep it
    if text.endswith(("다", "요", "세요", "시오", "습니다", "니다")):
        return text

    # Add natural ending
    if any(text.endswith(c) for c in ("확인", "완료", "실행", "선택")):
        return f"{text}합니다."
    elif text.endswith(("클릭", "이동", "설정", "저장", "생성")):
        return f"{text}합니다."

    return f"{text}."


def _dominant_action_type(steps: list[Step]) -> ActionType:
    """Find the most common action type among steps."""
    if not steps:
        return ActionType.NARRATION_ONLY

    type_counts: dict[ActionType, int] = {}
    for step in steps:
        type_counts[step.action_type] = type_counts.get(step.action_type, 0) + 1

    return max(type_counts, key=type_counts.get)  # type: ignore[arg-type]
