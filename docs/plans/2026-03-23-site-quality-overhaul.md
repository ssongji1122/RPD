# RPD Site Quality Overhaul — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 분석 리포트(claudedocs/2026-03-23-site-deep-analysis.md) 기반으로 토큰 하드코딩 정리, 컴포넌트 중복 해소, 전 페이지 App Grid 레이아웃 통일, 접근성/보안/퍼포먼스 개선을 Bottom-Up으로 수행한다.

**Architecture:** 6 Phase Bottom-Up — 토큰 정리 → 컴포넌트 통합 → 레이아웃 통일(inha/week/admin → App Grid) → 접근성/보안 → 퍼포먼스 → 레거시 제거. 각 Phase는 독립적으로 커밋 가능하며, Phase 3가 가장 큰 작업.

**Tech Stack:** Vanilla CSS (custom properties), Vanilla JS (ES5 IIFE), HTML5

**Analysis Report:** `claudedocs/2026-03-23-site-deep-analysis.md`
**Previous Design Docs:** `docs/plans/2026-03-20-layout-redesign-design.md`, `docs/plans/2026-03-19-design-system-director-design.md`

---

## Phase 1: 토큰 시스템 강제 (Token Enforcement)

> font-weight, border-radius, rgba 하드코딩을 토큰 변수로 치환.
> 이 Phase를 먼저 해야 이후 새 CSS 작성 시 올바른 토큰 사용 가능.

### Task 1: tokens.css — 누락 토큰 추가

**Files:**
- Modify: `course-site/assets/tokens.css:80-86` (`:root` 블록)

**Step 1: border-radius 토큰 확장**

현재:
```css
--radius: 12px;
--radius-sm: 8px;
--radius-md: 16px;
--radius-lg: 20px;
--radius-xl: 24px;
--radius-pill: 999px;
```

추가할 토큰:
```css
--radius-2xl: 26px;   /* .rpd-panel, .content-block 대형 패널 */
```

> 14px는 `--radius` (12px)로, 18px는 `--radius-md` (16px) 또는 신규 토큰으로 매핑. 22px는 `--radius-xl` (24px)로 통일.
> **원칙**: 가장 가까운 기존 토큰으로 매핑. 시각 차이 2px 이내는 수용.

**Step 2: Commit**
```bash
git add course-site/assets/tokens.css
git commit -m "feat(tokens): add --radius-2xl token for large panels"
```

---

### Task 2: font-weight 하드코딩 → 토큰 치환

**Files:**
- Modify: `course-site/assets/chrome.css` (lines 64, 92, 125, 377, 387, 450)
- Modify: `course-site/assets/meta.css` (lines 64, 86)
- Modify: `course-site/assets/page-shortcuts.css` (lines 103, 126)
- Modify: `course-site/assets/page-library.css` (line 354)

**Step 1: 치환 매핑표**

| 현재 값 | 토큰 | 근거 |
|---------|------|------|
| `font-weight: 500` | `var(--fw-medium)` | 정확히 일치 |
| `font-weight: 560` | `var(--fw-semi)` | 560→600 (가장 가까운 상위) |
| `font-weight: 620` | `var(--fw-semi)` | 620→600 (20 차이, 수용) |
| `font-weight: 650` | `var(--fw-bold)` | 650→700 (디자인 시스템 결정에 의해 통일) |
| `font-weight: 700` (토큰 아닌 곳) | `var(--fw-bold)` | 정확히 일치 |

**Step 2: 각 파일 수정**

`chrome.css:64` `.rpd-brand-lockup .brand-copy strong` → `font-weight: var(--fw-bold);`
`chrome.css:92` `.rpd-hero-title` → `font-weight: var(--fw-bold);`
`chrome.css:125` `.rpd-hero-meta-label` → `font-weight: var(--fw-bold);`
`chrome.css:377` `.rpd-sidecard-label, .rpd-rail-label` → `font-weight: var(--fw-bold);`
`chrome.css:387` `.rpd-sidecard-title, .rpd-rail-title` → `font-weight: var(--fw-bold);`
`chrome.css:450` `.rpd-page-rail .rpd-rail-link.is-active ...` → `font-weight: var(--fw-semi);`
`meta.css:64` `.rpd-stat-chip strong ...` → `font-weight: var(--fw-semi);`
`meta.css:86` `.rpd-status-pill, .status-pill` → `font-weight: var(--fw-bold);`
`page-shortcuts.css:103` `.filter-chip` → `font-weight: var(--fw-medium);`
`page-shortcuts.css:126` `.view-btn` → `font-weight: var(--fw-medium);`
`page-library.css:354` → `font-weight: var(--fw-semi);`

