# Cognitive UI Guide

작성일: 2026-03-18  
대상: `/Users/ssongji/Developer/Workspace/RPD`

## 1. 목표

RPD 페이지를 `보기 예쁜 화면`보다 `빨리 찾고, 덜 헷갈리고, 바로 행동하게 하는 화면`으로 정리한다.

핵심 질문은 하나다.

`이 정보가 지금 이 순간, 첫 선택에 꼭 필요한가?`

필요 없으면 첫 화면에서 뺀다.

---

## 2. 핵심 원칙

### 2.1 Extraneous Load 먼저 줄이기

- 작업에 직접 도움이 되지 않는 반복 메타 정보는 줄인다.
- 같은 뜻을 칩, 보조문장, slug로 반복하지 않는다.
- 학생이 클릭 전에 결정해야 하는 정보만 남긴다.

### 2.2 Dense Surface는 이름 우선

- 카드가 많이 반복되는 화면에서는 기본적으로 `이름`만 노출한다.
- 카테고리, 난이도, 혼동 포인트, 선수 지식은 필터/검색/상세 모달로 이동한다.
- 특히 라이브러리, DB, 카드 그리드, 레퍼런스 목록에서 이 규칙을 강하게 적용한다.

### 2.3 Scan First

- 사용자는 읽기 전에 훑는다.
- 제목과 카드 라벨은 앞 단어만 봐도 의미가 보여야 한다.
- 긴 설명보다 짧은 라벨, 명확한 그룹, 일정한 정렬을 우선한다.

### 2.4 Progressive Disclosure

- 첫 화면: 선택에 필요한 정보
- 클릭 후: 설명, 예시, 비교, 팁
- 마지막 단계: 심화 자료, 공식 문서, 보충 설명

### 2.5 Choice Complexity 줄이기

- 선택지가 많은 화면에서 비교 축까지 많으면 판단 속도가 떨어진다.
- 한 화면에서 비교 차원은 1개만 앞에 둔다.
- 나머지는 필터, 정렬, 토글, 상세 보기로 분리한다.

### 2.6 Focus 유지

- mid-task 시선 분산 요소를 줄인다.
- 과한 배지, 장식용 아이콘, 자동 재생, 설명 과다, 여러 강조색을 피한다.
- 학생이 잠깐 딴생각해도 다시 돌아올 수 있게 구조를 단순하게 유지한다.

### 2.7 Predictable UI

- 같은 의미의 요소는 항상 같은 위치와 스타일로 둔다.
- 닫기 버튼, 검색, 필터, 섹션 제목 위계가 페이지마다 달라지지 않게 한다.

---

## 3. RPD 적용 규칙

### 3.1 라이브러리 / 브라우징 화면

- 반복 카드가 12개 이상이면 카드에는 이름만 둔다.
- 검색과 카테고리 필터는 남긴다.
- 메타 정보는 `dataset`, tooltip, modal, 상세 패널로 이동한다.
- 시각적 노이즈를 줄이기 위해 카드 내부 세로 층 수를 최소화한다.

### 3.2 주차 페이지

- 각 섹션은 "이번에 해야 할 한 가지" 중심으로 구성한다.
- Hero 아래에는 요약보다 행동 진입점이 먼저 와야 한다.
- 실습 카드에는 `무엇`, `왜`, `완료 기준`만 먼저 보이게 한다.

### 3.3 ShowMe / 보충 설명

- 기본 카드 본문은 핵심 개념과 인터랙션에 집중한다.
- 보충 설명은 항상 2차 레이어로 둔다.
- 이해를 돕는 시각화는 좋지만, 비교용 장식이 본문보다 앞서면 안 된다.

### 3.4 카피

- 한 문장 한 생각
- 앞 단어에 핵심 명사/동사
- 전문용어는 유지하되 불필요한 수식은 제거

---

## 4. 빠른 휴리스틱

출시 전 아래 5개를 본다.

1. 3초 안에 페이지 용도가 보이는가  
2. 카드 하나에 한 결정만 남아 있는가  
3. 스캔만으로도 다음 클릭을 정할 수 있는가  
4. 검색 없이도 구조가 이해되는가  
5. 모바일에서도 같은 위계가 유지되는가

---

## 5. 연구 근거

2026-03-18 기준으로 직접 확인한 **현재 공식 가이드**와 **기초 HCI 연구**를 같이 사용한다.

### 5.1 현재 공식 가이드

1. W3C WAI, *Cognitive Accessibility at W3C*  
   - 2024-04-25 업데이트된 현재 안내 페이지다. 인지 접근성 판단에는 `Content Usable`, 설계 패턴, 사용자 참여 테스트를 함께 보라고 안내한다.  
   - 링크: https://www.w3.org/WAI/cognitive/

