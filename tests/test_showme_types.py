from tools.showme_lib.types import Card, Step, Video


def test_card_minimal_fields():
    card = Card(
        card_id="array-modifier",
        label="Array Modifier 이해",
        icon="repeat-2",
        category="modifier",
        weeks=[3],
        priority="P0",
        status="published",
        concept_md="복사기처럼...",
        usage_md="규칙적 반복...",
        pitfall_md="Origin 위치...",
        steps=[],
        videos=[],
        widget_id="array-modifier",
        blender_version="5.0",
        official_docs="https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/array.html",
        prerequisites=[],
        related=[],
    )
    assert card.card_id == "array-modifier"
    assert card.weeks == [3]
    assert card.has_widget is True


def test_card_no_widget():
    card = Card(
        card_id="x",
        label="x",
        icon="x",
        category="modeling",
        weeks=[1],
        priority="P1",
        status="draft",
        concept_md="",
        usage_md="",
        pitfall_md="",
        steps=[],
        videos=[],
        widget_id=None,
        blender_version="5.0",
        official_docs=None,
        prerequisites=[],
        related=[],
    )
    assert card.has_widget is False


def test_step_structure():
    step = Step(n=1, action="Cube 추가", hotkey="Shift + A", menu="Add → Mesh → Cube", screenshot=None, note=None)
    assert step.n == 1
    assert step.hotkey == "Shift + A"


def test_video_structure():
    video = Video(
        title="Array Modifier 완전정복",
        url="https://youtube.com/watch?v=xyz",
        channel="Blender Studio",
        duration_sec=480,
        language="en",
        blender_version="5.0",
        official=True,
        recommended_reason="공식 채널 + 5.0 기준",
    )
    assert video.official is True
