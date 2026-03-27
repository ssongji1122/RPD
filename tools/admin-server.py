#!/usr/bin/env python3
"""
RPD Admin Server
================
Stdlib-only HTTP server that manages the canonical curriculum
(`weeks/site-data.json`), regenerates public site assets, and serves
static files from `course-site/`.

Usage:
    ADMIN_KEY=... python3 tools/admin-server.py [--host 127.0.0.1] [--port 8765]

Environment variables:
    PORT       - server port (default 8765)
    HOST       - bind host (default 127.0.0.1)
    ADMIN_KEY  - required admin password for cookie-based login
"""

from __future__ import annotations

import argparse
import hashlib
from http import cookies
import json
import mimetypes
import os
import re
import shutil
import secrets
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse, parse_qs

from content_pipeline import (
    compute_curriculum_diff,
    content_version,
    load_canonical_curriculum,
    write_canonical_curriculum,
    write_generated_outputs,
)
from notion_api import (
    load_notion_mapping,
    sync_week_to_notion,
    week_to_notion_blocks,
)
from grading_db import (
    query_submissions,
    query_grades,
    _load_grading_ids,
)
from runtime_paths import (
    AUDIT_LOG_PATH,
    CANONICAL_JSON,
    COURSE_SITE,
    IMAGES_DIR,
    ROOT,
    VIDEOS_DIR,
    WEEK_UI_JSON,
    WEEKS_DIR,
)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
CURRICULUM_JS = COURSE_SITE / "data" / "curriculum.js"
NOTION_TOKEN: str | None = os.environ.get("NOTION_TOKEN")
MOCK_NOTION_SYNC = os.environ.get("RPD_MOCK_NOTION") == "1"

# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------
ADMIN_KEY: str | None = os.environ.get("ADMIN_KEY")
SESSION_COOKIE_NAME = "rpd_admin_session"
SESSION_TTL_SECONDS = int(os.environ.get("ADMIN_SESSION_TTL", "28800"))
ADMIN_SESSIONS: dict[str, dict[str, float]] = {}

# ---------------------------------------------------------------------------
# curriculum.js header/footer templates
# ---------------------------------------------------------------------------
LECTURE_SYNC_START = "<!-- AUTO:CURRICULUM-SYNC:START -->"
LECTURE_SYNC_END = "<!-- AUTO:CURRICULUM-SYNC:END -->"

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
# curriculum canonical read / write helpers
# ---------------------------------------------------------------------------
def read_curriculum() -> list[dict]:
    """Read the canonical curriculum payload from weeks/site-data.json."""
    return load_canonical_curriculum()


def write_curriculum(data: list[dict]) -> dict[str, str | int]:
    """Write canonical curriculum and regenerate public site data."""
    if CURRICULUM_JS.exists():
        backup = CURRICULUM_JS.with_suffix(".js.bak")
        shutil.copy2(CURRICULUM_JS, backup)

    normalized = write_canonical_curriculum(data)
    result = write_generated_outputs(normalized)
    return result


def _read_json_file(path: Path) -> dict:
    with open(path, encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{path.name} must be a JSON object")
    return payload


def _write_json_file(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def validate_week_ui_config(data: dict) -> dict:
    if not isinstance(data, dict):
        raise ValueError("week-ui config must be a JSON object")
    if not isinstance(data.get("presets"), dict) or not data["presets"]:
        raise ValueError("week-ui config must include a non-empty presets object")
    default_preset = str(data.get("defaultPreset", "")).strip()
    if default_preset and default_preset not in data["presets"]:
        raise ValueError("defaultPreset must match a preset key")
    return data


def week_ui_version(data: dict) -> str:
    payload = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]


def read_week_ui() -> dict:
    return validate_week_ui_config(_read_json_file(WEEK_UI_JSON))


def write_week_ui(data: dict) -> dict[str, str]:
    normalized = validate_week_ui_config(data)
    _write_json_file(WEEK_UI_JSON, normalized)
    return {"version": week_ui_version(normalized)}


def notion_push_enabled() -> bool:
    return bool(NOTION_TOKEN or MOCK_NOTION_SYNC)


def sync_week_to_notion_safe(week: dict) -> dict:
    if MOCK_NOTION_SYNC:
        mapping = load_notion_mapping()
        week_num = str(week.get("week", ""))
        page_id = mapping.get(week_num) or f"mock-week-{week_num.zfill(2)}"
        return {
            "ok": True,
            "page_id": page_id,
            "blocks_written": len(week_to_notion_blocks(week)),
            "mock": True,
        }
    return sync_week_to_notion(week)


def audit_event(action: str, *, ok: bool, detail: str = "", request: BaseHTTPRequestHandler | None = None) -> None:
    record = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "action": action,
        "ok": ok,
        "detail": detail,
    }
    if request is not None:
        record["path"] = getattr(request, "path", "")
        record["client"] = request.client_address[0] if request.client_address else ""

    AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")



