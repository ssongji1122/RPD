# Card SSoT Phase 2 — 백로그 카드 8개 작성 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** "ShowMe 신규 카드 보강 계획" (Notion page 32754d65-4971-81fc-b832-f8cbb3388e66) 백로그 8개 카드를 신규 SSoT 시스템(Notion Card DB + showme_build.py)으로 작성하고 사이트에 빌드한다.

**Architecture:** Phase 1 인프라 그대로 활용. 각 카드 = Notion Cards DB row 1개. 콘텐츠는 사용자 검수 후 published 상태. 위젯 코드는 카드별로 작성 가능하나 P0 단계는 텍스트+steps만 우선.

**Tech Stack:** Notion MCP (create-pages), `tools/showme_build.py`, 기존 Phase 1 라이브러리.

**Scope:** Phase 2만. Phase 3 (79카드 마이그레이션) · Phase 4 (Week 페이지 정리) · Phase 5 (cleanup)는 별도 plan.

**카드 목록 (백로그 우선순위):**

P0 (이번 plan):
1. `collection-outliner` — 이미 Phase 1 파일럿으로 작성됨. 콘텐츠 보강만.
2. `modifier-stack-order` — Mirror, Subdivision, Bevel, Weighted Normal 순서 차이 + Apply 타이밍
3. `shade-smooth-auto-smooth` — Flat / Shade Smooth / Auto Smooth by Angle 차이
4. `merge-by-distance` — 겹친 버텍스 정리, Boolean/Extrude 실수 복구
5. `bridge-edge-loops` — 두 열린 루프 연결 토폴로지

P1 (이번 plan 후반):
6. `duplicate-vs-linked-duplicate`
7. `face-orientation-normals`
8. `apply-modifier-vs-keep-procedural`

**File Structure:**
- New: Notion DB rows (1 per card)
- New: `tests/fixtures/showme/cards/{card_id}.json` (Notion-shape fixture for snapshot regression)
- Updated: `course-site/assets/showme/{card_id}.html` (built artifacts)
- Updated: `course-site/assets/showme/_registry.js`, `_catalog.json` (re-merged)
- Updated: `tests/test_showme_snapshot.py` (add per-card snapshot assertions)

위젯 코드 (Canvas/Three.js)는 이 phase에서 선택. P0 카드 중 시각적 비교 효과가 큰 `modifier-stack-order`, `shade-smooth-auto-smooth`만 위젯 작성 권장 (별도 task).

---

### Task 1: Content draft for all 8 cards (사용자 검수)

**Files:**
- Create: `docs/superpowers/specs/2026-05-19-phase2-card-drafts.md` (drafts for user review)

이 task는 콘텐츠 작성 task. 8개 카드 본문(concept/usage/pitfall/steps) 초안을 markdown으로 작성. 사용자 검수 후 다음 task에서 Notion으로 푸시.

- [ ] **Step 1: Write the draft document**

Create `docs/superpowers/specs/2026-05-19-phase2-card-drafts.md` with 8 card drafts. Each card draft has:

- `card_id`, `label`, `icon` (Lucide name), `category`, `week` (multi-select), `priority`, `status`
- `concept_md`: 비유 + 핵심 개념 (2-3 paragraphs, 한국어, **bold** 강조 키워드)
- `usage_md`: 언제 쓰는지 (1-2 sentences)
- `pitfall_md`: 흔한 실수 + 해결 (2-3 sentences)
- `steps_json`: Blender 5.0 절차 step JSON (3-6 steps per card)
- `widget_id`: null (P0는 위젯 없음. modifier-stack-order, shade-smooth는 Task 5에서 위젯 추가)
- `official_docs`: Blender 5.0 docs URL

Use Week 03 Notion page (31354d65-4971-8193-a446-f3b9d02fb790) for cross-reference of existing analogies/wording. Reuse the "레고 블록" / "사포" / "필름 필터" 비유 family for consistency.

For `modifier-stack-order`:
```
concept_md: |
  Modifier는 **요리 레시피**처럼 위에서 아래로 순서대로 계산돼요.
  **같은 재료라도 넣는 순서가 다르면 맛이 달라져요.**

  Mirror → Boolean → Subdivision 이 가장 안전한 시작 순서.
  Mirror가 먼저 좌우 대칭을 잡고, Boolean이 구멍을 뚫고,
  Subdivision이 마지막에 부드럽게 만들어요.

usage_md: |
  여러 Modifier를 같이 쓸 때, 결과가 의도와 다를 때 순서를 점검.

pitfall_md: |
  Subdivision을 먼저 넣고 Boolean을 하면 곡면이 깨져서 지저분해져요.
  **Subdivision은 거의 항상 마지막 또는 끝에서 두 번째.**

steps_json:
  - n: 1, action: "Modifier Stack에서 핸들(::) 잡기", hotkey: null, menu: null
  - n: 2, action: "위/아래 화살표로 순서 변경", hotkey: null, menu: "Move Up/Down"
  - n: 3, action: "Mirror가 가장 위", hotkey: null, menu: null
  - n: 4, action: "Subdivision은 가장 아래", hotkey: null, menu: null

official_docs: https://docs.blender.org/manual/en/latest/modeling/modifiers/introduction.html#order-of-modifiers
```