**Step 3: 시각 검증**

각 페이지를 브라우저에서 열어 font-weight 변경이 자연스러운지 확인:
- index.html (archive cards, hero)
- library.html (card list)
- shortcuts.html (filter chips, view buttons)
- inha.html (brand lockup, hero, rail)

**Step 4: Commit**
```bash
git add course-site/assets/chrome.css course-site/assets/meta.css \
        course-site/assets/page-shortcuts.css course-site/assets/page-library.css
git commit -m "refactor(tokens): replace hardcoded font-weight with token vars"
```

---

### Task 3: border-radius 하드코딩 → 토큰 치환

**Files:**
- Modify: `course-site/assets/components.css` (lines 28, 82, 147)
- Modify: `course-site/assets/chrome.css` (lines 118, 293, 413, 529)
- Modify: `course-site/assets/surface.css` (lines 8, 43)
- Modify: `course-site/assets/page-library.css` (lines 49, 178, 318, 482)
- Modify: `course-site/assets/page-shortcuts.css` (line 60)
- Modify: `course-site/assets/page-index.css` (lines 148, 315)

**Step 1: 치환 매핑표**

| 현재 값 | 토큰 | 적용 위치 |
|---------|------|-----------|
| `14px` | `var(--radius)` | 12→14 차이 2px 수용 |
| `16px` | `var(--radius-md)` | 정확히 일치 |
| `18px` | `var(--radius-md)` | 18→16 차이 2px 수용 |
| `22px` | `var(--radius-xl)` | 22→24 차이 2px 수용 |
| `26px` | `var(--radius-2xl)` | Task 1에서 추가한 토큰 |

**Step 2: 치환 실행**

`components.css:28` `.rpd-glass-card` → `border-radius: var(--radius-md);`
`components.css:82` `.rpd-icon-well` → `border-radius: var(--radius);`
`components.css:147` `.rpd-search-input` → `border-radius: var(--radius-md);`
`chrome.css:118` `.rpd-hero-meta-wrap` → `border-radius: var(--radius-md);`
`chrome.css:293` `.rpd-page-rail-toggle` → `border-radius: var(--radius);`
`chrome.css:413` `.rpd-sidecard-link ...` → `border-radius: var(--radius-md);`
`chrome.css:529` (mobile `.rpd-sidecard`) → `border-radius: var(--radius-xl);`
`surface.css:8` `.rpd-panel` → `border-radius: var(--radius-2xl);`
`surface.css:43` `.rpd-icon-well` → `border-radius: var(--radius);`
`page-library.css:49` `.lib-search` → `border-radius: var(--radius-md);`
`page-library.css:178` `.lib-card` → `border-radius: var(--radius-md);`
`page-library.css:318` `.lib-nav-letter` → `border-radius: var(--radius-md);`
`page-library.css:482` `.lib-detail-close` → `border-radius: var(--radius);`
`page-shortcuts.css:60` `.search-input` → `border-radius: var(--radius-md);`
`page-index.css:148` `.content-block` → `border-radius: var(--radius-2xl);`
`page-index.css:315` `.week-card` → `border-radius: var(--radius-xl);`

**Step 3: 시각 검증** — 동일하게 전 페이지 확인

**Step 4: Commit**
```bash
git add course-site/assets/components.css course-site/assets/chrome.css \
        course-site/assets/surface.css course-site/assets/page-library.css \
        course-site/assets/page-shortcuts.css course-site/assets/page-index.css
git commit -m "refactor(tokens): replace hardcoded border-radius with token vars"
```

---

## Phase 2: 컴포넌트 중복 해소 (Component Dedup)

### Task 4: `.rpd-icon-well` 중복 제거

**Files:**
- Modify: `course-site/assets/surface.css:40-49` — 중복 정의 제거
- Verify: `course-site/assets/components.css:76-88` — 이것이 canonical

**Step 1: surface.css에서 `.rpd-icon-well` 블록 제거**

`surface.css:40-49` 의 `.rpd-icon-well { ... }` 전체 삭제.

> **주의**: surface.css는 inha.html만 로드. inha.html이 components.css도 로드하는지 확인 필요.

**Step 2: inha.html이 components.css를 로드하는지 확인**

