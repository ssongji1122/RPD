# Week 1-5 기획 심화 감사 리포트

> **감사 방법:** Week 6 파일럿 동일 방식 적용 (Rubric 4차원 × 5주차)
> **감사자:** Content Lead
> **감사일:** 2026-04-05 (2026-04-05 업데이트: 시간배분 차원 제외)
> **참고:** [Week 6 파일럿 감사 결과 — RPD-1](/RPD/issues/RPD-1)

---

## 1. 주차별 Rubric 점수 요약

> Rubric 4차원: 학습목표 구체성 · 전제 명시 · Stuck Map · 평가 정합성 (각 1-5점, 총 20점)

| 주차 | 주제 | 학습목표 구체성 | 전제 명시 | Stuck Map | 평가 정합성 | **총점** |
|------|------|:-:|:-:|:-:|:-:|:-:|
| Week 1 | 오리엔테이션 + AI 무드보드 | 3 | 4 | 3 | 2 | **12/20** |
| Week 2 | Blender 인터페이스 + MCP | 3 | 3 | 3 | 1 | **10/20** |
| Week 3 | 기초 모델링 1 (Edit + Modifier) | 4 | 4 | 3 | 4 | **15/20** |
| Week 4 | 기초 모델링 2 (디테일 + 음영) | 4 | 3 | 3 | 2 | **12/20** |
| Week 5 | AI 3D 생성 + Sculpting | 4 | 4 | 3 | 3 | **14/20** |
| **Week 6** | **Material & Shader (파일럿)** | **4** | **3** | **3** | **2** | **12/20** |

> **Week 1-5 평균:** 12.6/20 (63%) — 개선 여지 큼
> **Week 6 파일럿:** 12/20 (60%)

### 차원별 패턴

| 차원 | 평균 점수 | 분석 |
|------|----------|------|
| 학습 목표 구체성 | 3.6 | Week 3-5가 양호(4점). Week 1-2는 목표 모호성 또는 분량 과다 문제 |
| 전제 명시 | 3.6 | 대체로 양호. Week 3-5는 이전 주차 연결 명시. Week 2 약점(미설치 학생 대응) |
| Stuck Map 완성도 | **3.0** | 전 주차 동일 — 필수 막힘 포인트는 있으나 세부 대응 가이드 보완 필요 |
| 평가 정합성 | **2.4** | **가장 낮은 차원.** SSOT 불일치가 4개 주차에서 발견됨 |

---

## 2. 발견된 SSOT 불일치 목록 (가장 중요)

> curriculum.js ↔ assignment.md ↔ slides.md 3중 비교 결과

### P0 — 즉시 수정 필요 (수업 전 반드시 반영)

| # | 주차 | 파일 | 불일치 내용 | 권고 수정 방향 |
|---|------|------|------------|--------------|
| 1 | **Week 1** | `curriculum.js` | 과제: "Blender 설치 확인 스크린샷" | → "무드보드 제작"으로 수정 (assignment.md + slides.md + lecture-note.md 기준) |
| 2 | **Week 2** | `curriculum.js` | 과제: "간단한 로우폴리 소품 만들기" | → "기본 도형 배치 + MCP 테스트"로 수정 (assignment.md + slides.md 기준) |
| 3 | **Week 2** | `lecture-note.md` | 과제 섹션에 Week 1 과제 내용이 복붙됨 | → Week 2 과제 내용으로 교체 |
| 4 | **Week 4** | `curriculum.js` | 과제: "로봇 몸체 완성" (팔다리 포함 전신 조립) | → "로봇 디테일 & 음영 정리"로 수정 (assignment.md + slides.md 기준) |

### P1 — 이번 주 내 반영 권고

| # | 주차 | 파일 | 불일치 내용 | 권고 수정 방향 |
|---|------|------|------------|--------------|
| 5 | **Week 5** | `assignment.md`, `slides.md` | curriculum.js보다 체크리스트가 간략함. "Week 6 .blend 파일 저장" 항목 누락 | → curriculum.js 체크리스트 수준으로 보강 |
| 6 | **Week 3** | 채점 기준 문구 | 3개 파일 간 채점 기준 표현이 약간 다름 | → 통일 필요 (내용은 일치하므로 P1) |

### 상세: P0 수정 전후 비교

#### P0-1: Week 1 curriculum.js 과제