def _find_lecture_note_path(week_num: int) -> Path | None:
    """Return the lecture note path for a week if it exists."""
    matches = sorted(WEEKS_DIR.glob(f"week{week_num:02d}-*/lecture-note.md"))
    return matches[0] if matches else None


def _render_link_list(items: list[dict]) -> list[str]:
    lines: list[str] = []
    for item in items or []:
        title = str(item.get("title", "")).strip()
        url = str(item.get("url", "")).strip()
        if title and url:
            lines.append(f"- [{title}]({url})")
    return lines


def _render_curriculum_sync_markdown(week: dict) -> str:
    """Render the managed lecture-note summary block for a curriculum week."""
    lines = [
        "## 커리큘럼 연동 요약",
        "",
        "> 이 섹션은 `course-site/data/curriculum.js` 기준으로 자동 갱신됩니다.",
        "",
    ]

    meta = []
    subtitle = str(week.get("subtitle", "")).strip()
    duration = str(week.get("duration", "")).strip()
    if subtitle:
        meta.append(f"- 핵심 키워드: {subtitle}")
    if duration:
        meta.append(f"- 예상 시간: {duration}")
    if meta:
        lines.extend(meta)
        lines.append("")

    steps = week.get("steps", []) or []
    if steps:
        lines.extend(["### 실습 단계", ""])
        for idx, step in enumerate(steps, start=1):
            title = str(step.get("title", "")).strip() or f"Step {idx}"
            copy = str(step.get("copy", "")).strip()
            lines.append(f"#### {idx}. {title}")
            lines.append("")
            if copy:
                lines.append(copy)
                lines.append("")

            image_path = str(step.get("image", "")).strip()
            if image_path:
                note_image_path = f"../../course-site/{image_path.lstrip('/')}"
                lines.append(f"![{title}]({note_image_path})")
                lines.append("")

            goals = [str(goal).strip() for goal in step.get("goal", []) if str(goal).strip()]
            if goals:
                lines.append("배울 것")
                lines.append("")
                lines.extend(f"- {goal}" for goal in goals)
                lines.append("")

            tasks = step.get("tasks", []) or []
            if tasks:
                lines.append("체크해볼 것")
                lines.append("")
                for task in tasks:
                    label = str(task.get("label", "")).strip()
                    detail = str(task.get("detail", "")).strip()
                    if not label:
                        continue
                    task_line = f"- {label}"
                    if detail:
                        task_line += f" ({detail})"
                    lines.append(task_line)
                lines.append("")

    shortcuts = week.get("shortcuts", []) or []
    if shortcuts:
        lines.extend(["### 핵심 단축키", ""])
        for shortcut in shortcuts:
            keys = str(shortcut.get("keys", "")).strip()
            action = str(shortcut.get("action", "")).strip()
            if keys and action:
                lines.append(f"- `{keys}`: {action}")
        lines.append("")

    assignment = week.get("assignment", {}) or {}
    assignment_title = str(assignment.get("title", "")).strip()
    assignment_description = str(assignment.get("description", "")).strip()
    assignment_checklist = [
        str(item).strip() for item in assignment.get("checklist", []) if str(item).strip()
    ]
    if assignment_title or assignment_description or assignment_checklist:
        lines.extend(["### 과제 한눈에 보기", ""])
        if assignment_title:
            lines.append(f"- 과제명: {assignment_title}")
        if assignment_description:
            lines.append(f"- 설명: {assignment_description}")
        if assignment_checklist:
            lines.append("- 제출 체크:")
            lines.extend(f"  - {item}" for item in assignment_checklist)
        lines.append("")

    mistakes = [str(item).strip() for item in week.get("mistakes", []) if str(item).strip()]
    if mistakes:
        lines.extend(["### 자주 막히는 지점", ""])
        lines.extend(f"- {item}" for item in mistakes)
        lines.append("")

    videos = _render_link_list(week.get("videos", []))
    if videos:
        lines.extend(["### 공식 영상 튜토리얼", ""])
        lines.extend(videos)
        lines.append("")

    docs = _render_link_list(week.get("docs", []))
    if docs:
        lines.extend(["### 공식 문서", ""])
        lines.extend(docs)
        lines.append("")

    while lines and lines[-1] == "":
        lines.pop()

    return "\n".join(lines)


