#!/usr/bin/env python3
"""
sync_references.py — Notion 참고자료 아카이브 → course-site/data/references.json 동기화

Notion 교수자 운영 페이지 > 📚 참고자료 페이지를 파싱하여
주차별/섹션별 참고자료를 references.json으로 생성한다.

Usage:
    python3 tools/sync_references.py [--week N] [--dry-run]

Options:
    --week N     특정 주차만 동기화 (기본: 전체)
    --dry-run    파일에 쓰지 않고 stdout에 출력
"""
import os
import sys
import json
import re
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from notion_api import _get_page_blocks, notion_request

ARCHIVE_PAGE_ID = "66c54d654971826496f801ab48dce4c8"  # 📚 참고자료
OUTPUT_PATH = Path(__file__).parent.parent / "course-site/data/references.json"

# 아카이브 섹션 → 주차 매핑 (heading_3 텍스트 → 주차 번호들)
SECTION_WEEK_MAP = {
    "1. Blender 기초 (Week 2)": [2],
    "2. 모델링 (Week 3-5)": [3, 4, 5],
    "3. 재질 — Material (Week 6)": [6],
    "4. UV & 텍스처 (Week 7)": [7],
    "5. 조명 (Week 9)": [9],
    "6. 카메라 & 렌더링 (Week 9-10)": [9, 10],
    "7. 애니메이션 (Week 10)": [10],
    "8. 리깅 (Week 11-12)": [11, 12],
    "9. 물리 시뮬레이션": [],
    "10. 추천 영상 자료": [],
}


def get_text(rt_list):
    return "".join(
        rt.get("plain_text", "") for rt in (rt_list or []) if isinstance(rt, dict)
    )


def slugify(title):
    """Material Basic → material-basic"""
    s = title.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def extract_notion_url_id(url):
    """https://www.notion.so/abc123... → abc123..."""
    m = re.search(r"([a-f0-9]{32})", url or "")
    return m.group(1) if m else None


def extract_links_from_block(b):
    """블록에서 외부/Notion 링크 추출"""
    btype = b.get("type", "")
    content = b.get(btype, {}) or {}
    links = []
    if isinstance(content, dict):
        for rt in content.get("rich_text", []) or []:
            if isinstance(rt, dict) and rt.get("href"):
                links.append({"text": rt.get("plain_text", ""), "url": rt["href"]})
        if btype == "bookmark" and content.get("url"):
            links.append({"text": "bookmark", "url": content["url"]})
        if btype == "embed" and content.get("url"):
            links.append({"text": "embed", "url": content["url"]})
        if btype == "video":
            vu = (content.get("external") or {}).get("url", "") or (
                content.get("file") or {}
            ).get("url", "")
            if vu:
                links.append({"text": "video", "url": vu})
    return links


def parse_archive():
    """📚 참고자료 페이지 → 섹션별 항목 파싱"""
    blocks = _get_page_blocks(ARCHIVE_PAGE_ID)
    sections = []
    current_section = None

    for b in blocks:
        btype = b.get("type", "")
        content = b.get(btype, {}) or {}

        if btype == "heading_3":
            title = get_text(content.get("rich_text", []))
            current_section = {
                "title": title,
                "weeks": SECTION_WEEK_MAP.get(title, []),
                "items": [],
                "video_toggles": [],
            }
            sections.append(current_section)
        elif btype == "bulleted_list_item" and current_section:
            text = get_text(content.get("rich_text", []))
            links = extract_links_from_block(b)
            if links:
                for link in links:
                    current_section["items"].append(
                        {
                            "title": text or link["text"],
                            "notion_url": link["url"],
                            "notion_page_id": extract_notion_url_id(link["url"]),
                        }
                    )
            elif text:
                current_section["items"].append({"title": text, "notion_url": None})
        elif btype == "toggle" and current_section:
            toggle_text = get_text(content.get("rich_text", []))
            if "🎬" in toggle_text or "영상" in toggle_text:
                # Fetch toggle children for video items
                children = _get_page_blocks(b["id"])
                videos = []
                for ch in children:
                    ch_type = ch.get("type", "")
                    ch_content = ch.get(ch_type, {}) or {}
                    if ch_type == "bulleted_list_item":
                        ch_text = get_text(ch_content.get("rich_text", []))
                        ch_links = extract_links_from_block(ch)
                        videos.append(
                            {
                                "title": ch_text,
                                "links": ch_links,
                                "has_nested": ch.get("has_children", False),
                                "block_id": ch.get("id"),
                            }
                        )
                current_section["video_toggles"].append(
                    {"label": toggle_text, "videos": videos}
                )

    return sections


def build_references(sections, filter_week=None):
    """섹션 목록 → references.json 구조"""
    refs = {
        "_meta": {
            "source": "Notion 교수자 운영 페이지 > 📚 참고자료",
            "source_page_id": ARCHIVE_PAGE_ID,
            "generated_by": "tools/sync_references.py",
        },
        "sections": [],
    }

    for section in sections:
        if filter_week is not None:
            if filter_week not in section["weeks"]:
                continue
        section_entry = {
            "title": section["title"],
            "weeks": section["weeks"],
            "tutorials": [],
            "video_collections": [],
        }
        for item in section["items"]:
            section_entry["tutorials"].append(
                {
                    "slug": slugify(item["title"]),
                    "title": item["title"],
                    "notion_url": item.get("notion_url"),
                    "notion_page_id": item.get("notion_page_id"),
                }
            )
        for vt in section["video_toggles"]:
            videos_out = []
            for v in vt["videos"]:
                videos_out.append(
                    {
                        "title": v["title"],
                        "external_links": [
                            l["url"] for l in v.get("links", []) if l.get("url")
                        ],
                        "notion_block_id": v.get("block_id"),
                    }
                )
            section_entry["video_collections"].append(
                {"label": vt["label"], "videos": videos_out}
            )
        refs["sections"].append(section_entry)

    return refs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", type=int, help="특정 주차만 (예: --week 6)")
    ap.add_argument("--dry-run", action="store_true", help="파일 쓰지 않음")
    args = ap.parse_args()

    print(f"📚 Notion 아카이브 파싱 중...", file=sys.stderr)
    sections = parse_archive()
    print(
        f"  → {len(sections)}개 섹션 발견, {sum(len(s['items']) for s in sections)}개 문서, {sum(len(s['video_toggles']) for s in sections)}개 비디오 토글",
        file=sys.stderr,
    )

    refs = build_references(sections, filter_week=args.week)
    total_tutorials = sum(len(s["tutorials"]) for s in refs["sections"])
    print(
        f"  → {len(refs['sections'])}개 섹션, {total_tutorials}개 튜토리얼 링크 출력",
        file=sys.stderr,
    )

    output = json.dumps(refs, ensure_ascii=False, indent=2)

    if args.dry_run:
        print(output)
    else:
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_PATH.write_text(output + "\n", encoding="utf-8")
        print(f"✅ 저장: {OUTPUT_PATH}", file=sys.stderr)


if __name__ == "__main__":
    main()