**현재 (수정 전)**
```json
"assignment": {
  "title": "Blender 설치 확인 스크린샷",
  "description": "Blender를 실행해서 Welcome Screen이 보이는 화면을 캡처해서 제출하세요.",
  "checklist": ["Blender 정상 실행 확인", "버전 번호 포함된 스크린샷 제출"]
}
```

**권고 (수정 후)**
```json
"assignment": {
  "title": "무드보드 제작",
  "description": "Mixboard 또는 나노바나나를 활용하여 자신의 로봇/캐릭터 무드보드를 제작한다. 무드보드 이미지 2장 + 캐릭터/로봇 컨셉 한줄 설명을 Discord #week01-assignment 채널에 제출.",
  "checklist": ["AI 도구(Mixboard 또는 나노바나나) 사용", "무드보드 이미지 2장 이상 생성", "캐릭터/로봇 컨셉 한줄 설명 작성", "Discord #week01-assignment 제출 완료"]
}
```

#### P0-2: Week 2 curriculum.js 과제

**현재 (수정 전)**
```json
"assignment": {
  "title": "간단한 로우폴리 소품 만들기",
  "description": "화면 조작과 기본 모델링 도구를 사용해 간단한 소품을 만들고 제출합니다.",
  "checklist": ["완성 이미지 2장 이상", ".blend 파일 1개", "사용한 도구 3개 이상 적기"]
}
```

**권고 (수정 후)**
```json
"assignment": {
  "title": "기본 도형 배치 + MCP 테스트",
  "description": "기본 도형 5개 이상을 자유 배치한 씬 스크린샷 + Blender MCP 연결 테스트 성공 스크린샷 + 한줄 코멘트를 Discord #week02-assignment 채널에 제출.",
  "checklist": ["기본 도형 5개 이상 배치한 씬 스크린샷", "Blender MCP 연결 테스트 성공 스크린샷", "한줄 코멘트 (어려웠던 점 포함)"]
}
```

#### P0-3: Week 2 lecture-note.md 과제 섹션

**현재 (수정 전):** Week 1 무드보드 과제 내용이 그대로 복붙됨

**권고 (수정 후):** Week 2 과제 내용으로 교체
```markdown
## 과제

- **제출:** Discord #week02-assignment 채널
- **내용:** 스크린샷 2장(도형 배치 + MCP 연결 테스트) + 한줄 코멘트
- **기한:** 다음 수업 전까지
```

#### P0-4: Week 4 curriculum.js 과제

**현재 (수정 전)**
```json
"assignment": {
  "title": "로봇 몸체 완성",
  "description": "Week 03 머리/얼굴/안테나에 몸통, 팔다리, 손발을 붙여 로봇 전신을 완성하세요.",
  "checklist": ["몸통 + 관절 구체 배치 완료", "팔/다리 파츠 좌우 대칭 제작", "손 또는 발 디테일 1곳 이상", "Bevel 1회 이상 사용", "파츠 정리 + Apply Transform 완료 스크린샷"]
}
```

**권고 (수정 후)**
```json
"assignment": {
  "title": "로봇 디테일 & 음영 정리",
  "description": "Week 03 기본형에 디테일을 추가하고 표면 음영을 정리한다. 스크린샷 3장 + 사용한 도구/Modifier 목록 + 한줄 코멘트 제출.",
  "checklist": ["얼굴/관절/패널 중 디테일 1곳 이상 추가", "Ctrl+B 또는 Bevel Modifier 1회 이상 사용", "Weighted Normal 적용 확인", "Apply Transform 완료 + Modifier Stack 스크린샷", "한줄 코멘트"]
}
```

---

## 3. P0 액션 리스트 (즉시 수정 필요)

> 수업 진행에 직접 영향을 주는 항목. 해당 주차 수업 전까지 반영 필요.

- [ ] **[Week 1] curriculum.js 과제 수정** — 과제 제목/설명/체크리스트를 "무드보드 제작" 기준으로 통일
- [ ] **[Week 2] curriculum.js 과제 수정** — "로우폴리 소품" → "기본 도형 배치 + MCP 테스트"로 통일
- [ ] **[Week 2] lecture-note.md 과제 섹션 교체** — Week 1 복붙 내용 → Week 2 과제 내용으로 교체
- [ ] **[Week 4] curriculum.js 과제 수정** — "로봇 몸체 완성(전신 조립)" → "로봇 디테일 & 음영 정리"로 스코프 통일

---

