# Supplement System Design

**날짜**: 2026-03-17
**상태**: 승인됨

## 목적

학생들이 showme 카드의 개념 이해 탭을 봤는데도 헷갈릴 때, 추가 보충 설명(비유 + before/after + 핵심 한 줄)을 제공하는 시스템.

## 핵심 결정

| 항목 | 결정 |
|------|------|
| 비유 개수 | 1개 (개념에 가장 맞는 것 자동 선택), 억지스러우면 생략 |
| 콘텐츠 구성 | 비유(선택) + before/after + 핵심 한 줄 |
| 접근 방식 | 개념이해 탭 하단 accordion ("아직 헷갈린다면?") |
| 데이터 저장 | `_supplements.js` (재사용 가능, 플러그앤플레이) |
| 렌더링 | 부모 페이지(week.html)에서 iframe DOM에 주입 → 기존 카드 수정 불필요 |
| Notion 연동 | 기존 notion-sync 확장, 토글 블록으로 자동 삽입 |

## 1. 데이터 구조 — `_supplements.js`

**위치**: `course-site/assets/showme/_supplements.js`

```javascript
const SHOWME_SUPPLEMENTS = {
  "supplement-id": {
    title: "아직 헷갈린다면?",
    analogy: {                          // 비유가 억지스러우면 null
      source: "요리|일상|게임|디지털",   // 비유 소스 카테고리
      emoji: "🍕",
      headline: "비유 제목",
      body: "비유 설명"
    },
    before_after: {
      before: "이 기능 없이 하면 어떻게 되는지",
      after: "이 기능을 쓰면 어떻게 달라지는지"
    },
    takeaway: "핵심 한 줄 요약",
    targets: ["card-id-1", "card-id-2"]  // 여러 카드에서 재사용 가능
  }
};
```

### 필드 규칙

- `analogy`: 자연스러운 비유가 있을 때만 사용. 억지스러우면 `null`로 두고 before/after + takeaway만으로 구성.
- `targets`: 같은 보충이 여러 카드에 표시될 수 있음 (예: "메시 흐름" 보충 → subdivision, loop-cut, bevel 카드 모두).
- `title`: 기본값 "아직 헷갈린다면?" — 필요 시 커스터마이징 가능.

## 2. 렌더링 — 부모 페이지에서 iframe DOM 주입

showme 카드는 `week.html` 및 `library.html`에서 iframe으로 로드됨. 같은 origin이므로 부모가 iframe DOM을 직접 조작 가능.

### 흐름

```
week.html (부모)
  ├─ <script src="assets/showme/_supplements.js">
  └─ iframe: extrude.html
       └─ #panel-concept
            ├─ [기존 개념 카드들]
            └─ [accordion] ← 부모가 iframe.onload에서 삽입
```

### 주입 로직 (week.html / library.html에 추가)

```javascript
iframe.addEventListener("load", function() {
  var wid = /* 현재 카드 widget-id */;
  var doc = iframe.contentDocument;
  if (!doc || !window.SHOWME_SUPPLEMENTS) return;

  // targets 배열에 wid가 포함된 supplement 찾기
  var supplement = null;
  for (var key in SHOWME_SUPPLEMENTS) {
    if (SHOWME_SUPPLEMENTS[key].targets.indexOf(wid) !== -1) {
      supplement = SHOWME_SUPPLEMENTS[key];
      break;
    }
  }
  if (!supplement) return;

  var panel = doc.getElementById("panel-concept");
  if (!panel) return;

  // accordion HTML 생성 및 삽입
  var accordion = buildSupplementAccordion(supplement);
  panel.appendChild(accordion);
});
```

### Accordion UI

- 닫힌 상태: "💡 아직 헷갈린다면?" 버튼만 보임
- 클릭 시 펼침: 비유(있으면) + before/after + takeaway
- 스타일: 기존 `.tip-box` 계열과 통일된 다크 테마

## 3. Notion 연동 — `week_to_notion_blocks()` 확장

`tools/notion_api.py`의 `week_to_notion_blocks()` 함수 확장:

### 변경 사항

1. `_supplements.js` 데이터를 Python에서 읽을 수 있도록 JSON 파싱 또는 별도 `_supplements.json` 생성
2. step에 `showme` 필드가 있으면 → 매칭되는 supplement 찾기
3. 있으면 → Notion 토글 블록으로 삽입:

```
heading_3: Step 제목
paragraph: Step 설명
  ▶ toggle: "아직 헷갈린다면?"
    paragraph: 비유 (있으면)
    paragraph: Before → After
    paragraph: 핵심 한 줄
```

### 듀얼 포맷 옵션

`_supplements.js` (JS) + `_supplements.json` (동일 데이터, Python용)을 동기화하거나,
스킬이 생성할 때 두 파일 모두 업데이트.

## 4. `/brainstormC` 스킬

**위치**: `.claude/commands/brainstormC.md`

### 사용법

```
/brainstormC extrude
/brainstormC subdivision-surface loop-cut   # 병렬 생성
/brainstormC list                            # 기존 supplement 목록
```

### 동작

1. 해당 showme 카드 HTML 읽기 (개념 파악)
2. Blender 공식 문서 참고
3. 최적 비유 소스 자동 선택 (요리/일상/게임/디지털) — 자연스럽지 않으면 비유 생략
4. before/after + takeaway 작성
5. `_supplements.js`에 항목 추가
6. `_supplements.json` 동기화 (Notion용)
7. 공식 홈페이지 링크 하단 mention 포함

### 비유 선택 가이드라인 (스킬 내장)

- 비유가 개념을 정확히 설명하는지 검증
- 학생이 비유 소스를 모를 가능성이 있으면 다른 소스 선택
- **억지스러운 비유는 넣지 않는다** — before/after만으로 충분한 경우가 많음

## 5. 영향 범위

### 새로 생성하는 파일

| 파일 | 역할 |
|------|------|
| `course-site/assets/showme/_supplements.js` | 보충 데이터 (JS) |
| `course-site/assets/showme/_supplements.json` | 보충 데이터 (Python/Notion용) |
| `.claude/commands/brainstormC.md` | 보충 생성 스킬 |

### 수정하는 파일

| 파일 | 변경 내용 |
|------|-----------|
| `course-site/week.html` | `_supplements.js` 로드 + iframe onload 주입 로직 |
| `course-site/library.html` | 동일한 주입 로직 |
| `tools/notion_api.py` | `week_to_notion_blocks()`에 supplement 토글 블록 추가 |

### 수정하지 않는 파일

- 기존 showme 카드 58개 — 변경 없음
- `_registry.js` — 변경 없음
- `_template.html` — 변경 없음 (새 카드용으로 supplement 로더 추가는 선택사항)
