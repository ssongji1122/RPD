"""
remove_time_refs.py
===================
Notion 강의자료에서 시간 명시 내용을 탐지하고 삭제하는 스크립트.

탐지 패턴:
  - X분, 약 X분
  - X:XX (시간 형식)
  - 총 Xmin
  - 시간 배분
  - Step X — XX분
  - 시간 관련 헤딩/셀

Usage:
    cd /Users/ssongji/Developer/Workspace/RPD
    NOTION_TOKEN=... python tools/remove_time_refs.py [--weeks 1,2,3] [--archive] [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# Path setup
# ─────────────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "site" / "_scripts"))

# Load .env if NOTION_TOKEN not set
if not os.environ.get("NOTION_TOKEN"):
    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())

from notion_api import (  # noqa: E402
    _get_page_blocks,
    get_page_blocks_recursive,
    extract_text,
    notion_request,
    load_notion_mapping,
)

# ─────────────────────────────────────────────────────────────────────────────
# Time-pattern detection
# ─────────────────────────────────────────────────────────────────────────────
TIME_PATTERNS = [
    r"\d+\s*분",           # X분, 15 분
    r"약\s*\d+\s*분",      # 약 15분
    r"\d+:\d{2}",          # X:XX
    r"총\s*\d+\s*min",     # 총 30min
    r"시간\s*배분",         # 시간 배분
    r"Step\s*\d+\s*[—-]+\s*\d+\s*분",  # Step X — XX분
    r"\d+\s*min",          # 30min
    r"소요\s*시간",         # 소요 시간
    r"수업\s*시간",         # 수업 시간
    r"\(\d+분\)",           # (15분)
    r"\[\d+분\]",           # [15분]
]

_TIME_RE = re.compile("|".join(TIME_PATTERNS), re.IGNORECASE)

# Heading text that is entirely about time
_TIME_HEADING_RE = re.compile(
    r"^(시간\s*배분|소요\s*시간|수업\s*시간|시간표|타임라인)$",
    re.IGNORECASE,
)

# Patterns that are NOT class time allocations — skip these blocks entirely
_SKIP_PATTERNS = re.compile(
    r"수업\s*시간에\s*(진행|발표|최소|참석)"  # "수업 시간에 진행/발표" = contextual, not allocation
    r"|수업\s*시간에\s*\d+명"               # "수업 시간에 3명" = contextual
    r"|minute[s]?"                          # English "minute(s)" = AI prompts, durations
    r"|이라도\s*진지"                        # "10분이라도 진지하게" = colloquial
    r"|대기",                               # "(1~5분 대기)" = wait time, not class allocation
    re.IGNORECASE,
)

# Clean trailing (XX분) patterns from heading text
_TRAILING_PAREN_TIME_RE = re.compile(r"\s*\([^)]*\d+[^)]*분[^)]*\)\s*$")
_TRAILING_TILDE_TIME_RE = re.compile(r"\s*~\d+분\s*$")


def has_time_ref(text: str) -> bool:
    """Return True if text contains any time reference pattern."""
    return bool(_TIME_RE.search(text))


def should_skip(text: str, btype: str) -> bool:
    """Return True if this block should be skipped despite having a time pattern."""
    if btype == "code":
        return True  # Code blocks are AI prompts / technical content
    if _SKIP_PATTERNS.search(text):
        return True
    return False


def is_time_only_heading(text: str) -> bool:
    """Return True if the heading is exclusively about time."""
    return bool(_TIME_HEADING_RE.match(text.strip()))


# ─────────────────────────────────────────────────────────────────────────────
# Block-level text extraction (handles all block types)
# ─────────────────────────────────────────────────────────────────────────────
_RICH_TEXT_KEYS = [
    "rich_text", "title", "text", "caption",
]

_BLOCK_TYPES_WITH_RICH_TEXT = {
    "paragraph", "heading_1", "heading_2", "heading_3",
    "bulleted_list_item", "numbered_list_item", "to_do",
    "toggle", "quote", "callout", "code",
}


def block_plain_text(block: dict) -> str:
    """Extract all plain text from any block type."""
    btype = block.get("type", "")
    content = block.get(btype, {})
    if not isinstance(content, dict):
        return ""

    for key in _RICH_TEXT_KEYS:
        rt = content.get(key)
        if rt and isinstance(rt, list):
            return extract_text(rt)

    # Table row: check all cells
    if btype == "table_row":
        cells = content.get("cells", [])
        return " ".join(extract_text(cell) for cell in cells)

    return ""


# ─────────────────────────────────────────────────────────────────────────────
# Edit helpers: strip time refs from rich_text
# ─────────────────────────────────────────────────────────────────────────────
def clean_text_content(content: str) -> str:
    """Remove time allocation patterns from a text string, cleaning up artifacts."""
    # Remove trailing (XX분) parenthetical time markers — most common in headings
    content = _TRAILING_PAREN_TIME_RE.sub("", content)
    content = _TRAILING_TILDE_TIME_RE.sub("", content)
    # Remove inline time patterns
    content = _TIME_RE.sub("", content)
    # Clean up artifacts: orphan parentheses, extra spaces, trailing dashes
    content = re.sub(r"\(\s*\)", "", content)       # ()
    content = re.sub(r"\s{2,}", " ", content)       # multiple spaces
    content = re.sub(r"\s*[—–-]\s*$", "", content)  # trailing dash
    content = re.sub(r"^\s*[—–-]\s*", "", content)  # leading dash
    return content.strip()


def clean_rich_text(rich_text_list: list) -> list:
    """Return a new rich_text list with time patterns removed from each item."""
    result = []
    for rt in rich_text_list:
        plain = rt.get("plain_text", "")
        if not has_time_ref(plain):
            result.append(rt)
            continue
        # Remove time refs from the text content
        raw_content = rt.get("text", {}).get("content", "")
        new_content = clean_text_content(raw_content)
        if not new_content:
            continue  # omit the whole segment
        new_rt = dict(rt)
        new_rt["text"] = {**rt.get("text", {}), "content": new_content}
        new_rt["plain_text"] = new_content
        result.append(new_rt)
    return result


# ─────────────────────────────────────────────────────────────────────────────
# Core processing
# ─────────────────────────────────────────────────────────────────────────────
def process_page(
    page_id: str,
    label: str,
    dry_run: bool = False,
) -> list[dict]:
    """
    Scan all blocks in a Notion page and remove time references.

    Returns a list of action dicts for reporting:
        {"action": "delete"|"edit", "block_id": ..., "text": ..., "result": "ok"|"dry-run"}
    """
    token = os.environ.get("NOTION_TOKEN")
    for attempt in range(3):
        try:
            blocks = get_page_blocks_recursive(page_id, token=token)
            break
        except urllib.error.HTTPError as e:
            if e.code in (429, 502, 503) and attempt < 2:
                wait = (attempt + 1) * 5
                print(f"  HTTP {e.code} — retrying in {wait}s...")
                time.sleep(wait)
            else:
                print(f"  ERROR fetching blocks: HTTP {e.code} — skipping page")
                return []
        except Exception as e:
            print(f"  ERROR fetching blocks: {e} — skipping page")
            return []

    actions = []
    # Track which parent IDs contain time-headings so we can skip their children
    skip_children_of: set[str] = set()

    for block in blocks:
        bid = block["id"]
        btype = block.get("type", "")
        text = block_plain_text(block)
        parent_id = block.get("parent", {}).get("block_id") or block.get("parent", {}).get("page_id")

        # Skip children of already-deleted time-heading blocks
        if parent_id in skip_children_of:
            skip_children_of.add(bid)
            continue

        if not text:
            continue

        # Skip blocks that match known false-positive patterns
        if should_skip(text, btype):
            continue

        action = None

        # Heading that is entirely about time → delete block + children
        if btype in ("heading_1", "heading_2", "heading_3", "heading_4"):
            if is_time_only_heading(text):
                action = "delete"
                skip_children_of.add(bid)

        # Any block whose text contains time refs
        if action is None and has_time_ref(text):
            # Table row: delete the entire row if it's primarily time data
            if btype == "table_row":
                action = "delete"
            # Blocks where text is almost entirely a time reference → delete
            elif _TIME_RE.sub("", text).strip() in ("", ":", "–", "—", "-", "·", "•"):
                action = "delete"
            # Otherwise: edit the rich text to strip time parts
            else:
                action = "edit"

        if action is None:
            continue

        result_status = "dry-run" if dry_run else "pending"
        entry = {"action": action, "block_id": bid, "text": text, "result": result_status, "label": label}
        actions.append(entry)

        if dry_run:
            print(f"  [DRY-RUN] {action.upper()} | {btype} | {text[:80]!r}")
            continue

        try:
            if action == "delete":
                notion_request("DELETE", f"/blocks/{bid}", token=token)
                entry["result"] = "deleted"
                print(f"  DELETED  | {btype} | {text[:80]!r}")

            elif action == "edit":
                # Fetch current block to get latest rich_text
                current = notion_request("GET", f"/blocks/{bid}", token=token)
                bdata = current.get(btype, {})
                new_rich_text = None
                for key in _RICH_TEXT_KEYS:
                    rt = bdata.get(key)
                    if rt and isinstance(rt, list):
                        new_rich_text = clean_rich_text(rt)
                        patch_key = key
                        break
                if new_rich_text is None:
                    entry["result"] = "skip-no-richtext"
                    continue
                if not new_rich_text:
                    # All content removed → delete the block
                    notion_request("DELETE", f"/blocks/{bid}", token=token)
                    entry["result"] = "deleted-empty"
                    print(f"  DELETED(empty) | {btype} | {text[:80]!r}")
                else:
                    notion_request("PATCH", f"/blocks/{bid}", {btype: {patch_key: new_rich_text}}, token=token)
                    entry["result"] = "edited"
                    new_text = extract_text(new_rich_text)
                    print(f"  EDITED   | {btype} | {text[:60]!r} → {new_text[:60]!r}")

        except Exception as e:
            entry["result"] = f"error: {e}"
            print(f"  ERROR    | {btype} | {text[:60]!r} → {e}")

    return actions


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────
ARCHIVE_PAGE_ID = "66c54d654971826496f801ab48dce4c8"


def main() -> None:
    parser = argparse.ArgumentParser(description="Remove time references from Notion pages")
    parser.add_argument("--weeks", default="1,2,3,4,5,6", help="Comma-separated week numbers (default: 1-6)")
    parser.add_argument("--all-weeks", action="store_true", help="Process all 15 weeks")
    parser.add_argument("--archive", action="store_true", default=True, help="Also process archive page (default: on)")
    parser.add_argument("--no-archive", dest="archive", action="store_false")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be changed without modifying Notion")
    args = parser.parse_args()

    if not os.environ.get("NOTION_TOKEN"):
        print("ERROR: NOTION_TOKEN not set", file=sys.stderr)
        sys.exit(1)

    mapping = load_notion_mapping()
    week_nums = list(range(1, 16)) if args.all_weeks else [int(w) for w in args.weeks.split(",") if w.strip()]

    all_actions = []

    print(f"\n{'='*60}")
    print(f"  Mode: {'DRY-RUN' if args.dry_run else 'LIVE'}")
    print(f"  Weeks: {week_nums}")
    print(f"  Archive: {args.archive}")
    print(f"{'='*60}\n")

    for week_num in week_nums:
        page_id = mapping.get(str(week_num))
        if not page_id:
            print(f"Week {week_num}: No page ID found, skipping.")
            continue
        print(f"\n── Week {week_num} (page: {page_id}) ──")
        actions = process_page(page_id, label=f"Week {week_num}", dry_run=args.dry_run)
        all_actions.extend(actions)
        print(f"   → {len(actions)} block(s) affected")

    if args.archive:
        print(f"\n── Archive page ({ARCHIVE_PAGE_ID}) ──")
        actions = process_page(ARCHIVE_PAGE_ID, label="Archive", dry_run=args.dry_run)
        all_actions.extend(actions)
        print(f"   → {len(actions)} block(s) affected")

    # Summary
    print(f"\n{'='*60}")
    print(f"  Total blocks affected: {len(all_actions)}")
    deleted = [a for a in all_actions if "deleted" in a.get("result", "")]
    edited = [a for a in all_actions if "edited" in a.get("result", "")]
    dry = [a for a in all_actions if a.get("result") == "dry-run"]
    print(f"  Deleted: {len(deleted)}")
    print(f"  Edited: {len(edited)}")
    if dry:
        print(f"  Would-change (dry-run): {len(dry)}")
    print(f"{'='*60}\n")

    # Output JSON report
    report_path = ROOT / ".tmp" / "remove_time_refs_report.json"
    report_path.parent.mkdir(exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(all_actions, f, ensure_ascii=False, indent=2)
    print(f"Report saved to: {report_path}")


if __name__ == "__main__":
    main()
