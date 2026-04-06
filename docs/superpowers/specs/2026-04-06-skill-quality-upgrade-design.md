# RPD 스킬 품질 표준화 — Anthropic PDF 5패턴 적용

**날짜:** 2026-04-06
**범위:** `/showme`, `/curriculum`, `/rpd-check` 3개 핵심 스킬 업그레이드
**상태:** Approved
**참조:** Anthropic "The Complete Guide to Building Skills for Claude" (33p)

---

## 1. 목표

Anthropic 공식 스킬 빌딩 가이드의 5가지 패턴을 기존 RPD 프로젝트 스킬에 적용하여, 실행 품질의 일관성과 결과물 깊이를 개선한다.

### 적용 패턴

| 패턴 | 적용 대상 |
|------|----------|
| Pattern 1: Sequential Workflow | showme, curriculum |
| Pattern 3: Iterative Refinement | showme, curriculum, rpd-check |
| Pattern 4: Context-aware Selection | rpd-check |
| Pattern 5: Domain-specific Intelligence | showme |
| Progressive Disclosure | 전체 |

### 공통 문제점 (현재)

1. 검증 후 재시도 없음 — 결과물이 기준 미달이어도 그대로 출력
2. 성공/실패 기준 불명확 — 언제가 "완료"인지 정의 없음
3. 한 파일에 모든 내용 — Progressive Disclosure 미적용
4. 에러 복구 방법 없음 — 실패 시 사용자가 알아서 해결
5. Gotchas 비어있음 — 실패 경험이 축적되지 않음

---

## 2. `/showme` 개선

### 2.1 모델 강제

frontmatter에 `model: opus` 추가. SKILL.md 본문 최상단에 품질 철학 명시:

```
이 스킬은 반드시 Opus 4.6 모델로 실행해야 합니다.
표면적 정의가 아닌, Blender를 실제로 쓸 때 학생이 겪는
혼란과 깨달음을 관통하는 카드를 만드세요.
```

### 2.2 Progressive Disclosure

```
.claude/commands/showme/
├── SKILL.md              # 모드 분기 + 생성 절차 (핵심만)
└── references/
    ├── css-reference.md   # CSS 변수/컴포넌트 표
    ├── card-quality.md    # 품질 기준 + 좋은/나쁜 예시
    └── template.md        # HTML 골격
```

현재 SKILL.md에서 분리할 내용:
- CSS 변수 레퍼런스 (현재 158~165줄) → `references/css-reference.md`
- CSS 컴포넌트 요약 (167~182줄) → `references/css-reference.md`
- HTML 골격 템플릿 (54~83줄) → `references/template.md`
- Blender 공식 문서 URL 패턴 (184~191줄) → `references/template.md`

### 2.3 품질 게이트 (Iterative Refinement)

Step 3 (HTML 생성) 이후 자동 검증 루프:

```
Step 3.5: 자기 검증
1. 개념탭: 각 concept-card에 "왜 이게 중요한지" 설명이 있는가?
   → 단순 정의만이면 FAIL
2. interaction탭: 슬라이더/프리셋이 학습 포인트와 연결되는가?
   → 무관한 파라미터만 있으면 FAIL
3. 퀴즈: 암기가 아닌 이해를 묻는가?
   → 단순 용어 질문만이면 FAIL
4. FAIL이면 → 해당 탭 재생성 (최대 2회)
```

### 2.4 Success Criteria

- 개념 카드에 "비유(analogy)" + "왜 중요한지(why)" 둘 다 포함
- interaction 데모에 프리셋 3개 이상 + 각 프리셋에 "이 조합의 핵심" 설명
- 퀴즈 5문제 중 최소 2문제가 "상황 판단형" (단순 암기 X)
- doc-ref 공식 문서 링크 포함
- 모바일 반응형 + 터치 이벤트 지원

### 2.5 `references/card-quality.md` 내용

좋은 카드 vs 나쁜 카드 비교 예시:

