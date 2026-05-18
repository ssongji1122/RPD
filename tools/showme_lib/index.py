"""Regenerate _registry.js and _catalog.json from Card list."""
from __future__ import annotations

import json

from .types import Card


_HEADER = """// ============================================================
// Show Me 위젯 레지스트리 — DO NOT EDIT BY HAND
// Generated from Notion Card DB by tools/showme_build.py
// ============================================================
"""


def _published(cards: list[Card]) -> list[Card]:
    return [c for c in cards if c.status != "deprecated"]


def build_registry_js(cards: list[Card]) -> str:
    entries = []
    for c in _published(cards):
        weeks = ", ".join(str(w) for w in c.weeks)
        entry = (
            f'  "{c.card_id}": {{ '
            f'label: "{c.label}", '
            f'icon: "{c.icon}", '
            f'week: [{weeks}], '
            f'category: "{c.category}" '
            f'}}'
        )
        entries.append(entry)
    body = ",\n".join(entries)
    return f"{_HEADER}\nconst SHOWME_REGISTRY = {{\n{body}\n}};\n"


def build_catalog_json(cards: list[Card]) -> str:
    category_map: dict[str, list[str]] = {}
    for c in _published(cards):
        category_map.setdefault(c.category, []).append(c.card_id)
    for ids in category_map.values():
        ids.sort()
    return json.dumps({"categoryMap": category_map}, ensure_ascii=False, indent=2)
