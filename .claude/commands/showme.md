---
description: "Show Me 교육 카드 생성. 예: /showme array-modifier, /showme list, /showme verify"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(python3 -m http.server:*), Bash(curl:*), Bash(wc:*), Bash(ls:*), Agent
---

## Context

- 워크트리 위치: !`git worktree list 2>/dev/null | head -3`
- 기존 카드 수: !`ls course-site/assets/showme/*.html 2>/dev/null | grep -v _template | wc -l | tr -d ' '`개
- 기존 카드: !`ls course-site/assets/showme/*.html 2>/dev/null | grep -v _template | xargs -I{} basename {} .html | tr '\n' ', '`
- 레지스트리 항목 수: !`grep -c '"label"' course-site/assets/showme/_registry.js 2>/dev/null || echo 0`개

## Task

인자: `$ARGUMENTS`

---

### 모드 분기

**`list`**: 기존 카드 목록 + 레지스트리 미매칭 항목 출력
**`verify`**: 전체 카드 무결성 검증 (initQuiz, postMessage, doc-ref, 4탭)
**`verify {id}`**: 특정 카드 검증
**`{widget-id}`**: 새 카드 생성 (아래 표준 절차)
**`{id1} {id2} ...`**: 여러 카드 병렬 생성 (각각 독립 에이전트)
**인자 없음**: 이 도움말 출력

---

### 카드 단위(granularity) 결정 가이드

**원칙: 1 카드 = 1 학습 단위 (atomic learning unit)**

카드를 새로 만들기 전에 반드시 아래 기준으로 **개별 카드 vs 기존 카드에 포함**을 판단한다.

#### 개별 카드로 만들어야 하는 경우
- **Modifier** (Mirror, Array, Decimate 등): 각각 독립적인 파라미터 체계가 있어 5분+ 학습 필요
- **독립 Mode/Editor** (Sculpt Mode, UV Editor 등): 고유 인터페이스와 워크플로우 보유
- **복잡한 개념** (Origin vs 3D Cursor, Proportional Editing 등): 혼동 빈도가 높아 별도 설명 필요

#### 기존 카드에 묶어야 하는 경우 (개별 카드 X)
- **같은 모드의 도구 패밀리**: Sculpt 브러시(Draw, Grab, Smooth, Clay Strips 등)는 **비교/선택 맥락**에서 의미가 있으므로 `sculpt-basics`, `sculpt-brushes`처럼 묶는다
- **단독으로 5분 분량이 안 되는 도구**: 개별 브러시 하나만으로 1100줄 카드를 채우기 어려움
- **이미 포함된 경우**: `edit-mode-tools`가 Extrude/Loop Cut/Inset/Bevel을 묶은 것처럼, 도구 패밀리 카드가 이미 존재하면 거기에 섹션으로 추가

#### 노션과의 역할 분담
- **ShowMe 카드**: 보편적/재사용 가능한 도구 레퍼런스 (여러 주차에서 참조)
- **노션 주차 페이지**: 해당 주차 맥락에 맞는 상세 설명 + 카드 링크 + 스크린샷 + YouTube
- 애드온(QRemeshify, Instant Meshes 등)은 카드가 아닌 **노션에서만 상세 설명** (Blender 내장이 아니므로 카드 부적합)

#### 판단 플로우
```
새 도구 설명 필요?
  ├─ Modifier/Mode/복잡 개념? → 개별 카드 생성
  ├─ 기존 도구 패밀리에 속함? → 기존 카드에 섹션 추가
  ├─ 외부 애드온? → 노션에서만 설명 (카드 X)
  └─ 단독 5분 분량 안됨? → 기존 카드에 포함 or 노션만
```

---

### 새 카드 생성 표준 절차

#### Step 1: 리서치 브리프 확인

`claudedocs/research/{widget-id}-brief.md` 존재 시 자동 참조:
- **개념탭**: 브리프 §1 공식정의 + §7 비유 활용
- **퀴즈탭**: 브리프 §5 학생혼란포인트에서 문제 출제
- **단축키**: 브리프 §3에서 검증된 단축키 사용
- **흔한 실수**: 브리프 §6 "증상→해결" 활용
- 없으면 → `⚠️ 리서치 브리프가 없습니다. /rpd-research {id} 먼저 실행하면 더 정확한 카드를 만들 수 있어요.`