**나쁜 개념 카드:**
```
Mirror Modifier는 오브젝트를 대칭 복제하는 모디파이어입니다.
```

**좋은 개념 카드:**
```
Mirror Modifier는 오브젝트를 축 기준으로 대칭 복제합니다.
캐릭터나 차량처럼 좌우 대칭인 모델을 만들 때, 한쪽만 작업하면
반대쪽이 자동으로 따라옵니다. 작업량이 절반으로 줄어요.

비유: 종이를 반으로 접고 한쪽만 오리면 대칭 무늬가 나오는 것
```

**나쁜 퀴즈:**
```
Q: Mirror Modifier의 한글 이름은?
→ 용어 암기. 학습에 도움 안 됨.
```

**좋은 퀴즈:**
```
Q: 자동차 모델링 중 한쪽 문만 수정했는데 반대쪽에 반영이 안 됩니다.
   가장 가능성 높은 원인은?
→ 상황 판단. 실제 사용 시 겪는 문제 해결력 측정.
```

---

## 3. `/curriculum` 개선

### 3.1 `validate` → Iterative Refinement

현재: 검증 → 리포트 → 끝
개선:
```
validate 실행
  → 이슈 발견 → severity별 분류
  → auto-fixable 항목 자동 수정 제안 (사용자 확인)
  → 수정 후 재검증
  → 통과할 때까지 (최대 2회)
```

Auto-fixable 항목:
- task ID 중복 → 재번호
- 누락 status → "upcoming" 기본값
- showme 참조 중 registry 미등록 → registry에 추가

### 3.2 `sync` Error Recovery

```
sync 실행
  → Step 1: notion-sync.py 실행
    → 실패 시: NOTION_TOKEN 확인 → 네트워크 확인 → 재시도 안내
  → Step 2: merge 결과 검증
    → curriculum.json과 예상 merge 불일치 시 diff 출력 + 롤백 안내
  → Step 3: /rpd-check Phase 1
    → critical 이슈 있으면 sync 결과 "부분 성공"으로 표시
```

### 3.3 Success Criteria

```
validate: critical 0건이면 PASS, warning 3건 이하면 GOOD
sync: curriculum.json 재생성 + rpd-check critical 0건
add-week: 새 주차가 validate 통과 + 이미지 디렉토리 존재
```

### 3.4 Progressive Disclosure

```
.claude/commands/curriculum/
├── SKILL.md              # 모드 분기 + 핵심 절차
└── references/
    ├── file-paths.md      # 핵심 파일 경로 표
    └── parsing-guide.md   # curriculum.js 파싱 패턴
```

분리 대상:
- 핵심 파일 경로 표 (128~153줄) → `references/file-paths.md`
- curriculum.js 파싱 패턴 (145~153줄) → `references/parsing-guide.md`

---

## 4. `/rpd-check` 개선

### 4.1 Context-aware Scoping (Pattern 4)

```
/rpd-check (인자 없음)
  → git diff --name-only HEAD~3 분석
  → showme 파일 변경됨? → ShowMe 체인 검증 우선
  → images/ 변경됨? → 이미지 검증 우선
  → curriculum 관련 변경? → 데이터 구조 검증 우선
  → 변경 없음? → Phase 1 전체
```

우선 실행된 검증 결과를 먼저 출력하고, 나머지는 백그라운드에서 실행.

### 4.2 Pass/Fail 판정 기준

```
PASS: critical 0건
WARN: critical 0건 + warning 5건 이하
FAIL: critical 1건 이상

최종 한 줄: "✅ PASS (0 critical / 2 warning / 3 info)"
또는: "❌ FAIL (1 critical / 3 warning / 1 info)"
```

### 4.3 `--fix` 후 재검증 루프

```
/rpd-check --fix
  → Phase 1 실행 → 이슈 수집
  → auto-fixable 항목 수정
  → Phase 1 재실행 (수정 검증)
  → 잔여 이슈만 리포트
  → 최종 PASS/FAIL 판정
```

### 4.4 Progressive Disclosure