## 4. 공통 패턴 분석 (반복 나타나는 문제)

### 패턴 1: curriculum.js가 실제 수업과 불일치 (4주차 발견)

Week 1, 2, 4에서 curriculum.js 과제 내용이 assignment.md, slides.md, lecture-note.md와 다름.
curriculum.js가 **실제 수업 내용보다 뒤처져 있거나 초기 기획 내용을 그대로 유지**하는 것으로 보임.

**원인 가설:** 수업 콘텐츠 업데이트 시 curriculum.js를 함께 업데이트하지 않는 워크플로우 문제.

**권고:** 과제 변경 시 curriculum.js를 체크리스트 항목으로 포함하는 업데이트 규칙 도입.
```
과제 변경 체크리스트:
- [ ] assignment.md 수정
- [ ] slides.md 과제 슬라이드 수정
- [ ] lecture-note.md 과제 섹션 수정
- [ ] curriculum.js assignment 필드 수정
```

### 패턴 2: Stuck Map이 "항목은 있으나 대응 가이드가 약함"

모든 주차에서 Stuck Map 점수 3점. 막힘 지점 항목은 존재하나 구체적인 해결 단계(스크린샷, supplement 카드)가 부족.

**권고:** 각 주차 P1 액션에서 상위 3개 막힘 지점에 대해 supplement 카드 또는 lecture-note 흔한 실수 섹션에 단계별 해결법 추가.

### 패턴 3: 파일 저장 연결 안내 누락

Week 3 → Week 4, Week 4 → Week 5, Week 5 → Week 6 모두 이전 주차 파일이 다음 주차 시작점이 되지만, 해당 연결 안내가 모든 주차에서 명시되지 않음.

**권고:** 각 주차 lecture-note 과제 섹션 말미에 "이 파일을 Week XX에서 씁니다 — 저장 경로 확인" 안내 표준화.

### 패턴 4: 시간 계획에 기술 이슈 버퍼 없음

Week 2(설치), Week 3(Boolean 이슈), Week 5(AI 생성 대기) 모두 예상 외 소요 시간이 있으나 시간 계획에 버퍼가 없음.

**권고:** 각 주차 시간 계획에 "기술 이슈 버퍼 10분" 명시. 특히 새 도구를 처음 소개하는 주차(Week 2 MCP, Week 5 AI 도구).

---

## 5. 주차별 추가 P1 액션 요약

> 각 주차 design.md의 P1 액션 중 공통성 있거나 우선순위 높은 항목 요약

| 주차 | P1 액션 (핵심 1개) |
|------|------------------|
| Week 1 | Blender 사전 설치 독려 문구 강화 + 컨셉 시트 미니 템플릿 추가 |
| Week 2 | MCP 설치 Supplement 가이드 + 시간 배분 재조정 (MCP를 과제로 이월) |
| Week 3 | Boolean 검은 면 대응 Supplement + Week 4 파일 저장 안내 추가 |
| Week 4 | Week 3 기본형 미완성 학생 대응 방안 + Week 5 파일 저장 안내 |
| Week 5 | assignment.md + slides.md 체크리스트 보강 (Week 6 .blend 저장 포함) |

---

## 6. 개선 이후 예상 효과

| 영역 | 현재 | 개선 후 예상 |
|------|------|------------|
| SSOT 정합성 | 4개 주차 P0 불일치 | P0 0건 (P0 수정 후) |
| 학생 과제 혼란 | "어느 파일 기준으로 제출?" 질문 빈발 | curriculum.js = assignment.md = slides.md 통일로 혼란 제거 |
| 주차 연속성 | 파일 저장 누락으로 다음 주차 시작 지연 | 저장 안내 표준화로 연속 작업 원활 |
| Stuck Map 품질 | 항목 있으나 해결법 약함 | Supplement 카드 추가로 강사 대응 속도 향상 |

---

## 7. 감사 방법론 메모

- **참고 파일:** `weeks/week06-material/design.md` (파일럿 완성본) 동일 구조 적용
- **3중 비교 파일:** `course-site/data/curriculum.js` ↔ `weeks/weekXX/assignment.md` ↔ `weeks/weekXX/slides.md`
- **추가 참조:** `weeks/weekXX/lecture-note.md` (강의 내용 확인)
- **이슈 트래킹:** [RPD-1](/RPD/issues/RPD-1) (Week 6 파일럿), [RPD-2](/RPD/issues/RPD-2) (이 감사)
