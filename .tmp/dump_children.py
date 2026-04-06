#!/usr/bin/env python3
"""has_children=True 인 quote 블록 내부 자식 재귀 확인"""
import sys, os
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "tools"))

env_path = ROOT / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

from grading_db import load_student_roster, parse_student_weeks
from notion_api import _get_page_blocks, extract_text, get_notion_token

token = get_notion_token()
students = load_student_roster(class_num="1")
targets = ["김민서", "이정민", "전영훈", "조수연", "이지연", "윤서현"]

for s in students:
    if s["name"] not in targets:
        continue
    print(f"\n=== {s['name']} ===")
    try:
        blocks = _get_page_blocks(s["page_id"], token=token)
        weeks = parse_student_weeks(blocks)
        w4 = weeks.get("04", [])
        if not w4:
            # 조수연 같은 경우 - Week 03 섹션 확인
            w3 = weeks.get("03", [])
            print(f"  Week 04 없음. Week 03 내용 확인:")
            for i, b in enumerate(w3):
                btype = b.get("type", "")
                text = extract_text(b.get(btype, {}).get("rich_text", []))[:60]
                print(f"    {i} [{btype}] {text!r}")
            continue
        for i, b in enumerate(w4):
            btype = b.get("type", "")
            bid = b.get("id", "")
            has_children = b.get("has_children", False)
            text = extract_text(b.get(btype, {}).get("rich_text", []))[:60]
            print(f"  Week04 블록 {i} [{btype}] {text!r} has_children={has_children}")
            if has_children:
                # 자식 블록 조회
                try:
                    children = _get_page_blocks(bid, token=token)
                    print(f"    → 자식 {len(children)}개:")
                    for j, c in enumerate(children):
                        ctype = c.get("type", "")
                        ctext = extract_text(c.get(ctype, {}).get("rich_text", []))[:60]
                        c_has_children = c.get("has_children", False)
                        marker = "📎" if ctype in ("image", "file", "video", "embed", "pdf") else "  "
                        print(f"      {marker} {j} [{ctype}] {ctext!r} has_children={c_has_children}")
                        if c_has_children and ctype in ("column_list", "column", "toggle"):
                            # 한 층 더
                            gchildren = _get_page_blocks(c.get("id",""), token=token)
                            for k, g in enumerate(gchildren):
                                gtype = g.get("type", "")
                                gtext = extract_text(g.get(gtype, {}).get("rich_text", []))[:60]
                                gmarker = "📎" if gtype in ("image", "file", "video", "embed", "pdf") else "  "
                                print(f"        {gmarker} {k} [{gtype}] {gtext!r}")
                except Exception as e:
                    print(f"    ERROR: {e}")

print("\n=== Done ===")

