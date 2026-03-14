"""Configuration loading and validation."""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class TTSConfig(BaseModel):
    engine: str = "edge_tts"  # "edge_tts", "elevenlabs", "supertone"
    voice: str = "ko-KR-SunHiNeural"
    rate: str = "+5%"
    pitch: str = "+0Hz"

    class ElevenLabs(BaseModel):
        voice_id: str = ""
        model: str = "eleven_multilingual_v2"
        stability: float = 0.5
        similarity_boost: float = 0.8

    elevenlabs: ElevenLabs = Field(default_factory=ElevenLabs)


class VideoConfig(BaseModel):
    resolution: tuple[int, int] = (1920, 1080)
    fps: int = 30
    target_segment_minutes: tuple[int, int] = (20, 30)
    segments_per_week: tuple[int, int] = (2, 3)


class RecordingConfig(BaseModel):
    display: str = "1"

    class Blender(BaseModel):
        executable: str = "/Applications/Blender.app/Contents/MacOS/Blender"
        mcp_port: int = 9876

    class Browser(BaseModel):
        headless: bool = False
        viewport: tuple[int, int] = (1920, 1080)

    blender: Blender = Field(default_factory=Blender)
    browser: Browser = Field(default_factory=Browser)


class ThemeConfig(BaseModel):
    """Design tokens derived from marp-theme.css."""

    background: str = "#1a1a2e"
    surface: str = "#2d2d44"
    accent: str = "#00d4ff"
    emphasis: str = "#ff6b6b"
    text: str = "#eaeaea"
    text_muted: str = "#aaaaaa"
    border: str = "#3a3a55"
    font_body: str = "Pretendard, -apple-system, sans-serif"
    font_code: str = "JetBrains Mono, SF Mono, monospace"


class RemotionConfig(BaseModel):
    template: str = "lesson"
    theme: ThemeConfig = Field(default_factory=ThemeConfig)


class YouTubeConfig(BaseModel):
    playlist: str = "RPD 2026 Spring"
    category: str = "27"  # Education
    language: str = "ko"
    privacy: str = "unlisted"
    tags_base: list[str] = Field(
        default_factory=lambda: ["블렌더", "Blender", "3D모델링", "로봇디자인", "인하대학교"]
    )


class ProjectConfig(BaseModel):
    name: str = "로봇프러덕트 디자인 (RPD)"
    professor: str = "송지희"
    university: str = "인하대학교"
    semester: str = "2026 Spring"
    lectures_root: str = "../../weeks"
    output_root: str = "./output"


class LessonForgeConfig(BaseModel):
    """Top-level configuration for the LessonForge pipeline."""

    project: ProjectConfig = Field(default_factory=ProjectConfig)
    video: VideoConfig = Field(default_factory=VideoConfig)
    tts: TTSConfig = Field(default_factory=TTSConfig)
    recording: RecordingConfig = Field(default_factory=RecordingConfig)
    remotion: RemotionConfig = Field(default_factory=RemotionConfig)
    youtube: YouTubeConfig = Field(default_factory=YouTubeConfig)


def load_config(config_path: Path | str | None = None) -> LessonForgeConfig:
    """Load config from YAML file, falling back to defaults."""
    if config_path is None:
        return LessonForgeConfig()

    path = Path(config_path)
    if not path.exists():
        return LessonForgeConfig()

    with open(path) as f:
        data = yaml.safe_load(f) or {}

    return LessonForgeConfig(**data)


def resolve_lectures_root(config: LessonForgeConfig, config_path: Path) -> Path:
    """Resolve the lectures root directory relative to the config file."""
    base = config_path.parent if config_path else Path.cwd()
    return (base / config.project.lectures_root).resolve()
