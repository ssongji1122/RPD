# Tab System & User Profile Redesign — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Claude Code 스타일의 3탭 시스템(Archive / Class / My Studio) + 좌하단 유저 프로필 + 관리자 드롭다운을 구현한다.

**Architecture:** 기존 HTML 파일을 유지하면서 공통 topbar에 탭 UI를 추가. 각 페이지에 `data-tab` 속성을 부여해 현재 탭을 자동 하이라이트. 사이드바는 탭별로 다른 내용을 표시. 유저 프로필은 사이드바 하단에 고정 배치.

**Tech Stack:** HTML, CSS custom properties, vanilla JS, localStorage (인증 없이 먼저, Supabase는 향후)

**Security Note:** shell.js 등에서 DOM 조작 시 createElement + textContent 방식을 사용할 것. innerHTML 대신 안전한 DOM 메서드 사용 필수.

---

## 현재 상태

### 파일 구조
```
course-site/
├── index.html          → 홈 (Archive 탭 허브)
├── library.html        → 카드 라이브러리 (Archive)
├── shortcuts.html      → 단축키 DB (Archive)
├── inha.html           → 인하대 수업 개요 (Class)
├── week.html           → 주차별 수업 (Class)
├── admin.html          → 관리자 (Admin — 관리자 전용)
├── prototype.html      → 디자인 프로토타입 (사용 안 함)
├── assets/
│   ├── tokens.css      → 디자인 토큰
│   ├── components.css  → 공유 컴포넌트
│   ├── layout.css      → 레일 + topbar + grid
│   ├── chrome.css      → RPD 브랜드 스타일
│   ├── page-index.css
│   ├── page-library.css
│   ├── page-shortcuts.css
│   └── meta.css
```

### 기존 레이아웃 (layout.css)
- `.app` grid: 56px(rail) + 1fr(main)
- `.app-topbar`: 로고 + 검색 + 우측 컨트롤
- `.rail`: 56px 접힘 / 220px 펼침
- 모바일(<=720px): rail → 하단 56px 탭바

### 페이지 → 탭 매핑
| 탭 | 페이지 | 역할 |
|---|---|---|
| **Archive** | index.html, library.html, shortcuts.html | 카드/단축키 아카이브 탐색 |
| **Class** | inha.html, week.html | 수업 수강 (주차별 실습) |
| **My Studio** | studio.html (신규) | 내 덱, 진도, 설정 |
| — | admin.html | 관리자 전용 (프로필 메뉴에서 접근) |

---

## 설계 결정사항

### 1. MPA 유지 + 탭 UI 오버레이
기존 HTML 파일을 그대로 유지. 탭 클릭 = 해당 HTML로 이동.
각 페이지에 `data-tab` 속성 부여하면 topbar 탭이 자동 활성화.

### 2. 사이드바 = 탭별 컨텍스트
| 탭 | 사이드바 내용 |
|---|---|
| Archive | 홈/카드찾기/단축키 메뉴 |
| Class | 주차 목록 (Week 1~15), 수업 목차 |
| My Studio | 내 덱 목록, 진도 현황, 설정 |

### 3. 유저 프로필 — 좌하단 (Claude Code 벤치마크)
- 클릭하면 드롭다운 메뉴 (설정, 진도, 관리자)
- "관리자 패널" 메뉴: role === 'admin' 일 때만 표시
- 비로그인: "게스트" + "이름 변경" 버튼

### 4. 모바일
- 상단: 탭 3개 (Archive/Class/My Studio) — 항상 표시
- 사이드바: 햄버거로 접근 (하단 탭바 제거)

### 5. 검색 — 탭별 컨텍스트
- Archive: 카드/단축키 검색
- Class: 주차/토픽 검색
- My Studio: 내 덱 검색

### 6. 딥링크 보존
기존 URL 100% 유지. week.html?week=3 은 Class 탭 활성화 상태로 로드.

### 7. 인증 (Phase 1: localStorage)
- 유저 이름 + 역할을 localStorage에 저장
- admin 역할: ?role=admin URL 파라미터로 설정
- Phase 2(향후): Google OAuth + Supabase

### 8. "내 덱" 정의
- 덱 = 카드 + 단축키의 커스텀 조합 (JSON 객체)
- 교수의 15주 커리큘럼 = "프리셋 덱" (읽기 전용)
- 학생은 프리셋 복제해서 편집 가능
- localStorage에 저장 (Phase 2에서 Supabase 동기화)

---

## Task 1: Topbar에 탭 UI 추가

**Files:**
- Modify: `course-site/assets/layout.css`
- Create: `course-site/assets/tab-system.js`

