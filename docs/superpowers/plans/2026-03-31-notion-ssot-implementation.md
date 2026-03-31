# Notion SSOT 아키텍처 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Notion을 유일한 콘텐츠 SSOT로 확립하고, curriculum.json 직접 수정을 금지하여 Notion-사이트 간 데이터 충돌을 원천 차단한다.

**Architecture:** curriculum.json/curriculum.js를 generated file로 전환. 콘텐츠 수정은 Notion API, 코드 에셋(이미지/showme/status)은 overrides.json만 수정. /curriculum sync 명령으로 fetch+merge+검증을 원스텝으로 실행.

**Tech Stack:** Notion MCP (mcp__notion__*), Python (notion-sync.py, notion_api.py), Claude Code skills (.claude/commands/*.md)

**Spec:** `docs/superpowers/specs/2026-03-31-notion-ssot-architecture-design.md`

---

## File Structure

| 파일 | 변경 | 역할 |
|------|------|------|
| `.claude/projects/-Users-ssongji-Developer-Workspace-RPD/CLAUDE.md` | 생성 | 프로젝트 레벨 규칙 (curriculum.json 수정 금지 등) |
| `.claude/commands/curriculum.md` | 수정 | sync 모드 변경, 쓰기 경로 분리 |
| `.claude/commands/rpd-check.md` | 수정 | 1.8 동기화 상태 검증 추가 |
| `.claude/skills/rpd-content-write/SKILL.md` | 수정 | 대상 파일을 Notion API 경로로 전환 |
| `.claude/skills/rpd-week-review/SKILL.md` | 수정 | 수정 반영 시 Notion/overrides 분리 |

---

### Task 1: 프로젝트 CLAUDE.md에 콘텐츠 관리 규칙 추가

**Files:**
- Create: `.claude/projects/-Users-ssongji-Developer-Workspace-RPD/CLAUDE.md`

- [ ] **Step 1: 프로젝트 CLAUDE.md 생성**

```markdown
# RPD Project Rules

## 콘텐츠 관리 규칙

### Generated Files — 직접 수정 금지
다음 파일은 자동 생성되므로 Edit/Write tool로 직접 수정하지 않는다:
- `course-site/data/curriculum.json`
- `course-site/data/curriculum-notion.json`
- `course-site/data/curriculum.js`

이 파일들을 수정하라는 요청을 받으면, 아래 수정 경로를 따른다.

### 수정 경로
| 수정 대상 | 수정 위치 | 도구 |
|-----------|----------|------|
| step title/copy/tasks/goal/assignment/shortcuts/mistakes/docs | Notion | Notion MCP (mcp__notion__*) |
| image, showme, status, videos, done, summary | overrides.json | Edit tool |
| showme 카드 HTML/supplement | course-site/assets/showme/ | /showme 스킬 |

### 수정 후 필수 절차
1. Notion 수정 시: `python3 tools/notion-sync.py --fetch-only` 실행
2. curriculum.json 재생성 확인
3. `/rpd-check` 검증
```

- [ ] **Step 2: 파일 생성 확인**

Run: `cat .claude/projects/-Users-ssongji-Developer-Workspace-RPD/CLAUDE.md`
Expected: 위 내용이 출력됨

- [ ] **Step 3: Commit**

```bash
git add .claude/projects/-Users-ssongji-Developer-Workspace-RPD/CLAUDE.md
git commit -m "feat: add project CLAUDE.md with content management rules

Notion SSOT 아키텍처 규칙 추가 — curriculum.json 직접 수정 금지,
필드별 소유권(Notion vs overrides.json) 명시"
```

---

### Task 2: `/curriculum` 스킬 수정 — sync 모드 + 쓰기 경로 분리

**Files:**
- Modify: `.claude/commands/curriculum.md`

- [ ] **Step 1: sync 모드를 Notion fetch + merge + check로 변경**

`.claude/commands/curriculum.md`의 `#### sync` 섹션 (줄 104-111)을 다음으로 교체:

```markdown
#### `sync` — Notion 동기화 + 검증

Notion에서 최신 콘텐츠를 가져와 curriculum.json을 재생성하고 검증합니다.

**절차:**
1. `python3 tools/notion-sync.py --fetch-only` 실행 — Notion snapshot 갱신
2. curriculum-notion.json + overrides.json → curriculum.json 자동 merge 확인
3. `/rpd-check` 스킬 호출 — Phase 1 데이터 검증
4. 변경된 주차 요약 출력

**환경 요구사항:**
- `NOTION_TOKEN` 환경변수 필수 (없으면 안내 메시지 출력)
```

- [ ] **Step 2: status 모드를 overrides.json 경로로 변경**

`#### status` 섹션 (줄 87-101)의 절차를 다음으로 교체:

```markdown
**절차:**
1. 범위 파싱 (단일 숫자 또는 N-M 범위)
2. `course-site/data/overrides.json`에서 해당 주차의 `"status"` 값 변경
3. curriculum.json 재생성 (merge)
4. 변경 전후 diff 출력
5. 한 번에 하나만 `active` 상태여야 함 — 여러 주차가 active면 경고
```

- [ ] **Step 3: add-week 모드를 Notion API 경로로 변경**

`#### add-week` 섹션 (줄 48-84)의 절차를 다음으로 교체:

```markdown
**절차:**
1. `tools/notion-mapping.json`에서 Week N의 Notion 페이지 ID 확인
2. 페이지 ID가 있으면 → Notion MCP로 해당 페이지에 템플릿 블록 추가
3. 페이지 ID가 없으면 → 경고 출력 ("Notion에 Week N 페이지를 먼저 만들고 notion-mapping.json에 ID를 추가하세요")
4. `course-site/data/overrides.json`에 Week N 엔트리 추가 (status: "upcoming")
5. `course-site/assets/images/week{NN:02d}/` 디렉토리 생성
6. `/curriculum sync` 자동 실행
```

- [ ] **Step 4: link-images 모드를 overrides.json 경로로 변경**

`#### link-images` 섹션 (줄 115-125)의 절차 항목 5를 다음으로 교체:

```markdown
5. 사용자 확인 후 `course-site/data/overrides.json`의 해당 주차 steps에 `image` 필드 추가/업데이트
```

- [ ] **Step 5: 핵심 파일 경로 테이블 업데이트**

줄 148-158의 핵심 파일 경로 테이블을 다음으로 교체:

```markdown
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
```

- [ ] **Step 6: Gotchas에 규칙 추가**

Gotchas 섹션에 추가:

```markdown
1. curriculum.json, curriculum-notion.json, curriculum.js는 generated file — 직접 수정 금지
2. 콘텐츠(title/copy/tasks) 수정은 반드시 Notion MCP 경로로
3. 에셋(image/showme/status/done) 수정은 overrides.json만
4. sync 실행 시 NOTION_TOKEN 환경변수 필요
```

- [ ] **Step 7: 수정 확인**

Run: `grep -n "overrides.json\|notion-sync\|GENERATED\|직접 수정 금지" .claude/commands/curriculum.md`
Expected: 여러 줄에서 새로 추가된 키워드가 검색됨

- [ ] **Step 8: Commit**

```bash
git add .claude/commands/curriculum.md
git commit -m "refactor(curriculum): route writes through Notion API + overrides.json

sync → notion-sync.py fetch + merge + rpd-check
status → overrides.json만 수정
add-week → Notion API로 페이지 생성
link-images → overrides.json에 image 필드 추가
curriculum.json/js를 generated file로 명시"
```

---

### Task 3: `/rpd-check` 스킬에 동기화 검증 추가

**Files:**
- Modify: `.claude/commands/rpd-check.md`

- [ ] **Step 1: Phase 1에 1.8 동기화 상태 검증 카테고리 추가**

`.claude/commands/rpd-check.md`에서 `## Phase 2: Browser Verify` 라인 바로 위에 다음 섹션 삽입:

```markdown
### 1.8 동기화 상태 검증 (warning/critical)

1. `curriculum-notion.json` 파일의 마지막 git commit 시간 확인:
   ```bash
   git log -1 --format="%ci" -- course-site/data/curriculum-notion.json
   ```
   - 30분 이상 경과 시 → `[INFO] Notion snapshot이 오래됨 — /curriculum sync 권장`
   - 24시간 이상 경과 시 → `[WARNING] Notion snapshot이 매우 오래됨`

2. overrides.json의 week/step 인덱스가 curriculum-notion.json 구조와 매칭되는지:
   - curriculum-notion.json 읽기 → 각 week의 steps 배열 길이 확인
   - overrides.json 읽기 → 각 week의 steps 키(인덱스) 확인
   - step 인덱스가 curriculum-notion.json의 steps 범위를 초과하면
     → `[CRITICAL] overrides step 인덱스 불일치: week {N} step {idx} — Notion에서 step이 추가/삭제됨`

3. curriculum-notion.json + overrides.json을 수동 merge한 결과와 현재 curriculum.json 비교:
   - 두 파일을 읽고 merge 로직 적용 (overrides 필드가 notion 필드를 덮어씀)
   - 현재 curriculum.json과 비교
   - 불일치 시 → `[WARNING] curriculum.json이 stale — /curriculum sync 필요`
```

- [ ] **Step 2: 수정 확인**

Run: `grep -c "1.8\|동기화 상태" .claude/commands/rpd-check.md`
Expected: 2 이상

- [ ] **Step 3: Commit**

```bash
git add .claude/commands/rpd-check.md
git commit -m "feat(rpd-check): add sync state verification (phase 1.8)

Notion snapshot 타임스탬프, overrides 인덱스 매칭,
curriculum.json stale 여부 검증 추가"
```

---

### Task 4: `/rpd-content-write` 스킬 수정 — Notion API 경로로 전환

**Files:**
- Modify: `.claude/skills/rpd-content-write/SKILL.md`

- [ ] **Step 1: 대상 파일 섹션 변경**

`.claude/skills/rpd-content-write/SKILL.md`의 줄 14-15를 다음으로 교체:

기존:
```markdown
## 대상 파일
- `course-site/data/curriculum.js` — 15주 커리큘럼 데이터 (단일 소스)
```

변경:
```markdown
## 수정 경로

콘텐츠 수정은 Notion을 통해 수행한다. curriculum.json/js는 generated file이므로 직접 수정하지 않는다.

| 필드 | 수정 위치 | 방법 |
|------|----------|------|
| step title, copy, tasks, goal, assignment | Notion | Notion MCP (mcp__notion__update-page) |
| shortcuts, mistakes, docs | Notion | Notion MCP |
| image, showme, done, status | overrides.json | Edit tool |

### Notion 수정 절차
1. `tools/notion-mapping.json`에서 대상 week의 Notion page ID 확인
2. Notion MCP로 해당 페이지의 블록 수정
3. `python3 tools/notion-sync.py --fetch-only` 실행
4. curriculum.json 재생성 확인
5. `/rpd-check week {N}` 검증

### 참고 파일
- `course-site/data/curriculum.json` — 읽기 전용, 현재 상태 확인용
- `course-site/data/overrides.json` — 코드 에셋 필드 수정용
- `tools/notion-mapping.json` — week → Notion page ID
```

- [ ] **Step 2: Gotchas 섹션에 규칙 추가**

Gotchas 섹션에 추가:

```markdown
- curriculum.json/js를 직접 수정하지 말 것 — Notion MCP + overrides.json 경로만 사용
- Notion 수정 후 반드시 notion-sync.py --fetch-only 실행
```

- [ ] **Step 3: 수정 확인**

Run: `grep -n "Notion MCP\|overrides.json\|generated file\|직접 수정" .claude/skills/rpd-content-write/SKILL.md`
Expected: 여러 줄에서 검색됨

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/rpd-content-write/SKILL.md
git commit -m "refactor(rpd-content-write): route content edits through Notion API

curriculum.js 직접 수정 → Notion MCP + overrides.json 경로로 전환
수정 절차 및 필드별 소유권 명시"
```

---

### Task 5: `/rpd-week-review` 스킬 수정 — 수정 반영 경로 분리

**Files:**
- Modify: `.claude/skills/rpd-week-review/SKILL.md`

- [ ] **Step 1: 수정 반영 규칙 추가**

`.claude/skills/rpd-week-review/SKILL.md`의 inspection procedure 섹션 끝에 다음 추가:

```markdown
## 수정 반영 규칙

리뷰에서 발견된 문제를 수정할 때:

| 문제 유형 | 수정 위치 |
|-----------|----------|
| copy 톤/표현 수정 | Notion MCP → notion-sync.py --fetch-only |
| task label 수정 | Notion MCP → notion-sync.py --fetch-only |
| 이미지 누락/연결 | overrides.json |
| showme 연결 | overrides.json |
| done 체크리스트 수정 | overrides.json |

**주의**: curriculum.json/js를 직접 수정하지 않는다.
```

- [ ] **Step 2: 수정 확인**

Run: `grep -n "Notion MCP\|overrides.json\|직접 수정" .claude/skills/rpd-week-review/SKILL.md`
Expected: 여러 줄에서 검색됨

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/rpd-week-review/SKILL.md
git commit -m "refactor(rpd-week-review): add edit routing rules for Notion SSOT

리뷰 수정 시 Notion API (콘텐츠) + overrides.json (에셋) 경로 분리"
```

---

### Task 6: 통합 검증

**Files:** (읽기 전용 — 수정 없음)

- [ ] **Step 1: CLAUDE.md 규칙이 로드되는지 확인**

Run: `cat .claude/projects/-Users-ssongji-Developer-Workspace-RPD/CLAUDE.md`
Expected: "Generated Files — 직접 수정 금지" 규칙 포함

- [ ] **Step 2: /curriculum 스킬의 sync 모드 확인**

Run: `grep -A5 "sync" .claude/commands/curriculum.md | head -10`
Expected: "notion-sync.py --fetch-only" 포함

- [ ] **Step 3: /rpd-check 스킬의 1.8 카테고리 확인**

Run: `grep -A3 "1.8" .claude/commands/rpd-check.md`
Expected: "동기화 상태 검증" 포함

- [ ] **Step 4: rpd-content-write 스킬의 Notion 경로 확인**

Run: `grep "Notion MCP" .claude/skills/rpd-content-write/SKILL.md`
Expected: Notion MCP 참조 포함

- [ ] **Step 5: rpd-week-review 스킬의 수정 규칙 확인**

Run: `grep "overrides.json" .claude/skills/rpd-week-review/SKILL.md`
Expected: overrides.json 참조 포함

- [ ] **Step 6: 전체 변경 요약 확인**

Run: `git log --oneline -5`
Expected: Task 1~5의 커밋 5개 표시

- [ ] **Step 7: Final commit (필요 시)**

모든 검증 통과 후 변경사항이 남아있으면:
```bash
git status
```
