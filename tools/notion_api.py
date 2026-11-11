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
import subprocess
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path

from runtime_paths import COURSE_SITE, ROOT

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
NOTION_API = "https://api.notion.com/v1"
NOTION_MAPPING = Path(
    os.environ.get("RPD_NOTION_MAPPING_JSON", str(ROOT / "tools" / "notion-mapping.json"))
).expanduser().resolve()
SUPPLEMENTS_JSON = Path(
    os.environ.get(
        "RPD_SUPPLEMENTS_JSON",
        str(COURSE_SITE / "assets" / "showme" / "_supplements.json"),
    )
).expanduser().resolve()


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


def get_page_title(page_id: str, token: str | None = None) -> str:
    """Return the plain-text title of a Notion page, or empty string on error."""
    try:
        result = notion_request("GET", f"/pages/{page_id}", token=token)
        props = result.get("properties", {})
        # Title can be under any property with type "title"
        for prop in props.values():
            if prop.get("type") == "title":
                return extract_text(prop.get("title", []))
    except Exception:
        pass
    return ""


def fetch_block_tree(page_id: str, token: str | None = None) -> list[dict]:
    """Fetch all blocks of a Notion page preserving parent-child nesting.

    Each block dict has a `children` key listing nested blocks (toggle, callout,
    column_list contents, etc.). This is the canonical tree representation used
    by the web mirror.

    For `link_to_page` blocks, injects `_resolved_title` so the renderer can
    display a meaningful label without an extra round-trip at render time.
    """
    title_cache: dict[str, str] = {}

    def resolve_title(pid: str) -> str:
        if pid not in title_cache:
            title_cache[pid] = get_page_title(pid, token=token)
        return title_cache[pid]

    def walk(parent_id: str) -> list[dict]:
        nodes: list[dict] = []
        for block in _get_page_blocks(parent_id, token=token):
            children: list[dict] = []
            if block.get("has_children"):
                children = walk(block["id"])
            block["children"] = children
            # Inject resolved title for link_to_page blocks
            if block.get("type") == "link_to_page":
                ltp = block.get("link_to_page", {})
                if ltp.get("type") == "page_id":
                    block["_resolved_title"] = resolve_title(ltp["page_id"])
            nodes.append(block)
        return nodes

    return walk(page_id)


def notion_page_url(page_id: str) -> str:
    return "https://www.notion.so/" + page_id.replace("-", "")


def get_page_title(page_id: str, token: str | None = None) -> str:
    """Fetch a Notion page title by ID."""
    page = notion_request("GET", f"/pages/{page_id}", token=token)
    props = page.get("properties") or {}
    for prop in props.values():
        if prop.get("type") == "title":
            return extract_text(prop.get("title") or []).strip()
    return ""


def enrich_link_to_page_blocks(blocks: list[dict], token: str | None = None) -> None:
    """Resolve link_to_page block titles from Notion API (mutates blocks in place)."""
    if not token:
        return

    title_cache: dict[str, str] = {}

    def title_for(page_id: str) -> str:
        if page_id in title_cache:
            return title_cache[page_id]
        try:
            title = get_page_title(page_id, token=token)
        except Exception:
            title = ""
        title_cache[page_id] = title
        return title

    def visit(nodes: list[dict]) -> None:
        for block in nodes:
            if block.get("type") == "link_to_page":
                link = block.get("link_to_page") or {}
                page_id = link.get("page_id")
                if page_id:
                    block["linked_page_url"] = notion_page_url(page_id)
                    title = title_for(page_id)
                    if title:
                        block["linked_page_title"] = title
            visit(block.get("children") or [])

    visit(blocks)


# ---------------------------------------------------------------------------
# Image / file download for offline mirror
# ---------------------------------------------------------------------------
def _resolve_block_file_url(block: dict) -> tuple[str, str] | None:
    """Return (url, source_kind) for blocks that carry an image/file payload, else None.

    Notion temporary signed URLs expire ~1 hour, so we download once at sync time.
    Only `file` (Notion-hosted) gets downloaded; `external` URLs are kept as-is.
    """
    btype = block.get("type", "")
    payload = block.get(btype) or {}
    if btype not in {"image", "file", "video", "pdf", "audio"}:
        return None
    file_data = payload.get("file") or {}
    external_data = payload.get("external") or {}
    if file_data.get("url"):
        return file_data["url"], "file"
    if external_data.get("url"):
        return external_data["url"], "external"
    return None


def _ext_from_url(url: str, fallback: str = ".bin") -> str:
    path = urllib.parse.urlparse(url).path
    suffix = Path(path).suffix
    return suffix if suffix else fallback


