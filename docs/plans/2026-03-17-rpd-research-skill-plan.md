# /rpd-research 스킬 구현 계획

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 블렌더 교안 콘텐츠의 정확성을 보장하는 리서치 전용 스킬 `/rpd-research` 구현

**Architecture:** Claude Code 스킬 파일(`.claude/skills/rpd-research/SKILL.md`) + 리서치 브리프 출력 디렉토리(`claudedocs/research/`). 스킬은 Phase 1~4 파이프라인(공식소스→커뮤니티→크로스체크→가공)을 정의하고, 기존 스킬들이 브리프를 자동 참조하도록 연동한다.

**Tech Stack:** Claude Code Skill (Markdown), WebFetch, WebSearch, Context7 MCP, Agent tool (병렬)

---

### Task 1: 리서치 브리프 출력 디렉토리 생성

**Files:**
- Create: `claudedocs/research/.gitkeep`

**Step 1: 디렉토리 생성**

```bash
mkdir -p claudedocs/research
touch claudedocs/research/.gitkeep
```

**Step 2: .gitignore 확인**

claudedocs/가 gitignore에 포함되어 있는지 확인. 리서치 브리프는 버전 관리에 포함되어야 하므로 ignore되면 안 됨.

```bash
grep -n "claudedocs" .gitignore
```

Expected: 매칭 없음 (또는 있으면 제거)

**Step 3: Commit**

```bash
git add claudedocs/research/.gitkeep
git commit -m "chore: claudedocs/research/ 디렉토리 생성"
```

---

### Task 2: 스킬 파일 생성 — 기본 구조

**Files:**
- Create: `.claude/skills/rpd-research/SKILL.md`
- Reference: `.claude/skills/rpd-content-write/SKILL.md` (구조 참고)
- Reference: `docs/plans/2026-03-17-rpd-research-skill-design.md` (설계 문서)

**Step 1: 스킬 파일 작성**

`.claude/skills/rpd-research/SKILL.md` 내용:

```markdown
---
name: rpd-research
description: 블렌더/디자인 교안 콘텐츠 리서치. 공식 문서 + 커뮤니티 혼란 포인트 수집, 크로스팩트체크 후 검증된 브리프 생성. Use before /rpd-content-write or /showme to ensure content accuracy.
---

# RPD Research — 교안 콘텐츠 리서치 스킬

## 호출

\`\`\`
/rpd-research {tool-id}              # 단일 도구 리서치
/rpd-research {tool-id} --deep       # 연관 개념 재귀 탐색 (깊이 2)
/rpd-research week {N}               # 주차 전체 리서치
\`\`\`

## 출력

`claudedocs/research/{tool-id}-brief.md`

## 모드 분기

**`{tool-id}`**: 단일 도구/개념 리서치 → 아래 Phase 1~4 실행
**`{tool-id} --deep`**: 단일 리서치 + 연관 개념 재귀 (최대 깊이 2, 각 재귀는 병렬 Agent)
**`week {N}`**: curriculum.js에서 주차 N의 showme ID 추출 → 각 ID별 병렬 리서치 → week summary 생성

---

## Phase 1: 공식 소스 수집 (정확성)

### 1-1. Blender 공식 문서 (WebFetch)

대상 URL 패턴:
| 카테고리 | URL |
|----------|-----|
| Generate 모디파이어 | `https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/{name}.html` |
| Mesh 도구 | `https://docs.blender.org/manual/en/latest/modeling/meshes/tools/{tool}.html` |
| Edge 편집 | `https://docs.blender.org/manual/en/latest/modeling/meshes/editing/edge/{tool}.html` |
| Mesh 편집 | `https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/{tool}.html` |
| Sculpt 도구 | `https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/{tool}.html` |
| 조명 | `https://docs.blender.org/manual/en/latest/render/lights/{type}.html` |
| 재질 | `https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/{node}.html` |

추출 항목:
- 공식 정의 (영어 원문)
- 파라미터 테이블 (이름, 기본값, 설명)
- 관련 단축키
- See Also / Related 링크

### 1-2. Blender Python API (Context7 MCP)

```
--c7 → resolve-library-id "blender" → query-docs "{tool-id}"
```

추출 항목:
- API에서의 정확한 이름/경로
- 프로그래밍적 접근 시 파라미터명

### 1-3. 릴리즈 노트 (WebFetch)

최근 3개 버전의 변경사항 확인:
```
https://wiki.blender.org/wiki/Reference/Release_Notes/4.x
```

**Phase 1 내부는 1-1, 1-2, 1-3 모두 병렬 실행.**

---

## Phase 2: 학생 혼란 포인트 수집 (공감)

### 2-1. 영어 커뮤니티 (WebSearch)

병렬 검색 3개:
```
"{tool-name} blender" site:reddit.com/r/blender
"{tool-name}" site:blender.stackexchange.com
"{tool-name} blender tutorial common mistake"
```

### 2-2. 한글 커뮤니티 (WebSearch)