`inha.html`의 `<head>`:
```html
<link rel="stylesheet" href="assets/tokens.css" />
<link rel="stylesheet" href="assets/surface.css" />
<link rel="stylesheet" href="assets/meta.css" />
<link rel="stylesheet" href="assets/chrome.css" />
```

→ components.css를 로드하지 않음! 따라서:

**Step 3: inha.html에 components.css 추가**

```html
<link rel="stylesheet" href="assets/tokens.css" />
<link rel="stylesheet" href="assets/components.css" />   <!-- 추가 -->
<link rel="stylesheet" href="assets/surface.css" />
```

**Step 4: surface.css에서 `.rpd-icon-well` 삭제**

**Step 5: inha.html에서 icon-well이 정상 렌더되는지 확인**

**Step 6: Commit**
```bash
git add course-site/assets/surface.css course-site/inha.html
git commit -m "refactor: deduplicate .rpd-icon-well — canonical in components.css"
```

---

### Task 5: `.status-pill` 중복 정리

**Files:**
- Review: `course-site/assets/tokens.css:524-535` (`.status-pill` 기본 정의)
- Review: `course-site/assets/meta.css:82-110` (`.rpd-status-pill, .status-pill` 확장 정의)

**Step 1: 분석**

tokens.css의 `.status-pill`은 기본 스타일 (padding, radius, font-size 등).
meta.css의 정의는 이를 `rpd-status-pill`과 함께 확장 (min-height 추가, complete/active/locked 변형).

→ **액션**: tokens.css의 `.status-pill`에서 meta.css와 중복되는 속성 제거. meta.css를 canonical로.

**Step 2: tokens.css에서 `.status-pill` 의 중복 속성 식별 후 정리**

tokens.css의 `.status-pill`에서 padding, border-radius, font-size, font-weight 등 meta.css에서 재정의되는 속성이 있으면, 하나로 통합.

**Step 3: 시각 검증** — inha.html과 week.html에서 status pill 확인

**Step 4: Commit**
```bash
git add course-site/assets/tokens.css course-site/assets/meta.css
git commit -m "refactor: consolidate .status-pill definitions"
```

---

### Task 6: filter-chip 클래스명 통일

**Files:**
- Review: `course-site/assets/components.css:118-141` (`.rpd-filter-chip`)
- Review: `course-site/assets/page-shortcuts.css:98-116` (`.filter-chip`)

**Step 1: 두 정의를 비교**

둘 다 동일 패턴 (pill shape, border, hover, is-active). shortcuts가 `rpd-` prefix 없이 자체 정의.

**Step 2: shortcuts.html에서 `.filter-chip` → `.rpd-filter-chip` 교체**

HTML에서 `class="filter-chip"` → `class="rpd-filter-chip"` 변경.

**Step 3: page-shortcuts.css에서 `.filter-chip` 블록 삭제**

components.css의 `.rpd-filter-chip`이 대신함.

**Step 4: 시각 검증** — shortcuts.html 카테고리 필터 정상 동작 확인

**Step 5: Commit**
```bash
git add course-site/shortcuts.html course-site/assets/page-shortcuts.css
git commit -m "refactor: unify filter-chip → rpd-filter-chip from components.css"
```

---

## Phase 3: App Grid 레이아웃 통일

> 가장 큰 Phase. inha.html, week.html, admin.html을 page-shell → App Grid로 전환.
> 기존 index/library/shortcuts의 App Grid 구현(layout.css + layout.js)을 재사용.

### Task 7: week.html — App Grid 전환 + 인라인 CSS 분리

**Files:**
- Modify: `course-site/week.html` — 마크업 교체 + `<style>` 블록 제거
- Create: `course-site/assets/page-week.css` — 인라인 CSS를 외부 파일로

**Step 1: week.html의 인라인 `<style>` 블록(~2,078 lines) 을 page-week.css로 추출**

새 파일 `course-site/assets/page-week.css` 생성. `<style>...</style>` 사이의 CSS를 그대로 이동.

**Step 2: week.html `<head>` CSS 링크 교체**

Before:
```html
<link rel="stylesheet" href="assets/tokens.css" />
<link rel="stylesheet" href="assets/components.css" />
<script>/* FOUC */...</script>
<style>/* 2078 lines */</style>
```

After:
```html
<link rel="stylesheet" href="assets/tokens.css" />
<link rel="stylesheet" href="assets/components.css" />
<link rel="stylesheet" href="assets/layout.css" />
<link rel="stylesheet" href="assets/page-week.css" />
<script>/* FOUC */...</script>
```

**Step 3: week.html 마크업을 App Grid로 교체**

