# RPD 스킬 품질 표준화 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `/showme`, `/curriculum`, `/rpd-check` 3개 핵심 스킬에 Anthropic PDF 5패턴을 적용하여 실행 품질을 표준화한다.

**Architecture:** 각 단일 파일 스킬(`.md`)을 폴더 구조(`SKILL.md` + `references/`)로 변환하고, Progressive Disclosure + Iterative Refinement + Success Criteria를 추가한다. 기존 도메인 지식은 보존하면서 패턴만 오버레이한다.

**Tech Stack:** Markdown (SKILL.md), Bash (로그), Paperclip API (이슈 등록)

---

## File Structure

### 변환 전 (현재)

```
.claude/commands/
├── showme.md          # 225줄, 단일 파일
├── curriculum.md      # 167줄, 단일 파일
└── rpd-check.md       # 291줄, 단일 파일
```

### 변환 후 (목표)

```
.claude/commands/
├── showme/
│   ├── SKILL.md                  # ~120줄 (핵심 절차 + 품질 게이트)
│   └── references/
│       ├── css-reference.md      # CSS 변수/컴포넌트 표
│       ├── card-quality.md       # 좋은/나쁜 카드 예시
│       └── template.md           # HTML 골격 + URL 패턴
├── curriculum/
│   ├── SKILL.md                  # ~120줄 (모드 분기 + 핵심 절차)
│   └── references/
│       ├── file-paths.md         # 핵심 파일 경로 표
│       └── parsing-guide.md      # curriculum.js 파싱 패턴
└── rpd-check/
    ├── SKILL.md                  # ~170줄 (Phase 1 + smart scoping)
    └── references/
        ├── browser-verify.md     # Phase 2 브라우저 검증 상세
        └── fix-rules.md          # --fix 자동 수정 규칙표
```

---

### Task 1: `/showme` 폴더 구조 변환

**Files:**
- Create: `.claude/commands/showme/SKILL.md`
- Create: `.claude/commands/showme/references/css-reference.md`
- Create: `.claude/commands/showme/references/template.md`
- Create: `.claude/commands/showme/references/card-quality.md`
- Delete: `.claude/commands/showme.md`

- [ ] **Step 1: 디렉토리 생성**

```bash
mkdir -p .claude/commands/showme/references
```

- [ ] **Step 2: 기존 showme.md를 SKILL.md로 복사**

```bash
cp .claude/commands/showme.md .claude/commands/showme/SKILL.md
```

- [ ] **Step 3: references/css-reference.md 추출**

`.claude/commands/showme/SKILL.md`에서 아래 두 섹션을 잘라서 `references/css-reference.md`로 이동:

- `### CSS 변수 레퍼런스` (현재 158~165줄)
- `### CSS 컴포넌트 요약` (현재 167~182줄)

`references/css-reference.md` 내용:

```markdown
# ShowMe CSS 레퍼런스

## CSS 변수

| 변수 | 값 |
|------|-----|
| `--bg` | `#0a0a0a` |
| `--surface` | `#17181a` |
| `--line` | `rgba(255,255,255,.08)` |
| `--key` | `#0a84ff` |
| `--key-soft` | `#8ec5ff` |
| `--success` | `#10b981` |
| `--warn` | `#f59e0b` |
| `--danger` | `#ef4444` |
| `--text` | `#f5f5f7` |
| `--muted` | `#a1a1aa` |
| `--radius-sm` | `12px` |
| `--radius-md` | `18px` |

## CSS 컴포넌트

