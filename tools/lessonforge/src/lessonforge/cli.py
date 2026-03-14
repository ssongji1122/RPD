"""LessonForge CLI - AI lecture video production pipeline.

Usage:
    lessonforge parse week02              # Parse lecture notes
    lessonforge narrate week02            # Generate scripts + TTS audio
    lessonforge build week02              # Full pipeline: slides + audio → video
    lessonforge build week02 --segments 1 # Build specific segment only
    lessonforge build week02 --dry-run    # Preview plan without building
    lessonforge status week02             # Show build manifest
"""

from __future__ import annotations

import asyncio
import json
import re
import sys
from pathlib import Path
from typing import Any

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree

from .config import LessonForgeConfig, load_config, resolve_lectures_root
from .parser.lecture_parser import parse_lecture_note
from .parser.script_generator import generate_segments

console = Console()

# Resolve paths relative to this file's location
TOOL_ROOT = Path(__file__).resolve().parent.parent.parent  # tools/lessonforge/
DEFAULT_CONFIG = TOOL_ROOT / "lessonforge.config.yaml"


def _resolve_week(week_arg: str, lectures_root: Path) -> tuple[int, Path]:
    """Resolve 'week02' or '2' to (2, /path/to/week02-blender-basics/)."""
    # Extract number
    m = re.search(r"(\d+)", week_arg)
    if not m:
        raise click.BadParameter(f"Cannot parse week number from '{week_arg}'")
    week_num = int(m.group(1))

    # Find directory
    pattern = f"week{week_num:02d}-*"
    matches = sorted(lectures_root.glob(pattern))
    if not matches:
        # Try without suffix
        pattern2 = f"week{week_num:02d}*"
        matches = sorted(lectures_root.glob(pattern2))

    if not matches:
        raise click.BadParameter(
            f"No directory found for week {week_num} in {lectures_root}"
        )

    return week_num, matches[0]


@click.group()
@click.option("--config", "-c", type=click.Path(exists=False), default=None)
@click.pass_context
def cli(ctx: click.Context, config: str | None) -> None:
    """LessonForge: AI lecture video production pipeline."""
    config_path = Path(config) if config else DEFAULT_CONFIG
    ctx.ensure_object(dict)
    ctx.obj["config"] = load_config(config_path if config_path.exists() else None)
    ctx.obj["config_path"] = config_path


@cli.command()
@click.argument("week")
@click.pass_context
def parse(ctx: click.Context, week: str) -> None:
    """Parse a week's lecture-note.md and display its structure."""
    cfg: LessonForgeConfig = ctx.obj["config"]
    config_path: Path = ctx.obj["config_path"]
    lectures_root = resolve_lectures_root(cfg, config_path)

    week_num, week_dir = _resolve_week(week, lectures_root)
    lecture_file = week_dir / "lecture-note.md"

    if not lecture_file.exists():
        console.print(f"[red]Error:[/red] {lecture_file} not found")
        sys.exit(1)

    console.print(f"\n[cyan]Parsing:[/cyan] {lecture_file}\n")

    # Parse
    lecture = parse_lecture_note(lecture_file)

    # Display structure
    tree = Tree(f"[bold cyan]Week {lecture.week:02d}: {lecture.title}[/bold cyan]")

    # Learning objectives
    obj_branch = tree.add("[yellow]학습 목표[/yellow]")
    for obj in lecture.learning_objectives:
        obj_branch.add(f"{'[green]✓[/green]' if obj.completed else '[ ]'} {obj.text}")

    # Sections
    for section in lecture.sections:
        section_label = (
            f"[magenta]{section.title}[/magenta]"
            if section.type.value == "theory"
            else f"[green]{section.title}[/green]"
        )
        sec_branch = tree.add(section_label)

        if section.subsections:
            for sub in section.subsections:
                flags = []
                if sub.has_table:
                    flags.append("📊")
                if sub.has_list:
                    flags.append("📝")
                sec_branch.add(f"  {sub.title} {' '.join(flags)}")

        for step in section.steps:
            step_label = (
                f"Step {step.number}: {step.title} "
                f"({step.estimated_minutes}min) "
                f"[dim][{step.action_type.value}][/dim]"
            )
            step_branch = sec_branch.add(step_label)

            if step.shortcuts:
                step_branch.add(f"[cyan]Shortcuts: {', '.join(step.shortcuts)}[/cyan]")
            if step.urls:
                for url in step.urls:
                    step_branch.add(f"[blue]{url}[/blue]")
            step_branch.add(f"[dim]{len(step.sub_steps)} sub-steps[/dim]")

    console.print(tree)

    # Summary
    console.print(f"\n[bold]Summary:[/bold]")
    console.print(f"  Total estimated time: {lecture.total_minutes} minutes")
    console.print(f"  Theory sections: {len(lecture.theory_sections)}")
    console.print(f"  Practice sections: {len(lecture.practice_sections)}")

    total_steps = sum(len(s.steps) for s in lecture.practice_sections)
    console.print(f"  Practice steps: {total_steps}")


