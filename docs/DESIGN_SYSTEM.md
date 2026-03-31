# RPD Design System

> Source of Truth — 모든 CSS 코드는 이 문서의 스케일과 규칙을 따른다.
> 마지막 업데이트: 2026-03-27

---

## 1. 스페이싱 스케일

허용값:

```
4px / 8px / 12px / 16px / 24px / 32px / 48px / 64px
```

| 토큰 | 값 |
|------|----|
| `--sp-1` | 4px |
| `--sp-2` | 8px |
| `--sp-3` | 12px |
| `--sp-4` | 16px |
| `--sp-6` | 24px |
| `--sp-8` | 32px |
| `--sp-12` | 48px |
| `--sp-16` | 64px |

이 값만 허용. 중간값(10px, 14px, 18px, 20px, 28px 등) 사용 금지.

---

## 2. border-radius 스케일

| 토큰 | 값 | 용도 |
|------|----|------|
| `--radius-sm` | 8px | 인풋, 작은 칩 |
| `--radius` | 12px | 카드, 버튼 |
| `--radius-md` | 16px | 서브 패널 |
| `--radius-lg` | 20px | 섹션 컨테이너 (기존 18px→20px 통일) |
| `--radius-xl` | 24px | 사이드바, 검색바 |
| `--radius-pill` | 999px | 칩, 필터, 뱃지 |

기존 26px, 28px 등 중간값은 가장 가까운 스케일 값으로 통일.

---

## 3. font-weight 스케일

| 토큰 | 값 | 용도 |
|------|----|------|
| `--fw-normal` | 400 | 본문 |
| `--fw-medium` | 500 | 캡션, 라벨 |
| `--fw-semi` | 600 | 카드 제목, 섹션 타이틀 |
| `--fw-bold` | 700 | h1, h2, 강조 |

기존 620, 630, 640, 650 등은 가장 가까운 스케일로 통일.

---

## 4. 타이포 위계

| 역할 | 크기 | weight | letter-spacing |
|------|------|--------|----------------|
| h1 (페이지 제목) | clamp(1.5rem, 3vw, 2rem) | 700 | -.03em |
| h2 (섹션 제목) | clamp(1rem, 1.5vw, 1.2rem) | 600 | -.02em |
| card-title | .88rem | 600 | -.01em |
| body | .86rem | 400 | 0 |
| caption/chip | .72rem | 600 | .02em |
| kicker (대문자) | .68rem | 700 | .1em |

---

## 5. 컬러 규칙

- **메인 강조색**: 블루(`--key`) 하나만 사용
- **덱 키컬러**: dot/아이콘에만 허용, 텍스트/배경에 쓰지 않음
- **성공**: 초록 — 완료 상태에서만
- **경고**: 앰버 — 에러/경고에서만
- **카드 구분**: 밝기 차 + 보더, 색으로 구분하지 않음

---

## 6. 덱 키컬러 팔레트

| 이름 | 값 | 용도 |
|------|----|------|
| blue | `#93c5fd` | 기본, 인하대 프리셋 |
| green | `#34d399` | 사용자 덱 |
| purple | `#a78bfa` | 사용자 덱 |
| amber | `#fbbf24` | 사용자 덱 |
| rose | `#fb7185` | 사용자 덱 |
| cyan | `#22d3ee` | 사용자 덱 |

**적용 범위:**
- 덱 필터 칩의 아이콘 배경 + 보더
- 카드의 덱 표시 dot (6px 원)
- deck.html 헤더 악센트
- **그 외 UI에는 키컬러 사용 금지** — 본문, 버튼, 링크는 항상 기본 블루

---

## 7. 컴포넌트 카탈로그

| 컴포넌트 | 클래스 | 용도 |
|---------|--------|------|
| Glass Panel | `.rpd-glass-panel` | 사이드바, 검색바, 모달 |
| Glass Card | `.rpd-glass-card` | 패널 안 자식 카드 |
| Glass Surface | `.rpd-glass-surface` | 대형 섹션 블록 |
| Filter Chip | `.rpd-filter-chip` | 검색/필터 UI |
| Pill Count | `.rpd-pill-count` | 카운터 뱃지 |
| Icon Well | `.rpd-icon-well` | 44px 아이콘 박스 |
| Kicker | `.rpd-kicker` | 대문자 아이브로우 텍스트 |
| Search Input | `.rpd-search-input` | 검색 인풋 |
| Hero Mesh | `.hero-mesh` | animated gradient 배경 (히어로) |
| Journey Phase | `.journey-phase` | Phase 그룹 컨테이너 |
| Journey Card | `.journey-week-card` | compact 주차 카드 |
| Progress Track | `.journey-progress-track` | 진행률 바 (4px, green fill) |
| Quick Link | `.archive-quick-link` | pill 형태 아카이브 바로가기 |

---

## 8. 금지 규칙

1. 카드에 설명 기본 노출 금지 (12개 이상일 때)
2. 한 페이지에서 강조색 역할 2개 이상 금지
3. 스페이싱 스케일 외의 값 사용 금지
4. font-weight 스케일 외의 값 사용 금지
5. border-radius 스케일 외의 값 사용 금지
6. 인라인 `<style>` 사용 금지 (외부 CSS 파일만)
7. 하드코딩 rgba 사용 금지 (토큰 사용)
8. 이모지 아이콘 사용 금지 (Lucide SVG만)
9. 신규 페이지에 `chrome.css` 사용 금지 (레거시 — week.html/inha.html 전용)

---

## 9. CSS 파일 구조

