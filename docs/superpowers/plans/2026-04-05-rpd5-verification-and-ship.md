# RPD-5 Verification & Ship Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** RPD-5 커밋(92732d4)이 주장하는 3가지 작업 — (1) Notion Week 5/6 서술형 콘텐츠 동기화, (2) Week 5/6 design.md Rubric 재채점, (3) 원격 푸시 — 가 실제로 이루어졌는지 검증하고, 누락·불일치가 있으면 수정 후 원격에 푸시한다.

**Architecture:** 검증 우선 접근(verification-first). 커밋 주장을 맹신하지 않고 (a) 로컬 문서의 실제 내용, (b) Notion API 응답을 읽어 비교한다. 발견된 문제만 수정하고, 수정이 끝나면 별도 커밋으로 기록 후 `git push origin main`으로 배포한다.

**Tech Stack:**
- Python 3 + `tools/notion_api.py` (Notion 블록 조회)
- `curl` for Notion REST API
- Git CLI for commit & push
- Markdown (design.md 수정)

**전제 SoT 경계** (`docs/superpowers/specs/2026-04-05-edu-home-transition-design.md` §2):
| 대상 | SoT |
|------|-----|
| Step 구조 (순서, task ID, shortcuts) | `curriculum.js` |
| 서술형 본문 (설명, 튜토리얼) | Notion Week 5/6 페이지 |
| Rubric 채점 | `weeks/weekXX/design.md` |

**Notion 페이지 ID:**
- Week 5: `31354d654971811e85feed7681421e37`
- Week 6: `31354d654971818c8cb5e7814445e3eb`

---

## File Structure

### 검증 대상 (읽기 전용)
- `weeks/week05-ai3d-sculpting/design.md` — Rubric 재채점 검증
- `weeks/week06-material/design.md` — Rubric 재채점 + Remesh Step 1 반영 검증
- Notion Week 5 페이지 (Remesh 블록 제거 → "AI 초안 완성" 교체 검증)
- Notion Week 6 페이지 (Step 1 Remesh 블록 11개 추가 검증)

### 수정 가능 파일 (문제 발견 시만)
- `weeks/week05-ai3d-sculpting/design.md` — Rubric 수정
- `weeks/week06-material/design.md` — Rubric 수정
- Notion Week 5/6 페이지 — 블록 보완

### 산출물
- `.tmp/rpd5-verification-report.md` — 검증 결과 리포트 (임시, 커밋 대상 아님)
- Git 커밋 (수정 발생 시): `fix(content): RPD-5 검증 후 불일치 수정`
- `git push origin main` 실행

---

## Task 1: Week 5 design.md Rubric 재채점 검증

**Files:**
- Read: `weeks/week05-ai3d-sculpting/design.md`

**Background:** 커밋 메시지는 "Week 5 design.md: 끝 상태 Remesh 항목 → Week 6 참고 안내로 교체"라고 주장. Rubric 섹션이 Remesh 제거 반영해서 재채점됐는지 검증 필요.

- [ ] **Step 1: Week 5 design.md 전체 읽기**

Run:
```bash
wc -l weeks/week05-ai3d-sculpting/design.md
```
Expected: 파일 라인 수 출력 (100줄 이상 예상)

그다음 Read 도구로 전체 파일을 읽는다.

- [ ] **Step 2: Rubric 섹션 확인**

```bash
grep -n -A 20 "## 6. Rubric" weeks/week05-ai3d-sculpting/design.md
```

Expected: Rubric 채점표 4차원(학습 목표 구체성 / 개념 전달 / Stuck Map 완성도 / 평가 정합성) 각 점수와 근거가 표시됨. 근거 문구에 Remesh 제거가 반영돼 있어야 함.

검증 포인트:
- [ ] Rubric 채점표가 존재하는가?
- [ ] 각 차원에 1-5점이 부여됐는가?
- [ ] 근거 문구가 "Remesh Step 제거" 또는 "Week 6로 이동" 맥락을 언급하는가?
- [ ] 총점이 명시되는가?

- [ ] **Step 3: Stuck Map에서 Remesh 항목 제거 여부 확인**

```bash
grep -n "Remesh" weeks/week05-ai3d-sculpting/design.md
```

Expected: Remesh 언급은 "Week 6로 이동 안내" 맥락에서만 등장. Stuck Map 테이블에는 Remesh 관련 항목이 남아있지 않아야 함.

