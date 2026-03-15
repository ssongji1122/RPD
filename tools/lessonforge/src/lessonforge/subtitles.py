"""Draft subtitle generation for silent tutorial clips.

Builds SRT captions from clip metadata plus curated video notes when available.
This is intended for screen recordings that have little or no narration audio.
"""

from __future__ import annotations

import json
import re
import subprocess
from dataclasses import asdict, dataclass, field
from datetime import timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterable

import srt
import yaml
from PIL import Image, ImageDraw, ImageFont

from .compositor.ffmpeg_compose import find_ffmpeg, find_ffprobe

VIDEO_SUFFIXES = {".mp4", ".mov", ".mkv", ".avi", ".webm"}
TARGET_SECONDS_PER_CUE = 8.0
MIN_CUES = 2
MAX_CUES = 8
FONT_CANDIDATES = [
    Path("/System/Library/Fonts/AppleSDGothicNeo.ttc"),
    Path("/System/Library/Fonts/Supplemental/AppleGothic.ttf"),
    Path("/System/Library/Fonts/Helvetica.ttc"),
]


@dataclass
class ClipNotes:
    """Structured notes for one clip section in video_notes.md."""

    clip_number: int | None
    title: str
    core: str = ""
    details: list[str] = field(default_factory=list)


@dataclass
class SubtitleNoteLibrary:
    """Lookups for subtitle note sources."""

    by_number: dict[int, ClipNotes] = field(default_factory=dict)
    by_name: dict[str, ClipNotes] = field(default_factory=dict)

    def get_for_video(self, video_path: Path) -> ClipNotes | None:
        name_key = _normalize_file_key(video_path.name)
        if name_key in self.by_name:
            return self.by_name[name_key]

        clip_number = _extract_clip_number(video_path)
        if clip_number is not None and clip_number in self.by_number:
            return self.by_number[clip_number]

        return None


@dataclass
class SubtitleCue:
    """One timed subtitle entry."""

    start_seconds: float
    end_seconds: float
    text: str


@dataclass
class SubtitleDraft:
    """Generated subtitle plan for a single video."""

    video_path: Path
    duration_seconds: float
    clip_number: int | None
    title: str
    cue_source: str
    cues: list[SubtitleCue] = field(default_factory=list)


@dataclass
class VideoProbeInfo:
    """Basic stream information needed for rendering derived videos."""

    width: int
    height: int
    duration_seconds: float
    fps: float
    has_audio: bool
    sample_rate: int = 48000


@dataclass
class OutlineCardItem:
    """One numbered row on a chapter overview card."""

    title: str
    subtitle: str = ""


@dataclass
class OutlineCardContent:
    """Structured content for chapter overview and table-of-contents cards."""

    title: str
    summary: str
    items: list[OutlineCardItem] = field(default_factory=list)


def discover_videos(source: Path) -> list[Path]:
    """Return videos from a file or directory input."""
    if source.is_file():
        return [source]

    videos = [
        path for path in sorted(source.iterdir())
        if (
            path.is_file()
            and path.suffix.lower() in VIDEO_SUFFIXES
            and not path.name.startswith(".")
            and not path.name.startswith("._")
            and "preview" not in path.stem.lower()
            and "subtitled" not in path.stem.lower()
        )
    ]
    return videos


def infer_default_notes_paths(source: Path) -> list[Path]:
    """Guess relevant notes sources near the video source."""
    base = source.parent if source.is_file() else source
    candidates = [
        base / "video_notes.md",
        base.parent / "video_notes.md",
        base.parent / "week_02" / "video_notes.md",
        base.parent.parent / "week_02" / "video_notes.md",
        base / "week_video_map.yaml",
        base.parent / "week_video_map.yaml",
        base.parent.parent / "week_video_map.yaml",
        Path(__file__).resolve().parents[2] / "week_video_map.yaml",
    ]
    existing: list[Path] = []
    seen: set[Path] = set()
    for candidate in candidates:
        if candidate.exists() and candidate not in seen:
            existing.append(candidate)
            seen.add(candidate)
    return existing


