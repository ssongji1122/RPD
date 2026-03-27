# Foundation Cleanup — CSS 추출 + 토큰 강제 + 접근성 + 모바일 QA

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 인라인 CSS를 외부 파일로 추출하고, 하드코딩 값을 토큰으로 교체하고, 접근성을 보강하고, 모바일 레이아웃을 검증한다.

**Architecture:** 3개 HTML(week, inha, admin)의 `<style>` 블록을 page-*.css 파일로 추출. 추출 후 하드코딩 font-weight/border-radius/rgba를 tokens.css 변수로 교체. 접근성은 ARIA 라벨 + focus-visible + skip-link 보강. 모바일은 375/720/1280px에서 시각 검증.

**Tech Stack:** CSS custom properties, HTML aria attributes, Playwright preview

---

## 현재 상태

### 인라인 CSS 규모
| 파일 | `<style>` 라인 수 | 하드코딩 값 수 |
|------|-----------------|-------------|
| week.html | 2,095줄 (12~2107) | ~140개 (rgba, font-weight, border-radius) |
| inha.html | 577줄 (14~591) | ~49개 |
| admin.html | 1,419줄 (11~1430) | ~128개 |

### 이미 추출된 페이지
- index.html → page-index.css (완료)
- library.html → page-library.css (완료)
- shortcuts.html → page-shortcuts.css (완료)
- studio.html → page-studio.css (완료)

### 접근성 현황
- skip-link: index, library, shortcuts에 있음. inha, week, admin에 없거나 불완전
- ARIA: library(19), week(19), shortcuts(12)는 양호. inha(2)는 부족
- focus-visible: 전역 스타일 없음

---

## Task 1: week.html 인라인 CSS → page-week.css 추출

**Files:**
- Create: `course-site/assets/page-week.css`
- Modify: `course-site/week.html`

**Step 1: week.html의 `<style>` 블록 전체(line 12~2107)를 복사해서 page-week.css로 저장**

week.html에서 `<style>...</style>` 사이의 CSS 전체를 `course-site/assets/page-week.css`로 이동.

**Step 2: week.html에서 `<style>...</style>` 블록 제거, `<link>` 추가**

```html
<!-- 기존 <style>...</style> 블록 제거 후 -->
<link rel="stylesheet" href="assets/page-week.css" />
```

tokens.css 다음, `</head>` 이전에 배치.

**Step 3: 시각 검증** — week.html?week=3 로드, 레이아웃 깨짐 없는지 확인

**Step 4: Commit**
```bash
git add course-site/assets/page-week.css course-site/week.html
git commit -m "refactor(week): extract inline CSS to page-week.css (2095 lines)"
```

---

## Task 2: inha.html 인라인 CSS → page-inha.css 추출

**Files:**
- Create: `course-site/assets/page-inha.css`
- Modify: `course-site/inha.html`

**Step 1: inha.html의 `<style>` 블록 전체(line 14~591)를 page-inha.css로 이동**

**Step 2: inha.html에서 블록 제거, `<link>` 추가**

```html
<link rel="stylesheet" href="assets/page-inha.css" />
```

**Step 3: 시각 검증** — inha.html 로드 확인

**Step 4: Commit**
```bash
git add course-site/assets/page-inha.css course-site/inha.html
git commit -m "refactor(inha): extract inline CSS to page-inha.css (577 lines)"
```

---

## Task 3: admin.html 인라인 CSS → page-admin.css 추출

**Files:**
- Create: `course-site/assets/page-admin.css`
- Modify: `course-site/admin.html`

**Step 1: admin.html의 `<style>` 블록 전체(line 11~1430)를 page-admin.css로 이동**

**Step 2: admin.html에서 블록 제거, `<link>` 추가**

```html
<link rel="stylesheet" href="assets/page-admin.css" />
```

**Step 3: 시각 검증** — admin.html 로드 확인

**Step 4: Commit**
```bash
git add course-site/assets/page-admin.css course-site/admin.html
git commit -m "refactor(admin): extract inline CSS to page-admin.css (1419 lines)"
```

---

## Task 4: page-week.css 토큰 강제 — font-weight

**Files:**
- Modify: `course-site/assets/page-week.css`

**Step 1: font-weight 하드코딩 값을 토큰으로 교체**

| 하드코딩 | 토큰 |
|---------|------|
| `font-weight: 620` | `font-weight: var(--fw-semi)` |
| `font-weight: 630` | `font-weight: var(--fw-semi)` |
| `font-weight: 500` | `font-weight: var(--fw-medium)` |
| `font-weight: 600` | `font-weight: var(--fw-semi)` |
| `font-weight: 700` | `font-weight: var(--fw-bold)` |
| `font-weight: 400` | `font-weight: var(--fw-normal)` |

> 620→600(semi), 630→600(semi)는 미세한 시각 변화. 의도된 통일.

**Step 2: 시각 검증** — week.html 로드, 폰트 굵기 확인

**Step 3: Commit**
```bash
git add course-site/assets/page-week.css
git commit -m "refactor(week): replace hardcoded font-weight with tokens"
```

---

## Task 5: page-week.css 토큰 강제 — border-radius + clamp

**Files:**
- Modify: `course-site/assets/page-week.css`

**Step 1: border-radius 하드코딩 → 토큰**

