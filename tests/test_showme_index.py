import json

from tools.showme_lib.index import build_registry_js, build_catalog_json
from tools.showme_lib.types import Card


def _card(card_id: str, label: str, icon: str, weeks: list[int], category: str = "modifier", status: str = "published") -> Card:
    return Card(
        card_id=card_id, label=label, icon=icon, category=category, weeks=weeks,
        priority="P1", status=status, concept_md="", usage_md="", pitfall_md="",
        steps=[], videos=[], widget_id=None, blender_version="5.0",
        official_docs=None, prerequisites=[], related=[],
    )


def test_registry_emits_js_object():
    cards = [
        _card("array-modifier", "Array Modifier 이해", "repeat-2", [3, 4]),
        _card("mirror", "Mirror Modifier", "flip-horizontal", [3]),
    ]
    js = build_registry_js(cards)
    assert "SHOWME_REGISTRY" in js
    assert "window.SHOWME_REGISTRY" in js  # ensures window-scope attachment for getRegistry()
    assert '"array-modifier"' in js
    assert '"Array Modifier 이해"' in js
    assert '"repeat-2"' in js
    # multi-week emits array
    assert "week: [3, 4]" in js
    # single-week emits scalar (legacy-compatible)
    assert "week: 3," in js or "week: 3 " in js


def test_registry_skips_deprecated():
    cards = [
        _card("a", "A", "x", [1], status="published"),
        _card("b", "B", "y", [1], status="deprecated"),
    ]
    js = build_registry_js(cards)
    assert '"a"' in js
    assert '"b"' not in js


def test_catalog_uses_manual_section_map_shape():
    """Catalog emits legacy-compatible shape: { manualSectionMap: {card_id: category} }."""
    cards = [
        _card("array-modifier", "Array", "x", [3], category="modifier"),
        _card("extrude", "Extrude", "x", [3], category="edit-mode"),
        _card("mirror", "Mirror", "x", [3], category="modifier"),
    ]
    catalog = json.loads(build_catalog_json(cards))
    assert catalog["manualSectionMap"]["array-modifier"] == "modifier"
    assert catalog["manualSectionMap"]["mirror"] == "modifier"
    assert catalog["manualSectionMap"]["extrude"] == "edit-mode"


def test_registry_merges_legacy_entries(tmp_path):
    """DB에 없는 기존 카드 항목은 _registry.js에 보존되어야 한다."""
    from tools.showme_lib.index import build_registry_js_merged

    legacy_path = tmp_path / "legacy.js"
    legacy_path.write_text(
        'const SHOWME_REGISTRY = {\n  "array-modifier": { label: "Array", icon: "x", week: 3 }\n};\n'
    )
    cards = [_card("new-card", "New", "y", [1])]
    js = build_registry_js_merged(cards, legacy_path=legacy_path)
    assert '"array-modifier"' in js
    assert '"new-card"' in js


def test_catalog_merge_preserves_legacy_keys_and_section_map(tmp_path):
    """Real legacy catalog has top-level keys (categoryOrder, manualSectionOrder,
    manualSectionMap, ...). Merge must preserve all of them and only update
    manualSectionMap for new cards."""
    import json as _json
    from tools.showme_lib.index import build_catalog_json_merged

    legacy_path = tmp_path / "legacy.json"
    legacy_path.write_text(_json.dumps({
        "categoryOrder": ["전체", "Generate Modifiers", "Edit Mode"],
        "manualSectionOrder": ["modeling", "user-interface"],
        "manualSectionMap": {
            "array-modifier": "modeling",
            "extrude": "modeling",
            "viewport-navigation": "user-interface",
        },
        "categoryDefaults": {"modeling": "Generate Modifiers"},
        "cardOverrides": {"extrude": {"label": "Custom"}},
    }))
    cards = [_card("collection-outliner", "Collection", "y", [3], category="object")]
    result = _json.loads(build_catalog_json_merged(cards, legacy_path=legacy_path))

    assert result["categoryOrder"] == ["전체", "Generate Modifiers", "Edit Mode"]
    assert result["manualSectionOrder"] == ["modeling", "user-interface"]
    assert result["categoryDefaults"] == {"modeling": "Generate Modifiers"}
    assert result["cardOverrides"] == {"extrude": {"label": "Custom"}}

    # legacy section_map entries preserved
    assert result["manualSectionMap"]["array-modifier"] == "modeling"
    assert result["manualSectionMap"]["extrude"] == "modeling"
    assert result["manualSectionMap"]["viewport-navigation"] == "user-interface"
    # new card added
    assert result["manualSectionMap"]["collection-outliner"] == "object"


def test_catalog_merge_with_missing_legacy(tmp_path):
    """If legacy catalog is absent, emit only manualSectionMap from current cards."""
    from tools.showme_lib.index import build_catalog_json_merged

    legacy_path = tmp_path / "nonexistent.json"
    cards = [_card("new-card", "New", "y", [1], category="object")]
    result = json.loads(build_catalog_json_merged(cards, legacy_path=legacy_path))
    assert result == {"manualSectionMap": {"new-card": "object"}}


def test_registry_week_scalar_vs_array():
    """Single-week emits scalar 3, multi-week emits array [3, 4]."""
    single = build_registry_js([_card("a", "A", "x", [3])])
    multi = build_registry_js([_card("b", "B", "x", [3, 4])])
    assert "week: 3," in single or "week: 3 " in single
    assert "week: [3, 4]" in multi