def _download_and_transcode_video(url: str, target: Path, req: urllib.request.Request) -> None:
    """Download a Notion-hosted video to a temp file, transcode to a compressed mp4 at target.

    Notion signed URLs expire ~1 hour, so we download once at sync time. Raw uploads
    (.mov screen recordings) are large, so we compress with ffmpeg to keep the repo small —
    matching the existing `clips/` "small compressed mp4" policy. On any download or
    transcode failure, raise so the caller leaves no `local_url` (renderer falls back to the
    remote URL rather than pointing at a missing/partial file).
    """
    suffix = _ext_from_url(url, ".mov")
    tmp_dir = Path(tempfile.mkdtemp(prefix="rpd-video-"))
    tmp_path = tmp_dir / f"src{suffix}"
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            tmp_path.write_bytes(resp.read())
        cmd = [
            "ffmpeg", "-y", "-i", str(tmp_path),
            "-vcodec", "libx264", "-crf", "28", "-preset", "fast",
            "-vf", "scale='min(1280,iw)':-2",
            "-acodec", "aac", "-b:a", "128k",
            "-movflags", "+faststart",
            str(target),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if result.returncode != 0:
            target.unlink(missing_ok=True)
            raise RuntimeError(f"ffmpeg failed (rc={result.returncode}): {result.stderr[-200:]}")
    finally:
        tmp_path.unlink(missing_ok=True)
        try:
            tmp_dir.rmdir()
        except OSError:
            pass


def download_block_assets(
    blocks: list[dict],
    dest_dir: Path,
    public_prefix: str,
) -> int:
    """Walk a block tree, download Notion-hosted assets to dest_dir.

    Mutates each affected block to add `local_url` (web-relative) and `local_path`
    (filesystem). External URLs are left untouched. Returns count of downloaded files.
    """
    dest_dir.mkdir(parents=True, exist_ok=True)
    downloaded = 0

    def visit(node_list: list[dict]) -> None:
        nonlocal downloaded
        for block in node_list:
            resolved = _resolve_block_file_url(block)
            if resolved is not None:
                url, kind = resolved
                if kind == "file":
                    block_id = block.get("id", "").replace("-", "")
                    if block_id:
                        is_video = block.get("type") == "video"
                        # 영상은 압축 mp4로 변환해 저장(repo 비대 방지 — clips/ 정책과 동일).
                        ext = ".mp4" if is_video else _ext_from_url(url)
                        target = dest_dir / f"{block_id}{ext}"
                        if not target.exists():
                            try:
                                req = urllib.request.Request(url, headers={"User-Agent": "rpd-notion-sync/1.0"})
                                if is_video:
                                    _download_and_transcode_video(url, target, req)
                                else:
                                    with urllib.request.urlopen(req, timeout=30) as resp:
                                        target.write_bytes(resp.read())
                                downloaded += 1
                            except Exception as exc:  # noqa: BLE001
                                print(f"  ! failed to download {url[:80]}...: {exc}")
                        # 파일이 존재하면(캐시 또는 방금 생성) local_url을 설정한다.
                        # 다운로드/변환 실패 시 target이 없으므로 local_url 미설정 →
                        # 렌더러가 원격 URL로 fallback(만료 전까지 동작, 깨진 로컬 경로 방지).
                        if target.exists():
                            block["local_url"] = f"{public_prefix.rstrip('/')}/{target.name}"
                            block["local_path"] = str(target)
            children = block.get("children") or []
            if children:
                visit(children)

    visit(blocks)
    return downloaded


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

    def append_link_section(title: str, items: list[dict], include_video_blocks: bool = False) -> None:
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
            preview_url = item.get("preview_url", "").strip() or link_url
            is_embeddable = bool(item.get("preview_url")) or bool(
                re.search(
                    r"(?:youtu\.be/[A-Za-z0-9_-]{11}|youtube\.com/(?:watch\?v=|embed/|shorts/|live/)[A-Za-z0-9_-]{11}|"
                    r"\.(?:mp4|webm|mov|m4v)(?:$|[?#]))",
                    preview_url,
                    flags=re.IGNORECASE,
                )
            )
            if include_video_blocks and is_embeddable:
                blocks.append({
                    "object": "block",
                    "type": "video",
                    "video": {
                        "type": "external",
                        "external": {"url": preview_url},
                        "caption": [{
                            "type": "text",
                            "text": {
                                "content": link_title,
                                "link": {"url": link_url},
                            },
                        }],
                    },
                })
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
    _supplements = load_supplements()
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

    append_link_section("공식 영상 튜토리얼", week.get("videos", []), include_video_blocks=True)
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


def parse_blocks_to_curriculum(
    blocks: list[dict],
    week_num: int,
    existing_week: dict,
    title: str | None = None,
) -> dict:
    """Pure function: parse a Notion block tree into curriculum-compatible data.

    Token-free. Used by both ``fetch_notion_to_curriculum`` (live API path) and
    the cache-based regeneration scripts.

    Heading_2 keywords recognized as section markers:
        - "학습 목표" or "실습"  -> steps section
        - "공식 영상"            -> videos
        - "공식 문서"            -> docs
        - "단축키"               -> shortcuts
        - "실수" / "해결"         -> mistakes
        - "과제"                 -> assignment

    Inside the steps section, each heading_3 starts a new step. Step body blocks:
        - paragraph / callout    -> copy
        - bulleted_list_item     -> goal
        - to_do / numbered_list_item -> tasks (one per item)
        - code                    -> tasks (split on lines that start with ``N.``)
    """
    result = {**existing_week}
    if title:
        result["title"] = title

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
    pending_video_preview = ""

    task_counter = 0  # global per-week task counter (preserves w{N}-t{n} uniqueness)

    def _append_task(label: str, detail: str = "") -> None:
        nonlocal task_counter
        if current_step is None or not label:
            return
        task_counter += 1
        current_step["tasks"].append({
            "id": f"w{week_num}-t{task_counter}",
            "label": label.strip(),
            "detail": detail.strip(),
        })

    def _append_copy(text: str) -> None:
        if current_step is None or not text:
            return
        if current_step["copy"]:
            current_step["copy"] += "\n\n" + text
        else:
            current_step["copy"] = text

    for block in blocks:
        btype = block.get("type", "")

        if btype == "heading_2":
            text = extract_text(block["heading_2"].get("rich_text", []))
            current_step = None
            if "학습 목표" in text or "실습" in text:
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
            # Strip "Step N: " prefix so the title matches the on-site label.
            clean_step_title = re.sub(r"^Step\s*\d+\s*[:：]\s*", "", text).strip() or text
            existing_step = existing_steps[len(steps)] if len(steps) < len(existing_steps) else {}
            current_step = {
                "title": clean_step_title,
                "copy": "",
                "goal": [],
                "done": list(existing_step.get("done", []) or []),
                "image": existing_step.get("image", ""),
                "tasks": [],
            }
            steps.append(current_step)

        elif btype == "paragraph" and current_section == "steps" and current_step is not None:
            text = extract_text(block["paragraph"].get("rich_text", []))
            _append_copy(text)

        elif btype == "callout" and current_section == "steps" and current_step is not None:
            text = extract_text(block["callout"].get("rich_text", []))
            _append_copy(text)

        elif btype == "paragraph" and current_section == "assignment":
            text = extract_text(block["paragraph"].get("rich_text", []))
            if text:
                if not assignment_title:
                    assignment_title = text
                else:
                    assignment_description_parts.append(text)

        elif btype == "callout" and current_section == "assignment":
            text = extract_text(block["callout"].get("rich_text", []))
            if text:
                if not assignment_title:
                    assignment_title = text
                else:
                    assignment_description_parts.append(text)

        elif btype == "numbered_list_item" and current_section == "assignment":
            text = extract_text(block["numbered_list_item"].get("rich_text", []))
            if text:
                assignment_checklist.append(text)

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

        elif btype == "code" and current_section == "steps" and current_step is not None:
            code_text = extract_text(block["code"].get("rich_text", []))
            for raw_line in code_text.strip().split("\n"):
                line = raw_line.strip()
                if not line:
                    continue
                # Accept numbered prefixes like "1.", "1)", "1 ."
                match = re.match(r"^\d+\s*[\.\)]\s+(.+)$", line)
                if not match:
                    continue
                label_full = match.group(1).strip()
                label, sep, detail = label_full.partition(" — ")
                _append_task(label, detail if sep else "")

        elif btype == "bulleted_list_item" and current_section == "steps" and current_step is not None:
            text = extract_text(block["bulleted_list_item"].get("rich_text", []))
            if text:
                current_step["goal"].append(text)

        elif btype == "bulleted_list_item" and current_section == "mistakes":
            text = extract_text(block["bulleted_list_item"].get("rich_text", []))
            if text:
                mistakes.append(text)

        elif btype == "video" and current_section == "videos":
            video_data = block.get("video", {})
            video_type = video_data.get("type", "")
            pending_video_preview = (
                video_data.get(video_type, {}).get("url", "")
                if video_type in ("external", "file")
                else ""
            )

        elif btype == "bulleted_list_item" and current_section in ("videos", "docs"):
            link = _extract_link(block["bulleted_list_item"].get("rich_text", []))
            if link:
                if current_section == "videos":
                    if pending_video_preview:
                        link["preview_url"] = pending_video_preview
                        pending_video_preview = ""
                    videos.append(link)
                else:
                    docs.append(link)

        elif btype == "to_do" and current_section == "steps" and current_step is not None:
            text = extract_text(block["to_do"].get("rich_text", []))
            if text:
                label, sep, detail = text.partition(" — ")
                _append_task(label, detail if sep else "")

        elif btype == "numbered_list_item" and current_section == "steps" and current_step is not None:
            text = extract_text(block["numbered_list_item"].get("rich_text", []))
            if text:
                label, sep, detail = text.partition(" — ")
                _append_task(label, detail if sep else "")

        elif btype == "to_do" and current_section == "assignment":
            text = extract_text(block["to_do"].get("rich_text", []))
            if text:
                assignment_checklist.append(text)

    if "steps" in seen_sections:
        # 빈 리스트도 명시적으로 반영한다(실습 섹션을 의도적으로 비운 주차).
        # `and steps`를 붙이면 실습이 0개일 때 이전 stale steps가 남는다.
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

    return parse_blocks_to_curriculum(blocks, week_num, existing_week, clean_title)


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