검증 포인트:
- [ ] Stuck Map 테이블에 Remesh 관련 행이 없는가?
- [ ] 평가 정합성 매핑표에 Remesh Step 매핑이 없는가?

- [ ] **Step 4: 검증 결과를 리포트 파일에 기록**

```bash
mkdir -p .tmp
```

`.tmp/rpd5-verification-report.md` 파일을 Write 도구로 생성:

```markdown
# RPD-5 Verification Report
Date: 2026-04-05

## Task 1: Week 5 design.md Rubric

- [x/✗] Rubric 채점표 존재: YES/NO
- [x/✗] Remesh 제거 반영된 근거 문구: YES/NO
- [x/✗] Stuck Map에서 Remesh 제거: YES/NO
- [x/✗] 평가 정합성 매핑에서 Remesh 제거: YES/NO

### 문제점 (있다면)
- ...

### 수정 필요 여부
- [x/✗] 수정 필요
```

---

## Task 2: Week 6 design.md Rubric 재채점 + Remesh Step 1 반영 검증

**Files:**
- Read: `weeks/week06-material/design.md`

**Background:** 커밋 메시지는 "Week 6 design.md: 시작 상태·끝 상태·Stuck Map·매핑·Rubric 재채점"이라고 주장. 실제로 신규 Step 1(Remesh)이 모든 섹션에 반영됐는지 검증 필요.

- [ ] **Step 1: Week 6 design.md 전체 읽기**

Read 도구로 `weeks/week06-material/design.md` 전체 파일을 읽는다.

- [ ] **Step 2: 시작 상태·끝 상태에 Remesh 반영 확인**

```bash
grep -n -A 10 "### 시작 상태\|### 끝 상태" weeks/week06-material/design.md
```

Expected: 끝 상태에 "Remesh로 AI 메쉬를 Material 적용 가능한 상태로 정리" 류의 항목 포함.

검증 포인트:
- [ ] 시작 상태가 "Week 5 종료 시점" 기준으로 갱신됐는가?
- [ ] 끝 상태에 Remesh 항목이 추가됐는가?
- [ ] 아하 모먼트 3개 중 Remesh 관련 항목이 포함됐는가?

- [ ] **Step 3: Stuck Map에 Remesh 항목 추가 확인**

```bash
grep -n "Step 1 (Remesh)" weeks/week06-material/design.md
```

Expected: 최소 3개 Remesh 관련 Stuck Map 행 존재.

검증 포인트:
- [ ] Stuck Map에 Step 1 Remesh 관련 막힘 지점 3개 이상 존재하는가?

- [ ] **Step 4: 평가 정합성 매핑에 Remesh Step 추가 확인**

```bash
grep -n -B 1 -A 1 "AI 메쉬 Remesh 정리\|Remesh 전후" weeks/week06-material/design.md
```

Expected: 평가 정합성 매핑 테이블에 "AI 메쉬 Remesh 정리 | Step 1 | Remesh 전후 폴리곤 수 비교 스크린샷" 류 행 존재.

- [ ] **Step 5: Rubric 재채점 확인**

```bash
grep -n -A 15 "## 6. Rubric" weeks/week06-material/design.md
```

Expected: 각 차원 점수와 근거 문구에 Remesh Step 1 추가가 반영됨. 총점이 이전 점수 대비 변동 여부 명시.

검증 포인트:
- [ ] 4차원 모두 채점됐는가?
- [ ] 근거 문구에 Remesh Step 1 추가가 언급되는가?
- [ ] 총점 변화가 명시됐는가? (이전 12점 → 현재 N점)

- [ ] **Step 6: 검증 결과를 리포트에 추가**

`.tmp/rpd5-verification-report.md`에 다음 섹션을 Edit 도구로 추가:

```markdown

## Task 2: Week 6 design.md Rubric + Remesh Step 1

- [x/✗] 시작 상태 갱신: YES/NO
- [x/✗] 끝 상태에 Remesh 항목 추가: YES/NO
- [x/✗] Stuck Map Remesh 3+ 항목: YES/NO
- [x/✗] 평가 정합성에 Remesh Step 매핑: YES/NO
- [x/✗] Rubric 재채점 (근거에 Remesh 반영): YES/NO
- [x/✗] 총점 변화 명시: YES/NO

### 문제점 (있다면)
- ...

### 수정 필요 여부
- [x/✗] 수정 필요
```

