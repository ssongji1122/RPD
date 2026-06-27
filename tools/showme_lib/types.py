"""Card / Step / Video data classes."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Step:
    n: int
    action: str
    hotkey: Optional[str]
    menu: Optional[str]
    screenshot: Optional[str]
    note: Optional[str]


@dataclass
class Video:
    title: str
    url: str
    channel: str
    duration_sec: int
    language: str
    blender_version: str
    official: bool
    recommended_reason: str


@dataclass
class Card:
    card_id: str
    label: str
    icon: str
    category: str
    weeks: list[int]
    priority: str
    status: str
    concept_md: str
    usage_md: str
    pitfall_md: str
    steps: list[Step]
    videos: list[Video]
    widget_id: Optional[str]
    blender_version: str
    official_docs: Optional[str]
    prerequisites: list[str]
    related: list[str]

    @property
    def has_widget(self) -> bool:
        return self.widget_id is not None and self.widget_id != ""

    @property
    def has_steps(self) -> bool:
        return len(self.steps) > 0

    @property
    def has_videos(self) -> bool:
        return len(self.videos) > 0