| 클래스 | 용도 |
|--------|------|
| `.concept-grid` / `.concept-card` | 개념 카드 그리드 |
| `.badge` `.badge-blue/green/amber/red` | 인라인 뱃지 |
| `.analogy` | 비유 설명 박스 (amber) |
| `.shortcut-list` / `.shortcut-row` / `.kbd` | 단축키 목록 |
| `.demo-wrap` / `.demo-controls` / `.demo-btn` | Canvas 데모 영역 |
| `.modifier-panel` / `.mp-row` / `.mp-slider` / `.mp-value` | 파라미터 패널 |
| `.usage-grid` / `.usage-card` | 사용 사례 2열 |
| `.combo-section` / `.combo-grid` / `.combo-card` | 추천 조합 |
| `.tip-box` | 팁/주의사항 박스 |
| `.doc-ref` / `.doc-ref-list` | 공식 문서 링크 |
| `.compare-table` | 비교 테이블 |
| `.section-divider` | 섹션 구분선 |
```

- [ ] **Step 4: references/template.md 추출**

`.claude/commands/showme/SKILL.md`에서 아래 두 섹션을 잘라서 `references/template.md`로 이동:

- HTML 골격 템플릿 (현재 54~83줄의 `<!DOCTYPE html>` ~ `</html>` 코드 블록)
- `### Blender 공식 문서 URL 패턴` (현재 184~191줄)

`references/template.md` 내용:

```markdown
# ShowMe HTML 템플릿

## 골격 구조

​```html
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
​```

## Blender 공식 문서 URL 패턴

| 카테고리 | URL 패턴 |
|----------|----------|
| Generate 모디파이어 | `https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/{name}.html` |
| Mesh 도구 | `https://docs.blender.org/manual/en/latest/modeling/meshes/tools/{tool}.html` |
| Edge 편집 | `https://docs.blender.org/manual/en/latest/modeling/meshes/editing/edge/{tool}.html` |
| Mesh 편집 | `https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/{tool}.html` |

## 참조 파일

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
```

- [ ] **Step 5: references/card-quality.md 작성**

```markdown
# ShowMe 카드 품질 기준

## 핵심 원칙

이 스킬은 반드시 Opus 4.6 모델로 실행해야 합니다.
표면적 정의가 아닌, Blender를 실제로 쓸 때 학생이 겪는
혼란과 깨달음을 관통하는 카드를 만드세요.

## Success Criteria

- [ ] 개념 카드에 "비유(analogy)" + "왜 중요한지(why)" 둘 다 포함
- [ ] interaction 데모에 프리셋 3개 이상 + 각 프리셋에 "이 조합의 핵심" 설명
- [ ] 퀴즈 5문제 중 최소 2문제가 "상황 판단형" (단순 암기 X)
- [ ] doc-ref 공식 문서 링크 포함
- [ ] 모바일 반응형 + 터치 이벤트 지원

## 좋은 카드 vs 나쁜 카드

### 개념 카드

**나쁜 예 (단순 정의):**
```
Mirror Modifier는 오브젝트를 대칭 복제하는 모디파이어입니다.
```
문제: "왜" 쓰는지, "어떤 상황에서" 유용한지 빠져 있음.

**좋은 예 (관통하는 설명):**
```
Mirror Modifier는 오브젝트를 축 기준으로 대칭 복제합니다.
캐릭터나 차량처럼 좌우 대칭인 모델을 만들 때, 한쪽만 작업하면
반대쪽이 자동으로 따라옵니다. 작업량이 절반으로 줄어요.

비유: 종이를 반으로 접고 한쪽만 오리면 대칭 무늬가 나오는 것
```

### 퀴즈

**나쁜 예 (암기형):**
```
Q: Mirror Modifier의 한글 이름은?
→ 용어 암기. 학습에 도움 안 됨.
```

**좋은 예 (상황 판단형):**
```
Q: 자동차 모델링 중 한쪽 문만 수정했는데 반대쪽에 반영이 안 됩니다.
   가장 가능성 높은 원인은?
→ 상황 판단. 실제 사용 시 겪는 문제 해결력 측정.
```

### interaction 탭

**나쁜 예:**
- 슬라이더가 있지만 "이걸 왜 조절하는지" 안내 없음
- 프리셋 이름이 "Preset 1", "Preset 2"

