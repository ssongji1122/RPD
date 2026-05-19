# Card SSoT Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Notion Card DB + Videos DB 신설, `tools/showme_build.py` 생성기 PoC, 신규 카드 1개(`collection-outliner`) End-to-end 생성.

**Architecture:** Notion이 콘텐츠 SSoT, repo가 위젯·레이아웃 소유. `showme_build.py`가 Notion DB row를 fetch → `_template.html` 치환 → `course-site/assets/showme/{id}.html` 출력. 파생 인덱스 `_registry.js`, `_catalog.json`도 빌드가 재생성. 기존 79 카드 무영향.

**Tech Stack:** Python 3 (stdlib only — `tools/notion_api.py` 패턴 따름), pytest, Notion API v1 (직접 HTTP), 기존 `_template.html`(퀴즈 제거 변형).

**Scope:** spec의 Phase 1만 다룸. Phase 2 (백로그 8개 작성), Phase 3 (79 카드 마이그레이션), Phase 4 (Week 페이지 정리), Phase 5 (cleanup)는 Phase 1 검증 완료 후 별도 plan으로 작성한다.

**File Structure:**
- `tools/showme_build.py` — 생성기 CLI 진입점
- `tools/showme_lib/__init__.py` — 패키지 마커
- `tools/showme_lib/notion_cards.py` — Notion Card DB fetch + 정규화
- `tools/showme_lib/renderer.py` — HTML 템플릿 치환
- `tools/showme_lib/index.py` — `_registry.js` / `_catalog.json` 재생성
- `tools/showme_lib/types.py` — Card / Video 데이터클래스
- `course-site/assets/showme/_template.v2.html` — 퀴즈 제거, steps 탭 추가된 신규 템플릿
- `tests/test_showme_renderer.py` — 렌더러 단위 테스트
- `tests/test_showme_notion_cards.py` — fetch 정규화 테스트
- `tests/test_showme_index.py` — 인덱스 재생성 테스트
- `tests/fixtures/showme/card_sample.json` — Notion API 응답 샘플 (mock)
- `tests/fixtures/showme/expected_card_sample.html` — 기대 출력
- `.claude/commands/showme-build.md` — `/showme-build` 스킬 정의

각 파일 단일 책임. Notion fetch / rendering / indexing 분리. CLI는 얇은 wrapper.

---

### Task 1: 패키지 골격 + 데이터클래스

**Files:**
- Create: `tools/showme_lib/__init__.py`
- Create: `tools/showme_lib/types.py`
- Create: `tests/test_showme_types.py`

- [ ] **Step 1: Write the failing test for Card dataclass**

`tests/test_showme_types.py`:

```python
from tools.showme_lib.types import Card, Step, Video


def test_card_minimal_fields():
    card = Card(
        card_id="array-modifier",
        label="Array Modifier 이해",
        icon="repeat-2",
        category="modifier",
        weeks=[3],
        priority="P0",
        status="published",
        concept_md="복사기처럼...",
        usage_md="규칙적 반복...",
        pitfall_md="Origin 위치...",
        steps=[],
        videos=[],
        widget_id="array-modifier",
        blender_version="5.0",
        official_docs="https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/array.html",
        prerequisites=[],
        related=[],
    )
    assert card.card_id == "array-modifier"
    assert card.weeks == [3]
    assert card.has_widget is True


def test_card_no_widget():
    card = Card(
        card_id="x",
        label="x",
        icon="x",
        category="modeling",
        weeks=[1],
        priority="P1",
        status="draft",
        concept_md="",
        usage_md="",
        pitfall_md="",
        steps=[],
        videos=[],
        widget_id=None,
        blender_version="5.0",
        official_docs=None,
        prerequisites=[],
        related=[],
    )
    assert card.has_widget is False


def test_step_structure():
    step = Step(n=1, action="Cube 추가", hotkey="Shift + A", menu="Add → Mesh → Cube", screenshot=None, note=None)
    assert step.n == 1
    assert step.hotkey == "Shift + A"


def test_video_structure():
    video = Video(
        title="Array Modifier 완전정복",
        url="https://youtube.com/watch?v=xyz",
        channel="Blender Studio",
        duration_sec=480,
        language="en",
        blender_version="5.0",
        official=True,
        recommended_reason="공식 채널 + 5.0 기준",
    )
    assert video.official is True
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_showme_types.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'tools.showme_lib'`

- [ ] **Step 3: Create package marker**

`tools/showme_lib/__init__.py`:

```python
"""ShowMe card generator library — Notion DB → HTML."""
```

- [ ] **Step 4: Implement dataclasses**

`tools/showme_lib/types.py`:

```python
"""Card / Step / Video data classes."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Step:
    n: int
    action: str
    hotkey: Optional[str]
    menu: Optional[str]
    screenshot: Optional[str]
    note: Optional[str]


@dataclass
class Video:
    title: str
    url: str
    channel: str
    duration_sec: int
    language: str
    blender_version: str
    official: bool
    recommended_reason: str


@dataclass
class Card:
    card_id: str
    label: str
    icon: str
    category: str
    weeks: list[int]
    priority: str
    status: str
    concept_md: str
    usage_md: str
    pitfall_md: str
    steps: list[Step]
    videos: list[Video]
    widget_id: Optional[str]
    blender_version: str
    official_docs: Optional[str]
    prerequisites: list[str]
    related: list[str]

    @property
    def has_widget(self) -> bool:
        return self.widget_id is not None and self.widget_id != ""

    @property
    def has_steps(self) -> bool:
        return len(self.steps) > 0

    @property
    def has_videos(self) -> bool:
        return len(self.videos) > 0
```

- [ ] **Step 5: Run test to verify it passes**

Run: `pytest tests/test_showme_types.py -v`
Expected: 4 passed

- [ ] **Step 6: Commit**

```bash
git add tools/showme_lib/__init__.py tools/showme_lib/types.py tests/test_showme_types.py
git commit -m "feat(showme): Card/Step/Video dataclasses for SSoT generator"
```

---

### Task 2: Notion Card DB 생성 (1회성 스크립트)

**Files:**
- Create: `tools/showme_create_dbs.py`

