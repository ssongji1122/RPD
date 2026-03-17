# Supplement System Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** showme 카드 개념이해 탭 하단에 보충 설명 accordion을 주입하는 시스템 구축

**Architecture:** `_supplements.js`에 보충 데이터 저장 → 부모 페이지(week.html, library.html)가 iframe onload 시 매칭되는 데이터를 accordion으로 주입 → Notion sync 시 토글 블록으로 변환. `/brainstormC` 스킬로 콘텐츠 생성.

**Tech Stack:** Vanilla JS (프론트), Python stdlib (Notion sync), Claude skill markdown

**Design doc:** `docs/plans/2026-03-17-supplement-system-design.md`

---

### Task 1: `_supplements.js` 데이터 파일 생성

**Files:**
- Create: `course-site/assets/showme/_supplements.js`

**Step 1: 빈 데이터 구조 생성**

```javascript
// ============================================================
// Show Me 보충 설명 데이터
// 개념이해 탭 하단 "아직 헷갈린다면?" accordion에 표시
// targets 배열로 여러 카드에서 재사용 가능
// ============================================================

var SHOWME_SUPPLEMENTS = {
  // /brainstormC 스킬로 항목 추가
  // 구조:
  // "supplement-id": {
  //   title: "아직 헷갈린다면?",
  //   analogy: { source: "요리|일상|게임|디지털", emoji: "🍕", headline: "...", body: "..." } | null,
  //   before_after: { before: "...", after: "..." },
  //   takeaway: "핵심 한 줄",
  //   targets: ["card-id-1", "card-id-2"]
  // }
};
```

**Step 2: Commit**

```bash
git add course-site/assets/showme/_supplements.js
git commit -m "feat: add _supplements.js data file for showme supplement system"
```

---

### Task 2: `_supplements.json` 듀얼 포맷 파일 생성

**Files:**
- Create: `course-site/assets/showme/_supplements.json`

**Step 1: 빈 JSON 생성**

```json
{}
```

이 파일은 `_supplements.js`와 동일한 데이터를 JSON으로 유지. `/brainstormC` 스킬이 두 파일 모두 업데이트.

**Step 2: Commit**

```bash
git add course-site/assets/showme/_supplements.json
git commit -m "feat: add _supplements.json for Notion sync compatibility"
```

---

### Task 3: `buildSupplementAccordion()` 함수 + week.html 주입 로직

**Files:**
- Modify: `course-site/week.html`

**Step 1: `_supplements.js` 스크립트 태그 추가**

`week.html`에서 `_registry.js` 로드하는 부분 바로 아래에 추가:

```html
<script src="assets/showme/_supplements.js"></script>
```

찾을 위치: `<script src="assets/showme/_registry.js"></script>` 바로 아래

**Step 2: `buildSupplementAccordion()` 함수 작성**

week.html의 `<script>` 블록 내, `openShowMe()` 함수 앞에 추가:

