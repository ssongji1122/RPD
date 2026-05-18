"""
showme_create_dbs.py — Bootstrap Notion DBs for ShowMe SSoT
============================================================
ShowMe Cards + ShowMe Videos DB를 부모 페이지 산하에 생성한다.

Usage:
    python3 tools/showme_create_dbs.py --parent <PAGE_ID>

Writes the created DB IDs to tools/showme_db_ids.json (gitignored).
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from notion_api import NOTION_API, get_notion_token

OUTPUT = Path(__file__).parent / "showme_db_ids.json"


def _post(path: str, body: dict, token: str) -> dict:
    req = urllib.request.Request(
        f"{NOTION_API}{path}",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode("utf-8"))


CARDS_SCHEMA = {
    "card_id": {"title": {}},
    "label": {"rich_text": {}},
    "icon": {"rich_text": {}},
    "category": {
        "select": {
            "options": [
                {"name": n}
                for n in [
                    "modeling", "edit-mode", "modifier", "object", "scene",
                    "material", "ai", "sculpt", "animation", "rigging", "render",
                ]
            ]
        }
    },
    "week": {
        "multi_select": {"options": [{"name": str(i)} for i in range(1, 16)]}
    },
    "priority": {"select": {"options": [{"name": p} for p in ["P0", "P1", "P2"]]}},
    "status": {
        "select": {
            "options": [{"name": s} for s in ["planned", "draft", "published", "deprecated"]]
        }
    },
    "concept_md": {"rich_text": {}},
    "usage_md": {"rich_text": {}},
    "pitfall_md": {"rich_text": {}},
    "steps_json": {"rich_text": {}},
    "widget_id": {"rich_text": {}},
    "blender_version": {"rich_text": {}},
    "official_docs": {"url": {}},
}


VIDEOS_SCHEMA = {
    "title": {"title": {}},
    "url": {"url": {}},
    "channel": {"rich_text": {}},
    "duration_sec": {"number": {}},
    "language": {"select": {"options": [{"name": x} for x in ["ko", "en", "ja"]]}},
    "blender_version": {"rich_text": {}},
    "official": {"checkbox": {}},
    "recommended_reason": {"rich_text": {}},
    "last_verified": {"date": {}},
}


def create_db(parent_id: str, title: str, properties: dict, token: str) -> str:
    body = {
        "parent": {"type": "page_id", "page_id": parent_id},
        "title": [{"type": "text", "text": {"content": title}}],
        "properties": properties,
    }
    resp = _post("/databases", body, token)
    return resp["id"]


def add_relations(cards_db_id: str, videos_db_id: str, token: str) -> None:
    """카드 → 비디오 / 카드 → 카드 self relation 추가 (생성 후 patch)."""
    patch_body = {
        "properties": {
            "videos_relation": {
                "relation": {"database_id": videos_db_id, "type": "single_property", "single_property": {}}
            },
            "prerequisites": {
                "relation": {"database_id": cards_db_id, "type": "single_property", "single_property": {}}
            },
            "related": {
                "relation": {"database_id": cards_db_id, "type": "single_property", "single_property": {}}
            },
        }
    }
    req = urllib.request.Request(
        f"{NOTION_API}/databases/{cards_db_id}",
        data=json.dumps(patch_body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        },
        method="PATCH",
    )
    with urllib.request.urlopen(req) as r:
        r.read()


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--parent", required=True, help="Parent Notion page ID")
    args = p.parse_args()

    token = get_notion_token()

    print("Creating ShowMe Videos DB...")
    videos_id = create_db(args.parent, "ShowMe Videos", VIDEOS_SCHEMA, token)
    print(f"  → {videos_id}")

    print("Creating ShowMe Cards DB...")
    cards_id = create_db(args.parent, "ShowMe Cards", CARDS_SCHEMA, token)
    print(f"  → {cards_id}")

    print("Adding relations...")
    add_relations(cards_id, videos_id, token)
    print("  → relations added (videos_relation, prerequisites, related)")

    OUTPUT.write_text(
        json.dumps({"cards_db_id": cards_id, "videos_db_id": videos_id}, indent=2)
    )
    print(f"\nWritten: {OUTPUT}")


if __name__ == "__main__":
    main()
