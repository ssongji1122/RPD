"""
showme_build.py — Notion Card DB → ShowMe HTML generator
========================================================
Fetches cards from Notion, renders HTML, regenerates registry + catalog.

Usage:
    python3 tools/showme_build.py --card <card_id>     # single card
    python3 tools/showme_build.py --week <N>           # all cards for week N
    python3 tools/showme_build.py --all                # everything (use in CI)
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from notion_api import NOTION_API, get_notion_token  # noqa: E402

from showme_lib.index import build_catalog_json, build_registry_js  # noqa: E402
from showme_lib.notion_cards import normalize_card_page  # noqa: E402
from showme_lib.renderer import render_card_html  # noqa: E402
from showme_lib.types import Video  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = ROOT / "course-site" / "assets" / "showme" / "_template.v2.html"
OUTPUT_DIR = ROOT / "course-site" / "assets" / "showme"
REGISTRY_PATH = OUTPUT_DIR / "_registry.js"
CATALOG_PATH = OUTPUT_DIR / "_catalog.json"
DB_IDS_PATH = Path(__file__).parent / "showme_db_ids.json"


def _load_db_ids() -> tuple[str, str]:
    if not DB_IDS_PATH.exists():
        raise SystemExit(f"Missing {DB_IDS_PATH}. Run tools/showme_create_dbs.py first.")
    data = json.loads(DB_IDS_PATH.read_text())
    return data["cards_db_id"], data["videos_db_id"]


def _query_db(db_id: str, token: str, filter_obj: dict | None = None) -> list[dict]:
    results: list[dict] = []
    start_cursor: str | None = None
    while True:
        body: dict = {"page_size": 100}
        if filter_obj:
            body["filter"] = filter_obj
        if start_cursor:
            body["start_cursor"] = start_cursor
        req = urllib.request.Request(
            f"{NOTION_API}/databases/{db_id}/query",
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {token}",
                "Notion-Version": "2022-06-28",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(req) as r:
            resp = json.loads(r.read().decode("utf-8"))
        results.extend(resp["results"])
        if not resp.get("has_more"):
            break
        start_cursor = resp.get("next_cursor")
    return results


def _normalize_video_page(page: dict) -> Video:
    props = page["properties"]

    def plain(key: str) -> str:
        return "".join(p.get("plain_text", "") for p in props.get(key, {}).get("rich_text", []))

    title = "".join(p.get("plain_text", "") for p in props.get("title", {}).get("title", []))
    return Video(
        title=title,
        url=props.get("url", {}).get("url") or "",
        channel=plain("channel"),
        duration_sec=int(props.get("duration_sec", {}).get("number") or 0),
        language=(props.get("language", {}).get("select") or {}).get("name") or "en",
        blender_version=plain("blender_version") or "5.0",
        official=bool(props.get("official", {}).get("checkbox")),
        recommended_reason=plain("recommended_reason"),
    )


def fetch_all_cards(token: str, cards_db_id: str, videos_db_id: str):
    video_pages = _query_db(videos_db_id, token)
    videos_by_id = {p["id"]: _normalize_video_page(p) for p in video_pages}
    card_pages = _query_db(cards_db_id, token)
    return [normalize_card_page(p, videos_by_id) for p in card_pages]


def write_card_html(card, template: str) -> Path:
    html_out = render_card_html(card, template)
    out_path = OUTPUT_DIR / f"{card.card_id}.html"
    out_path.write_text(html_out, encoding="utf-8")
    return out_path


def main() -> int:
    p = argparse.ArgumentParser()
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--card", help="Single card_id")
    group.add_argument("--week", type=int, help="All cards for week N")
    group.add_argument("--all", action="store_true", help="All published cards")
    args = p.parse_args()

    cards_db_id, videos_db_id = _load_db_ids()
    token = get_notion_token()
    template = TEMPLATE_PATH.read_text()

    all_cards = fetch_all_cards(token, cards_db_id, videos_db_id)

    if args.card:
        targets = [c for c in all_cards if c.card_id == args.card]
        if not targets:
            print(f"ERROR: card_id {args.card!r} not found")
            return 1
    elif args.week is not None:
        targets = [c for c in all_cards if args.week in c.weeks and c.status != "deprecated"]
    else:
        targets = [c for c in all_cards if c.status != "deprecated"]

    for card in targets:
        path = write_card_html(card, template)
        print(f"  wrote {path.relative_to(ROOT)}")

    REGISTRY_PATH.write_text(build_registry_js(all_cards), encoding="utf-8")
    CATALOG_PATH.write_text(build_catalog_json(all_cards), encoding="utf-8")
    print(f"\nregenerated {REGISTRY_PATH.relative_to(ROOT)}")
    print(f"regenerated {CATALOG_PATH.relative_to(ROOT)}")
    print(f"total: {len(targets)} card(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
