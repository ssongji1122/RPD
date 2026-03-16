# Notion 자동 동기화 (2-Layer Architecture) Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 노션을 콘텐츠 정본(Source of Truth)으로 전환하고, GitHub Actions cron으로 자동 동기화 + 어드민 override가 공존하는 시스템 구축

**Architecture:** curriculum-notion.json(노션 자동 스냅샷) + overrides.json(어드민 수정) → merge → curriculum.js(최종 웹 출력). GitHub Actions가 30분마다 노션에서 풀하여 자동 배포.

**Tech Stack:** Python 3 (stdlib only), GitHub Actions, Notion API v2022-06-28

---

## 데이터 흐름

```
Notion Pages (정본)
    ↓  GitHub Actions cron (30분)
    ↓  tools/notion-sync.py
curriculum-notion.json  ← 노션 원본 스냅샷
    +
overrides.json          ← 어드민 수정 (이미지, 영상, 멘트, status)
    ↓  merge (notion-sync.py --merge)
curriculum.js           ← 최종 웹 렌더링용
    ↓  auto-commit + deploy-pages.yml
GitHub Pages
```

## 필드 소유권

| 소유자 | 필드 | 비고 |
|--------|------|------|
| **노션** | title, subtitle, duration, topics, steps[].title, steps[].copy, steps[].goal, steps[].tasks, assignment, shortcuts, mistakes, docs | 자동 동기화, 어드민에서 읽기 전용 |
| **어드민** | status, summary, steps[].image, steps[].done, steps[].showme, steps[].link, videos, explore | overrides.json에 저장 |
| **어드민 (선택)** | 아무 필드 copy override | overrides에 명시하면 노션보다 우선 |

## overrides.json 스키마

```json
{
  "_comment": "어드민 전용 필드. 노션 동기화 시 이 값이 우선함.",
  "weeks": {
    "1": {
      "status": "done",
      "summary": "Blender 설치, Mixboard로 컨셉 설정.",
      "videos": [{ "title": "...", "url": "..." }],
      "explore": [{ "title": "...", "hint": "..." }],
      "steps": {
        "0": {
          "image": "assets/images/week-01/step-0.png",
          "done": ["Blender가 정상적으로 열린다"],
          "showme": "mirror-modifier"
        },
        "1": {
          "copy": "어드민에서 수정한 멘트 (노션 원본 대신 사용)"
        }
      }
    }
  }
}
```

## 머지 규칙

1. 기본: curriculum-notion.json의 주차 데이터를 베이스로 사용
2. overrides.json에 해당 주차/필드가 있으면 → 오버라이드 값이 우선
3. steps는 인덱스 기반 머지 (step 0, 1, 2, ...)
4. 배열 필드(videos, explore, done 등)는 전체 교체 (개별 항목 머지 아님)
5. overrides에 없는 필드 → 노션 원본 그대로

---

## Task 1: Notion API 공유 모듈 추출

**Files:**
- Create: `tools/notion_api.py`
- Modify: `tools/admin-server.py` (import로 교체)

**Step 1: notion_api.py 생성**

admin-server.py에서 다음 함수들을 추출:
```python
# tools/notion_api.py
"""Shared Notion API helpers. Stdlib only."""

import json
import os
import re
import urllib.request
from pathlib import Path

NOTION_API = "https://api.notion.com/v1"
ROOT = Path(__file__).resolve().parent.parent
NOTION_MAPPING = ROOT / "tools" / "notion-mapping.json"


def get_notion_token() -> str | None:
    return os.environ.get("NOTION_TOKEN")


def load_notion_mapping() -> dict:
    ...  # 기존 _load_notion_mapping 로직


def notion_request(method: str, endpoint: str, body: dict | None = None,
                   token: str | None = None) -> dict:
    ...  # 기존 _notion_request 로직, token 파라미터 추가


def extract_text(rich_text_array: list) -> str:
    ...  # 기존 _extract_text 로직


def get_page_blocks_recursive(page_id: str, token: str | None = None) -> list[dict]:
    ...  # 기존 _get_notion_page_blocks_recursive 로직


def fetch_notion_to_curriculum(week_num: int, existing_week: dict,
                                token: str | None = None) -> dict:
    ...  # 기존 fetch_notion_to_curriculum 로직


def delete_all_blocks(page_id: str, token: str | None = None) -> int:
    ...  # 기존 _delete_all_notion_blocks 로직


def week_to_notion_blocks(week: dict) -> list[dict]:
    ...  # 기존 _week_to_notion_blocks 로직


def sync_week_to_notion(week: dict, token: str | None = None) -> dict:
    ...  # 기존 sync_week_to_notion 로직
```

