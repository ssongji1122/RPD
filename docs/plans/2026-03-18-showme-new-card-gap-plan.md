# ShowMe 신규 카드 보강 계획
Date: 2026-03-18

## 목적
기존 ShowMe 카드의 시각화 업그레이드와 별개로, 실제 Blender 수업 흐름에서 자주 막히지만 아직 독립 카드가 없는 핵심 주제를 신규 카드로 편성한다.

이 문서는 `docs/plans/2026-03-18-showme-bulk-upgrade-design.md`의 보완 문서다. 기존 문서는 이미 존재하는 61개 카드의 연결과 업그레이드에 집중하고 있고, 이 문서는 "아직 없는 카드"를 새로 정의하는 백로그를 다룬다.

## 왜 지금 필요한가
- 현재 라이브러리는 카드 수 자체는 많지만, 수업에서 자주 쓰는 몇몇 연결 개념이 독립 카드로 비어 있다.
- `course-site/data/curriculum.js`에는 이미 `Collection` 스텝이 존재하지만 ShowMe 카드가 없다.
- `Modifier Stack 정리` 스텝은 `transform-apply`만 연결되어 있어, 실제로 더 많이 헷갈리는 "순서"와 "Apply 타이밍"이 약하다.
- `Weighted Normal`과 `Subdivision` 설명은 이미 있지만, 그 전제인 `Shade Smooth / Auto Smooth`, `Merge by Distance`, `Face Orientation` 같은 정리 개념은 독립 카드가 없다.
- 강의 노트에는 `Bridge Edge Loops`, `Collection`, `Outliner`, `Merge by Distance`가 반복 등장하는데 라이브러리 차원에서 바로 열어볼 카드가 없다.

## 선정 기준
새 카드는 아래 조건을 3개 이상 만족할 때 우선 제작한다.

1. 초보자가 실제로 자주 막힌다.
2. 두 개 이상의 주차 또는 단계에서 재사용된다.
3. 기존 카드의 선행 개념이거나 후속 개념을 매끄럽게 이어 준다.
4. Blender Manual 또는 강의 노트에 명시적으로 등장한다.
5. 기존 카드 내부의 일부 설명이 아니라 독립된 상호작용 데모로 보여줄 가치가 있다.

## 새로 만들지 않아도 되는 주제
아래는 중요하지만, 지금은 신규 카드보다 기존 카드의 범위 안에서 충분히 커버된다고 본다.

- `Vertex / Edge / Face 선택 모드`
  이미 `edit-mode`와 `edit-mode-tools`가 1/2/3 선택 모드와 루프 선택을 다루고 있다.
- `3D Cursor 기본 개념`
  이미 `origin-vs-3dcursor`와 `pivot-point`가 핵심 혼란을 충분히 커버한다.
- `Support Loop / Edge Crease`
  이미 `subdivision-surface`가 두 방법의 차이를 설명한다.
- `Reference 이미지 잠금`
  이미 `image-reference` 안에서 Outliner 잠금과 Opacity 조절을 다룬다.

## Priority 0 — 흐름상 반드시 추가

### 1. `collection-outliner`
- 제목: `Collection & Outliner 이해`
- 필요한 이유:
  Week 3의 `Collection` 스텝이 현재 ShowMe 없이 텍스트만 있다.
  레퍼런스 이미지 잠금, 가시성 제어, 파츠 정리 같은 실무 습관과 직접 연결된다.
- 배치 위치:
  Week 3 `Collection` 스텝 메인 ShowMe
  Week 2 UI 소개의 보조 위젯으로도 재사용 가능
- 핵심 interaction:
  좌측은 뷰포트, 우측은 Outliner 트리
  오브젝트를 Collection 사이로 이동
  `눈`, `선택 잠금`, `이름 그룹` 토글 비교
- 학습 질문:
  "왜 레퍼런스가 자꾸 잡히지?"
  "왜 어떤 건 숨겼는데 전체가 같이 사라지지?"

### 2. `modifier-stack-order`
- 제목: `Modifier Stack 순서와 Apply`
- 필요한 이유:
  `transform-apply`는 변환값 정리에는 좋지만, Modifier 자체의 순서 문제를 설명하지는 못한다.
  Week 3, Week 4, 하드서피스 정리 과정을 모두 잇는 핵심 카드다.