**좋은 예:**
- 각 슬라이더 옆에 Blender 실제 파라미터명 표시
- 프리셋 클릭 시 "이 조합의 핵심: Roughness 0으로 거울 표면 구현" 설명
- 프리셋 이름이 실제 재질 (금속, 유리, 고무 등)

## 품질 게이트 (자기 검증)

카드 HTML 생성 후, 아래 기준으로 자기 검증을 수행합니다.
FAIL이면 해당 탭을 재생성합니다 (최대 2회).

1. **개념탭**: 각 concept-card에 "왜 이게 중요한지" 설명이 있는가?
   → 단순 정의만이면 FAIL
2. **interaction탭**: 슬라이더/프리셋이 학습 포인트와 연결되는가?
   → 무관한 파라미터만 있으면 FAIL
3. **퀴즈**: 암기가 아닌 이해를 묻는가?
   → 단순 용어 질문만이면 FAIL
```

- [ ] **Step 6: SKILL.md에서 분리된 내용 제거 + 새 내용 추가**

SKILL.md 수정사항:

1. frontmatter에 `model: opus` 추가
2. description에 negative trigger 추가
3. 분리된 CSS/템플릿/URL 섹션을 `references/` 참조 안내로 교체
4. Step 3.5 품질 게이트 추가
5. Success Criteria 섹션 추가
6. Gotchas 패턴 업데이트
7. 실행 로그 표준화

frontmatter 변경:

```yaml
---
description: "Show Me 교육 카드 생성. 예: /showme array-modifier, /showme list, /showme verify. DO NOT use for: 카드 내용 질문, 기존 카드 수정(Edit 사용), 보충 설명(/brainstormC 사용)"
model: opus
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(python3 -m http.server:*), Bash(curl:*), Bash(wc:*), Bash(ls:*), Agent
---
```

본문 최상단 추가 (Context 위):

```markdown
> **품질 철학**: 이 스킬은 반드시 Opus 4.6 모델로 실행합니다. 표면적 정의가 아닌, Blender를 실제로 쓸 때 학생이 겪는 혼란과 깨달음을 관통하는 카드를 만드세요. 품질 기준은 `references/card-quality.md`를 참조.
```

CSS/템플릿 섹션 교체:

```markdown
### 레퍼런스 (필요 시 참조)

- CSS 변수/컴포넌트: `references/css-reference.md`
- HTML 골격/URL 패턴/참조 파일: `references/template.md`
- 품질 기준/좋은·나쁜 예시: `references/card-quality.md`
```

Step 3.5 추가 (Step 3과 Step 4 사이):

```markdown
#### Step 3.5: 품질 게이트 (자기 검증)

생성된 HTML을 아래 기준으로 검증합니다 (`references/card-quality.md` 상세 참조):

1. **개념탭**: 각 concept-card에 "왜 이게 중요한지" + "비유(analogy)" 포함?
   → 단순 정의만이면 → 해당 카드 재작성
2. **interaction탭**: 프리셋에 "이 조합의 핵심" 설명 포함?
   → 설명 없으면 → 프리셋 설명 추가
3. **퀴즈**: 5문제 중 2문제 이상이 상황 판단형?
   → 암기형만이면 → 퀴즈 재출제
4. FAIL 항목이 있으면 재생성 (최대 2회 반복)
5. 2회 후에도 FAIL이면 → 사용자에게 어떤 기준을 충족하지 못했는지 명시하고 판단 요청
```

Gotchas 섹션 교체:

```markdown
## Gotchas ⚠️ (자동 축적)

스킬 실행 중 예상치 못한 실패/우회가 발생하면:
1. 이 섹션 하단에 한 줄 추가
2. 형식: `N. [날짜] 증상 → 원인 → 해결`
3. 같은 실수 반복 시 해당 항목에 빈도 카운터 추가

