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
    assert js.startswith("const SHOWME_REGISTRY") or "const SHOWME_REGISTRY" in js
    assert '"array-modifier"' in js
    assert '"Array Modifier 이해"' in js
    assert '"repeat-2"' in js
    assert "week: [3, 4]" in js or '"week": [3, 4]' in js


def test_registry_skips_deprecated():
    cards = [
        _card("a", "A", "x", [1], status="published"),
        _card("b", "B", "y", [1], status="deprecated"),
    ]
    js = build_registry_js(cards)
    assert '"a"' in js
    assert '"b"' not in js


def test_catalog_groups_by_category():
    cards = [
        _card("array-modifier", "Array", "x", [3], category="modifier"),
        _card("extrude", "Extrude", "x", [3], category="edit-mode"),
        _card("mirror", "Mirror", "x", [3], category="modifier"),
    ]
    catalog = json.loads(build_catalog_json(cards))
    assert catalog["categoryMap"]["modifier"] == ["array-modifier", "mirror"]
    assert catalog["categoryMap"]["edit-mode"] == ["extrude"]


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


def test_catalog_merges_legacy_entries(tmp_path):
    """DB에 없는 기존 카테고리 매핑은 _catalog.json에 보존되어야 한다."""
    import json as _json
    from tools.showme_lib.index import build_catalog_json_merged

    legacy_path = tmp_path / "legacy.json"
    legacy_path.write_text(_json.dumps({
        "categoryMap": {
            "modifier": ["array-modifier", "boolean"],
            "edit-mode": ["extrude"],
        }
    }))
    cards = [_card("new-card", "New", "y", [1], category="object")]
    result = _json.loads(build_catalog_json_merged(cards, legacy_path=legacy_path))
    assert "new-card" in result["categoryMap"]["object"]
    assert "array-modifier" in result["categoryMap"]["modifier"]
    assert "boolean" in result["categoryMap"]["modifier"]
    assert "extrude" in result["categoryMap"]["edit-mode"]
