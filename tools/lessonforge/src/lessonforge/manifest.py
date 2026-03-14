"""Build manifest for tracking pipeline stage progress.

Allows resuming failed builds from the last successful checkpoint.
Each stage writes its status to a JSON manifest file.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .parser.models import BuildStageStatus, SegmentManifest, StageResult, WeekManifest


STAGES = ["parse", "slides", "narrate", "compose", "publish"]


def load_manifest(week: int, output_root: Path) -> WeekManifest:
    """Load existing manifest or create a new one."""
    manifest_path = output_root / f"week{week:02d}" / "manifest.json"
    if manifest_path.exists():
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        return WeekManifest(**data)
    return WeekManifest(week=week)


def save_manifest(manifest: WeekManifest, output_root: Path) -> Path:
    """Save manifest to disk."""
    manifest_path = output_root / f"week{manifest.week:02d}" / "manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest.model_dump(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return manifest_path


def update_stage(
    manifest: WeekManifest,
    segment_id: str,
    stage: str,
    status: BuildStageStatus,
    *,
    output_paths: Optional[list[str]] = None,
    error: Optional[str] = None,
    output_root: Optional[Path] = None,
) -> None:
    """Update a stage's status in the manifest."""
    if segment_id not in manifest.segments:
        manifest.segments[segment_id] = SegmentManifest(segment_id=segment_id)

    manifest.segments[segment_id].stages[stage] = StageResult(
        stage=stage,
        status=status,
        output_paths=output_paths or [],
        error=error,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    if output_root:
        save_manifest(manifest, output_root)


def get_resume_stage(manifest: WeekManifest, segment_id: str) -> Optional[str]:
    """Find the first incomplete stage for a segment.

    Returns the stage name to resume from, or None if all complete.
    """
    seg = manifest.segments.get(segment_id)
    if not seg:
        return STAGES[0]

    for stage in STAGES:
        result = seg.stages.get(stage)
        if not result or result.status != BuildStageStatus.COMPLETE:
            return stage

    return None  # All stages complete


def is_stage_complete(manifest: WeekManifest, segment_id: str, stage: str) -> bool:
    """Check if a specific stage is already complete."""
    seg = manifest.segments.get(segment_id)
    if not seg:
        return False
    result = seg.stages.get(stage)
    return result is not None and result.status == BuildStageStatus.COMPLETE