---

## Task 3: Notion Week 5 페이지 동기화 검증

**Files:**
- Read: Notion API via `tools/notion_api.py`

**Background:** 커밋 메시지는 "Week 5: 'Remesh와 마무리' 블록 → 'AI 초안 완성 및 .blend 저장'으로 교체"라고 주장. Notion API로 실제 Week 5 페이지 블록을 조회해 검증.

- [ ] **Step 1: Notion Week 5 페이지 블록 조회**

Run:
```bash
python3 -c "
from tools.notion_api import _get_page_blocks
blocks = _get_page_blocks('31354d654971811e85feed7681421e37')
print(f'Total blocks: {len(blocks)}')
for i, b in enumerate(blocks):
    btype = b.get('type','')
    text = ''
    if btype in b:
        rt = b[btype].get('rich_text', [])
        text = ''.join(r.get('plain_text','') for r in rt)
    print(f'{i:3} [{btype}] {text[:80]}')
" 2>&1 | head -60
```

Expected: Week 5 페이지의 모든 블록이 타입과 텍스트 첫 80자와 함께 출력됨.

- [ ] **Step 2: 'Remesh와 마무리' 제거 검증**

Run:
```bash
python3 -c "
from tools.notion_api import _get_page_blocks
blocks = _get_page_blocks('31354d654971811e85feed7681421e37')
found_old = False
found_new = False
for b in blocks:
    btype = b.get('type','')
    if btype not in b: continue
    rt = b[btype].get('rich_text', [])
    text = ''.join(r.get('plain_text','') for r in rt)
    if 'Remesh와 마무리' in text: found_old = True
    if 'AI 초안 완성' in text or '.blend 저장' in text: found_new = True
print(f'Old (Remesh와 마무리) present: {found_old}')
print(f'New (AI 초안 완성/.blend 저장) present: {found_new}')
"
```

Expected:
```
Old (Remesh와 마무리) present: False
New (AI 초안 완성/.blend 저장) present: True
```

검증 포인트:
- [ ] 'Remesh와 마무리' 블록이 Notion에서 제거됐는가?
- [ ] 'AI 초안 완성 및 .blend 저장' 블록이 새로 존재하는가?

- [ ] **Step 3: 검증 결과를 리포트에 추가**

`.tmp/rpd5-verification-report.md`에 Edit 도구로 추가:

```markdown

## Task 3: Notion Week 5 Page Sync

- [x/✗] 'Remesh와 마무리' 블록 제거: YES/NO
- [x/✗] 'AI 초안 완성 및 .blend 저장' 블록 추가: YES/NO

### 문제점 (있다면)
- ...

### 수정 필요 여부
- [x/✗] 수정 필요
```

---

## Task 4: Notion Week 6 페이지 동기화 검증

**Files:**
- Read: Notion API via `tools/notion_api.py`

**Background:** 커밋 메시지는 "Week 6: Step 1 Remesh 블록 11개 신규 추가"라고 주장. 실제로 11개 블록이 존재하고 Voxel Remesh / Quad Remesh / Decimate / QRemeshify / Mesh Cleaner 2가 다뤄지는지 검증.

- [ ] **Step 1: Notion Week 6 페이지 블록 조회**

Run:
```bash
python3 -c "
from tools.notion_api import _get_page_blocks
blocks = _get_page_blocks('31354d654971818c8cb5e7814445e3eb')
print(f'Total blocks: {len(blocks)}')
for i, b in enumerate(blocks):
    btype = b.get('type','')
    text = ''
    if btype in b:
        rt = b[btype].get('rich_text', [])
        text = ''.join(r.get('plain_text','') for r in rt)
    print(f'{i:3} [{btype}] {text[:80]}')
" 2>&1 | head -80
```

Expected: Week 6 페이지 모든 블록 출력. Step 1 Remesh 섹션이 시작 부분에 위치.

- [ ] **Step 2: 필수 키워드 존재 검증**