**Step 2: admin-server.py에서 import로 교체**

```python
# admin-server.py 상단에 추가
from notion_api import (
    load_notion_mapping, notion_request, fetch_notion_to_curriculum,
    sync_week_to_notion, get_notion_token,
)
```

기존 `_load_notion_mapping`, `_notion_request`, `_extract_text`, `_get_notion_page_blocks_recursive`, `fetch_notion_to_curriculum`, `sync_week_to_notion`, `_week_to_notion_blocks`, `_delete_all_notion_blocks` 함수 삭제.

**Step 3: 동작 확인**

```bash
cd tools && python3 -c "from notion_api import load_notion_mapping; print(load_notion_mapping())"
NOTION_TOKEN=test python3 admin-server.py --port 0 &  # 기동 확인 후 종료
```

**Step 4: Commit**

```bash
git add tools/notion_api.py tools/admin-server.py
git commit -m "refactor: extract Notion API functions into shared module"
```

---

## Task 2: overrides.json 생성 + 마이그레이션 스크립트

**Files:**
- Create: `tools/migrate-to-overrides.py`
- Create: `course-site/data/overrides.json`

**Step 1: 마이그레이션 스크립트 작성**

현재 curriculum.js에서 어드민 전용 필드를 추출하여 overrides.json 생성:

```python
# tools/migrate-to-overrides.py
"""One-time migration: extract admin-owned fields from curriculum.js into overrides.json."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from admin_server_helpers import read_curriculum  # 또는 직접 파싱

ROOT = Path(__file__).resolve().parent.parent
CURRICULUM_JS = ROOT / "course-site" / "data" / "curriculum.js"
OVERRIDES_PATH = ROOT / "course-site" / "data" / "overrides.json"

# 어드민 소유 필드 (주차 레벨)
ADMIN_WEEK_FIELDS = {"status", "summary", "videos", "explore"}
# 어드민 소유 필드 (스텝 레벨)
ADMIN_STEP_FIELDS = {"image", "done", "showme", "link"}


def migrate():
    # curriculum.js 파싱 (JS→JSON 변환 포함)
    ...

    overrides = {"_comment": "어드민 전용 필드. 노션 동기화 시 이 값이 우선함.", "weeks": {}}

    for week in data:
        week_num = str(week["week"])
        week_override = {}

        for field in ADMIN_WEEK_FIELDS:
            if field in week and week[field]:
                week_override[field] = week[field]

        steps_override = {}
        for idx, step in enumerate(week.get("steps", [])):
            step_ov = {}
            for field in ADMIN_STEP_FIELDS:
                if field in step and step[field]:
                    step_ov[field] = step[field]
            if step_ov:
                steps_override[str(idx)] = step_ov

        if steps_override:
            week_override["steps"] = steps_override
        if week_override:
            overrides["weeks"][week_num] = week_override

    OVERRIDES_PATH.write_text(
        json.dumps(overrides, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )
    print(f"Wrote {OVERRIDES_PATH}")


if __name__ == "__main__":
    migrate()
```

**Step 2: 실행하여 overrides.json 생성**

```bash
python3 tools/migrate-to-overrides.py
cat course-site/data/overrides.json | python3 -m json.tool | head -30
```

Expected: JSON with weeks.1.status, weeks.1.steps.0.image 등이 포함됨

**Step 3: Commit**

```bash
git add tools/migrate-to-overrides.py course-site/data/overrides.json
git commit -m "feat: create overrides.json with migrated admin fields"
```

---

## Task 3: notion-sync.py (핵심 동기화 스크립트)

**Files:**
- Create: `tools/notion-sync.py`
- Create: `course-site/data/curriculum-notion.json`

**Step 1: notion-sync.py 작성**

