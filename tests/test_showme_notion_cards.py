import json
from pathlib import Path

from tools.showme_lib.notion_cards import normalize_card_page

FIXTURES = Path(__file__).parent / "fixtures" / "showme"


def test_normalize_card_minimal():
    page = json.loads((FIXTURES / "card_sample.json").read_text())
    card = normalize_card_page(page, video_pages_by_id={})

    assert card.card_id == "array-modifier"
    assert card.label == "Array Modifier 이해"
    assert card.icon == "repeat-2"
    assert card.category == "modifier"
    assert card.weeks == [3, 4]
    assert card.priority == "P0"
    assert card.status == "published"
    assert card.widget_id == "array-modifier"
    assert card.has_widget is True
    assert card.blender_version == "5.0"
    assert card.official_docs.startswith("https://docs.blender.org/")
    assert len(card.steps) == 1
    assert card.steps[0].n == 1
    assert card.steps[0].hotkey == "Shift + A"
    assert card.videos == []
    assert card.prerequisites == []
    assert card.related == []


def test_normalize_card_empty_widget_id():
    page = json.loads((FIXTURES / "card_sample.json").read_text())
    page["properties"]["widget_id"]["rich_text"] = []
    card = normalize_card_page(page, video_pages_by_id={})
    assert card.widget_id is None
    assert card.has_widget is False


def test_normalize_card_no_steps():
    page = json.loads((FIXTURES / "card_sample.json").read_text())
    page["properties"]["steps_json"]["rich_text"] = []
    card = normalize_card_page(page, video_pages_by_id={})
    assert card.steps == []
    assert card.has_steps is False