1. (아직 없음 — 사용하면서 추가)
```

실행 로그 교체:

```markdown
## 실행 로그
실행 완료 시 아래 형식으로 기록:
​```bash
echo "[$(date '+%Y-%m-%d %H:%M')] mode=$MODE result=$RESULT quality=$QUALITY target=$TARGET" >> .claude/skill-logs/showme.log
​```
- `result`: `success` / `partial` / `fail`
- `quality`: `pass` / `warn` / `fail`
```

- [ ] **Step 7: 기존 showme.md 삭제**

```bash
rm .claude/commands/showme.md
```

- [ ] **Step 8: 스킬 로드 검증**

```bash
# 폴더 구조 확인
ls -la .claude/commands/showme/
ls -la .claude/commands/showme/references/

# SKILL.md frontmatter 확인
head -5 .claude/commands/showme/SKILL.md

# model: opus 확인
grep "model:" .claude/commands/showme/SKILL.md
```

Expected:
- `SKILL.md` 존재
- `references/` 에 3개 파일
- frontmatter에 `model: opus` 포함

- [ ] **Step 9: 커밋**

```bash
git add .claude/commands/showme/ .claude/commands/showme.md
git commit -m "feat(skill): /showme Progressive Disclosure + Opus 4.6 강제 + 품질 게이트

- 단일 파일 → 폴더 구조 (SKILL.md + references/)
- model: opus frontmatter 추가
- Step 3.5 품질 게이트 (Iterative Refinement)
- references/card-quality.md 품질 기준 + 좋은/나쁜 예시
- Gotchas 자동 축적 패턴, 실행 로그 표준화
- description에 negative trigger 추가"
```

---

### Task 2: `/curriculum` 폴더 구조 변환

**Files:**
- Create: `.claude/commands/curriculum/SKILL.md`
- Create: `.claude/commands/curriculum/references/file-paths.md`
- Create: `.claude/commands/curriculum/references/parsing-guide.md`
- Delete: `.claude/commands/curriculum.md`

- [ ] **Step 1: 디렉토리 생성**

```bash
mkdir -p .claude/commands/curriculum/references
```

- [ ] **Step 2: 기존 curriculum.md를 SKILL.md로 복사**

```bash
cp .claude/commands/curriculum.md .claude/commands/curriculum/SKILL.md
```

- [ ] **Step 3: references/file-paths.md 추출**

`.claude/commands/curriculum/SKILL.md`에서 `### 핵심 파일 경로` 섹션 (128~153줄)을 잘라서 이동:

```markdown
# Curriculum 핵심 파일 경로

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

- [ ] **Step 4: references/parsing-guide.md 추출**

```markdown
# curriculum.js 파싱 가이드

## 파일 구조

​```javascript
// 헤더: "const CURRICULUM = "
// 본문: JSON 배열 (주석 포함, trailing comma 허용)
// 푸터: "];\n\nif (typeof module !== \"undefined\") module.exports = CURRICULUM;"
​```

## 읽기

`const CURRICULUM = ` 이후부터 `];` 까지 추출 → JS→JSON 변환 → parse

## 쓰기

JSON.stringify(indent=2) → 헤더/푸터 재부착 → 파일 저장

## 주의사항

- curriculum.json, curriculum-notion.json, curriculum.js는 generated file — 직접 수정 금지
- 콘텐츠(title/copy/tasks) 수정은 반드시 Notion MCP 경로로
- 에셋(image/showme/status/done) 수정은 overrides.json만
- sync 실행 시 NOTION_TOKEN 환경변수 필요
```

- [ ] **Step 5: SKILL.md 수정 — validate 재검증 루프 추가**

`#### validate` 섹션 끝에 재검증 루프 추가:

```markdown
**재검증 루프 (Iterative Refinement):**

1. 검증 실행 → 이슈 수집
2. auto-fixable 이슈 발견 시:
   - task ID 중복 → 재번호 제안
   - 누락 status → "upcoming" 기본값 제안
   - showme 참조 중 registry 미등록 → registry 추가 제안
3. 사용자 확인 후 수정 적용
4. 재검증 (최대 2회)
5. 최종 판정:
   - `PASS`: critical 0건
   - `GOOD`: critical 0건 + warning 3건 이하
   - `FAIL`: critical 1건 이상
```

- [ ] **Step 6: SKILL.md 수정 — sync Error Recovery 추가**

`#### sync` 섹션의 절차를 Error Recovery 포함으로 교체:

```markdown
**절차 (Error Recovery 포함):**
1. `python3 tools/notion-sync.py --fetch-only` 실행
   - 실패 시 진단:
     - `NOTION_TOKEN` 미설정? → `export NOTION_TOKEN=...` 안내
     - 네트워크 오류? → 재시도 안내
     - 권한 오류? → Notion integration Connect 안내
   - 3회 재시도 후에도 실패 → "sync 불가" 리포트 + 마지막 성공 시점 출력
2. curriculum-notion.json + overrides.json → curriculum.json 자동 merge 확인
   - 예상 merge 결과와 현재 curriculum.json 비교
   - 불일치 시 diff 출력 + "이전 버전으로 복구하려면 `git checkout -- course-site/data/curriculum.json`" 안내
3. `/rpd-check` Phase 1 실행
   - critical 이슈 있으면 → result를 "partial"로 표시 + 이슈 목록 출력
4. 최종 판정: `success` / `partial` / `fail`
```

- [ ] **Step 7: SKILL.md 수정 — frontmatter, Gotchas, 로그, references 교체**

frontmatter:
```yaml
---
description: "커리큘럼 관리. 예: /curriculum validate, /curriculum add-week 4, /curriculum status done 1-5, /curriculum sync. DO NOT use for: 수업 내용 질문, ShowMe 카드 관련(/showme 사용)"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(python3:*), Bash(node:*), Bash(curl:*), Bash(wc:*), Bash(ls:*), Bash(cat:*), Agent
---
```

분리된 섹션 교체:
```markdown
### 레퍼런스 (필요 시 참조)

- 핵심 파일 경로: `references/file-paths.md`
- curriculum.js 파싱 패턴: `references/parsing-guide.md`
```

Gotchas 교체:
```markdown
## Gotchas ⚠️ (자동 축적)

스킬 실행 중 예상치 못한 실패/우회가 발생하면:
1. 이 섹션 하단에 한 줄 추가
2. 형식: `N. [날짜] 증상 → 원인 → 해결`
3. 같은 실수 반복 시 해당 항목에 빈도 카운터 추가

1. curriculum.json, curriculum-notion.json, curriculum.js는 generated file — 직접 수정 금지
2. 콘텐츠(title/copy/tasks) 수정은 반드시 Notion MCP 경로로
3. 에셋(image/showme/status/done) 수정은 overrides.json만
4. sync 실행 시 NOTION_TOKEN 환경변수 필요
```

로그 교체:
```markdown
## 실행 로그
​```bash
echo "[$(date '+%Y-%m-%d %H:%M')] mode=$MODE result=$RESULT quality=$QUALITY target=$TARGET" >> .claude/skill-logs/curriculum.log
​```
- `result`: `success` / `partial` / `fail`
- `quality`: `pass` / `warn` / `fail`
```

- [ ] **Step 8: 기존 curriculum.md 삭제**

```bash
rm .claude/commands/curriculum.md
```

- [ ] **Step 9: 검증 + 커밋**

```bash
ls -la .claude/commands/curriculum/
ls -la .claude/commands/curriculum/references/
head -5 .claude/commands/curriculum/SKILL.md

git add .claude/commands/curriculum/ .claude/commands/curriculum.md
git commit -m "feat(skill): /curriculum Progressive Disclosure + Iterative Refinement

- 단일 파일 → 폴더 구조 (SKILL.md + references/)
- validate: 재검증 루프 + PASS/GOOD/FAIL 판정
- sync: Error Recovery + 3단계 진단
- Gotchas 자동 축적 패턴, 실행 로그 표준화
- description에 negative trigger 추가"
```