```python
#!/usr/bin/env python3
"""
Notion → curriculum.js 자동 동기화 스크립트.

Usage:
    # 전체 동기화 (fetch + merge)
    python3 tools/notion-sync.py

    # fetch만 (curriculum-notion.json 업데이트)
    python3 tools/notion-sync.py --fetch-only

    # merge만 (notion + overrides → curriculum.js)
    python3 tools/notion-sync.py --merge-only

Environment:
    NOTION_TOKEN  - Notion API 토큰 (--merge-only가 아닌 경우 필수)

Exit codes:
    0 - 성공 (변경 있음)
    1 - 에러
    2 - 성공 (변경 없음, GitHub Actions에서 commit 스킵용)
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from notion_api import (
    fetch_notion_to_curriculum, load_notion_mapping, get_notion_token,
)

ROOT = Path(__file__).resolve().parent.parent
COURSE_DATA = ROOT / "course-site" / "data"
NOTION_JSON = COURSE_DATA / "curriculum-notion.json"
OVERRIDES_JSON = COURSE_DATA / "overrides.json"
CURRICULUM_JS = COURSE_DATA / "curriculum.js"

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


def fetch_all_weeks() -> list[dict]:
    """모든 주차를 Notion에서 가져온다."""
    mapping = load_notion_mapping()
    weeks = []

    # 기존 curriculum-notion.json이 있으면 existing으로 사용
    existing_weeks = {}
    if NOTION_JSON.exists():
        for w in json.loads(NOTION_JSON.read_text(encoding="utf-8")):
            existing_weeks[w["week"]] = w

    for week_str in sorted(mapping.keys(), key=int):
        week_num = int(week_str)
        existing = existing_weeks.get(week_num, {"week": week_num})
        try:
            fetched = fetch_notion_to_curriculum(week_num, existing)
            weeks.append(fetched)
            print(f"  ✓ Week {week_num}: {fetched.get('title', '?')}")
        except Exception as exc:
            print(f"  ✗ Week {week_num}: {exc}", file=sys.stderr)
            # 실패 시 기존 데이터 유지
            if existing.get("title"):
                weeks.append(existing)

    return sorted(weeks, key=lambda w: w.get("week", 0))


def merge(notion_data: list[dict], overrides: dict) -> list[dict]:
    """notion 데이터에 overrides를 머지한다."""
    weeks_ov = overrides.get("weeks", {})
    result = []

    for week in notion_data:
        week_num = str(week["week"])
        merged = {**week}

        ov = weeks_ov.get(week_num, {})

        # 주차 레벨 필드 오버라이드
        for key, val in ov.items():
            if key == "steps":
                continue  # steps는 별도 처리
            merged[key] = val

        # 스텝 레벨 필드 오버라이드
        steps_ov = ov.get("steps", {})
        if steps_ov and "steps" in merged:
            merged_steps = []
            for idx, step in enumerate(merged["steps"]):
                step_ov = steps_ov.get(str(idx), {})
                merged_step = {**step, **step_ov}
                merged_steps.append(merged_step)
            merged["steps"] = merged_steps

        result.append(merged)

    return result


def write_curriculum_js(data: list[dict]) -> None:
    """curriculum.js로 출력한다."""
    pretty = json.dumps(data, ensure_ascii=False, indent=2)
    content = CURRICULUM_HEADER + pretty + CURRICULUM_FOOTER
    CURRICULUM_JS.write_text(content, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Notion → curriculum.js sync")
    parser.add_argument("--fetch-only", action="store_true",
                        help="Notion에서 가져오기만 (merge 안 함)")
    parser.add_argument("--merge-only", action="store_true",
                        help="기존 notion JSON + overrides → curriculum.js")
    args = parser.parse_args()

    changed = False

    # --- Fetch ---
    if not args.merge_only:
        token = get_notion_token()
        if not token:
            print("ERROR: NOTION_TOKEN 환경 변수가 필요합니다.", file=sys.stderr)
            sys.exit(1)

        print("Fetching from Notion...")
        weeks = fetch_all_weeks()

        new_json = json.dumps(weeks, ensure_ascii=False, indent=2) + "\n"
        old_json = NOTION_JSON.read_text(encoding="utf-8") if NOTION_JSON.exists() else ""

        if new_json != old_json:
            NOTION_JSON.write_text(new_json, encoding="utf-8")
            print(f"Updated {NOTION_JSON.name} ({len(weeks)} weeks)")
            changed = True
        else:
            print("No changes from Notion.")

    if args.fetch_only:
        sys.exit(0 if changed else 2)

    # --- Merge ---
    notion_data = json.loads(NOTION_JSON.read_text(encoding="utf-8"))

    overrides = {}
    if OVERRIDES_JSON.exists():
        overrides = json.loads(OVERRIDES_JSON.read_text(encoding="utf-8"))

    merged = merge(notion_data, overrides)

    new_js = CURRICULUM_HEADER + json.dumps(merged, ensure_ascii=False, indent=2) + CURRICULUM_FOOTER
    old_js = CURRICULUM_JS.read_text(encoding="utf-8") if CURRICULUM_JS.exists() else ""

    if new_js != old_js:
        CURRICULUM_JS.write_text(new_js, encoding="utf-8")
        print(f"Updated {CURRICULUM_JS.name}")
        changed = True
    else:
        print("curriculum.js unchanged.")

    sys.exit(0 if changed else 2)


if __name__ == "__main__":
    main()
```

