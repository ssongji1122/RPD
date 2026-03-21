# 레이아웃 리디자인 — 프로토타입 → 실제 페이지 적용

> 작성일: 2026-03-20
> 기반: prototype.html + 2026-03-19 디자인 시스템 설계 문서

## 1. 목표

프로토타입에서 설계한 레일+탑바 레이아웃을 실제 페이지(index, library, shortcuts)에 적용한다.
하이브리드 방식: 공통 레이아웃 셸을 공유하되 각 페이지는 별도 HTML 유지.

## 2. 아키텍처

### 2.1 새 파일

| 파일 | 역할 |
|------|------|
| `assets/layout.css` | 공통 레이아웃 (app grid, topbar, rail, mobile tabbar) |
| `assets/layout.js` | 레일 토글, 현재 페이지 하이라이트 |

### 2.2 레이아웃 구조

```
.app (CSS Grid)
├── .app-topbar (grid-column: 1/-1, sticky top:0)
│   ├── .app-logo (BA)
│   ├── .app-title (Blender Archive RPD)
│   ├── .app-search (전역 검색)
│   └── .app-topbar-right (테마토글, 언어)
├── .rail (grid-row:2, 56px→220px)
│   ├── rail-item × 5 (홈, 내덱, 카드찾기, 단축키, 설정)
│   ├── rail-sub (덱 서브목록)
│   └── rail-toggle (접기/펼치기)
└── .main (grid-row:2, 메인 콘텐츠)
    └── .main-inner (max-width: 1180px)
```

### 2.3 모바일 (≤720px)

- `.app` grid: `1fr` 단일 컬럼 + 하단 56px 탭바
- `.rail` → 하단 고정, flex-row, justify-around
- `.rail-sub`, `.rail-toggle` 숨김
- `.rail-item` → 세로 (아이콘 + 6px 라벨)
- `.main` → padding-bottom: 80px (탭바 공간)

### 2.4 각 페이지별 변경

**index.html:**
- `.page-shell` → `.app` 교체
- `.topbar` + `.index-sidebar` 제거 → 공통 레일+탑바
- `.index-main` → `.main > .main-inner` 안으로 이동
- page-index.css에서 `.topbar`, `.index-sidebar`, `.index-layout` 스타일 제거

**library.html:**
- `.page-shell` → `.app` 교체
- `.lib-header` 제거 → 공통 탑바
- 기존 검색바+필터는 `.main` 안에 유지
- page-library.css에서 `.lib-header` 스타일 제거

**shortcuts.html:**
- `.page-shell` → `.app` 교체
- `.topbar` 제거 → 공통 탑바
- 히어로 섹션은 `.main` 안에 유지
- page-shortcuts.css에서 `.topbar` 관련 스타일 제거

## 3. 디자인 토큰 준수

- 레일 border-radius: `var(--radius)` (12px)
- rail-item height: 40px (터치타겟 44px 근접)
- spacing: `var(--sp-2)` (8px) gap, `var(--sp-6)` (24px) main padding
- font-weight: `var(--fw-medium)` (500) rail text, `var(--fw-semi)` (600) titles

## 4. 제거되지 않는 것

- tokens.css의 기존 `.topbar`, `.brand` 스타일은 유지 (week.html, admin.html이 아직 사용)
- 각 page-*.css의 콘텐츠 스타일은 유지 (카드, 섹션, 그리드 등)
- 기존 JS 로직 (curriculum.js, i18n.js, showme 관련) 유지

## 5. 향후

- week.html → deck.html 전환 시에도 동일한 레이아웃 셸 적용
- admin.html은 퍼블릭 디자인 확정 후 적용
