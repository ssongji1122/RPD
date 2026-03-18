# RPD Card Modal Tone Guide

`Show Me` 카드 모달을 `course-site` 전반의 기준 시각 언어로 쓰기 위한 실무 가이드.

## Source of Truth

- 기준 화면: `course-site/week.html`의 `Show Me modal`
- 적용 대상: `index.html`, `library.html`, `shortcuts.html`, `admin.html`, 이후 추가되는 `course-site/*.html`
- 공통 토큰: `course-site/assets/tokens.css`의 `--modal-*` 변수군

## Visual Principles

1. 평면 리스트보다 `겹친 표면`이 먼저 보여야 한다.
2. 큰 영역은 `panel`, 그 안의 반복 항목은 `soft panel` 또는 `card`로 분리한다.
3. 활성 상태는 단순한 좌측 라인보다 `블루 틴트 + 내부 보더 + 약한 glow`로 표현한다.
4. 검색, 필터, 목차, 주차 목록처럼 반복 인터랙션이 많은 UI는 `브라우저 패널` 톤을 따른다.
5. 정보는 줄이되, 시각적 깊이는 유지한다.
6. 톤을 바꿔도 각 페이지의 `원래 정보 구조`는 유지한다.

## Shared Tokens

아래 토큰을 먼저 쓰고, 페이지별 보정은 그다음 단계에서만 한다.

- `--modal-panel-bg`: 큰 셸 배경
- `--modal-panel-soft-bg`: 반복 카드 배경
- `--modal-panel-soft-strong-bg`: 입력창/버튼처럼 조금 더 또렷한 표면
- `--modal-panel-shadow`: 큰 셸 그림자
- `--modal-card-shadow`: 카드 내부 하이라이트
- `--modal-hover-shadow`: hover 카드 그림자
- `--modal-active-shadow`: active 카드 그림자
- `--modal-top-line`: 상단 하이라이트 라인
- `--modal-accent-bg`: active/featured 카드 배경
- `--modal-hover-bg`: hover 카드 배경
- `--modal-nav-active-bg`: 좌측 탐색/필터 active 배경
- `--modal-icon-bg`: 아이콘 타일 배경
- `--modal-icon-shadow`: 아이콘 타일 그림자

## Component Patterns

### 1. Hero Shell

- 큰 제목 영역은 반드시 하나의 패널 안에 넣는다.
- 최소 요소: `eyebrow`, `title`, `description`, `CTA`, `meta chip`
- 배경은 `--modal-panel-bg`, 보더는 `var(--line)`, 상단 라인은 `--modal-top-line`

### 2. Browser Rail

- 좌측 목차, 필터 패널, 주차 리스트는 `브라우저 패널`처럼 묶는다.
- 항목은 개별 버튼처럼 보여야 한다.
- active는 `--modal-nav-active-bg` + `rgba(96,165,250,.34)` 보더를 기본값으로 쓴다.

### 3. Repeated Cards

- 반복 목록은 플랫한 `border-bottom list`보다 `rounded card grid/list`를 우선한다.
- 기본 카드: `18px~22px radius`
- hover: `translateY(-1px ~ -2px)` + `--modal-hover-bg`
- active/featured: `--modal-accent-bg` + `--modal-active-shadow`

### 4. Search / Filter Controls

- 입력창은 패널 안에 들어가야 한다.
- 검색창 배경은 `--modal-panel-soft-strong-bg`
- 필터 칩은 좌측 라인보다 `pill`로 처리한다.

### 5. Stat / Meta Chips

- 통계, 주차, 개수 표시는 전부 `pill`
- `padding: 6px 10px` 전후
- `border: 1px solid var(--line)` 또는 약한 블루 보더

### 6. Icon Tile

- 아이콘은 그냥 텍스트를 두지 말고 사각 타일에 담는다.
- `--modal-icon-bg` + `--modal-icon-shadow` 사용

## Page Mapping

### `index.html`

- Hero, archive blocks, week cards는 전부 카드 셸 안에 넣는다.
- 현재 주차 카드는 featured card처럼 한 단계 더 강조한다.

### `library.html`

- 헤더 검색영역, 좌측 목차, 섹션 그룹, 카드 리스트를 모두 modal browser 계열로 맞춘다.
- 카드 브라우저라는 성격이 강하므로 `nav rail + content panel` 구조를 유지한다.

### `shortcuts.html`

- DB성 화면이라도 표 형태보다 `검색 패널 + 카테고리 패널 + row cards` 흐름을 우선한다.
- 카테고리 그룹은 섹션 카드로 나누고, 각 단축키 행도 개별 카드처럼 보여야 한다.

### `admin.html`

- 관리 페이지도 예외가 아니다.
- 좌측 주차 목록, 상단 상태 배지, 입력 필드, step editor를 modal shell 체계로 맞춘다.
- 단, 공개 웹페이지처럼 `left rail + hero + section flow`를 유지해야 하며 별도 백오피스 대시보드처럼 재구성하지 않는다.
- 내부 편집 미리보기는 가능하면 `week.html`의 hero / practice / reference / assignment 흐름을 그대로 따라간다.
- 단, 가독성이 우선이므로 과한 장식은 금지한다.

### `week.html`

- 이미 기준 화면 역할을 하므로 큰 방향을 바꾸지 않는다.
- 새 섹션을 추가할 때는 modal tone을 벗어나지 않게만 유지한다.

## Do / Don’t

### Do

- 하나의 큰 배경 안에 다시 카드 레이어를 분리한다.
- hover/active 차이를 분명하게 준다.
- 같은 페이지 안에서 radius, border 강도, 그림자 톤을 일관되게 유지한다.
- 텍스트보다 `패널 구조`로 정보 위계를 만든다.
- 디자인 톤을 입혀도 페이지 고유의 정보 순서와 섹션 구성은 유지한다.

### Don’t

- border-bottom만 있는 평면 리스트로 돌아가지 않는다.
- active를 `파란 텍스트만`으로 처리하지 않는다.
- 페이지마다 radius와 shadow 스타일을 새로 만들지 않는다.
- 밝은 페이지/어두운 페이지를 섞어 톤을 깨지 않는다.
- `admin.html`을 공개 사이트와 동떨어진 별도 콘솔/대시보드 구조로 바꾸지 않는다.

## Implementation Checklist

- `course-site/assets/tokens.css`의 `--modal-*` 토큰을 우선 사용했는가
- hero/search/sidebar/section/card가 각각 다른 깊이 레이어로 분리됐는가
- active 상태가 hover보다 명확한가
- 모바일에서 패널 패딩과 radius가 너무 크지 않은가
- `week.html` Show Me modal 옆에 놓아도 같은 제품군처럼 보이는가
- 카드 모달 톤을 적용한 뒤에도 각 페이지의 원래 정보 구조가 유지되는가
