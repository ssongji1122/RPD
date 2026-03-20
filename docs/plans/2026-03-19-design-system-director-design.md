# Design System + Design Director — Design Document

> 작성일: 2026-03-19
> 기반: 브레인스토밍 세션에서 확정된 결정사항 + COURSE_SITE_STYLE_GUIDE + COGNITIVE_UI_GUIDE

---

## 1. 목표

RPD 사이트를 **덱 기반 모듈형 학습 플랫폼**으로 재구성하면서, 모든 페이지가 하나의 디자인 시스템 안에서 일관되게 동작하도록 한다.

두 가지를 만든다:
1. **DESIGN_SYSTEM.md** — 스페이싱, 컬러, 타이포, 컴포넌트의 유일한 규칙 문서
2. **Design Director 에이전트** — 수정 전후에 전체 밸런스를 검증하는 커맨드

---

## 2. 확정된 아키텍처 결정

### 2.1 페이지 구조

| 페이지 | 역할 | URL |
|--------|------|-----|
| index.html | 홈 — 카드 탐색 + 덱 필터 | `/` |
| deck.html | 덱 뷰어 — 순서 있는 학습 모드 | `/deck.html?id=inha-rpd-w03` |
| library.html | 카드 라이브러리 — 카테고리별 탐색 | `/library.html` |
| shortcuts.html | 단축키 DB — Show Me 연결 | `/shortcuts.html` |
| admin.html | 관리자 — 퍼블릭과 동일 디자인 + 편집 오버레이 | `/admin.html` |

- `week.html` → `deck.html`로 리네임
- 15주 커리큘럼 = 교수자 프리셋 덱 (curriculum.js 데이터 유지)
- 일반 사용자 덱 = 카드 + 메모 구조

### 2.2 레이아웃

```
┌─────────────────────────────────────────────┐
│  Topbar (로고 · 전역검색 · 테마/언어/로그인) │
├────────┬────────────────────────────────────┤
│  Rail  │  Main Content (max-width: 1180px)  │
│ 56/220 │                                    │
│        │                                    │
├────────┴────────────────────────────────────┤
│  모바일: Rail → 하단 탭바 56px               │
└─────────────────────────────────────────────┘
```

- 사이드 레일: 56px 접힘 / 220px 펼침 (토글)
- 레일 항목: 홈, 내 덱(서브목록), 카드 찾기, 단축키, 설정
- 모바일(≤720px): 레일 → 하단 탭바 + 텍스트 라벨

### 2.3 덱 시스템

- **저장**: localStorage + URL 파라미터 (`?deck=extrude,boolean,mirror&name=...`)
- **인증**: Google OAuth + Supabase (향후)
- **덱 데이터 구조**:

```js
{
  id: "inha-rpd-w03",
  name: "Week 3: 모델링 기초",
  color: "blue",           // 키컬러
  author: "송지",
  cards: [
    { cardId: "extrude", note: "꼭 따라해보세요" },
    { cardId: "loop-cut", note: "" }
  ],
  // 프리셋 전용 (선택)
  assignment: { ... },
  references: [ ... ]
}
```

- 프리셋 덱: curriculum.js 확장 필드 (steps, tasks, assignment) 유지
- 일반 덱: 카드 + 메모만

### 2.4 덱별 키컬러

6색 팔레트:

| 이름 | 값 | 용도 |
|------|-----|------|
| blue | `#93c5fd` | 기본, 인하대 프리셋 |
| green | `#34d399` | 사용자 덱 |
| purple | `#a78bfa` | 사용자 덱 |
| amber | `#fbbf24` | 사용자 덱 |
| rose | `#fb7185` | 사용자 덱 |
| cyan | `#22d3ee` | 사용자 덱 |

적용 범위:
- 덱 필터 칩의 아이콘 배경 + 보더
- 카드의 덱 표시 dot (6px 원)
- deck.html 헤더 악센트
- **그 외 UI에는 키컬러 사용 금지** — 본문, 버튼, 링크는 항상 기본 블루

### 2.5 카드 디자인 원칙

**기본 상태 = 아이콘 + 제목 (1행)**
- 설명, 태그, 상세 → hover/클릭/모달에서만
- 덱 소속 표시: 오른쪽에 dot + 약칭 (W3, UV 등)
- 12개 이상 카드가 보이면 설명 절대 기본 노출 안 함

### 2.6 단축키 → Show Me 연결

- Show Me 카드가 있는 단축키: `📖 Show Me →` 링크 표시
- 없는 단축키: 링크 없음 (빈 열 placeholder로 정렬 유지)

---

## 3. DESIGN_SYSTEM.md 구조

### 3.1 스페이싱 스케일

```
4px / 8px / 12px / 16px / 24px / 32px / 48px / 64px
```
이 값만 허용. 중간값(10px, 14px, 18px, 20px, 28px 등) 사용 금지.

### 3.2 border-radius 스케일

| 토큰 | 값 | 용도 |
|------|-----|------|
| `--radius-sm` | 8px | 인풋, 작은 칩 |
| `--radius` | 12px | 카드, 버튼 |
| `--radius-md` | 16px | 서브 패널 |
| `--radius-lg` | 20px | 섹션 컨테이너 (기존 18px→20px 통일) |
| `--radius-xl` | 24px | 사이드바, 검색바 |
| `--radius-pill` | 999px | 칩, 필터, 뱃지 |

