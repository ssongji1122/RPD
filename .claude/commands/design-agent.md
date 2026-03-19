---
description: "인지부하 기반 UI 단순화와 페이지 리디자인. 예: /design-agent audit library, /design-agent simplify library, /design-agent apply week"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(node:*), Bash(ls:*), Bash(wc:*), Bash(curl:*), Agent
---

## Context

- 프로젝트 루트: !`git rev-parse --show-toplevel 2>/dev/null`
- 주요 페이지: !`ls course-site/*.html 2>/dev/null | xargs -I{} basename {} | tr '\n' ' '`
- ShowMe 카드 수: !`ls course-site/assets/showme/*.html 2>/dev/null | grep -v _template | wc -l | tr -d ' '`개
- 스타일 가이드: !`ls docs/COURSE_SITE_STYLE_GUIDE_2026-03-13.md docs/COGNITIVE_UI_GUIDE_2026-03-18.md 2>/dev/null | tr '\n' ' '`

## Task

인자: `$ARGUMENTS`

---

## 최신 근거 수집 규칙

사용자가 `최신`, `current`, `2026`, `근거`, `검증`, `공신력`을 언급하면 수정 전에 먼저 웹에서 확인한다.

출처 우선순위:
1. **W3C / WAI / WCAG**
2. **정부 디자인 시스템·매뉴얼**
   - GOV.UK Service Manual
   - U.S. Web Design System (USWDS)
   - Department for Education Accessibility Manual
3. **플랫폼 공식 가이드**
   - Apple Human Interface Guidelines
   - Material Design
   - Microsoft Fluent
4. **동료심사 HCI / Human Factors 연구**
5. 블로그·에이전시 글은 보조 참고만 허용

2026-03-18 기준 직접 확인한 현재 출처:
- W3C Cognitive Accessibility at W3C — 2024-04-25 업데이트
- W3C Content Usable / Clear Content / WCAG 2.2 Consistent Help
- W3C Cognitive Accessibility Research Modules: Voice Systems and Conversational Interfaces — 2026-02-05 공개 버전
- GOV.UK Service Manual — Writing for user interfaces
- GOV.UK Service Manual — Designing how content and transactions work together
- USWDS Design principles / Accessibility / Progress easily
- DfE Accessibility Manual — COGA guidelines

## 모드 분기

### `audit {target}` — 정보 과밀도 감사

지정한 페이지나 컴포넌트의 인지부하를 점검한다.

반드시 아래를 본다:
- 반복 카드에 한 번에 몇 개의 정보 축이 노출되는지
- 제목, 검색, 필터, 상태 배지 중 무엇이 첫 시선 경로를 끊는지
- 클릭 전에 꼭 필요한 정보와 클릭 후로 미뤄도 되는 정보가 섞여 있는지
- 모바일에서 한 화면에 보이는 선택지가 과도하게 시끄럽지 않은지
- 도움말, 탐색, 닫기 위치가 페이지 간 일관된지
- 정보가 한 번에 너무 큰 덩어리로 제시되지 않는지

출력은 아래 우선순위를 따른다:
1. 학생이 바로 헷갈리는 문제
2. 시선 분산을 만드는 문제
3. 일관성/접근성 문제

### `simplify {target}` — 저잡음 리디자인 적용

대상 페이지를 실제로 수정한다.

핵심 원칙:
1. **한 카드 = 한 결정**
   - 반복 카드가 12개 이상 보이면 기본 상태에서는 `주 이름/도구 이름`만 노출한다.
   - 카테고리, 난이도, 슬러그, 혼동 포인트는 검색 인덱스, 필터, 모달, 상세 페이지로 이동한다.
2. **검색 전 스캔 가능**
   - 사용자는 먼저 훑어보고, 그 다음 검색한다.
   - 카드 첫 줄은 가장 중요한 명사/동사만 남긴다.
3. **점진적 공개**
   - 첫 화면에서는 고르기 위한 정보만 보여준다.
   - 설명은 클릭 후, hover, accordion, modal, secondary panel로 미룬다.
4. **한 페이지 한 강조**
   - 같은 화면에서 강조 색의 역할은 하나만 둔다.
   - 배지는 정말 분류를 빨리 하는 데 필요할 때만 남긴다.
5. **일관된 예측 가능성**
   - 버튼 위치, 닫기 방식, 필터 구조, 제목 위계는 페이지 간 동일하게 유지한다.