이 스크립트는 Notion에 두 DB(ShowMe Cards, ShowMe Videos)를 생성하는 1회용 부트스트랩. Notion MCP `create-database`를 직접 호출하지 않고, `tools/notion_api.py` 패턴(HTTP) 으로 수행.

- [ ] **Step 1: Read existing notion_api token loader**

Run: `head -100 tools/notion_api.py | grep -A 20 "def get_notion_token"`
Expected: 함수 시그니처 + Bearer 토큰 로드 로직 확인. 새 스크립트도 동일 패턴.

- [ ] **Step 2: Write the script**

`tools/showme_create_dbs.py`:

```python
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
```

- [ ] **Step 3: Gitignore the output file**

Append to `.gitignore`:

```
tools/showme_db_ids.json
```

Run: `echo "tools/showme_db_ids.json" >> .gitignore`

- [ ] **Step 4: Dry-run check (no network)**

Run: `python3 -c "import ast; ast.parse(open('tools/showme_create_dbs.py').read()); print('syntax OK')"`
Expected: `syntax OK`

- [ ] **Step 5: User executes script with real parent page**

NOTE TO IMPLEMENTER: This step requires the user to provide the parent page ID (likely `e395b2b4-1ddc-4641-9b74-2b59b0abe41b` — studio.soluta 수업자료 허브). Ask the user to run:

```bash
python3 tools/showme_create_dbs.py --parent e395b2b4-1ddc-4641-9b74-2b59b0abe41b
```

Verify `tools/showme_db_ids.json` exists with both IDs. DO NOT commit this file.

- [ ] **Step 6: Commit script (NOT the output)**

```bash
git add tools/showme_create_dbs.py .gitignore
git commit -m "feat(showme): Notion DB bootstrap script for Cards + Videos"
```

---

### Task 3: Notion Card fetch + 정규화

**Files:**
- Create: `tools/showme_lib/notion_cards.py`
- Create: `tests/fixtures/showme/card_sample.json`
- Create: `tests/test_showme_notion_cards.py`

- [ ] **Step 1: Capture Notion API response fixture**

`tests/fixtures/showme/card_sample.json`:

```json
{
  "object": "page",
  "id": "fake-page-id",
  "properties": {
    "card_id": {"title": [{"plain_text": "array-modifier"}]},
    "label": {"rich_text": [{"plain_text": "Array Modifier 이해"}]},
    "icon": {"rich_text": [{"plain_text": "repeat-2"}]},
    "category": {"select": {"name": "modifier"}},
    "week": {"multi_select": [{"name": "3"}, {"name": "4"}]},
    "priority": {"select": {"name": "P0"}},
    "status": {"select": {"name": "published"}},
    "concept_md": {"rich_text": [{"plain_text": "복사기처럼 규칙적으로 반복."}]},
    "usage_md": {"rich_text": [{"plain_text": "손가락 마디, 척추, 볼트."}]},
    "pitfall_md": {"rich_text": [{"plain_text": "Origin 위치 잘못."}]},
    "steps_json": {"rich_text": [{"plain_text": "{\"blender_version\":\"5.0\",\"platform_note\":null,\"steps\":[{\"n\":1,\"action\":\"Cube 추가\",\"hotkey\":\"Shift + A\",\"menu\":\"Add → Mesh → Cube\",\"screenshot\":null,\"note\":null}]}"}]},
    "widget_id": {"rich_text": [{"plain_text": "array-modifier"}]},
    "blender_version": {"rich_text": [{"plain_text": "5.0"}]},
    "official_docs": {"url": "https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/array.html"},
    "prerequisites": {"relation": []},
    "related": {"relation": []},
    "videos_relation": {"relation": []}
  }
}
```

- [ ] **Step 2: Write failing test**

`tests/test_showme_notion_cards.py`:

```python
import json
from pathlib import Path

from tools.showme_lib.notion_cards import normalize_card_page

FIXTURES = Path(__file__).parent / "fixtures" / "showme"


def test_normalize_card_minimal():
    page = json.loads((FIXTURES / "card_sample.json").read_text())
    card = normalize_card_page(page, video_pages_by_id={})

    assert card.card_id == "array-modifier"
    assert card.label == "Array Modifier 이해"
    assert card.icon == "repeat-2"
    assert card.category == "modifier"
    assert card.weeks == [3, 4]
    assert card.priority == "P0"
    assert card.status == "published"
    assert card.widget_id == "array-modifier"
    assert card.has_widget is True
    assert card.blender_version == "5.0"
    assert card.official_docs.startswith("https://docs.blender.org/")
    assert len(card.steps) == 1
    assert card.steps[0].n == 1
    assert card.steps[0].hotkey == "Shift + A"
    assert card.videos == []
    assert card.prerequisites == []
    assert card.related == []


def test_normalize_card_empty_widget_id():
    page = json.loads((FIXTURES / "card_sample.json").read_text())
    page["properties"]["widget_id"]["rich_text"] = []
    card = normalize_card_page(page, video_pages_by_id={})
    assert card.widget_id is None
    assert card.has_widget is False


def test_normalize_card_no_steps():
    page = json.loads((FIXTURES / "card_sample.json").read_text())
    page["properties"]["steps_json"]["rich_text"] = []
    card = normalize_card_page(page, video_pages_by_id={})
    assert card.steps == []
    assert card.has_steps is False
```

- [ ] **Step 3: Run test to verify it fails**

Run: `pytest tests/test_showme_notion_cards.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'tools.showme_lib.notion_cards'`

- [ ] **Step 4: Implement normalizer**

`tools/showme_lib/notion_cards.py`:

```python
"""Notion Card DB page → Card dataclass normalization."""
from __future__ import annotations

import json
from typing import Any

from .types import Card, Step, Video


def _plain_text(rich_text_list: list[dict]) -> str:
    if not rich_text_list:
        return ""
    return "".join(part.get("plain_text", "") for part in rich_text_list)


def _title(prop: dict) -> str:
    return _plain_text(prop.get("title", []))


def _select(prop: dict) -> str | None:
    sel = prop.get("select")
    return sel.get("name") if sel else None


def _multi_select_ints(prop: dict) -> list[int]:
    return [int(opt["name"]) for opt in prop.get("multi_select", []) if opt["name"].isdigit()]


def _url(prop: dict) -> str | None:
    return prop.get("url")


def _relation_ids(prop: dict) -> list[str]:
    return [rel["id"] for rel in prop.get("relation", [])]


def _opt_text(prop: dict) -> str | None:
    txt = _plain_text(prop.get("rich_text", []))
    return txt or None


def _parse_steps(raw_json: str) -> list[Step]:
    if not raw_json:
        return []
    data = json.loads(raw_json)
    return [
        Step(
            n=s["n"],
            action=s["action"],
            hotkey=s.get("hotkey"),
            menu=s.get("menu"),
            screenshot=s.get("screenshot"),
            note=s.get("note"),
        )
        for s in data.get("steps", [])
    ]


def normalize_card_page(page: dict[str, Any], video_pages_by_id: dict[str, Video]) -> Card:
    props = page["properties"]
    steps_raw = _plain_text(props.get("steps_json", {}).get("rich_text", []))
    video_ids = _relation_ids(props.get("videos_relation", {}))
    videos = [video_pages_by_id[vid] for vid in video_ids if vid in video_pages_by_id]

    return Card(
        card_id=_title(props["card_id"]),
        label=_plain_text(props["label"].get("rich_text", [])),
        icon=_plain_text(props["icon"].get("rich_text", [])),
        category=_select(props.get("category", {})) or "modeling",
        weeks=_multi_select_ints(props.get("week", {})),
        priority=_select(props.get("priority", {})) or "P2",
        status=_select(props.get("status", {})) or "draft",
        concept_md=_plain_text(props.get("concept_md", {}).get("rich_text", [])),
        usage_md=_plain_text(props.get("usage_md", {}).get("rich_text", [])),
        pitfall_md=_plain_text(props.get("pitfall_md", {}).get("rich_text", [])),
        steps=_parse_steps(steps_raw),
        videos=videos,
        widget_id=_opt_text(props.get("widget_id", {})),
        blender_version=_plain_text(props.get("blender_version", {}).get("rich_text", [])) or "5.0",
        official_docs=_url(props.get("official_docs", {})),
        prerequisites=_relation_ids(props.get("prerequisites", {})),
        related=_relation_ids(props.get("related", {})),
    )
```

- [ ] **Step 5: Run test to verify it passes**

Run: `pytest tests/test_showme_notion_cards.py -v`
Expected: 3 passed

- [ ] **Step 6: Commit**

```bash
git add tools/showme_lib/notion_cards.py tests/fixtures/showme/card_sample.json tests/test_showme_notion_cards.py
git commit -m "feat(showme): Notion Card page normalizer + fixture-driven tests"
```

---

### Task 4: 신규 HTML 템플릿 (퀴즈 제거, steps 탭 추가)

**Files:**
- Create: `course-site/assets/showme/_template.v2.html`

기존 `_template.html`(약 800줄)을 복사 후 변형. 퀴즈 탭/JS 제거, steps 탭 추가, 영상 섹션 추가. 치환 placeholder는 `{{CONCEPT_HTML}}`, `{{STEPS_HTML}}`, `{{USAGE_HTML}}`, `{{PITFALL_HTML}}`, `{{VIDEOS_HTML}}`, `{{WIDGET_SCRIPT}}`, `{{LABEL}}`, `{{DOCS_URL}}`.

- [ ] **Step 1: Read existing template head + tab section**

Run: `wc -l course-site/assets/showme/_template.html`
Expected: 700-900 lines reported.

Run: `grep -n "tabs\|panel\|initQuiz\|postMessage" course-site/assets/showme/_template.html | head -40`
Expected: 탭 nav, panel section, initQuiz 함수 위치 확인.

- [ ] **Step 2: Copy template as v2**

Run: `cp course-site/assets/showme/_template.html course-site/assets/showme/_template.v2.html`
Expected: 새 파일 생성됨.

- [ ] **Step 3: Replace tab nav**

Edit `course-site/assets/showme/_template.v2.html`. Locate `<nav class="tabs">` block and replace with:

```html
<nav class="tabs">
  <button class="tab active" data-tab="concept">개념</button>
  <button class="tab" data-tab="steps" data-conditional="has-steps">따라하기</button>
  <button class="tab" data-tab="interaction" data-conditional="has-widget">인터랙션</button>
  <button class="tab" data-tab="usage">언제 쓰나요</button>
  <button class="tab" data-tab="videos" data-conditional="has-videos">영상</button>
</nav>
```

- [ ] **Step 4: Replace panel sections**

Replace all `<section class="panel" ...>` blocks with 5 placeholder panels:

```html
<section class="panel active" data-panel="concept">
  {{CONCEPT_HTML}}
</section>

<section class="panel" data-panel="steps">
  {{STEPS_HTML}}
</section>

<section class="panel" data-panel="interaction">
  {{WIDGET_HTML}}
</section>

<section class="panel" data-panel="usage">
  {{USAGE_HTML}}
  {{PITFALL_HTML}}
</section>

<section class="panel" data-panel="videos">
  {{VIDEOS_HTML}}
</section>
```

- [ ] **Step 5: Remove quiz JS**

Locate `function initQuiz()` and the `postMessage({ type: "showme-quiz-complete" ...})` calls. Delete the entire `initQuiz` function definition and its invocation (often `document.addEventListener('DOMContentLoaded', initQuiz)` or similar). Keep tab-switching JS intact.

- [ ] **Step 6: Add conditional tab/panel hide JS**

At the end of the `<script>` block (before `</script>`), append:

```javascript
// Hide tabs/panels that lack content (data-conditional flags injected by builder)
(function hideConditional() {
  document.querySelectorAll('[data-conditional]').forEach(el => {
    const flag = el.dataset.conditional;
    if (!document.body.classList.contains(flag)) {
      el.style.display = 'none';
      const panelKey = el.dataset.tab;
      if (panelKey) {
        const panel = document.querySelector(`[data-panel="${panelKey}"]`);
        if (panel) panel.style.display = 'none';
      }
    }
  });
})();
```

- [ ] **Step 7: Add widget script include placeholder**

Just before `</body>`, add:

```html
{{WIDGET_SCRIPT}}
```

- [ ] **Step 8: Update <title>**

Change `<title>Show Me — [위젯 제목]</title>` to `<title>Show Me — {{LABEL}}</title>`.

- [ ] **Step 9: Add doc-ref footer placeholder**

If the existing template has a doc-ref footer, replace its URL/text with `{{DOCS_HTML}}`. Builder will emit `<a class="doc-ref" href="...">Blender Docs</a>` or empty string.

- [ ] **Step 10: Validate HTML structure**

Run: `python3 -c "from html.parser import HTMLParser; HTMLParser().feed(open('course-site/assets/showme/_template.v2.html').read()); print('parse OK')"`
Expected: `parse OK` (no exception).

- [ ] **Step 11: Verify placeholders present**

Run: `grep -c "{{" course-site/assets/showme/_template.v2.html`
Expected: 8 or more (one per placeholder).

- [ ] **Step 12: Commit**

```bash
git add course-site/assets/showme/_template.v2.html
git commit -m "feat(showme): v2 template — quiz removed, steps/videos tabs added"
```

---

### Task 5: HTML 렌더러

**Files:**
- Create: `tools/showme_lib/renderer.py`
- Create: `tests/fixtures/showme/expected_concept.html` (snippet)
- Create: `tests/test_showme_renderer.py`

- [ ] **Step 1: Write failing test for concept rendering**

`tests/test_showme_renderer.py`:

```python
from tools.showme_lib.renderer import render_concept_html, render_steps_html, render_videos_html, render_card_html
from tools.showme_lib.types import Card, Step, Video


def _make_card(**overrides) -> Card:
    base = dict(
        card_id="array-modifier",
        label="Array Modifier 이해",
        icon="repeat-2",
        category="modifier",
        weeks=[3],
        priority="P0",
        status="published",
        concept_md="복사기처럼 **규칙적**으로 반복.",
        usage_md="볼트, 척추 같은 구조.",
        pitfall_md="Origin 위치 확인.",
        steps=[Step(n=1, action="Cube 추가", hotkey="Shift + A", menu="Add → Mesh → Cube", screenshot=None, note=None)],
        videos=[Video(title="X", url="https://youtube.com/y", channel="Blender Studio", duration_sec=480, language="en", blender_version="5.0", official=True, recommended_reason="공식")],
        widget_id="array-modifier",
        blender_version="5.0",
        official_docs="https://docs.blender.org/array",
        prerequisites=[],
        related=[],
    )
    base.update(overrides)
    return Card(**base)


def test_concept_renders_markdown_bold():
    html = render_concept_html(_make_card())
    assert "<strong>규칙적</strong>" in html
    assert "복사기처럼" in html


def test_steps_renders_hotkey_kbd():
    html = render_steps_html(_make_card())
    assert "<kbd>Shift + A</kbd>" in html
    assert "Cube 추가" in html
    assert "Add → Mesh → Cube" in html


def test_videos_renders_official_badge():
    html = render_videos_html(_make_card())
    assert "공식" in html
    assert 'href="https://youtube.com/y"' in html
    assert "Blender Studio" in html


def test_full_card_html_has_label_in_title():
    template = "<title>Show Me — {{LABEL}}</title><body class=\"{{BODY_CLASSES}}\">{{CONCEPT_HTML}}{{STEPS_HTML}}{{WIDGET_HTML}}{{USAGE_HTML}}{{PITFALL_HTML}}{{VIDEOS_HTML}}{{WIDGET_SCRIPT}}{{DOCS_HTML}}</body>"
    html = render_card_html(_make_card(), template=template)
    assert "<title>Show Me — Array Modifier 이해</title>" in html
    assert "has-widget" in html
    assert "has-steps" in html
    assert "has-videos" in html


def test_card_without_widget_has_no_widget_flag():
    template = "<body class=\"{{BODY_CLASSES}}\"></body>"
    html = render_card_html(_make_card(widget_id=None), template=template)
    assert "has-widget" not in html
    assert "has-steps" in html


def test_card_without_steps_no_steps_flag():
    template = "<body class=\"{{BODY_CLASSES}}\"></body>"
    html = render_card_html(_make_card(steps=[]), template=template)
    assert "has-steps" not in html
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_showme_renderer.py -v`
Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Implement renderer (minimal markdown subset)**

`tools/showme_lib/renderer.py`:

```python
"""Card → HTML renderer. Minimal markdown subset (bold, italic, paragraphs, links)."""
from __future__ import annotations

import html
import re

from .types import Card


_BOLD = re.compile(r"\*\*(.+?)\*\*")
_ITALIC = re.compile(r"(?<!\*)\*([^*]+?)\*(?!\*)")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def _md_to_html(md: str) -> str:
    if not md.strip():
        return ""
    # paragraphs split by blank line
    paragraphs = [p.strip() for p in md.split("\n\n") if p.strip()]
    out = []
    for p in paragraphs:
        escaped = html.escape(p)
        escaped = _BOLD.sub(r"<strong>\1</strong>", escaped)
        escaped = _ITALIC.sub(r"<em>\1</em>", escaped)
        escaped = _LINK.sub(r'<a href="\2">\1</a>', escaped)
        out.append(f"<p>{escaped}</p>")
    return "\n".join(out)


def render_concept_html(card: Card) -> str:
    return f'<div class="card-concept">{_md_to_html(card.concept_md)}</div>'


def render_steps_html(card: Card) -> str:
    if not card.steps:
        return ""
    items = []
    for step in card.steps:
        parts = [f'<span class="step-n">{step.n}</span>', f'<span class="step-action">{html.escape(step.action)}</span>']
        if step.hotkey:
            parts.append(f'<kbd>{html.escape(step.hotkey)}</kbd>')
        if step.menu:
            parts.append(f'<span class="step-menu">{html.escape(step.menu)}</span>')
        if step.note:
            parts.append(f'<span class="step-note">{html.escape(step.note)}</span>')
        body = " ".join(parts)
        if step.screenshot:
            body += f'<img class="step-screenshot" src="{html.escape(step.screenshot)}" alt="">'
        items.append(f'<li class="step-item">{body}</li>')
    return f'<ol class="steps-list">{"".join(items)}</ol>'


def render_usage_html(card: Card) -> str:
    if not card.usage_md.strip():
        return ""
    return f'<div class="card-usage"><h3>언제 쓰나요</h3>{_md_to_html(card.usage_md)}</div>'


def render_pitfall_html(card: Card) -> str:
    if not card.pitfall_md.strip():
        return ""
    return f'<div class="card-pitfall"><h3>흔한 실수</h3>{_md_to_html(card.pitfall_md)}</div>'


def render_videos_html(card: Card) -> str:
    if not card.videos:
        return ""
    items = []
    for v in card.videos:
        badge = '<span class="badge badge-official">공식</span>' if v.official else ''
        items.append(
            f'<li class="video-item">'
            f'<a href="{html.escape(v.url)}" target="_blank" rel="noopener">{html.escape(v.title)}</a>'
            f' {badge}'
            f'<div class="video-meta">{html.escape(v.channel)} · {v.duration_sec // 60}분 · Blender {html.escape(v.blender_version)}</div>'
            f'<div class="video-reason">{html.escape(v.recommended_reason)}</div>'
            f'</li>'
        )
    return f'<ul class="videos-list">{"".join(items)}</ul>'


def render_widget_html(card: Card) -> str:
    if not card.has_widget:
        return ""
    return f'<div class="widget-mount" data-widget="{html.escape(card.widget_id)}"></div>'


def render_widget_script(card: Card) -> str:
    if not card.has_widget:
        return ""
    return f'<script src="widgets/{html.escape(card.widget_id)}.js" defer></script>'


def render_docs_html(card: Card) -> str:
    if not card.official_docs:
        return ""
    return f'<a class="doc-ref" href="{html.escape(card.official_docs)}" target="_blank" rel="noopener">Blender Docs</a>'


def _body_classes(card: Card) -> str:
    flags = []
    if card.has_widget:
        flags.append("has-widget")
    if card.has_steps:
        flags.append("has-steps")
    if card.has_videos:
        flags.append("has-videos")
    return " ".join(flags)


def render_card_html(card: Card, template: str) -> str:
    substitutions = {
        "{{LABEL}}": html.escape(card.label),
        "{{BODY_CLASSES}}": _body_classes(card),
        "{{CONCEPT_HTML}}": render_concept_html(card),
        "{{STEPS_HTML}}": render_steps_html(card),
        "{{WIDGET_HTML}}": render_widget_html(card),
        "{{USAGE_HTML}}": render_usage_html(card),
        "{{PITFALL_HTML}}": render_pitfall_html(card),
        "{{VIDEOS_HTML}}": render_videos_html(card),
        "{{WIDGET_SCRIPT}}": render_widget_script(card),
        "{{DOCS_HTML}}": render_docs_html(card),
    }
    out = template
    for k, v in substitutions.items():
        out = out.replace(k, v)
    return out
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_showme_renderer.py -v`
Expected: 6 passed

- [ ] **Step 5: Commit**

```bash
git add tools/showme_lib/renderer.py tests/test_showme_renderer.py
git commit -m "feat(showme): HTML renderer with markdown subset + conditional flags"
```

---

### Task 6: Registry / Catalog 재생성

**Files:**
- Create: `tools/showme_lib/index.py`
- Create: `tests/test_showme_index.py`

`_registry.js`(JS object literal) + `_catalog.json`을 카드 리스트로부터 재생성.

- [ ] **Step 1: Write failing test**

`tests/test_showme_index.py`:

```python
import json

from tools.showme_lib.index import build_registry_js, build_catalog_json
from tools.showme_lib.types import Card


def _card(card_id: str, label: str, icon: str, weeks: list[int], category: str = "modifier", status: str = "published") -> Card:
    return Card(
        card_id=card_id, label=label, icon=icon, category=category, weeks=weeks,
        priority="P1", status=status, concept_md="", usage_md="", pitfall_md="",
        steps=[], videos=[], widget_id=None, blender_version="5.0",
        official_docs=None, prerequisites=[], related=[],
    )


def test_registry_emits_js_object():
    cards = [
        _card("array-modifier", "Array Modifier 이해", "repeat-2", [3, 4]),
        _card("mirror", "Mirror Modifier", "flip-horizontal", [3]),
    ]
    js = build_registry_js(cards)
    assert js.startswith("const SHOWME_REGISTRY")
    assert '"array-modifier"' in js
    assert '"Array Modifier 이해"' in js
    assert '"repeat-2"' in js
    assert "week: [3, 4]" in js or '"week": [3, 4]' in js


def test_registry_skips_deprecated():
    cards = [
        _card("a", "A", "x", [1], status="published"),
        _card("b", "B", "y", [1], status="deprecated"),
    ]
    js = build_registry_js(cards)
    assert '"a"' in js
    assert '"b"' not in js


def test_catalog_groups_by_category():
    cards = [
        _card("array-modifier", "Array", "x", [3], category="modifier"),
        _card("extrude", "Extrude", "x", [3], category="edit-mode"),
        _card("mirror", "Mirror", "x", [3], category="modifier"),
    ]
    catalog = json.loads(build_catalog_json(cards))
    assert catalog["categoryMap"]["modifier"] == ["array-modifier", "mirror"]
    assert catalog["categoryMap"]["edit-mode"] == ["extrude"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_showme_index.py -v`
Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Implement index**

`tools/showme_lib/index.py`:

```python
"""Regenerate _registry.js and _catalog.json from Card list."""
from __future__ import annotations

import json

from .types import Card


_HEADER = """// ============================================================
// Show Me 위젯 레지스트리 — DO NOT EDIT BY HAND
// Generated from Notion Card DB by tools/showme_build.py
// ============================================================
"""


def _published(cards: list[Card]) -> list[Card]:
    return [c for c in cards if c.status != "deprecated"]


def build_registry_js(cards: list[Card]) -> str:
    entries = []
    for c in _published(cards):
        weeks = ", ".join(str(w) for w in c.weeks)
        entry = (
            f'  "{c.card_id}": {{ '
            f'label: "{c.label}", '
            f'icon: "{c.icon}", '
            f'week: [{weeks}], '
            f'category: "{c.category}" '
            f'}}'
        )
        entries.append(entry)
    body = ",\n".join(entries)
    return f"{_HEADER}\nconst SHOWME_REGISTRY = {{\n{body}\n}};\n"


def build_catalog_json(cards: list[Card]) -> str:
    category_map: dict[str, list[str]] = {}
    for c in _published(cards):
        category_map.setdefault(c.category, []).append(c.card_id)
    for ids in category_map.values():
        ids.sort()
    return json.dumps({"categoryMap": category_map}, ensure_ascii=False, indent=2)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_showme_index.py -v`
