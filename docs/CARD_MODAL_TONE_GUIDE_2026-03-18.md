# RPD Card Modal Tone Guide

`Show Me` 카드 모달을 `course-site` 전반의 기준 시각 언어로 쓰기 위한 실무 가이드.

## Source of Truth

- 기준 화면: `course-site/week.html`의 `Show Me modal`
- 적용 대상: `index.html`, `library.html`, `shortcuts.html`, `admin.html`, 이후 추가되는 `course-site/*.html`
- 공통 토큰: `course-site/assets/tokens.css`의 `--modal-*` 변수군
- 공통 스타일 계층:
  - `course-site/assets/surface.css` = panel / shell / surface
  - `course-site/assets/meta.css` = pill / chip / status / meta
  - `course-site/assets/chrome.css` = topbar / rail / navigation chrome

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
- `--pill-radius`: 사이트 전체 pill/capsule 기본 반경
- `--pill-padding-y`, `--pill-padding-x`: pill 내부 여백 기본값

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

### 6. Capsule System

- 사이트 전체에서 `pill/capsule`은 한 가지 외곽 규격만 쓴다.
- 기본값은 `--pill-radius: 18px`를 기준으로 한다.
- 기본 control 높이는 `--pill-control-height: 40px`, 내부 세그먼트는 `--pill-inner-radius: 12px`를 기준으로 한다.
- 이 규격은 `tokens.css`의 값과 `meta.css`의 capsule primitives가 함께 책임진다.
- primary CTA, ghost 버튼, 필터 칩, 통계 칩, 주차 칩, meta chip은 전부 같은 외곽 반경을 공유한다.
- 차이는 `배경 / 보더 / 텍스트 색`으로만 주고, pill마다 반경을 다시 정하지 않는다.
- `999px` 완전 원형 pill은 쓰지 않는다. 너무 둥근 CTA와 덜 둥근 stat chip이 한 화면에 섞이면 제품 톤이 무너진다.
- 예외는 `언어 토글 내부 세그먼트`처럼 아주 작은 내부 버튼뿐이다. 이 경우에도 바깥 shell은 같은 pill 체계를 유지한다.

### 7. Icon Tile

- 아이콘은 그냥 텍스트를 두지 말고 사각 타일에 담는다.
- `--modal-icon-bg` + `--modal-icon-shadow` 사용

### 8. High-Fidelity Infographics

- `Show Me` 카드 내부 인포그래픽은 장식이 아니라 핵심 설명면이다. 카드 바깥 셸보다 안쪽 도식이 약해 보이면 실패로 본다.
- 선, 화살표, 배지, 라벨은 가능하면 `DOM + CSS` 또는 `SVG`로 만든다. 한국어 라벨은 가능한 한 살아있는 텍스트 레이어로 유지한다.
- `canvas`가 꼭 필요하면 CSS 표시 크기와 별도로 고밀도 backing store를 잡고, `devicePixelRatio` 기준으로 다시 그린다.
- 작은 고정 캔버스를 CSS로 키워 쓰지 않는다. 핵심 비교 도식이 필요하면 레이아웃 자체를 더 크게 잡는다.
- 이미지나 스크린샷은 표시 크기보다 충분히 큰 원본을 사용한다. 안쪽 텍스트가 흐리면 이미지를 키우는 대신 주석 레이어를 따로 분리해 다시 만든다.
- 브라우저/플랫폼별 차이가 큰 이모지나 흐린 래스터 아이콘을 핵심 설명 아이콘으로 쓰지 않는다.
- 설명력이 중요한 도식은 `텍스트 축소`로 문제를 숨기지 않는다. 패널 수를 줄이거나, 2열을 1열로 바꾸거나, 단계 수를 나눠서라도 선명도를 확보한다.
- 기준은 단순 해상도 수치보다 `실제 모달 크기에서 바로 읽히는가`다.

### 9. Korean Copy Wrapping

- 한국어 설명문은 기본적으로 `word-break: keep-all`, `line-break: strict`, `overflow-wrap: normal`을 사용한다.
- hero 설명, 카드 설명, 상단 소개문처럼 의미 단위가 중요한 카피에는 `rpd-readable-copy` 유틸을 우선 적용한다.
- 브라우저 자동 줄바꿈만으로는 원하는 지점에서 끊기지 않으면, CSS로 억지로 맞추지 말고 문장 안에 `<wbr>`를 넣어 `의미 단위` 브레이크 포인트를 명시한다.
- 꼭 붙어 보여야 하는 짧은 구는 `<span class="rpd-phrase-keep">...</span>`으로 묶고, 그 앞에 `<wbr>`를 둬서 `여기서 끊기면 좋다`는 신호를 준다.
- 기준은 `어색한 음절 분리 방지`보다 한 단계 더 나아가, `읽기 좋은 구 단위 줄바꿈`이다.
- 예: `수업 페이지입니다.<wbr> <span class="rpd-phrase-keep">필요한 주차만</span> 바로 열어볼 수 있습니다.`
- 반대로 조사나 어미 앞에서 강제로 끊기게 만드는 별도 spacing hack은 쓰지 않는다.

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
- 가능하면 `admin`은 별도 설명용 셸을 만들지 말고, `실제 웹페이지 + 편집 모드` 형태로 유지한다.
- 내부 편집 미리보기는 `week.html`의 hero / practice / reference / assignment 흐름을 그대로 따라간다.
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
- CTA와 stat/filter pill의 roundness를 다르게 주지 않는다.
- 밝은 페이지/어두운 페이지를 섞어 톤을 깨지 않는다.
- `admin.html`을 공개 사이트와 동떨어진 별도 콘솔/대시보드 구조로 바꾸지 않는다.
- 실제 웹페이지 위에 얇게 얹을 수 있는 편집 모드를, 불필요한 보조 히어로/소개 섹션으로 다시 감싸지 않는다.
- 한국어 hero/body 카피를 브라우저 기본 줄바꿈에만 맡겨서 어색한 구 단위 분리가 생기게 두지 않는다.
- 작은 저해상도 캔버스나 이미지를 크게 확대해 핵심 인포그래픽 자리에 두지 않는다.
- 라벨이 흐린 스크린샷/비트맵을 그대로 유지한 채 카드 바깥 셸만 고급스럽게 다듬지 않는다.
- 핵심 설명 도식에 이모지 아이콘이나 브라우저 기본 글리프를 그대로 써서 품질 편차를 만들지 않는다.

## Implementation Checklist

- `course-site/assets/tokens.css`의 `--modal-*` 토큰을 우선 사용했는가
- hero/search/sidebar/section/card가 각각 다른 깊이 레이어로 분리됐는가
- active 상태가 hover보다 명확한가
- 모바일에서 패널 패딩과 radius가 너무 크지 않은가
- `week.html` Show Me modal 옆에 놓아도 같은 제품군처럼 보이는가
- 카드 모달 톤을 적용한 뒤에도 각 페이지의 원래 정보 구조가 유지되는가
- 핵심 인포그래픽이 실제 표시 크기에서 선명하게 읽히는가
- 인포그래픽 안의 텍스트가 살아있는 레이어 또는 고밀도 렌더링으로 처리됐는가
- 비교/도식 패널이 너무 작아서 정보가 압축돼 보이지 않는가
- 이미지/스크린샷이 표시 크기에 비해 충분한 원본 해상도를 갖고 있는가