```
"블렌더 {한글명}" site:cafe.naver.com OR site:clien.net OR site:arca.live
```

### 수집 기준

- 상위 5-10개 반복 질문 패턴 식별
- 각 질문에 출처 URL 기록
- "왜 안 되죠?" / "이해가 안 돼요" 패턴 우선 수집

**Phase 2 내부도 모두 병렬 실행.**

---

## Phase 3: 크로스체크 + 연관 개념 그래프

### 3-1. 팩트체크

Phase 2에서 수집한 각 커뮤니티 답변을 Phase 1 공식 정보와 대조:
- ✅ 정확: 그대로 채택
- ⚠️ 부분 정확: 정정 사항 명시
- ❌ 오류: 올바른 정보로 대체 + 왜 틀린지 설명

### 3-2. 연관 개념 그래프 구성

Phase 2 질문에서 역추적:
- **선수 지식**: "이 질문을 하려면 뭘 몰라야 하는가?"
  - 예: Loop Cut 질문 → 점·선·면 위계를 모름
- **연결 개념**: "이 도구와 자주 함께 쓰이는 것"
  - 예: Loop Cut + Subdivision Surface
- **심화**: "알면 이해가 깊어지는 원리"
  - 예: N-gon → Circle 근사, 해상도 vs 폴리곤 수

---

## Phase 4: 교안용 가공

### 4-1. CONTENT_GUIDE.md 톤 적용

참조 파일: `course-site/CONTENT_GUIDE.md`

규칙:
- ~해요/~이에요 존댓말
- 결론 먼저
- 비유는 학생이 이미 경험한 것에서

### 4-2. 출력 포맷

`claudedocs/research/{tool-id}-brief.md`:

```markdown
# 리서치 브리프: {한글 이름} ({영문 이름})
> 생성일: {YYYY-MM-DD} | 소스: Blender {버전}

## 1. 공식 정의
- **영문**: {Blender Docs 원문}
- **한글 풀이**: {쉬운 설명}
- **공식 문서**: {URL}

## 2. 핵심 파라미터
| 파라미터 | 기본값 | 설명 | 학생에게 중요한 이유 |
|---------|-------|------|-------------------|

## 3. 단축키
| 키 | 동작 | 컨텍스트 | 비고 |
|----|------|---------|------|

## 4. 연관 개념 그래프
### 선수 지식 (이걸 모르면 이해 불가)
- **{개념}**: {왜 필요한지 한 줄}

### 연결 개념 (함께 쓰이는 것)
- **{개념}**: {조합 시 효과}

### 심화 (알면 이해가 깊어지는 것)
- **{개념}**: {원리}

## 5. 학생 혼란 포인트
| # | 질문 (실제) | 출처 | 검증된 답변 |
|---|-----------|------|-----------|

## 6. 흔한 실수 & 해결
| 증상 | 원인 | 해결 |
|------|------|------|

## 7. 추천 비유 후보
1. **{비유}** — {왜 이 비유가 맞는지}

## 8. 크로스체크 로그
| 주장 | 소스 | 검증 | 결과 |
|------|------|------|------|
```

---

## `--deep` 모드 추가 동작

Phase 3에서 식별된 선수 지식 각각에 대해:
1. 이미 `claudedocs/research/{concept}-brief.md`가 있는지 확인
2. 없으면 → 병렬 Agent로 해당 개념 리서치 (깊이+1)
3. 깊이 2 도달 시 중단, 참조 링크만 기록

```
/rpd-research loop-cut --deep
  ├── loop-cut-brief.md (깊이 0)
  ├── vertex-edge-face-brief.md (깊이 1, 병렬 Agent)
  ├── subdivision-concept-brief.md (깊이 1, 병렬 Agent)
  └── 깊이 2 → 중단
```

---

## `week N` 모드 추가 동작

1. `course-site/data/curriculum.js` 읽기
2. week N의 모든 step에서 `showme` 필드 추출
3. 각 showme ID별 병렬 Agent로 개별 리서치
4. 완료 후 `claudedocs/research/week{NN}-summary.md` 생성:

```markdown
# Week {N} 리서치 요약: {주차 제목}

## 개념 흐름
{카드 간 관계 설명}

## 학습 순서 권장
{선수지식 기반 권장 순서}

## 개별 브리프
- [{card-id}](./card-id-brief.md)
- ...
```

---

## 기존 스킬 연동 (수정 필요)

### rpd-content-write 수정

`.claude/skills/rpd-content-write/SKILL.md` 상단에 추가:

```markdown
## 리서치 브리프 참조

작업 시작 전 `claudedocs/research/{관련-id}-brief.md` 존재 여부 확인:
- 있으면 → 비유, 실수, 단축키를 브리프에서 가져와 curriculum.js에 반영
- 없으면 → "⚠️ {id} 리서치 브리프가 없습니다. `/rpd-research {id}` 를 먼저 실행하세요."
```

### showme 스킬 수정

`.claude/commands/showme.md` Step 2 직전에 추가:

```markdown
#### Step 1.5: 리서치 브리프 확인
`claudedocs/research/{widget-id}-brief.md` 존재 시:
- 개념탭: 브리프 §1 공식정의 + §7 비유 활용
- 퀴즈탭: 브리프 §5 학생혼란포인트에서 문제 출제
- 단축키: 브리프 §3에서 검증된 단축키 사용
```

---

## 검증

스킬 생성 후 테스트:
```
/rpd-research mirror-modifier
```

확인 항목:
- [ ] Phase 1: 공식 문서 URL 접근 + 파라미터 추출 성공
- [ ] Phase 2: Reddit/StackExchange 검색 결과 5개 이상
- [ ] Phase 3: 크로스체크 로그 작성됨
- [ ] Phase 4: 브리프 파일 생성됨 (`claudedocs/research/mirror-modifier-brief.md`)
- [ ] 브리프 구조가 템플릿과 일치
- [ ] 연관 개념 그래프에 선수지식 1개 이상
```

---

### Task 3: 스킬 파일 생성 — SKILL.md 작성

**Files:**
- Create: `.claude/skills/rpd-research/SKILL.md`
- Reference: `docs/plans/2026-03-17-rpd-research-skill-design.md`

**Step 1: 스킬 파일 작성**

Task 2의 Step 1에 정의된 전체 내용을 `.claude/skills/rpd-research/SKILL.md`에 작성.

**Step 2: 스킬 등록 확인**

Claude Code는 `.claude/skills/` 하위 디렉토리의 `SKILL.md`를 자동 감지. 별도 등록 불필요.

```bash
ls .claude/skills/rpd-research/SKILL.md
```

Expected: 파일 존재

**Step 3: Commit**

```bash
git add .claude/skills/rpd-research/SKILL.md
git commit -m "feat: /rpd-research 스킬 생성 — 교안 리서치 전용"
```

---

### Task 4: 기존 스킬 연동 수정

**Files:**
- Modify: `.claude/skills/rpd-content-write/SKILL.md`
- Modify: `.claude/commands/showme.md`

**Step 1: rpd-content-write에 브리프 참조 섹션 추가**

파일 상단 (## 대상 파일 섹션 직전)에 추가:

```markdown
## 리서치 브리프 참조

작업 시작 전 `claudedocs/research/{관련-id}-brief.md` 존재 여부 확인:
- 있으면 → 비유, 실수, 단축키를 브리프에서 가져와 curriculum.js에 반영
- 없으면 → "⚠️ {id} 리서치 브리프가 없습니다. `/rpd-research {id}` 먼저 실행을 권장합니다."
```

**Step 2: showme 스킬에 브리프 참조 추가**

`.claude/commands/showme.md`의 Step 2 (HTML 생성) 직전에 추가:

```markdown
#### Step 1.5: 리서치 브리프 확인
`claudedocs/research/{widget-id}-brief.md` 존재 시:
- 개념탭: 브리프 §1 공식정의 + §7 비유 활용
- 퀴즈탭: 브리프 §5 학생혼란포인트에서 문제 출제
- 단축키: 브리프 §3에서 검증된 단축키 사용
- 흔한 실수: 브리프 §6에서 가져오기
```

**Step 3: Commit**

```bash
git add .claude/skills/rpd-content-write/SKILL.md .claude/commands/showme.md
git commit -m "feat: rpd-content-write, showme 스킬에 리서치 브리프 연동 추가"
```

---

### Task 5: 테스트 — mirror-modifier 리서치 실행

**Step 1: 스킬 실행**

```
/rpd-research mirror-modifier
```

**Step 2: 출력 파일 확인**

```bash
cat claudedocs/research/mirror-modifier-brief.md
```

Expected:
- 8개 섹션 모두 존재
- 공식 문서 URL 유효
- 크로스체크 로그 1개 이상
- 연관 개념 1개 이상

**Step 3: Commit 브리프**

```bash
git add claudedocs/research/mirror-modifier-brief.md
git commit -m "docs: mirror-modifier 리서치 브리프 생성 (테스트)"
```

---

### Task 6: 테스트 — --deep 모드

**Step 1: deep 모드 실행**

```
/rpd-research mirror-modifier --deep
```

**Step 2: 재귀 브리프 확인**

```bash
ls claudedocs/research/
```

Expected: `mirror-modifier-brief.md` + 선수지식 브리프 1개 이상

**Step 3: Commit**

```bash
git add claudedocs/research/
git commit -m "docs: mirror-modifier --deep 리서치 브리프들"
```

---

### Task 7: 테스트 — week 모드

**Step 1: week 모드 실행**

```
/rpd-research week 2
```

**Step 2: 주차 요약 + 개별 브리프 확인**

```bash
ls claudedocs/research/week02*
ls claudedocs/research/
```

Expected: `week02-summary.md` + 해당 주차 showme ID별 브리프

**Step 3: Commit**

```bash
git add claudedocs/research/
git commit -m "docs: week 2 전체 리서치 브리프"
```