def _upsert_lecture_sync_block(text: str, block_markdown: str) -> str:
    """Insert or replace the managed lecture-note sync block."""
    managed_block = f"{LECTURE_SYNC_START}\n{block_markdown}\n{LECTURE_SYNC_END}"

    if LECTURE_SYNC_START in text and LECTURE_SYNC_END in text:
        pattern = re.compile(
            rf"{re.escape(LECTURE_SYNC_START)}.*?{re.escape(LECTURE_SYNC_END)}",
            re.DOTALL,
        )
        return pattern.sub(managed_block, text, count=1)

    reference_match = re.search(r"^##\s+.*참고\s*자료.*$", text, re.MULTILINE)
    if reference_match:
        insert_at = reference_match.start()
        prefix = text[:insert_at].rstrip()
        suffix = text[insert_at:].lstrip("\n")
        return f"{prefix}\n\n{managed_block}\n\n{suffix}"

    return text.rstrip() + f"\n\n{managed_block}\n"


def _strip_duplicate_official_reference_sections(text: str) -> str:
    """Remove manual official resource subsections once the managed block exists."""
    reference_match = re.search(r"^##\s+.*참고\s*자료.*$", text, re.MULTILINE)
    if not reference_match:
        return text

    next_section_match = re.search(r"^##\s+", text[reference_match.end() :], re.MULTILINE)
    section_start = reference_match.start()
    section_end = (
        reference_match.end() + next_section_match.start()
        if next_section_match
        else len(text)
    )
    section = text[section_start:section_end]

    for heading in ("공식 영상 튜토리얼", "공식 문서"):
        section = re.sub(
            rf"\n?^###\s+{heading}\s*$.*?(?=^###\s+|^##\s+|\Z)",
            "",
            section,
            flags=re.MULTILINE | re.DOTALL,
        )

    section = re.sub(r"\n{3,}", "\n\n", section).rstrip() + "\n"

    if re.fullmatch(r"##\s+.*참고\s*자료.*\n?", section.strip()):
        return (text[:section_start].rstrip() + "\n") + text[section_end:].lstrip("\n")

    return text[:section_start] + section + text[section_end:]


