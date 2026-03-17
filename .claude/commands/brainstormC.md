---
description: "showme 카드 보충 설명 생성. 예: /brainstormC extrude, /brainstormC list"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

## Context

- 현재 supplements: !`node -e "try{var s=require('./course-site/assets/showme/_supplements.json');console.log(Object.keys(s).length+' 개')}catch(e){console.log('0 개')}" 2>/dev/null`
- 현재 showme 카드: !`ls course-site/assets/showme/*.html 2>/dev/null | grep -v _template | wc -l | tr -d ' '`개

## 인자

`$ARGUMENTS`

---

## 모드 분기

**인자가 `list`**: 기존 supplement 목록 출력. `_supplements.json` 읽어서 각 항목의 id, title, targets 출력.

**인자가 위젯 ID 하나 이상**: 각 ID에 대해 보충 설명 생성. ID가 여러 개면 순서대로 처리.

**인자 없음**: 사용법 안내 출력.

---

## 보충 설명 생성 절차

### 1. 대상 카드 분석

`course-site/assets/showme/{widget-id}.html` 읽어서:
- 개념이해 탭(`#panel-concept`) 내 핵심 내용 파악
- 학생들이 헷갈릴 만한 지점 식별

### 2. 비유 판단

**비유 소스 후보**: 요리, 일상 사물, 게임, 디지털 경험

**선택 기준 (모두 충족해야 사용)**:
- 비유가 개념의 핵심 동작을 정확히 반영하는가?
- 학생이 비유 소스를 확실히 알 만한가?
- 설명이 자연스럽게 읽히는가?

**하나라도 아니면 `analogy: null`** — before/after + takeaway만으로 충분.

### 3. 콘텐츠 작성 기준

**before_after**:
- `before`: 이 기능 없이 작업하면 어떻게 되는지 (결과 기준)
- `after`: 이 기능을 쓰면 어떻게 달라지는지 (결과 기준)
- 두 항목 모두 한 문장 이내

**takeaway**: 핵심 한 문장. "~다" 로 끝나는 평서문.

**금지**:
- 억지스러운 비유 (비유보다 설명이 더 복잡하면 안 됨)
- 과장된 표현 ("엄청난", "완벽한")
- AI가 생성한 티 나는 문체 ("~하는 것이 중요합니다", "~에 유의하세요")
- 공식 홈페이지 링크 언급 (supplement 카드에서는 제외)

### 4. 두 파일에 저장

**`_supplements.js`** 에 항목 추가:
```javascript
"widget-id": {
  title: "아직 헷갈린다면?",
  analogy: { source: "카테고리", emoji: "이모지", headline: "제목", body: "설명" },
  // 또는 analogy: null,
  before_after: { before: "...", after: "..." },
  takeaway: "핵심 한 문장.",
  targets: ["widget-id"]
},
```

**`_supplements.json`** 에 동일 데이터 추가 (JSON 형식).

두 파일이 항상 동기화 상태여야 함.

### 5. 검증

JSON 유효성 확인:
```bash
node -e "JSON.parse(require('fs').readFileSync('./course-site/assets/showme/_supplements.json','utf8')); console.log('OK')"
```

targets에 지정된 카드 HTML이 실제로 존재하는지 확인:
```bash
ls course-site/assets/showme/{widget-id}.html
```

### 6. 결과 출력

생성된 supplement 내용을 보여주고, 두 파일 업데이트 완료 메시지 출력.

---

## 참조 파일

| 파일 | 역할 |
|------|------|
| `course-site/assets/showme/_supplements.js` | 보충 데이터 (JS, 프론트엔드) |
| `course-site/assets/showme/_supplements.json` | 보충 데이터 (JSON, Notion sync) |
| `course-site/assets/showme/_registry.js` | 위젯 메타데이터 |
| `course-site/assets/showme/{id}.html` | 대상 showme 카드 |
