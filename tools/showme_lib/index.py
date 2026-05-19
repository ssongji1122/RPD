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


def _format_week_literal(weeks: list[int]) -> str:
    """Emit scalar for single week (legacy-compatible), array for multi-week."""
    if len(weeks) == 1:
        return str(weeks[0])
    return "[" + ", ".join(str(w) for w in weeks) + "]"


def build_registry_js(cards: list[Card]) -> str:
    entries = []
    for c in _published(cards):
        entry = (
            f'  "{c.card_id}": {{ '
            f'label: "{c.label}", '
            f'icon: "{c.icon}", '
            f'week: {_format_week_literal(c.weeks)}, '
            f'category: "{c.category}" '
            f'}}'
        )
        entries.append(entry)
    body = ",\n".join(entries)
    return (
        f"{_HEADER}\n"
        f"var SHOWME_REGISTRY = {{\n{body}\n}};\n"
        f"if (typeof window !== \"undefined\") window.SHOWME_REGISTRY = SHOWME_REGISTRY;\n"
    )


def build_catalog_json(cards: list[Card]) -> str:
    """Emit catalog in legacy shape: top-level `manualSectionMap: {card_id: category}`."""
    section_map: dict[str, str] = {}
    for c in _published(cards):
        section_map[c.card_id] = c.category
    return json.dumps({"manualSectionMap": section_map}, ensure_ascii=False, indent=2)


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
        entries.append(
            f'  "{c.card_id}": {{ '
            f'label: "{c.label}", '
            f'icon: "{c.icon}", '
            f'week: {_format_week_literal(c.weeks)}, '
            f'category: "{c.category}" '
            f'}}'
        )
    for legacy_id, literal in legacy.items():
        if legacy_id not in db_ids:
            entries.append(f"  {literal}")

    body = ",\n".join(entries)
    return (
        f"{_HEADER}\n"
        f"var SHOWME_REGISTRY = {{\n{body}\n}};\n"
        f"if (typeof window !== \"undefined\") window.SHOWME_REGISTRY = SHOWME_REGISTRY;\n"
    )


def build_catalog_json_merged(cards: list[Card], legacy_path: Path) -> str:
    """Merge new card categorizations into legacy catalog, preserving all top-level keys.

    Legacy shape (real file): {
      "categoryOrder": [...],
      "manualSectionOrder": [...],
      "manualSectionMap": {card_id: section_name},
      "categoryDefaults": {...},
      "cardOverrides": {...}
    }
    We only update `manualSectionMap`. Other keys pass through unchanged.
    """
    legacy: dict = {}
    if legacy_path.exists():
        legacy = json.loads(legacy_path.read_text())

    section_map = dict(legacy.get("manualSectionMap", {}))
    for c in _published(cards):
        section_map[c.card_id] = c.category

    merged = dict(legacy)
    merged["manualSectionMap"] = section_map
    return json.dumps(merged, ensure_ascii=False, indent=2)
