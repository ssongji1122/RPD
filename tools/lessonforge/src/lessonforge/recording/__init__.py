"""Recording module: screen capture and application automation.

Provides:
- ScenePlanner: classify practice steps into recording modes
- ScreenRecorder: FFmpeg + AVFoundation screen capture
- BlenderAgent: Blender bpy script automation
- BrowserAgent: Playwright browser automation
"""

from .scene_planner import (
    RecordingMode,
    RecordingAction,
    ScenePlan,
    classify_step,
    plan_step_recording,
    plan_week_recordings,
)

__all__ = [
    "RecordingMode",
    "RecordingAction",
    "ScenePlan",
    "classify_step",
    "plan_step_recording",
    "plan_week_recordings",
]