#!/usr/bin/env python3
"""
RPD Admin Server
================
Stdlib-only HTTP server that manages course-site/data/curriculum.js
and serves static files from course-site/.

Usage:
    python3 tools/admin-server.py [--port 8765]

Environment variables:
    PORT       - server port (default 8765)
    ADMIN_KEY  - if set, PUT/POST require Authorization: Bearer <key>
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import shutil
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import urllib.request
from urllib.parse import unquote

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
COURSE_SITE = ROOT / "course-site"
CURRICULUM_JS = COURSE_SITE / "data" / "curriculum.js"
IMAGES_DIR = COURSE_SITE / "assets" / "images"
NOTION_MAPPING = ROOT / "tools" / "notion-mapping.json"
NOTION_TOKEN: str | None = os.environ.get("NOTION_TOKEN")
NOTION_API = "https://api.notion.com/v1"

# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------
ADMIN_KEY: str | None = os.environ.get("ADMIN_KEY")

# ---------------------------------------------------------------------------
# curriculum.js header/footer templates
# ---------------------------------------------------------------------------
CURRICULUM_HEADER = """\
// ============================================================
// 15주 블렌더 수업 커리큘럼 데이터
// 이 파일만 수정하면 메인 페이지와 각 주차 페이지가 자동 반영됨
// ============================================================

const CURRICULUM = """

CURRICULUM_FOOTER = """\
;