| 파일 | 역할 | 모든 페이지 |
|------|------|-------------|
| `tokens.css` | 디자인 토큰 (색상, 타이포, 간격, radius) | ✅ 필수 |
| `components.css` | 공유 컴포넌트 (.rpd-* 클래스) | ✅ 필수 |
| `layout.css` | 앱 셸 (topbar, rail, main 레이아웃) | ✅ 필수 |
| `page-*.css` | 페이지별 전용 스타일 | 해당 페이지만 |
| `chrome.css` | 레거시 — week.html, inha.html 전용 | 신규 사용 금지 |

**페이지별 CSS 매핑:**

| 페이지 | CSS 파일 |
|--------|---------|
| index.html | page-index.css |
| library.html | page-library.css |
| shortcuts.html | page-shortcuts.css |
| inha.html | page-inha.css |
| week.html | page-week.css |
| studio.html | page-studio.css |
| admin.html | page-admin.css |

---

## 10. 앱 셸 레이아웃

```
┌─────────────────────────────────┐
│  app-topbar (56px 고정)          │
│  [햄버거] [로고] [탭바] [테마]    │
├────────┬────────────────────────┤
│ rail   │  main                  │
│ 56px   │  (flex: 1, 스크롤)     │
│ →220px │                        │
│ (hover)│                        │
└────────┴────────────────────────┘
```

- **`app-topbar`**: 탭바 가운데 정렬, topbar-left / topbar-right 양끝
- **`rail`**: 56px 기본 → hover 220px. 하단에 유저 프로필 (`rail-user`)
- **`main`**: overflow-y: auto, max-width: var(--max-width), padding: 24px

**주의:**
- `admin.html`에 `.rail` 클래스 추가 금지 → layout.css 충돌로 사이드바 화면 밖으로 밀림
- `week.html` sidebar에 `.rpd-page-rail` 클래스 추가 금지 → chrome.css의 `position:static`이 `position:fixed`를 덮어씀 (모바일 콘텐츠 844px 아래로 밀림)

---

## 11. 탭 시스템

3탭 구조 — topbar 가운데 `.app-tabs`에 위치:

| 탭 | 페이지 | `data-tab` |
|----|--------|-----------|
| Archive | index.html | `archive` |
| Class | inha.html | `class` |
| My Studio | studio.html | `studio` |

- 활성 탭: `.app-tab.is-active`
- `<body data-tab="studio">` 로 현재 탭 표시
- JS: `tab-system.js` 에서 URL 기반 자동 활성화

---

## 12. 아이콘 시스템

**Lucide Icons SVG** (stroke, no fill) 사용. 이모지 사용 금지.

```html
<!-- 표준 패턴 -->
<svg width="18" height="18" viewBox="0 0 24 24"
     fill="none" stroke="currentColor"
     stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
     aria-hidden="true">
  ...
</svg>
```

- `aria-hidden="true"` 필수 (텍스트와 함께 사용 시)
- `stroke="currentColor"` → CSS `color` 로 색상 제어
- 기본 크기: 18px (레일), 16px (버튼), 13-14px (인라인)

---

## 13. 유저 프로필

Claude Code 스타일 좌하단 고정. `rail-user` → `rail-user-btn` → `rail-user-menu`.

- 이름/역할 localStorage 저장 (`rpd-user-name`, `rpd-user-role`)
- `admin-only` 클래스: admin 유저만 메뉴 항목 표시 (JS 제어)
- 구현: `user-profile.js`

---

## 14. 덱 시스템 컴포넌트 (My Studio)

**파일 구조:**
- `deck-store.js` — localStorage CRUD + 프리셋 생성
- `deck-ui.js` — 렌더링 + 모달 + 카드 피커
- `page-studio.css` — 전용 스타일

**주요 클래스:**

| 클래스 | 역할 |
|--------|------|
| `.deck-grid` | auto-fill, minmax(240px, 1fr) |
| `.deck-card` | 덱 카드 (기본) |
| `.deck-card.is-preset` | 프리셋 덱 (파란색 강조) |
| `.deck-btn` | 덱 카드 내 작은 버튼 |
| `.deck-modal-overlay` | 모달 오버레이 (fixed, backdrop-blur) |
| `.card-picker-list` | 카드 선택 리스트 (flex-column, max-height: 240px) |

**중요 버그 패턴:**
- `.deck-field input:not([type="checkbox"])` — checkbox에 `width:100%` 적용 방지 필수

**데이터 구조:**
```js
{
  id: 'deck-xxx',       // 자동 생성
  preset: false,         // true = 읽기 전용 프리셋
  name: '덱 이름',
  description: '',
  items: [{ type: 'card', id: 'slug' }],
  createdAt: ISO,
  updatedAt: ISO
}
```

---

## 15. 접근성

- **focus-visible**: `tokens.css` 전역 — `outline: 2px solid var(--key-soft)`
- **skip-link**: 모든 페이지 `<a href="#main" class="skip-link">본문으로 건너뛰기</a>`
- **터치 타겟**: 최소 44×44px (버튼, 링크)
- **최소 폰트**: 12px (`.82rem` 이하 금지)
- **한국어 line-height**: 본문 1.7, UI 레이블 1.4

---

## 16. 한국어 텍스트 스타일

토스(Toss) 스타일 해요체 사용:

| 금지 | 사용 |
|------|------|
| ~합니다 / ~입니다 | ~해요 / ~있어요 |
| ~하십시오 | ~해 주세요 |
| ~하였습니다 | ~했어요 |
| ~할 수 있습니다 | ~할 수 있어요 |

빈 상태 메시지: `아직 X가 없어요. Y를 해 보세요.`
