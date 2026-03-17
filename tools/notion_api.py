"""
Notion API shared module
========================
Stdlib-only helpers for interacting with the Notion API.
Extracted from admin-server.py so that other scripts
(CLI tools, sync jobs, etc.) can reuse the same logic.

Usage:
    from notion_api import (
        load_notion_mapping,
        notion_request,
        extract_text,
        get_page_blocks_recursive,
        fetch_notion_to_curriculum,
        delete_all_blocks,
        week_to_notion_blocks,
        sync_week_to_notion,
        get_notion_token,
    )
"""

from __future__ import annotations

import json
import os
import re
import urllib.request
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
NOTION_API = "https://api.notion.com/v1"
ROOT = Path(__file__).resolve().parent.parent
NOTION_MAPPING = ROOT / "tools" / "notion-mapping.json"
SUPPLEMENTS_JSON = ROOT / "course-site" / "assets" / "showme" / "_supplements.json"


# ---------------------------------------------------------------------------
# Token helper
# ---------------------------------------------------------------------------
def get_notion_token() -> str | None:
    """Return the Notion integration token from the environment."""
    return os.environ.get("NOTION_TOKEN")


# ---------------------------------------------------------------------------
# Mapping
# ---------------------------------------------------------------------------
def load_notion_mapping() -> dict:
    """Load week -> Notion page ID mapping from notion-mapping.json."""
    if not NOTION_MAPPING.exists():
        return {}
    with open(NOTION_MAPPING, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("weeks", {})


def load_supplements() -> dict:
    """Load showme supplement data from _supplements.json."""
    if not SUPPLEMENTS_JSON.exists():
        return {}
    with open(SUPPLEMENTS_JSON, encoding="utf-8") as f:
        return json.load(f)


def find_supplement_for_widget(widget_id: str, supplements: dict) -> dict | None:
    """Return the supplement whose targets include widget_id, or None."""
    for sup in supplements.values():
        if widget_id in sup.get("targets", []):
            return sup
    return None


# ---------------------------------------------------------------------------
# Low-level API request
# ---------------------------------------------------------------------------
def notion_request(
    method: str,
    endpoint: str,
    body: dict | None = None,
    token: str | None = None,
) -> dict:
    """Make an authenticated request to the Notion API.

    Parameters
    ----------
    method : str
        HTTP method (GET, POST, PATCH, DELETE, ...).
    endpoint : str
        API path starting with ``/`` (e.g. ``/pages/{id}``).
    body : dict | None
        JSON payload to send (optional).
    token : str | None
        Bearer token.  Falls back to ``get_notion_token()`` when *None*.
    """
    token = token or get_notion_token()
    if not token:
        raise RuntimeError("NOTION_TOKEN environment variable not set")

    url = f"{NOTION_API}{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }

    data = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


# ---------------------------------------------------------------------------
# Text extraction helpers
# ---------------------------------------------------------------------------
def extract_text(rich_text_list: list) -> str:
    """Extract plain text from a Notion rich_text array."""
    return "".join(rt.get("plain_text", "") for rt in rich_text_list)


def _extract_link(rich_text_list: list) -> dict | None:
    """Extract a title/url pair from Notion rich_text."""
    title = extract_text(rich_text_list).strip()
    if not title:
        return None

    url = ""
    for item in rich_text_list:
        url = item.get("href") or ""
        if not url:
            url = item.get("text", {}).get("link", {}).get("url", "")
        if url:
            break

    if not url:
        return None
    return {"title": title, "url": url}


# ---------------------------------------------------------------------------
# Block-level helpers
# ---------------------------------------------------------------------------
def _get_page_blocks(page_id: str, token: str | None = None) -> list[dict]:
    """Fetch all top-level blocks from a Notion page (paginated)."""
    all_blocks: list[dict] = []
    cursor = None
    while True:
        endpoint = f"/blocks/{page_id}/children?page_size=100"
        if cursor:
            endpoint += f"&start_cursor={cursor}"
        result = notion_request("GET", endpoint, token=token)
        all_blocks.extend(result.get("results", []))
        if not result.get("has_more"):
            break
        cursor = result.get("next_cursor")
    return all_blocks


def get_page_blocks_recursive(
    page_id: str, token: str | None = None
) -> list[dict]:
    """Fetch all page blocks in depth-first order, including nested children."""
    flat_blocks: list[dict] = []

    def walk(parent_id: str) -> None:
        for block in _get_page_blocks(parent_id, token=token):
            flat_blocks.append(block)
            if block.get("has_children"):
                walk(block["id"])

    walk(page_id)
    return flat_blocks


def delete_all_blocks(page_id: str, token: str | None = None) -> None:
    """Delete all block children from a Notion page."""
    blocks = _get_page_blocks(page_id, token=token)
    for block in blocks:
        try:
            notion_request("DELETE", f"/blocks/{block['id']}", token=token)
        except Exception:
            pass  # Some blocks may not be deletable


# ---------------------------------------------------------------------------
# Curriculum <-> Notion conversion
# ---------------------------------------------------------------------------
def week_to_notion_blocks(week: dict) -> list[dict]:
    """Convert a curriculum week object to Notion block children."""
    blocks: list[dict] = []

    def append_link_section(title: str, items: list[dict]) -> None:
        if not items:
            return
        blocks.append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": title}}]
            }
        })
        for item in items:
            link_title = item.get("title", "").strip()
            link_url = item.get("url", "").strip()
            if not link_title or not link_url:
                continue
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{
                        "type": "text",
                        "text": {
                            "content": link_title,
                            "link": {"url": link_url},
                        }
                    }]
                }
            })

    # Title heading
    blocks.append({
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": "학습 목표"}}]
        }
    })

    # Steps as checklist
    for step in week.get("steps", []):
        # Step title as heading_3
        blocks.append({
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{"type": "text", "text": {"content": step["title"]}}]
            }
        })
        # Step copy as paragraph
        if step.get("copy"):
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": step["copy"]}}]
                }
            })
        # Goals as bullet list
        for goal in step.get("goal", []):
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": goal}}]
                }
            })
        # Tasks as to_do items
        for task in step.get("tasks", []):
            text = task.get("label", "")
            if task.get("detail"):
                text += f" — {task['detail']}"
            blocks.append({
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": [{"type": "text", "text": {"content": text}}],
                    "checked": False
                }
            })

        # Supplement toggle (if available)
        showme_ids = step.get("showme", [])
        if isinstance(showme_ids, str):
            showme_ids = [showme_ids]
        _supplements = load_supplements()
        for sid in showme_ids:
            sup = find_supplement_for_widget(sid, _supplements)
            if not sup:
                continue
            toggle_children: list[dict] = []
            if sup.get("analogy"):
                a = sup["analogy"]
                toggle_children.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": f"{a.get('emoji', '')} {a['headline']}\n"},
                                "annotations": {"bold": True},
                            },
                            {"type": "text", "text": {"content": a["body"]}},
                        ]
                    },
                })
            if sup.get("before_after"):
                ba = sup["before_after"]
                toggle_children.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": "❌ Without: "},
                                "annotations": {"bold": True},
                            },
                            {"type": "text", "text": {"content": ba["before"] + "\n"}},
                            {
                                "type": "text",
                                "text": {"content": "✅ With: "},
                                "annotations": {"bold": True},
                            },
                            {"type": "text", "text": {"content": ba["after"]}},
                        ]
                    },
                })
            if sup.get("takeaway"):
                toggle_children.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": f"→ {sup['takeaway']}"},
                                "annotations": {"bold": True, "color": "blue"},
                            }
                        ]
                    },
                })
            if toggle_children:
                blocks.append({
                    "object": "block",
                    "type": "toggle",
                    "toggle": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": sup.get("title", "아직 헷갈린다면?")},
                            }
                        ],
                        "children": toggle_children,
                    },
                })

    append_link_section("공식 영상 튜토리얼", week.get("videos", []))
    append_link_section("공식 문서", week.get("docs", []))

    # Shortcuts section
    shortcuts = week.get("shortcuts", [])
    if shortcuts:
        blocks.append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "📌 단축키 퀵 레퍼런스"}}]
            }
        })
        shortcut_text = "\n".join(f"{s['keys'].ljust(24)}{s['action']}" for s in shortcuts)
        blocks.append({
            "object": "block",
            "type": "code",
            "code": {
                "rich_text": [{"type": "text", "text": {"content": shortcut_text}}],
                "language": "plain text"
            }
        })

    # Assignment section
    assignment = week.get("assignment", {})
    if assignment:
        blocks.append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "과제"}}]
            }
        })
        if assignment.get("title"):
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {"type": "text", "text": {"content": assignment["title"]}, "annotations": {"bold": True}},
                    ]
                }
            })
        if assignment.get("description"):
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": assignment["description"]}}]
                }
            })
        for item in assignment.get("checklist", []):
            blocks.append({
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": [{"type": "text", "text": {"content": item}}],
                    "checked": False
                }
            })

    # Mistakes section
    mistakes = week.get("mistakes", [])
    if mistakes:
        blocks.append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "⚠️ 흔한 실수와 해결법"}}]
            }
        })
        for m in mistakes:
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": m}}]
                }
            })

    return blocks


