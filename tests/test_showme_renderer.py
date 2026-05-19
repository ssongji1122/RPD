from tools.showme_lib.renderer import render_concept_html, render_steps_html, render_videos_html, render_card_html
from tools.showme_lib.types import Card, Step, Video


def _make_card(**overrides) -> Card:
    base = dict(
        card_id="array-modifier",
        label="Array Modifier 이해",
        icon="repeat-2",
        category="modifier",
        weeks=[3],
        priority="P0",
        status="published",
        concept_md="복사기처럼 **규칙적**으로 반복.",
        usage_md="볼트, 척추 같은 구조.",
        pitfall_md="Origin 위치 확인.",
        steps=[Step(n=1, action="Cube 추가", hotkey="Shift + A", menu="Add → Mesh → Cube", screenshot=None, note=None)],
        videos=[Video(title="X", url="https://youtube.com/y", channel="Blender Studio", duration_sec=480, language="en", blender_version="5.0", official=True, recommended_reason="공식")],
        widget_id="array-modifier",
        blender_version="5.0",
        official_docs="https://docs.blender.org/array",
        prerequisites=[],
        related=[],
    )
    base.update(overrides)
    return Card(**base)


def test_concept_renders_markdown_bold():
    html = render_concept_html(_make_card())
    assert "<strong>규칙적</strong>" in html
    assert "복사기처럼" in html


def test_steps_renders_hotkey_kbd():
    html = render_steps_html(_make_card())
    assert "<kbd>Shift + A</kbd>" in html
    assert "Cube 추가" in html
    assert "Add → Mesh → Cube" in html


def test_videos_renders_official_badge():
    html = render_videos_html(_make_card())
    assert "공식" in html
    assert 'href="https://youtube.com/y"' in html
    assert "Blender Studio" in html


def test_full_card_html_has_label_in_title():
    template = "<title>Show Me — {{LABEL}}</title><body class=\"{{BODY_CLASSES}}\">{{CONCEPT_HTML}}{{STEPS_HTML}}{{WIDGET_HTML}}{{USAGE_HTML}}{{PITFALL_HTML}}{{VIDEOS_HTML}}{{WIDGET_SCRIPT}}{{DOCS_HTML}}</body>"
    html = render_card_html(_make_card(), template=template)
    assert "<title>Show Me — Array Modifier 이해</title>" in html
    assert "has-widget" in html
    assert "has-steps" in html
    assert "has-videos" in html


def test_card_without_widget_has_no_widget_flag():
    template = "<body class=\"{{BODY_CLASSES}}\"></body>"
    html = render_card_html(_make_card(widget_id=None), template=template)
    assert "has-widget" not in html
    assert "has-steps" in html


def test_card_without_steps_no_steps_flag():
    template = "<body class=\"{{BODY_CLASSES}}\"></body>"
    html = render_card_html(_make_card(steps=[]), template=template)
    assert "has-steps" not in html