Before (page-shell 구조):
```html
<body>
  <div class="page-shell">
    <header class="topbar">...</header>
    <div class="rpd-page-layout">
      <aside class="rpd-page-rail">...</aside>
      <main class="rpd-page-main">...</main>
    </div>
  </div>
</body>
```

After (App Grid 구조):
```html
<body>
  <a href="#main-content" class="skip-link">본문으로 건너뛰기</a>
  <div class="app">
    <header class="app-topbar">
      <div class="app-topbar-left">
        <div class="app-logo">BA</div>
        <div class="app-title">Blender Archive <span>RPD</span></div>
      </div>
      <div class="app-topbar-right">
        <div id="langSwitcher"></div>
        <button class="theme-toggle" id="themeToggle" type="button" aria-label="테마 전환">
          <!-- 기존 SVG 아이콘 -->
        </button>
      </div>
    </header>
    <nav class="rail" id="sideRail" aria-label="메인 탐색">
      <!-- index.html과 동일한 rail 마크업 -->
    </nav>
    <main class="main" id="main-content">
      <div class="main-inner">
        <!-- 기존 week 콘텐츠 (hero, sections, etc.) -->
      </div>
    </main>
  </div>
</body>
```

**Step 4: page-week.css에서 .topbar, .rpd-page-layout 등 page-shell 전용 스타일 제거**

삭제 대상: `.topbar`, `.topbar-inner`, `.rpd-page-layout`, `.rpd-page-rail`, `.rpd-page-main` 등 layout.css가 대체하는 스타일.

**Step 5: page-week.css에서 하드코딩 값 → 토큰 치환** (Phase 1에서 정립한 매핑표 적용)

**Step 6: layout.js `<script>` 추가** — `</body>` 전에:
```html
<script src="assets/layout.js"></script>
```

**Step 7: 시각 검증**
- week.html?week=3 등 실제 주차 페이지 열어서 레이아웃 확인
- Rail 네비게이션이 정상 동작하는지 확인
- 모바일(720px) 하단 탭바 동작 확인
- 테마 토글 동작 확인

**Step 8: Commit**
```bash
git add course-site/week.html course-site/assets/page-week.css
git commit -m "refactor: migrate week.html to App Grid layout + extract inline CSS"
```

---

### Task 8: inha.html — App Grid 전환 + 인라인 CSS 분리

**Files:**
- Modify: `course-site/inha.html` — 마크업 교체 + `<style>` 블록 제거
- Create: `course-site/assets/page-inha.css` — 인라인 CSS (~554 lines) 외부 추출

**Step 1: inha.html의 `<style>` 블록 → page-inha.css 추출**

**Step 2: `<head>` CSS 링크 교체**

After:
```html
<link rel="stylesheet" href="assets/tokens.css" />
<link rel="stylesheet" href="assets/components.css" />
<link rel="stylesheet" href="assets/layout.css" />
<link rel="stylesheet" href="assets/page-inha.css" />
```

> surface.css, meta.css, chrome.css는 page-inha.css가 필요한 부분만 포함하므로 더 이상 별도 로드 불필요.
> 단, page-inha.css가 chrome.css의 hero/sidecard 등을 사용한다면 chrome.css도 유지.
> **실행 시 판단**: chrome.css에서 inha가 실제로 쓰는 클래스를 확인하고, 쓰는 것만 page-inha.css에 포함.

**Step 3: 마크업을 App Grid로 교체** (Task 7과 동일 패턴)

**Step 4: page-inha.css에서 page-shell 전용 스타일 제거 + 토큰 치환**

**Step 5: 시각 검증 + Commit**
```bash
git add course-site/inha.html course-site/assets/page-inha.css
git commit -m "refactor: migrate inha.html to App Grid layout + extract inline CSS"
```

---

### Task 9: admin.html — App Grid 전환 + 인라인 CSS 분리

**Files:**
- Modify: `course-site/admin.html` — 마크업 + `<style>` (~1,420 lines) 제거
- Create: `course-site/assets/page-admin.css`

**Step 1-5: Task 7/8과 동일 패턴**

admin은 추가 고려사항:
- `.admin-topbar` → `.app-topbar` 교체
- `.admin-sidebar` → `.rail` 교체 (admin은 주차 목록을 사이드바에 표시 → rail-sub에 표시)
- `.admin-brand` → `.app-logo` + `.app-title` 교체
- week selector (topbar context) → app-topbar 내 select로 이동