| 하드코딩 | 토큰 |
|---------|------|
| `border-radius: 12px` | `border-radius: var(--radius)` |
| `border-radius: 8px` | `border-radius: var(--radius-sm)` |
| `border-radius: 16px` | `border-radius: var(--radius-md)` |
| `border-radius: 20px` | `border-radius: var(--radius-lg)` |
| `border-radius: 24px` | `border-radius: var(--radius-xl)` |
| `border-radius: 999px` | `border-radius: var(--radius-pill)` |
| `border-radius: 10px` | `border-radius: var(--radius-sm)` (8→10 허용) |
| `border-radius: 14px` | `border-radius: var(--radius)` (12→14 허용) |

**Step 2: clamp 값 → 시맨틱 타이포 토큰 (해당하는 경우만)**

이미 week.html 히어로에 `var(--type-hero)` 적용됨. 나머지 clamp는 페이지 고유 값이므로 유지.

**Step 3: Commit**
```bash
git add course-site/assets/page-week.css
git commit -m "refactor(week): replace hardcoded border-radius with tokens"
```

---

## Task 6: page-inha.css + page-admin.css 토큰 강제

**Files:**
- Modify: `course-site/assets/page-inha.css`
- Modify: `course-site/assets/page-admin.css`

**Step 1: 동일 패턴으로 font-weight + border-radius 토큰 교체**

inha.css: ~49개 하드코딩 값
admin.css: ~128개 하드코딩 값

**Step 2: 시각 검증** — inha.html, admin.html 각각 확인

**Step 3: Commit**
```bash
git add course-site/assets/page-inha.css course-site/assets/page-admin.css
git commit -m "refactor(inha,admin): replace hardcoded values with design tokens"
```

---

## Task 7: 전역 focus-visible 스타일 추가

**Files:**
- Modify: `course-site/assets/tokens.css`

**Step 1: tokens.css 끝에 focus-visible 스타일 추가**

```css
/* ─── Focus visible ─────────────────────────────── */
:focus-visible {
  outline: 2px solid var(--key);
  outline-offset: 2px;
}
:focus:not(:focus-visible) {
  outline: none;
}
.btn:focus-visible,
.app-tab:focus-visible,
.rail-item:focus-visible {
  outline: 2px solid var(--key);
  outline-offset: 2px;
  border-radius: var(--radius-sm);
}
```

**Step 2: 키보드 탭으로 탭/사이드바/버튼 이동 확인**

**Step 3: Commit**
```bash
git add course-site/assets/tokens.css
git commit -m "feat(a11y): add global :focus-visible styles"
```

---

## Task 8: ARIA 라벨 + skip-link 보강

**Files:**
- Modify: `course-site/inha.html` (skip-link 추가, ARIA 보강)
- Modify: `course-site/week.html` (ARIA 보강)
- Modify: `course-site/admin.html` (skip-link 추가)

**Step 1: inha.html에 skip-link 추가**

`<body>` 바로 뒤에:
```html
<a href="#main-content" class="skip-link">본문으로 건너뛰기</a>
```

main 콘텐츠 영역에 `id="main-content"` 추가.

**Step 2: week.html 탭바에 aria-label 추가**

```html
<div class="app-tabs" role="tablist" aria-label="사이트 탐색">
```

**Step 3: admin.html에 skip-link 추가**

동일 패턴.

**Step 4: Commit**
```bash
git add course-site/inha.html course-site/week.html course-site/admin.html
git commit -m "feat(a11y): add skip-links and ARIA labels to inha, week, admin"
```

---

## Task 9: 모바일 레이아웃 QA (375px / 720px / 1280px)

**Step 1:** preview_start → 각 페이지를 3가지 뷰포트에서 확인

| 페이지 | 375px (모바일) | 720px (태블릿) | 1280px (데스크탑) |
|--------|-------------|-------------|-------------|
| index.html | ☐ 탭 가운데, 사이드바 숨김 | ☐ 레일 표시 | ☐ 정상 |
| library.html | ☐ | ☐ | ☐ |
| shortcuts.html | ☐ | ☐ | ☐ |
| week.html | ☐ | ☐ | ☐ |
| inha.html | ☐ | ☐ | ☐ |
| studio.html | ☐ | ☐ | ☐ |

**Step 2:** 발견된 이슈 수정

**Step 3: Commit**
```bash
git commit -m "fix: responsive layout issues from mobile QA"
```

---

## Task 10: prototype.html 정리

**Files:**
- Move: `course-site/prototype.html` → `course-site/.archive/prototype.html`

**Step 1:** prototype.html을 .archive 폴더로 이동 (삭제하지 않고 보관)

```bash
mkdir -p course-site/.archive
mv course-site/prototype.html course-site/.archive/
```

**Step 2: Commit**
```bash
git add -A
git commit -m "chore: archive prototype.html (not production code)"
```

---

## Summary

| Task | 파일 | 변경 | 규모 |
|------|------|------|------|
| 1 | week.html → page-week.css | CSS 추출 2095줄 | 작음 |
| 2 | inha.html → page-inha.css | CSS 추출 577줄 | 작음 |
| 3 | admin.html → page-admin.css | CSS 추출 1419줄 | 작음 |
| 4 | page-week.css | font-weight 토큰화 | 작음 |
| 5 | page-week.css | border-radius 토큰화 | 작음 |
| 6 | page-inha.css, page-admin.css | 토큰 강제 | 중간 |
| 7 | tokens.css | focus-visible 전역 스타일 | 작음 |
| 8 | inha, week, admin | skip-link + ARIA | 작음 |
| 9 | — | 모바일 QA 검증 | 작음 |
| 10 | prototype.html | 아카이브로 이동 | 작음 |