// Node.js 환경 대응
if (typeof module !== "undefined") module.exports = CURRICULUM;
"""

# ---------------------------------------------------------------------------
# MIME types (ensure common web types are registered)
# ---------------------------------------------------------------------------
EXTRA_MIME: dict[str, str] = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
    ".webp": "image/webp",
    ".woff": "font/woff",
    ".woff2": "font/woff2",
    ".ttf": "font/ttf",
    ".otf": "font/otf",
    ".mp4": "video/mp4",
    ".webm": "video/webm",
}


def guess_mime(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext in EXTRA_MIME:
        return EXTRA_MIME[ext]
    mt, _ = mimetypes.guess_type(path)
    return mt or "application/octet-stream"


# ---------------------------------------------------------------------------
# curriculum.js read / write helpers
# ---------------------------------------------------------------------------
def _js_to_json(text: str) -> str:
    """
    Convert a JS value expression (object/array literal) to valid JSON.

    Handles:
    - Stripping single-line comments (// ...) outside strings
    - Quoting bare (unquoted) object keys
    - Removing trailing commas before } or ]

    Uses a character-level scanner so it never modifies content inside
    double-quoted string literals.
    """
    result: list[str] = []
    i = 0
    length = len(text)

    while i < length:
        ch = text[i]

        # --- Double-quoted string: copy verbatim ---
        if ch == '"':
            j = i + 1
            while j < length:
                if text[j] == "\\":
                    j += 2  # skip escaped char
                    continue
                if text[j] == '"':
                    j += 1
                    break
                j += 1
            result.append(text[i:j])
            i = j
            continue

        # --- Single-line comment: skip to EOL ---
        if ch == "/" and i + 1 < length and text[i + 1] == "/":
            while i < length and text[i] != "\n":
                i += 1
            continue

        # --- Bare identifier key: quote it ---
        # A bare key appears after { or , or at start-of-line (after whitespace)
        # and is followed (with optional whitespace) by a colon.
        # We only trigger when we see a letter/underscore that is NOT inside a string.
        if ch.isalpha() or ch == "_":
            # Check if this looks like a bare key by scanning ahead for `:`
            j = i
            while j < length and (text[j].isalnum() or text[j] == "_"):
                j += 1
            # Skip whitespace between identifier and potential colon
            k = j
            while k < length and text[k] in " \t":
                k += 1
            if k < length and text[k] == ":":
                # Verify this is a key position: preceding non-whitespace
                # should be one of { , [ or newline (start of structure)
                preceding = "".join(result).rstrip()
                if preceding and preceding[-1] in "{,[\n":
                    # It's a bare key -- quote it
                    key = text[i:j]
                    result.append(f'"{key}"')
                    i = j
                    continue

            # Not a key -- just append the char
            result.append(ch)
            i += 1
            continue

        result.append(ch)
        i += 1

    output = "".join(result)

    # Remove trailing commas before } or ] (JS allows, JSON doesn't)
    output = re.sub(r",\s*([}\]])", r"\1", output)

    return output


def read_curriculum() -> list[dict]:
    """Read curriculum.js and return the parsed array."""
    text = CURRICULUM_JS.read_text(encoding="utf-8")

    # Find the array between `const CURRICULUM = ` and `];`
    start_marker = "const CURRICULUM = "
    start = text.find(start_marker)
    if start == -1:
        raise ValueError("Cannot find 'const CURRICULUM = ' in curriculum.js")
    start += len(start_marker)

    # Find the closing `];`
    end = text.find("];", start)
    if end == -1:
        raise ValueError("Cannot find closing '];' in curriculum.js")
    # Include the `]`
    array_text = text[start : end + 1]

    # Convert JS object literal syntax to valid JSON
    json_text = _js_to_json(array_text)

    return json.loads(json_text)


def write_curriculum(data: list[dict]) -> None:
    """Write curriculum array back to curriculum.js with backup."""
    # Backup
    if CURRICULUM_JS.exists():
        backup = CURRICULUM_JS.with_suffix(".js.bak")
        shutil.copy2(CURRICULUM_JS, backup)

    pretty = json.dumps(data, ensure_ascii=False, indent=2)
    content = CURRICULUM_HEADER + pretty + CURRICULUM_FOOTER
    CURRICULUM_JS.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# Notion API helpers
# ---------------------------------------------------------------------------
def _load_notion_mapping() -> dict:
    """Load week -> Notion page ID mapping."""
    if not NOTION_MAPPING.exists():
        return {}
    with open(NOTION_MAPPING, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("weeks", {})

def _notion_request(method: str, endpoint: str, body: dict | None = None) -> dict:
    """Make an authenticated request to the Notion API."""
    if not NOTION_TOKEN:
        raise RuntimeError("NOTION_TOKEN environment variable not set")

    url = f"{NOTION_API}{endpoint}"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }

    data = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def _week_to_notion_blocks(week: dict) -> list[dict]:
    """Convert a curriculum week object to Notion block children."""
    blocks = []

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

def _get_notion_page_blocks(page_id: str) -> list[dict]:
    """Fetch all blocks from a Notion page."""
    all_blocks = []
    cursor = None
    while True:
        endpoint = f"/blocks/{page_id}/children?page_size=100"
        if cursor:
            endpoint += f"&start_cursor={cursor}"
        result = _notion_request("GET", endpoint)
        all_blocks.extend(result.get("results", []))
        if not result.get("has_more"):
            break
        cursor = result.get("next_cursor")
    return all_blocks

def _delete_all_notion_blocks(page_id: str) -> None:
    """Delete all block children from a Notion page."""
    blocks = _get_notion_page_blocks(page_id)
    for block in blocks:
        try:
            _notion_request("DELETE", f"/blocks/{block['id']}")
        except Exception:
            pass  # Some blocks may not be deletable

def sync_week_to_notion(week: dict) -> dict:
    """Push a curriculum week to its Notion page."""
    mapping = _load_notion_mapping()
    week_num = str(week.get("week", ""))
    page_id = mapping.get(week_num)
    if not page_id:
        raise ValueError(f"No Notion page mapped for week {week_num}")

    # Update page title
    title_text = f"Week {week_num.zfill(2)}: {week.get('title', '')}"
    _notion_request("PATCH", f"/pages/{page_id}", {
        "properties": {
            "title": {
                "title": [{"type": "text", "text": {"content": title_text}}]
            }
        }
    })

    # Delete existing blocks and replace with new content
    _delete_all_notion_blocks(page_id)

    # Add new blocks (Notion API limit: 100 blocks per append)
    new_blocks = _week_to_notion_blocks(week)
    for i in range(0, len(new_blocks), 100):
        chunk = new_blocks[i:i+100]
        _notion_request("PATCH", f"/blocks/{page_id}/children", {
            "children": chunk
        })

    return {"ok": True, "page_id": page_id, "blocks_written": len(new_blocks)}

def _extract_text(rich_text_list: list) -> str:
    """Extract plain text from Notion rich_text array."""
    return "".join(rt.get("plain_text", "") for rt in rich_text_list)

def fetch_notion_to_curriculum(week_num: int, existing_week: dict) -> dict:
    """Fetch a Notion page and extract curriculum-compatible data."""
    mapping = _load_notion_mapping()
    page_id = mapping.get(str(week_num))
    if not page_id:
        raise ValueError(f"No Notion page mapped for week {week_num}")

    # Fetch page properties (title)
    page = _notion_request("GET", f"/pages/{page_id}")
    title_parts = page.get("properties", {}).get("title", {}).get("title", [])
    raw_title = _extract_text(title_parts)
    # Strip "Week NN: " prefix if present
    clean_title = re.sub(r"^(?:⭐\s*)?Week\s*\d+\s*[:：]\s*", "", raw_title).strip()

    # Fetch blocks
    blocks = _get_notion_page_blocks(page_id)

    # Parse blocks into structured sections
    result = {**existing_week, "title": clean_title or existing_week.get("title", "")}

    # Extract shortcuts from code blocks
    shortcuts = []
    mistakes = []
    assignment_checklist = []
    current_section = ""

    for block in blocks:
        btype = block.get("type", "")

        if btype == "heading_2":
            text = _extract_text(block["heading_2"].get("rich_text", []))
            if "단축키" in text:
                current_section = "shortcuts"
            elif "실수" in text or "해결" in text:
                current_section = "mistakes"
            elif "과제" in text:
                current_section = "assignment"
            else:
                current_section = text

        elif btype == "code" and current_section == "shortcuts":
            code_text = _extract_text(block["code"].get("rich_text", []))
            for line in code_text.strip().split("\n"):
                line = line.strip()
                if not line:
                    continue
                # Try to split on multiple spaces
                parts = re.split(r"\s{2,}", line, maxsplit=1)
                if len(parts) == 2:
                    shortcuts.append({"keys": parts[0].strip(), "action": parts[1].strip()})

        elif btype == "bulleted_list_item" and current_section == "mistakes":
            text = _extract_text(block["bulleted_list_item"].get("rich_text", []))
            if text:
                mistakes.append(text)

        elif btype == "to_do" and current_section == "assignment":
            text = _extract_text(block["to_do"].get("rich_text", []))
            if text:
                assignment_checklist.append(text)

    if shortcuts:
        result["shortcuts"] = shortcuts
    if mistakes:
        result["mistakes"] = mistakes
    if assignment_checklist:
        result.setdefault("assignment", {})["checklist"] = assignment_checklist

    return result


# ---------------------------------------------------------------------------
# Multipart parser (stdlib only)
# ---------------------------------------------------------------------------
def parse_multipart(body: bytes, content_type: str) -> dict[str, tuple[str, bytes]]:
    """
    Minimal multipart/form-data parser.
    Returns {field_name: (filename, file_bytes)} for file fields.
    """
    # Extract boundary from content-type
    match = re.search(r"boundary=([^\s;]+)", content_type)
    if not match:
        raise ValueError("No boundary found in Content-Type")
    boundary = match.group(1).encode()

    # Some clients prefix boundary with `--`, some don't in the header
    delimiter = b"--" + boundary
    parts = body.split(delimiter)

    result: dict[str, tuple[str, bytes]] = {}
    for part in parts:
        # Skip preamble and epilogue
        if part in (b"", b"--\r\n", b"--\n", b"--"):
            continue
        if part.startswith(b"--"):
            continue

        # Split headers from body
        if b"\r\n\r\n" in part:
            header_section, file_data = part.split(b"\r\n\r\n", 1)
        elif b"\n\n" in part:
            header_section, file_data = part.split(b"\n\n", 1)
        else:
            continue

        # Strip trailing \r\n from file data
        if file_data.endswith(b"\r\n"):
            file_data = file_data[:-2]
        elif file_data.endswith(b"\n"):
            file_data = file_data[:-1]

        header_text = header_section.decode("utf-8", errors="replace")

        # Extract field name
        name_match = re.search(r'name="([^"]+)"', header_text)
        if not name_match:
            continue
        field_name = name_match.group(1)

        # Extract filename (if file upload)
        filename_match = re.search(r'filename="([^"]*)"', header_text)
        filename = filename_match.group(1) if filename_match else ""

        result[field_name] = (filename, file_data)

    return result


# ---------------------------------------------------------------------------
# Request handler
# ---------------------------------------------------------------------------
class AdminHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the admin server."""

    server_version = "RPD-Admin/1.0"

    # -- helpers -----------------------------------------------------------

    def _set_cors(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, PUT, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def _send_json(self, data: dict | list, status: int = 200) -> None:
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._set_cors()
        self.end_headers()
        self.wfile.write(body)

    def _send_error_json(self, status: int, message: str) -> None:
        self._send_json({"ok": False, "error": message}, status)

    def _read_body(self) -> bytes:
        length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(length) if length > 0 else b""

    def _check_auth(self) -> bool:
        """Return True if authorised, False (and send 401) if not."""
        if ADMIN_KEY is None:
            return True
        auth = self.headers.get("Authorization", "")
        if auth == f"Bearer {ADMIN_KEY}":
            return True
        self._send_error_json(401, "Unauthorized")
        return False

    def _route_path(self) -> str:
        """Decoded, normalised request path."""
        return unquote(self.path).split("?", 1)[0]

    # -- verbs -------------------------------------------------------------

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self._set_cors()
        self.end_headers()

    def do_GET(self) -> None:
        path = self._route_path()

        # API: GET /api/curriculum
        if path == "/api/curriculum":
            try:
                data = read_curriculum()
                self._send_json(data)
            except Exception as exc:
                self._send_error_json(500, str(exc))
            return

        # API: GET /api/notion-status
        if path == "/api/notion-status":
            mapping = _load_notion_mapping()
            self._send_json({
                "configured": bool(NOTION_TOKEN),
                "mapping_loaded": bool(mapping),
                "weeks_mapped": len(mapping),
            })
            return

        # Static files
        self._serve_static(path)

    def do_PUT(self) -> None:
        if not self._check_auth():
            return

        path = self._route_path()

        # PUT /api/curriculum
        if path == "/api/curriculum":
            self._handle_put_curriculum()
            return

        # PUT /api/week/{n}/status
        week_status_match = re.match(r"^/api/week/(\d+)/status$", path)
        if week_status_match:
            week_num = int(week_status_match.group(1))
            self._handle_put_week_status(week_num)
            return

        self._send_error_json(404, "Not found")

    def do_POST(self) -> None:
        path = self._route_path()

        # POST /api/notion-quiz — no auth required (student-facing endpoint)
        if path == "/api/notion-quiz":
            self._handle_notion_quiz()
            return

        # All other POST endpoints require auth
        if not self._check_auth():
            return

        # POST /api/upload/{weekNum}/{stepIdx}
        upload_match = re.match(r"^/api/upload/(\d+)/(\d+)$", path)
        if upload_match:
            week_num = int(upload_match.group(1))
            step_idx = int(upload_match.group(2))
            self._handle_upload(week_num, step_idx)
            return

        # POST /api/notion-push/{weekNum}
        notion_push_match = re.match(r"^/api/notion-push/(\d+)$", path)
        if notion_push_match:
            week_num = int(notion_push_match.group(1))
            self._handle_notion_push(week_num)
            return

        # POST /api/notion-pull/{weekNum}
        notion_pull_match = re.match(r"^/api/notion-pull/(\d+)$", path)
        if notion_pull_match:
            week_num = int(notion_pull_match.group(1))
            self._handle_notion_pull(week_num)
            return

        self._send_error_json(404, "Not found")

    # -- API handlers ------------------------------------------------------

    def _handle_put_curriculum(self) -> None:
        body = self._read_body()
        try:
            data = json.loads(body)
        except json.JSONDecodeError as exc:
            self._send_error_json(400, f"Invalid JSON: {exc}")
            return

        if not isinstance(data, list):
            self._send_error_json(400, "Body must be a JSON array")
            return

        try:
            write_curriculum(data)
        except Exception as exc:
            self._send_error_json(500, f"Write failed: {exc}")
            return

        self._send_json({"ok": True})

    def _handle_put_week_status(self, week_num: int) -> None:
        body = self._read_body()
        try:
            payload = json.loads(body)
        except json.JSONDecodeError as exc:
            self._send_error_json(400, f"Invalid JSON: {exc}")
            return

        new_status = payload.get("status")
        if new_status not in ("done", "active", "upcoming"):
            self._send_error_json(
                400, 'status must be "done", "active", or "upcoming"'
            )
            return

        try:
            data = read_curriculum()
        except Exception as exc:
            self._send_error_json(500, f"Read failed: {exc}")
            return

        found = False
        for entry in data:
            if entry.get("week") == week_num:
                entry["status"] = new_status
                found = True
                break

        if not found:
            self._send_error_json(404, f"Week {week_num} not found")
            return

        try:
            write_curriculum(data)
        except Exception as exc:
            self._send_error_json(500, f"Write failed: {exc}")
            return

        self._send_json({"ok": True, "week": week_num, "status": new_status})

    def _handle_upload(self, week_num: int, step_idx: int) -> None:
        content_type = self.headers.get("Content-Type", "")
        if "multipart/form-data" not in content_type:
            self._send_error_json(400, "Expected multipart/form-data")
            return

        body = self._read_body()
        try:
            fields = parse_multipart(body, content_type)
        except Exception as exc:
            self._send_error_json(400, f"Multipart parse error: {exc}")
            return

        if "image" not in fields:
            self._send_error_json(400, 'No field named "image" found')
            return

        filename, file_data = fields["image"]
        if not filename:
            self._send_error_json(400, "No filename provided")
            return

        # Determine extension from original filename
        ext = os.path.splitext(filename)[1].lower()
        if not ext:
            ext = ".png"

        # Sanitize extension — allow common image types only
        allowed_ext = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}
        if ext not in allowed_ext:
            self._send_error_json(
                400, f"Unsupported image type: {ext}. Allowed: {sorted(allowed_ext)}"
            )
            return

        # Build destination path
        week_dir = IMAGES_DIR / f"week-{week_num:02d}"
        week_dir.mkdir(parents=True, exist_ok=True)
        dest_filename = f"step-{step_idx}{ext}"
        dest_path = week_dir / dest_filename

        # Write file
        dest_path.write_bytes(file_data)

        # Relative path from course-site/ root
        relative_path = f"assets/images/week-{week_num:02d}/{dest_filename}"

        # Update curriculum.js
        try:
            data = read_curriculum()
        except Exception as exc:
            self._send_error_json(500, f"Read curriculum failed: {exc}")
            return

        week_entry = None
        for entry in data:
            if entry.get("week") == week_num:
                week_entry = entry
                break

        if week_entry is None:
            self._send_error_json(404, f"Week {week_num} not found in curriculum")
            return

        steps = week_entry.get("steps", [])
        if step_idx < 0 or step_idx >= len(steps):
            self._send_error_json(
                400,
                f"Step index {step_idx} out of range (week {week_num} has {len(steps)} steps)",
            )
            return

        steps[step_idx]["image"] = relative_path

        try:
            write_curriculum(data)
        except Exception as exc:
            self._send_error_json(500, f"Write curriculum failed: {exc}")
            return

        self._send_json({"ok": True, "path": relative_path})

    def _handle_notion_push(self, week_num: int) -> None:
        """Push curriculum week data to Notion."""
        if not NOTION_TOKEN:
            self._send_error_json(503, "NOTION_TOKEN not configured")
            return

        try:
            data = read_curriculum()
        except Exception as exc:
            self._send_error_json(500, f"Read failed: {exc}")
            return

        week = None
        for entry in data:
            if entry.get("week") == week_num:
                week = entry
                break

        if not week:
            self._send_error_json(404, f"Week {week_num} not found")
            return

        try:
            result = sync_week_to_notion(week)
            self._send_json(result)
        except Exception as exc:
            self._send_error_json(500, f"Notion sync failed: {exc}")

    def _handle_notion_pull(self, week_num: int) -> None:
        """Pull data from Notion and return diff preview (does NOT auto-save)."""
        if not NOTION_TOKEN:
            self._send_error_json(503, "NOTION_TOKEN not configured")
            return

        try:
            data = read_curriculum()
        except Exception as exc:
            self._send_error_json(500, f"Read failed: {exc}")
            return

        existing = None
        for entry in data:
            if entry.get("week") == week_num:
                existing = entry
                break

        if not existing:
            self._send_error_json(404, f"Week {week_num} not found")
            return

        try:
            updated = fetch_notion_to_curriculum(week_num, existing)
            self._send_json({"ok": True, "week": updated})
        except Exception as exc:
            self._send_error_json(500, f"Notion fetch failed: {exc}")

    def _handle_notion_quiz(self) -> None:
        """Log a Show Me quiz completion to the Notion 제출/공개피드백 database."""
        # Load per-site config (gitignored), falling back to env var
        config_path = COURSE_SITE / "data" / "notion-config.json"
        token: str | None = None
        if config_path.exists():
            try:
                with open(config_path, encoding="utf-8") as f:
                    cfg = json.load(f)
                if not cfg.get("enabled"):
                    self._send_json({"ok": False, "reason": "disabled"})
                    return
                token = cfg.get("token") or NOTION_TOKEN
            except Exception as exc:
                self._send_error_json(500, f"Config read error: {exc}")
                return
        else:
            token = NOTION_TOKEN

        if not token:
            self._send_json({"ok": False, "reason": "no token configured"})
            return

        body = self._read_body()
        try:
            payload = json.loads(body)
        except json.JSONDecodeError as exc:
            self._send_error_json(400, f"Invalid JSON: {exc}")
            return

        req = urllib.request.Request(
            f"{NOTION_API}/pages",
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {token}",
                "Notion-Version": "2022-06-28",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req) as resp:
                result = json.loads(resp.read().decode("utf-8"))
            self._send_json({"ok": True, "id": result.get("id")})
        except urllib.error.HTTPError as exc:
            err_body = exc.read().decode("utf-8", errors="replace")
            self._send_error_json(exc.code, err_body)
        except Exception as exc:
            self._send_error_json(500, str(exc))

    # -- static file serving -----------------------------------------------

    def _serve_static(self, path: str) -> None:
        # Default: / -> admin.html
        if path == "/" or path == "":
            path = "/admin.html"

        # Security: prevent directory traversal
        # Resolve relative to COURSE_SITE and ensure it stays within
        try:
            requested = (COURSE_SITE / path.lstrip("/")).resolve()
        except (ValueError, OSError):
            self._send_error_json(400, "Invalid path")
            return

        if not str(requested).startswith(str(COURSE_SITE.resolve())):
            self._send_error_json(403, "Forbidden")
            return

        if not requested.is_file():
            self._send_error_json(404, f"Not found: {path}")
            return

        mime = guess_mime(str(requested))
        try:
            data = requested.read_bytes()
        except OSError as exc:
            self._send_error_json(500, str(exc))
            return

        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(data)))
        self._set_cors()
        self.end_headers()
        self.wfile.write(data)

    # -- logging -----------------------------------------------------------

    def log_message(self, fmt: str, *args) -> None:
        # Coloured status-code logging
        try:
            status = int(args[1])
        except (IndexError, ValueError, TypeError):
            status = 0

        if 200 <= status < 300:
            colour = "\033[32m"  # green
        elif 300 <= status < 400:
            colour = "\033[33m"  # yellow
        elif status >= 400:
            colour = "\033[31m"  # red
        else:
            colour = ""
        reset = "\033[0m" if colour else ""

        sys.stderr.write(
            f"{colour}{self.address_string()} - [{self.log_date_time_string()}] "
            f"{fmt % args}{reset}\n"
        )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="RPD Admin Server")
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("PORT", "8765")),
        help="Port to listen on (default: 8765 or PORT env var)",
    )
    args = parser.parse_args()

    # Validate curriculum.js exists
    if not CURRICULUM_JS.exists():
        print(f"ERROR: {CURRICULUM_JS} not found", file=sys.stderr)
        sys.exit(1)

    # Quick sanity check — can we parse it?
    try:
        entries = read_curriculum()
        week_count = len(entries)
    except Exception as exc:
        print(f"ERROR: Failed to parse curriculum.js: {exc}", file=sys.stderr)
        sys.exit(1)

    auth_mode = "ENABLED (ADMIN_KEY set)" if ADMIN_KEY else "DISABLED (development)"
    notion_mode = "ENABLED" if NOTION_TOKEN else "DISABLED (set NOTION_TOKEN)"
    notion_weeks = len(_load_notion_mapping()) if NOTION_MAPPING.exists() else 0

    HTTPServer.allow_reuse_address = True
    server = HTTPServer(("0.0.0.0", args.port), AdminHandler)

    print("=" * 60)
    print("  RPD Admin Server")
    print("=" * 60)
    print(f"  URL:        http://localhost:{args.port}/")
    print(f"  Static:     {COURSE_SITE}")
    print(f"  Curriculum: {CURRICULUM_JS} ({week_count} weeks)")
    print(f"  Auth:       {auth_mode}")
    print(f"  Notion:     {notion_mode} ({notion_weeks} weeks mapped)")
    print("=" * 60)
    print()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.server_close()


if __name__ == "__main__":
    main()
