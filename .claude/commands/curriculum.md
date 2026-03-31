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
1. `tools/notion-mapping.json`에서 Week N의 Notion 페이지 ID 확인
2. 페이지 ID가 있으면 → Notion MCP로 해당 페이지에 템플릿 블록 추가
3. 페이지 ID가 없으면 → 경고 출력 ("Notion에 Week N 페이지를 먼저 만들고 notion-mapping.json에 ID를 추가하세요")
4. `course-site/data/overrides.json`에 Week N 엔트리 추가 (status: "upcoming")
5. `course-site/assets/images/week{NN:02d}/` 디렉토리 생성
6. `/curriculum sync` 자동 실행

---

#### `status {상태} {범위}` — 주차 상태 일괄 변경

예시:
- `/curriculum status done 1-5` → Week 1~5를 "done"으로
- `/curriculum status active 6` → Week 6만 "active"로
- `/curriculum status upcoming 7-15` → Week 7~15를 "upcoming"으로

**유효 상태**: `done`, `active`, `upcoming`, `draft`, `exam`

**절차:**
1. 범위 파싱 (단일 숫자 또는 N-M 범위)
2. `course-site/data/overrides.json`에서 해당 주차의 `"status"` 값 변경
3. curriculum.json 재생성 (merge)
4. 변경 전후 diff 출력
5. 한 번에 하나만 `active` 상태여야 함 — 여러 주차가 active면 경고

---

#### `sync` — Notion 동기화 + 검증

Notion에서 최신 콘텐츠를 가져와 curriculum.json을 재생성하고 검증합니다.

**절차:**
1. `python3 tools/notion-sync.py --fetch-only` 실행 — Notion snapshot 갱신
2. curriculum-notion.json + overrides.json → curriculum.json 자동 merge 확인
3. `/rpd-check` 스킬 호출 — Phase 1 데이터 검증
4. 변경된 주차 요약 출력

**환경 요구사항:**
- `NOTION_TOKEN` 환경변수 필수 (없으면 안내 메시지 출력)

---

#### `link-images {week}` — Step에 이미지 자동 연결

지정된 주차의 `course-site/assets/images/week{NN}/` 디렉토리를 스캔하고, step들에 이미지를 연결합니다.

**절차:**
1. 해당 주차 이미지 디렉토리의 파일 목록 확인
2. curriculum.js의 해당 주차 steps 확인
3. 파일명↔step title 매칭 시도 (유사도 기반)
4. 매칭 결과를 표로 제시
5. 사용자 확인 후 `course-site/data/overrides.json`의 해당 주차 steps에 `image` 필드 추가/업데이트

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
| `course-site/data/curriculum.json` | 최종 merge 결과 (GENERATED — 직접 수정 금지) |
| `course-site/data/curriculum-notion.json` | Notion snapshot (GENERATED — 직접 수정 금지) |
| `course-site/data/curriculum.js` | curriculum.json wrapper (GENERATED) |
| `course-site/data/overrides.json` | 코드 에셋 필드 (image, showme, status, videos, done) |
| `tools/notion-sync.py` | Notion fetch + merge 스크립트 |
| `tools/notion_api.py` | Notion API 공유 모듈 |
| `tools/notion-mapping.json` | week → Notion page ID 매핑 |
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

## 실행 로그
실행 완료 시 아래 형식으로 기록:
```bash
echo "[$(date '+%Y-%m-%d %H:%M')] mode=$MODE result=$RESULT target=$TARGET" >> .claude/skill-logs/curriculum.log
```

## Gotchas ⚠️
> Claude가 이 스킬을 쓸 때 실수했던 것들. 새 함정 발견 시 여기에 추가.

1. curriculum.json, curriculum-notion.json, curriculum.js는 generated file — 직접 수정 금지
2. 콘텐츠(title/copy/tasks) 수정은 반드시 Notion MCP 경로로
3. 에셋(image/showme/status/done) 수정은 overrides.json만
4. sync 실행 시 NOTION_TOKEN 환경변수 필요