Run:
```bash
python3 -c "
from tools.notion_api import _get_page_blocks
blocks = _get_page_blocks('31354d654971818c8cb5e7814445e3eb')
all_text = ''
for b in blocks:
    btype = b.get('type','')
    if btype not in b: continue
    rt = b[btype].get('rich_text', [])
    all_text += ''.join(r.get('plain_text','') for r in rt) + '\n'

keywords = ['Voxel Remesh', 'Quad Remesh', 'Decimate', 'QRemeshify', 'Mesh Cleaner']
for kw in keywords:
    print(f'{kw}: {\"✓\" if kw in all_text else \"✗\"}')
print(f'\nTotal blocks: {len(blocks)}')
"
```

Expected: 5개 키워드 모두 `✓`.

검증 포인트:
- [ ] Voxel Remesh 언급 존재
- [ ] Quad Remesh 언급 존재
- [ ] Decimate 언급 존재
- [ ] QRemeshify 언급 존재
- [ ] Mesh Cleaner 언급 존재

- [ ] **Step 3: Step 1이 페이지 앞부분에 위치하는지 확인**

Step 2의 출력에서 위 키워드들이 페이지 상단(처음 20블록 이내)에 집중되어야 함.

검증 포인트:
- [ ] Remesh 관련 내용이 Material 관련 내용보다 앞에 나오는가?

- [ ] **Step 4: 검증 결과를 리포트에 추가**

`.tmp/rpd5-verification-report.md`에 Edit 도구로 추가:

```markdown

## Task 4: Notion Week 6 Page Sync

- [x/✗] Voxel Remesh 언급: YES/NO
- [x/✗] Quad Remesh 언급: YES/NO
- [x/✗] Decimate 언급: YES/NO
- [x/✗] QRemeshify 언급: YES/NO
- [x/✗] Mesh Cleaner 언급: YES/NO
- [x/✗] Remesh 섹션이 Material 앞에 위치: YES/NO

### 문제점 (있다면)
- ...

### 수정 필요 여부
- [x/✗] 수정 필요
```

---

## Task 5: 검증 결과 종합 및 수정 결정

**Files:**
- Read: `.tmp/rpd5-verification-report.md`

- [ ] **Step 1: 리포트 전체 읽기**

Read 도구로 `.tmp/rpd5-verification-report.md` 전체를 읽는다.

- [ ] **Step 2: 수정 필요 항목 집계**

리포트의 "수정 필요 여부" 항목을 모두 확인.

- 모든 Task에서 "수정 필요: NO" → Task 7(푸시)로 스킵
- 하나라도 "수정 필요: YES" → Task 6(수정)로 진행

- [ ] **Step 3: 사용자에게 보고**

수정 필요 항목이 있으면 사용자에게 리스트업해서 보고:

```
검증 결과: 총 N건 수정 필요

1. Week 5 design.md: [구체적 문제]
2. Notion Week 6: [구체적 문제]
...

수정하고 진행할까요?
```

**중요:** 사용자 승인 없이 Task 6 (수정) 진행 금지.

---

## Task 6: 수정 실행 (문제 발견 시만)

**Files:**
- Modify: (발견된 문제에 따라 달라짐)
  - `weeks/week05-ai3d-sculpting/design.md` (Rubric/Stuck Map)
  - `weeks/week06-material/design.md` (Rubric/Stuck Map/매핑)
  - Notion 페이지 (블록 추가/수정/삭제)

**Background:** Task 1-4에서 발견된 불일치를 수정. 각 항목별로 SoT 경계 준수:
- Rubric/Stuck Map → design.md (로컬 파일 Edit)
- 서술형 본문 → Notion API 호출

- [ ] **Step 1: design.md 문제 수정 (해당 시)**

Edit 도구로 `weeks/weekXX/design.md`의 해당 섹션 수정.

구체적 수정 내용은 Task 1-2에서 발견된 문제에 따라 결정됨. 예:
- 누락된 Rubric 차원 채점 추가
- Remesh 제거 반영 안 된 근거 문구 갱신
- Stuck Map 누락 항목 추가

각 수정 후:
```bash
grep -n "<수정한 문구>" weeks/weekXX-*/design.md
```
으로 반영 확인.

- [ ] **Step 2: Notion 페이지 문제 수정 (해당 시)**

구체적 수정 내용은 Task 3-4에서 발견된 문제에 따라 결정됨. 예:
- 누락된 키워드 블록 추가
- 잘못 남아있는 구버전 블록 삭제