```javascript
// ─── Supplement Accordion Builder ──────────────
function findSupplementForWidget(wid) {
  if (typeof SHOWME_SUPPLEMENTS === "undefined") return null;
  for (var key in SHOWME_SUPPLEMENTS) {
    var s = SHOWME_SUPPLEMENTS[key];
    if (s.targets && s.targets.indexOf(wid) !== -1) return s;
  }
  return null;
}

function buildSupplementAccordion(doc, supplement) {
  var wrap = doc.createElement("div");
  wrap.style.cssText = "margin-top:20px;border:1px solid rgba(245,158,11,.18);border-radius:18px;overflow:hidden;background:rgba(245,158,11,.04);";

  var toggle = doc.createElement("button");
  toggle.style.cssText = "display:flex;align-items:center;gap:8px;width:100%;padding:14px 16px;border:none;background:none;color:#fbbf24;font:inherit;font-size:.88rem;font-weight:600;cursor:pointer;text-align:left;";
  toggle.textContent = "💡 " + (supplement.title || "아직 헷갈린다면?");

  var arrow = doc.createElement("span");
  arrow.style.cssText = "margin-left:auto;transition:transform .2s;font-size:.8rem;";
  arrow.textContent = "▼";
  toggle.appendChild(arrow);

  var content = doc.createElement("div");
  content.style.cssText = "display:none;padding:0 16px 16px;";

  var open = false;
  toggle.addEventListener("click", function() {
    open = !open;
    content.style.display = open ? "block" : "none";
    arrow.style.transform = open ? "rotate(180deg)" : "";
  });

  // Analogy (있으면)
  if (supplement.analogy) {
    var analogyDiv = doc.createElement("div");
    analogyDiv.style.cssText = "margin-bottom:12px;padding:12px 14px;border-radius:12px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.06);";

    var headlineEl = doc.createElement("div");
    headlineEl.style.cssText = "font-size:.9rem;font-weight:600;color:#f5f5f7;margin-bottom:6px;";
    headlineEl.textContent = (supplement.analogy.emoji || "") + " " + supplement.analogy.headline;

    var bodyEl = doc.createElement("div");
    bodyEl.style.cssText = "font-size:.85rem;color:#d4d4d8;line-height:1.7;";
    bodyEl.textContent = supplement.analogy.body;

    analogyDiv.appendChild(headlineEl);
    analogyDiv.appendChild(bodyEl);
    content.appendChild(analogyDiv);
  }

  // Before / After
  if (supplement.before_after) {
    var baDiv = doc.createElement("div");
    baDiv.style.cssText = "display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px;";

    var beforeDiv = doc.createElement("div");
    beforeDiv.style.cssText = "padding:12px;border-radius:12px;background:rgba(239,68,68,.06);border:1px solid rgba(239,68,68,.15);";
    var beforeLabel = doc.createElement("div");
    beforeLabel.style.cssText = "font-size:.76rem;font-weight:600;color:#fca5a5;margin-bottom:4px;text-transform:uppercase;letter-spacing:.04em;";
    beforeLabel.textContent = "WITHOUT";
    var beforeText = doc.createElement("div");
    beforeText.style.cssText = "font-size:.84rem;color:#d4d4d8;line-height:1.6;";
    beforeText.textContent = supplement.before_after.before;
    beforeDiv.appendChild(beforeLabel);
    beforeDiv.appendChild(beforeText);

    var afterDiv = doc.createElement("div");
    afterDiv.style.cssText = "padding:12px;border-radius:12px;background:rgba(16,185,129,.06);border:1px solid rgba(16,185,129,.15);";
    var afterLabel = doc.createElement("div");
    afterLabel.style.cssText = "font-size:.76rem;font-weight:600;color:#6ee7b7;margin-bottom:4px;text-transform:uppercase;letter-spacing:.04em;";
    afterLabel.textContent = "WITH";
    var afterText = doc.createElement("div");
    afterText.style.cssText = "font-size:.84rem;color:#d4d4d8;line-height:1.6;";
    afterText.textContent = supplement.before_after.after;
    afterDiv.appendChild(afterLabel);
    afterDiv.appendChild(afterText);

    baDiv.appendChild(beforeDiv);
    baDiv.appendChild(afterDiv);
    content.appendChild(baDiv);
  }

  // Takeaway
  if (supplement.takeaway) {
    var takeawayDiv = doc.createElement("div");
    takeawayDiv.style.cssText = "padding:10px 14px;border-radius:12px;background:rgba(10,132,255,.08);border:1px solid rgba(10,132,255,.18);font-size:.86rem;color:#8ec5ff;font-weight:500;";
    takeawayDiv.textContent = "→ " + supplement.takeaway;
    content.appendChild(takeawayDiv);
  }

  wrap.appendChild(toggle);
  wrap.appendChild(content);
  return wrap;
}

function injectSupplement(iframe, widgetId) {
  try {
    var doc = iframe.contentDocument;
    if (!doc) return;
    var supplement = findSupplementForWidget(widgetId);
    if (!supplement) return;
    var panel = doc.getElementById("panel-concept");
    if (!panel) return;
    panel.appendChild(buildSupplementAccordion(doc, supplement));
  } catch(e) {}
}
```

**Step 3: `openShowMe()` 함수에 iframe onload 리스너 추가**

`openShowMe()` 함수에서 `iframe.src = ...` 설정 직후에 추가:

```javascript
iframe.onload = function() { injectSupplement(iframe, widgetId); };
```

**Step 4: 브라우저에서 week.html 열어 기존 showme 카드가 정상 동작하는지 확인**

supplement 데이터가 비어있으므로 accordion이 안 보이면 정상.

**Step 5: Commit**

```bash
git add course-site/week.html
git commit -m "feat: add supplement accordion injection to week.html showme modal"
```

---

### Task 4: library.html에 동일한 주입 로직 추가

**Files:**
- Modify: `course-site/library.html`

**Step 1: `_supplements.js` 스크립트 태그 추가**

`library.html`에서 `_registry.js` 로드 바로 아래에:

```html
<script src="assets/showme/_supplements.js"></script>
```

**Step 2: `findSupplementForWidget`, `buildSupplementAccordion`, `injectSupplement` 함수 추가**