@cli.command()
@click.argument("week")
@click.option("--voice", "-v", default=None, help="TTS voice name")
@click.option("--rate", "-r", default=None, help="Speech rate (e.g., +5%%)")
@click.option("--dry-run", is_flag=True, help="Show script without generating audio")
@click.pass_context
def narrate(ctx: click.Context, week: str, voice: str | None, rate: str | None, dry_run: bool) -> None:
    """Generate narration scripts and TTS audio for a week."""
    cfg: LessonForgeConfig = ctx.obj["config"]
    config_path: Path = ctx.obj["config_path"]
    lectures_root = resolve_lectures_root(cfg, config_path)

    week_num, week_dir = _resolve_week(week, lectures_root)
    lecture_file = week_dir / "lecture-note.md"

    if not lecture_file.exists():
        console.print(f"[red]Error:[/red] {lecture_file} not found")
        sys.exit(1)

    # Parse
    console.print(f"\n[cyan]Parsing:[/cyan] {lecture_file}")
    lecture = parse_lecture_note(lecture_file)

    # Generate segments
    console.print("[cyan]Generating segments and narration scripts...[/cyan]")
    segments = generate_segments(lecture)

    # Display segments
    for seg in segments:
        table = Table(
            title=f"[bold]{seg.segment_id}: {seg.title}[/bold]",
            show_lines=True,
        )
        table.add_column("ID", style="dim", width=30)
        table.add_column("Narration", width=60)
        table.add_column("Visual", style="cyan", width=20)
        table.add_column("~Sec", justify="right", width=6)

        for block in seg.narration_blocks:
            text_preview = block.text[:80] + "..." if len(block.text) > 80 else block.text
            table.add_row(
                block.id,
                text_preview,
                f"{block.visual_type.value}\n{block.visual_ref}",
                f"{block.timing_hint_seconds:.0f}",
            )

        console.print(table)
        console.print(
            f"  [dim]Target duration: ~{seg.target_duration_seconds // 60}min "
            f"({seg.target_duration_seconds}s), "
            f"{len(seg.narration_blocks)} blocks[/dim]\n"
        )

    if dry_run:
        console.print("[yellow]Dry run - no audio generated.[/yellow]")
        return

    # Generate audio
    output_dir = Path(cfg.project.output_root) / f"week{week_num:02d}"
    tts_voice = voice or cfg.tts.voice
    tts_rate = rate or cfg.tts.rate

    console.print(
        f"\n[cyan]Generating TTS audio...[/cyan]\n"
        f"  Engine: {cfg.tts.engine}\n"
        f"  Voice: {tts_voice}\n"
        f"  Rate: {tts_rate}\n"
        f"  Output: {output_dir}\n"
    )

    asyncio.run(_generate_audio(segments, output_dir, tts_voice, tts_rate))


