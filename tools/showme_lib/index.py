"""Regenerate _registry.js and _catalog.json from Card list."""
from __future__ import annotations

import json
import re
from pathlib import Path

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


_LEGACY_ENTRY = re.compile(r'"([a-z0-9-]+)":\s*\{[^}]+\}', re.DOTALL)


def _parse_legacy_registry(path: Path) -> dict[str, str]:
    """Extract { card_id: entry_literal } from existing _registry.js."""
    if not path.exists():
        return {}
    text = path.read_text()
    return {m.group(1): m.group(0) for m in _LEGACY_ENTRY.finditer(text)}


def build_registry_js_merged(cards: list[Card], legacy_path: Path) -> str:
    legacy = _parse_legacy_registry(legacy_path)
    db_ids = {c.card_id for c in _published(cards)}

    entries: list[str] = []
    for c in _published(cards):
        weeks = ", ".join(str(w) for w in c.weeks)
        entries.append(
            f'  "{c.card_id}": {{ '
            f'label: "{c.label}", '
            f'icon: "{c.icon}", '
            f'week: [{weeks}], '
            f'category: "{c.category}" '
            f'}}'
        )
    for legacy_id, literal in legacy.items():
        if legacy_id not in db_ids:
            entries.append(f"  {literal}")

    body = ",\n".join(entries)
    return f"{_HEADER}\nconst SHOWME_REGISTRY = {{\n{body}\n}};\n"


def build_catalog_json_merged(cards: list[Card], legacy_path: Path) -> str:
    legacy_catalog: dict[str, list[str]] = {}
    if legacy_path.exists():
        legacy_catalog = json.loads(legacy_path.read_text()).get("categoryMap", {})

    db_ids = {c.card_id for c in _published(cards)}
    category_map: dict[str, list[str]] = {}
    for c in _published(cards):
        category_map.setdefault(c.category, []).append(c.card_id)

    for cat, ids in legacy_catalog.items():
        for legacy_id in ids:
            if legacy_id not in db_ids:
                category_map.setdefault(cat, []).append(legacy_id)

    for ids in category_map.values():
        ids.sort()
    return json.dumps({"categoryMap": category_map}, ensure_ascii=False, indent=2)