library.html의 `<script>` 블록 내, `openShowMe()` 함수 앞에 Task 3 Step 2와 동일한 세 함수를 추가.

**Step 3: library.html의 `openShowMe()` 함수에 onload 추가**

```javascript
// openShowMe 내부, iframe.src 설정 직후:
document.getElementById("showmeIframe").onload = function() {
  injectSupplement(this, widgetId);
};
```

**Step 4: Commit**

```bash
git add course-site/library.html
git commit -m "feat: add supplement accordion injection to library.html"
```

---

### Task 5: Notion sync 확장 — `notion_api.py`

**Files:**
- Modify: `tools/notion_api.py`

**Step 1: supplement JSON 로더 함수 추가**

`notion_api.py` 상단 Constants 영역 아래에:

```python
SUPPLEMENTS_JSON = ROOT / "course-site" / "assets" / "showme" / "_supplements.json"


def load_supplements() -> dict:
    """Load showme supplement data from _supplements.json."""
    if not SUPPLEMENTS_JSON.exists():
        return {}
    with open(SUPPLEMENTS_JSON, encoding="utf-8") as f:
        return json.load(f)


def find_supplement_for_widget(widget_id: str, supplements: dict) -> dict | None:
    """Find a supplement whose targets include the given widget_id."""
    for _key, sup in supplements.items():
        if widget_id in sup.get("targets", []):
            return sup
    return None
```

**Step 2: `week_to_notion_blocks()` 함수에 supplement 토글 블록 추가**

step 처리 루프 내, step의 goal/tasks 블록 이후에 삽입. showme 필드가 있으면 매칭 supplement 찾아서 토글 추가:

```python
# step 처리 루프 내, tasks 이후에 추가:
showme_ids = step.get("showme", [])
if isinstance(showme_ids, str):
    showme_ids = [showme_ids]
supplements = load_supplements()
for sid in showme_ids:
    sup = find_supplement_for_widget(sid, supplements)
    if not sup:
        continue
    # 토글 블록 (children 포함)
    toggle_children = []
    if sup.get("analogy"):
        a = sup["analogy"]
        toggle_children.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {"type": "text", "text": {"content": f"{a.get('emoji', '')} {a['headline']}"}, "annotations": {"bold": True}},
                    {"type": "text", "text": {"content": f"\n{a['body']}"}},
                ]
            }
        })
    if sup.get("before_after"):
        ba = sup["before_after"]
        toggle_children.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {"type": "text", "text": {"content": "❌ Without: "}, "annotations": {"bold": True}},
                    {"type": "text", "text": {"content": ba["before"]}},
                    {"type": "text", "text": {"content": "\n✅ With: "}, "annotations": {"bold": True}},
                    {"type": "text", "text": {"content": ba["after"]}},
                ]
            }
        })
    if sup.get("takeaway"):
        toggle_children.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {"type": "text", "text": {"content": f"→ {sup['takeaway']}"}, "annotations": {"bold": True, "color": "blue"}},
                ]
            }
        })
    if toggle_children:
        blocks.append({
            "object": "block",
            "type": "toggle",
            "toggle": {
                "rich_text": [{"type": "text", "text": {"content": sup.get("title", "아직 헷갈린다면?")}}],
                "children": toggle_children
            }
        })
```

**Step 3: Commit**

```bash
git add tools/notion_api.py
git commit -m "feat: add supplement toggle blocks to Notion sync"
```

---

### Task 6: `/brainstormC` 스킬 생성

**Files:**
- Create: `.claude/commands/brainstormC.md`

**Step 1: 스킬 파일 작성**