Expected: 3 passed

- [ ] **Step 5: Commit**

```bash
git add tools/showme_lib/index.py tests/test_showme_index.py
git commit -m "feat(showme): regenerate _registry.js + _catalog.json from cards"
```

---

### Task 7: Build CLI entry

**Files:**
- Create: `tools/showme_build.py`

- [ ] **Step 1: Sanity-check token + DB ids loader exists**

Run: `python3 -c "from tools.notion_api import get_notion_token; print(get_notion_token()[:5])"`
Expected: 5 글자 출력 (token 앞부분). 토큰 미설정 시 환경 변수 안내.

- [ ] **Step 2: Write CLI script**

`tools/showme_build.py`:

```python
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

    # registry + catalog는 항상 전체 카드 기준
    REGISTRY_PATH.write_text(build_registry_js(all_cards), encoding="utf-8")
    CATALOG_PATH.write_text(build_catalog_json(all_cards), encoding="utf-8")
    print(f"\nregenerated {REGISTRY_PATH.relative_to(ROOT)}")
    print(f"regenerated {CATALOG_PATH.relative_to(ROOT)}")
    print(f"total: {len(targets)} card(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 3: Syntax check**

Run: `python3 -c "import ast; ast.parse(open('tools/showme_build.py').read()); print('syntax OK')"`
Expected: `syntax OK`

- [ ] **Step 4: Dry-run help**

Run: `python3 tools/showme_build.py --help`
Expected: argparse help text shows `--card`, `--week`, `--all`.

- [ ] **Step 5: Commit**

```bash
git add tools/showme_build.py
git commit -m "feat(showme): showme_build CLI — Notion → HTML + registry + catalog"
```

---

### Task 8: `/showme-build` 스킬 정의

**Files:**
- Create: `.claude/commands/showme-build.md`

- [ ] **Step 1: Inspect existing skill format**

Run: `head -40 .claude/commands/showme/SKILL.md`
Expected: 스킬 frontmatter + 호출 가이드 형식 확인.

- [ ] **Step 2: Write skill definition**

`.claude/commands/showme-build.md`:

```markdown
---
name: showme-build
description: |
  Notion Card DB → ShowMe HTML 생성. 단일 카드/주차/전체 모드.
  카드 1개: /showme-build {card_id}
  주차 전체: /showme-build week N
  전체: /showme-build all
  사용 시점: Notion에서 카드 수정 후 사이트 발행 전, 새 카드 생성 후, 마이그레이션 후.
---

# /showme-build

Notion **ShowMe Cards** DB를 SSoT로 두고, 각 row를 `course-site/assets/showme/{card_id}.html` 로 빌드한다. 파생 인덱스 `_registry.js`, `_catalog.json` 도 함께 재생성.

## 호출 방식

- `/showme-build {card_id}` — 단일 카드. 예: `/showme-build array-modifier`
- `/showme-build week {N}` — 주차 N의 모든 카드. 예: `/showme-build week 3`
- `/showme-build all` — 전체 published 카드

## 실행 흐름

1. `tools/showme_db_ids.json` 존재 확인. 없으면 사용자에게 `tools/showme_create_dbs.py` 먼저 실행 안내.
2. argument 매칭에 따라 적절한 `python3 tools/showme_build.py` 명령 구성:
   - `{card_id}` → `--card {card_id}`
   - `week {N}` → `--week {N}`
   - `all` → `--all`
3. 실행. 출력 로그를 그대로 보여줌.
4. 오류 시 그대로 표기. 422 / 401 / 404 의 경우 토큰 또는 DB id 점검 안내.

## 사전 조건

- `NOTION_TOKEN` 환경변수 또는 `tools/notion-mapping.json` 의 token 필드 설정
- `tools/showme_db_ids.json` 존재 (없으면 `showme_create_dbs.py` 부트스트랩 필요)
- `course-site/assets/showme/_template.v2.html` 존재

## 후속

빌드 후 `/sync` 또는 `/rpd-check` 로 사이트 발행 + 검증.
```

- [ ] **Step 3: Verify file**

Run: `head -10 .claude/commands/showme-build.md`
Expected: frontmatter `name`, `description` 보임.

- [ ] **Step 4: Commit**

```bash
git add .claude/commands/showme-build.md
git commit -m "feat(showme): /showme-build skill definition"
```

---

### Task 9: 파일럿 카드 (`collection-outliner`) End-to-end

이 태스크는 Phase 1 검증이 핵심. Notion DB가 만들어진 상태에서 신규 카드 1개를 작성하고, 빌드해서 결과물을 확인한다.

**Files:**
- Modify: Notion `ShowMe Cards` DB (새 row 추가)
- Create: `course-site/assets/showme/collection-outliner.html` (빌드 결과물)

- [ ] **Step 1: Verify DB ids loaded**

Run: `cat tools/showme_db_ids.json`
Expected: `cards_db_id`, `videos_db_id` 두 UUID 출력.

- [ ] **Step 2: Create Notion row via MCP**

IMPLEMENTER NOTE: Use the `mcp__ed9f2562-...__notion-create-pages` tool to create a row. The parent is the `cards_db_id`. The properties must match the 4장 schema.

Properties (paste into MCP create-pages call):
- `card_id` (title): `collection-outliner`
- `label`: `Collection 과 Outliner 이해`
- `icon`: `folder-tree`
- `category`: `object`
- `week`: `[3]`
- `priority`: `P0`
- `status`: `draft`
- `concept_md`:
  ```
  Collection은 **폴더**처럼 오브젝트를 묶는 단위예요. Outliner는 그 폴더 구조를 보여주는 트리.

  로봇처럼 파츠가 많은 모델은 머리/몸통/팔다리를 Collection으로 분리하면 가시성, 선택 잠금, 일괄 조작이 쉬워져요.
  ```
- `usage_md`:
  ```
  파츠 수가 많아질 때, 좌우 대칭 작업 중 한쪽만 숨기고 싶을 때, 렌더에서 일부만 제외하고 싶을 때.
  ```
- `pitfall_md`:
  ```
  Outliner 눈 아이콘은 **뷰포트 가시성**, 모니터 아이콘은 **렌더 가시성**이에요. 헷갈리면 렌더에서 사라져요.
  ```
- `steps_json`:
  ```json
  {"blender_version":"5.0","platform_note":null,"steps":[
    {"n":1,"action":"Outliner에서 빈 공간 우클릭","hotkey":null,"menu":"New Collection","screenshot":null,"note":null},
    {"n":2,"action":"오브젝트 선택 후 Collection으로 이동","hotkey":"M","menu":"Move to Collection","screenshot":null,"note":null},
    {"n":3,"action":"뷰포트 가시성 토글","hotkey":null,"menu":"눈 아이콘 클릭","screenshot":null,"note":"H 단축키도 동일"},
    {"n":4,"action":"선택 잠금","hotkey":null,"menu":"화살표 아이콘 클릭","screenshot":null,"note":"실수로 움직이는 방지"}
  ]}
  ```
- `widget_id`: (빈값)
- `blender_version`: `5.0`
- `official_docs`: `https://docs.blender.org/manual/en/latest/scene_layout/collections/index.html`

