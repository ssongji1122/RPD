# Notion SSOT 아키텍처 — 콘텐츠 관리 일원화

## Context

RPD 과정 사이트의 콘텐츠가 Notion과 curriculum.json 양쪽에서 수정되면서 반복적으로 충돌이 발생한다:
- Notion에서 수정한 내용이 로컬에 반영 안 됨
- Claude Code가 curriculum.json을 직접 수정하면 다음 Notion sync에서 덮어써짐
- 어느 쪽이 최신인지 판단 불가
- Notion에 추가한 step이 showme/이미지 같은 코드 에셋과 연결 안 됨

**목표**: Notion을 유일한 콘텐츠 SSOT로 확립하고, curriculum.json 직접 수정을 금지하여 충돌을 원천 차단한다.

## 아키텍처

```
┌─────────────────────────────────────────────────┐
│                  Notion (SSOT)                  │
│         title, copy, tasks, goal, docs          │
│                                                 │
│   ↑ Claude Code writes via Notion MCP/API       │
│   ↑ ssonji edits directly in browser            │
└───────────────────┬─────────────────────────────┘
                    │ fetch (notion-sync.py --fetch-only)
                    ▼
          curriculum-notion.json (read-only, auto-generated)
                    +
          overrides.json (Claude Code writes)
            image, showme, status, videos, done
                    │
                    ▼  merge (notion-sync.py)
          curriculum.json (generated, never hand-edited)
                    │
                    ▼
              RPD 사이트 (GitHub Pages)
```

## 핵심 규칙

### 1. Generated Files — 직접 수정 금지

다음 파일은 자동 생성되므로 직접 수정하지 않는다:
- `course-site/data/curriculum.json`
- `course-site/data/curriculum-notion.json`
- `course-site/data/curriculum.js`

### 2. 필드별 소유권

| 필드 | 소유자 | 수정 방법 |
|------|--------|-----------|
| step.title | Notion | Notion MCP 또는 Notion 웹 |
| step.copy | Notion | Notion MCP 또는 Notion 웹 |
| step.tasks (id, label, detail) | Notion | Notion MCP 또는 Notion 웹 |
| step.goal | Notion | Notion MCP 또는 Notion 웹 |
| assignment | Notion | Notion MCP 또는 Notion 웹 |
| shortcuts | Notion | Notion MCP 또는 Notion 웹 |
| mistakes | Notion | Notion MCP 또는 Notion 웹 |
| docs, videos (외부 링크) | Notion | Notion MCP 또는 Notion 웹 |
| step.image / step.images | overrides.json | Claude Code Edit tool |
| step.showme | overrides.json | Claude Code Edit tool |
| step.done | overrides.json | Claude Code Edit tool |
| week.status | overrides.json | Claude Code Edit tool |
| week.summary | overrides.json | Claude Code Edit tool |
| week.videos (보충 영상) | overrides.json | Claude Code Edit tool |

### 3. 수정 후 필수 절차

**Notion 수정 후:**
1. `python3 tools/notion-sync.py --fetch-only` — Notion snapshot 갱신
2. curriculum.json 자동 재생성 확인
3. `/rpd-check` 검증

**overrides.json 수정 후:**
1. curriculum.json 재생성 (merge)
2. `/rpd-check` 검증

## 변경 사항

### 변경 1: CLAUDE.md에 콘텐츠 관리 규칙 추가

프로젝트 CLAUDE.md에 위 핵심 규칙 3개를 추가한다.
모든 Claude Code 스킬이 이 규칙을 따르게 된다.

**파일**: `.claude/CLAUDE.md` (프로젝트 레벨)

### 변경 2: `/curriculum` 스킬 수정

현재 curriculum.json을 직접 수정하는 부분을 두 갈래로 분리:

| 모드 | 현재 | 변경 후 |
|------|------|---------|
| `validate` | curriculum.json 읽기 | 변경 없음 |
| `add-week N` | curriculum.json에 week 추가 | Notion API로 새 페이지 생성 + overrides.json에 status 추가 |
| `status done 1-5` | curriculum.json status 수정 | overrides.json의 status만 수정 |
| `sync` | lecture notes 동기화 | notion-sync.py --fetch-only + merge + /rpd-check |
| `link-images` | curriculum.json image 필드 수정 | overrides.json의 image 필드만 수정 |
| `show` | curriculum.json 읽기 | 변경 없음 |

**파일**: `.claude/commands/curriculum.md`

### 변경 3: `/rpd-check`에 동기화 검증 추가

