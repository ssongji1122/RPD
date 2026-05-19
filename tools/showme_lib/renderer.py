"""Card → HTML renderer. Minimal markdown subset (bold, italic, paragraphs, links)."""
from __future__ import annotations

import html
import re

from .types import Card


_BOLD = re.compile(r"\*\*(.+?)\*\*")
_ITALIC = re.compile(r"(?<!\*)\*([^*]+?)\*(?!\*)")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def _md_to_html(md: str) -> str:
    if not md.strip():
        return ""
    paragraphs = [p.strip() for p in md.split("\n\n") if p.strip()]
    out = []
    for p in paragraphs:
        escaped = html.escape(p)
        escaped = _BOLD.sub(r"<strong>\1</strong>", escaped)
        escaped = _ITALIC.sub(r"<em>\1</em>", escaped)
        escaped = _LINK.sub(r'<a href="\2">\1</a>', escaped)
        out.append(f"<p>{escaped}</p>")
    return "\n".join(out)


def render_concept_html(card: Card) -> str:
    return f'<div class="card-concept">{_md_to_html(card.concept_md)}</div>'


def render_steps_html(card: Card) -> str:
    if not card.steps:
        return ""
    items = []
    for step in card.steps:
        parts = [f'<span class="step-n">{step.n}</span>', f'<span class="step-action">{html.escape(step.action)}</span>']
        if step.hotkey:
            parts.append(f'<kbd>{html.escape(step.hotkey)}</kbd>')
        if step.menu:
            parts.append(f'<span class="step-menu">{html.escape(step.menu)}</span>')
        if step.note:
            parts.append(f'<span class="step-note">{html.escape(step.note)}</span>')
        body = " ".join(parts)
        if step.screenshot:
            body += f'<img class="step-screenshot" src="{html.escape(step.screenshot)}" alt="">'
        items.append(f'<li class="step-item">{body}</li>')
    return f'<ol class="steps-list">{"".join(items)}</ol>'


def render_usage_html(card: Card) -> str:
    if not card.usage_md.strip():
        return ""
    return f'<div class="card-usage"><h3>언제 쓰나요</h3>{_md_to_html(card.usage_md)}</div>'


def render_pitfall_html(card: Card) -> str:
    if not card.pitfall_md.strip():
        return ""
    return f'<div class="card-pitfall"><h3>흔한 실수</h3>{_md_to_html(card.pitfall_md)}</div>'


def render_videos_html(card: Card) -> str:
    if not card.videos:
        return ""
    items = []
    for v in card.videos:
        badge = '<span class="badge badge-official">공식</span>' if v.official else ''
        items.append(
            f'<li class="video-item">'
            f'<a href="{html.escape(v.url)}" target="_blank" rel="noopener">{html.escape(v.title)}</a>'
            f' {badge}'
            f'<div class="video-meta">{html.escape(v.channel)} · {v.duration_sec // 60}분 · Blender {html.escape(v.blender_version)}</div>'
            f'<div class="video-reason">{html.escape(v.recommended_reason)}</div>'
            f'</li>'
        )
    return f'<ul class="videos-list">{"".join(items)}</ul>'


def render_widget_html(card: Card) -> str:
    if not card.has_widget:
        return ""
    return f'<div class="widget-mount" data-widget="{html.escape(card.widget_id)}"></div>'


def render_widget_script(card: Card) -> str:
    if not card.has_widget:
        return ""
    return f'<script src="widgets/{html.escape(card.widget_id)}.js" defer></script>'


def render_docs_html(card: Card) -> str:
    if not card.official_docs:
        return ""
    return f'<a class="doc-ref" href="{html.escape(card.official_docs)}" target="_blank" rel="noopener">Blender Docs</a>'


def _body_classes(card: Card) -> str:
    flags = []
    if card.has_widget:
        flags.append("has-widget")
    if card.has_steps:
        flags.append("has-steps")
    if card.has_videos:
        flags.append("has-videos")
    return " ".join(flags)


def render_card_html(card: Card, template: str) -> str:
    substitutions = {
        "{{LABEL}}": html.escape(card.label),
        "{{BODY_CLASSES}}": _body_classes(card),
        "{{CONCEPT_HTML}}": render_concept_html(card),
        "{{STEPS_HTML}}": render_steps_html(card),
        "{{WIDGET_HTML}}": render_widget_html(card),
        "{{USAGE_HTML}}": render_usage_html(card),
        "{{PITFALL_HTML}}": render_pitfall_html(card),
        "{{VIDEOS_HTML}}": render_videos_html(card),
        "{{WIDGET_SCRIPT}}": render_widget_script(card),
        "{{DOCS_HTML}}": render_docs_html(card),
    }
    out = template
    for k, v in substitutions.items():
        out = out.replace(k, v)
    return out
