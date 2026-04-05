# Week 3 기획 심화 (Design Doc)

> **목적:** curriculum.js의 콘텐츠가 아닌, 수업 기획 자체의 질을 검증하기 위한 문서.
> Content Lead + CPO가 Rubric 기반으로 주차별 기획을 심층 리뷰할 때 사용한다.

**주제:** 기초 모델링 1 — Edit Mode + Modifier
**수업일:** 2026-03-18 (화) 예정
**강의실:** 인하대학교 (60주년관)
**Duration:** ~3시간
**Status:** done
**리뷰 완료일:** 2026-04-05

---

## 1. Student Journey (학생 여정)

### 시작 상태 (Week 2 종료 시점)
- Blender 설치 완료, 뷰포트 조작 가능
- G/R/S + 축 제한 이해, Apply Transform 개념 습득
- 기본 도형 배치 경험 있으나 Edit Mode 진입 경험 없음

### 끝 상태 (Week 3 종료 시점)
- [ ] Tab으로 Object/Edit Mode 자유 전환 가능
- [ ] Extrude, Loop Cut, Inset, Bevel 4가지 도구 사용 가능
- [ ] Mirror, Subdivision Surface, Solidify, Array, Boolean Modifier 사용 가능
- [ ] Bevel Modifier + Weighted Normal 조합으로 음영 정리 가능
- [ ] Ctrl+A vs Modifier Apply 시점 구분 가능
- [ ] Join(Ctrl+J) / Separate(P)로 파츠 관리 가능
- [ ] 로봇/캐릭터 기본형(머리+몸통 수준) 완성
- [ ] Discord #week03-assignment 제출 완료 (스크린샷 3장 + Modifier 목록 + 한줄)

### 핵심 전환점 ("아하!" 모먼트)
1. **Mirror Modifier를 켰을 때 한쪽만 작업해도 반대쪽이 자동으로 생길 때** — "이러면 작업이 절반이잖아!"
2. **Extrude로 팔을 잡아당기는 순간** — "점토를 늘리듯 형태가 만들어지는구나"
3. **Modifier Apply 전까지 언제든 되돌릴 수 있다는 걸 알았을 때** — Non-destructive workflow의 핵심 체감

---

## 2. Stuck Map (예상 막힘 지점)

| Step | 예상 막힘 | 원인 | 대응 |
|------|----------|------|------|
| Edit Mode 진입 | Tab 눌렀는데 아무것도 안 됨 | 오브젝트 미선택 상태 | "Tab 전에 LMB로 오브젝트 클릭 먼저" |
| Extrude | E 눌렀는데 면이 제자리에 있음 | Extrude 후 이동 없이 RMB로 취소 | "E 누른 직후 바로 마우스로 이동 or 숫자 입력" |
| Loop Cut | Ctrl+R 했는데 선이 안 보임 | 분할 수가 너무 적거나 방향이 맞지 않음 | "마우스 커서 위치에 따라 방향 결정됨" 시연 |
| Inset | I 눌렀는데 두 면이 동시에 생김 | 여러 면 선택 상태에서 Inset | 원하는 면 하나만 선택 후 I 안내 |
| Bevel | Ctrl+B가 이상하게 작동 | Scale 미적용 상태에서 Bevel | "Ctrl+A 먼저, 그 다음 Bevel" 체크리스트 |
| Mirror | Mirror 결과가 이상한 위치에 생김 | Origin이 중앙에 없음 | "Set Origin > Origin to Geometry 또는 Cursor to World Origin 후 Set Origin to 3D Cursor" |
| Subdivision | 너무 High subdivision으로 버벅임 | Viewport Level 높게 설정 | "Viewport Level 2 이하 권고" 텍스트 |
| Boolean | Boolean 결과가 검은 면으로 나옴 | Face Normal 방향 문제 | "Overlay > Face Orientation으로 빨간 면 찾기 + Flip" |
| Boolean | 커터 오브젝트가 사라지지 않음 | Exact Solver 모드 | "Solver를 Fast로 변경 또는 커터 Hide" 안내 |
| Modifier 추가 안 됨 | Edit Mode에서 Modifier 버튼 없음 | Edit Mode 상태 | "Tab으로 Object Mode 먼저" |
| Apply 타이밍 | Modifier Apply 했더니 모양이 이상 | Scale 미적용 후 Apply | "Ctrl+A 후 Modifier Apply 순서 준수" |
| Weighted Normal | Weighted Normal 추가해도 차이 없음 | Shade Smooth 미적용 상태 | "Shade Smooth 선행 필수" |

---


## 3. 평가 정합성 (Assignment Alignment)

### 과제
> Edit Mode 도구 3가지 이상 + Modifier 2가지 이상 사용한 로봇 기본형. 스크린샷 3장(과정/Modifier Stack/최종) + Modifier 목록 + 한줄 코멘트 제출.

### 학습 목표 ↔ 수업 Step ↔ 과제 매핑

| 학습 목표 | 수업 Step | 과제 검증 |
|----------|-----------|----------|
| Edit Mode 도구 활용 | Extrude, Loop Cut, Inset, Bevel 실습 | 3가지 이상 사용 + 스크린샷 |
| Modifier 스택 구성 | Mirror, Subdivision, Solidify, Array, Boolean 실습 | 2가지 이상 + 스택 스크린샷 |
| 필수 추가 Modifier | Bevel Modifier + Weighted Normal | 1가지 이상 확인 |
| 파츠 관리 흐름 | Join/Separate + Apply 타이밍 | 워크플로우 확인 |
| 기본형 완성 | 전체 실습 | 머리·몸통·팔다리 구조가 드러날 것 |