---

### Task 3: `/rpd-check` 폴더 구조 변환

**Files:**
- Create: `.claude/commands/rpd-check/SKILL.md`
- Create: `.claude/commands/rpd-check/references/browser-verify.md`
- Create: `.claude/commands/rpd-check/references/fix-rules.md`
- Delete: `.claude/commands/rpd-check.md`

- [ ] **Step 1: 디렉토리 생성**

```bash
mkdir -p .claude/commands/rpd-check/references
```

- [ ] **Step 2: 기존 rpd-check.md를 SKILL.md로 복사**

```bash
cp .claude/commands/rpd-check.md .claude/commands/rpd-check/SKILL.md
```

- [ ] **Step 3: references/browser-verify.md 추출**

SKILL.md에서 `## Phase 2: Browser Verify` 전체 섹션 (119~200줄)을 잘라서 이동. SKILL.md에는 한 줄 참조만 남김:

```markdown
## Phase 2: Browser Verify

`week {N}` 또는 `all` 인자가 있을 때만 실행. 상세: `references/browser-verify.md`
```

- [ ] **Step 4: references/fix-rules.md 추출**

SKILL.md에서 `### --fix 자동 수정` 표 (256~267줄)를 잘라서 이동:

```markdown
# rpd-check --fix 자동 수정 규칙

| 이슈 | 자동 수정 | 방법 |
|------|----------|------|
| 누락 supplement | skeleton 생성 | `_supplements.json`에 템플릿 엔트리 추가 |
| task ID 중복 | 재번호 | 중복 ID를 순차 번호로 변경 |
| registry 누락 | 엔트리 추가 | curriculum의 showme ID를 registry에 추가 |
| 누락 이미지 | **수정 안 함** | 목록만 출력 (수동 대응) |
| orphan 파일 | **수정 안 함** | 목록만 출력 (수동 판단) |
| 테마 불일치 | **수정 안 함** | 목록만 출력 (CSS 수정 필요) |

## 재검증 루프

`--fix` 실행 시:
1. Phase 1 실행 → 이슈 수집
2. auto-fixable 항목 수정
3. Phase 1 재실행 (수정 검증)
4. 잔여 이슈만 리포트
5. 최종 PASS/FAIL 판정
```

- [ ] **Step 5: SKILL.md 수정 — Context-aware Scoping 추가**

`## 모드 분기` 표 아래에 Smart Scoping 섹션 추가:

```markdown
### Smart Scoping (인자 없을 때)

인자 없이 `/rpd-check` 실행 시, 최근 변경 파일 기반으로 관련 검증을 우선 실행:

```bash
git diff --name-only HEAD~3
```

| 변경 패턴 | 우선 검증 |
|----------|----------|
| `course-site/assets/showme/` | 1.3 ShowMe 카드 체인 |
| `course-site/assets/images/` | 1.1 이미지 검증 |
| `course-site/data/curriculum*` 또는 `overrides.json` | 1.4 데이터 구조 + 1.8 동기화 |
| 변경 없음 | Phase 1 전체 |

우선 검증 결과를 먼저 출력한 뒤, 나머지 Phase 1 항목도 실행.
```

- [ ] **Step 6: SKILL.md 수정 — Pass/Fail 판정 추가**

`## Phase 3: Report + Fix` 섹션의 리포트 출력 끝에 판정 기준 추가:

```markdown
### 최종 판정

```
PASS: critical 0건            → "✅ PASS (0 critical / N warning / N info)"
WARN: critical 0 + warning ≤5 → "⚠️ WARN (0 critical / N warning / N info)"
FAIL: critical ≥1             → "❌ FAIL (N critical / N warning / N info)"
```

판정 결과를 리포트 맨 마지막 줄에 출력.
```