(이런 형식으로 8개 카드 모두 작성)

- [ ] **Step 2: User review gate**

Pause. Tell user: "8개 카드 초안 작성 완료. `docs/superpowers/specs/2026-05-19-phase2-card-drafts.md` 검토 후 OK 주시면 Notion으로 푸시."

DO NOT proceed without explicit user approval. 콘텐츠 품질이 학생 학습 결과 좌우. 임의 진행 금지.

- [ ] **Step 3: Commit draft**

```bash
git add docs/superpowers/specs/2026-05-19-phase2-card-drafts.md
git commit -m "docs(showme): Phase 2 card drafts for user review"
```

---

### Task 2: Push approved cards to Notion DB

**Tool:** Notion MCP `notion-create-pages` (data_source_id = `f5b0d619-a7ff-4734-93cf-8a304b336d3f`)

- [ ] **Step 1: For each approved card draft**

Use `mcp__ed9f2562-...__notion-create-pages` with parent `{type: "data_source_id", data_source_id: "f5b0d619-a7ff-4734-93cf-8a304b336d3f"}`. Properties match Phase 1 schema.

Card `collection-outliner` already exists (Notion page 36454d65-4971-817e-a665-c900d9960073) — UPDATE via `notion-update-page` instead of creating a new row. Promote status to `published` and refine content from the approved draft.

- [ ] **Step 2: Verify rows**

Fetch the Cards DB and confirm 8 rows exist with status=`published` (or `draft` if user wants staging). Use `notion-search` or query via the data source.

- [ ] **Step 3: Capture per-card fixtures**

For each card, save a Notion-page-shape JSON fixture to `tests/fixtures/showme/cards/{card_id}.json`. These fixtures power Phase 2 snapshot tests (Task 4) and let future tests run offline.

The fixture is the Notion API response shape — easiest to construct by hand from the approved draft (faster than fetching live).

- [ ] **Step 4: Commit fixtures**

```bash
git add tests/fixtures/showme/cards/
git commit -m "test(showme): Phase 2 card fixtures (8 cards)"
```

---

### Task 3: Build all 8 cards via showme_build.py

- [ ] **Step 1: Set NOTION_TOKEN env var**

```bash
export NOTION_TOKEN=<your-integration-token>
```

NOTE TO IMPLEMENTER: The token must be obtainable from Notion integrations settings or from `tools/notion-mapping.json` (existing convention). If `tools/notion_api.py:get_notion_token()` returns None, fall back to MCP-based normalize → render (see Phase 1 Task 9 pattern at `tools/showme_pilot_local.py` for the inline approach).

- [ ] **Step 2: Run build**

```bash
python3 tools/showme_build.py --all
```

Expected: 8 cards → `course-site/assets/showme/{card_id}.html` written; `_registry.js` and `_catalog.json` re-merged with legacy 79 + new 8.

If `NOTION_TOKEN` unset, write a local pilot script (mirror of Phase 1 `showme_pilot_local.py`) reading from the fixtures in `tests/fixtures/showme/cards/`.

- [ ] **Step 3: Verify HTML output**

For each card:
- `python3 -c "from html.parser import HTMLParser; HTMLParser().feed(open('course-site/assets/showme/{id}.html').read()); print('OK')"`
- `grep -c "initQuiz" course-site/assets/showme/{id}.html` → 0
- `grep -c "has-steps" course-site/assets/showme/{id}.html` → ≥1

- [ ] **Step 4: Commit built artifacts**

```bash
git add course-site/assets/showme/{collection-outliner,modifier-stack-order,shade-smooth-auto-smooth,merge-by-distance,bridge-edge-loops,duplicate-vs-linked-duplicate,face-orientation-normals,apply-modifier-vs-keep-procedural}.html course-site/assets/showme/_registry.js course-site/assets/showme/_catalog.json
git commit -m "feat(showme): Phase 2 — 8 backlog cards built from Notion"
```

---

### Task 4: Snapshot regression tests

**File:**
- Modify: `tests/test_showme_snapshot.py`

Add a snapshot test per card that loads the fixture from `tests/fixtures/showme/cards/{card_id}.json` and asserts key substrings.

- [ ] **Step 1: Parameterized test**

Append to `tests/test_showme_snapshot.py`:

```python
import json as _json
import pytest

from pathlib import Path as _Path

FIXTURES_DIR = _Path(__file__).parent / "fixtures" / "showme" / "cards"


@pytest.mark.parametrize("card_id", [
    "collection-outliner",
    "modifier-stack-order",
    "shade-smooth-auto-smooth",
    "merge-by-distance",
    "bridge-edge-loops",
    "duplicate-vs-linked-duplicate",
    "face-orientation-normals",
    "apply-modifier-vs-keep-procedural",
])
def test_phase2_card_renders(card_id):
    fixture_path = FIXTURES_DIR / f"{card_id}.json"
    page = _json.loads(fixture_path.read_text())
    card = normalize_card_page(page, video_pages_by_id={})
    template = TEMPLATE.read_text()
    html = render_card_html(card, template)

    assert card_id in html or card.label in html
    assert "<body class=\"" in html
    assert "initQuiz" not in html
    assert "<title>Show Me — " in html
```

- [ ] **Step 2: Run tests**

```bash
/Users/ssongji/Developer/Workspace/RPD/.tmp/ci-verify-venv/bin/pytest tests/test_showme_snapshot.py -v
```

Expected: 10 passed (2 from Phase 1 + 8 new).

- [ ] **Step 3: Commit**

```bash
git add tests/test_showme_snapshot.py
git commit -m "test(showme): Phase 2 snapshot regression for 8 cards"
```

---

### Task 5: Widget for `modifier-stack-order` (optional)

This task is optional and can be deferred to Phase 2.5. The widget shows side-by-side comparison of identical Modifier list with different stack orders.

If implementing:
- Create `course-site/assets/showme/widgets/modifier-stack-order.js`
- Update the Notion row to set `widget_id` = `modifier-stack-order`
- Re-run build to regenerate HTML with `has-widget` body class + `<script src=...>` include
- The widget mounts into `.widget-mount` div, renders two canvases showing pre/post-Boolean Subdivision difference

Skip if Phase 2 should land without widgets. The other 7 P0/P1 cards stay text+steps only.

---

### Task 6: Site smoke test

- [ ] **Step 1: Local serve**

```bash
python3 tools/serve-static.py &
SERVE_PID=$!
sleep 2
```

- [ ] **Step 2: Smoke check 3 cards via browser preview tool**

Open in preview:
- `http://localhost:8000/course-site/assets/showme/collection-outliner.html`
- `http://localhost:8000/course-site/assets/showme/modifier-stack-order.html`
- `http://localhost:8000/course-site/assets/showme/shade-smooth-auto-smooth.html`

For each:
- Verify 4 visible tabs (no 인터랙션 tab if no widget): 개념 / 따라하기 / 언제 쓰나요
- Tab switching works
- Concept body bold renders
- Steps have `<kbd>` chips
- No console errors

If issue found, fix the template or renderer, re-build affected cards, re-verify.

- [ ] **Step 3: Stop server**

```bash
kill $SERVE_PID
```

- [ ] **Step 4: Commit any fixes from smoke**

If any fix needed, commit separately:

```bash
git add <files>
git commit -m "fix(showme): Phase 2 — <specific issue> from smoke test"
```

---

### Task 7: Update Phase 1 plan reference

- [ ] **Step 1: Append Phase 2 outcome to Phase 1 plan**

Append to `docs/superpowers/plans/2026-05-18-card-ssot-phase1.md` end:

```markdown
---

## Phase 2 Outcome (2026-05-XX)

8 backlog cards published. Plan: `2026-05-19-card-ssot-phase2-backlog.md`. Notion DB now has 9 rows. Next: Phase 3 migration of 79 legacy cards.
```

- [ ] **Step 2: Commit**

```bash
git add docs/superpowers/plans/2026-05-18-card-ssot-phase1.md
git commit -m "docs(showme): link Phase 2 outcome to Phase 1 plan"
```

---

## Self-Review Notes

**Spec coverage**: Phase 2 plan covers `ShowMe 신규 카드 보강 계획` Notion backlog (page 32754d65) priority P0 + P1.

**Out of scope (Phase 3+ separate plans)**:
- 79 legacy ShowMe HTML migration to DB
- Week 페이지 인라인 정리 (Notion side)
- 퀴즈 코드 cleanup in legacy HTML files
- `_supplements.json` deprecation

**Risks**:
- Content quality bottleneck: 8 cards × ~200 words each = ~1600 words of curated Korean Blender content. User review gate (Task 1 Step 2) is the highest-friction step. Plan separately blocks here.
- Notion API rate limit: 8 page creates = trivial, no concern.
- Widget complexity: Task 5 marked optional precisely because it's a side quest.

**Estimated effort**: 6-10 hours
- Task 1 (content drafts): 3-4 hr (8 cards × 20-30 min research+writing)
- Task 2 (Notion push): 30 min (MCP calls)
- Task 3 (build): 15 min
- Task 4 (snapshot tests): 30 min
- Task 5 (widget, optional): 2-3 hr if attempted
- Task 6 (smoke): 30 min
- Task 7 (docs): 5 min
