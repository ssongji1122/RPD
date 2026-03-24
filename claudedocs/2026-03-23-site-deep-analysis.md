# RPD Course Site — 종합 분석 리포트

> 분석일: 2026-03-23
> 범위: course-site/ 전체 (7 HTML, 10 CSS, 8 JS, ~89K LOC)
> 관점: 디자인 일관성, 퀄리티, 구성, 구조, 내용, 퍼포먼스, 아키텍처

---

## Executive Summary

| 도메인 | 등급 | 요약 |
|--------|------|------|
| CSS 아키텍처 | B+ | 토큰 시스템 우수, 하드코딩 값 산재 |
| 디자인 일관성 | C+ | 2개 레이아웃 패러다임 공존 (app-grid vs page-shell) |
| HTML 구조/접근성 | B | skip-link 있으나 ARIA 불균등 |
| JavaScript 품질 | B- | XSS 리스크(innerHTML), ES5 스타일 혼재 |
| 퍼포먼스 | C+ | 렌더블로킹 리소스, FOUC 패치워크 |
| 콘텐츠 아키텍처 | B+ | i18n 체계 탄탄, 데이터-뷰 분리 양호 |

---

## 1. CSS 아키텍처

### 1.1 토큰 시스템 (tokens.css — 793 lines)

**장점**
- Dark/Light 완벽 이중 테마 토큰 (200+ 변수)
- 스페이싱 스케일 (`--sp-1` ~ `--sp-16`), font-weight 4단계 정의
- Glass morphism 토큰 체계화 (tint, shadow, border, accent)

**🔴 CRITICAL: 하드코딩 값 대량 잔존**

| 문제 | 파일 | 건수 |
|------|------|------|
| `border-radius: [raw px]` | 모든 CSS | **44건** |
| `font-weight: [raw number]` (토큰 외) | chrome/meta/shortcuts/library | **11건** |
| `rgba()` 하드코딩 | 모든 CSS | **237건** |

구체적 위반 사례:
```
chrome.css:64   → font-weight: 650   (토큰에 없는 값)
chrome.css:387  → font-weight: 650
chrome.css:450  → font-weight: 620   (토큰에 없는 값)
meta.css:64     → font-weight: 620
page-library.css:354 → font-weight: 560   (토큰에 없는 값)
page-shortcuts.css:103 → font-weight: 500 (--fw-medium=500이지만 직접 수치 사용)
```

**font-weight 불일치**: 토큰은 400/500/600/700 4단계인데, 실제 CSS에서 500, 560, 620, 650 등 **6가지 이상** 서로 다른 값을 사용. 디자인 시스템의 제약이 작동하지 않음.

**border-radius 불일치**: 토큰은 8/12/16/20/24/999 6단계인데, `14px`, `18px`, `22px`, `26px` 등 토큰에 없는 값 다수 사용. 특히 `components.css`에서 `.rpd-glass-card { border-radius: 16px }` 처럼 토큰 대신 직접 값을 쓰는 패턴.

### 1.2 CSS 파일 구조

```
tokens.css (793L) → 공유 토큰 + 리셋 + 공유 컴포넌트(!)
  ├── components.css (171L) → glass 컴포넌트
  ├── layout.css (298L) → app-grid 레이아웃 (index/library/shortcuts)
  ├── surface.css (53L) → inha용 패널 프리미티브
  ├── chrome.css (531L) → inha용 topbar/rail/hero
  ├── meta.css (126L) → inha용 pill/chip 프리미티브
  ├── page-index.css (550L)
  ├── page-library.css (878L)
  └── page-shortcuts.css (273L)
```

**🟡 IMPORTANT: 두 개의 레이아웃 패러다임 공존**

| 패러다임 | 사용 페이지 | 레이아웃 | CSS 파일 |
|----------|-------------|----------|----------|
| **App Grid** (.app) | index, library, shortcuts | 56px rail + main | layout.css |
| **Page Shell** (.page-shell) | inha, week, admin | topbar + page-rail | chrome.css + surface.css + meta.css |

동일 컴포넌트(topbar, 테마토글, 검색)를 완전히 다른 마크업과 CSS로 두 번 구현함. 이는 유지보수 비용을 2배로 만듦.

### 1.3 CSS 로드 패턴 불일치

