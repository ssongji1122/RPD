"""YouTube metadata auto-generation.

Generates title, description, tags, and thumbnail info
from lecture content for YouTube uploads.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from ..parser.models import LectureNote, VideoSegment


@dataclass
class VideoMetadata:
    """YouTube-ready metadata for a video."""

    title: str
    description: str
    tags: list[str] = field(default_factory=list)
    category_id: str = "27"  # Education
    language: str = "ko"
    privacy_status: str = "unlisted"  # unlisted, private, public
    playlist_name: Optional[str] = None


def generate_metadata(
    segment: VideoSegment,
    lecture: LectureNote,
    *,
    base_tags: Optional[list[str]] = None,
    playlist: Optional[str] = None,
    privacy: str = "unlisted",
) -> VideoMetadata:
    """Generate YouTube metadata for a video segment.

    Args:
        segment: The video segment.
        lecture: The full lecture note (for context).
        base_tags: Base tags to include (from config).
        playlist: Playlist name.
        privacy: Privacy status.

    Returns:
        VideoMetadata ready for YouTube upload.
    """
    # Title: "[RPD Week 02] 세그먼트 제목 | 교수이름"
    title = (
        f"[RPD Week {lecture.week:02d}] {segment.title}"
    )
    if len(title) > 100:
        title = title[:97] + "..."

    # Description
    desc_parts = [
        f"로봇프러덕트 디자인 - Week {lecture.week:02d}: {lecture.title}",
        f"세그먼트 {segment.segment_number}: {segment.title}",
        "",
        "📋 학습 내용:",
    ]

    # Add learning objectives
    for obj in lecture.learning_objectives[:5]:
        desc_parts.append(f"  • {obj.text}")

    # Add section summary
    desc_parts.append("")
    desc_parts.append("📌 주요 항목:")
    for section in lecture.sections:
        if section.steps:
            for step in section.steps[:5]:
                desc_parts.append(f"  {step.number}. {step.title}")

    # Footer
    desc_parts.extend([
        "",
        "---",
        f"인하대학교 로봇프러덕트 디자인 (2026 Spring)",
        f"Blender 5.0 + AI Tools",
        "",
        "#블렌더 #Blender #3D모델링 #인하대학교 #로봇디자인",
    ])

    description = "\n".join(desc_parts)

    # Tags
    tags = list(base_tags or [])

    # Add week-specific tags from content
    week_tags = _extract_tags(lecture)
    tags.extend(week_tags)

    # Deduplicate while preserving order
    seen = set()
    unique_tags = []
    for tag in tags:
        lower = tag.lower()
        if lower not in seen:
            seen.add(lower)
            unique_tags.append(tag)
    tags = unique_tags[:30]  # YouTube limit: 500 chars total

    return VideoMetadata(
        title=title,
        description=description,
        tags=tags,
        privacy_status=privacy,
        playlist_name=playlist,
    )


def _extract_tags(lecture: LectureNote) -> list[str]:
    """Extract relevant tags from lecture content."""
    tags = []

    # Common tool/feature names to look for
    tag_keywords = {
        "모델링": "3D모델링",
        "sculpt": "스컬프팅",
        "UV": "UV맵핑",
        "texture": "텍스처",
        "material": "머티리얼",
        "lighting": "라이팅",
        "render": "렌더링",
        "animation": "애니메이션",
        "rigging": "리깅",
        "MCP": "MCP",
        "Claude": "ClaudeAI",
        "Meshy": "MeshyAI",
        "Mixamo": "Mixamo",
        "Eevee": "Eevee",
        "Cycles": "Cycles",
        "modifier": "모디파이어",
        "armature": "아마추어",
        "keyframe": "키프레임",
        "weight paint": "웨이트페인트",
        "particle": "파티클",
        "Geometry Nodes": "지오메트리노드",
    }

    full_text = lecture.title.lower()
    for section in lecture.sections:
        full_text += " " + section.title.lower()
        for step in section.steps:
            full_text += " " + step.title.lower()

    for keyword, tag in tag_keywords.items():
        if keyword.lower() in full_text:
            tags.append(tag)

    # Add week topic tag
    tags.append(f"Week{lecture.week:02d}")

    return tags