- [ ] **Step 7: SKILL.md 수정 — frontmatter, Gotchas, 로그 교체**

frontmatter:
```yaml
---
description: "사이트 콘텐츠 검증. 예: /rpd-check, /rpd-check week 5, /rpd-check all, /rpd-check showme, /rpd-check --fix. DO NOT use for: 코드 품질 검증(/quality 사용), 배포 확인(/deploy 사용)"
allowed-tools: Read, Glob, Grep, Bash(ls:*), Bash(wc:*), Bash(stat:*), Bash(npx serve:*), Bash(git diff:*), Agent, Write, Edit
---
```

`allowed-tools`에 `Bash(git diff:*)` 추가 (Smart Scoping용).

Gotchas 교체 (기존 6개 항목을 자동 축적 패턴으로):
```markdown
## Gotchas ⚠️ (자동 축적)

스킬 실행 중 예상치 못한 실패/우회가 발생하면:
1. 이 섹션 하단에 한 줄 추가
2. 형식: `N. [날짜] 증상 → 원인 → 해결`
3. 같은 실수 반복 시 해당 항목에 빈도 카운터 추가

1. curriculum.json은 ~3800줄이므로 전체를 한 번에 읽는다 (분할 불필요)
2. `_registry.js`는 JS 파일이므로 JSON 파싱 불가 — Grep으로 키 추출
3. Phase 2 브라우저 검증 시 서버가 이미 떠 있으면 재기동하지 않는다
4. 외부 URL에 HTTP 요청을 보내지 않는다 (속도/안정성)
5. showme 모달 클릭 시 iframe 로드 시간이 필요하므로 짧은 대기 필요
6. 이미지 테마 검증 시 iframe cross-origin 제한 — 배경색만 확인
```

로그 교체:
```markdown
## 실행 로그
​```bash
echo "[$(date '+%Y-%m-%d %H:%M')] mode=$MODE result=$RESULT quality=$QUALITY critical=$CRITICAL warning=$WARNING info=$INFO" >> .claude/skill-logs/rpd-check.log
​```
- `result`: `success` / `partial` / `fail`
- `quality`: `pass` / `warn` / `fail`
```

- [ ] **Step 8: 기존 rpd-check.md 삭제**

```bash
rm .claude/commands/rpd-check.md
```

- [ ] **Step 9: 검증 + 커밋**

```bash
ls -la .claude/commands/rpd-check/
ls -la .claude/commands/rpd-check/references/
head -5 .claude/commands/rpd-check/SKILL.md
grep "Smart Scoping" .claude/commands/rpd-check/SKILL.md
grep "PASS\|FAIL" .claude/commands/rpd-check/SKILL.md

git add .claude/commands/rpd-check/ .claude/commands/rpd-check.md
git commit -m "feat(skill): /rpd-check Smart Scoping + Pass/Fail + Progressive Disclosure

- 단일 파일 → 폴더 구조 (SKILL.md + references/)
- Context-aware Scoping (git diff 기반 우선 검증)
- PASS/WARN/FAIL 최종 판정
- --fix 후 재검증 루프
- Gotchas 자동 축적 패턴, 실행 로그 표준화
- description에 negative trigger 추가"
```

---

### Task 4: Paperclip 이슈 등록

**Files:** 없음 (API 호출)

- [ ] **Step 1: Paperclip 서버 확인**

```bash
curl -s http://localhost:3100/api/companies
```

서버가 꺼져 있으면 → 사용자에게 `cd ~/Developer/Workspace/paperclip && pnpm dev` 안내.

- [ ] **Step 2: RPD 프로젝트/에이전트 매칭**

```bash
# 회사 목록에서 RPD 프로젝트를 가진 회사 찾기
curl -s http://localhost:3100/api/companies | python3 -c "import sys,json; [print(c['id'],c.get('name','')) for c in json.load(sys.stdin)]"
```