**Step 2: 수동 테스트 — merge-only 모드**

overrides.json + 현재 curriculum-notion.json 없으므로 먼저 생성:
```bash
# 현재 curriculum.js를 notion JSON으로 변환 (초기 시드)
python3 -c "
import sys; sys.path.insert(0, 'tools')
from admin_server_helpers import read_curriculum
import json
data = read_curriculum()
# admin 필드 제거하여 notion-only 데이터 생성
for w in data:
    w.pop('status', None); w.pop('summary', None); w.pop('videos', None); w.pop('explore', None)
    for s in w.get('steps', []):
        s.pop('image', None); s.pop('done', None); s.pop('showme', None); s.pop('link', None)
print(json.dumps(data, ensure_ascii=False, indent=2))
" > course-site/data/curriculum-notion.json

# merge 테스트
python3 tools/notion-sync.py --merge-only
```

Expected: curriculum.js 내용이 기존과 동일 (notion + overrides = 원본)

**Step 3: Notion fetch 테스트 (토큰 있을 때)**

```bash
NOTION_TOKEN=ntn_xxx python3 tools/notion-sync.py --fetch-only
```

Expected: curriculum-notion.json 업데이트, 각 주차 ✓ 출력

**Step 4: Commit**

```bash
git add tools/notion-sync.py course-site/data/curriculum-notion.json
git commit -m "feat: add notion-sync.py for automated Notion→curriculum.js sync"
```

---

## Task 4: GitHub Actions 워크플로우

**Files:**
- Create: `.github/workflows/notion-sync.yml`

**Step 1: 워크플로우 작성**

```yaml
name: Notion Auto-Sync

on:
  schedule:
    # 매 30분마다 실행 (UTC)
    - cron: '*/30 * * * *'
  workflow_dispatch:
    inputs:
      force:
        description: '변경 없어도 강제 커밋'
        required: false
        default: 'false'

permissions:
  contents: write
  pages: write
  id-token: write

jobs:
  sync:
    runs-on: ubuntu-latest
    env:
      FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Run Notion Sync
        id: sync
        env:
          NOTION_TOKEN: ${{ secrets.NOTION_TOKEN }}
        run: |
          python3 tools/notion-sync.py
          echo "changed=true" >> "$GITHUB_OUTPUT"
        continue-on-error: true

      - name: Check for changes
        id: check
        run: |
          if git diff --quiet course-site/data/; then
            echo "changed=false" >> "$GITHUB_OUTPUT"
          else
            echo "changed=true" >> "$GITHUB_OUTPUT"
          fi

      - name: Commit and push
        if: steps.check.outputs.changed == 'true' || github.event.inputs.force == 'true'
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add course-site/data/curriculum-notion.json course-site/data/curriculum.js
          git commit -m "sync: Notion 자동 동기화 $(date -u +'%Y-%m-%d %H:%M UTC')"
          git push

  # 변경이 있으면 deploy-pages가 자동 트리거됨 (course-site/** push on main)
```

**Step 2: GitHub repo에 NOTION_TOKEN 시크릿 추가 필요**

```
Settings → Secrets and variables → Actions → New repository secret
Name: NOTION_TOKEN
Value: ntn_xxx...
```

**Step 3: Commit**

```bash
git add .github/workflows/notion-sync.yml
git commit -m "ci: add Notion auto-sync cron workflow (30min interval)"
```

---

## Task 5: admin-server.py 수정 — overrides.json 기반 저장

**Files:**
- Modify: `tools/admin-server.py`

**변경 사항:**

### 5-1. 새 상수 추가

```python
OVERRIDES_JSON = COURSE_SITE / "data" / "overrides.json"

# 어드민 소유 필드 정의
ADMIN_WEEK_FIELDS = {"status", "summary", "videos", "explore"}
ADMIN_STEP_FIELDS = {"image", "done", "showme", "link"}
```

### 5-2. overrides 읽기/쓰기 헬퍼