| 페이지 | CSS 로드 체인 |
|--------|---------------|
| index.html | tokens → components → layout → page-index |
| library.html | tokens → components → layout → page-library |
| shortcuts.html | tokens → components → layout → page-shortcuts |
| inha.html | tokens → surface → meta → chrome (+ inline `<style>`) |
| week.html | tokens → components (+ inline `<style>`) |
| admin.html | tokens → components (+ inline `<style>`) |

**week.html과 admin.html은 아직 인라인 CSS 미분리 상태** — 핸드오프 문서에도 기록됨.

---

## 2. 디자인 일관성

### 2.1 Topbar

| 요소 | App Grid (index/lib/shortcuts) | Page Shell (inha/week/admin) |
|------|--------------------------------|------------------------------|
| 구조 | `.app-topbar` (flex 3col) | `.topbar` → `.topbar-inner` (flex/grid) |
| 로고 | `.app-logo` (text "BA") | `.brand-badge` (text "BA") |
| 검색 | `.app-search` (글로벌 input) | 없음 (각 페이지에 자체 검색) |
| 테마토글 | 동일 마크업 | 동일 마크업 |
| 반응형 | 720px breakpoint | 1100px + 720px breakpoints |

**🟡 같은 사이트인데 네비게이션 패턴이 다름**: App Grid 페이지는 좌측 Rail 네비게이션, Page Shell 페이지는 Topbar 중앙 탭 네비게이션. 사용자가 index → inha로 이동하면 네비게이션 위치가 완전히 바뀜.

### 2.2 타이포그래피 스케일 불일치

히어로 제목 font-size:
- index: `clamp(1.5rem, 3vw, 2rem)`
- shortcuts: `clamp(2rem, 4vw, 3rem)` — 50% 더 큼!
- week: `clamp(1.42rem, 2.2vw, 1.9rem)`
- library: `clamp(1.34rem, 2.4vw, 1.94rem)`

→ 4개 페이지, 4개 서로 다른 타이포 스케일. 디자인 시스템의 타이포 스케일이 부재함.

### 2.3 컴포넌트 중복 정의

| 컴포넌트 | 정의 위치 | 문제 |
|----------|-----------|------|
| `.rpd-icon-well` | components.css:76 **AND** surface.css:40 | 두 파일에서 서로 다른 스타일로 중복 정의 |
| `.status-pill` | tokens.css:524 **AND** meta.css:82 | 두 곳에서 정의, meta가 tokens를 덮어씀 |
| `.hero-meta-chip` | page-index.css:122 **AND** meta.css:68 | 서로 다른 스타일 충돌 |
| `.content-block` | tokens.css:371 **AND** page-shortcuts.css:138 | shortcuts에서 재정의 |
| `filter-chip` | components.css(rpd-filter-chip) vs page-shortcuts.css(filter-chip) | 동일 패턴, 다른 클래스명 |

---

## 3. HTML 구조 & 접근성

### 3.1 구조 일관성

**🟢 양호**
- 모든 페이지: `<!DOCTYPE html>`, `lang="ko"`, viewport meta, favicon
- FOUC 방지 인라인 스크립트 통일 (theme + lang 복원)
- skip-link 있음 (index, library, shortcuts)

**🟡 이슈**

| 이슈 | 심각도 | 상세 |
|------|--------|------|
| Rail 네비게이션이 모든 페이지에 **100% 동일 마크업으로 복붙** | Medium | 변경 시 6개 파일 동시 수정 필요 |
| inha/week/admin에 skip-link 없음 | Medium | 접근성 불균등 |
| `<main>` id 불일치 | Low | index: `id="main-content"`, library: `id` 없음 (skip-link 타겟 `#libMain`) |

### 3.2 ARIA 분포

```
index.html      →  8건 (rail aria-label, theme button)
library.html    → 30건 (검색, 필터, 상태 표시 등 - 우수)
shortcuts.html  → 24건 (양호)
week.html       → 54건 (가장 많음 - 우수)
admin.html      →  5건 (부족)
inha.html       →  5건 (부족)
```

library와 week는 접근성 노력이 명확히 보이지만, admin과 inha는 거의 없음.

### 3.3 innerHTML 사용 (XSS 리스크)

```
index.html:     4건 (HTML 문자열 빌드 후 innerHTML 할당)
week.html:      8건
admin.html:     19건 (가장 많음)
library.html:   2건
shortcuts.html: 2건
inha.html:      3건
_helpers.js:    2건
```