**Step 6: Commit**
```bash
git add course-site/admin.html course-site/assets/page-admin.css
git commit -m "refactor: migrate admin.html to App Grid layout + extract inline CSS"
```

---

## Phase 4: 접근성 & 보안 (A11y + Security)

### Task 10: skip-link 통일

**Files:**
- Modify: `course-site/inha.html` — skip-link 추가
- Modify: `course-site/week.html` — skip-link 확인 (Phase 3에서 이미 추가)
- Modify: `course-site/admin.html` — skip-link 추가

**Step 1: inha.html과 admin.html `<body>` 직후에 추가**

```html
<a href="#main-content" class="skip-link">본문으로 건너뛰기</a>
```

**Step 2: `<main>` 태그에 `id="main-content"` 확인**

**Step 3: Commit**
```bash
git add course-site/inha.html course-site/admin.html
git commit -m "a11y: add skip-link to inha and admin pages"
```

---

### Task 11: ARIA 레이블 균등화

**Files:**
- Modify: `course-site/admin.html` — ARIA 레이블 추가 (현재 5건 → 15건+)
- Modify: `course-site/inha.html` — ARIA 레이블 추가 (현재 5건 → 15건+)

**Step 1: 최소 필수 ARIA 추가**

모든 페이지에 공통으로 있어야 할 것:
- `<nav aria-label="메인 탐색">` — rail
- `<main id="main-content">` — 메인 콘텐츠
- `<button aria-label="테마 전환">` — 테마 토글
- `<input aria-label="...">` — 모든 input
- `role="status" aria-live="polite"` — 동적 상태 표시 영역

**Step 2: admin.html 추가 ARIA**

- week selector: `aria-label="주차 선택"`
- save 버튼: `aria-label="변경사항 저장"`
- editor 영역: `role="region" aria-label="편집기"`
- sidebar: `role="navigation" aria-label="주차 목록"`

**Step 3: 시각 검증** (스크린리더 또는 접근성 트리 확인)

**Step 4: Commit**
```bash
git add course-site/admin.html course-site/inha.html
git commit -m "a11y: add ARIA labels to admin and inha pages"
```

---

### Task 12: innerHTML XSS 완화 (admin.html 우선)

**Files:**
- Modify: `course-site/admin.html` — 고위험 innerHTML 19건 검토

**Step 1: 위험도 분류**

admin.html의 innerHTML 사용 중:
- `esc()` 함수로 이스케이프하는 것: 상대적 안전 (확인 필요)
- 사용자 입력(커리큘럼 데이터)이 직접 들어가는 것: 위험

**Step 2: `esc()` 함수 존재 여부 확인**

admin.html에서 `esc` 함수가 정의되어 있는지, HTML entity escape를 올바르게 수행하는지 확인.

**Step 3: esc() 미적용 innerHTML을 textContent 또는 createElement로 교체**

교체 우선순위:
1. 사용자 입력이 들어가는 곳 (week title, step description 등)
2. 동적 HTML 생성 (sidebar list, editor HTML 등)

> 모든 19건을 한번에 바꾸면 리스크가 큼. 사용자 입력 경로만 우선 처리.

**Step 4: 기능 검증** — admin에서 주차 편집 → 저장이 정상 동작하는지 확인

**Step 5: Commit**
```bash
git add course-site/admin.html
git commit -m "security: sanitize innerHTML usage in admin editor"
```

---

## Phase 5: 퍼포먼스 (Performance)

### Task 13: Google Fonts 로딩 최적화

**Files:**
- Modify: `course-site/assets/tokens.css:6` — `@import` 제거
- Modify: All HTML files `<head>` — `<link rel="preconnect">` + `<link rel="stylesheet">` 추가

**Step 1: tokens.css에서 @import 제거**

```css
/* 삭제 */
@import url("https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700&display=swap");
```

