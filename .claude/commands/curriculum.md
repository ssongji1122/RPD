---
description: "커리큘럼 관리. 예: /curriculum validate, /curriculum add-week 4, /curriculum status done 1-5, /curriculum sync"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(python3:*), Bash(node:*), Bash(curl:*), Bash(wc:*), Bash(ls:*), Bash(cat:*), Agent
---

## Context

- 프로젝트 루트: !`git rev-parse --show-toplevel 2>/dev/null`
- curriculum.js: !`wc -l course-site/data/curriculum.js 2>/dev/null | awk '{print $1}'`줄
- 전체 주차: !`grep -c '"week"' course-site/data/curriculum.js 2>/dev/null || echo 0`개
- 주차별 상태: !`grep '"status"' course-site/data/curriculum.js 2>/dev/null | head -15`
- 이미지 디렉토리: !`ls -d course-site/assets/images/week* 2>/dev/null | wc -l | tr -d ' '`개
- Admin 서버: !`curl -s -o /dev/null -w "%{http_code}" http://localhost:8765/api/curriculum 2>/dev/null || echo "꺼짐"`

## Task

인자: `$ARGUMENTS`

---

### 모드 분기

---

#### `validate` — 커리큘럼 구조 검증

전체 curriculum.js를 검사하여 문제점을 리포트합니다.

**검증 항목:**
1. **필수 필드 존재**: 각 주차에 `week`, `status`, `title`, `subtitle`, `summary`, `duration`, `topics[]`, `steps[]` 확인
2. **Step 필수 필드**: 각 step에 `title`, `copy`, `goal[]`, `done[]`, `tasks[]` 확인
3. **Task 필수 필드**: 각 task에 `id`, `label` 확인
4. **Task ID 유일성**: 전체에서 `id` 중복 없는지
5. **이미지 참조 유효성**: `step.image`가 있으면 해당 파일 존재 여부
6. **showme 참조 유효성**: `step.showme` 값에 대응하는 `assets/showme/{id}.html` 존재 여부
7. **주차 번호 연속성**: 1~15 순서대로인지
8. **status 값 유효**: `done`, `active`, `upcoming`, `draft`, `exam` 중 하나인지

**출력 형식:**
```
✅ Week 01: 필수 필드 OK, 5 steps, 15 tasks
⚠️ Week 03 Step 2: image "assets/images/week03/mirror.png" 파일 없음
❌ Week 04: "topics" 필드 누락
```

---

#### `add-week {N}` — 새 주차 추가

Week N을 curriculum.js에 템플릿으로 추가합니다.

**절차:**
1. curriculum.js를 읽고 Week N이 이미 존재하는지 확인
2. 이미 있으면 경고 후 중단
3. 없으면 아래 템플릿을 적절한 위치에 삽입:

```javascript
{
  "week": N,
  "status": "upcoming",
  "title": "",
  "subtitle": "",
  "summary": "",
  "duration": "~3시간",
  "topics": [],
  "steps": [
    {
      "title": "",
      "copy": "",
      "goal": [],
      "done": [],
      "tasks": [
        { "id": "wN-t1", "label": "", "detail": "" }
      ]
    }
  ],
  "shortcuts": [],
  "references": []
}
```

4. `course-site/assets/images/week{NN:02d}/` 디렉토리 생성
5. 삽입 완료 후 `validate` 모드 자동 실행

---

#### `status {상태} {범위}` — 주차 상태 일괄 변경

예시:
- `/curriculum status done 1-5` → Week 1~5를 "done"으로
- `/curriculum status active 6` → Week 6만 "active"로
- `/curriculum status upcoming 7-15` → Week 7~15를 "upcoming"으로

**유효 상태**: `done`, `active`, `upcoming`, `draft`, `exam`

**절차:**
1. 범위 파싱 (단일 숫자 또는 N-M 범위)
2. curriculum.js에서 해당 주차의 `"status"` 값 변경
3. 변경 전후 diff 출력
4. 한 번에 하나만 `active` 상태여야 함 — 여러 주차가 active면 경고

---

#### `sync` — 강의노트 동기화

curriculum.js → weeks/weekNN-*/lecture-note.md 동기화를 실행합니다.

**절차:**
1. `python3 tools/sync_course_content.py` 실행
2. 출력 결과 리포트
3. 동기화된 파일 수와 경로 표시

---

#### `link-images {week}` — Step에 이미지 자동 연결

지정된 주차의 `course-site/assets/images/week{NN}/` 디렉토리를 스캔하고, step들에 이미지를 연결합니다.

**절차:**
1. 해당 주차 이미지 디렉토리의 파일 목록 확인
2. curriculum.js의 해당 주차 steps 확인
3. 파일명↔step title 매칭 시도 (유사도 기반)
4. 매칭 결과를 표로 제시
5. 사용자 확인 후 curriculum.js의 `image` 필드 업데이트

---

#### `show {week}` — 주차 내용 요약 출력

지정된 주차의 전체 내용을 읽기 좋은 형태로 출력합니다.

**출력 내용:**
- 주차 번호, 제목, 부제, 상태
- 요약
- 토픽 목록
- 각 Step: 제목, 설명, 목표, 완료 기준, 태스크, showme 연결, 이미지
- 단축키 목록
- 참고 자료

---

#### 인자 없음 — 도움말

사용 가능한 모든 모드와 예시를 출력합니다.

---

### 핵심 파일 경로

| 파일 | 역할 |
|------|------|
| `course-site/data/curriculum.js` | 커리큘럼 마스터 데이터 (JS wrapped JSON) |
| `tools/admin-server.py` | read_curriculum() / write_curriculum() 함수 |
| `tools/sync_course_content.py` | curriculum → lecture-note.md 동기화 |
| `course-site/assets/images/weekNN/` | 주차별 이미지 디렉토리 |
| `course-site/assets/showme/` | Show Me 카드 HTML 파일들 |
| `course-site/assets/showme/_registry.js` | Show Me 위젯 레지스트리 |

### curriculum.js 파싱 패턴

```javascript
// 헤더: "const CURRICULUM = "
// 본문: JSON 배열 (주석 포함, trailing comma 허용)
// 푸터: "];\n\nif (typeof module !== \"undefined\") module.exports = CURRICULUM;"
```

**읽기**: `const CURRICULUM = ` 이후부터 `];` 까지 추출 → JS→JSON 변환 → parse
**쓰기**: JSON.stringify(indent=2) → 헤더/푸터 재부착 → 파일 저장

## Gotchas ⚠️
> Claude가 이 스킬을 쓸 때 실수했던 것들. 새 함정 발견 시 여기에 추가.

1. (아직 없음 — 사용하면서 추가)
