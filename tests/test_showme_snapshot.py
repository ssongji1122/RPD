"""End-to-end snapshot: Notion-shaped page → rendered HTML.

Catches regressions in the full normalize → render chain by asserting on
key substrings of the output. Not a byte-exact snapshot to keep tests
robust against whitespace shifts in the template.
"""

from pathlib import Path

from tools.showme_lib.notion_cards import normalize_card_page
from tools.showme_lib.renderer import render_card_html

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "course-site" / "assets" / "showme" / "_template.v2.html"


PILOT_PAGE = {
    "object": "page",
    "id": "snapshot-pilot",
    "properties": {
        "card_id": {"title": [{"plain_text": "collection-outliner"}]},
        "label": {"rich_text": [{"plain_text": "Collection 과 Outliner 이해"}]},
        "icon": {"rich_text": [{"plain_text": "folder-tree"}]},
        "category": {"select": {"name": "object"}},
        "week": {"multi_select": [{"name": "3"}]},
        "priority": {"select": {"name": "P0"}},
        "status": {"select": {"name": "published"}},
        "concept_md": {"rich_text": [{"plain_text": "Collection은 **폴더**처럼 묶는 단위."}]},
        "usage_md": {"rich_text": [{"plain_text": "파츠 수가 많아질 때."}]},
        "pitfall_md": {"rich_text": [{"plain_text": "**눈 아이콘** 헷갈리기 쉬움."}]},
        "steps_json": {"rich_text": [{"plain_text": (
            '{"blender_version":"5.0","platform_note":null,"steps":['
            '{"n":1,"action":"Outliner 우클릭","hotkey":null,"menu":"New Collection","screenshot":null,"note":null},'
            '{"n":2,"action":"Move","hotkey":"M","menu":null,"screenshot":null,"note":null}'
            ']}'
        )}]},
        "widget_id": {"rich_text": []},
        "blender_version": {"rich_text": [{"plain_text": "5.0"}]},
        "official_docs": {"url": "https://docs.blender.org/manual/en/latest/scene_layout/collections/index.html"},
        "prerequisites": {"relation": []},
        "related": {"relation": []},
        "videos_relation": {"relation": []},
    },
}


def test_end_to_end_pilot_renders_expected_substrings():
    card = normalize_card_page(PILOT_PAGE, video_pages_by_id={})
    template = TEMPLATE.read_text()
    html = render_card_html(card, template)

    # Title injected
    assert "<title>Show Me — Collection 과 Outliner 이해</title>" in html

    # Body class flags: has-steps only (no widget, no videos)
    assert '<body class="has-steps">' in html

    # Concept markdown bold escaped + rendered
    assert "<strong>폴더</strong>" in html

    # Step with hotkey rendered as kbd
    assert "<kbd>M</kbd>" in html
    assert "Outliner 우클릭" in html
    assert "New Collection" in html

    # Usage + pitfall sections
    assert "<h3>언제 쓰나요</h3>" in html
    assert "<h3>흔한 실수</h3>" in html

    # Doc-ref footer
    assert 'href="https://docs.blender.org/' in html
    assert "Blender Docs" in html

    # NO quiz code (Phase 1 contract)
    assert "initQuiz" not in html
    assert "showme-quiz-complete" not in html

    # NO widget mount div (widget_id absent) — but CSS rule .widget-mount may still appear
    assert 'class="widget-mount"' not in html
    assert 'data-widget=' not in html

    # NO videos rendered (empty relation) — but CSS rule .videos-list may appear
    assert '<ul class="videos-list">' not in html

    # CSS class hooks exist for renderer-emitted markup
    assert ".card-concept" in html  # CSS rule present in template
    assert ".steps-list" in html


def test_end_to_end_widget_present_when_widget_id_set():
    page = {**PILOT_PAGE, "properties": {**PILOT_PAGE["properties"]}}
    page["properties"] = dict(PILOT_PAGE["properties"])
    page["properties"]["widget_id"] = {"rich_text": [{"plain_text": "collection-outliner"}]}

    card = normalize_card_page(page, video_pages_by_id={})
    template = TEMPLATE.read_text()
    html = render_card_html(card, template)

    assert 'has-widget' in html.split("<body")[1].split(">")[0]
    assert 'data-widget="collection-outliner"' in html
    assert 'src="widgets/collection-outliner.js"' in html
