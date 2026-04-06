# RPD Design Guide

## Product Context
- **What:** 인하대 Blender 수업 플랫폼 (학습 허브, 주차별 콘텐츠, Show Me 카드, 덱 관리)
- **Who:** 대학생, 3D 입문자
- **Type:** 학습 대시보드 (web app)
- **Stack:** 바닐라 HTML/CSS/JS, GitHub Pages

## Aesthetic Direction
- **Direction:** Flat Outline (2026.04 전환)
- **Mood:** 깔끔하고 도구적. Linear, Raycast 같은 느낌. 콘텐츠가 주인공이고, UI는 배경.
- **Anti-patterns:** gradient overlay, radial-gradient glow, backdrop-filter blur, inset glow ring, box-shadow halo. 전부 금지.

## Color System

### Accent: Mint
| Token | Dark | Light | 용도 |
|-------|------|-------|------|
| `--key` | `#00bfa5` | `#00897b` | Primary 버튼, 인터랙티브 요소 |
| `--key-strong` | `#009e8a` | `#006b5f` | Hover/pressed 상태 |
| `--key-soft` | `#6ee8d8` | `#00897b` | 텍스트 액센트, 아이콘 활성 |
| `--key-border` | `rgba(110,232,216,.28)` | `rgba(0,137,123,.2)` | 포커스 보더, 활성 카드 |

### Surfaces (Dark 기본)
| Token | Value | 용도 |
|-------|-------|------|
| `--bg` | `#0a0a0a` | 페이지 배경 |
| `--bg-soft` | `#101113` | 약간 밝은 배경 |
| `--surface` | `#141517` | 카드, 패널 배경 |
| `--surface-strong` | `#191b1e` | 강조 패널 배경 |
| `--line` | `rgba(255,255,255,.08)` | 기본 보더 |
| `--line-strong` | `rgba(255,255,255,.14)` | 강조 보더 |

### Semantic
| Token | Value | 용도 |
|-------|-------|------|
| `--success` | `#10b981` | 완료, 성공 |
| `--warn` | `#f59e0b` | 경고 |
| `--text` | `#f5f5f7` | 본문 텍스트 |
| `--muted` | `#a1a1aa` | 보조 텍스트 |
| `--muted-strong` | `#d4d4d8` | 준강조 텍스트 |

## Typography
- **Font:** Noto Sans KR (Google Fonts CDN)
- **Fallback:** -apple-system, BlinkMacSystemFont, Apple SD Gothic Neo, sans-serif
- **Scale:**
  - Hero: `clamp(1.5rem, 2.4vw, 2rem)`
  - Section: `clamp(1.12rem, 1.6vw, 1.4rem)`
  - Sub: `clamp(1rem, 1.3vw, 1.14rem)`
  - Body: `.84rem ~ .88rem`
  - Small: `.75rem ~ .78rem`
- **Weights:** 400(normal) / 500(medium) / 600(semi) / 700(bold)
- **Korean wrapping:** `word-break: keep-all; overflow-wrap: break-word`

## Spacing
- **Base unit:** 4px
- **Scale:** 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64
- **Density:** Comfortable (카드 내부 18~24px padding)
- **CSS tokens:** `--sp-1`(4) `--sp-2`(8) `--sp-3`(12) `--sp-4`(16) `--sp-6`(24) `--sp-8`(32) `--sp-12`(48) `--sp-16`(64)

## Border Radius
| Token | Value | 용도 |
|-------|-------|------|
| `--radius-sm` | 8px | 칩, 인풋, 작은 요소 |
| `--radius` | 12px | 카드, 패널 |
| `--radius-md` | 16px | 모달 |
| `--radius-lg` | 20px | 히어로 카드 |
| `--radius-xl` | 24px | 사이드카드 |
| `--radius-pill` | 999px | 뱃지, 아바타 |

## Layout

### App Shell
```
grid-template-columns: 56px minmax(0, 1fr)   /* rail collapsed */
grid-template-columns: 220px minmax(0, 1fr)   /* rail expanded */
grid-template-rows: auto minmax(0, 1fr)
```
- **Topbar:** `grid-column: 1/-1`, sticky, 중앙 탭 3개 (Archive / Class / My Studio)
- **Rail:** 56px collapsed, 220px expanded, sticky
- **Main:** `max-width: 1180px`, padding 24px 28px

### Responsive Breakpoints
| Width | 변화 |
|-------|------|
| 1100px | 콘텐츠 좁힘 |
| 980px | 2열 → 1열 |
| 720px | 모바일 전환: 햄버거, 사이드바 오버레이, 탭바 분리 |
| 600px | 최소 폰 사이즈 |

## Card Pattern (핵심)

**모든 카드의 기본형:**
```css
.card {
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--surface);
  padding: 18px;
}
.card:hover {
  border-color: var(--line-strong);
}
```

**활성/선택 카드:**
```css
.card.is-active {
  border-color: var(--key-border);
  background: var(--glass-accent);
}
```

**하지 말 것:**
- `background: linear-gradient(...)` — 플랫 color만 사용
- `box-shadow: 0 16px 32px rgba(...)` — 글로우 금지
- `backdrop-filter: blur(...)` — 블러 금지
- `inset 0 1px 0 rgba(255,255,255,...)` — 상단 하이라이트 금지
- `radial-gradient(...)` — 장식 그라디언트 금지

## Button Pattern
```css
/* Primary */
.btn-primary {
  border: 1px solid var(--key-strong);
  background: var(--key);
  color: #fff;
  border-radius: var(--radius-sm);
  padding: 10px 18px;
}

/* Ghost */
.btn-ghost {
  border: 1px solid var(--line-strong);
  background: transparent;
  color: var(--muted-strong);
}
```

## Icon System
- **Library:** Lucide Icons (SVG inline, 18x18, stroke-width 2)
- **이모지 금지.** UI 아이콘은 반드시 SVG.
- **Active color:** `var(--key-soft)`

## Motion
- **Approach:** Minimal-functional (상태 전환만)
- **Duration:** `.14s` (hover), `.2s` (layout shift)
- **Easing:** `ease` (기본), `ease-in-out` (layout)
- **Transition targets:** `color`, `background`, `border-color`, `opacity`
- **금지:** 입장 애니메이션, scroll-driven 효과, decorative keyframes

## CSS Architecture
```
tokens.css      — 디자인 토큰 (색상, 타이포, 스페이싱, 라디우스)
components.css  — 공용 컴포넌트 (버튼, 인풋, 뱃지, 모달)
layout.css      — 앱 셸 (topbar, rail, main grid)
page-*.css      — 페이지별 스타일
chrome.css      — 레거시 (week/inha 전용, 신규 금지)
meta.css        — 상태 뱃지, 유틸
surface.css     — 페이지 셸 배경
```

## Decisions Log
| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-04-06 | Blue → Mint 전환 | 파란색이 촌스럽다는 피드백. 민트가 다크 배경에 더 세련됨 |
| 2026-04-06 | Glassmorphism → Flat Outline | 학습 플랫폼에 장식이 과함. 콘텐츠 우선. -154 LOC |
