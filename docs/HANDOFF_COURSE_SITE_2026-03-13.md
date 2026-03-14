# Handoff: Course Site Build

작성일: 2026-03-13  
프로젝트 루트: `/Users/ssongji/Developer/Workspace/RPD`

## 1. 현재 목표

사용자는 `노션은 정리용`, `웹페이지는 수업용`으로 역할을 나누고 싶어 한다.

핵심 요구:

1. 학생이 한눈에 흐름을 이해할 수 있어야 한다.
2. 단순히 읽는 페이지가 아니라 `직접 따라하고 넘어가는 페이지`여야 한다.
3. Blender 수업 내용을 단계별로 수행하도록 만들고 싶다.
4. 15주차 전체를 운영할 수 있는 구조로 가고 싶다.
5. 시각 스타일은 `애플처럼 깔끔하고 가독성 좋고 인지가 잘 되는 방향`을 원한다.
6. 현재 페이지의 제목 폰트가 너무 크고 과하다는 피드백이 있었고, 그에 맞춰 밸런싱을 진행했다.

---

## 2. 지금까지 완료된 것

### 2.1 스타일 가이드 문서

- [Course Site Style Guide](/Users/ssongji/Developer/Workspace/RPD/docs/COURSE_SITE_STYLE_GUIDE_2026-03-13.md)
- [Lecture Infographic Style Guide](/Users/ssongji/Developer/Workspace/RPD/docs/LECTURE_INFOGRAPHIC_STYLE_GUIDE_2026-03-13.md)

의미:

- `Apple-like`한 정돈된 수업 사이트 방향을 문서화함
- 15주 구조에서 왜 단일 HTML보다 실제 웹사이트가 더 적합한지 정리함
- 공통 컬러, 타이포, 컴포넌트 규칙을 정리함

### 2.2 Week 02 노션용 템플릿

- [Week_02_Notion_Page_Template.md](/Users/ssongji/Developer/Workspace/RPD/Blender_2026/week_02/Week_02_Notion_Page_Template.md)

의미:

- 노션에 바로 복붙 가능한 형태로 Week 02 본문 템플릿이 정리되어 있음

### 2.3 Week 02 학생용 웹페이지 시안

- [week02_lecture_page_mockup.html](/Users/ssongji/Developer/Workspace/RPD/Blender_2026/week_02/week02_lecture_page_mockup.html)

현재 포함 내용:

1. 차분하게 밸런싱한 타이포와 카드 스타일
2. 단계별 실습 흐름
3. 체크리스트 기반 진도 저장
4. 공식 Blender 문서 카드
5. 단계별 짧은 시연 클립 연결
6. 단계별 starter `.blend` 다운로드 연결

### 2.4 Starter `.blend` 생성 스크립트와 결과물

- 생성 스크립트:
  [create_starter_blends.py](/Users/ssongji/Developer/Workspace/RPD/Blender_2026/week_02/create_starter_blends.py)

- 생성된 결과물:
  - [week02_factory_start.blend](/Users/ssongji/Developer/Workspace/RPD/Blender_2026/week_02/starter_files/week02_factory_start.blend)
  - [week02_navigation_practice.blend](/Users/ssongji/Developer/Workspace/RPD/Blender_2026/week_02/starter_files/week02_navigation_practice.blend)
  - [week02_transform_practice.blend](/Users/ssongji/Developer/Workspace/RPD/Blender_2026/week_02/starter_files/week02_transform_practice.blend)
  - [week02_pencil_holder_start.blend](/Users/ssongji/Developer/Workspace/RPD/Blender_2026/week_02/starter_files/week02_pencil_holder_start.blend)
  - [week02_feature_drill_start.blend](/Users/ssongji/Developer/Workspace/RPD/Blender_2026/week_02/starter_files/week02_feature_drill_start.blend)

---

## 3. 현재 페이지 확인 방법

이전 세션에서는 로컬 서버를 아래 방식으로 띄워서 확인했다.

```bash
cd /Users/ssongji/Developer/Workspace/RPD
python3 -m http.server 4173 --bind 127.0.0.1
```

확인 URL:

