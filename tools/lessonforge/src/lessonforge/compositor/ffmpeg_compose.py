"""FFmpeg-based video composition.

Combines slide images, title cards, and audio narration into final video files.
"""

import json
import os
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple


@dataclass
class VideoScene:
    """A single scene in the video timeline."""

    image_path: Path
    audio_path: Optional[Path] = None
    duration_seconds: float = 5.0
    scene_type: str = "slide"   # slide, title, section, step, outro, screen_recording
    narration_id: str = ""


@dataclass
class CompositionPlan:
    """Complete plan for a video segment."""

    segment_id: str
    scenes: List[VideoScene] = field(default_factory=list)
    output_path: Optional[Path] = None
    width: int = 1920
    height: int = 1080
    fps: int = 30

    @property
    def total_duration(self) -> float:
        return sum(s.duration_seconds for s in self.scenes)


def find_ffmpeg() -> str:
    """Find ffmpeg binary - system install or node_modules."""
    sys_ffmpeg = shutil.which("ffmpeg")
    if sys_ffmpeg:
        return sys_ffmpeg

    for search_dir in [Path.cwd(), Path(__file__).parent.parent.parent.parent]:
        candidate = search_dir / "node_modules" / "ffmpeg-static" / "ffmpeg"
        if candidate.exists():
            return str(candidate)

    raise RuntimeError(
        "FFmpeg not found. Install via:\n"
        "  brew install ffmpeg\n"
        "  OR: cd tools/lessonforge && npm install ffmpeg-static"
    )


def find_ffprobe() -> str:
    """Find ffprobe binary."""
    sys_ffprobe = shutil.which("ffprobe")
    if sys_ffprobe:
        return sys_ffprobe

    import platform
    arch: str = "arm64" if platform.machine() == "arm64" else "x64"
    system_name: str = "darwin" if platform.system() == "Darwin" else "linux"

    for search_dir in [Path.cwd(), Path(__file__).parent.parent.parent.parent]:
        # Use os.path.join to avoid pyright Path.__truediv__ inference bug
        candidate = Path(os.path.join(
            str(search_dir), "node_modules", "ffprobe-static",
            "bin", system_name, arch, "ffprobe",
        ))
        if candidate.exists():
            return str(candidate)

    raise RuntimeError("ffprobe not found")


def get_audio_duration(audio_path: Path) -> float:
    """Get audio file duration in seconds using ffprobe."""
    try:
        ffprobe = find_ffprobe()
        r = subprocess.run(
            [ffprobe, "-v", "quiet", "-print_format", "json",
             "-show_format", str(audio_path)],
            capture_output=True,
        )
        info = json.loads(r.stdout)
        return float(info["format"]["duration"])
    except Exception:
        pass

    try:
        from mutagen.mp3 import MP3  # type: ignore[import-untyped]
        return float(MP3(str(audio_path)).info.length)
    except Exception:
        return 5.0


def _run(cmd: List[str], timeout: int = 600) -> Tuple[int, str]:
    """Run subprocess, return (returncode, stderr_as_str)."""
    r = subprocess.run(cmd, capture_output=True, timeout=timeout)
    raw_err = r.stderr
    err: str = raw_err.decode("utf-8", errors="replace") if raw_err else ""
    return r.returncode, err


