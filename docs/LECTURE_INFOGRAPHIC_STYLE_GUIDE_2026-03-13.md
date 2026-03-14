# Lecture Infographic Style Guide

작성일: 2026-03-13
대상 작업공간: `/Users/ssongji/Developer/Workspace/RPD`

## 1. 목적

`reference` 폴더 자체에는 실제 소스가 없었고, 현재 작업물에서 확인 가능한 최근 스크린샷과 강의 제작 스크립트를 기준으로 레퍼런스 스타일을 역분석했다.

목표는 아래 3가지다.

1. 레퍼런스의 장점은 유지한다.
2. 너무 비슷해 보이지 않게 시각 언어를 재해석한다.
3. 강의 페이지를 `깔끔한 인포그래픽` 구조로 일관되게 생성할 수 있는 기준을 만든다.

---

## 2. 레퍼런스 스타일 분석

최근 스크린샷에서 반복적으로 보인 특징:

1. 배경은 거의 완전한 블랙이다.
2. 텍스트는 `굵은 흰색 한 줄 메시지` 중심이다.
3. 포인트 컬러는 1개만 강하게 사용한다.
4. 원형 아이콘, 단계 번호, 흐름선, 카드형 강조 박스가 자주 등장한다.
5. 한 화면에 메시지는 적고, 구조는 아주 단순하다.
6. 정보 전달 방식은 `설명`보다 `요약 도식화`에 가깝다.

현재 코드에서도 같은 패턴이 확인된다.

- 타이틀 카드가 `짙은 배경 + 중앙 정렬 + 상단 소제목 + 큰 제목` 구조로 만들어져 있다.
- 오버레이 시스템이 `강조색`, `둥근 사각형`, `하이라이트 박스`, `짧은 텍스트 콜아웃` 중심으로 설계돼 있다.

관련 근거:

- [Blender_2026/concat_clips.py](/Users/ssongji/Developer/Workspace/RPD/Blender_2026/concat_clips.py#L18)
- [Blender_2026/overlay_images.py](/Users/ssongji/Developer/Workspace/RPD/Blender_2026/overlay_images.py#L74)
- [docs/NOTION_REBUILD_BLUEPRINT_2026-03-07.md](/Users/ssongji/Developer/Workspace/RPD/docs/NOTION_REBUILD_BLUEPRINT_2026-03-07.md#L200)

---

## 3. 그대로 가져가도 되는 것

이 요소들은 레퍼런스의 `형식`이므로 가져가도 괜찮다.

1. 검은색 또는 아주 어두운 배경 기반
2. 굵은 제목 + 짧은 보조 설명
3. 단계형 흐름도
4. 아이콘 + 숫자 + 한 줄 메시지 조합
5. 긴 문단 대신 카드 단위 정보 분리
6. 스크린샷 위에 콜아웃을 얹는 방식

---

## 4. 반드시 바꿔야 하는 것

아래는 복제 느낌을 피하기 위해 의도적으로 바꿔야 한다.

1. 포인트 컬러를 형광 그린 계열에서 완전히 벗어난다.
2. 중앙 정렬 한 줄 슬라이드 패턴을 쓰더라도 `컬러`, `폰트`, `아이콘 톤`은 분명히 바꾼다.
3. 원형 아이콘만 반복하지 말고 `카드`, `칩`, `세로 타임라인`, `2열 인포그래픽`을 보조적으로 섞는다.
4. 동일한 검은 배경 대비만 쓰지 말고, 아주 짙은 남청/먹청 톤의 표면 레이어를 둔다.
5. 강조 방식도 단순 glow 대신 `라인`, `배경 틴트`, `번호 배지`, `미세 보더`로 나눈다.

핵심은 `레이아웃 리듬은 유지하되, 컬러와 서체의 인상을 완전히 내 것으로 바꾸는 것`이다.

---

## 5. 제안하는 나만의 키 컬러

레퍼런스의 네온 그린을 피하면서도, 기술적이고 차분한 인상을 주는 컬러로 아래를 추천한다.

### 컬러 이름

`RPD Signal Blue`

### 메인 팔레트

- Key: `#3B82F6`
- Key Strong: `#2563EB`
- Key Soft: `#93C5FD`
- Key Tint: `rgba(59, 130, 246, 0.14)`
- Background: `#06080D`
- Surface 1: `#0D1320`
- Surface 2: `#121A2B`
- Border: `rgba(147, 197, 253, 0.28)`
- Text Primary: `#F8FAFC`
- Text Secondary: `#94A3B8`

### 왜 이 컬러가 맞는가

1. 초록 계열과 충분히 멀어서 레퍼런스 복제 느낌이 줄어든다.
2. 블렌더, 툴, 인터페이스, 프로세스 설명 같은 `기술형 강의`와 잘 맞는다.
3. 인포그래픽에서 선, 번호, 배지, 하이라이트 박스에 모두 안정적으로 쓸 수 있다.
4. 검은 배경에서도 과하게 시끄럽지 않고 정리된 인상을 준다.

---

## 6. 제안하는 폰트 방향

중앙 정렬 한 줄 슬라이드 패턴을 유지한다면, 사실 가장 큰 차이는 `폰트`에서 난다.

### 6.1 추천 조합 A

- 제목: `Paperlogy 7Bold` 또는 `Paperlogy 8ExtraBold`
- 본문/보조텍스트: `SUIT`

느낌:

1. 제목은 힘 있고 또렷하다.
2. 본문은 깔끔해서 인포그래픽과 잘 맞는다.
3. 기존 바이럴 슬라이드 톤과 거리를 만들기 쉽다.

### 6.2 추천 조합 B

- 제목: `S-Core Dream 8Heavy`
- 본문/보조텍스트: `Pretendard` 또는 `SUIT`

느낌:

1. 조금 더 공학적이고 강의자료다운 인상
2. 숫자, 단계, 키워드 카드에 잘 어울림

### 6.3 추천 조합 C

- 제목/본문 통일: `SUIT`
- 제목만 weight를 크게 사용

느낌:

1. 가장 깔끔하고 안정적
2. 노션/웹/영상 자막까지 통일하기 쉽다
3. 대신 개성은 조금 덜하므로 색 체계가 중요해진다

### 6.4 내 추천

가장 무난하고 결과가 좋은 조합은 아래다.

- 제목: `Paperlogy 8ExtraBold`
- 보조텍스트: `SUIT Medium`
- 영어 라벨 / Week 표기: `SUIT SemiBold`

이 조합이면 `한 줄 메시지의 존재감`은 살리면서도 기존 레퍼런스보다 더 브랜드화된 인상을 줄 수 있다.

---

## 7. 페이지 스타일 방향

한 장짜리 강의 페이지를 만든다면, `슬라이드 묶음`이 아니라 아래처럼 `정보 설계된 스크롤 페이지`가 좋다.

다만 사용자가 선호하는 패턴을 반영해서, 각 섹션의 첫 화면은 `중앙 정렬 한 줄 메시지`로 시작하고 바로 다음 화면에서 인포그래픽 설명으로 확장하는 2단 구조를 추천한다.

### 7.1 전체 구조

1. Hero
2. 오늘 배울 것
3. 개념 흐름도
4. 핵심 기능 설명
5. 화면 캡처 + 콜아웃
6. 실습 순서
7. 과제 / 체크리스트
8. 참고 자료

### 7.2 화면 규칙

1. 각 대단락의 시작 화면은 `중앙 정렬 한 줄 메시지`를 써도 좋다.
2. 대신 바로 다음 화면에서는 `제목 + 짧은 설명 + 시각 요소`로 내용을 풀어준다.
3. 한 줄 슬라이드는 전체의 35~45% 정도까지는 허용 가능하다.
4. 나머지 화면은 카드, 도식, 순서도, 표, 콜아웃으로 채운다.
5. 각 섹션의 핵심 정보는 3~5개 단위로 끊는다.
6. 아이콘은 선형 스타일로 통일한다.

---

## 8. 추천 레이아웃 시스템

### 8.1 Hero

- 좌측: `Week`, 수업명, 한 줄 요약
- 우측: 오늘 배울 3개 키워드 카드
- 상단에 작은 배지: `Week 02`, `Blender Basics`

### 8.2 섹션 오프너 슬라이드

- 중앙 정렬
- 큰 한 줄 메시지
- 상단에 작은 단계 라벨
- 하단에 1줄 보조 설명

예시:

- `블렌더 화면을 읽으면 작업이 쉬워집니다`
- `기본 조작만 익혀도 형태를 만들 수 있습니다`
- `Extrude와 Bevel이 기초 모델링의 시작입니다`

### 8.3 오늘 배울 것

- 3개 카드
- 각 카드 구성: 번호, 제목, 1문장 설명
- 카드 배경은 `Surface 1`, 보더는 얇게

### 8.4 개념 흐름도

- 가로형 4단계 또는 세로형 5단계
- 예시:
  - 설치
  - 인터페이스 이해
  - 오브젝트 조작
  - 기본 모델링

### 8.5 화면 캡처 설명

- 좌측: Blender UI 스크린샷
- 우측: 콜아웃 카드 3개
- 하이라이트 색상은 모두 Key 컬러 계열만 사용

### 8.6 실습 순서

- 세로 타임라인
- 각 스텝마다:
  - Step 번호
  - 해야 할 행동
  - 자주 하는 실수

### 8.7 과제 섹션

- 제출물
- 마감
- 체크리스트
- 참고 링크

이 섹션은 [docs/NOTION_REBUILD_BLUEPRINT_2026-03-07.md](/Users/ssongji/Developer/Workspace/RPD/docs/NOTION_REBUILD_BLUEPRINT_2026-03-07.md#L208)의 `이번 주 수업 / 이번 주 과제 / 주차별 강의자료` 구조와 자연스럽게 연결된다.

---

## 9. 중앙 정렬 한 줄 슬라이드용 컬러/폰트 적용 규칙

### 9.1 제목 스타일

- 폰트: `Paperlogy 8ExtraBold`
- 색상: `#F8FAFC`
- 자간: 아주 약간 좁게
- 중앙 정렬
- 한 줄 최대 14자~20자 권장

### 9.2 단계 라벨

- 폰트: `SUIT SemiBold`
- 색상: `#93C5FD`
- 크기: 작게
- 제목 위에 배치

### 9.3 강조 아이콘

- 테두리/아이콘: `#3B82F6`
- 내부 glow는 약하게
- 배경은 투명 또는 아주 진한 남색 원

### 9.4 배경

- 완전한 순수 블랙 하나만 쓰지 말고 아래 중 하나로 운용
- `#06080D`
- `#08101A`
- `#0B1220`

### 9.5 보조 문장

- 폰트: `SUIT Medium`
- 색상: `#94A3B8`
- 제목보다 1~2단 낮은 톤

---

## 10. 인포그래픽 컴포넌트 규칙

### 10.1 제목

- H1은 크고 짧게
- H2는 섹션 요약 중심
- 한 제목에 핵심 메시지는 12자~24자 정도로 유지

### 10.2 카드

- radius: 18~24px
- 내부 여백: 넉넉하게
- 진한 배경 + 얇은 보더
- glow는 약하게만 사용

### 10.3 번호 배지

- 꽉 찬 원보다 `얇은 라인 원 + 숫자` 추천
- 너무 레퍼런스처럼 보이면 `둥근 사각 배지`로 바꿔도 좋다

### 10.4 아이콘

- 2px 선 굵기
- 단순 도형 위주
- 색상은 흰색 또는 Key 컬러만 사용

### 10.5 콜아웃

- 한 카드에 2문장 이하
- 중요 단어만 Key 컬러
- 긴 설명은 리스트로 자른다

---

## 11. 강의 페이지 생성 프롬프트 초안

아래 프롬프트를 디자인 생성용 가이드로 그대로 써도 된다.

```text
Create a clean infographic-style lecture page for a Blender class.

Visual direction:
- dark editorial background
- one custom key color: RPD Signal Blue (#3B82F6)
- bold Korean headings
- thin line icons
- minimal but information-dense layout
- not a clone of neon-green viral lecture slides
- cleaner, more structured, more academic, more infographic-driven

Layout:
- hero section with week label, title, and 3 learning goals
- concept flow section with 4 steps
- annotated UI screenshot section
- key tools section with numbered cards
- practice workflow section with vertical timeline
- assignment and checklist section
- reference links footer

Style rules:
- use black and deep navy surfaces instead of flat pure black everywhere
- keep whitespace generous
- use thin borders and tinted panels
- use the key color only for emphasis, icons, labels, and active lines
- avoid heavy gradients, avoid multiple accent colors, avoid neon green
- feel precise, calm, and premium
```

---

## 12. 노션 페이지로 옮길 때의 적용법

노션에서는 완전한 자유 레이아웃이 어렵기 때문에, 아래처럼 블록 단위로 번역하면 된다.

1. `콜아웃 블록`을 Hero 요약에 사용한다.
2. `3열 컬럼`으로 오늘의 목표 카드 3개를 만든다.
3. `토글`로 세부 설명을 숨겨 페이지를 짧게 유지한다.
4. `갤러리 뷰`는 주차 카드 목록에만 사용한다.
5. 긴 설명은 문단보다 `불릿 + 번호 목록 + 콜아웃`으로 끊는다.
6. 스크린샷 설명은 이미지 아래에 `번호 콜아웃 3개`를 둔다.

---

## 13. 샘플 구성안: Week 02

현재 정리된 [Blender_2026/week_02/video_notes.md](/Users/ssongji/Developer/Workspace/RPD/Blender_2026/week_02/video_notes.md)를 기준으로 강의 페이지를 구성하면 아래처럼 잡을 수 있다.

```text
Week 02
Blender 인터페이스와 기초 모델링

이번 주 한 줄 요약
Blender 화면을 읽고, 오브젝트를 조작하고, 기본 모델링 도구를 익힙니다.

[오늘 배울 것]
1. 인터페이스 구조 이해
2. 오브젝트 기본 조작
3. Extrude / Bevel / Loop Cut 익히기

[개념 흐름도]
설치 & 시작 → 인터페이스 → 기본 조작 → 모델링 도구 → 실습 적용

[핵심 도구]
- Viewport
- Outliner
- Properties
- G / R / S
- Tab / 1 / 2 / 3
- E / I / Ctrl+B / Ctrl+R

[실습 순서]
1. Blender를 열고 기본 화면 이해하기
2. 오브젝트 추가 후 이동/회전/스케일 해보기
3. Edit Mode 전환 후 면 선택하기
4. Extrude와 Inset으로 형태 만들기
5. Bevel과 Loop Cut으로 디테일 추가하기

[과제]
- 간단한 로우폴리 소품 1개 만들기
- 필수 사용 도구: G, R, S, Extrude, Bevel
- 제출물: 이미지 2장 + 작업 파일
```

이 샘플은 `슬라이드식 문장 나열`보다 `학습 목표 + 개념 흐름 + 실습 순서 + 과제`를 먼저 보이게 만드는 데 목적이 있다.

---

## 14. 바로 적용할 수 있는 운영 규칙

1. 한 페이지당 메인 컬러는 1개만 쓴다.
2. 섹션당 핵심 메시지는 1개, 보조 포인트는 최대 3개까지만 둔다.
3. 스크린샷은 반드시 `설명 없는 단독 이미지`로 두지 말고 콜아웃을 붙인다.
4. 과제 정보는 항상 카드 또는 체크리스트로 끝나게 만든다.
5. 강의 소개 페이지와 주차 페이지는 동일한 색 체계를 공유한다.

---

## 15. 추천 결론

가장 좋은 방향은 아래다.

1. 레퍼런스의 `검은 배경 + 강한 타이포 + 단일 포인트 컬러`는 유지한다.
2. 포인트 컬러는 `RPD Signal Blue`로 교체한다.
3. 한 줄 메시지 슬라이드 느낌은 줄이고, `카드형 인포그래픽 페이지` 비중을 늘린다.
4. 학생이 실제로 써야 하는 정보는 `이번 주 목표`, `실습 순서`, `과제`, `참고 링크` 기준으로 구조화한다.

이 방식이면 레퍼런스의 시선집중력은 유지하면서도, 훨씬 더 `내 강의 브랜드`처럼 보이는 페이지를 만들 수 있다.