기존 26px, 28px 등 중간값은 가장 가까운 스케일 값으로 통일.

### 3.3 font-weight 스케일

| 토큰 | 값 | 용도 |
|------|-----|------|
| `--fw-normal` | 400 | 본문 |
| `--fw-medium` | 500 | 캡션, 라벨 |
| `--fw-semi` | 600 | 카드 제목, 섹션 타이틀 |
| `--fw-bold` | 700 | h1, h2, 강조 |

기존 620, 630, 640, 650 등은 가장 가까운 스케일로 통일.

### 3.4 타이포 위계

| 역할 | 크기 | weight | letter-spacing |
|------|------|--------|----------------|
| h1 (페이지 제목) | clamp(1.5rem, 3vw, 2rem) | 700 | -.03em |
| h2 (섹션 제목) | clamp(1rem, 1.5vw, 1.2rem) | 600 | -.02em |
| card-title | .88rem | 600 | -.01em |
| body | .86rem | 400 | 0 |
| caption/chip | .72rem | 600 | .02em |
| kicker (대문자) | .68rem | 700 | .1em |

### 3.5 컬러 규칙

- 메인 강조색: 블루(`--key`) 하나만
- 덱 키컬러: dot/아이콘에만 허용, 텍스트/배경에 쓰지 않음
- 성공: 초록 — 완료 상태에서만
- 경고: 앰버 — 에러/경고에서만
- 카드 구분: 밝기 차 + 보더, 색으로 구분하지 않음

### 3.6 컴포넌트 카탈로그

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

### 3.7 금지 규칙

1. 카드에 설명 기본 노출 금지 (12개 이상일 때)
2. 한 페이지에서 강조색 역할 2개 이상 금지
3. 스페이싱 스케일 외의 값 사용 금지
4. font-weight 스케일 외의 값 사용 금지
5. border-radius 스케일 외의 값 사용 금지
6. 인라인 `<style>` 사용 금지 (외부 CSS 파일만)
7. 하드코딩 rgba 사용 금지 (토큰 사용)

---

## 4. Design Director 에이전트 설계

### 4.1 모드

| 모드 | 커맨드 | 동작 |
|------|--------|------|
| `pre-check` | `/design-agent pre-check "변경 설명"` | 변경 영향 분석 → 연쇄 수정 플랜 |
| `post-verify` | `/design-agent post-verify` | 전체 퍼블릭 페이지 스크린샷 비교 → 위반 리포트 |
| `audit` | `/design-agent audit {target}` | 기존 인지부하 감사 (유지) |
| `simplify` | `/design-agent simplify {target}` | 기존 저잡음 리디자인 (유지) |
| `system-check` | `/design-agent system-check` | DESIGN_SYSTEM.md vs 코드 불일치 감지 |

### 4.2 pre-check 흐름

```
1. 변경 설명 파싱 → 영향받는 CSS/HTML 파일 식별
2. DESIGN_SYSTEM.md 규칙 대조
3. 영향받는 다른 페이지 목록 생성
4. 위반 없음 → "✅ 진행하세요"
   위반 있음 → "⚠️ [규칙 번호] 위반. 연쇄 수정 필요: [파일 목록]"
```

### 4.3 post-verify 흐름

```
1. preview_start → 모든 퍼블릭 페이지 순회
2. 각 페이지 desktop(1440) + mobile(375) 스크린샷
3. DESIGN_SYSTEM.md 체크리스트 대조:
   - 스페이싱 스케일 준수?
   - 컬러 규칙 준수?
   - 카드 정보 밀도 1축?
   - 터치 타겟 44px?
   - focus-visible 있음?
4. 위반 리포트 출력
```

### 4.4 system-check 흐름

```
1. DESIGN_SYSTEM.md 파싱 → 규칙 목록 추출
2. tokens.css + components.css + page-*.css 스캔
3. 불일치 리포트:
   - 문서에 없는 토큰이 코드에 있음
   - 코드에서 금지 값 사용
   - 컴포넌트 카탈로그에 없는 패턴 사용
```

### 4.5 적용 범위

- 체크 대상: index.html, deck.html, library.html, shortcuts.html
- admin.html: 퍼블릭 동일 디자인 + 편집 오버레이 (기본 규칙 자동 상속)
- Show Me 카드: 독립 모달, 본 체크 범위 밖

---

## 5. 구현 순서

1. `docs/DESIGN_SYSTEM.md` 작성 (위 3장 내용)
2. `.claude/commands/design-agent.md` 업그레이드 (위 4장 내용)
3. `tokens.css` 정리 — 스페이싱/radius/weight 스케일에 맞게 통일
4. prototype.html → 실제 페이지 구현 (별도 플랜)

---

## 6. 기존 CSS 마이그레이션 상태

이미 완료된 작업 (이번 세션):
- ✅ tokens.css 토큰 확장 (fw, radius, glass)
- ✅ components.css 생성 + 전 페이지 연결
- ✅ shortcuts.html 인라인 CSS 외부 파일 분리
- ✅ index.html 인라인 CSS 외부 파일 분리

남은 작업 (다음 세션):
- ⬜ library.html 마이그레이션
- ⬜ week.html → deck.html 마이그레이션 + 덱 시스템 구현
- ⬜ FOUC 방지 + 접근성 통일
- ⬜ 전체 시각 회귀 검증