def compose_segment(
    plan: CompositionPlan,
    keystroke_srt: Optional[Path] = None,
    screen_recording: Optional[Path] = None,
) -> Path:
    """Compose a complete video segment from scenes.

    Args:
        plan: Composition plan with scenes and output path.
        keystroke_srt: Optional SRT file with keystroke overlays to burn in.
        screen_recording: Optional pre-recorded screen video for demo scenes.
    """
    ffmpeg = find_ffmpeg()

    # Resolve output path with explicit branching so pyright narrows to Path
    plan_out = plan.output_path
    output: Path = plan_out if plan_out is not None else Path("output") / plan.segment_id / "video.mp4"
    output.parent.mkdir(parents=True, exist_ok=True)

    # Step 1: Create individual scene clips
    scene_clips: List[Path] = []
    temp_dir: Path = output.parent / "_temp_scenes"
    temp_dir.mkdir(parents=True, exist_ok=True)

    for i, scene in enumerate(plan.scenes):
        clip_path: Path = temp_dir / f"scene_{i:03d}.mp4"
        rec = screen_recording
        if rec is not None and rec.exists() and scene.scene_type == "screen_recording":
            shutil.copy2(str(rec), str(clip_path))
        else:
            _render_scene(ffmpeg, scene, clip_path, plan.width, plan.height, plan.fps)
        scene_clips.append(clip_path)

    if not scene_clips:
        raise RuntimeError("No scenes to compose")

    # Step 2: Concatenate all scene clips
    concat_file: Path = temp_dir / "concat.txt"
    with open(str(concat_file), "w") as f:
        for clip in scene_clips:
            f.write(f"file '{clip.resolve()}'\n")

    intermediate: Path = output.parent / "_intermediate.mp4"
    code, err = _run([
        ffmpeg, "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-c:v", "libx264", "-preset", "medium", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart",
        str(intermediate),
    ])
    if code != 0:
        raise RuntimeError(f"FFmpeg concat failed:\n{err}")

    # Step 3: Apply keystroke SRT overlay if provided
    srt_file = keystroke_srt
    if srt_file is not None and srt_file.exists() and srt_file.stat().st_size > 10:
        _apply_srt_overlay(ffmpeg, intermediate, output, srt_file)
        intermediate.unlink(missing_ok=True)
    else:
        shutil.move(str(intermediate), str(output))

    shutil.rmtree(str(temp_dir), ignore_errors=True)
    return output


def _apply_srt_overlay(
    ffmpeg: str,
    input_video: Path,
    output_video: Path,
    srt_path: Path,
) -> None:
    """Burn SRT keystroke overlay into video.

    Style: White bold text, semi-transparent dark background, bottom-left.
    """
    srt_escaped = str(srt_path.resolve()).replace("\\", "\\\\").replace(":", "\\:")
    vf = (
        "subtitles='" + srt_escaped + "'"
        ":force_style='"
        "FontName=SF Pro Display,"
        "FontSize=38,Bold=1,"
        "PrimaryColour=&H00FFFFFF,"
        "BackColour=&H99000000,"
        "BorderStyle=3,Outline=0,Shadow=0,"
        "MarginL=50,MarginV=60"
        "'"
    )
    code, err = _run([
        ffmpeg, "-y",
        "-i", str(input_video),
        "-vf", vf,
        "-c:v", "libx264", "-preset", "medium", "-crf", "23",
        "-c:a", "copy",
        str(output_video),
    ])
    if code != 0:
        print("  ⚠️  SRT overlay failed (non-fatal):", err[:200])
        shutil.copy2(str(input_video), str(output_video))


def _render_scene(
    ffmpeg: str,
    scene: VideoScene,
    output: Path,
    width: int,
    height: int,
    fps: int,
) -> None:
    """Render a single scene: static image + optional audio → video clip."""
    duration = scene.duration_seconds
    image_path: Path = scene.image_path.resolve()

    # Narrow Optional[Path] via local variable
    audio_raw: Optional[Path] = scene.audio_path
    audio_path: Optional[Path] = audio_raw.resolve() if audio_raw is not None else None

    scale_pad = (
        f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=0x1a1a2e"
    )

    if audio_path is not None and audio_path.exists():
        duration = get_audio_duration(audio_path) + 0.5
        cmd: List[str] = [
            ffmpeg, "-y",
            "-loop", "1", "-i", str(image_path),
            "-i", str(audio_path),
            "-c:v", "libx264", "-tune", "stillimage",
            "-c:a", "aac", "-b:a", "128k",
            "-pix_fmt", "yuv420p",
            "-vf", scale_pad,
            "-t", f"{duration:.2f}", "-shortest",
            str(output),
        ]
    else:
        cmd = [
            ffmpeg, "-y",
            "-loop", "1", "-i", str(image_path),
            "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
            "-c:v", "libx264", "-tune", "stillimage",
            "-c:a", "aac",
            "-pix_fmt", "yuv420p",
            "-vf", scale_pad,
            "-t", f"{duration:.2f}", "-shortest",
            str(output),
        ]

    code, err = _run(cmd, timeout=120)
    if code != 0:
        err_preview = err[:500]  # type: ignore[index]
        raise RuntimeError(f"FFmpeg scene render failed for {scene.image_path}:\n{err_preview}")