```python
def read_overrides() -> dict:
    """Read overrides.json."""
    if not OVERRIDES_JSON.exists():
        return {"weeks": {}}
    return json.loads(OVERRIDES_JSON.read_text(encoding="utf-8"))


def write_overrides(overrides: dict) -> None:
    """Write overrides.json."""
    OVERRIDES_JSON.write_text(
        json.dumps(overrides, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )
```

### 5-3. GET /api/curriculum 변경

기존: `read_curriculum()` (curriculum.js 직접 파싱)
변경: curriculum-notion.json + overrides.json 머지 결과 반환 + 필드 소유권 메타데이터 추가

```python
def get_merged_curriculum() -> list[dict]:
    """Read curriculum-notion.json + overrides.json, return merged."""
    # curriculum-notion.json이 없으면 기존 curriculum.js 폴백
    notion_path = COURSE_SITE / "data" / "curriculum-notion.json"
    if notion_path.exists():
        notion_data = json.loads(notion_path.read_text(encoding="utf-8"))
    else:
        notion_data = read_curriculum()

    overrides = read_overrides()
    # merge 로직 (notion-sync.py의 merge 함수와 동일)
    ...
    return merged
```

### 5-4. PUT /api/curriculum 변경 → PUT /api/overrides

전체 curriculum 배열을 받는 대신, 변경된 어드민 필드만 overrides.json에 저장:

```python
# PUT /api/overrides
def _handle_put_overrides(self) -> None:
    body = self._read_body()
    payload = json.loads(body)  # { weekNum: 1, field: "status", value: "done" }

    overrides = read_overrides()
    week_num = str(payload["weekNum"])

    if week_num not in overrides["weeks"]:
        overrides["weeks"][week_num] = {}

    field = payload["field"]

    if payload.get("stepIdx") is not None:
        # 스텝 레벨 오버라이드
        step_idx = str(payload["stepIdx"])
        if "steps" not in overrides["weeks"][week_num]:
            overrides["weeks"][week_num]["steps"] = {}
        if step_idx not in overrides["weeks"][week_num]["steps"]:
            overrides["weeks"][week_num]["steps"][step_idx] = {}
        overrides["weeks"][week_num]["steps"][step_idx][field] = payload["value"]
    else:
        # 주차 레벨 오버라이드
        overrides["weeks"][week_num][field] = payload["value"]

    write_overrides(overrides)

    # curriculum.js 재생성
    merged = get_merged_curriculum()
    write_curriculum(merged)

    self._send_json({"ok": True})
```

기존 `PUT /api/curriculum` 엔드포인트도 하위 호환을 위해 유지하되, 내부적으로 overrides 기반으로 동작하도록 변경.

### 5-5. 이미지 업로드 → overrides.json에 경로 저장

`_handle_upload` 수정: curriculum.js 직접 수정 대신 overrides.json의 해당 step에 image 경로 저장.

### 5-6. GET /api/curriculum 응답에 소유권 메타데이터 추가

```python
# 응답 형식
{
    "data": [...],  # 머지된 curriculum 배열
    "ownership": {
        "notion": ["title", "subtitle", "duration", "topics", "steps.title",
                    "steps.copy", "steps.goal", "steps.tasks", "assignment",
                    "shortcuts", "mistakes", "docs"],
        "admin": ["status", "summary", "videos", "explore",
                  "steps.image", "steps.done", "steps.showme", "steps.link"]
    }
}
```

### 5-7: Notion Push/Pull 엔드포인트 유지 (선택적 수동 트리거)

Push/Pull은 제거하지 않고, 긴급 수동 동기화용으로 유지. 다만 Pull 결과를 overrides가 아닌 curriculum-notion.json에 저장하도록 변경.

**Step 8: 동작 확인**

```bash
ADMIN_KEY=test python3 tools/admin-server.py &
# 어드민 열기: http://localhost:8765/admin.html
# 이미지 업로드 → overrides.json에 경로 저장 확인
# status 변경 → overrides.json 업데이트 확인
cat course-site/data/overrides.json | python3 -m json.tool | head -20
kill %1
```

**Step 9: Commit**

```bash
git add tools/admin-server.py
git commit -m "feat: admin-server saves to overrides.json, reads merged data"
```

---

## Task 6: admin.html UI 업데이트

**Files:**
- Modify: `course-site/admin.html`

**변경 사항:**

### 6-1. 노션 소유 필드 읽기 전용 표시

