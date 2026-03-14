"""Build orchestrator: coordinates all pipeline stages for a segment.

This is the core module that ties parsing, slides, narration, and
composition together into a single coherent workflow.

Pipeline:  parse → slides → narrate → compose → [publish]
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from ..config import LessonForgeConfig, load_config
from ..manifest import (
    is_stage_complete,
    load_manifest,
    save_manifest,
    update_stage,
)
from ..parser.lecture_parser import parse_lecture_note
from ..parser.models import (
    BuildStageStatus,
    NarrationBlock,
    VideoSegment,
    VisualType,
)
from ..parser.script_generator import generate_segments
from ..parser.slide_parser import get_slide_titles, render_slides
from .ffmpeg_compose import CompositionPlan, VideoScene, compose_segment, get_audio_duration
from .title_card import (
    generate_outro_card,
    generate_section_header,
    generate_step_indicator,
    generate_title_card,
)


def build_week(
    week: int,
    config: Optional[LessonForgeConfig] = None,
    *,
    segments_filter: Optional[list[int]] = None,
    resume_from: Optional[str] = None,
    dry_run: bool = False,
) -> list[Path]:
    """Build all video segments for a week.

    Args:
        week: Week number (1-15).
        config: Configuration (loaded from yaml if not provided).
        segments_filter: Only build specific segment numbers.
        resume_from: Resume from a specific pipeline stage.
        dry_run: Print plan without executing.

    Returns:
        List of paths to generated video files.
    """
    if config is None:
        config = load_config()

    output_root = Path(config.project.output_root)
    week_dir = _find_week_dir(week, config)
    lecture_note_path = week_dir / "lecture-note.md"
    slides_path = week_dir / "slides.md"

    if not lecture_note_path.exists():
        raise FileNotFoundError(f"No lecture-note.md found at {lecture_note_path}")

    # Load or create manifest
    manifest = load_manifest(week, output_root)
    if not manifest.started_at:
        from datetime import datetime, timezone
        manifest.started_at = datetime.now(timezone.utc).isoformat()

    # Stage 1: Parse
    lecture = parse_lecture_note(lecture_note_path)
    segments = generate_segments(lecture)

    if segments_filter:
        segments = [s for s in segments if s.segment_number in segments_filter]

    if dry_run:
        return _print_dry_run(segments)

    results = []
    for segment in segments:
        video_path = _build_segment(
            segment=segment,
            slides_path=slides_path,
            config=config,
            output_root=output_root,
            manifest=manifest,
            resume_from=resume_from,
        )
        if video_path:
            results.append(video_path)

    save_manifest(manifest, output_root)
    return results


def _build_segment(
    segment: VideoSegment,
    slides_path: Path,
    config: LessonForgeConfig,
    output_root: Path,
    manifest,
    resume_from: Optional[str] = None,
) -> Optional[Path]:
    """Build a single video segment through all pipeline stages."""
    seg_dir = output_root / f"week{segment.week:02d}" / "segments" / segment.segment_id

    # Stage: Slides
    slide_images = []
    if slides_path.exists():
        slides_dir = seg_dir / "slides"
        if not is_stage_complete(manifest, segment.segment_id, "slides") or resume_from in (
            None, "slides"
        ):
            try:
                update_stage(
                    manifest, segment.segment_id, "slides",
                    BuildStageStatus.RUNNING, output_root=output_root,
                )
                theme_css = _find_theme_css(config)
                slide_images = render_slides(
                    slides_path, slides_dir, theme_css=theme_css
                )
                update_stage(
                    manifest, segment.segment_id, "slides",
                    BuildStageStatus.COMPLETE,
                    output_paths=[str(p) for p in slide_images],
                    output_root=output_root,
                )
            except Exception as e:
                update_stage(
                    manifest, segment.segment_id, "slides",
                    BuildStageStatus.FAILED, error=str(e),
                    output_root=output_root,
                )
                # Continue without slides - use title cards instead
                slide_images = []
        else:
            # Load existing slides
            slides_dir.mkdir(parents=True, exist_ok=True)
            slide_images = sorted(slides_dir.glob("*.png"))

    # Stage: Generate title cards and section images
    cards_dir = seg_dir / "cards"
    cards_dir.mkdir(parents=True, exist_ok=True)

    title_card = generate_title_card(
        week=segment.week,
        title=segment.title,
        segment_number=segment.segment_number,
        output_path=cards_dir / "title.png",
    )

    outro_card = generate_outro_card(
        output_path=cards_dir / "outro.png",
    )

    # Stage: Narrate (check if audio already exists from Phase 1)
    audio_dir = seg_dir / "audio"
    audio_files = {}
    if audio_dir.exists():
        for mp3 in audio_dir.glob("*.mp3"):
            audio_files[mp3.stem] = mp3

    # If no audio files exist, run TTS
    if not audio_files and segment.narration_blocks:
        import asyncio
        from ..narration.edge_tts_engine import synthesize_blocks

        update_stage(
            manifest, segment.segment_id, "narrate",
            BuildStageStatus.RUNNING, output_root=output_root,
        )
        try:
            blocks = [{"id": b.id, "text": b.text} for b in segment.narration_blocks]
            tts_config = config.tts
            asyncio.run(synthesize_blocks(
                blocks, audio_dir,
                voice=tts_config.voice,
                rate=tts_config.rate,
            ))
            for mp3 in audio_dir.glob("*.mp3"):
                audio_files[mp3.stem] = mp3
            update_stage(
                manifest, segment.segment_id, "narrate",
                BuildStageStatus.COMPLETE,
                output_paths=[str(p) for p in audio_dir.glob("*.mp3")],
                output_root=output_root,
            )
        except Exception as e:
            update_stage(
                manifest, segment.segment_id, "narrate",
                BuildStageStatus.FAILED, error=str(e),
                output_root=output_root,
            )
            return None

    # Stage: Compose - build scene list and render video
    update_stage(
        manifest, segment.segment_id, "compose",
        BuildStageStatus.RUNNING, output_root=output_root,
    )

    try:
        plan = _build_composition_plan(
            segment=segment,
            slide_images=slide_images,
            slide_titles=get_slide_titles(slides_path) if slides_path.exists() else [],
            audio_files=audio_files,
            title_card=title_card,
            outro_card=outro_card,
            cards_dir=cards_dir,
        )

        video_path = seg_dir / "video.mp4"
        plan.output_path = video_path
        result_path = compose_segment(plan)

        update_stage(
            manifest, segment.segment_id, "compose",
            BuildStageStatus.COMPLETE,
            output_paths=[str(result_path)],
            output_root=output_root,
        )
        return result_path

    except Exception as e:
        update_stage(
            manifest, segment.segment_id, "compose",
            BuildStageStatus.FAILED, error=str(e),
            output_root=output_root,
        )
        return None


def _build_composition_plan(
    segment: VideoSegment,
    slide_images: list[Path],
    slide_titles: list[str],
    audio_files: dict[str, Path],
    title_card: Path,
    outro_card: Path,
    cards_dir: Path,
) -> CompositionPlan:
    """Build a composition plan mapping narration blocks to visual scenes."""
    scenes = []

    # Build a simple title-to-slide-index mapping
    slide_map = {}
    for idx, title in enumerate(slide_titles):
        if title:
            slide_map[title.lower().strip()] = idx

    for block in segment.narration_blocks:
        audio = audio_files.get(block.id)
        duration = get_audio_duration(audio) + 0.5 if audio else 3.0

        # Determine which image to show
        if block.visual_type == VisualType.OVERLAY:
            # Use title card, section header, step indicator, or outro
            image = _resolve_overlay_image(
                block, segment, title_card, outro_card, cards_dir
            )
        elif block.visual_type == VisualType.SLIDE and slide_images:
            # Try to match slide by visual_ref
            image = _match_slide(block.visual_ref, slide_images, slide_map)
        else:
            # Fallback: use title card as placeholder for screen recordings
            image = title_card

        scenes.append(VideoScene(
            image_path=image,
            audio_path=audio,
            duration_seconds=duration,
            scene_type=block.visual_type.value,
            narration_id=block.id,
        ))

    return CompositionPlan(
        segment_id=segment.segment_id,
        scenes=scenes,
    )


def _resolve_overlay_image(
    block: NarrationBlock,
    segment: VideoSegment,
    title_card: Path,
    outro_card: Path,
    cards_dir: Path,
) -> Path:
    """Generate or select the appropriate overlay image for a block."""
    ref = block.visual_ref.lower() if block.visual_ref else ""

    if "title" in ref or "intro" in block.id:
        return title_card
    elif "outro" in ref or "outro" in block.id:
        return outro_card
    elif "section" in ref:
        section_type = "practice" if "실습" in ref or "practice" in ref else "theory"
        section_title = ref.replace("section_header:", "").strip()
        out = cards_dir / f"section_{section_type}.png"
        if not out.exists():
            generate_section_header(section_type, section_title or section_type, out)
        return out
    elif "step" in ref or "step" in block.id:
        # Extract step number from block id
        import re
        match = re.search(r"step(\d+)", block.id)
        step_num = int(match.group(1)) if match else 1
        step_title = ref.replace("step_indicator:", "").strip()
        out = cards_dir / f"step_{step_num}.png"
        if not out.exists():
            generate_step_indicator(step_num, step_title or f"Step {step_num}", out)
        return out
    else:
        return title_card


def _match_slide(
    visual_ref: str,
    slide_images: list[Path],
    slide_map: dict[str, int],
) -> Path:
    """Match a visual reference to a slide image."""
    if not visual_ref or not slide_images:
        return slide_images[0] if slide_images else Path()

    ref = visual_ref.lower().strip()

    # Try exact title match
    if "slide:" in ref:
        title = ref.replace("slide:", "").strip()
        idx = slide_map.get(title)
        if idx is not None and idx < len(slide_images):
            return slide_images[idx]

    # Try index match
    try:
        idx = int(ref)
        if 0 <= idx < len(slide_images):
            return slide_images[idx]
    except ValueError:
        pass

    # Fuzzy match: find best matching slide title
    for title, idx in slide_map.items():
        if ref in title or title in ref:
            if idx < len(slide_images):
                return slide_images[idx]

    # Default to first slide
    return slide_images[0]


def _find_week_dir(week: int, config: LessonForgeConfig) -> Path:
    """Find the week directory."""
    lectures_root = Path(config.project.lectures_root)
    if not lectures_root.is_absolute():
        # Resolve relative to config file location
        config_dir = Path(__file__).parent.parent.parent.parent
        lectures_root = (config_dir / lectures_root).resolve()

    # Search for week directory
    patterns = [
        f"week{week:02d}-*",
        f"week{week:02d}",
        f"Week{week:02d}-*",
    ]
    for pattern in patterns:
        matches = list(lectures_root.glob(pattern))
        if matches:
            return matches[0]

    raise FileNotFoundError(
        f"No directory found for week {week} in {lectures_root}"
    )


def _find_theme_css(config: LessonForgeConfig) -> Optional[Path]:
    """Find the Marp theme CSS file."""
    config_dir = Path(__file__).parent.parent.parent.parent
    candidates = [
        config_dir / "../../templates/marp-theme.css",
        config_dir / "../templates/marp-theme.css",
        Path("templates/marp-theme.css"),
    ]
    for c in candidates:
        resolved = c.resolve()
        if resolved.exists():
            return resolved
    return None


def _print_dry_run(segments: list[VideoSegment]) -> list[Path]:
    """Print what would be built without actually building."""
    from rich.console import Console
    from rich.panel import Panel

    console = Console()
    for seg in segments:
        console.print(Panel(
            f"[bold]{seg.segment_id}[/bold]: {seg.title}\n"
            f"Blocks: {len(seg.narration_blocks)}\n"
            f"Target: ~{seg.target_duration_seconds // 60}min",
            title=f"Segment {seg.segment_number}",
        ))
    return []