#### Step 2: 사전 확인
1. `course-site/assets/showme/{widget-id}.html` 이미 존재하는지 확인
2. `_registry.js`에 해당 ID 등록 여부 확인
3. Blender 공식 문서 URL 확인: `https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/{name}.html`

#### Step 3: HTML 생성

**파일 위치**: `course-site/assets/showme/{widget-id}.html`

반드시 `mirror-modifier.html`의 **전체 CSS**를 복사하여 사용 (외부 참조 없이 독립형).

**필수 구조** (4탭):

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{한글 제목}</title>
  <style>
    /* ── 전체 CSS 인라인 (mirror-modifier.html에서 복사) ── */
  </style>
</head>
<body>
  <nav class="tabs" role="tablist">
    <button class="tab is-active" data-tab="concept" role="tab" aria-selected="true">개념 이해</button>
    <button class="tab" data-tab="visual" role="tab" aria-selected="false">interaction</button>
    <button class="tab" data-tab="when" role="tab" aria-selected="false">언제 쓰나요?</button>
    <button class="tab" data-tab="quiz" role="tab" aria-selected="false">퀴즈</button>
  </nav>

  <section class="panel is-active" id="panel-concept" role="tabpanel">...</section>
  <section class="panel" id="panel-visual" role="tabpanel">...</section>
  <section class="panel" id="panel-when" role="tabpanel">...</section>
  <section class="panel" id="panel-quiz" role="tabpanel">...</section>

  <script>
    /* 탭 전환 + initQuiz + postMessage */
  </script>
</body>
</html>
```

#### 탭별 필수 컴포넌트

**탭 1 — 개념 이해**:
- `.concept-grid` > `.concept-card` (2~3개)
  - 각 카드에 `.badge` + 설명 + `.analogy` 비유 박스
- 길거나 부차적인 설명은 `<details class="concept-more"><summary>더보기</summary>...</details>`로 숨김
- 필요하면 개념 시각화 요약(예: before/after, cause-effect, 시나리오 핵심 한 장면)도 이 탭 하단에 함께 배치
- `.shortcut-list` > `.shortcut-row` (주요 단축키 3~5개)
- `.doc-ref` 또는 `.doc-ref-list` (Blender 공식 문서 링크)

**탭 2 — interaction**:
- `.demo-wrap` > `<canvas>` (680x300 권장)
- 파라미터형 기능은 `.modifier-panel` + `input[type="range"]` + `input[type="number"]` + checkbox 조합을 우선 사용
- `.demo-controls` > `.demo-btn` 는 모드 전환이나 Reset 같이 꼭 필요한 경우만 사용
- 문장형 보조 설명은 최소화하고, 꼭 필요한 정보는 작은 카드 2~3개로 요약
- `.demo-hint` 는 조작 안내 한 줄만 남김
- 이 탭에는 `/showme` 스타일의 잘 그려진 HTML 인터랙션만 둠
- 개념 설명용 시각화(before/after, cause-effect, 시나리오 설명)는 탭 1로 이동
- "얇은 벽 / 두꺼운 벽" 같은 프리셋 이름보다 `Thickness`, `Offset`, `Count`, `Bevel Width`처럼 Blender 실제 파라미터명을 그대로 노출
- Canvas에 `requestAnimationFrame` 애니메이션 사용
- 터치 이벤트 지원 (`touchend` with `preventDefault`)

**탭 3 — 언제 쓰나요?**:
- `.usage-grid` > `.usage-card` (2열: 필요할 때 vs 안 필요할 때)
- `.combo-section` > `.combo-grid` > `.combo-card` (추천 조합 2~3개)
- `.tip-box` (팁/주의사항)
- `.doc-ref` (공식 문서 링크)

**탭 4 — 퀴즈**:
- `<div id="quiz-wrap"></div>`
- `initQuiz(questions)` 호출 — 4~5문제
- 각 문제: `{ question, options[], answer(0-indexed), explanation }`
- 75% 이상 통과
- 완료 시 `postMessage` 전송:
```javascript
window.parent.postMessage({
  type: "showme-quiz-complete",
  widgetId: new URLSearchParams(location.search).get("wid"),
  score: score,
  total: questions.length,
  pass: score >= Math.ceil(questions.length * 0.75)
}, "*");
```

#### Step 4: 레지스트리 등록

`course-site/assets/showme/_registry.js`에 추가:
```javascript
"widget-id": { label: "한글 라벨", icon: "이모지" },
```

#### Step 5: curriculum.js 연결 (선택)

해당 주차의 step에 `showme` 필드 추가:
```javascript
// 단일
"showme": "widget-id"
// 복수
"showme": ["widget-id-1", "widget-id-2"]
```

#### Step 6: 검증 체크리스트
- [ ] 파일 존재: `course-site/assets/showme/{id}.html`
- [ ] `initQuiz` 포함
- [ ] `postMessage` 포함
- [ ] `doc-ref` 포함 (공식 문서 링크)
- [ ] `data-tab` 4개 (concept, visual, when, quiz)
- [ ] `_registry.js`에 등록
- [ ] 모바일 반응형 (`@media max-width: 600px`)
- [ ] 터치 이벤트 지원

---

### CSS 변수 레퍼런스

```
--bg: #0a0a0a          --surface: #17181a      --line: rgba(255,255,255,.08)
--key: #0a84ff         --key-soft: #8ec5ff     --success: #10b981
--warn: #f59e0b        --danger: #ef4444       --text: #f5f5f7
--muted: #a1a1aa       --radius-sm: 12px       --radius-md: 18px
```

### CSS 컴포넌트 요약

| 클래스 | 용도 |
|--------|------|
| `.concept-grid` / `.concept-card` | 개념 카드 그리드 |
| `.badge` `.badge-blue/green/amber/red` | 인라인 뱃지 |
| `.analogy` | 비유 설명 박스 (amber) |
| `.shortcut-list` / `.shortcut-row` / `.kbd` | 단축키 목록 |
| `.demo-wrap` / `.demo-controls` / `.demo-btn` | Canvas 데모 영역 |
| `.usage-grid` / `.usage-card` | 사용 사례 2열 |
| `.combo-section` / `.combo-grid` / `.combo-card` | 추천 조합 |
| `.tip-box` | 팁/주의사항 박스 |
| `.doc-ref` / `.doc-ref-list` | 공식 문서 링크 |
| `.compare-table` | 비교 테이블 |
| `.section-divider` | 섹션 구분선 |

### Blender 공식 문서 URL 패턴

| 카테고리 | URL 패턴 |
|----------|----------|
| Generate 모디파이어 | `https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/{name}.html` |
| Mesh 도구 | `https://docs.blender.org/manual/en/latest/modeling/meshes/tools/{tool}.html` |
| Edge 편집 | `https://docs.blender.org/manual/en/latest/modeling/meshes/editing/edge/{tool}.html` |
| Mesh 편집 | `https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/{tool}.html` |