def parse_clip_notes(notes_path: Path) -> SubtitleNoteLibrary:
    """Parse clip notes from the structured Markdown file."""
    library = SubtitleNoteLibrary()
    current: ClipNotes | None = None
    in_details = False

    for raw_line in notes_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        heading_match = re.match(r"^###\s+(\d+)\.\s+(.+)$", line)
        if heading_match:
            clip_number = int(heading_match.group(1))
            current = ClipNotes(
                clip_number=clip_number,
                title=_clean_markdown_text(heading_match.group(2)),
            )
            library.by_number[clip_number] = current
            in_details = False
            continue

        if current is None:
            continue

        if line.startswith("- **핵심**:"):
            current.core = _clean_markdown_text(line.split(":", 1)[1].strip())
            continue

        if line.startswith("- **다루는 내용**:"):
            in_details = True
            continue

        if line.startswith("- **추가 영상 아이디어**:"):
            in_details = False
            continue

        if in_details:
            detail_match = re.match(r"^\s*-\s+(.+)$", line)
            if detail_match:
                current.details.append(_clean_markdown_text(detail_match.group(1)))
                continue
            if line.strip():
                in_details = False

    return library


def parse_week_video_map(map_path: Path) -> SubtitleNoteLibrary:
    """Parse file-specific notes from week_video_map.yaml."""
    payload = yaml.safe_load(map_path.read_text(encoding="utf-8")) or {}
    library = SubtitleNoteLibrary()

    weeks = payload.get("weeks", {})
    for week_data in weeks.values():
        week_title = _clean_markdown_text(str(week_data.get("title", "")))
        for entry in week_data.get("existing_videos", []) or []:
            file_name = entry.get("file")
            if not file_name:
                continue

            covers = _clean_markdown_text(str(entry.get("covers", "")))
            notes_text = _clean_markdown_text(str(entry.get("notes", "")))
            title = _derive_title_from_cover(covers) or _infer_title_from_filename(Path(file_name))
            details = []
            if notes_text:
                details.append(notes_text)
            if week_title:
                details.append(f"{week_title} 관련 실습 흐름입니다.")
            if covers and covers != title:
                details.insert(0, covers)

            clip_note = ClipNotes(
                clip_number=_extract_clip_number(Path(file_name)),
                title=title,
                core=notes_text,
                details=details,
            )
            library.by_name[_normalize_file_key(file_name)] = clip_note

            clip_number = clip_note.clip_number
            if clip_number is not None and clip_number not in library.by_number:
                library.by_number[clip_number] = clip_note

    return library


def merge_note_libraries(*libraries: SubtitleNoteLibrary) -> SubtitleNoteLibrary:
    """Merge note sources, preserving earlier libraries as higher priority."""
    merged = SubtitleNoteLibrary()

    for library in reversed(libraries):
        merged.by_number.update(library.by_number)
        merged.by_name.update(library.by_name)

    return merged


