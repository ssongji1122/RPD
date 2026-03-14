"""Screen recorder using FFmpeg + AVFoundation on macOS.

Records the screen (or a specific window region) to MP4 video files.
Uses macOS AVFoundation capture device via FFmpeg.
"""

from __future__ import annotations

import subprocess
import signal
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from ..compositor.ffmpeg_compose import find_ffmpeg


@dataclass
class RecordingConfig:
    """Configuration for screen recording."""

    display: str = "1"           # macOS display index
    width: int = 1920
    height: int = 1080
    fps: int = 30
    offset_x: int = 0
    offset_y: int = 0
    capture_mouse: bool = True
    audio_device: Optional[str] = None  # None = no system audio


class ScreenRecorder:
    """FFmpeg-based screen recorder for macOS.

    Usage:
        recorder = ScreenRecorder()
        recorder.start(Path("output/recording.mp4"))
        # ... do stuff ...
        recorder.stop()
    """

    def __init__(self, config: Optional[RecordingConfig] = None):
        self.config = config or RecordingConfig()
        self._process: Optional[subprocess.Popen] = None
        self._output_path: Optional[Path] = None
        self._ffmpeg = find_ffmpeg()

    @property
    def is_recording(self) -> bool:
        return self._process is not None and self._process.poll() is None

    def start(self, output_path: Path) -> None:
        """Start screen recording."""
        if self.is_recording:
            raise RuntimeError("Already recording")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        self._output_path = output_path

        cfg = self.config
        cmd = [
            self._ffmpeg,
            "-y",
            # macOS AVFoundation screen capture
            "-f", "avfoundation",
            "-framerate", str(cfg.fps),
            "-capture_cursor", "1" if cfg.capture_mouse else "0",
            "-i", f"{cfg.display}:none",  # display:audio (none=no audio)
            # Output settings
            "-vf", f"scale={cfg.width}:{cfg.height}",
            "-c:v", "libx264",
            "-preset", "ultrafast",  # Fast encoding during live recording
            "-crf", "23",
            "-pix_fmt", "yuv420p",
            str(output_path),
        ]

        self._process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def stop(self) -> Optional[Path]:
        """Stop recording and return the output file path."""
        if not self.is_recording:
            return self._output_path

        # Send 'q' to FFmpeg to gracefully stop
        try:
            self._process.stdin.write(b"q")
            self._process.stdin.flush()
        except (BrokenPipeError, OSError):
            pass

        try:
            self._process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self._process.send_signal(signal.SIGINT)
            try:
                self._process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._process.kill()

        self._process = None
        return self._output_path

    def record_duration(self, output_path: Path, duration_seconds: float) -> Path:
        """Record for a fixed duration and return the file path."""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        cfg = self.config
        cmd = [
            self._ffmpeg,
            "-y",
            "-f", "avfoundation",
            "-framerate", str(cfg.fps),
            "-capture_cursor", "1" if cfg.capture_mouse else "0",
            "-i", f"{cfg.display}:none",
            "-t", f"{duration_seconds:.1f}",
            "-vf", f"scale={cfg.width}:{cfg.height}",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-crf", "23",
            "-pix_fmt", "yuv420p",
            str(output_path),
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=int(duration_seconds) + 30,
        )

        if result.returncode != 0 and not output_path.exists():
            raise RuntimeError(f"Recording failed:\n{result.stderr[:500]}")

        return output_path


def record_with_actions(
    output_path: Path,
    actions: list[dict],
    config: Optional[RecordingConfig] = None,
) -> Path:
    """Record screen while executing a sequence of timed actions.

    Args:
        output_path: Where to save the recording.
        actions: List of dicts with 'callback' and 'delay_seconds' keys.
        config: Recording configuration.

    Returns:
        Path to the recorded video.
    """
    recorder = ScreenRecorder(config)
    recorder.start(output_path)

    try:
        for action in actions:
            delay = action.get("delay_seconds", 1.0)
            time.sleep(delay)
            callback = action.get("callback")
            if callback:
                callback()
    finally:
        recorder.stop()

    return output_path