- [Week 02 Guided Lesson](http://127.0.0.1:4173/Blender_2026/week_02/week02_lecture_page_mockup.html)

참고:

- 다음 세션에서는 서버가 안 떠 있을 수 있으므로 다시 실행해야 한다.

---

## 4. 공식 문서 연결 상태

현재 페이지에 아래 공식 문서가 연결되어 있다.

1. [Preferences Introduction](https://docs.blender.org/manual/en/latest/editors/preferences/introduction.html)
2. [3D View Navigation](https://docs.blender.org/manual/en/latest/editors/3dview/navigate/introduction.html)
3. [Extrude Region](https://docs.blender.org/manual/en/latest/modeling/meshes/tools/extrude_region.html)
4. [Loop Cut](https://docs.blender.org/manual/en/latest/modeling/meshes/tools/loop.html)
5. [Bevel](https://docs.blender.org/manual/en/latest/modeling/meshes/tools/bevel.html)

페이지에는 문서 링크뿐 아니라 공식 문서 이미지 미리보기도 붙여두었다.

---

## 5. 사용자 피드백 메모

다음 세션에서 반드시 유지해야 할 사용자 선호:

1. 제목 폰트가 너무 크고 과한 느낌은 싫다.
2. 전체적으로 `애플처럼 깔끔하고`, `인지 잘 되고`, `가독성 좋은` 스타일이 좋다.
3. 노션은 정리가 잘 되지만 한눈에 잘 안 들어오므로, 수업용 웹페이지가 필요하다.
4. 학생들이 시연만 보고 바로 따라오기 힘들고, 영상만 봐도 잊어버리기 쉬우니 `직접 따라하고 체크하는 구조`를 원한다.

---

## 6. 아키텍처 판단

현재 결론:

- `단일 HTML로 15주차 운영`은 비추천
- `작은 수업 웹사이트`로 가는 것이 맞음

추천 방향:

### 1순위 추천

`Astro + MDX`

이유:

1. 콘텐츠 중심 구조에 적합
2. 15주 페이지를 파일 단위로 관리하기 쉬움
3. 정적 사이트로 빠르게 운영 가능
4. 스타일 가이드와 공통 템플릿 적용이 쉬움

### 보류 가능한 방향

`Next.js`

필요해지는 시점:

1. 로그인
2. 학생별 저장
3. 제출 상태 동기화
4. 서버 기반 기능이 필요할 때

현재는 아직 이 단계까지는 아님.

---

## 7. 다음 세션에서 가장 먼저 할 일

다음 세션의 최우선 작업은 `수업 사이트 골격 생성`이다.

권장 순서:

1. `course-site` 폴더 생성
2. Astro 프로젝트 초기화
3. 공통 레이아웃 만들기
4. 공통 스타일 토큰과 컴포넌트로 분리
5. Week 02 페이지를 첫 실제 페이지로 이식
6. Week별 콘텐츠를 MDX 또는 데이터 파일로 분리

---

## 8. 추천 사이트 구조

다음 세션에서 만들면 좋은 디렉터리 예시:

```text
course-site/
├─ src/
│  ├─ components/
│  │  ├─ Hero.astro
│  │  ├─ StepCard.astro
│  │  ├─ VideoCard.astro
│  │  ├─ StarterFileCard.astro
│  │  ├─ OfficialDocsCard.astro
│  │  └─ ProgressBar.astro
│  ├─ layouts/
│  │  └─ CourseLayout.astro
│  ├─ content/
│  │  └─ weeks/
│  │     ├─ week-01.mdx
│  │     ├─ week-02.mdx
│  │     └─ ...
│  ├─ pages/
│  │  ├─ index.astro
│  │  ├─ weeks/
│  │  │  ├─ 01.astro
│  │  │  ├─ 02.astro
│  │  │  └─ ...
│  │  └─ resources.astro
│  └─ styles/
│     └─ tokens.css
├─ public/
│  ├─ media/
│  │  └─ week02/
│  ├─ starter-files/
│  │  └─ week02/
│  └─ images/
└─ package.json
```

---

## 9. Week 02 이식 시 유지해야 할 요소

아래 요소는 다음 세션에서도 반드시 유지하거나 컴포넌트화해야 한다.

1. 단계 잠금 / 완료 체크 / 진도 저장 구조
2. 공식 문서 카드
3. 단계별 짧은 클립
4. 단계별 starter 파일
5. `자주 막히는 지점` 보완 카드
6. 과제 연결 구조

---

## 10. 확인해야 할 오픈 포인트

다음 세션에서 사용자에게 확인하거나 결정할 만한 것:

1. 15주 전체 주차 이름/주제 목록이 이미 정리되어 있는지
2. 각 주차마다 `starter .blend`를 만들 계획인지
3. 클립은 로컬 파일 기반으로 둘지, 나중에 외부 업로드를 할지
4. 학생 진행 저장은 브라우저 로컬 저장만으로 충분한지
5. 사이트 배포까지 할지, 로컬/학내 공유 수준으로 운영할지

---

## 11. 바로 이어서 사용할 명령어

Starter 파일을 다시 생성해야 할 경우:

```bash
'/Applications/Blender.app/Contents/MacOS/Blender' \
  --background \
  --python /Users/ssongji/Developer/Workspace/RPD/Blender_2026/week_02/create_starter_blends.py
```

페이지 로컬 확인:

```bash
cd /Users/ssongji/Developer/Workspace/RPD
python3 -m http.server 4173 --bind 127.0.0.1
```

---

## 12. 다음 세션용 한 줄 지시문

다음 세션에서는 `Week 02 HTML 시안`을 기반으로 `15주 운영 가능한 Astro 기반 course-site 골격`을 만들고,  
현재 스타일 가이드에 맞는 공통 레이아웃/컴포넌트/토큰 시스템을 먼저 세팅한 뒤, `Week 02`를 첫 실제 페이지로 이식하면 된다.