def get_video_duration(video_path: Path) -> float:
    """Read video duration via ffprobe, falling back to 10 seconds."""
    ffprobe = find_ffprobe()
    result = subprocess.run(
        [
            ffprobe,
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            str(video_path),
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        return 10.0

    try:
        payload = json.loads(result.stdout)
        return float(payload["format"]["duration"])
    except Exception:
        return 10.0


def generate_subtitle_draft(
    video_path: Path,
    notes_library: SubtitleNoteLibrary | None = None,
) -> SubtitleDraft:
    """Generate timed subtitle cues for a silent clip."""
    clip_number = _extract_clip_number(video_path)
    note = notes_library.get_for_video(video_path) if notes_library else None
    duration = get_video_duration(video_path)
    units = _build_units(video_path, note)
    cue_groups = _group_units(units, duration)
    cues = _allocate_timings(cue_groups, duration)

    return SubtitleDraft(
        video_path=video_path,
        duration_seconds=duration,
        clip_number=clip_number,
        title=note.title if note else _infer_title_from_filename(video_path),
        cue_source="notes" if note else "filename",
        cues=cues,
    )


def build_outline_bullets(draft: SubtitleDraft, max_bullets: int = 5) -> list[str]:
    """Convert draft cues into concise chapter overview bullets."""
    bullets: list[str] = []
    seen: set[str] = set()
    prefix = f"{draft.title}: "

    for cue in draft.cues:
        for raw_line in cue.text.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith(prefix):
                line = line[len(prefix):].strip()
            line = re.sub(r"\s+", " ", line)
            if line not in seen:
                seen.add(line)
                bullets.append(line)
            if len(bullets) >= max_bullets:
                return bullets

    return bullets[:max_bullets]


def build_outline_card_content(
    draft: SubtitleDraft,
    *,
    max_items: int = 4,
) -> OutlineCardContent:
    """Turn draft cues into a stylized chapter overview structure."""
    bullets = build_outline_bullets(draft, max_bullets=max_items + 1)

    if not bullets:
        return OutlineCardContent(title=draft.title, summary=draft.title, items=[])

    summary = draft.title
    item_texts = bullets

    if len(bullets) >= 3 and _looks_like_summary_line(bullets[0]):
        summary = bullets[0]
        item_texts = bullets[1:]
    elif len(bullets) == 2 and bullets[1] != draft.title:
        summary = bullets[1]
        item_texts = [bullets[0]]
    elif bullets:
        summary = bullets[0]

    items = [_split_outline_item(text) for text in item_texts[:max_items]]
    if not items:
        items = [_split_outline_item(summary)]

    return OutlineCardContent(
        title=draft.title,
        summary=summary,
        items=items,
    )


def write_srt(draft: SubtitleDraft, output_path: Path) -> Path:
    """Persist a draft as an SRT sidecar file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    subtitles = [
        srt.Subtitle(
            index=index,
            start=timedelta(seconds=cue.start_seconds),
            end=timedelta(seconds=cue.end_seconds),
            content=cue.text,
        )
        for index, cue in enumerate(draft.cues, start=1)
    ]
    output_path.write_text(srt.compose(subtitles), encoding="utf-8")
    return output_path


def write_manifest(drafts: Iterable[SubtitleDraft], output_path: Path) -> Path:
    """Write a compact JSON manifest for review."""
    payload = []
    for draft in drafts:
        payload.append(
            {
                "video_path": str(draft.video_path),
                "duration_seconds": round(draft.duration_seconds, 3),
                "clip_number": draft.clip_number,
                "title": draft.title,
                "cue_source": draft.cue_source,
                "cues": [asdict(cue) for cue in draft.cues],
            }
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return output_path


def burn_in_subtitles(video_path: Path, srt_path: Path, output_path: Path) -> Path:
    """Render a new MP4 with burned or embedded subtitles."""
    ffmpeg = find_ffmpeg()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if _ffmpeg_supports_overlay(ffmpeg):
        return _hard_burn_with_overlays(ffmpeg, video_path, srt_path, output_path)

    escaped_srt = _escape_filter_value(str(srt_path.resolve()))
    vf = (
        "subtitles=filename="
        + escaped_srt
        + ":force_style='"
        "FontName=Arial,"
        "FontSize=34,"
        "Bold=1,"
        "PrimaryColour=&H00FFFFFF,"
        "BackColour=&H99000000,"
        "BorderStyle=3,"
        "Outline=0,"
        "Shadow=0,"
        "Alignment=2,"
        "MarginL=80,"
        "MarginR=80,"
        "MarginV=52"
        "'"
    )

    result = subprocess.run(
        [
            ffmpeg,
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(video_path),
            "-vf",
            vf,
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "20",
            "-c:a",
            "copy",
            str(output_path),
        ],
        capture_output=True,
        text=True,
        timeout=1800,
    )
    if result.returncode != 0:
        return _mux_subtitles(ffmpeg, video_path, srt_path, output_path)
    return output_path


def prepend_outline_opener(
    video_path: Path,
    outline_image_path: Path,
    output_path: Path,
    *,
    opener_seconds: float = 4.0,
) -> Path:
    """Prepend a chapter overview card to the beginning of a video."""
    ffmpeg = find_ffmpeg()
    probe = probe_video(video_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Prefer a fast concat-copy path so batch rendering long tutorials stays practical.
    if probe.has_audio:
        try:
            return _prepend_outline_opener_concat_copy(
                ffmpeg,
                video_path,
                outline_image_path,
                output_path,
                probe,
                opener_seconds=opener_seconds,
            )
        except RuntimeError:
            pass

    return _prepend_outline_opener_reencode(
        ffmpeg,
        video_path,
        outline_image_path,
        output_path,
        probe,
        opener_seconds=opener_seconds,
    )


def _prepend_outline_opener_concat_copy(
    ffmpeg: str,
    video_path: Path,
    outline_image_path: Path,
    output_path: Path,
    probe: VideoProbeInfo,
    *,
    opener_seconds: float,
) -> Path:
    """Encode only the opener clip, then remux-copy the original video body."""
    fps = _normalize_fps(probe.fps)
    sample_rate = probe.sample_rate or 48000

    with TemporaryDirectory(prefix="lessonforge-opener-") as temp_dir_str:
        temp_dir = Path(temp_dir_str)
        opener_clip_path = temp_dir / "opener.mp4"
        concat_list_path = temp_dir / "concat.txt"

        opener_result = subprocess.run(
            [
                ffmpeg,
                "-loglevel",
                "error",
                "-y",
                "-loop",
                "1",
                "-t",
                f"{opener_seconds:.3f}",
                "-i",
                str(outline_image_path),
                "-f",
                "lavfi",
                "-t",
                f"{opener_seconds:.3f}",
                "-i",
                f"anullsrc=channel_layout=stereo:sample_rate={sample_rate}",
                "-vf",
                f"fps={fps:.3f},format=yuv420p",
                "-c:v",
                "libx264",
                "-preset",
                "veryfast",
                "-crf",
                "20",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "aac",
                "-b:a",
                "128k",
                "-ar",
                str(sample_rate),
                "-movflags",
                "+faststart",
                str(opener_clip_path),
            ],
            capture_output=True,
            text=True,
            timeout=600,
        )
        if opener_result.returncode != 0:
            raise RuntimeError(opener_result.stderr.strip() or "ffmpeg opener render failed")

        concat_list_path.write_text(
            "\n".join(
                [
                    f"file '{_escape_concat_path(opener_clip_path.resolve())}'",
                    f"file '{_escape_concat_path(video_path.resolve())}'",
                ]
            )
            + "\n",
            encoding="utf-8",
        )

        concat_result = subprocess.run(
            [
                ffmpeg,
                "-loglevel",
                "error",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_list_path),
                "-c",
                "copy",
                "-movflags",
                "+faststart",
                str(output_path),
            ],
            capture_output=True,
            text=True,
            timeout=1800,
        )
        if concat_result.returncode != 0:
            raise RuntimeError(concat_result.stderr.strip() or "ffmpeg concat-copy prepend failed")

    return output_path


def _prepend_outline_opener_reencode(
    ffmpeg: str,
    video_path: Path,
    outline_image_path: Path,
    output_path: Path,
    probe: VideoProbeInfo,
    *,
    opener_seconds: float,
) -> Path:
    """Fallback path that re-encodes the full video."""

    fps = _normalize_fps(probe.fps)
    sample_rate = probe.sample_rate or 48000

    cmd = [
        ffmpeg,
        "-loglevel",
        "error",
        "-y",
        "-loop",
        "1",
        "-t",
        f"{opener_seconds:.3f}",
        "-i",
        str(outline_image_path),
        "-f",
        "lavfi",
        "-t",
        f"{opener_seconds:.3f}",
        "-i",
        f"anullsrc=channel_layout=stereo:sample_rate={sample_rate}",
        "-i",
        str(video_path),
    ]

    if probe.has_audio:
        filter_complex = (
            f"[0:v]fps={fps:.3f},format=yuv420p[v0];"
            f"[1:a]atrim=duration={opener_seconds:.3f}[a0];"
            f"[2:v]fps={fps:.3f},format=yuv420p[v1];"
            f"[2:a]aresample={sample_rate}[a1];"
            f"[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]"
        )
    else:
        cmd.extend(
            [
                "-f",
                "lavfi",
                "-t",
                f"{probe.duration_seconds:.3f}",
                "-i",
                f"anullsrc=channel_layout=stereo:sample_rate={sample_rate}",
            ]
        )
        filter_complex = (
            f"[0:v]fps={fps:.3f},format=yuv420p[v0];"
            f"[1:a]atrim=duration={opener_seconds:.3f}[a0];"
            f"[2:v]fps={fps:.3f},format=yuv420p[v1];"
            f"[3:a]atrim=duration={probe.duration_seconds:.3f}[a1];"
            f"[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]"
        )

    cmd.extend(
        [
            "-filter_complex",
            filter_complex,
            "-map",
            "[v]",
            "-map",
            "[a]",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "20",
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            "-movflags",
            "+faststart",
            str(output_path),
        ]
    )

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=3600,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "ffmpeg outline opener prepend failed")
    return output_path


def _build_units(video_path: Path, note: ClipNotes | None) -> list[str]:
    if note:
        units: list[str] = []
        if note.core:
            units.append(f"{note.title}: {note.core}")
        elif note.title:
            units.append(note.title)
        units.extend(note.details)
        cleaned = [_normalize_caption_text(unit) for unit in units if unit.strip()]
        if cleaned:
            return cleaned

    fallback_title = _infer_title_from_filename(video_path)
    return [
        _normalize_caption_text(f"{fallback_title} 작업 흐름을 보여주는 클립입니다."),
        _normalize_caption_text("핵심 화면 변화에 맞춰 필요한 메뉴와 도구를 차례대로 확인합니다."),
    ]


def _group_units(units: list[str], duration_seconds: float) -> list[str]:
    if not units:
        return []

    cue_count = round(duration_seconds / TARGET_SECONDS_PER_CUE)
    cue_count = max(MIN_CUES, cue_count)
    cue_count = min(MAX_CUES, cue_count, len(units))
    cue_count = max(1, cue_count)

    if cue_count >= len(units):
        return units

    groups: list[str] = []
    start = 0
    remaining_units = len(units)
    remaining_groups = cue_count

    while remaining_groups > 0:
        group_size = max(1, round(remaining_units / remaining_groups))
        chunk = units[start:start + group_size]
        groups.append("\n".join(chunk))
        start += group_size
        remaining_units -= group_size
        remaining_groups -= 1

    return groups


def _allocate_timings(groups: list[str], duration_seconds: float) -> list[SubtitleCue]:
    if not groups:
        return []

    total_weight = sum(max(len(group.replace("\n", " ").strip()), 1) for group in groups)
    start = 0.0
    cues: list[SubtitleCue] = []

    for index, group in enumerate(groups):
        weight = max(len(group.replace("\n", " ").strip()), 1)
        if index == len(groups) - 1:
            end = duration_seconds
        else:
            proportion = weight / total_weight
            end = start + max(duration_seconds * proportion, 1.6)

        cues.append(
            SubtitleCue(
                start_seconds=round(start, 3),
                end_seconds=round(min(end, duration_seconds), 3),
                text=group,
            )
        )
        start = end

    if cues:
        cues[-1].end_seconds = round(duration_seconds, 3)

    return cues


def _extract_clip_number(video_path: Path) -> int | None:
    match = re.match(r"^\s*(\d+)", video_path.stem)
    if not match:
        return None
    return int(match.group(1))


def _infer_title_from_filename(video_path: Path) -> str:
    title = re.sub(r"^\s*\d+[\s._-]*", "", video_path.stem)
    title = re.sub(r"[_-]+", " ", title)
    title = re.sub(r"\s+", " ", title).strip()
    if not title:
        return video_path.stem
    return title[0].upper() + title[1:]


def _clean_markdown_text(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _normalize_caption_text(text: str) -> str:
    text = _clean_markdown_text(text)
    text = text.replace("→", " -> ")
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return ""
    if text.endswith((".", "!", "?", "…")):
        return text
    return f"{text}."


def _escape_filter_value(value: str) -> str:
    """Escape a filesystem path for ffmpeg filter arguments."""
    value = value.replace("\\", "\\\\")
    value = value.replace(":", "\\:")
    value = value.replace(",", "\\,")
    value = value.replace("'", "\\'")
    value = value.replace("[", "\\[")
    value = value.replace("]", "\\]")
    value = value.replace(";", "\\;")
    value = value.replace(" ", "\\ ")
    return value


def _escape_concat_path(path: Path) -> str:
    """Escape a filesystem path for an ffmpeg concat list file."""
    return str(path).replace("\\", "\\\\").replace("'", r"'\''")


def _ffmpeg_supports_subtitles_filter(ffmpeg: str) -> bool:
    """Check whether the current FFmpeg build includes the subtitles filter."""
    result = subprocess.run(
        [ffmpeg, "-filters"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    return " subtitles " in result.stdout


def _ffmpeg_supports_overlay(ffmpeg: str) -> bool:
    """Check whether the current FFmpeg build includes the overlay filter."""
    result = subprocess.run(
        [ffmpeg, "-filters"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    return " overlay " in result.stdout


def _mux_subtitles(ffmpeg: str, video_path: Path, srt_path: Path, output_path: Path) -> Path:
    """Fallback when burn-in is unavailable: attach subtitles as a soft track."""
    result = subprocess.run(
        [
            ffmpeg,
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(video_path),
            "-i",
            str(srt_path),
            "-map",
            "0",
            "-map",
            "1:0",
            "-c:v",
            "copy",
            "-c:a",
            "copy",
            "-c:s",
            "mov_text",
            "-metadata:s:s:0",
            "language=kor",
            str(output_path),
        ],
        capture_output=True,
        text=True,
        timeout=1800,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "ffmpeg subtitle mux failed")
    return output_path


def _hard_burn_with_overlays(ffmpeg: str, video_path: Path, srt_path: Path, output_path: Path) -> Path:
    """Hard-burn subtitles by overlaying rendered cue images."""
    width, height = get_video_dimensions(video_path)
    subtitles = list(srt.parse(srt_path.read_text(encoding="utf-8")))

    if not subtitles:
        raise RuntimeError(f"No subtitles found in {srt_path}")

    with TemporaryDirectory(prefix="lessonforge-subtitles-") as temp_dir_str:
        temp_dir = Path(temp_dir_str)
        overlay_paths = []
        duration = get_video_duration(video_path)

        for index, subtitle in enumerate(subtitles, start=1):
            overlay_path = temp_dir / f"cue_{index:03d}.png"
            cue = SubtitleCue(
                start_seconds=subtitle.start.total_seconds(),
                end_seconds=subtitle.end.total_seconds(),
                text=subtitle.content,
            )
            _render_overlay_image(cue, overlay_path, width, height)
            overlay_paths.append(overlay_path)

        cmd = [ffmpeg, "-loglevel", "error", "-y", "-i", str(video_path)]
        for overlay_path in overlay_paths:
            cmd.extend(["-loop", "1", "-t", f"{duration:.3f}", "-i", str(overlay_path)])

        filter_parts = []
        current_label = "[0:v]"
        for index, subtitle in enumerate(subtitles, start=1):
            next_label = f"[v{index}]"
            start = subtitle.start.total_seconds()
            end = subtitle.end.total_seconds()
            filter_parts.append(
                f"{current_label}[{index}:v]overlay=0:0:eof_action=pass:"
                f"enable='between(t,{start:.3f},{end:.3f})'{next_label}"
            )
            current_label = next_label

        cmd.extend(
            [
                "-filter_complex",
                ";".join(filter_parts),
                "-map",
                current_label,
                "-map",
                "0:a?",
                "-c:v",
                "libx264",
                "-preset",
                "veryfast",
                "-crf",
                "20",
                "-c:a",
                "copy",
                str(output_path),
            ]
        )

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=1800,
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "ffmpeg hard-burn failed")

    return output_path


def get_video_dimensions(video_path: Path) -> tuple[int, int]:
    """Read video width and height."""
    ffprobe = find_ffprobe()
    result = subprocess.run(
        [
            ffprobe,
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-select_streams",
            "v:0",
            "-show_streams",
            str(video_path),
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        return (1920, 1080)

    try:
        payload = json.loads(result.stdout)
        stream = payload["streams"][0]
        return int(stream["width"]), int(stream["height"])
    except Exception:
        return (1920, 1080)


def probe_video(video_path: Path) -> VideoProbeInfo:
    """Collect video metadata required for opener rendering."""
    ffprobe = find_ffprobe()
    result = subprocess.run(
        [
            ffprobe,
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_streams",
            "-show_format",
            str(video_path),
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )

    if result.returncode != 0:
        return VideoProbeInfo(
            width=1920,
            height=1080,
            duration_seconds=10.0,
            fps=30.0,
            has_audio=False,
        )

    try:
        payload = json.loads(result.stdout)
        streams = payload.get("streams", [])
        format_data = payload.get("format", {})
        video_stream = next((s for s in streams if s.get("codec_type") == "video"), {})
        audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)

        width = int(video_stream.get("width", 1920))
        height = int(video_stream.get("height", 1080))
        fps = _parse_fps(str(video_stream.get("avg_frame_rate") or video_stream.get("r_frame_rate") or "30/1"))
        duration = float(format_data.get("duration", 10.0))
        sample_rate = int(audio_stream.get("sample_rate", 48000)) if audio_stream else 48000

        return VideoProbeInfo(
            width=width,
            height=height,
            duration_seconds=duration,
            fps=fps,
            has_audio=audio_stream is not None,
            sample_rate=sample_rate,
        )
    except Exception:
        return VideoProbeInfo(
            width=1920,
            height=1080,
            duration_seconds=10.0,
            fps=30.0,
            has_audio=False,
        )


def _render_overlay_image(
    cue: SubtitleCue,
    output_path: Path,
    width: int,
    height: int,
) -> Path:
    """Create a transparent PNG containing one subtitle cue."""
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    font_path = _resolve_font_path()
    font_size = max(34, int(width * 0.018))
    font = ImageFont.truetype(str(font_path), font_size)

    max_text_width = width - 240
    lines = _wrap_text(cue.text, draw, font, max_text_width)
    text = "\n".join(lines)

    bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=10, align="center")
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    padding_x = max(48, int(width * 0.025))
    padding_y = max(26, int(height * 0.018))
    box_width = min(width - 120, text_width + padding_x * 2)
    box_height = text_height + padding_y * 2
    box_x = (width - box_width) // 2
    box_y = height - box_height - max(42, int(height * 0.03))

    draw.rounded_rectangle(
        (box_x, box_y, box_x + box_width, box_y + box_height),
        radius=max(18, int(height * 0.012)),
        fill=(10, 12, 16, 200),
        outline=(255, 255, 255, 64),
        width=2,
    )

    text_x = width // 2
    text_y = box_y + padding_y
    draw.multiline_text(
        (text_x, text_y),
        text,
        font=font,
        fill=(255, 255, 255, 255),
        anchor="ma",
        align="center",
        spacing=10,
    )

    image.save(output_path)
    return output_path


def _wrap_text(text: str, draw: ImageDraw.ImageDraw, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    """Wrap subtitle text to fit the cue box width."""
    paragraphs = text.splitlines() or [text]
    wrapped: list[str] = []

    for paragraph in paragraphs:
        words = paragraph.split()
        if not words:
            wrapped.append("")
            continue

        current = words[0]
        for word in words[1:]:
            candidate = f"{current} {word}"
            bbox = draw.textbbox((0, 0), candidate, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current = candidate
            else:
                wrapped.append(current)
                current = word
        wrapped.append(current)

    return wrapped


def _resolve_font_path() -> Path:
    """Find a system font that can render Korean text."""
    for candidate in FONT_CANDIDATES:
        if candidate.exists():
            return candidate
    raise RuntimeError("No usable font found for hard-burn subtitles")


def _normalize_file_key(value: str) -> str:
    """Normalize file names for fuzzy lookup across punctuation changes."""
    stem = Path(value).stem.lower()
    return re.sub(r"[^0-9a-z가-힣]+", "", stem)


def _derive_title_from_cover(covers: str) -> str:
    """Strip generic prefixes from week_video_map titles."""
    cleaned = re.sub(r"^Step\s*[\d-]+\s*:\s*", "", covers, flags=re.IGNORECASE)
    return cleaned.strip()


def _looks_like_summary_line(text: str) -> bool:
    """Detect broad summary sentences that work better as a bottom takeaway."""
    lowered = text.lower()
    keywords = [
        "주요 영역",
        "관련 실습 흐름",
        "워크플로우",
        "흐름",
        "기초",
        "핵심",
        "소개",
    ]
    return any(keyword in lowered for keyword in keywords) and "—" not in text


def _split_outline_item(text: str) -> OutlineCardItem:
    """Split a line into bold title + smaller subtitle."""
    cleaned = text.strip().rstrip(".")

    for delimiter in ("—", "->", "→", ":"):
        if delimiter in cleaned:
            left, right = cleaned.split(delimiter, 1)
            left = left.strip()
            right = right.strip()
            if left and right:
                return OutlineCardItem(title=left, subtitle=right)

    paren_match = re.match(r"^(.*?)\s*\((.*?)\)$", cleaned)
    if paren_match:
        title = paren_match.group(1).strip()
        subtitle = paren_match.group(2).strip()
        if title and subtitle:
            return OutlineCardItem(title=title, subtitle=subtitle)

    if cleaned.endswith("입니다"):
        cleaned = cleaned.removesuffix("입니다").strip()

    return OutlineCardItem(title=cleaned)


def _parse_fps(value: str) -> float:
    """Parse ffprobe frame rate strings like '30000/1001'."""
    if "/" in value:
        num, den = value.split("/", 1)
        try:
            numerator = float(num)
            denominator = float(den)
            if denominator == 0:
                return 30.0
            return numerator / denominator
        except ValueError:
            return 30.0
    try:
        return float(value)
    except ValueError:
        return 30.0


def _normalize_fps(value: float) -> float:
    """Clamp FPS to a practical range for derived exports."""
    if value <= 1:
        return 30.0
    if value > 60:
        return 60.0
    return value