```
.claude/commands/rpd-check/
├── SKILL.md              # 모드 분기 + Phase 1 핵심
└── references/
    ├── browser-verify.md  # Phase 2 브라우저 검증 상세
    └── fix-rules.md       # --fix 자동 수정 규칙표
```

분리 대상:
- Phase 2 브라우저 검증 전체 (119~200줄) → `references/browser-verify.md`
- --fix 자동 수정 규칙표 (256~267줄) → `references/fix-rules.md`

---

## 5. 공통 적용

### 5.1 Gotchas 자동 축적

세 스킬 모두 동일 패턴:

```markdown
## Gotchas ⚠️ (자동 축적)

스킬 실행 중 예상치 못한 실패/우회가 발생하면:
1. 이 섹션 하단에 한 줄 추가
2. 형식: `N. [날짜] 증상 → 원인 → 해결`
3. 같은 실수 반복 시 해당 항목에 빈도 카운터 추가
```

### 5.2 실행 로그 표준화

```bash
echo "[$(date '+%Y-%m-%d %H:%M')] mode=$MODE result=$RESULT quality=$QUALITY target=$TARGET" >> .claude/skill-logs/{skill}.log
```

- `result`: `success` / `partial` / `fail`
- `quality`: `pass` / `warn` / `fail` (검증 결과)

### 5.3 frontmatter 개선

각 스킬의 description에 negative trigger 추가:

```yaml
# showme
description: "Show Me 교육 카드 생성. 예: /showme array-modifier.
  DO NOT use for: 카드 내용 질문, 기존 카드 수정(Edit 사용), 보충 설명(/brainstormC 사용)"

# curriculum
description: "커리큘럼 관리. 예: /curriculum validate.
  DO NOT use for: 수업 내용 질문, ShowMe 카드 관련(/showme 사용)"

# rpd-check
description: "사이트 콘텐츠 검증. 예: /rpd-check.
  DO NOT use for: 코드 품질 검증(/quality 사용), 배포 확인(/deploy 사용)"
```

---

## 6. Paperclip 전달

스킬 개선 완료 후 Paperclip 이슈 등록:

```
제목: RPD 스킬 품질 표준화 — Anthropic PDF 5패턴 적용
담당: CTO
내용:
- /showme: Opus 4.6 강제, 품질 게이트, Progressive Disclosure
- /curriculum: Validation Gate, Error Recovery, 재검증 루프
- /rpd-check: Smart Scoping, Pass/Fail 판정, --fix 후 재검증
- 공통: Gotchas 자동 축적, 실행 로그 표준화, negative triggers
- 참조: Anthropic "Complete Guide to Building Skills" 5패턴
```

---

## 7. 구현 순서

### 폴더 구조 변환 방법

현재 `.claude/commands/showme.md` (단일 파일) →  `.claude/commands/showme/SKILL.md` + `references/` (폴더 구조)로 변환.

절차:
1. `.claude/commands/{skill}/` 디렉토리 생성
2. `.claude/commands/{skill}.md` → `.claude/commands/{skill}/SKILL.md`로 이동
3. 분리 대상 내용을 `references/*.md`로 추출
4. SKILL.md에서 해당 내용 제거 + `references/` 파일 참조 안내 추가

### 실행 순서

1. `/showme` — 폴더 구조 변환 + model:opus + 품질 게이트 + references/ + card-quality.md 작성
2. `/curriculum` — 폴더 구조 변환 + validate 재검증 + sync recovery + references/
3. `/rpd-check` — 폴더 구조 변환 + smart scoping + pass/fail + references/
4. 공통 — Gotchas 패턴, 로그 표준화, frontmatter negative triggers
5. Paperclip 이슈 등록

---

## 8. 범위 외

- 나머지 7개 RPD 스킬 (brainstormC, capture, lessonforge 등) — 이 3개 패턴 검증 후 점진 확산
- 유저 레벨 스킬 (SC 26개 등) — 이번 범위 아님
- Hook 개선 — 별도 스펙 필요 (CC101 가이드 참조)
