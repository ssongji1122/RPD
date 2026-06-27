"""Notion Card DB page → Card dataclass normalization."""
from __future__ import annotations

import json
from typing import Any

from .types import Card, Step, Video


def _plain_text(rich_text_list: list[dict]) -> str:
    if not rich_text_list:
        return ""
    return "".join(part.get("plain_text", "") for part in rich_text_list)


def _title(prop: dict) -> str:
    return _plain_text(prop.get("title", []))


def _select(prop: dict) -> str | None:
    sel = prop.get("select")
    return sel.get("name") if sel else None


def _multi_select_ints(prop: dict) -> list[int]:
    return [int(opt["name"]) for opt in prop.get("multi_select", []) if opt["name"].isdigit()]


def _url(prop: dict) -> str | None:
    return prop.get("url")


def _relation_ids(prop: dict) -> list[str]:
    return [rel["id"] for rel in prop.get("relation", [])]


def _opt_text(prop: dict) -> str | None:
    txt = _plain_text(prop.get("rich_text", []))
    return txt or None


def _parse_steps(raw_json: str) -> list[Step]:
    if not raw_json:
        return []
    data = json.loads(raw_json)
    return [
        Step(
            n=s["n"],
            action=s["action"],
            hotkey=s.get("hotkey"),
            menu=s.get("menu"),
            screenshot=s.get("screenshot"),
            note=s.get("note"),
        )
        for s in data.get("steps", [])
    ]


def normalize_card_page(page: dict[str, Any], video_pages_by_id: dict[str, Video]) -> Card:
    props = page["properties"]
    steps_raw = _plain_text(props.get("steps_json", {}).get("rich_text", []))
    video_ids = _relation_ids(props.get("videos_relation", {}))
    videos = [video_pages_by_id[vid] for vid in video_ids if vid in video_pages_by_id]

    return Card(
        card_id=_title(props["card_id"]),
        label=_plain_text(props["label"].get("rich_text", [])),
        icon=_plain_text(props["icon"].get("rich_text", [])),
        category=_select(props.get("category", {})) or "modeling",
        weeks=_multi_select_ints(props.get("week", {})),
        priority=_select(props.get("priority", {})) or "P2",
        status=_select(props.get("status", {})) or "draft",
        concept_md=_plain_text(props.get("concept_md", {}).get("rich_text", [])),
        usage_md=_plain_text(props.get("usage_md", {}).get("rich_text", [])),
        pitfall_md=_plain_text(props.get("pitfall_md", {}).get("rich_text", [])),
        steps=_parse_steps(steps_raw),
        videos=videos,
        widget_id=_opt_text(props.get("widget_id", {})),
        blender_version=_plain_text(props.get("blender_version", {}).get("rich_text", [])) or "5.0",
        official_docs=_url(props.get("official_docs", {})),
        prerequisites=_relation_ids(props.get("prerequisites", {})),
        related=_relation_ids(props.get("related", {})),
    )