2. W3C, *Making Content Usable for People with Cognitive and Learning Disabilities*  
   - `Support Simplification` 패턴에서 비필수 기능 숨기기, 더 적은/더 쉬운 텍스트 제공, 필요할 때만 추가 기능 찾게 하기 를 직접 권장한다.  
   - 링크: https://www.w3.org/TR/coga-usable/

3. W3C WAI, *Use Clear and Understandable Content*  
   - 짧은 문장, 짧은 텍스트 블록, 쉬운 단어, 좋은 시각적 레이아웃, 충분한 여백이 이해를 돕는다고 정리한다.  
   - 링크: https://www.w3.org/WAI/WCAG2/supplemental/objectives/o3-clear-content/

4. W3C WAI, *Understanding WCAG 2.2 — Consistent Help*  
   - 도움말이 있을 때는 사용자가 “hunt for it” 하지 않도록 일관된 위치와 단일한 자기 도움 경로를 두는 것이 인지 장애 사용자에게 특히 중요하다고 설명한다.  
   - 링크: https://www.w3.org/WAI/WCAG22/Understanding/consistent-help.html

5. GOV.UK Service Manual, *Writing for user interfaces*  
   - 사람들은 읽기보다 스캔하는 경향이 있으므로 `start with less`, `keep copy short and direct`, `put the important words first`를 권장한다.  
   - 링크: https://www.gov.uk/service-manual/design/writing-for-user-interfaces

6. GOV.UK Service Manual, *Designing how GOV.UK content and transactions work together*  
   - 복잡한 자격 조건을 긴 설명으로 먼저 보여주기보다, 트랜잭션 안에서 간단한 질문으로 라우팅하면 cognitive load를 줄일 수 있다고 설명한다.  
   - 링크: https://www.gov.uk/service-manual/design/govuk-content-transactions

7. U.S. Web Design System, *Progress easily*  
   - 복잡한 흐름은 cognitive load를 줄이기 위해 progressive disclosure, 작은 의미 단위, one micro-topic at a time, 단계 표시를 쓰라고 권장한다.  
   - 링크: https://designsystem.digital.gov/patterns/complete-a-complex-form/progress-easily/

8. U.S. Web Design System, *Design principles* / *Accessibility*  
   - 연속성 있는 일관된 경험을 강조하고, 2025년 3월에 44개 컴포넌트를 평가해 2025년 5월 ACR을 공개했다.  
   - 링크: https://designsystem.digital.gov/design-principles/  
   - 링크: https://designsystem.digital.gov/documentation/accessibility/

9. Department for Education Accessibility Manual, *COGA guidelines*  
   - 명확한 레이아웃, 작은 관리 가능한 섹션, 짧은 문장, 명확한 선택지, cluttered layout 회피, one thing per page를 구체적으로 권장한다.  
   - 링크: https://accessibility.education.gov.uk/guidelines/coga

10. W3C, *Cognitive Accessibility Research Modules — Voice Systems and Conversational Interfaces*  
   - 2026-02-05 공개 버전. 현재 W3C 인지 접근성 작업이 2026에도 계속 갱신되고 있음을 보여주는 최신 공개 노트다. 앞으로 챗봇·음성 인터랙션을 붙일 때 참고한다.  
   - 링크: https://www.w3.org/TR/coga-voice/

### 5.2 기초 HCI 연구

1. John Sweller, *Cognitive load during problem solving: Effects on learning* (1988)  
   - 문제 해결 자체가 처리 용량을 많이 쓰면 학습에 쓸 자원이 줄 수 있다는 점을 보여준다. 화면 설계에서는 불필요한 해석 작업을 줄이는 근거가 된다.  
   - 링크: https://iiif.library.cmu.edu/file/Simon_box00032_fld02400_bdl0001_doc0001/Simon_box00032_fld02400_bdl0001_doc0001.pdf

2. Oulasvirta et al., *Human-Computer Interaction: Foundations and New Paradigms* — Hick–Hyman law section  
   - 선택지가 늘수록 반응 시간이 늘고, 실제 인터페이스에서는 계층화와 시각 탐색 비용도 함께 고려해야 함을 설명한다.  
   - 링크: https://academic.oup.com/book/60808/chapter/528999086

3. Tuch et al., *Visual complexity of websites: Effects on users’ experience, physiology, performance, and memory* (2009)  
   - 시각적 복잡성이 높아질수록 반응 시간은 늘고 기억 성능은 낮아질 수 있음을 보였다. 반복 카드 화면의 요소 수를 줄이는 직접 근거로 쓴다.  
   - 링크: https://www.sciencedirect.com/science/article/pii/S107158190900055X

---

## 6. 실무 결론

RPD에서 가장 먼저 줄여야 하는 것은 `정보 수`보다 `한 번에 보이는 판단 축의 수`다.

즉:
- 카드가 많으면 이름만 보여준다
- 설명은 클릭 후로 미룬다
- 강조는 하나만 남긴다
- 구조는 페이지마다 같게 유지한다