각 회사의 projects에서 현재 git 루트 (`/Users/ssongji/Developer/Workspace/RPD`)와 매칭되는 프로젝트 찾기.

- [ ] **Step 3: CTO 에이전트에게 이슈 생성**

```bash
curl -s -X POST "http://localhost:3100/api/companies/{COMPANY_ID}/issues" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "RPD 스킬 품질 표준화 — Anthropic PDF 5패턴 적용",
    "agentRole": "CTO",
    "description": "## 완료된 작업\n\n### /showme\n- Opus 4.6 모델 강제 (model: opus)\n- Progressive Disclosure: SKILL.md + references/ (css-reference, card-quality, template)\n- 품질 게이트: Step 3.5 자기 검증 루프 (개념/인터랙션/퀴즈 품질 체크, 최대 2회 재생성)\n- Success Criteria: 비유+why 포함, 프리셋 3개+핵심 설명, 상황 판단형 퀴즈 2문제 이상\n\n### /curriculum\n- Progressive Disclosure: SKILL.md + references/ (file-paths, parsing-guide)\n- validate 재검증 루프: auto-fix → 재검증 → PASS/GOOD/FAIL 판정\n- sync Error Recovery: 3단계 진단 (토큰/네트워크/권한) + rollback 안내\n\n### /rpd-check\n- Progressive Disclosure: SKILL.md + references/ (browser-verify, fix-rules)\n- Context-aware Scoping: git diff 기반 우선 검증\n- PASS/WARN/FAIL 최종 판정\n- --fix 후 재검증 루프\n\n### 공통\n- Gotchas 자동 축적 패턴\n- 실행 로그 표준화 (result + quality 필드)\n- frontmatter negative trigger 추가\n\n## 참조\n- Anthropic \"Complete Guide to Building Skills\" 5패턴\n- 스펙: docs/superpowers/specs/2026-04-06-skill-quality-upgrade-design.md",
    "priority": "medium"
  }'
```

- [ ] **Step 4: 이슈 생성 확인**

```bash
curl -s "http://localhost:3100/api/companies/{COMPANY_ID}/issues?limit=1" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d[0]['title'] if d else 'No issues')"
```

Expected: "RPD 스킬 품질 표준화 — Anthropic PDF 5패턴 적용"

- [ ] **Step 5: 커밋 (없음 — API 호출만)**

Paperclip 이슈는 외부 시스템이므로 커밋 불필요.

---

### Task 5: 최종 검증 + main 머지

- [ ] **Step 1: 전체 폴더 구조 검증**

```bash
echo "=== showme ==="
ls .claude/commands/showme/SKILL.md .claude/commands/showme/references/*.md
echo "=== curriculum ==="
ls .claude/commands/curriculum/SKILL.md .claude/commands/curriculum/references/*.md
echo "=== rpd-check ==="
ls .claude/commands/rpd-check/SKILL.md .claude/commands/rpd-check/references/*.md
echo "=== 기존 단일 파일 제거 확인 ==="
ls .claude/commands/showme.md .claude/commands/curriculum.md .claude/commands/rpd-check.md 2>&1
```

Expected: 3개 폴더 각각 SKILL.md + references/ 존재. 기존 `.md` 파일은 "No such file".

- [ ] **Step 2: frontmatter 검증**

```bash
for skill in showme curriculum rpd-check; do
  echo "=== $skill ==="
  head -4 .claude/commands/$skill/SKILL.md
  grep -c "DO NOT use for" .claude/commands/$skill/SKILL.md
done
```

Expected: 각 스킬에 `description` + negative trigger 포함. showme에 `model: opus`.

- [ ] **Step 3: main 머지**

```bash
git -C /Users/ssongji/Developer/Workspace/RPD merge claude/strange-hofstadter --no-edit
```

- [ ] **Step 4: 완료 확인**

```bash
git -C /Users/ssongji/Developer/Workspace/RPD log --oneline -5
```