Phase 1에 카테고리 1.8 추가:

**1.8 동기화 상태 검증**
- curriculum-notion.json의 git commit 시간 확인
  - 30분 이상 경과 시 → `[INFO] Notion snapshot이 오래됨 — /curriculum sync 권장`
- curriculum-notion.json + overrides.json merge 결과와 현재 curriculum.json 비교
  - 불일치 시 → `[WARNING] curriculum.json이 stale — /curriculum sync 필요`
- overrides.json의 week/step 인덱스가 curriculum-notion.json 구조와 매칭되는지
  - step 인덱스 범위 초과 시 → `[CRITICAL] overrides step 인덱스 불일치 — Notion에서 step이 추가/삭제됨`

**파일**: `.claude/commands/rpd-check.md`

### 변경 4: 관련 스킬 규칙 적용

curriculum.json을 수정할 가능성이 있는 스킬들에 규칙 적용:

| 스킬 | 변경 |
|------|------|
| `/showme` | showme 필드 → overrides.json만 수정. 변경 없음 (이미 HTML/supplement만 건드림) |
| `/rpd-content-write` | 콘텐츠 작성 시 Notion API 경로 사용 |
| `/rpd-week-review` | 리뷰 결과 반영 시 Notion API (콘텐츠) + overrides.json (에셋) 분리 |
| `/brainstormC` | supplement만 건드리므로 변경 없음 |
| `/capture` | 이미지 생성 후 overrides.json에 경로 추가 |

**파일**: 해당 `.claude/commands/*.md` 파일들

## 사용 시나리오

### 시나리오 1: Claude Code로 새 주차 콘텐츠 정리

```
ssonji: "week 6 material 수업 내용 정리해줘"

1. /rpd-research material-basics → 리서치
2. Notion MCP로 week 6 페이지에 steps/tasks 작성
3. python3 tools/notion-sync.py --fetch-only → 로컬 반영
4. overrides.json에 showme/image/status 추가
5. curriculum.json 자동 merge
6. /rpd-check week 6 → 검증
```

### 시나리오 2: Notion에서 직접 수정 후 코드 에셋 추가

```
ssonji: "week 5 노션에서 수정했어, 반영해줘"

1. python3 tools/notion-sync.py --fetch-only → 최신 가져옴
2. curriculum.json 재생성
3. /rpd-check week 5 → 새 step에 빠진 에셋 확인
4. overrides.json에 showme/image 추가
5. /showme new-card → 카드 생성
```

### 시나리오 3: showme/이미지 추가 (Notion 안 건드림)

```
ssonji: "week 3에 bevel-tool showme 연결해줘"

1. /showme bevel-tool → 카드 HTML 생성
2. overrides.json에 showme 필드 추가
3. curriculum.json 재생성
4. /rpd-check week 3 → 검증
```

### 시나리오 4: 상태 확인

```
ssonji: "week 5 최신 맞아?"

1. /curriculum sync → fetch + merge + check
2. 리포트: "Notion 기준 5 steps, 이미지 3개 누락, 동기화 정상"
```

## 핵심 파일

| 파일 | 역할 | 변경 |
|------|------|------|
| `.claude/CLAUDE.md` | 프로젝트 규칙 | 콘텐츠 관리 규칙 추가 |
| `.claude/commands/curriculum.md` | 커리큘럼 스킬 | 쓰기 경로 분리 |
| `.claude/commands/rpd-check.md` | 검증 스킬 | 1.8 동기화 검증 추가 |
| `.claude/commands/rpd-content-write.md` | 콘텐츠 작성 | Notion API 경로 전환 |
| `tools/notion-sync.py` | 동기화 스크립트 | 변경 없음 (이미 동작) |
| `tools/notion_api.py` | Notion API 모듈 | 변경 없음 |
| `tools/notion-mapping.json` | week → page ID | 변경 없음 |
| `course-site/data/overrides.json` | 코드 에셋 저장 | 기존 구조 유지 |

## 검증 방법

1. Claude Code에서 curriculum.json 직접 수정 시도 → CLAUDE.md 규칙에 의해 차단되는지 확인
2. `/curriculum sync` 실행 → notion-sync.py fetch + merge + rpd-check 정상 동작
3. overrides.json 수정 후 curriculum.json 재생성 확인
4. `/rpd-check` 실행 → 1.8 동기화 상태 검증이 정상 리포트 출력
5. Notion에서 step 추가 → sync → overrides 인덱스 불일치 감지 확인
