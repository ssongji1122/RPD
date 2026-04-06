#!/usr/bin/env python3
"""
학생 제출 페이지 전수 덤프 - 오탐 원인 조사용
Week 4 미제출로 찍힌 9명의 페이지 전체 블록 구조를 출력.
"""
import sys
import os
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "tools"))

# .env 로드
env_path = ROOT / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

from grading_db import load_student_roster, parse_student_weeks, detect_submission, PLACEHOLDERS
from notion_api import _get_page_blocks, extract_text, get_notion_token

# Week 4 미제출 9명 (로그에서 추출)
NOT_SUBMITTED_W4 = ["김민서", "엄다현", "윤서현", "이정민", "이지연", "이채원", "이태윤", "전영훈", "조수연"]
WEEK = "04"

token = get_notion_token()
students = load_student_roster(class_num="1")
target_students = [s for s in students if s["name"] in NOT_SUBMITTED_W4]

print(f"=== Week {WEEK} '미제출' 판정 9명 전수 조사 ===\n")

for s in target_students:
    print("=" * 70)
    print(f"학생: {s['name']} (class {s['class_num']})")
    print(f"page_id: {s['page_id']}")
    print("-" * 70)
    try:
        blocks = _get_page_blocks(s["page_id"], token=token)
    except Exception as e:
        print(f"ERROR: {e}")
        continue

    # 1. 먼저 모든 heading 블록 나열 (주차 구분 확인)
    print("[모든 heading 블록]")
    for i, b in enumerate(blocks):
        btype = b.get("type", "")
        if btype in ("heading_1", "heading_2", "heading_3"):
            text = extract_text(b[btype].get("rich_text", []))
            print(f"  {i:3d} [{btype}] {text!r}")

    # 2. parse_student_weeks 결과
    weeks = parse_student_weeks(blocks)
    print(f"\n[파싱된 주차 키]: {sorted(weeks.keys())}")
    print(f"[Week {WEEK} 블록 개수]: {len(weeks.get(WEEK, []))}")

    # 3. Week 04 섹션 내용 dump
    print(f"\n[Week {WEEK} 섹션의 모든 블록 상세]")
    w_blocks = weeks.get(WEEK, [])
    if not w_blocks:
        print("  (빈 섹션 — heading 매칭 실패 또는 다음 주차 바로 시작)")
    for i, b in enumerate(w_blocks):
        btype = b.get("type", "")
        has_children = b.get("has_children", False)
        text_preview = ""
        if btype in b:
            rt = b[btype].get("rich_text", [])
            text_preview = extract_text(rt)[:80]
        marker = "📎" if btype in ("image", "file", "video", "embed", "pdf", "column_list", "column") else "  "
        child_marker = " [has_children=True]" if has_children else ""
        print(f"  {marker} {i:2d} [{btype}] {text_preview!r}{child_marker}")

    # 4. detect_submission 결과
    submitted = detect_submission(w_blocks)
    print(f"\n[detect_submission 판정]: {'✅ 제출' if submitted else '❌ 미제출'}")
    print()

print("=" * 70)
print("조사 완료")