**🔴 CRITICAL**: `index.html`의 `buildHeroActions()`, `buildArchiveItems()` 등에서 `innerHTML`로 HTML 문자열을 직접 생성. 데이터 소스가 `CURRICULUM` 배열(정적 신뢰 데이터)이라 현재는 안전하지만, **admin.html의 19건은 사용자 입력이 들어갈 수 있어 위험**.

---

## 4. JavaScript 품질

### 4.1 아키텍처

```
site-shell.js   → RPDAppShell (IIFE, window 전역)
i18n.js         → RPDI18n (IIFE, window 전역)
week-ui.js      → RPDWeekUI (IIFE, window 전역)
layout.js       → 즉시 실행 (IIFE, 부수효과)
curriculum.js   → CURRICULUM 전역 배열
```

**패턴**: 모든 JS가 ES5 IIFE + window 전역 객체 패턴. 모듈 시스템 없음. 빌드 도구 없음.

**장점**
- 각 모듈의 책임 분리가 명확 (i18n, UI 설정, 앱 셸)
- 데이터-뷰 분리 양호 (curriculum.json → curriculum.js → 렌더 함수)
- 프리셋 시스템이 유연 (URL param, localStorage 기반 preset 전환)

**🟡 이슈**

| 이슈 | 파일 | 상세 |
|------|------|------|
| `var` 전용 (let/const 없음) | 전체 | ES5 호환성 의도적이지만, strict mode도 일부만 |
| `forEach` + 문자열 조합 | index.html | DOM 조작과 문자열 빌드 혼용 (일부는 createElement, 일부는 innerHTML) |
| 전역 함수 선언 | index.html | `renderPage()`, `buildHeroMeta()` 등 20+ 함수가 전역 스코프 |
| `script` 태그 7개 순차 로딩 | index.html | 번들링 없이 7개 파일 순차 요청 |
| 매직 넘버 | week-ui.js | `DEFAULT_CONFIG` 내 다수의 하드코딩 값 |

### 4.2 i18n 시스템 (i18n.js — 1,817 lines)

**잘 된 점**: 완전한 ko/en 이중 언어 지원, 페이지별 문자열 분리, localStorage 기반 언어 전환.

**이슈**: 1,800줄 단일 파일에 모든 번역 문자열이 들어있음. 별도 JSON으로 분리하면 캐싱/유지보수가 나아짐.

---

## 5. 퍼포먼스

### 5.1 렌더링 경로

```
1. HTML 파싱 시작
2. <head> 내 CSS 4~5개 순차 로딩 (렌더 블로킹)
3. FOUC 방지 인라인 JS 실행
4. </head>
5. <body> 파싱
6. </body> 직전 JS 7개 순차 로딩
7. JS 실행 → DOM 렌더링
```

**🟡 이슈**

| 이슈 | 영향 | 해결 |
|------|------|------|
| Google Fonts 외부 CSS @import | FCP +200~500ms | `<link rel="preload">` 또는 로컬 호스팅 |
| JS 7개 순차 `<script>` | 네트워크 워터폴 | 번들링 또는 `defer` |
| CSS 4개 순차 `<link>` | 렌더 블로킹 | 크리티컬 CSS 인라인 + 나머지 async |
| tokens.css 793줄 전체 로딩 | 미사용 규칙 다수 | 페이지별 사용 토큰만 추출 (선택적) |
| innerHTML 기반 대량 DOM 생성 | 리플로우 | DocumentFragment 사용 |

### 5.2 이미지/미디어

- `img, video { max-width: 100%; display: block; }` — 기본 반응형 이미지 처리 있음
- `loading="lazy"` 없음 — week.html의 step 이미지들에 적용 필요
- `.step-video { max-height: 420px }` — 고정 높이, aspect-ratio 미사용

---

## 6. 콘텐츠 아키텍처

### 6.1 정보 구조

```
index.html ─── 허브: 아카이브 소개 + 주차 그리드
  ├── library.html ─── Show Me 카드 라이브러리 (카테고리+검색+ABC)
  ├── shortcuts.html ─── 단축키 DB (검색+카테고리+키보드뷰)
  ├── week.html?week=N ─── 주차별 실습 페이지
  ├── inha.html ─── 인하대 전용 수업 허브 (index와 유사하지만 별도)
  └── admin.html ─── 커리큘럼 관리자
```