```markdown
---
description: "보충 설명 생성. 예: /brainstormC extrude, /brainstormC list"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(wc:*), Bash(ls:*), Bash(node:*), Agent
---

## Context

- 기존 supplements: !`node -e "var s=require('./course-site/assets/showme/_supplements.json');console.log(Object.keys(s).length)" 2>/dev/null || echo 0`개
- 기존 카드: !`ls course-site/assets/showme/*.html 2>/dev/null | grep -v _template | wc -l | tr -d ' '`개

## Task

인자: `$ARGUMENTS`

---

### 모드 분기

**`list`**: 기존 supplement 목록 출력 (targets 매핑 포함)
**`{widget-id}`**: 해당 카드의 보충 설명 생성
**`{id1} {id2} ...`**: 여러 보충 병렬 생성 (각각 독립 에이전트)
**인자 없음**: 이 도움말 출력

---

### 보충 설명 생성 절차

#### Step 1: 대상 카드 분석
1. `course-site/assets/showme/{widget-id}.html` 읽기
2. 개념이해 탭(#panel-concept) 내용 파악
3. 해당 Blender 기능의 핵심 개념 정리

#### Step 2: 비유 소스 선택
가능한 소스: 요리, 일상 사물, 게임, 디지털 경험

**선택 기준**:
- 비유가 개념의 핵심 동작을 정확히 반영하는가?
- 학생이 비유 소스를 확실히 알 만한가?
- **억지스러우면 비유를 넣지 않는다** — before/after + takeaway만으로 충분

#### Step 3: 콘텐츠 작성

**필수 항목**:
- `before_after.before`: 이 기능 없이 하면 어떻게 되는지
- `before_after.after`: 이 기능을 쓰면 어떻게 달라지는지
- `takeaway`: 핵심 한 줄 (한 문장)

**선택 항목**:
- `analogy`: 자연스러운 비유가 있을 때만

**금지 사항**:
- 억지스러운 비유
- 과장된 표현
- AI가 만든 티 나는 문체

#### Step 4: 두 파일에 저장

1. `course-site/assets/showme/_supplements.js` — JS 객체에 항목 추가
2. `course-site/assets/showme/_supplements.json` — 동일 데이터 JSON으로 동기화

**_supplements.js 항목 형식**:
```javascript
"widget-id": {
  title: "아직 헷갈린다면?",
  analogy: { source: "카테고리", emoji: "이모지", headline: "제목", body: "설명" },
  // 또는 analogy: null
  before_after: { before: "...", after: "..." },
  takeaway: "핵심 한 줄",
  targets: ["widget-id"]  // 여러 카드에 해당하면 배열에 추가
},
```

#### Step 5: 검증
- JS 문법 오류 없는지 확인: `node -e "require('./course-site/assets/showme/_supplements.js')"`는 var 선언이므로 대신 JSON 파일로 검증: `node -e "JSON.parse(require('fs').readFileSync('./course-site/assets/showme/_supplements.json','utf8'))"`
- targets에 지정된 카드 HTML이 실제로 존재하는지 확인

### 톤 가이드라인

- 학생에게 말하듯 자연스러운 구어체
- 짧고 명확한 문장
- 전문 용어를 쓸 때는 바로 옆에 쉬운 말로 풀어주기
- 공식 홈페이지 링크가 있으면 하단에 mention으로 포함

### 참조 파일

| 파일 | 역할 |
|------|------|
| `course-site/assets/showme/_supplements.js` | 보충 데이터 (JS) |
| `course-site/assets/showme/_supplements.json` | 보충 데이터 (JSON) |
| `course-site/assets/showme/_registry.js` | 위젯 메타데이터 |
| `course-site/assets/showme/{id}.html` | 대상 showme 카드 |
```

**Step 2: Commit**

```bash
git add .claude/commands/brainstormC.md
git commit -m "feat: add /brainstormC skill for supplement content creation"
```

---

### Task 7: 샘플 supplement 1개 생성으로 E2E 검증

**Files:**
- Modify: `course-site/assets/showme/_supplements.js`
- Modify: `course-site/assets/showme/_supplements.json`

**Step 1: extrude 카드용 샘플 supplement 작성**

`_supplements.js`에 추가하고 `_supplements.json`도 동기화.

**Step 2: 로컬 서버로 week.html 열어서 extrude showme 카드 모달 열기**

- 개념이해 탭 하단에 "💡 아직 헷갈린다면?" accordion이 보이는지 확인
- 클릭하면 펼쳐지고 before/after + takeaway가 표시되는지 확인
- library.html에서도 동일하게 작동하는지 확인

**Step 3: supplement가 없는 카드 (예: mirror-modifier)에서 accordion이 안 보이는지 확인**

**Step 4: Commit**

```bash
git add course-site/assets/showme/_supplements.js course-site/assets/showme/_supplements.json
git commit -m "feat: add sample extrude supplement for E2E verification"
```

---

### Task 8: showme 스킬 문서 업데이트

**Files:**
- Modify: `.claude/commands/showme.md`

**Step 1: showme 스킬에 supplement 관련 참조 추가**

참조 파일 테이블에 추가:

```markdown
| `course-site/assets/showme/_supplements.js` | 보충 설명 데이터 |
| `course-site/assets/showme/_supplements.json` | 보충 데이터 (Notion용) |
```

**Step 2: Commit**

```bash
git add .claude/commands/showme.md
git commit -m "docs: add supplement file references to showme skill"
```