def sync_lecture_notes(data: list[dict]) -> list[Path]:
    """Sync managed curriculum summary blocks into lecture-note files."""
    updated_paths: list[Path] = []

    for week in data:
        week_num = int(week.get("week", 0) or 0)
        if week_num <= 0:
            continue

        lecture_path = _find_lecture_note_path(week_num)
        if not lecture_path or not lecture_path.exists():
            continue

        original = lecture_path.read_text(encoding="utf-8")
        block_markdown = _render_curriculum_sync_markdown(week)
        updated = _upsert_lecture_sync_block(original, block_markdown)
        updated = _strip_duplicate_official_reference_sections(updated)
        if updated != original:
            lecture_path.write_text(updated, encoding="utf-8")
            updated_paths.append(lecture_path)

    return updated_paths


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

    def _send_json(self, data: dict | list, status: int = 200) -> None:
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "same-origin")
        self.end_headers()
        self.wfile.write(body)

    def _send_error_json(self, status: int, message: str) -> None:
        self._send_json({"ok": False, "error": message}, status)

    def _read_body(self) -> bytes:
        length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(length) if length > 0 else b""

    def _load_session(self) -> dict[str, float] | None:
        raw_cookie = self.headers.get("Cookie", "")
        if not raw_cookie:
            return None

        jar = cookies.SimpleCookie()
        jar.load(raw_cookie)
        morsel = jar.get(SESSION_COOKIE_NAME)
        if morsel is None:
            return None

        token = morsel.value
        session = ADMIN_SESSIONS.get(token)
        if session is None:
            return None

        expires_at = session.get("expires_at", 0.0)
        now = time.time()
        if now >= expires_at:
            ADMIN_SESSIONS.pop(token, None)
            return None

        session["expires_at"] = now + SESSION_TTL_SECONDS
        return session

    def _set_session_cookie(self, token: str, *, max_age: int = SESSION_TTL_SECONDS) -> None:
        cookie = cookies.SimpleCookie()
        cookie[SESSION_COOKIE_NAME] = token
        cookie[SESSION_COOKIE_NAME]["path"] = "/"
        cookie[SESSION_COOKIE_NAME]["httponly"] = True
        cookie[SESSION_COOKIE_NAME]["samesite"] = "Strict"
        cookie[SESSION_COOKIE_NAME]["max-age"] = str(max_age)
        self.send_header("Set-Cookie", cookie.output(header="").strip())

    def _clear_session_cookie(self) -> None:
        cookie = cookies.SimpleCookie()
        cookie[SESSION_COOKIE_NAME] = ""
        cookie[SESSION_COOKIE_NAME]["path"] = "/"
        cookie[SESSION_COOKIE_NAME]["httponly"] = True
        cookie[SESSION_COOKIE_NAME]["samesite"] = "Strict"
        cookie[SESSION_COOKIE_NAME]["expires"] = "Thu, 01 Jan 1970 00:00:00 GMT"
        cookie[SESSION_COOKIE_NAME]["max-age"] = "0"
        self.send_header("Set-Cookie", cookie.output(header="").strip())

    def _check_auth(self) -> bool:
        """Return True if a valid admin session exists."""
        session = self._load_session()
        if session is not None:
            return True
        self._send_error_json(401, "Unauthorized")
        return False

    def _require_admin_key(self) -> bool:
        if ADMIN_KEY:
            return True
        self._send_error_json(503, "ADMIN_KEY not configured")
        return False

    def _route_path(self) -> str:
        """Decoded, normalised request path."""
        return unquote(self.path).split("?", 1)[0]

    def _enforce_same_origin(self) -> bool:
        """Reject cross-origin write requests when an Origin header is present."""
        origin = self.headers.get("Origin", "").strip()
        if not origin:
            return True

        try:
            origin_netloc = urlparse(origin).netloc
        except ValueError:
            self._send_error_json(403, "Invalid Origin header")
            return False

        host = self.headers.get("Host", "").strip()
        if not origin_netloc or not host or origin_netloc != host:
            self._send_error_json(403, "Cross-origin write requests are not allowed")
            return False
        return True

    # -- verbs -------------------------------------------------------------

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Allow", "GET, POST, PUT, OPTIONS")
        self.end_headers()

    def do_GET(self) -> None:
        path = self._route_path()

        if path == "/api/admin/session":
            if self._load_session():
                self._send_json({"ok": True, "authenticated": True})
            else:
                self._send_json({"ok": True, "authenticated": False}, status=401)
            return

        # API: GET /api/curriculum
        if path == "/api/curriculum":
            if not self._check_auth():
                return
            try:
                data = read_curriculum()
                self._send_json({"data": data, "version": content_version(data)})
            except Exception as exc:
                audit_event("curriculum.read", ok=False, detail=str(exc), request=self)
                self._send_error_json(500, str(exc))
            return

        if path == "/api/week-ui":
            if not self._check_auth():
                return
            try:
                data = read_week_ui()
                self._send_json({"data": data, "version": week_ui_version(data)})
            except Exception as exc:
                audit_event("week-ui.read", ok=False, detail=str(exc), request=self)
                self._send_error_json(500, str(exc))
            return

        # API: GET /api/notion-status
        if path == "/api/notion-status":
            if not self._check_auth():
                return
            mapping = load_notion_mapping()
            self._send_json({
                "configured": notion_push_enabled(),
                "mapping_loaded": bool(mapping),
                "weeks_mapped": len(mapping),
                "mock": MOCK_NOTION_SYNC,
            })
            return

        # --- Grading API ---
        if path == "/api/submissions":
            if not self._check_auth():
                return
            params = dict(parse_qs(urlparse(self.path).query))
            class_num = params.get("class", [None])[0]
            week = params.get("week", [None])[0]
            try:
                data = query_submissions(class_num=class_num, week=week)
                self._send_json(data)
            except RuntimeError as e:
                self._send_error_json(500, str(e))
            return

        if path == "/api/grades":
            if not self._check_auth():
                return
            params = dict(parse_qs(urlparse(self.path).query))
            class_num = params.get("class", [None])[0]
            try:
                data = query_grades(class_num=class_num)
                self._send_json(data)
            except RuntimeError as e:
                self._send_error_json(500, str(e))
            return

        # Static files
        self._serve_static(path)

    def do_PUT(self) -> None:
        if not self._enforce_same_origin():
            return
        if not self._check_auth():
            return

        path = self._route_path()

        # PUT /api/curriculum
        if path == "/api/curriculum":
            self._handle_put_curriculum()
            return

        if path == "/api/week-ui":
            self._handle_put_week_ui()
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

        if not self._enforce_same_origin():
            return

        if path == "/api/admin/login":
            self._handle_admin_login()
            return

        if path == "/api/admin/logout":
            self._handle_admin_logout()
            return

        # POST /api/notion-quiz — disabled until authenticated student sync exists
        if path == "/api/notion-quiz":
            self._send_error_json(410, "Quiz server sync is disabled")
            return

        # All other POST endpoints require auth
        if not self._check_auth():
            return

        if path == "/api/curriculum/diff":
            self._handle_curriculum_diff()
            return

        # POST /api/upload/{weekNum}/{stepIdx}
        upload_match = re.match(r"^/api/upload/(\d+)/(\d+)$", path)
        if upload_match:
            week_num = int(upload_match.group(1))
            step_idx = int(upload_match.group(2))
            self._handle_upload(week_num, step_idx)
            return

        # POST /api/upload-video/{weekNum}/{videoIdx}
        video_upload_match = re.match(r"^/api/upload-video/(\d+)/(\d+)$", path)
        if video_upload_match:
            week_num = int(video_upload_match.group(1))
            video_idx = int(video_upload_match.group(2))
            self._handle_video_upload(week_num, video_idx)
            return

        # POST /api/notion-push/{weekNum}
        notion_push_match = re.match(r"^/api/notion-push/(\d+)$", path)
        if notion_push_match:
            week_num = int(notion_push_match.group(1))
            self._handle_notion_push(week_num)
            return

        # POST /api/notion-push-all
        if path == "/api/notion-push-all":
            self._handle_notion_push_all()
            return

        self._send_error_json(404, "Not found")

    # -- API handlers ------------------------------------------------------

    def _handle_admin_login(self) -> None:
        if not self._require_admin_key():
            return

        body = self._read_body()
        try:
            payload = json.loads(body or b"{}")
        except json.JSONDecodeError as exc:
            self._send_error_json(400, f"Invalid JSON: {exc}")
            return

        password = str(payload.get("password", "")).strip()
        if password != ADMIN_KEY:
            audit_event("auth.login", ok=False, detail="invalid password", request=self)
            self._send_error_json(401, "Invalid credentials")
            return

        token = secrets.token_urlsafe(32)
        ADMIN_SESSIONS[token] = {
            "issued_at": time.time(),
            "expires_at": time.time() + SESSION_TTL_SECONDS,
        }

        self.send_response(200)
        self._set_session_cookie(token)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        body_bytes = json.dumps({"ok": True}, ensure_ascii=False).encode("utf-8")
        self.send_header("Content-Length", str(len(body_bytes)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body_bytes)
        audit_event("auth.login", ok=True, detail="session created", request=self)

    def _handle_admin_logout(self) -> None:
        session_cookie = self.headers.get("Cookie", "")
        if session_cookie:
            jar = cookies.SimpleCookie()
            jar.load(session_cookie)
            morsel = jar.get(SESSION_COOKIE_NAME)
            if morsel is not None:
                ADMIN_SESSIONS.pop(morsel.value, None)

        self.send_response(200)
        self._clear_session_cookie()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        body_bytes = json.dumps({"ok": True}, ensure_ascii=False).encode("utf-8")
        self.send_header("Content-Length", str(len(body_bytes)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body_bytes)
        audit_event("auth.logout", ok=True, detail="session cleared", request=self)

    def _handle_curriculum_diff(self) -> None:
        body = self._read_body()
        try:
            candidate = json.loads(body)
        except json.JSONDecodeError as exc:
            self._send_error_json(400, f"Invalid JSON: {exc}")
            return

        try:
            current = read_curriculum()
            diff = compute_curriculum_diff(current, candidate)
        except Exception as exc:
            self._send_error_json(400, str(exc))
            return

        self._send_json({"ok": True, "diff": diff})

    def _handle_put_curriculum(self) -> None:
        """Handle full curriculum save through the canonical pipeline."""
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
            result = write_curriculum(data)
        except Exception as exc:
            audit_event("curriculum.write", ok=False, detail=str(exc), request=self)
            self._send_error_json(400, str(exc))
            return

        audit_event(
            "curriculum.write",
            ok=True,
            detail=f"version={result['version']} weeks={result['weeks']}",
            request=self,
        )
        self._send_json({"ok": True, "version": result["version"]})

    def _handle_put_week_ui(self) -> None:
        body = self._read_body()
        try:
            data = json.loads(body)
        except json.JSONDecodeError as exc:
            self._send_error_json(400, f"Invalid JSON: {exc}")
            return

        if not isinstance(data, dict):
            self._send_error_json(400, "Body must be a JSON object")
            return

        try:
            result = write_week_ui(data)
        except Exception as exc:
            audit_event("week-ui.write", ok=False, detail=str(exc), request=self)
            self._send_error_json(400, str(exc))
            return

        audit_event("week-ui.write", ok=True, detail=f"version={result['version']}", request=self)
        self._send_json({"ok": True, "version": result["version"]})

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

        curriculum = read_curriculum()
        for week in curriculum:
            if week.get("week") == week_num:
                week["status"] = new_status
                break
        result = write_curriculum(curriculum)
        audit_event(
            "curriculum.status",
            ok=True,
            detail=f"week={week_num} status={new_status} version={result['version']}",
            request=self,
        )
        self._send_json(
            {"ok": True, "week": week_num, "status": new_status, "version": result["version"]}
        )

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

        # Save image path directly to curriculum.js
        curriculum = read_curriculum()
        for week in curriculum:
            if week.get("week") == week_num:
                steps = week.get("steps", [])
                if step_idx < len(steps):
                    steps[step_idx]["image"] = relative_path
                break
        result = write_curriculum(curriculum)
        audit_event(
            "asset.upload.image",
            ok=True,
            detail=f"week={week_num} step={step_idx} path={relative_path} version={result['version']}",
            request=self,
        )
        self._send_json({"ok": True, "path": relative_path, "version": result["version"]})

    def _handle_video_upload(self, week_num: int, video_idx: int) -> None:
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

        if "video" not in fields:
            self._send_error_json(400, 'No field named "video" found')
            return

        filename, file_data = fields["video"]
        if not filename:
            self._send_error_json(400, "No filename provided")
            return

        ext = os.path.splitext(filename)[1].lower()
        if not ext:
            ext = ".mp4"

        allowed_ext = {".mp4", ".webm", ".mov", ".ogg", ".avi"}
        if ext not in allowed_ext:
            self._send_error_json(
                400, f"Unsupported video type: {ext}. Allowed: {sorted(allowed_ext)}"
            )
            return

        # Validate curriculum state
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

        videos = week_entry.get("videos", [])
        if video_idx < 0 or video_idx >= len(videos):
            self._send_error_json(
                400,
                f"Video index {video_idx} out of range (week {week_num} has {len(videos)} videos)",
            )
            return

        # Build destination path and write file
        week_dir = VIDEOS_DIR / f"week-{week_num:02d}"
        week_dir.mkdir(parents=True, exist_ok=True)
        dest_filename = f"video-{video_idx}{ext}"
        dest_path = week_dir / dest_filename
        dest_path.write_bytes(file_data)

        # Relative path from course-site/ root
        relative_path = f"assets/videos/week-{week_num:02d}/{dest_filename}"

        # Save video URL directly to curriculum.js
        curriculum = read_curriculum()
        for week in curriculum:
            if week.get("week") == week_num:
                week_videos = week.get("videos", [])
                if video_idx < len(week_videos):
                    week_videos[video_idx]["url"] = relative_path
                break
        result = write_curriculum(curriculum)
        audit_event(
            "asset.upload.video",
            ok=True,
            detail=f"week={week_num} video={video_idx} path={relative_path} version={result['version']}",
            request=self,
        )
        self._send_json({"ok": True, "path": relative_path, "version": result["version"]})

    def _handle_notion_push(self, week_num: int) -> None:
        """Push curriculum week data to Notion."""
        if not notion_push_enabled():
            audit_event("notion.push", ok=False, detail="notion sync unavailable", request=self)
            self._send_error_json(503, "NOTION_TOKEN not configured")
            return

        try:
            data = read_curriculum()
        except Exception as exc:
            audit_event("notion.push", ok=False, detail=f"read failed: {exc}", request=self)
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
            result = sync_week_to_notion_safe(week)
            result["version"] = content_version([week])
            audit_event(
                "notion.push",
                ok=True,
                detail=f"week={week_num} version={result['version']}",
                request=self,
            )
            self._send_json(result)
        except Exception as exc:
            audit_event("notion.push", ok=False, detail=str(exc), request=self)
            self._send_error_json(500, f"Notion sync failed: {exc}")

    def _handle_notion_push_all(self) -> None:
        """Push all curriculum weeks to Notion."""
        if not notion_push_enabled():
            audit_event("notion.push_all", ok=False, detail="notion sync unavailable", request=self)
            self._send_error_json(503, "NOTION_TOKEN not configured")
            return

        try:
            data = read_curriculum()
        except Exception as exc:
            audit_event("notion.push_all", ok=False, detail=f"read failed: {exc}", request=self)
            self._send_error_json(500, f"Read failed: {exc}")
            return

        try:
            mapping = load_notion_mapping()
        except Exception as exc:
            audit_event("notion.push_all", ok=False, detail=f"mapping failed: {exc}", request=self)
            self._send_error_json(500, f"Mapping load failed: {exc}")
            return
        results = []
        for week in data:
            week_num = week.get("week")
            if str(week_num) not in mapping:
                results.append({
                    "week": week_num,
                    "ok": False,
                    "error": "no mapping",
                    "title": week.get("title", ""),
                })
                continue
            try:
                sync_week_to_notion_safe(week)
                results.append({"week": week_num, "ok": True, "title": week.get("title", "")})
            except Exception as exc:
                results.append({
                    "week": week_num,
                    "ok": False,
                    "error": str(exc),
                    "title": week.get("title", ""),
                })

        success_count = sum(1 for r in results if r["ok"])
        audit_event(
            "notion.push_all",
            ok=success_count == len(results),
            detail=f"success={success_count}/{len(results)} version={content_version(data)}",
            request=self,
        )
        self._send_json(
            {
                "results": results,
                "success_count": success_count,
                "total": len(results),
                "version": content_version(data),
            }
        )

    # -- static file serving -----------------------------------------------

    def _serve_static(self, path: str) -> None:
        # Default: / or /admin -> admin.html
        if path in ("/", "", "/admin"):
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
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "same-origin")
        if requested.name == "admin.html":
            self.send_header("Cache-Control", "no-store")
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
        "--host",
        default=os.environ.get("HOST", "127.0.0.1"),
        help="Bind host (default: 127.0.0.1 or HOST env var)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("PORT", "8765")),
        help="Port to listen on (default: 8765 or PORT env var)",
    )
    args = parser.parse_args()

    if not ADMIN_KEY:
        print("ERROR: ADMIN_KEY environment variable is required", file=sys.stderr)
        sys.exit(1)

    try:
        entries = read_curriculum()
        week_count = len(entries)
        version = content_version(entries)
    except Exception as exc:
        print(f"ERROR: Failed to parse canonical curriculum: {exc}", file=sys.stderr)
        sys.exit(1)

    auth_mode = "COOKIE SESSION"
    notion_mode = "MOCK" if MOCK_NOTION_SYNC else ("ENABLED" if NOTION_TOKEN else "DISABLED (set NOTION_TOKEN)")
    notion_weeks = len(load_notion_mapping())

    HTTPServer.allow_reuse_address = True
    server = HTTPServer((args.host, args.port), AdminHandler)

    print("=" * 60)
    print("  RPD Admin Server")
    print("=" * 60)
    print(f"  URL:        http://{args.host}:{args.port}/")
    print(f"  Static:     {COURSE_SITE}")
    try:
        curriculum_path = CANONICAL_JSON.relative_to(ROOT)
    except Exception:
        curriculum_path = CANONICAL_JSON
    print(f"  Curriculum: {curriculum_path} ({week_count} weeks, version {version})")
    print(f"  Auth:       {auth_mode}")
    print(f"  Notion:     {notion_mode} ({notion_weeks} weeks mapped)")
    print(f"  Audit log:  {AUDIT_LOG_PATH}")
    print("=" * 60)
    print()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.server_close()


if __name__ == "__main__":
    main()