```javascript
// 노션 소유 필드를 시각적으로 구분
const NOTION_FIELDS = new Set([
    "title", "subtitle", "duration", "topics",
    "assignment", "shortcuts", "mistakes", "docs"
]);
const NOTION_STEP_FIELDS = new Set(["title", "copy", "goal", "tasks"]);

function buildEditorHTML(week) {
    // 노션 필드: 회색 배경 + 자물쇠 아이콘 + disabled
    // 어드민 필드: 일반 편집 가능
    ...
}
```

### 6-2. 저장 플로우 변경

기존: `PUT /api/curriculum` (전체 배열 전송)
변경: 변경된 어드민 필드만 `PUT /api/overrides`로 전송

```javascript
async function saveOverride(weekNum, field, value, stepIdx = null) {
    const payload = { weekNum, field, value };
    if (stepIdx !== null) payload.stepIdx = stepIdx;

    const resp = await fetch("/api/overrides", {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${ADMIN_KEY}`
        },
        body: JSON.stringify(payload)
    });
    return resp.json();
}
```

### 6-3. Notion Push/Pull 버튼 → "수동 동기화" 버튼으로 변경

- "Notion Push" → 제거 (노션이 정본이므로 push 불필요)
- "Notion Pull" → "🔄 지금 동기화" (curriculum-notion.json 갱신)

### 6-4. 노션 필드 안내 문구

```html
<div class="notion-info-banner">
    📝 회색 필드는 노션에서 관리됩니다. 수정하려면 노션에서 편집하세요.
    <a href="https://notion.so/..." target="_blank">노션 열기</a>
</div>
```

**Step 5: 동작 확인**

```bash
ADMIN_KEY=test python3 tools/admin-server.py
# http://localhost:8765/admin.html 열어서:
# - 노션 필드가 읽기 전용인지 확인
# - status 변경 → overrides.json 반영 확인
# - 이미지 업로드 → overrides.json 반영 확인
# - "지금 동기화" 버튼 → curriculum-notion.json 갱신 확인
```

**Step 6: Commit**

```bash
git add course-site/admin.html
git commit -m "feat: admin UI shows Notion fields as read-only, saves to overrides"
```

---

## Task 7: 초기 curriculum-notion.json 시드 + 통합 테스트

**Files:**
- Generate: `course-site/data/curriculum-notion.json` (Notion에서 최초 fetch)

**Step 1: 최초 Notion fetch**

```bash
NOTION_TOKEN=ntn_xxx python3 tools/notion-sync.py --fetch-only
```

**Step 2: 전체 파이프라인 테스트**

```bash
# 1. merge만 실행
python3 tools/notion-sync.py --merge-only

# 2. curriculum.js가 정상인지 확인
python3 -c "
import sys; sys.path.insert(0, 'tools')
# curriculum.js를 Node.js로 파싱
"
node -e "const C = require('./course-site/data/curriculum.js'); console.log(C.length + ' weeks loaded')"

# 3. 웹 페이지 정상 확인
python3 tools/admin-server.py &
# http://localhost:8765/ 접속하여 주차 카드 렌더링 확인
# http://localhost:8765/week.html?week=1 접속하여 콘텐츠 확인
```

**Step 3: GitHub Actions 시뮬레이션**

```bash
# 로컬에서 전체 흐름 재현
NOTION_TOKEN=ntn_xxx python3 tools/notion-sync.py
git diff course-site/data/  # 변경 사항 확인
```

**Step 4: Commit**

```bash
git add course-site/data/curriculum-notion.json course-site/data/curriculum.js
git commit -m "feat: initial Notion sync — seed curriculum-notion.json"
```

---

## 완료 후 상태

```
tools/
  notion_api.py          ← NEW: 공유 Notion API 모듈
  notion-sync.py         ← NEW: cron 동기화 스크립트
  migrate-to-overrides.py ← NEW: 일회성 마이그레이션
  admin-server.py        ← MODIFIED: overrides.json 기반
  notion-mapping.json    ← UNCHANGED

course-site/data/
  curriculum-notion.json ← NEW: 노션 자동 스냅샷
  overrides.json         ← NEW: 어드민 수정 데이터
  curriculum.js          ← GENERATED: notion + overrides 머지 결과

.github/workflows/
  notion-sync.yml        ← NEW: 30분 cron 동기화
  deploy-pages.yml       ← UNCHANGED
```

## 롤백 계획

문제 발생 시:
1. `.github/workflows/notion-sync.yml`에서 cron 비활성화 (주석 처리)
2. curriculum.js는 항상 git에 있으므로 `git revert`로 복구 가능
3. overrides.json 삭제하면 기존 방식(curriculum.js 직접 편집)으로 즉시 복귀
