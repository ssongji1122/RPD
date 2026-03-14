"""Edit Agent: Post-processing of raw screen recordings.

Uses auto-editor to remove silence gaps automatically,
then hands off to FFmpeg composer for final assembly.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Optional


def find_auto_editor() -> Optional[str]:
    """Find auto-editor binary in PATH or venv."""
    ae = shutil.which("auto-editor")
    if ae:
        return ae

    # Check common venv locations
    import sys
    venv_bin = Path(sys.executable).parent / "auto-editor"
    if venv_bin.exists():
        return str(venv_bin)

    return None


def remove_silence(
    input_video: Path,
    output_video: Path,
    *,
    margin: str = "0.2s",
    silent_threshold: float = 0.04,
    video_speed: float = 1.0,
    silent_speed: float = 99999,
) -> Path:
    """Remove silent portions from a video using auto-editor.

    Uses auto-editor v29.8.1+ API:
    - --edit audio:threshold=N  (detect silence by audio level)
    - --when-normal speed:X     (speed for non-silent sections)
    - --when-silent speed:X     (speed for silent sections; 99999 = skip)
    - --margin N                (buffer around detected audio, e.g. "0.2s")

    NOTE: --video-speed / --silent-speed were removed in v29.
          Use --when-normal / --when-silent instead.

    Args:
        input_video: Raw screen recording from OBS.
        output_video: Path for cleaned output video.
        margin: Keep N seconds around detected audio (default "0.2s").
        silent_threshold: Audio level below this is considered silent (0-1).
        video_speed: Speed for non-silent sections (1.0 = normal).
        silent_speed: Speed for silent sections (99999 = skip entirely).

    Returns:
        Path to cleaned video file.
    """
    auto_editor = find_auto_editor()
    if not auto_editor:
        print("⚠️  auto-editor not found - skipping silence removal")
        # Just copy the input as-is
        shutil.copy2(input_video, output_video)
        return output_video

    output_video.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        auto_editor,
        str(input_video),
        "--output", str(output_video),
        "--margin", margin,
        "--edit", f"audio:threshold={silent_threshold}",
        "--when-normal", f"speed:{video_speed}",
        "--when-silent", f"speed:{silent_speed}",
    ]

    print(f"  ✂️  Removing silence from {input_video.name}...")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)

    if result.returncode != 0:
        err_preview: str = result.stderr  # type: ignore[assignment]
        print(f"⚠️  auto-editor failed: {err_preview[:200]}")
        # Fallback: copy original
        shutil.copy2(input_video, output_video)

    return output_video


def get_video_duration(video_path: Path) -> float:
    """Get video duration in seconds using ffprobe."""
    import json
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        return 0.0

    try:
        result = subprocess.run(
            [ffprobe, "-v", "quiet", "-print_format", "json",
             "-show_format", str(video_path)],
            capture_output=True, text=True, timeout=30,
        )
        info = json.loads(result.stdout)
        return float(info["format"]["duration"])
    except Exception:
        return 0.0
