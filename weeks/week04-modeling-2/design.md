# Week 4 기획 심화 (Design Doc)

> **목적:** curriculum.js의 콘텐츠가 아닌, 수업 기획 자체의 질을 검증하기 위한 문서.
> Content Lead + CPO가 Rubric 기반으로 주차별 기획을 심층 리뷰할 때 사용한다.

**주제:** 기초 모델링 2 — 하드서피스 디테일 & 음영 정리
**수업일:** 2026-03-25 (화) 예정
**강의실:** 인하대학교 (60주년관)
**Duration:** ~3시간
**Status:** done
**리뷰 완료일:** 2026-04-05

---

## 1. Student Journey (학생 여정)

### 시작 상태 (Week 3 종료 시점)
- 로봇 기본형(머리+몸통 수준) 완성
- Mirror, Subdivision, Solidify, Bevel Modifier + Weighted Normal 경험
- 파츠 분리/합치기(Join/Separate) 기본 이해
- Apply Transform 습관 형성 중

### 끝 상태 (Week 4 종료 시점)
- [ ] Ctrl+B(직접 Bevel)와 Bevel Modifier의 차이를 상황에 맞게 선택 가능
- [ ] Inset, Boolean을 활용한 얼굴/패널/관절 디테일 1곳 이상 추가
- [ ] Weighted Normal 적용 전후 음영 차이를 육안으로 확인
- [ ] Modifier Stack 순서 이해 및 Apply 타이밍 판단 가능
- [ ] Apply Transform + 파츠 정리 완료 상태 스크린샷 제출
- [ ] Discord #week04-assignment 제출 완료 (스크린샷 3장 + 도구 목록 + 한줄)

### 핵심 전환점 ("아하!" 모먼트)
1. **Ctrl+B로 날카로운 모서리가 부드럽게 깎일 때** — "이게 기계 느낌이구나"
2. **Weighted Normal 적용 후 하드서피스 음영이 깔끔해지는 순간** — "같은 모양인데 빛이 다르게 보이네"
3. **Modifier Stack 순서를 바꿨더니 결과가 달라질 때** — "순서가 중요하다는 게 이런 거구나"

---

## 2. Stuck Map (예상 막힘 지점)

| Step | 예상 막힘 | 원인 | 대응 |
|------|----------|------|------|
| Step 1 (Transform 정리) | Scale이 (1,1,1)이 아닌데 모름 | N 패널 확인 습관 미형성 | "작업 시작 전 N 패널 > Scale 확인" 체크리스트 |
| Step 2 (디테일) | Inset 후 Extrude 방향이 이상 | Normal 방향 불일치 | "Face Orientation 확인 + Alt+N > Recalculate Outside" |
| Step 2 (디테일) | Boolean 커터가 어디 있는지 모름 | Object Outliner에서 숨겨짐 | "H로 Hide, Alt+H로 Show" 단축키 안내 |
| Step 3 (Bevel) | Ctrl+B 결과가 Scale 적용 안 된 것처럼 이상 | Ctrl+A 미적용 | "Bevel 전 반드시 Ctrl+A 확인" |
| Step 3 (Bevel) | Bevel Modifier Width 값이 너무 크거나 작음 | 오브젝트 스케일에 따라 다름 | "Width 0.01~0.05 범위에서 시작" 권장값 제시 |
| Step 4 (Weighted Normal) | Weighted Normal 추가해도 차이 없음 | Shade Smooth 미적용 | "RMB > Shade Smooth 먼저, 그 다음 Weighted Normal" |
| Step 4 (Weighted Normal) | Weighted Normal이 Modifier 목록에 없음 | Blender 5.0 위치 변경 | "Normals 카테고리 아래에 있음" 안내 |
| Step 5 (Apply 타이밍) | Apply 했더니 모양이 망가짐 | Scale 미적용 후 Apply | "반드시 Ctrl+A 후 Modifier Apply 순서" |
| Step 5 (Apply 타이밍) | "Apply해야 하나요?" 질문 반복 | 타이밍 기준 불명확 | "이번 주는 Apply 안 해도 됨. 확정할 때만" 명확히 |
| 과제 내용 혼란 | "전신 완성인지, 디테일 추가인지" | curriculum.js vs assignment.md 불일치 → **P0 수정 필요** | 수업 중 구두 안내 (디테일 + 음영 정리가 이번 주) |