### 정합성 평가

| 파일 | 과제 제목 | 주요 내용 |
|------|----------|----------|
| `curriculum.js` | Edit + Modifier 로봇 | Edit Mode 3가지, Modifier 2가지, 필수 추가 1가지, Join/Separate 또는 Apply 확인 |
| `assignment.md` | Edit Mode + Modifier 로봇 기본 형태 | 동일 내용 (더 상세한 팁 포함) |
| `slides.md` | 과제 | 동일 요구사항 |

**결론:** 3개 파일이 비교적 잘 정합되어 있음. 채점 기준 항목명은 약간 다르나 내용은 일치. P2 수준 미세 조정.

### 채점 기준
- 도구 활용 (35%) — Edit Mode 도구와 Modifier를 적절히 조합했는가
- 형태 완성도 (35%) — 기본 구조와 실루엣이 명확한가
- 작업 흐름 이해 (20%) — 대칭, 곡면, 두께, 반복 문제를 Modifier로 해결했는가
- 창의성 (10%) — 자신만의 형태나 디테일 시도

---

## 4. 의존성 체크

### 전주차 연결
- Week 2: G/R/S, 축 제한, Apply Transform, Origin → Week 3 Edit Mode에 즉시 필요 ✅
- Week 2: Join/Separate 개념 소개됨 → Week 3 실전 적용으로 이어짐 ✅
- **Blender 미설치 학생** → 전 주차에 해결되어야 함. Week 3에서 설치 이슈 발생 시 수업 진행 불가 ⚠️

### 다음 주차 연결 (Week 4: 하드서피스 디테일)
- Week 3에서 만든 로봇 기본형 파일이 Week 4 과제의 출발점 → **파일 저장 필수** ⚠️
- Bevel Modifier + Weighted Normal → Week 4에서 심화 적용
- Apply Transform 습관 → Week 4에서도 계속 강조
- **Week 4 assignment.md 과제는 "Week 03에서 만든 로봇"을 명시** — Week 3 미완성 학생 대응 방안 필요

---

## 5. 콘텐츠 공백 (Gap Analysis)

### 검토 완료 항목
- [x] Edit Mode 4도구 설명 → lecture-note + slides 양쪽 커버 ✅
- [x] Non-destructive 개념 설명 → lecture-note에 "되돌릴 수 있음" 명시 ✅
- [x] Bevel Modifier vs Ctrl+B 차이 → lecture-note 비교표 있음 ✅
- [x] Apply Transform 타이밍 → lecture-note 표 있음 ✅
- [x] 선택 심화 Modifier(Simple Deform, Decimate) → assignment.md에 명시 ✅

### 추가 필요 항목
- [ ] **Boolean 결과 이상 (검은 면) 대응 카드** (P1): Face Orientation overlay 사용법 supplement 카드 없음
- [ ] **Mirror Origin 설정 가이드** (P1): Mirror Modifier가 잘못된 위치에 생기는 경우 supplement 필요
- [ ] **Week 3 파일 저장 체크리스트** (P1): Week 4 연속 작업을 위한 "이 파일을 Week 4에서 씁니다" 안내 필요
- [ ] **3시간 내 커버 범위 명확화** (P2): 필수 vs 선택 Modifier 구분을 slides.md에 더 명확히 표시

---

## 6. Rubric 자가 평가 (1-5점)

> Content Lead 리뷰 — 2026-04-05

| 차원 | 점수 | 근거 |
|------|------|------|
| 1. 학습 목표 구체성 | 4 | 6개 목표가 명확하고 측정 가능. Edit Mode 4도구 + Modifier 5개로 구체적 범위 명시. 우선순위 구분(필수/선택)도 있음. |
| 2. 전제 명시 | 4 | Week 2 복습 항목(G/R/S, Apply Transform, Join/Separate) 명시됨. Blender 미설치 학생 대응만 보강 필요. |
| 3. Stuck Map 완성도 | 3 | Edit Mode, Modifier, Apply 타이밍 주요 막힘 커버됨. Boolean 검은 면, Mirror Origin 이슈 대응 가이드 보완 필요. |
| 4. 평가 정합성 | 4 | 3개 파일(curriculum.js, assignment.md, slides.md)이 잘 정합됨. 채점 기준 문구 약간 다르나 내용 일치. 비교적 양호. |

**총점: 15/20**

---

## 7. 개선 액션

### P0 — 즉시 반영 필요

- 없음 (Week 3은 3파일 정합성 양호)

### P1 — 이번 주 내 반영 권고

- [ ] **Boolean 검은 면 대응 Supplement 추가:** Face Orientation Overlay 사용법 + Flip Normals 단계 안내. lecture-note "흔한 실수" 섹션에 추가.
- [ ] **Mirror Origin 설정 가이드 추가:** "Mirror Modifier가 이상한 위치에 생기면" → Set Origin 흐름 안내.
- [ ] **Week 4 파일 저장 안내:** lecture-note 과제 섹션에 "이 파일을 Week 4에서 계속 씁니다 — 저장 경로 확인" 문구 추가.

### P2 — 차기 주차 리뷰 전 반영

- [ ] 채점 기준 문구 slides.md ↔ assignment.md ↔ curriculum.js 세 파일 간 표현 통일 (현재 약간 다름).
- [ ] Array/Boolean을 "필수" vs "데모+심화" 로 slides.md에 명확히 구분 표시.
