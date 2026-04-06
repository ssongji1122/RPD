---
description: "Show Me 교육 카드 생성. 예: /showme array-modifier, /showme list, /showme verify. DO NOT use for: 카드 내용 질문, 기존 카드 수정(Edit 사용), 보충 설명(/brainstormC 사용)"
model: opus
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(python3 -m http.server:*), Bash(curl:*), Bash(wc:*), Bash(ls:*), Agent
---

> **품질 철학**: 학생이 이 카드 하나로 해당 개념을 **정확히 이해하고 즉시 실습**할 수 있어야 한다. 정보 나열이 아니라 인지 부하를 최소화한 학습 경험을 만든다.

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

**필수 구조** (4탭): → [references/template.md](references/template.md) 참조

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

#### Step 3.5: 품질 게이트

생성된 카드를 배포 전에 검증한다. → [references/card-quality.md](references/card-quality.md) 참조

1. **자가 검증**: 품질 기준 체크리스트를 순회하며 pass/fail 판정
2. **실패 항목 수정**: fail 항목이 있으면 해당 부분만 수정 후 재검증
3. **최대 2회 재시도**: 2회 수정 후에도 fail이면 실패 사유를 로그에 기록하고 진행
4. **통과 기준**: "기술 완성도" 5개는 필수 통과, 나머지는 80% 이상 통과

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

### CSS 레퍼런스

→ [references/css-reference.md](references/css-reference.md) 참조

### 병렬 생성 (여러 카드)

카드 간 의존성이 없으므로 Agent 도구로 병렬 실행 가능.
각 에이전트에게 전달할 프롬프트에 반드시 포함:
1. 이 스킬의 "새 카드 생성 표준 절차" 전체
2. `mirror-modifier.html` 전체 내용 (CSS 복사용)
3. 해당 Blender 기능의 개념/단축키/사용 사례

### 참조 파일

→ [references/template.md](references/template.md) 참조

## 실행 로그
실행 완료 시 아래 형식으로 기록:
```bash
echo "[$(date '+%Y-%m-%d %H:%M')] mode=$MODE target=$TARGET result=$RESULT quality=$QUALITY" >> .claude/skill-logs/showme.log
```
- `result`: `success` | `fail(reason)` | `skip(reason)`
- `quality`: `PASS` | `FAIL(reason)` | `N/A` (verify/list 모드)

## Gotchas
> 이 스킬 실행 중 발견된 함정들. 새 함정 발견 시 아래에 자동 추가한다.
> 형식: `- **{날짜}** {증상} → {원인} → {해결}`

- (아직 없음)