---

## 3. 시간 배분 (3시간 수업)

| 시간 | 내용 | 비율 |
|------|------|------|
| 00:00-00:10 | 인트로, Week 3 복습 + 각자 기본형 현황 공유 | 6% |
| 00:10-00:25 | 이론: 디테일 도구 (Inset, Boolean, Bevel 두 종류) | 8% |
| 00:25-00:55 | 실습 Step 1-2: Transform 정리 + 디테일 추가 | 17% |
| 00:55-01:20 | 실습 Step 3: Ctrl+B vs Bevel Modifier 비교 | 14% |
| 01:20-01:30 | 이론: Weighted Normal + Apply 타이밍 | 6% |
| 01:30-02:00 | **중간 휴식 + 개인 작업 시간** | - |
| 02:00-02:30 | 실습 Step 4-5: Weighted Normal + Modifier Stack 정리 | 17% |
| 02:30-02:50 | 개인 작업 + 트러블슈팅 | 11% |
| 02:50-03:00 | 과제 안내 + 마무리 | 6% |

**실습 : 강의 비율** = 약 65% : 35%

> ⚠️ **현실성 주의:** Week 3에서 기본형이 완성되지 않은 학생은 이번 주 디테일 추가가 불가. "기본형 미완성 학생 대응 방안" 필요 — Cube에서 시작하는 최소 대체 작업 경로 제시 권고. Boolean은 Normal 이슈로 디버깅 시간이 길어질 수 있음.

---

## 4. 평가 정합성 (Assignment Alignment)

### 과제
> Week 03 기본형에 디테일 1곳 이상 추가 + Bevel 1회 이상 + Weighted Normal 확인 + 스크린샷 3장 + 도구 목록 + 한줄 코멘트

### 학습 목표 ↔ 수업 Step ↔ 과제 매핑

| 학습 목표 | 수업 Step | 과제 검증 |
|----------|-----------|----------|
| Bevel 두 종류 이해 | Step 3: Ctrl+B vs Bevel Modifier 비교 | Bevel 1회 이상 사용 |
| 디테일 추가 | Step 2: Inset, Extrude, Boolean | 얼굴/관절/패널 디테일 1곳 이상 |
| Weighted Normal | Step 4: Weighted Normal 적용 | 실제 적용 또는 비교 확인 |
| Apply Transform | Step 1: Transform 정리 | Apply Transform 완료 스크린샷 |
| Modifier Stack | Step 5: 순서 확인 + Apply 타이밍 | Modifier Stack 스크린샷 |

### ⚠️ SSOT 불일치 발견 (P0)

| 파일 | 과제 제목 | 주요 내용 |
|------|----------|----------|
| `curriculum.js` | 로봇 몸체 완성 | 몸통+관절 배치, 팔/다리 좌우 대칭, 손/발 디테일, Bevel 1회, Apply 완료 |
| `assignment.md` | 로봇 디테일 & 음영 정리 | 디테일 1곳, Bevel 계열 1회, Weighted Normal 확인, Apply 확인 |
| `slides.md` | 과제 | 얼굴/관절/패널 디테일 1곳, Ctrl+B 또는 Bevel Modifier, Weighted Normal 확인, 스크린샷 3장 |

**결론:** curriculum.js는 "전신 조립 완성"(팔다리 포함), assignment.md+slides.md는 "디테일+음영 정리"로 스코프가 다름. curriculum.js의 Week 4 과제가 Week 4 실제 수업 내용과 불일치. P0 수정 필요.

### 채점 기준
- 디테일 완성도 (40%) — 얼굴, 패널, 관절 등 디테일이 분명하게 보이는가
- 도구 이해 (35%) — Bevel, Weighted Normal, Apply 시점을 적절히 이해했는가
- 화면 정리 (25%) — 음영과 파츠 구성이 깔끔하게 정리되었는가

---

## 5. 의존성 체크

### 전주차 연결
- Week 3 기본형 파일 필요 → 미완성 학생 대응 방안 없음 ⚠️
- Week 3: Bevel Modifier + Weighted Normal 소개 → Week 4에서 심화 적용
- Week 3: Apply 타이밍 → Week 4에서 반복 강조 (두 번 배우는 구조 의도적) ✅