### 병렬 생성 (여러 카드)

카드 간 의존성이 없으므로 Agent 도구로 병렬 실행 가능.
각 에이전트에게 전달할 프롬프트에 반드시 포함:
1. 이 스킬의 "새 카드 생성 표준 절차" 전체
2. `mirror-modifier.html` 전체 내용 (CSS 복사용)
3. 해당 Blender 기능의 개념/단축키/사용 사례

### 참조 파일

| 파일 | 역할 |
|------|------|
| `course-site/assets/showme/_template.html` | 전체 CSS 원본 |
| `course-site/assets/showme/_registry.js` | 위젯 메타데이터 |
| `course-site/assets/showme/mirror-modifier.html` | 표준 참조 카드 (단일 기능) |
| `course-site/assets/showme/edit-mode-tools.html` | 복합 참조 카드 (다중 도구) |
| `course-site/week.html` | 모달 시스템, iframe 임베드 |
| `course-site/data/curriculum.js` | 주차별 showme 필드 |
| `course-site/assets/showme/_supplements.js` | 보충 설명 데이터 (프론트엔드 accordion) |
| `course-site/assets/showme/_supplements.json` | 보충 설명 데이터 (Notion sync용) |

> 보충 설명 생성은 `/brainstormC` 스킬 사용

## 실행 로그
실행 완료 시 아래 형식으로 기록:
```bash
echo "[$(date '+%Y-%m-%d %H:%M')] mode=$MODE result=$RESULT target=$TARGET" >> .claude/skill-logs/showme.log
```

## Gotchas ⚠️
> Claude가 이 스킬을 쓸 때 실수했던 것들. 새 함정 발견 시 여기에 추가.

1. (아직 없음 — 사용하면서 추가)