- 배치 위치:
  Week 3 `Modifier Stack 정리` 스텝 메인 ShowMe
  Week 4 `Bevel Modifier`, `Weighted Normal` 보조 위젯
- 핵심 interaction:
  `Mirror`, `Subdivision`, `Bevel`, `Weighted Normal` 순서를 버튼으로 재배열
  순서별 결과 차이를 즉시 비교
  `Apply` 전/후 editable 여부를 상태 카드로 표시
- 학습 질문:
  "같은 Modifier인데 왜 순서만 바꿨는데 결과가 달라지지?"
  "언제 Apply하고 언제 남겨둬야 하지?"

### 3. `shade-smooth-auto-smooth`
- 제목: `Shade Smooth & Auto Smooth 이해`
- 필요한 이유:
  `Weighted Normal` 카드의 선행 개념인데 현재는 카드 안의 일부 문장으로만 소비된다.
  학생 입장에서는 "형태가 바뀐 것"과 "빛이 부드러워진 것"을 자주 혼동한다.
- 배치 위치:
  Week 3 `Weighted Normal`
  Week 4 하드서피스 정리
  Rendering 입문 전 셰이딩 감각 보강용
- 핵심 interaction:
  같은 메시에 대해 `Flat`, `Shade Smooth`, `Auto Smooth by Angle` 전환
  각도 슬라이더로 hard edge 유지 범위 비교
- 학습 질문:
  "Subdivision이 된 건지, Shade Smooth만 된 건지 모르겠어요."
  "왜 모서리는 살리고 면만 부드럽게 못 하지?"

### 4. `merge-by-distance`
- 제목: `Merge by Distance & Mesh Cleanup`
- 필요한 이유:
  강의 노트에서 `Extrude 후 ESC`, Boolean 실패, Loose Parts 정리의 대표 해결책으로 반복 등장한다.
  현재는 `join-separate` 안에서 일부 언급만 있고, 독립적으로 배우기 어렵다.
- 배치 위치:
  Week 3 `기본형 만들기`의 실수 복구 보조 위젯
  Week 3 `Boolean`과 `Join/Separate`의 후속 정리 카드
- 핵심 interaction:
  겹친 버텍스가 있는 메시 예시
  거리 슬라이더를 올리면 중복 점이 합쳐지고 카운트 감소
  너무 높은 값일 때 형태가 망가지는 경고도 함께 표시
- 학습 질문:
  "겉으로 멀쩡한데 왜 Boolean이 깨지지?"
  "Extrude 취소했는데 뭔가 이상해졌어요."

### 5. `bridge-edge-loops`
- 제목: `Bridge Edge Loops 이해`
- 필요한 이유:
  강의 노트에 명시적으로 등장하는데 라이브러리에 독립 카드가 없다.
  Join/Separate와 이어지는 토폴로지 연결 개념으로 교육 가치가 높다.
- 배치 위치:
  Week 2 또는 Week 3의 `Join / Separate` 보조 위젯
  향후 하드서피스 구멍 메우기, 관 연결 예제에도 재사용 가능
- 핵심 interaction:
  두 개의 열린 edge loop 선택
  `Bridge` 적용 전/후를 비교
  loop 개수 불일치 시 실패하는 예시 포함
- 학습 질문:
  "구멍 둘을 깔끔하게 연결하려면 왜 F가 아니라 Bridge를 써야 하지?"
  "왜 어떤 루프는 Bridge가 되고 어떤 건 안 되지?"

## Priority 1 — 흐름을 더 매끄럽게 만드는 카드

### 6. `duplicate-vs-linked-duplicate`
- 제목: `Duplicate vs Linked Duplicate`
- 필요한 이유:
  반복 파츠 제작, Array 이전 개념, 인스턴싱 감각을 가르치기에 좋다.
  `Shift + D`와 `Alt + D`는 수업에서 설명할 때 체감 차이가 커서 독립 카드 가치가 있다.
- 배치 위치:
  Week 3 `Array`
  추후 환경 배치, 반복 파츠 제작
- 핵심 interaction:
  원본을 수정했을 때 일반 복제는 독립, linked duplicate는 함께 변함