### `apply {target}` — 감사 + 수정 + 검증

1. `audit` 수행
2. 가장 큰 인지부하 원인 1~3개 제거
3. 모바일/키보드/빈 검색 결과 상태 확인
4. 바뀐 이유를 `docs/COGNITIVE_UI_GUIDE_2026-03-18.md` 기준으로 짧게 기록

### `compact library` — 라이브러리 전용 규칙

`course-site/library.html`에는 아래를 기본으로 적용한다:
- 카드에는 이름만 노출
- 검색창과 카테고리 필터는 유지
- 상세 정보는 모달 안 ShowMe 카드에서만 제공
- 카드 정렬은 스캔하기 쉬운 단순 패턴 우선

---

## 연구 기반 판단 규칙

### 1. Extraneous load 제거

- 반복적으로 보이는 장식/메타 정보는 학습에 도움이 되지 않으면 제거한다.
- 같은 정보를 여러 형태(칩, 보조문장, slug)로 중복 노출하지 않는다.
- W3C COGA의 `Support Simplification`처럼 필수 아닌 기능과 텍스트는 숨기거나 뒤로 미룬다.

### 2. Choice complexity 관리

- 선택지가 많을수록 반응 시간이 늘 수 있으므로, 한 번에 비교할 차원을 줄인다.
- 많은 카드는 `이름`, `필터`, `검색` 중심으로 설계한다.
- GOV.UK처럼 복잡한 조건은 긴 안내문보다 `간단한 질문 흐름`으로 바꿀 수 있는지 먼저 본다.

### 3. Visual complexity 관리

- 시각적 복잡도는 검색 속도와 기억 성능을 떨어뜨릴 수 있으므로, 카드 내부 요소 수를 줄인다.
- 그림, 배지, 보조 텍스트는 "찾기 속도"를 올릴 때만 남긴다.
- DfE COGA처럼 cluttered layout를 피하고, 중요 정보에만 시각적 위계를 쓴다.

### 4. Focus-first 흐름

- 사용자가 읽지 않고 훑어본다는 가정으로 설계한다.
- 제목/카드/버튼은 앞 단어만 봐도 의미가 드러나야 한다.
- GOV.UK처럼 중요한 단어를 앞에 두고, 설명보다 라벨을 먼저 정리한다.

### 5. Cognitive accessibility

- 일관된 위치, 예측 가능한 인터랙션, 짧은 문장, 작은 덩어리 구조를 유지한다.
- mid-task 방해 요소(과한 motion, 의미 없는 배지, 부가 설명 과다)를 피한다.
- WCAG 2.2 `Consistent Help`처럼 도움말과 지원 경로는 페이지마다 찾기 쉬운 같은 위치에 둔다.
- USWDS `Progress easily`처럼 micro-topic 단위로 쪼개고 step-by-step 흐름을 우선한다.

---

## 검증 체크리스트

수정 후 반드시 확인:
- [ ] 첫 화면 3초 안에 "여기서 뭘 할 수 있는지" 보이는지
- [ ] 카드 하나에 기본 정보가 1개 축만 남았는지
- [ ] 검색 없이도 5~10개 항목을 빠르게 훑을 수 있는지
- [ ] 모바일에서 터치 타겟이 44px 근처인지
- [ ] 키보드 focus가 보이는지
- [ ] 빈 결과 / 긴 이름 / 다국어 상태가 깨지지 않는지

---

## 참조 파일

| 파일 | 역할 |
|------|------|
| `docs/COGNITIVE_UI_GUIDE_2026-03-18.md` | 인지부하 기반 설계 근거 |
| `docs/COURSE_SITE_STYLE_GUIDE_2026-03-13.md` | RPD 시각 언어 기준 |
| `.claude/skills/rpd-site-improve/SKILL.md` | 사이트 수정 제약 |
| `.claude/skills/rpd-a11y-audit/SKILL.md` | 접근성 점검 기준 |
| `course-site/library.html` | 라이브러리 브라우징 페이지 |
| `course-site/week.html` | 주차 상세 페이지 |

## Gotchas ⚠️
> Claude가 이 스킬을 쓸 때 실수했던 것들. 새 함정 발견 시 여기에 추가.

1. (아직 없음 — 사용하면서 추가)