Notion 블록 추가는 `tools/notion_api.py`의 `notion_request` 사용:
```python
from tools.notion_api import notion_request
# PATCH /blocks/{page_id}/children 로 블록 추가
```

수정 후 Task 3/4의 검증 스크립트 재실행해 통과 확인.

- [ ] **Step 3: 수정 완료 커밋**

```bash
git status
git diff weeks/
git add weeks/week05-ai3d-sculpting/design.md weeks/week06-material/design.md
```

`.tmp/` 디렉토리는 커밋하지 않는다.

```bash
git commit -m "$(cat <<'EOF'
fix(content): RPD-5 검증 후 불일치 수정

[발견된 문제]
- (실제 발견된 항목 나열)

[수정 내용]
- Week X design.md: ...
- Notion Week X: ...

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 4: 수정 결과 검증**

```bash
git log --oneline -3
```

Expected: 방금 만든 fix 커밋이 top에 표시됨.

---

## Task 7: 원격 푸시

**Files:**
- Git: push origin main

**Background:** `origin/main`보다 로컬이 12 커밋 앞서있음 (Task 6에서 수정 커밋 추가됐으면 13+). 검증 완료 후 푸시.

- [ ] **Step 1: 푸시 전 최종 상태 확인**

Run:
```bash
git status
git log --oneline origin/main..HEAD
```

Expected:
- `git status`: clean working tree (untracked 파일은 있을 수 있음)
- `git log`: 푸시할 커밋 목록 (최소 12개, Task 6 수행 시 13+)

- [ ] **Step 2: 사용자에게 푸시 목록 보고 후 승인 받기**

푸시할 커밋 목록을 사용자에게 보여주고 승인 받기:

```
origin/main에 푸시할 커밋 N개:
<git log 출력>

푸시할까요?
```

**중요:** 사용자 승인 없이 push 금지.

- [ ] **Step 3: 원격 푸시**

Run:
```bash
git push origin main
```

Expected: `To github.com:ssongji1122/RPD.git` + `<old>..<new>  main -> main` 출력.

실패 시(rejected): 원인 분석 후 사용자에게 보고. force push 금지.

- [ ] **Step 4: 푸시 성공 확인**

```bash
git status
```

Expected: `Your branch is up to date with 'origin/main'.`

- [ ] **Step 5: 임시 리포트 정리**

```bash
rm .tmp/rpd5-verification-report.md
```

`.tmp/` 전체는 이미 `.gitignore`에 있을 가능성 높음 — 확인:
```bash
grep -n "\.tmp" .gitignore 2>/dev/null || echo "not in gitignore"
```

없으면 사용자에게 `.gitignore`에 추가할지 질문 (이 플랜 범위 밖).

- [ ] **Step 6: 최종 보고**

사용자에게 요약 보고:

```
✅ RPD-5 검증 & 배포 완료

검증 결과:
- Week 5 design.md Rubric: PASS/FIXED
- Week 6 design.md Rubric + Remesh Step 1: PASS/FIXED
- Notion Week 5 동기화: PASS/FIXED
- Notion Week 6 동기화: PASS/FIXED

푸시 결과:
- N개 커밋 origin/main에 반영 완료
- 수업일 2026-04-07 전 배포 완료
```

---

## Success Criteria

- [ ] Week 5 design.md Rubric 4차원 채점이 Remesh 제거 반영한 근거 문구를 가진다
- [ ] Week 6 design.md Rubric 4차원 채점이 Remesh Step 1 추가 반영한 근거 문구를 가진다
- [ ] Week 6 design.md Stuck Map에 Remesh 관련 항목 3개 이상 존재
- [ ] Week 6 design.md 평가 정합성 매핑에 "AI 메쉬 Remesh 정리 | Step 1" 행 존재
- [ ] Notion Week 5 페이지에 'Remesh와 마무리' 블록 없음
- [ ] Notion Week 5 페이지에 'AI 초안 완성' 또는 '.blend 저장' 블록 존재
- [ ] Notion Week 6 페이지에 Voxel Remesh / Quad Remesh / Decimate / QRemeshify / Mesh Cleaner 키워드 모두 존재
- [ ] Notion Week 6 페이지에서 Remesh 섹션이 Material 섹션 앞에 위치
- [ ] `git status`가 "up to date with origin/main"을 반환
- [ ] 수업일(2026-04-07) 전 푸시 완료
