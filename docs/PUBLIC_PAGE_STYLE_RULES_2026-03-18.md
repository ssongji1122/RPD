# Public Page Style Rules

이 문서는 `course-site` 공개 페이지의 공통 디자인 규칙을 한 기준으로 명시합니다.

적용 대상:
- `/Users/ssongji/Developer/Workspace/RPD/course-site/index.html`
- `/Users/ssongji/Developer/Workspace/RPD/course-site/inha.html`
- `/Users/ssongji/Developer/Workspace/RPD/course-site/library.html`
- `/Users/ssongji/Developer/Workspace/RPD/course-site/shortcuts.html`

기본 원칙:
- 한 제품처럼 보여야 한다.
- 구조와 타이포 규칙은 공통으로 유지한다.
- 페이지별 accent 색은 유지할 수 있다.
- 메인 화면이 먼저 읽혀야 하고, 보조 내비는 시선을 빼앗지 않는다.
- 복잡한 대시보드보다 깔끔한 인덱스/브라우저 감각을 우선한다.

## 1. 공통 구조

모든 공개 페이지는 아래 구조를 우선 사용한다.

1. `topbar`
2. `hero`
3. `left rail`
4. `main content`

공통 클래스:
- `rpd-brand-lockup`
- `rpd-topbar-3col`
- `rpd-topbar-nav`
- `rpd-topbar-utils`
- `rpd-hero-card`
- `rpd-hero-copy`
- `rpd-hero-title`
- `rpd-hero-description`
- `rpd-hero-meta-wrap`
- `rpd-page-layout`
- `rpd-page-rail`
- `rpd-page-main`

## 2. 타이포 스케일

공개 페이지 헤더/히어로의 크기 규칙은 `chrome.css` root token을 기준으로 통일한다.

주요 token:
- `--rpd-brand-title-size`
- `--rpd-brand-meta-size`
- `--rpd-hero-title-size`
- `--rpd-hero-body-size`
- `--rpd-hero-body-line-height`

원칙:
- 브랜드 타이틀은 작고 안정적이어야 한다.
- hero 제목은 페이지마다 문구가 달라도 같은 크기 체계를 쓴다.
- 설명문은 과장하지 않고 읽기 쉬운 밀도로 유지한다.

## 3. 좌측 레일 규칙

좌측 레일은 `보조 내비게이션`이다.

넣는 정보:
- 공개 페이지 바로가기
- 현재 페이지 스냅샷
- 현재 화면을 이해하는 데 필요한 최소 정보

넣지 않는 정보:
- hero와 중복되는 큰 설명
- 메인 콘텐츠보다 더 강한 강조
- 카드처럼 과도하게 독립된 보조 패널 연출

선택 상태:
- 선택 항목은 배경 강조보다 `텍스트 색 변화`를 우선한다.
- 사용자의 시선은 레일이 아니라 메인 콘텐츠로 가야 한다.

토글:
- 데스크톱에서도 레일을 접고 펼칠 수 있다.
- 토글은 텍스트 버튼보다 아이콘 중심으로 작고 조용하게 둔다.

## 4. 색 규칙

공통으로 맞추는 것:
- 구조
- spacing
- radius
- control height
- typography scale

페이지별로 달라도 되는 것:
- accent color
- hero tint
- page-specific emphasis

즉, `형태는 하나`, `accent는 페이지 성격대로`가 원칙이다.

## 5. 톤 앤 매너

- dark modal family 안에 있는 제품처럼 보여야 한다.
- line-only 화면보다 soft surface를 우선한다.
- 정보는 선명하되 과장되지 않아야 한다.
- 선택/상태/active는 조용하고 명확해야 한다.
- 텍스트는 한국어 문장 호흡에 맞게 끊긴다.

## 6. 예외

예외적으로 자체 정보 구조가 더 중요한 페이지는 내부 UI를 유지할 수 있다.

예:
- `week.html`: 학습 step/accordion 흐름이 우선
- `admin.html`: 편집 도구 흐름이 우선

단, 이 경우에도 topbar / panel tone / typography scale은 가능한 한 공통 시스템을 따른다.