- [ ] **Step 3: Run build for this card**

Run: `python3 tools/showme_build.py --card collection-outliner`
Expected:
```
  wrote course-site/assets/showme/collection-outliner.html

regenerated course-site/assets/showme/_registry.js
regenerated course-site/assets/showme/_catalog.json
total: 1 card(s)
```

- [ ] **Step 4: Verify HTML output structure**

Run: `python3 -c "from html.parser import HTMLParser; HTMLParser().feed(open('course-site/assets/showme/collection-outliner.html').read()); print('parse OK')"`
Expected: `parse OK`

Run: `grep -c "Collection은" course-site/assets/showme/collection-outliner.html`
Expected: `1` (concept body in output)

Run: `grep -c "<kbd>M</kbd>" course-site/assets/showme/collection-outliner.html`
Expected: `1` (hotkey rendered)

Run: `grep -c "has-widget" course-site/assets/showme/collection-outliner.html`
Expected: `0` (no widget for this card)

Run: `grep -c "has-steps" course-site/assets/showme/collection-outliner.html`
Expected: `1` (steps present)

Run: `grep -c "initQuiz" course-site/assets/showme/collection-outliner.html`
Expected: `0` (퀴즈 코드 부재 검증)

- [ ] **Step 5: Visual check via static server**

Run: `python3 tools/serve-static.py &` then open `http://localhost:8000/course-site/assets/showme/collection-outliner.html` in browser.
Expected: 4 탭(개념/따라하기/언제쓰나요) 보임, 인터랙션·영상 탭 숨김, 퀴즈 없음.

Stop server: `kill %1` (or matching PID).

- [ ] **Step 6: Verify _registry.js updated**

Run: `grep -c "collection-outliner" course-site/assets/showme/_registry.js`
Expected: `1`

- [ ] **Step 7: Verify _catalog.json updated**

Run: `python3 -c "import json; d=json.load(open('course-site/assets/showme/_catalog.json')); print('collection-outliner' in d['categoryMap'].get('object', []))"`
Expected: `True`

- [ ] **Step 8: Commit generated artifacts**

```bash
git add course-site/assets/showme/collection-outliner.html course-site/assets/showme/_registry.js course-site/assets/showme/_catalog.json
git commit -m "feat(showme): pilot card collection-outliner via DB → HTML build"
```

---

### Task 10: 기존 카드 충돌 회귀 확인

기존 79 카드는 손대지 않았지만, `_registry.js` 와 `_catalog.json` 이 빌드로 재생성되었으므로 기존 카드 항목이 빠지지 않았는지 확인.

- [ ] **Step 1: Compare card counts**

Run: `ls course-site/assets/showme/*.html | grep -v "_template\|collection-outliner" | wc -l`
Expected: 79 (기존 카드 수)

- [ ] **Step 2: Verify all old cards still in registry**

NOTE: 이 단계는 **현 빌드 동작 한계**를 노출한다 — 빌드가 DB만 기준으로 registry를 재생성하면 DB에 없는 기존 79 카드가 registry에서 사라진다. 이는 의도된 동작이 아니다. 마이그레이션 전까지는 기존 카드도 registry에 보존되어야 한다.

Run: `grep -c '"array-modifier"' course-site/assets/showme/_registry.js`
Expected (기대 동작): `1`
Actual (현재 빌드): `0` — **Bug discovered**

- [ ] **Step 3: Write failing regression test**

`tests/test_showme_index.py` 에 추가:

```python
def test_registry_merges_legacy_entries(tmp_path):
    """DB에 없는 기존 카드 항목은 _registry.js에 보존되어야 한다."""
    from tools.showme_lib.index import build_registry_js_merged

    legacy_path = tmp_path / "legacy.js"
    legacy_path.write_text(
        'const SHOWME_REGISTRY = {\n  "array-modifier": { label: "Array", icon: "x", week: [3] }\n};\n'
    )
    cards = [_card("new-card", "New", "y", [1])]
    js = build_registry_js_merged(cards, legacy_path=legacy_path)
    assert '"array-modifier"' in js
    assert '"new-card"' in js
```

- [ ] **Step 4: Run test to verify it fails**

Run: `pytest tests/test_showme_index.py::test_registry_merges_legacy_entries -v`
Expected: FAIL (function not defined)

- [ ] **Step 5: Implement merged variant**

Add to `tools/showme_lib/index.py`:

```python
import re
from pathlib import Path


_LEGACY_ENTRY = re.compile(r'"([a-z0-9-]+)":\s*\{[^}]+\}', re.DOTALL)


def _parse_legacy_registry(path: Path) -> dict[str, str]:
    """Extract { card_id: entry_literal } from existing _registry.js."""
    if not path.exists():
        return {}
    text = path.read_text()
    return {m.group(1): m.group(0) for m in _LEGACY_ENTRY.finditer(text)}


def build_registry_js_merged(cards: list[Card], legacy_path: Path) -> str:
    legacy = _parse_legacy_registry(legacy_path)
    db_ids = {c.card_id for c in _published(cards)}

    entries: list[str] = []
    for c in _published(cards):
        weeks = ", ".join(str(w) for w in c.weeks)
        entries.append(
            f'  "{c.card_id}": {{ '
            f'label: "{c.label}", '
            f'icon: "{c.icon}", '
            f'week: [{weeks}], '
            f'category: "{c.category}" '
            f'}}'
        )
    # legacy 카드 보존 (DB에 아직 마이그레이션 안 된 항목)
    for legacy_id, literal in legacy.items():
        if legacy_id not in db_ids:
            entries.append(f"  {literal}")

    body = ",\n".join(entries)
    return f"{_HEADER}\nconst SHOWME_REGISTRY = {{\n{body}\n}};\n"
```

- [ ] **Step 6: Update showme_build.py to call merged variant**

Edit `tools/showme_build.py`. Replace:

```python
from showme_lib.index import build_catalog_json, build_registry_js
```

with:

```python
from showme_lib.index import build_catalog_json, build_registry_js_merged
```

And replace:

```python
REGISTRY_PATH.write_text(build_registry_js(all_cards), encoding="utf-8")
```

with:

```python
REGISTRY_PATH.write_text(build_registry_js_merged(all_cards, REGISTRY_PATH), encoding="utf-8")
```

- [ ] **Step 7: Run test**

Run: `pytest tests/test_showme_index.py -v`
Expected: 4 passed (3 original + 1 new merge test)

- [ ] **Step 8: Rebuild and verify legacy preserved**

Run: `python3 tools/showme_build.py --card collection-outliner`
Then: `grep -c '"array-modifier"' course-site/assets/showme/_registry.js`
Expected: `1` (legacy preserved)

Also: `grep -c '"collection-outliner"' course-site/assets/showme/_registry.js`
Expected: `1` (new card added)

- [ ] **Step 9: Apply same merge strategy to catalog**

Add to `tools/showme_lib/index.py`:

```python
def build_catalog_json_merged(cards: list[Card], legacy_path: Path) -> str:
    legacy_catalog: dict[str, list[str]] = {}
    if legacy_path.exists():
        legacy_catalog = json.loads(legacy_path.read_text()).get("categoryMap", {})

    db_ids = {c.card_id for c in _published(cards)}
    category_map: dict[str, list[str]] = {}
    for c in _published(cards):
        category_map.setdefault(c.category, []).append(c.card_id)

    # preserve legacy entries not yet in DB
    for cat, ids in legacy_catalog.items():
        for legacy_id in ids:
            if legacy_id not in db_ids:
                category_map.setdefault(cat, []).append(legacy_id)

    for ids in category_map.values():
        ids.sort()
    return json.dumps({"categoryMap": category_map}, ensure_ascii=False, indent=2)
```

- [ ] **Step 10: Wire catalog merge into build**

Edit `tools/showme_build.py`. Replace the catalog write line:

```python
CATALOG_PATH.write_text(build_catalog_json(all_cards), encoding="utf-8")
```

with:

```python
CATALOG_PATH.write_text(build_catalog_json_merged(all_cards, CATALOG_PATH), encoding="utf-8")
```

Update import:

```python
from showme_lib.index import build_catalog_json_merged, build_registry_js_merged
```

- [ ] **Step 11: Final verification**

Run: `python3 tools/showme_build.py --card collection-outliner`

Run: `python3 -c "import json; d=json.load(open('course-site/assets/showme/_catalog.json')); print(len([c for cs in d['categoryMap'].values() for c in cs]))"`
Expected: `80` (79 legacy + 1 new)

- [ ] **Step 12: Commit merge logic**

```bash
git add tools/showme_lib/index.py tools/showme_build.py tests/test_showme_index.py course-site/assets/showme/_registry.js course-site/assets/showme/_catalog.json
git commit -m "fix(showme): preserve legacy registry/catalog entries during incremental build"
```

---

## Self-Review Notes

**Spec coverage**:
- ✓ Card DB schema (Task 2)
- ✓ Videos DB schema (Task 2)
- ✓ Template v2 with no quiz (Task 4)
- ✓ Renderer (Task 5)
- ✓ Indices (Tasks 6, 10)
- ✓ CLI (Task 7)
- ✓ Skill definition (Task 8)
- ✓ Pilot card end-to-end (Task 9)
- ✓ Legacy preservation (Task 10) — uncovered gap caught during self-review

**Out of scope (follow-up plans needed)**:
- Phase 2 — 백로그 8개 작성: `2026-05-XX-card-ssot-phase2.md`
- Phase 3 — 79 카드 마이그레이션 자동화: `2026-05-XX-card-ssot-phase3-migration.md`
- Phase 4 — Week 페이지 인라인 정리: `2026-05-XX-card-ssot-phase4-week-cleanup.md`
- Phase 5 — 퀴즈 코드 cleanup + `/brainstormC` deprecate: `2026-05-XX-card-ssot-phase5-cleanup.md`
- `week.html` 모달의 sidecar/탭 렌더 로직 확장 — v2 템플릿이 자체적으로 모든 탭을 들고 있어 모달 코드 변경 불요. 단 퀴즈 완료 핸들러 제거는 Phase 5에서.

**Placeholder scan**: No TBDs, no "implement later". All code blocks complete.

**Type consistency**: `Card` / `Step` / `Video` dataclasses defined in Task 1, used unchanged in Tasks 3, 5, 6, 7.

**Risks acknowledged**:
- Notion API 토큰 미설정 시 Task 2 step 5에서 실패. 사용자 안내 명시.
- Phase 1 종료 시점에 DB에는 카드 1개만 있음. 빌드 `--all` 호출 시 79 카드 HTML이 변경되지 않으나 registry/catalog는 머지로 보존.