### 7. `face-orientation-normals`
- 제목: `Face Orientation & Normal Recalculate`
- 필요한 이유:
  Solidify, Boolean, 렌더링 문제를 설명할 때 계속 돌아오게 되는 핵심 점검 카드다.
  현재 `weighted-normal`은 셰이딩 쪽 법선을 다루지만, 면의 앞뒤 방향은 따로 보여주지 않는다.
- 배치 위치:
  Week 3 `Solidify`, `Boolean`
  Week 6 재질/렌더링 전 점검 카드
- 핵심 interaction:
  앞면/뒷면 색상 오버레이
  `Recalculate Outside`, `Flip` 비교

### 8. `apply-modifier-vs-keep-procedural`
- 제목: `Apply Modifier vs Keep Live`
- 필요한 이유:
  `Ctrl + A`의 Transform Apply와 Modifier Apply를 초보자가 자주 혼동한다.
  비파괴 워크플로우 감각을 독립 카드로 한 번 정리해 두면 이후 수업이 훨씬 편해진다.
- 배치 위치:
  Week 3 `Modifier Stack 정리`
  Week 4 `Join / Separate / Triangulate / Weld` 주변
- 핵심 interaction:
  같은 오브젝트에 live modifier 상태와 applied 상태를 비교
  수치 재조정 가능 여부를 시각적으로 차등 표시

## Priority 2 — 이후 확장 후보

### 9. `parenting-basics`
- 제목: `Parent 관계와 계층`
- 필요 시점:
  애니메이션, 카메라, 리깅 이전 단계에서 계층 구조를 설명할 때

### 10. `knife-bisect`
- 제목: `Knife / Bisect 컷 이해`
- 필요 시점:
  하드서피스 디테일링이 더 깊어질 때

### 11. `selection-patterns`
- 제목: `Loop / Ring / Box / Lasso 선택`
- 필요 시점:
  편집 도구는 익혔지만 선택 효율이 낮아서 막히는 학생이 늘어날 때

## 제작 순서 제안

### Phase A — 수업 병목 먼저 해소
1. `collection-outliner`
2. `modifier-stack-order`
3. `shade-smooth-auto-smooth`

### Phase B — 모델링 정리 흐름 보강
4. `merge-by-distance`
5. `bridge-edge-loops`

### Phase C — 비파괴 워크플로우 확장
6. `duplicate-vs-linked-duplicate`
7. `face-orientation-normals`
8. `apply-modifier-vs-keep-procedural`

## 구현 원칙
- 신규 카드는 기존 ShowMe 4탭 구조를 유지한다.
- interaction 탭은 "학생이 실제로 틀리는 선택"을 직접 바꿔보게 만든다.
- 개념 설명보다 "왜 지금 이 카드가 필요한지"를 먼저 보여준다.
- 하나의 카드가 기존 카드와 겹치더라도, 선행/후행 관계가 명확하면 독립 카드로 분리한다.
- 반대로 기존 카드 안에서 충분히 소화되는 내용은 억지로 쪼개지 않는다.

## 파일 영향 범위
- 신규 카드 HTML:
  `course-site/assets/showme/<new-id>.html`
- 카드 등록:
  `course-site/assets/showme/_registry.js`
- 라이브러리 분류:
  `course-site/assets/showme/_catalog.json`
  `course-site/assets/i18n.js`
- 주차 연결:
  `course-site/data/curriculum.js`
- 테스트:
  `tools/tests/test_showme_widget_e2e.py`

## 테스트 기준
- 신규 카드마다 최소 1개의 상호작용 E2E를 추가한다.
- 가능한 경우 대표 렌더 상태를 픽셀 샘플 또는 상태 텍스트로 함께 검증한다.
- 수치 입력이 있는 카드는 slider와 number input 동기화를 공통 기준으로 삼는다.

## 완료 기준
- Priority 0 카드 5개가 라이브러리와 커리큘럼에 연결되어 있다.
- Week 3 `Collection`, `Modifier Stack`, Week 4 셰이딩 정리 흐름에 비어 있는 ShowMe가 없다.
- 학생이 자주 묻는 "왜 결과가 다르지?" 질문을 텍스트가 아니라 interaction으로 보여줄 수 있다.