def sync_week_to_notion(week: dict, token: str | None = None) -> dict:
    """Push a curriculum week to its Notion page."""
    mapping = load_notion_mapping()
    week_num = str(week.get("week", ""))
    page_id = mapping.get(week_num)
    if not page_id:
        raise ValueError(f"No Notion page mapped for week {week_num}")

    # Update page title
    title_text = f"Week {week_num.zfill(2)}: {week.get('title', '')}"
    notion_request("PATCH", f"/pages/{page_id}", {
        "properties": {
            "title": {
                "title": [{"type": "text", "text": {"content": title_text}}]
            }
        }
    }, token=token)

    # Delete existing blocks and replace with new content
    delete_all_blocks(page_id, token=token)

    # Add new blocks (Notion API limit: 100 blocks per append)
    new_blocks = week_to_notion_blocks(week)
    for i in range(0, len(new_blocks), 100):
        chunk = new_blocks[i:i + 100]
        notion_request("PATCH", f"/blocks/{page_id}/children", {
            "children": chunk
        }, token=token)

    return {"ok": True, "page_id": page_id, "blocks_written": len(new_blocks)}


def fetch_notion_to_curriculum(
    week_num: int,
    existing_week: dict,
    token: str | None = None,
) -> dict:
    """Fetch a Notion page and extract curriculum-compatible data."""
    mapping = load_notion_mapping()
    page_id = mapping.get(str(week_num))
    if not page_id:
        raise ValueError(f"No Notion page mapped for week {week_num}")

    # Fetch page properties (title)
    page = notion_request("GET", f"/pages/{page_id}", token=token)
    title_parts = page.get("properties", {}).get("title", {}).get("title", [])
    raw_title = extract_text(title_parts)
    # Strip "Week NN: " prefix if present
    clean_title = re.sub(r"^(?:⭐\s*)?Week\s*\d+\s*[:：]\s*", "", raw_title).strip()

    # Fetch blocks
    blocks = get_page_blocks_recursive(page_id, token=token)

    # Parse blocks into structured sections
    result = {**existing_week, "title": clean_title or existing_week.get("title", "")}

    # Extract shortcuts from code blocks
    existing_steps = existing_week.get("steps", []) or []
    steps: list[dict] = []
    current_step: dict | None = None
    shortcuts: list[dict] = []
    mistakes: list[str] = []
    assignment_title = ""
    assignment_description_parts: list[str] = []
    assignment_checklist: list[str] = []
    videos: list[dict] = []
    docs: list[dict] = []
    current_section = ""
    seen_sections: set[str] = set()

    for block in blocks:
        btype = block.get("type", "")

        if btype == "heading_2":
            text = extract_text(block["heading_2"].get("rich_text", []))
            current_step = None
            if "학습 목표" in text:
                current_section = "steps"
                seen_sections.add("steps")
            elif "공식 영상" in text:
                current_section = "videos"
                seen_sections.add("videos")
            elif "공식 문서" in text:
                current_section = "docs"
                seen_sections.add("docs")
            elif "단축키" in text:
                current_section = "shortcuts"
                seen_sections.add("shortcuts")
            elif "실수" in text or "해결" in text:
                current_section = "mistakes"
                seen_sections.add("mistakes")
            elif "과제" in text:
                current_section = "assignment"
                seen_sections.add("assignment")
            else:
                current_section = text

        elif btype == "heading_3" and current_section == "steps":
            text = extract_text(block["heading_3"].get("rich_text", []))
            existing_step = existing_steps[len(steps)] if len(steps) < len(existing_steps) else {}
            current_step = {
                "title": text,
                "copy": "",
                "goal": [],
                "done": list(existing_step.get("done", []) or []),
                "image": existing_step.get("image", ""),
                "tasks": [],
            }
            steps.append(current_step)

        elif btype == "paragraph" and current_section == "steps" and current_step is not None:
            text = extract_text(block["paragraph"].get("rich_text", []))
            if text:
                if current_step["copy"]:
                    current_step["copy"] += "\n\n" + text
                else:
                    current_step["copy"] = text

        elif btype == "paragraph" and current_section == "assignment":
            text = extract_text(block["paragraph"].get("rich_text", []))
            if text:
                if not assignment_title:
                    assignment_title = text
                else:
                    assignment_description_parts.append(text)

        elif btype == "code" and current_section == "shortcuts":
            code_text = extract_text(block["code"].get("rich_text", []))
            for line in code_text.strip().split("\n"):
                line = line.strip()
                if not line:
                    continue
                # Try to split on multiple spaces
                parts = re.split(r"\s{2,}", line, maxsplit=1)
                if len(parts) == 2:
                    shortcuts.append({"keys": parts[0].strip(), "action": parts[1].strip()})

        elif btype == "bulleted_list_item" and current_section == "steps" and current_step is not None:
            text = extract_text(block["bulleted_list_item"].get("rich_text", []))
            if text:
                current_step["goal"].append(text)

        elif btype == "bulleted_list_item" and current_section == "mistakes":
            text = extract_text(block["bulleted_list_item"].get("rich_text", []))
            if text:
                mistakes.append(text)

        elif btype == "bulleted_list_item" and current_section in ("videos", "docs"):
            link = _extract_link(block["bulleted_list_item"].get("rich_text", []))
            if link:
                if current_section == "videos":
                    videos.append(link)
                else:
                    docs.append(link)

        elif btype == "to_do" and current_section == "steps" and current_step is not None:
            text = extract_text(block["to_do"].get("rich_text", []))
            if text:
                existing_task = {}
                if steps:
                    step_idx = len(steps) - 1
                    if step_idx < len(existing_steps):
                        existing_tasks = existing_steps[step_idx].get("tasks", []) or []
                        if len(current_step["tasks"]) < len(existing_tasks):
                            existing_task = existing_tasks[len(current_step["tasks"])]

                label, sep, detail = text.partition(" — ")
                current_step["tasks"].append({
                    "id": existing_task.get("id") or f"w{week_num}-t{len(current_step['tasks']) + 1}",
                    "label": label.strip(),
                    "detail": detail.strip() if sep else "",
                })

        elif btype == "to_do" and current_section == "assignment":
            text = extract_text(block["to_do"].get("rich_text", []))
            if text:
                assignment_checklist.append(text)

    if "steps" in seen_sections and steps:
        result["steps"] = steps
    if shortcuts:
        result["shortcuts"] = shortcuts
    if mistakes:
        result["mistakes"] = mistakes
    if "assignment" in seen_sections:
        assignment = {**(existing_week.get("assignment", {}) or {})}
        if assignment_title:
            assignment["title"] = assignment_title
        if assignment_description_parts:
            assignment["description"] = "\n\n".join(assignment_description_parts)
        assignment["checklist"] = assignment_checklist
        result["assignment"] = assignment
    if "videos" in seen_sections:
        result["videos"] = videos
    if "docs" in seen_sections:
        result["docs"] = docs

    return result


# ---------------------------------------------------------------------------
# Merge: notion data + overrides
# ---------------------------------------------------------------------------
def merge_curriculum(notion_data: list[dict], overrides: dict) -> list[dict]:
    """Merge Notion snapshot with admin overrides.

    - Week-level: any key in override (except 'steps') replaces the notion value.
    - Step-level: shallow merge by index ``{**notion_step, **override_step}``.
    - Uses deepcopy to prevent mutation of source data.
    """
    import copy

    weeks_ov = overrides.get("weeks", {})
    result = []
    for week in notion_data:
        week_num = str(week["week"])
        ov = weeks_ov.get(week_num, {})
        if not ov:
            result.append(copy.deepcopy(week))
            continue
        merged = copy.deepcopy(week)
        for key, val in ov.items():
            if key == "steps":
                continue
            merged[key] = copy.deepcopy(val)
        steps_ov = ov.get("steps", {})
        if steps_ov and "steps" in merged:
            for idx, step in enumerate(merged["steps"]):
                step_ov = steps_ov.get(str(idx), {})
                if step_ov:
                    merged["steps"][idx] = {**step, **copy.deepcopy(step_ov)}
        result.append(merged)
    return result