async def _generate_audio(
    segments: list, output_dir: Path, voice: str, rate: str
) -> None:
    """Generate TTS audio for all segments."""
    from .narration.edge_tts_engine import synthesize_blocks

    for seg in segments:
        seg_dir = output_dir / "segments" / seg.segment_id
        blocks = [{"id": b.id, "text": b.text} for b in seg.narration_blocks if b.text.strip()]

        console.print(f"[cyan]Synthesizing {seg.segment_id}...[/cyan] ({len(blocks)} blocks)")

        results = await synthesize_blocks(
            blocks=blocks,
            output_dir=seg_dir / "audio",
            voice=voice,
            rate=rate,
        )

        total_duration = sum(r.duration_seconds for r in results)
        console.print(
            f"  [green]✓[/green] {len(results)} audio files, "
            f"total {total_duration:.0f}s (~{total_duration/60:.1f}min)"
        )

        # Save script as JSON
        script_path = seg_dir / "script.json"
        script_path.parent.mkdir(parents=True, exist_ok=True)
        script_data = {
            "segment_id": seg.segment_id,
            "title": seg.title,
            "blocks": [b.model_dump() for b in seg.narration_blocks],
        }
        script_path.write_text(
            json.dumps(script_data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        console.print(f"  [green]✓[/green] Script saved: {script_path}")

    console.print(f"\n[bold green]Done![/bold green] Output: {output_dir}")


@cli.command()
@click.pass_context
def voices(ctx: click.Context) -> None:
    """List available TTS voices."""
    async def _list():
        from .narration.edge_tts_engine import EdgeTTSEngine

        engine = EdgeTTSEngine()
        voices = await engine.list_voices("ko")

        table = Table(title="Korean TTS Voices (Edge TTS)")
        table.add_column("ID", style="cyan")
        table.add_column("Name")
        table.add_column("Gender")

        for v in voices:
            table.add_row(v["id"], v["name"], v["gender"])

        console.print(table)

    asyncio.run(_list())


@cli.command()
@click.argument("week")
@click.option("--segments", "-s", default=None, help="Comma-separated segment numbers (e.g., 1,2)")
@click.option("--resume-from", default=None, help="Resume from stage: slides, narrate, compose")
@click.option("--dry-run", is_flag=True, help="Show build plan without executing")
@click.pass_context
def build(ctx: click.Context, week: str, segments: str | None, resume_from: str | None, dry_run: bool) -> None:
    """Build video segments for a week (full pipeline).

    Stages: parse → slides → narrate → compose
    """
    from .compositor.builder import build_week

    cfg: LessonForgeConfig = ctx.obj["config"]
    config_path: Path = ctx.obj["config_path"]
    lectures_root = resolve_lectures_root(cfg, config_path)

    week_num, _ = _resolve_week(week, lectures_root)

    segments_filter = None
    if segments:
        segments_filter = [int(s.strip()) for s in segments.split(",")]

    console.print(f"\n[bold cyan]Building Week {week_num:02d}...[/bold cyan]\n")

    try:
        results = build_week(
            week=week_num,
            config=cfg,
            segments_filter=segments_filter,
            resume_from=resume_from,
            dry_run=dry_run,
        )

        if dry_run:
            console.print("[yellow]Dry run complete.[/yellow]")
            return

        if results:
            console.print(f"\n[bold green]Build complete![/bold green]")
            for path in results:
                size_mb = path.stat().st_size / 1024 / 1024
                console.print(f"  [green]✓[/green] {path} ({size_mb:.1f}MB)")
        else:
            console.print("[yellow]No videos generated.[/yellow]")

    except Exception as e:
        console.print(f"\n[red]Build failed:[/red] {e}")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        sys.exit(1)


@cli.command()
@click.argument("week")
@click.option("--segment", "-s", type=int, default=None, help="Specific segment number")
@click.option("--dry-run", is_flag=True, help="Show recording plan without executing")
@click.pass_context
def record(ctx: click.Context, week: str, segment: int | None, dry_run: bool) -> None:
    """Analyze and plan screen recordings for a week's practice steps."""
    cfg: LessonForgeConfig = ctx.obj["config"]
    config_path: Path = ctx.obj["config_path"]
    lectures_root = resolve_lectures_root(cfg, config_path)

    week_num, week_dir = _resolve_week(week, lectures_root)
    lecture_file = week_dir / "lecture-note.md"

    if not lecture_file.exists():
        console.print(f"[red]Error:[/red] {lecture_file} not found")
        sys.exit(1)

    # Parse
    lecture = parse_lecture_note(lecture_file)

    # Plan recordings
    from .recording.scene_planner import plan_week_recordings, RecordingMode

    plans = plan_week_recordings(lecture)

    # Display recording plan
    table = Table(
        title=f"[bold]Week {week_num:02d} Recording Plan[/bold]",
        show_lines=True,
    )
    table.add_column("Step", style="dim", width=6)
    table.add_column("Title", width=30)
    table.add_column("Mode", style="cyan", width=18)
    table.add_column("Actions", width=40)
    table.add_column("~Min", justify="right", width=6)

    mode_colors = {
        RecordingMode.SLIDE: "dim",
        RecordingMode.BLENDER_SCRIPTED: "green",
        RecordingMode.BLENDER_MCP: "magenta",
        RecordingMode.BROWSER: "blue",
        RecordingMode.MIXED: "yellow",
    }

    for plan in plans:
        mode = plan.primary_mode
        color = mode_colors.get(mode, "white")
        actions_desc = "; ".join(a.description[:40] for a in plan.actions)

        table.add_row(
            str(plan.step_number),
            plan.step_title[:30],
            f"[{color}]{mode.value}[/{color}]",
            actions_desc[:40],
            str(plan.estimated_minutes),
        )

    console.print(f"\n")
    console.print(table)

    # Summary
    mode_counts = {}
    for plan in plans:
        m = plan.primary_mode
        mode_counts[m] = mode_counts.get(m, 0) + 1

    console.print(f"\n[bold]Recording Summary:[/bold]")
    for mode, count in sorted(mode_counts.items(), key=lambda x: -x[1]):
        console.print(f"  {mode.value}: {count} steps")

    total_mins = sum(p.estimated_minutes for p in plans)
    console.print(f"  [dim]Total estimated: ~{total_mins} minutes[/dim]")

    # Check tool availability
    console.print(f"\n[bold]Tool Availability:[/bold]")

    # Blender
    from .recording.blender_agent import BlenderAgent
    blender = BlenderAgent()
    blender_ok = blender.verify_blender()
    console.print(f"  Blender: {'[green]✓[/green]' if blender_ok else '[red]✗[/red] (not found)'}")

    # Playwright
    from .recording.browser_agent import BrowserAgent
    pw_ok = BrowserAgent.is_available()
    console.print(f"  Playwright: {'[green]✓[/green]' if pw_ok else '[yellow]✗[/yellow] (pip install playwright)'}")

    # FFmpeg
    try:
        from .compositor.ffmpeg_compose import find_ffmpeg
        find_ffmpeg()
        console.print(f"  FFmpeg: [green]✓[/green]")
    except RuntimeError:
        console.print(f"  FFmpeg: [red]✗[/red]")

    if dry_run:
        console.print(f"\n[yellow]Dry run - no recordings made.[/yellow]")


@cli.command()
@click.argument("week")
@click.option("--segments", "-s", default=None, help="Comma-separated segment numbers")
@click.option("--privacy", type=click.Choice(["unlisted", "private", "public"]), default=None)
@click.option("--dry-run", is_flag=True, help="Show metadata without uploading")
@click.pass_context
def publish(ctx: click.Context, week: str, segments: str | None, privacy: str | None, dry_run: bool) -> None:
    """Upload built videos to YouTube.

    Requires client_secrets.json from Google Cloud Console.
    First run will open browser for OAuth2 authorization.
    """
    cfg: LessonForgeConfig = ctx.obj["config"]
    config_path: Path = ctx.obj["config_path"]
    lectures_root = resolve_lectures_root(cfg, config_path)

    week_num, week_dir = _resolve_week(week, lectures_root)
    lecture_file = week_dir / "lecture-note.md"

    if not lecture_file.exists():
        console.print(f"[red]Error:[/red] {lecture_file} not found")
        sys.exit(1)

    # Parse for metadata generation
    lecture = parse_lecture_note(lecture_file)
    video_segments = generate_segments(lecture)

    if segments:
        segment_nums = [int(s.strip()) for s in segments.split(",")]
        video_segments = [s for s in video_segments if s.segment_number in segment_nums]

    # Find built videos
    output_dir = Path(cfg.project.output_root) / f"week{week_num:02d}"
    from .publisher.metadata import generate_metadata

    upload_privacy = privacy or cfg.youtube.privacy

    for seg in video_segments:
        seg_dir = output_dir / "segments" / seg.segment_id
        video_path = seg_dir / "video.mp4"

        if not video_path.exists():
            console.print(f"[yellow]Skipping {seg.segment_id}: video.mp4 not found[/yellow]")
            continue

        # Generate metadata
        meta = generate_metadata(
            seg, lecture,
            base_tags=cfg.youtube.tags_base,
            playlist=cfg.youtube.playlist,
            privacy=upload_privacy,
        )

        size_mb = video_path.stat().st_size / 1024 / 1024

        console.print(f"\n[bold]{seg.segment_id}[/bold] ({size_mb:.1f}MB)")
        console.print(f"  Title: {meta.title}")
        console.print(f"  Tags: {', '.join(meta.tags[:10])}")
        console.print(f"  Privacy: {meta.privacy_status}")

        if dry_run:
            console.print(f"  [yellow]Dry run - not uploading[/yellow]")
            continue

        # Upload
        console.print(f"  [cyan]Uploading...[/cyan]")
        try:
            from .publisher.youtube import upload_video
            result = upload_video(video_path, meta)
            console.print(f"  [green]✓ Uploaded:[/green] {result['url']}")
        except FileNotFoundError as e:
            console.print(f"  [red]✗ {e}[/red]")
            console.print(f"  [dim]See: lessonforge publish --help[/dim]")
            break
        except Exception as e:
            console.print(f"  [red]✗ Upload failed:[/red] {e}")

    if dry_run:
        console.print(f"\n[yellow]Dry run complete. Use without --dry-run to upload.[/yellow]")


@cli.command()
@click.argument("week")
@click.pass_context
def status(ctx: click.Context, week: str) -> None:
    """Show build status for a week."""
    cfg: LessonForgeConfig = ctx.obj["config"]
    m = re.search(r"(\d+)", week)
    if not m:
        console.print("[red]Invalid week number[/red]")
        sys.exit(1)

    week_num = int(m.group(1))
    output_dir = Path(cfg.project.output_root) / f"week{week_num:02d}"

    if not output_dir.exists():
        console.print(f"[yellow]No output found for week {week_num}[/yellow]")
        return

    # List output contents
    tree = Tree(f"[bold]Week {week_num:02d} Output[/bold]")
    _build_file_tree(tree, output_dir)
    console.print(tree)


def _build_file_tree(tree: Tree, directory: Path, depth: int = 0) -> None:
    """Recursively build a tree of files."""
    if depth > 4:
        return
    for item in sorted(directory.iterdir()):
        if item.is_dir():
            branch = tree.add(f"[cyan]{item.name}/[/cyan]")
            _build_file_tree(branch, item, depth + 1)
        else:
            size = item.stat().st_size
            if size > 1024 * 1024:
                size_str = f"{size / 1024 / 1024:.1f}MB"
            elif size > 1024:
                size_str = f"{size / 1024:.0f}KB"
            else:
                size_str = f"{size}B"
            tree.add(f"{item.name} [dim]({size_str})[/dim]")


@cli.command()
@click.argument("week")
@click.option("--confirm", is_flag=True, help="Skip interactive confirmation (for scripting)")
@click.pass_context
def review(ctx: click.Context, week: str, confirm: bool) -> None:
    """Review lecture content before video generation.

    Shows a formatted summary of the lecture-note.md — learning objectives,
    theory sections, practice steps, and recording requirements — then asks
    for your confirmation before any video is built.

    Always run this before 'lessonforge build <week>'.
    """
    cfg: LessonForgeConfig = ctx.obj["config"]
    config_path: Path = ctx.obj["config_path"]
    lectures_root = resolve_lectures_root(cfg, config_path)

    week_num, week_dir = _resolve_week(week, lectures_root)
    lecture_file = week_dir / "lecture-note.md"

    if not lecture_file.exists():
        console.print(f"[red]Error:[/red] {lecture_file} not found")
        sys.exit(1)

    lecture = parse_lecture_note(lecture_file)
    segments = generate_segments(lecture)

    # ── Header ──────────────────────────────────────────────────────────────
    console.print()
    console.print(Panel(
        f"[bold cyan]Week {lecture.week:02d}: {lecture.title}[/bold cyan]\n"
        f"[dim]{lecture_file}[/dim]",
        title="[bold]LessonForge Review[/bold]",
        border_style="cyan",
    ))

    # ── Learning Objectives ──────────────────────────────────────────────────
    console.print("\n[bold yellow]학습 목표[/bold yellow]")
    for obj in lecture.learning_objectives:
        mark = "[green]✓[/green]" if obj.completed else "[ ]"
        console.print(f"  {mark} {obj.text}")

    # ── Theory Sections ──────────────────────────────────────────────────────
    if lecture.theory_sections:
        console.print("\n[bold magenta]이론 섹션[/bold magenta]")
        for sec in lecture.theory_sections:
            console.print(f"  [magenta]▸[/magenta] {sec.title}")
            for sub in sec.subsections:
                console.print(f"    [dim]• {sub.title}[/dim]")

    # ── Practice Steps Table ─────────────────────────────────────────────────
    console.print("\n[bold green]실습 단계[/bold green]")
    step_table = Table(show_lines=True, box=None)
    step_table.add_column("Step", style="dim", width=6)
    step_table.add_column("제목", width=30)
    step_table.add_column("예상시간", justify="right", width=10)
    step_table.add_column("단축키", style="cyan", width=25)
    step_table.add_column("소제목 수", justify="right", width=10)

    for sec in lecture.practice_sections:
        for step in sec.steps:
            shortcuts = ", ".join(step.shortcuts[:4]) if step.shortcuts else "—"
            step_table.add_row(
                str(step.number),
                step.title[:30],
                f"~{step.estimated_minutes}분",
                shortcuts,
                str(len(step.sub_steps)),
            )

    console.print(step_table)

    # ── Segment Plan ─────────────────────────────────────────────────────────
    console.print("\n[bold]영상 세그먼트 계획[/bold]")
    seg_table = Table(show_lines=True, box=None)
    seg_table.add_column("Segment", style="cyan", width=30)
    seg_table.add_column("제목", width=35)
    seg_table.add_column("블록 수", justify="right", width=8)
    seg_table.add_column("예상시간", justify="right", width=10)

    for seg in segments:
        duration_min = seg.target_duration_seconds // 60
        seg_table.add_row(
            seg.segment_id,
            seg.title[:35],
            str(len(seg.narration_blocks)),
            f"~{duration_min}분",
        )

    console.print(seg_table)

    # ── Recording Requirements ───────────────────────────────────────────────
    week_video_map_path = TOOL_ROOT / "week_video_map.yaml"
    if week_video_map_path.exists():
        import yaml  # type: ignore[import-untyped]
        week_map = yaml.safe_load(week_video_map_path.read_text(encoding="utf-8")) or {}
        week_key = f"week{week_num:02d}"
        week_info: dict[str, Any] = week_map.get(week_key, {})
        status_val: str = week_info.get("status", "unknown")
        status_color = {"reuse": "green", "partial": "yellow", "new": "red"}.get(status_val, "white")
        console.print(f"\n[bold]녹화 현황:[/bold] [{status_color}]{status_val.upper()}[/{status_color}]")

        if status_val in ("new", "partial"):
            recordings = week_info.get("new_recordings_needed", [])
            if recordings:
                console.print("[yellow]  신규 촬영 필요:[/yellow]")
                for rec in recordings:
                    label = rec.get("step", "?")
                    duration = rec.get("duration", "?")
                    tool = rec.get("tool", "?")
                    console.print(f"    • {label} ({duration}, {tool})")
        else:
            existing = week_info.get("existing_files", [])
            if existing:
                console.print(f"[green]  기존 영상 재활용:[/green] {len(existing)}개")

    # ── Summary ──────────────────────────────────────────────────────────────
    total_mins = lecture.total_minutes
    console.print(f"\n[bold]총 예상 수업 시간:[/bold] {total_mins}분")
    console.print(f"[bold]이론 섹션:[/bold] {len(lecture.theory_sections)}개")
    console.print(f"[bold]실습 단계:[/bold] {sum(len(s.steps) for s in lecture.practice_sections)}개")
    console.print(f"[bold]생성될 세그먼트:[/bold] {len(segments)}개")

    # ── Confirmation ─────────────────────────────────────────────────────────
    console.print()
    if confirm:
        console.print("[green]--confirm 플래그로 자동 승인됨.[/green]")
        return

    proceed = click.confirm(
        "위 내용으로 영상을 생성하시겠습니까? (N을 누르면 취소)",
        default=False,
    )
    if proceed:
        console.print(f"\n[green]확인 완료![/green] 다음 명령어로 빌드를 시작하세요:")
        console.print(f"  [bold]lessonforge build week{week_num:02d}[/bold]")
    else:
        console.print("\n[yellow]취소되었습니다.[/yellow] 강의 내용을 수정한 후 다시 review를 실행하세요.")
        sys.exit(0)


if __name__ == "__main__":
    cli()
