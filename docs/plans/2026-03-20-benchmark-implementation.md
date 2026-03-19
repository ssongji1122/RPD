# Benchmark Design Rules Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** tokens.css를 벤치마크 규칙에 맞게 통일하고, prototype.html에 탐색/학습 모드 온도 차이를 적용한다.

**Architecture:** tokens.css의 스페이싱/radius/fw 스케일을 벤치마크 규칙 값으로 교체하고, 학습 모드용 토큰 셋(`[data-mode="learn"]`)을 추가한다. prototype.html을 수정하여 레일 비율/여백/타이포를 벤치마크 기준에 맞춘다.

**Tech Stack:** CSS custom properties, HTML data attributes

**참조 문서:** `docs/plans/2026-03-20-benchmark-design-rules.md`

---

### Task 1: tokens.css — 스페이싱 토큰 추가

**Files:**
- Modify: `course-site/assets/tokens.css:78-86`

**Step 1: tokens.css의 `:root` 블록에 스페이싱 스케일 추가**

기존 `--radius` 라인 위에 삽입:

```css
/* Spacing scale (Vercel/Geist 기준 — 이 값만 허용) */
--sp-1:  4px;
--sp-2:  8px;
--sp-3:  12px;
--sp-4:  16px;
--sp-6:  24px;
--sp-8:  32px;
--sp-12: 48px;
--sp-16: 64px;
```

**Step 2: 커밋**

```bash
git add course-site/assets/tokens.css
git commit -m "feat(tokens): add spacing scale tokens (4-64px, Vercel/Geist based)"
```

---

### Task 2: tokens.css — border-radius 스케일 통일

**Files:**
- Modify: `course-site/assets/tokens.css:80-86`

**Step 1: 기존 radius 토큰을 벤치마크 스케일로 교체**

변경 전:
```css
--radius: 12px;
--radius-sm: 10px;
--radius-md: 14px;
--radius-lg: 18px;
--radius-xl:   24px;
--radius-2xl:  28px;
--radius-pill: 999px;
```

변경 후:
```css
/* Border-radius scale (벤치마크 기준 — 이 값만 허용) */
--radius-sm:   8px;   /* 인풋, 작은 칩 */
--radius:      12px;  /* 카드, 버튼 */
--radius-md:   16px;  /* 서브 패널 */
--radius-lg:   20px;  /* 섹션 컨테이너 */
--radius-xl:   24px;  /* 사이드바, 검색바 */
--radius-pill: 999px; /* 칩, 필터, 뱃지 */
```

`--radius-2xl` 삭제 (28px는 스케일에 없음). 기존 `--radius-2xl` 사용처는 `--radius-xl`로 대체.

**Step 2: page-index.css, page-shortcuts.css, components.css에서 `--radius-2xl` → `--radius-xl` 교체**

```bash
grep -rn "radius-2xl" course-site/assets/page-*.css course-site/assets/components.css
```

각 파일에서 `var(--radius-2xl)` → `var(--radius-xl)` 전역 교체.

**Step 3: 커밋**

```bash
git add course-site/assets/tokens.css course-site/assets/page-index.css course-site/assets/page-shortcuts.css course-site/assets/components.css
git commit -m "refactor(tokens): unify border-radius scale to benchmark spec (8/12/16/20/24/999)"
```

---

### Task 3: tokens.css — font-weight 스케일 통일

**Files:**
- Modify: `course-site/assets/tokens.css:105-109`

**Step 1: fw 토큰을 벤치마크 값으로 교체**

변경 전:
```css
--fw-normal:  500;
--fw-medium:  600;
--fw-semi:    620;
--fw-bold:    700;
```

변경 후:
```css
/* Font-weight scale (벤치마크 기준 — 이 4단계만 허용) */
--fw-normal:  400;  /* 본문 */
--fw-medium:  500;  /* 네비 라벨, 캡션 */
--fw-semi:    600;  /* 카드 제목, 섹션 타이틀 */
--fw-bold:    700;  /* 페이지 제목, 강조 */
```

**Step 2: 커밋**

```bash
git add course-site/assets/tokens.css
git commit -m "refactor(tokens): unify font-weight scale to 400/500/600/700"
```

---

### Task 4: tokens.css — 타이포그래피 스케일 토큰 추가

**Files:**
- Modify: `course-site/assets/tokens.css:74-76` (Typography 섹션)

**Step 1: 타이포 스케일 토큰 추가**

기존 `--font-display`, `--font-body` 아래에 삽입:

```css
/* Typography scale (Vercel 6-step) */
--text-nano: .6875rem;  /* 11px — 섹션 라벨 uppercase */
--text-xs:   .75rem;    /* 12px — 메타, 칩, 뱃지 */
--text-sm:   .8125rem;  /* 13px — 네비 라벨, 카드 보조 */
--text-base: .875rem;   /* 14px — 본문, 카드 설명 */
--text-lg:   1rem;      /* 16px — 카드 제목 */
--text-xl:   1.25rem;   /* 20px — 섹션 제목 */
--text-2xl:  1.5rem;    /* 24px — 페이지 제목 */
```

