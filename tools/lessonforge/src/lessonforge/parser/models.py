"""Data models for the LessonForge pipeline.

All structured data flowing through the pipeline is defined here as Pydantic models.
The key hierarchy: LectureNote → Section → Step → SubStep
These are then transformed into VideoSegment → NarrationBlock for video production.
"""

from __future__ import annotations

from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field


class ActionType(str, Enum):
    """What kind of screen activity a step requires."""

    NARRATION_ONLY = "narration_only"  # Slides/overlay only, no recording
    BLENDER = "blender"  # Blender desktop automation
    BROWSER = "browser"  # Web browser automation
    BLENDER_AND_BROWSER = "blender_and_browser"  # Both


class SectionType(str, Enum):
    """Top-level section type in a lecture note."""

    THEORY = "theory"
    PRACTICE = "practice"
    ASSIGNMENT = "assignment"


class VisualType(str, Enum):
    """What visual content accompanies narration."""

    SLIDE = "slide"
    SCREEN_RECORDING = "screen_recording"
    OVERLAY = "overlay"  # Animated overlay (shortcut, table, etc.)


# --- Parsed Lecture Structure ---


class SubStep(BaseModel):
    """A single numbered instruction within a Step (e.g., '1. Open Blender')."""

    number: int
    text: str
    shortcuts: list[str] = Field(default_factory=list)


class Step(BaseModel):
    """A practice step: '### Step 1: 뷰 조작 연습 (15분)'."""

    number: int
    title: str
    estimated_minutes: int = 0
    content_raw: str = ""  # Original markdown content
    sub_steps: list[SubStep] = Field(default_factory=list)
    action_type: ActionType = ActionType.NARRATION_ONLY
    shortcuts: list[str] = Field(default_factory=list)
    urls: list[str] = Field(default_factory=list)


class Section(BaseModel):
    """A major section: '## 이론 (30분)' or '## 실습 (90분)'."""

    type: SectionType
    title: str
    estimated_minutes: int = 0
    content_raw: str = ""  # For theory sections (prose content)
    steps: list[Step] = Field(default_factory=list)  # For practice sections
    subsections: list[SubSection] = Field(default_factory=list)  # For theory subsections


class SubSection(BaseModel):
    """A subsection within theory: '### Blender 5.0 UI 구조'."""

    title: str
    content_raw: str = ""
    has_table: bool = False
    has_list: bool = False


class LearningObjective(BaseModel):
    """A checkbox learning objective."""

    text: str
    completed: bool = False


class LectureNote(BaseModel):
    """Complete parsed representation of a lecture-note.md file."""

    week: int
    title: str
    learning_objectives: list[LearningObjective] = Field(default_factory=list)
    sections: list[Section] = Field(default_factory=list)
    assignment_text: str = ""
    references: list[str] = Field(default_factory=list)
    source_path: Path | None = None

    @property
    def total_minutes(self) -> int:
        return sum(s.estimated_minutes for s in self.sections)

    @property
    def theory_sections(self) -> list[Section]:
        return [s for s in self.sections if s.type == SectionType.THEORY]

    @property
    def practice_sections(self) -> list[Section]:
        return [s for s in self.sections if s.type == SectionType.PRACTICE]


# --- Video Production Models ---


class NarrationBlock(BaseModel):
    """A single block of narration text with timing and visual cue."""

    id: str
    text: str
    timing_hint_seconds: float = 0.0
    visual_type: VisualType = VisualType.SLIDE
    visual_ref: str = ""  # Slide index, recording file, or overlay name
    pause_after_seconds: float = 0.5


class SegmentSection(BaseModel):
    """A section within a video segment."""

    title: str
    section_type: SectionType
    narration_blocks: list[NarrationBlock] = Field(default_factory=list)
    action_type: ActionType = ActionType.NARRATION_ONLY


class VideoSegment(BaseModel):
    """A single video file to be produced (one of 2-3 per week)."""

    segment_id: str  # e.g., "week02-seg01"
    week: int
    segment_number: int
    title: str
    sections: list[SegmentSection] = Field(default_factory=list)
    target_duration_seconds: int = 1200  # 20 min default
    narration_blocks: list[NarrationBlock] = Field(default_factory=list)

    @property
    def total_narration_text(self) -> str:
        return "\n\n".join(b.text for b in self.narration_blocks)


class BuildStageStatus(str, Enum):
    """Status of a pipeline stage."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETE = "complete"
    FAILED = "failed"
    SKIPPED = "skipped"


class StageResult(BaseModel):
    """Result of a single pipeline stage execution."""

    stage: str
    status: BuildStageStatus
    input_hash: str = ""
    output_paths: list[str] = Field(default_factory=list)
    error: str | None = None
    timestamp: str = ""


class SegmentManifest(BaseModel):
    """Build manifest for a single segment."""

    segment_id: str
    stages: dict[str, StageResult] = Field(default_factory=dict)


class WeekManifest(BaseModel):
    """Build manifest tracking all segments for a week."""

    week: int
    started_at: str = ""
    segments: dict[str, SegmentManifest] = Field(default_factory=dict)