### 다음 주차 연결 (Week 5: AI 3D + Sculpting)
- Week 4 완성 파일이 Week 5 Sculpt Mode 작업의 기반 → **파일 저장 필수** ⚠️
- Week 5 Assignment: "1주차 무드보드 기반 AI 러프" → Week 1 컨셉 파일도 필요
- **Mesh 정리 상태(Weighted Normal, Apply Transform)** → Week 5 AI 모델 임포트 후 비교 기준이 됨

---

## 6. 콘텐츠 공백 (Gap Analysis)

### 검토 완료 항목
- [x] Ctrl+B vs Bevel Modifier 차이 → lecture-note 비교 설명 있음 ✅
- [x] Weighted Normal + Shade Smooth 순서 → lecture-note에 언급 ✅
- [x] Apply Transform 타이밍 → lecture-note 표 있음 ✅
- [x] Modifier Stack 순서 → Step 5에 포함 ✅

### 추가 필요 항목
- [ ] **curriculum.js 과제 수정** (P0): "로봇 몸체 완성" → "로봇 디테일 & 음영 정리"로 내용 일치 필요. checklist도 assignment.md 기준으로 교체.
- [ ] **Week 3 기본형 미완성 학생 대응 방안** (P1): "Cube에서 디테일 연습하기" 또는 "강사 제공 기본형 파일" 옵션 필요.
- [ ] **Week 5 연결 저장 안내** (P1): "이 파일을 Week 5 Sculpt 기반으로 씁니다" 안내 필요.
- [ ] **Boolean 커터 관리 가이드** (P1): Hide/Show 단축키 + Outliner에서 관리하는 방법 supplement.

---

## 7. Rubric 자가 평가 (1-5점)

> Content Lead 리뷰 — 2026-04-05

| 차원 | 점수 | 근거 |
|------|------|------|
| 1. 학습 목표 구체성 | 4 | Ctrl+B vs Bevel Modifier 비교, Weighted Normal 전후 비교, Apply 타이밍 기준이 모두 명확. "디테일 1곳 이상"은 측정 가능한 기준. |
| 2. 전제 명시 | 3 | Week 3 기본형 파일 필요함이 assignment.md에 명시됨. 그러나 미완성 학생 대응 방안 없음. |
| 3. Stuck Map 완성도 | 3 | Bevel, Weighted Normal, Apply 타이밍의 주요 막힘 커버됨. Boolean 커터 관리, Weighted Normal 위치 변경(Blender 5.0) 항목 보완 필요. |
| 4. 시간 배분 현실성 | 3 | 3시간 구성은 합리적. Week 3 기본형 미완성 학생 트러블슈팅 시간이 계획에 없음. 개인 작업 시간 30분이 이를 어느 정도 흡수할 수 있음. |
| 5. 평가 정합성 | 2 | **Major mismatch:** curriculum.js "로봇 몸체 완성(전신 조립)" vs assignment.md "디테일+음영 정리"로 스코프 다름. P0 수정 필요. |

**총점: 15/25**

---

## 8. 개선 액션

### P0 — 즉시 반영 필요

- [ ] **curriculum.js Week 4 과제 수정:** `assignment.title` → "로봇 디테일 & 음영 정리", `assignment.description` + `checklist` → assignment.md 기준 (디테일 1곳, Bevel 1회, Weighted Normal 확인, 스크린샷 3장)으로 통일.

### P1 — 이번 주 내 반영 권고

- [ ] **Week 3 기본형 미완성 학생 대응 방안:** lecture-note 도입부에 "Week 3 파일 없는 경우 → Cube에서 시작해도 됨" 안내 추가.
- [ ] **Week 5 파일 저장 안내:** lecture-note 과제 섹션에 "이 파일을 Week 5에서 씁니다" 안내.
- [ ] **Boolean 커터 관리 Supplement:** H/Alt+H 단축키 + Outliner 컬렉션 관리 방법 추가.

### P2 — 차기 주차 리뷰 전 반영

- [ ] 채점 기준 slides.md ↔ assignment.md 일치 확인 (현재 slides.md가 더 간략함 — 통일 권고).
- [ ] "Weighted Normal이 Blender 5.0에서 Normals 카테고리로 이동됨" 안내를 lecture-note에 추가.