**Step 2: 커밋**

```bash
git add course-site/assets/tokens.css
git commit -m "feat(tokens): add typography scale tokens (Vercel 7-step)"
```

---

### Task 5: tokens.css — 학습 모드 토큰 (웜톤)

**Files:**
- Modify: `course-site/assets/tokens.css` (light theme 블록 뒤에 추가)

**Step 1: `[data-mode="learn"]` 블록 추가**

light theme 블록 닫는 `}` 뒤에 삽입:

```css
/* ─── Learning mode (warm tone) ──────────────────── */
[data-mode="learn"] {
  --bg:             #0D0B09;
  --bg-soft:        #100E0B;
  --surface:        #141210;
  --surface-strong:  #1C1A17;
  --surface-alt:    #121009;
  --text:           #F0EDE8;
  --muted:          #9C9590;
  --muted-strong:   #D4CFC8;
  --body-bg: linear-gradient(180deg, #0D0B09 0%, #100E0C 100%);
  --topbar-bg: rgba(13, 11, 9, .9);

  /* 학습 모드 타이포: base 이상 +2px 오프셋 */
  --text-base: 1rem;      /* 16px (탐색 14px) */
  --text-lg:   1.25rem;   /* 20px (탐색 16px) */
  --text-xl:   1.5rem;    /* 24px (탐색 20px) */
  --text-2xl:  2rem;      /* 32px (탐색 24px) */
}
```

**Step 2: 커밋**

```bash
git add course-site/assets/tokens.css
git commit -m "feat(tokens): add learning mode warm-tone tokens with type scale offset"
```

---

### Task 6: tokens.css — 3단계 배경 레이어 정리

**Files:**
- Modify: `course-site/assets/tokens.css:9-14`

**Step 1: 배경 토큰을 Vercel 3-layer 기준으로 정리**

현재 `--bg`, `--bg-soft`, `--surface`, `--surface-strong`, `--surface-alt`, `--surface-tint` 6개 → 핵심 3개 + 보조 2개로 역할 명확화.

변경 전:
```css
--bg:            #0a0a0a;
--bg-soft:       #101113;
--surface:       #141517;
--surface-strong:#191b1e;
--surface-alt:   #111214;
--surface-tint:  rgba(255, 255, 255, 0.03);
```

변경 후:
```css
/* 3-layer background system (Vercel 기준) */
--bg:             #0A0A0A;  /* Layer 0: 가장 깊은 배경 */
--surface:        #111111;  /* Layer 1: 카드/패널 면 */
--surface-strong: #1A1A1A;  /* Layer 2: 강조 면, hover */
/* 보조 */
--bg-soft:        #101113;  /* Layer 0.5: 부드러운 배경 전환 */
--surface-alt:    #141517;  /* Layer 1.5: 대체 면 */
--surface-tint:   rgba(255, 255, 255, 0.03);
```

**Step 2: 커밋**

```bash
git add course-site/assets/tokens.css
git commit -m "refactor(tokens): align dark backgrounds to Vercel 3-layer system"
```

---

### Task 7: prototype.html — 레일 비율/여백 벤치마크 적용

**Files:**
- Modify: `course-site/prototype.html` (CSS 섹션)

**Step 1: 레일 아이템 크기와 간격을 벤치마크 스펙에 맞게 조정**

수정할 CSS 속성:
- `.rail` padding: `8px` → `var(--sp-2)` (8px)
- `.rail` gap: `2px` → `var(--sp-1)` (4px로 변경 — 아이템 간 최소 간격)
- `.rail-item` height: `40px` 유지 (터치 타겟)
- `.rail-item .rail-icon` font-size: `1.25rem` 유지
- `.rail-sub-item` padding 왼쪽: `42px` → `40px` (8의 배수)
- `.rail-sub-item` font-size: `.78rem` → `var(--text-sm)` (13px)

**Step 2: 메인 콘텐츠 여백을 벤치마크 스펙에 맞게 조정**

수정할 CSS 속성:
- `.main` padding: `24px 28px 64px` → `var(--sp-8) var(--sp-8) var(--sp-16)` (32px 32px 64px)
- `.main-inner` max-width: `1180px` → `var(--max-width)` (토큰 사용)

**Step 3: 카드 그리드 간격 조정**

- `.sm-grid` gap: `10px` → `var(--sp-4)` (16px)
- `.sm-card` padding: 현재값 → `var(--sp-4)` (16px)
- `.sec-divider` margin: 현재값 → `var(--sp-8) 0` (32px)

