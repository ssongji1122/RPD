"""Scene planner: classifies practice steps into recording actions.

Analyzes step content to determine what type of screen recording is needed:
- SLIDE: Theory/narration-only content → use slide images
- BLENDER: Blender 3D operations → record Blender viewport
- BROWSER: Web-based tools → record browser via Playwright
- MCP: Claude MCP interactions → record Claude + Blender together

Classification is rule-based using keyword patterns extracted from
12 weeks of consistent lecture-note.md formatting.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional

from ..parser.models import ActionType, LectureNote, Section, SectionType, Step


class RecordingMode(str, Enum):
    """How to record a step."""

    SLIDE = "slide"                # Static slide image, no recording
    BLENDER_SCRIPTED = "blender_scripted"  # Blender Python script execution
    BLENDER_MCP = "blender_mcp"    # MCP-driven Blender automation
    BROWSER = "browser"            # Playwright browser recording
    MIXED = "mixed"                # Multiple tools in sequence


@dataclass
class RecordingAction:
    """A single action to record for a practice step."""

    mode: RecordingMode
    description: str
    duration_hint_seconds: float = 30.0

    # For browser mode
    url: Optional[str] = None
    browser_actions: list[str] = field(default_factory=list)

    # For blender mode
    blender_script: Optional[str] = None  # Python script to execute
    shortcuts: list[str] = field(default_factory=list)

    # For MCP mode
    mcp_prompts: list[str] = field(default_factory=list)


@dataclass
class ScenePlan:
    """Complete recording plan for a step."""

    step_number: int
    step_title: str
    estimated_minutes: int
    actions: list[RecordingAction] = field(default_factory=list)

    @property
    def primary_mode(self) -> RecordingMode:
        if not self.actions:
            return RecordingMode.SLIDE
        modes = {a.mode for a in self.actions}
        if len(modes) == 1:
            return self.actions[0].mode
        return RecordingMode.MIXED


# --- Classification Patterns ---

BLENDER_KEYWORDS = {
    # Shortcuts (case-sensitive patterns)
    r"\b[GRSE]\b",
    r"Tab",
    r"Ctrl\s*\+\s*[A-Z]",
    r"Shift\s*\+\s*[A-Z]",
    r"Alt\s*\+\s*[A-Z]",
    r"Numpad\s*\d",
    r"F12",
    r"Middle Mouse",
    r"Scroll Wheel",
    # Blender UI elements
    r"Properties\s*(Panel|>)",
    r"(3D\s*)?Viewport",
    r"Edit\s*Mode",
    r"Object\s*Mode",
    r"Sculpt\s*Mode",
    r"Pose\s*Mode",
    r"Weight\s*Paint",
    r"Texture\s*Paint",
    r"Shader\s*(Editor|Node)",
    r"UV\s*Editor",
    r"Graph\s*Editor",
    r"NLA\s*Editor",
    r"Dope\s*Sheet",
    r"Outliner",
    r"Timeline",
    # 3D operations
    r"Extrude",
    r"Loop\s*Cut",
    r"Inset",
    r"Bevel",
    r"Modifier",
    r"Subdivision",
    r"Mirror",
    r"Solidify",
    r"Array",
    r"Boolean",
    r"Armature",
    r"Keyframe",
    r"Smooth\s*Shading",
    r"Mark\s*Seam",
    r"Unwrap",
    r"Principled\s*BSDF",
    r"Base\s*Color",
    r"Roughness",
    r"Metallic",
    r"Emission",
    r"Normal\s*Map",
    # Blender menus
    r"Shift\s*\+\s*A\s*>",
    r"File\s*>\s*(Import|Export|Save)",
    r"Render\s*(Engine|>)",
    r"Eevee",
    r"Cycles",
}

BROWSER_KEYWORDS = {
    r"https?://",
    r"접속",
    r"로그인",
    r"Sign\s*Up",
    r"업로드",
    r"다운로드",
    r"Download",
    r"Upload",
    r"웹사이트",
    r"\.com\b",
    r"\.ai\b",
    r"\.io\b",
    r"meshy",
    r"polyhaven",
    r"mixamo",
    r"tripo3d",
    r"blockadelabs",
    r"klingai",
    r"suno\.com",
}

MCP_KEYWORDS = {
    r"\bMCP\b",
    r"\bClaude\b",
    r"프롬프트",
    r"Create\s+a\s+",
    r"Set\s+(up|camera|render|light)",
    r"Make\s+(light|it)",
}


def classify_step(step: Step) -> RecordingMode:
    """Classify a single step into a recording mode.

    Priority: MCP > Browser > Blender > Slide
    """
    text = step.content_raw + " " + step.title
    for sub in step.sub_steps:
        text += " " + sub.text

    scores = {
        RecordingMode.BLENDER_SCRIPTED: 0,
        RecordingMode.BROWSER: 0,
        RecordingMode.BLENDER_MCP: 0,
    }

    for pattern in BLENDER_KEYWORDS:
        if re.search(pattern, text, re.IGNORECASE):
            scores[RecordingMode.BLENDER_SCRIPTED] += 1

    for pattern in BROWSER_KEYWORDS:
        if re.search(pattern, text, re.IGNORECASE):
            scores[RecordingMode.BROWSER] += 1

    for pattern in MCP_KEYWORDS:
        if re.search(pattern, text, re.IGNORECASE):
            scores[RecordingMode.BLENDER_MCP] += 1

    # Use existing ActionType from parser as a strong signal
    if step.action_type == ActionType.BROWSER:
        scores[RecordingMode.BROWSER] += 5
    elif step.action_type == ActionType.BLENDER:
        scores[RecordingMode.BLENDER_SCRIPTED] += 5
    elif step.action_type == ActionType.BLENDER_AND_BROWSER:
        scores[RecordingMode.BLENDER_SCRIPTED] += 3
        scores[RecordingMode.BROWSER] += 3

    # MCP overrides if strong signal
    if scores[RecordingMode.BLENDER_MCP] >= 2:
        return RecordingMode.BLENDER_MCP

    best = max(scores, key=lambda k: scores[k])
    if scores[best] == 0:
        return RecordingMode.SLIDE

    return best


def plan_step_recording(step: Step) -> ScenePlan:
    """Create a recording plan for a practice step."""
    mode = classify_step(step)
    text = step.content_raw

    plan = ScenePlan(
        step_number=step.number,
        step_title=step.title,
        estimated_minutes=step.estimated_minutes,
    )

    if mode == RecordingMode.BROWSER:
        # Extract URLs and browser actions
        urls = step.urls or re.findall(r"https?://[^\s)]+", text)
        actions = [sub.text for sub in step.sub_steps]

        for url in urls:
            plan.actions.append(RecordingAction(
                mode=RecordingMode.BROWSER,
                description=f"Navigate to {url}",
                url=url,
                browser_actions=actions,
                duration_hint_seconds=step.estimated_minutes * 60 / max(len(urls), 1),
            ))

        if not urls:
            plan.actions.append(RecordingAction(
                mode=RecordingMode.BROWSER,
                description=step.title,
                browser_actions=actions,
                duration_hint_seconds=step.estimated_minutes * 60,
            ))

    elif mode == RecordingMode.BLENDER_SCRIPTED:
        # Extract shortcuts and create action sequence
        plan.actions.append(RecordingAction(
            mode=RecordingMode.BLENDER_SCRIPTED,
            description=step.title,
            shortcuts=step.shortcuts,
            blender_script=_generate_blender_hint(step),
            duration_hint_seconds=step.estimated_minutes * 60,
        ))

    elif mode == RecordingMode.BLENDER_MCP:
        # Extract MCP prompts from quoted text
        prompts = re.findall(r'"([^"]+)"', text) or re.findall(r'"([^"]+)"', text)
        plan.actions.append(RecordingAction(
            mode=RecordingMode.BLENDER_MCP,
            description=step.title,
            mcp_prompts=prompts,
            duration_hint_seconds=step.estimated_minutes * 60,
        ))

    else:
        plan.actions.append(RecordingAction(
            mode=RecordingMode.SLIDE,
            description=step.title,
            duration_hint_seconds=step.estimated_minutes * 60,
        ))

    return plan


def plan_week_recordings(lecture: LectureNote) -> list[ScenePlan]:
    """Create recording plans for all practice steps in a lecture."""
    plans = []
    for section in lecture.practice_sections:
        for step in section.steps:
            plans.append(plan_step_recording(step))
    return plans


def _generate_blender_hint(step: Step) -> str:
    """Generate a hint for what Blender script should do.

    This is a descriptive hint, not executable Python.
    Actual scripts will be generated by the blender_agent.
    """
    lines = [f"# Step {step.number}: {step.title}"]
    for sub in step.sub_steps:
        lines.append(f"# {sub.number}. {sub.text}")
        if sub.shortcuts:
            lines.append(f"#   Shortcuts: {', '.join(sub.shortcuts)}")
    return "\n".join(lines)