**Step 2: 모든 HTML `<head>` 에 preconnect + font link 추가**

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700&display=swap" />
```

> 이렇게 하면 CSS 파싱 중 블로킹 @import 대신 HTML 파서가 preconnect를 먼저 시작.

**Step 3: Commit**
```bash
git add course-site/assets/tokens.css course-site/*.html
git commit -m "perf: move Google Fonts from CSS @import to HTML preconnect+link"
```

---

### Task 14: script defer + lazy loading

**Files:**
- Modify: All HTML files — `<script>` 태그에 `defer` 추가
- Modify: `course-site/week.html` — step 이미지에 `loading="lazy"` 추가 (JS 렌더링이므로 JS 코드 수정)

**Step 1: 모든 `<script src="...">` 에 defer 속성 추가**

```html
<!-- Before -->
<script src="assets/site-shell.js?v=20260318a"></script>

<!-- After -->
<script defer src="assets/site-shell.js?v=20260318a"></script>
```

> 주의: 인라인 `<script>` (FOUC 방지, renderPage 등)은 defer 불가 — 그대로 유지.
> defer는 외부 src 파일에만 적용.

**Step 2: week.html JS에서 이미지 생성 시 lazy 속성 추가**

week.html의 이미지 생성 코드에서:
```js
// Before
img.src = step.image;

// After
img.src = step.image;
img.loading = "lazy";
```

**Step 3: Commit**
```bash
git add course-site/*.html
git commit -m "perf: add defer to external scripts + lazy loading for step images"
```

---

## Phase 6: 레거시 제거 (Legacy Cleanup)

### Task 15: page-shell 전용 CSS 파일 정리

**Files:**
- Review: `course-site/assets/surface.css` — 아직 사용하는 페이지가 있는지 확인
- Review: `course-site/assets/chrome.css` — 동일
- Review: `course-site/assets/meta.css` — 동일

**Step 1: Phase 3 완료 후, 각 CSS를 `<link>`로 로드하는 HTML이 있는지 grep**

```bash
grep -r "surface.css\|chrome.css\|meta.css" course-site/*.html
```

Phase 3에서 inha/week/admin이 App Grid로 전환되면서 이 파일들의 `<link>`가 제거되었을 것.

**Step 2: 로드하는 페이지가 없으면 파일 삭제**

```bash
git rm course-site/assets/surface.css
git rm course-site/assets/chrome.css
git rm course-site/assets/meta.css
```

> 만약 page-inha.css 등이 이 파일의 일부를 인라인 흡수했다면, 원본은 삭제 가능.

**Step 3: 아직 사용 중이면 점진적 마이그레이션** — 해당 클래스들을 page-*.css로 이동 후 삭제.

**Step 4: Commit**
```bash
git commit -m "chore: remove unused page-shell CSS files (surface, chrome, meta)"
```

---

### Task 16: CSS 선택자 명명 일관성 감사

**Files:**
- Review: 전체 CSS 파일

**Step 1: `rpd-` prefix 없는 컴포넌트 클래스 목록화**

```bash
grep -hE '^\.[a-z]' course-site/assets/*.css | sort -u | grep -v '^\.\(rpd-\|app-\|rail-\|main\)'
```

**Step 2: 공유 컴포넌트 중 `rpd-` prefix가 없는 것 식별**

예: `.filter-chip` (Task 6에서 이미 처리), `.status-pill`, `.hero-meta-chip` 등

**Step 3: 점진적 리네이밍** (HTML + CSS 동시 변경)

> 이 Task는 범위가 넓으므로, 가장 혼동되는 것만 우선 처리.

**Step 4: Commit**
```bash
git add -A
git commit -m "refactor: align CSS class naming to rpd- prefix convention"
```

---

### Task 17: 전체 시각 회귀 검증

**Step 1: 모든 페이지를 Dark + Light 양쪽에서 확인**

| 페이지 | Dark | Light | Mobile(720px) |
|--------|------|-------|---------------|
| index.html | ☐ | ☐ | ☐ |
| library.html | ☐ | ☐ | ☐ |
| shortcuts.html | ☐ | ☐ | ☐ |
| week.html | ☐ | ☐ | ☐ |
| inha.html | ☐ | ☐ | ☐ |
| admin.html | ☐ | ☐ | ☐ |

**Step 2: 발견된 이슈 → hotfix commit**

**Step 3: Final commit**
```bash
git commit -m "chore: complete site quality overhaul — visual regression verified"
```

---

## Summary

| Phase | Tasks | 예상 규모 | 핵심 산출물 |
|-------|-------|-----------|-------------|
| 1. Token Enforcement | 1-3 | Small | 토큰 하드코딩 제거 |
| 2. Component Dedup | 4-6 | Small | 중복 정의 해소 |
| 3. App Grid 통일 | 7-9 | **Large** | week/inha/admin 레이아웃 전환 + page-*.css 3개 신규 |
| 4. A11y + Security | 10-12 | Medium | skip-link, ARIA, innerHTML 정리 |
| 5. Performance | 13-14 | Small | font preload, defer, lazy |
| 6. Legacy Cleanup | 15-17 | Medium | page-shell CSS 삭제, 명명 통일, 시각 검증 |