**Step 1: layout.css에 탭 스타일 추가**

**Step 2: 각 HTML body에 data-tab 속성 추가**

**Step 3: 각 HTML topbar에 탭 마크업 삽입**

**Step 4: tab-system.js — 현재 탭 자동 활성화 + 검색 placeholder 변경**

**Step 5: 시각 검증**

**Step 6: Commit**

---

## Task 2: 사이드바 탭별 컨텍스트 전환

**Files:**
- Modify: `course-site/assets/layout.css`
- Modify: 각 HTML 파일의 .rail 마크업

**Step 1: layout.css에 rail-context 스타일 추가**

**Step 2: 각 페이지 rail에 data-tab 기반 컨텍스트 섹션 추가**

**Step 3: tab-system.js에 현재 경로 기반 rail-item 활성화 추가**

**Step 4: Commit**

---

## Task 3: 좌하단 유저 프로필 (Claude Code 스타일)

**Files:**
- Modify: `course-site/assets/layout.css`
- Create: `course-site/assets/user-profile.js`
- Modify: 각 HTML .rail 마크업

**Step 1: layout.css에 유저 프로필 + 드롭다운 스타일 추가**

**Step 2: 각 HTML rail 하단에 유저 프로필 마크업 추가**

**Step 3: user-profile.js — localStorage 기반 유저 관리, 드롭다운, admin 역할**

**Step 4: Commit**

---

## Task 4: 모바일 탭바 재설계

**Files:**
- Modify: `course-site/assets/layout.css` (모바일 미디어 쿼리)

**Step 1: 기존 하단 탭바를 상단 탭 + 햄버거 사이드바로 변경**

**Step 2: 모바일 햄버거 버튼 + 오버레이 마크업 추가**

**Step 3: Commit**

---

## Task 5: studio.html 신규 생성 (My Studio 탭)

**Files:**
- Create: `course-site/studio.html`
- Create: `course-site/assets/page-studio.css`

**Step 1: 최소 HTML 구조 (빈 상태 UI)**

**Step 2: 기본 CSS**

**Step 3: Commit**

---

## Task 6: 공통 Shell 인젝션 (새 페이지용)

**Files:**
- Create: `course-site/assets/shell.js`

**Step 1: shell.js — createElement 방식으로 안전하게 topbar + rail 동적 생성**

data-shell 속성이 있는 페이지에만 적용. 기존 페이지는 영향 없음.

**Step 2: studio.html에 data-shell 적용**

**Step 3: Commit**

---

## Task 7: 기존 페이지에 탭 UI 통합

**Files:**
- Modify: 모든 HTML (index, library, shortcuts, inha, week)

**Step 1: 각 body에 data-tab 추가**

**Step 2: topbar에 탭 마크업 삽입**

**Step 3: script 태그 추가**

**Step 4: 사이드바에 유저 프로필 추가**

**Step 5: Commit**

---

## Task 8: 전체 시각 검증

| 검증 항목 | 체크 |
|-----------|------|
| index.html — Archive 탭 활성화 | |
| library.html — Archive 탭 활성화 | |
| shortcuts.html — Archive 탭 활성화 | |
| inha.html — Class 탭 활성화 | |
| week.html?week=3 — Class 탭 활성화 | |
| studio.html — My Studio 탭 활성화 | |
| 유저 프로필 드롭다운 동작 | |
| ?role=admin시 관리자 메뉴 노출 | |
| 모바일 (375px) — 상단 탭 + 햄버거 | |
| 다크/라이트 테마 전환 | |

---

## Summary

| Task | 파일 | 변경 |
|------|------|------|
| 1 | layout.css, tab-system.js | Topbar 탭 UI + 자동 활성화 |
| 2 | layout.css, 각 HTML | 사이드바 탭별 컨텍스트 |
| 3 | layout.css, user-profile.js | 좌하단 유저 프로필 + 드롭다운 |
| 4 | layout.css | 모바일: 상단 탭 + 햄버거 사이드바 |
| 5 | studio.html, page-studio.css | My Studio 페이지 (빈 상태) |
| 6 | shell.js | 공통 셸 인젝션 (새 페이지용) |
| 7 | 모든 HTML | 기존 페이지에 탭/프로필 통합 |
| 8 | — | 전체 시각 검증 |

### 향후 (이 플랜 범위 밖)
- Supabase + Google OAuth 연동
- localStorage에서 Supabase 마이그레이션
- 덱 CRUD 기능 (My Studio)
- 탭별 검색 컨텍스트 구현
- preset 시스템과 Class 탭 통합