**🟡 index.html과 inha.html의 역할 중복**: 둘 다 "주차별 수업 목록"을 보여주는 허브 페이지. 차이는 inha가 학교 커스텀 UI인데, 핸드오프 문서에 따르면 index가 "아카이브 허브", inha가 "학교별 맞춤 페이지"로 분리 의도.

### 6.2 데이터 흐름

```
curriculum.json (원본 데이터, Notion 동기화)
    ↓
curriculum.js (정적 CURRICULUM 배열로 변환)
    ↓
각 HTML 페이지 (JS에서 DOM 생성)
    ↓
i18n-content.js (보충 번역 데이터)
i18n.js (번역 엔진)
week-ui.js (UI 프리셋/설정)
```

양호한 분리. 데이터 소스가 명확하고, 각 계층의 책임이 구분됨.

---

## 7. 우선순위별 권장 사항

### 🔴 Critical (즉시)

1. **admin.html innerHTML XSS**: 사용자 입력이 innerHTML로 들어가는 19개 지점 확인 후 textContent/createElement로 교체
2. **font-weight 토큰 통일**: 650, 620, 560 → 토큰 값(400/500/600/700)으로 매핑
3. **`.rpd-icon-well` 중복 정의 해소**: surface.css의 정의 제거 또는 components.css로 통합

### 🟡 Important (다음 스프린트)

4. **레이아웃 패러다임 통일**: app-grid 또는 page-shell 중 하나로 수렴 (핸드오프 문서의 프로토타입이 app-grid 기반이므로 이쪽으로 통일 권장)
5. **border-radius 하드코딩 제거**: `14px` → `var(--radius)`, `26px` → `var(--radius-xl)` 등 매핑
6. **rgba() 하드코딩 감소**: 반복 사용되는 237건의 rgba 중 테마 의미가 있는 것을 토큰으로 승격
7. **Rail 네비게이션 컴포넌트화**: 6개 HTML에 동일 마크업 복붙 → JS include 또는 Web Component
8. **week.html / admin.html 인라인 CSS 분리**: 핸드오프 문서에 이미 기록된 미완 작업
9. **타이포 스케일 토큰 도입**: hero-title, section-title 등 의미 기반 토큰으로 통일
10. **ARIA 균등화**: admin.html, inha.html에 skip-link + 주요 aria 레이블 추가

### 🟢 Recommended (개선)

11. **Google Fonts preload**: `@import` → `<link rel="preload">`
12. **JS 번들링 또는 defer**: 7개 script 순차 로딩 최적화
13. **i18n.js 문자열 분리**: 1,800줄 → 페이지별 JSON + 공유 엔진
14. **step 이미지 lazy loading**: `loading="lazy"` 속성 추가
15. **CSS 선택자 명명 일관성**: `rpd-` prefix 있는 것과 없는 것 혼재 (`.filter-chip` vs `.rpd-filter-chip`)

---

## 8. 긍정적 평가

- **토큰 기반 테마 시스템**: Dark/Light 완벽 전환, 변수 체계가 잘 잡혀있음
- **i18n 시스템**: ko/en 완전 이중 언어, 동적 전환, localStorage 영속화
- **프리셋 시스템**: URL param 기반 학교별 커스텀 — 확장성 우수
- **FOUC 방지**: 모든 페이지에 일관된 인라인 스크립트
- **반응형**: 모든 페이지에 mobile breakpoint 대응
- **Glass morphism 디자인**: 시각적 완성도가 높고, 토큰으로 체계화
- **데이터-뷰 분리**: curriculum → render 파이프라인이 깔끔
- **Show Me 카드 아키텍처**: 40+ 카드를 독립 HTML로 관리하는 구조가 효율적

---

## 9. 메트릭 요약

| 메트릭 | 값 |
|--------|-----|
| HTML 페이지 | 7 (+ 40+ showme 카드) |
| CSS 파일 | 10 (3,673 LOC) |
| JS 파일 | 8 (8,059 LOC) |
| CSS 토큰 변수 | 200+ |
| 하드코딩 border-radius | 44건 |
| 하드코딩 font-weight | 11건 |
| 하드코딩 rgba() | 237건 |
| innerHTML 사용 | 41건 |
| ARIA 속성 | 127건 (불균등 분포) |
| 인라인 `<style>` 잔존 | 4 페이지 |