**Step 4: 타이포 토큰 적용**

- `.page-header h1` font-size → `var(--text-2xl)`
- `.page-header p` font-size → `var(--text-base)`
- `.sec-title` font-size → `var(--text-xl)`
- `.sm-card-title` font-size → `var(--text-base)`
- `.sm-card-badge` font-size → `var(--text-xs)`
- `.filter-search` font-size → `var(--text-base)`

**Step 5: preview_start → 데스크톱(1440x900) 스크린샷 → 비율 확인**

**Step 6: 커밋**

```bash
git add course-site/prototype.html
git commit -m "refactor(prototype): apply benchmark spacing, typography, and layout tokens"
```

---

### Task 8: prototype.html — 학습 모드 (덱 뷰) 웜톤 적용

**Files:**
- Modify: `course-site/prototype.html` (JS + CSS)

**Step 1: 뷰 전환 시 data-mode 속성 토글**

`showView()` JS 함수에서:
- `view-decks` 활성화 시: `document.documentElement.setAttribute('data-mode', 'learn')`
- 그 외 뷰 활성화 시: `document.documentElement.removeAttribute('data-mode')`

**Step 2: 덱 뷰 레이아웃을 학습 모드 스펙에 맞게 수정**

- `.deck-view` max-width: `760px` → `640px`
- `.deck-card-list` gap: `10px` → `var(--sp-3)` (12px)
- `.deck-card-item` padding: `16px` → `var(--sp-6)` (24px)
- `.deck-view-header` padding-bottom: `20px` → `var(--sp-8)` (32px)

**Step 3: preview에서 덱 뷰 전환 → 배경 온도 변화 스크린샷 확인**

**Step 4: 커밋**

```bash
git add course-site/prototype.html
git commit -m "feat(prototype): add warm-tone learning mode with data-mode=learn toggle"
```

---

### Task 9: prototype.html — 레일 push 동작 구현

**Files:**
- Modify: `course-site/prototype.html` (CSS)

**Step 1: 레일 펼침 시 메인 콘텐츠가 밀리도록 grid 조정**

현재: `.app` grid-template-columns가 `56px`로 고정되어 펼침 시 오버레이됨.

수정:
```css
.app {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  grid-template-rows: auto minmax(0, 1fr);
  min-height: 100vh;
}
```

레일의 `width`가 변하면 grid가 자동으로 재계산되어 push 동작.

**Step 2: 레일 transition 유지**

```css
.rail {
  width: 56px;
  transition: width .2s ease;
}
.rail.is-expanded {
  width: 220px;
}
```

**Step 3: preview에서 레일 펼침/접힘 → 메인 콘텐츠 push 확인**

**Step 4: 커밋**

```bash
git add course-site/prototype.html
git commit -m "fix(prototype): rail expand now pushes main content instead of overlaying"
```

---

### Task 10: design-agent 벤치마크 검증 규칙 추가

**Files:**
- Modify: `.claude/commands/design-agent.md`

**Step 1: post-verify 모드에 벤치마크 비교 항목 추가**

`post-verify` 섹션의 체크리스트에 추가:
```markdown
5. **벤치마크 비율 검증** (`docs/plans/2026-03-20-benchmark-design-rules.md` 참조)
   - 레일 비율: 56/220px (Linear 기준 ±10px)
   - 카드 그리드 갭: 16px (Vercel 기준)
   - 본문 폰트: 탐색 14px / 학습 16px
   - 배경 3-layer 밝기 차이: OKLCH 10-12 단위
   - 탐색 모드 = 쿨톤, 학습 모드 = 웜톤 확인
```

**Step 2: 참조 파일 테이블에 벤치마크 문서 추가**

```markdown
| `docs/plans/2026-03-20-benchmark-design-rules.md` | 벤치마크 디자인 규칙 |
```

**Step 3: 커밋**

```bash
git add .claude/commands/design-agent.md
git commit -m "feat(design-agent): add benchmark verification rules to post-verify mode"
```

---

### Task 11: 전체 검증 — design-agent post-verify

**Step 1: `/design-agent post-verify` 실행**

모든 퍼블릭 페이지를 desktop(1440x900) + mobile(375x812) 스크린샷으로 검증.

**Step 2: 벤치마크 규칙 위반 사항 확인 및 수정**

**Step 3: 최종 커밋**

```bash
git add -A
git commit -m "chore: fix benchmark rule violations found in post-verify"
```

---

## 범위 외 (이 플랜에서 하지 않는 것)

- library.html / week.html 인라인 CSS 분리 (별도 플랜)
- week.html → deck.html 리네임 (별도 플랜)
- Show Me 카드의 radius/fw 토큰 통일 (60+ 파일, 별도 플랜)
- Light theme의 학습 모드 토큰 (dark 우선 확정 후)
- Supabase/OAuth 연동
