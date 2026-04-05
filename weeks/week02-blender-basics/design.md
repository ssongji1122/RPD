# Week 2 기획 심화 (Design Doc)

> **목적:** curriculum.js의 콘텐츠가 아닌, 수업 기획 자체의 질을 검증하기 위한 문서.
> Content Lead + CPO가 Rubric 기반으로 주차별 기획을 심층 리뷰할 때 사용한다.

**주제:** Blender 5.0 인터페이스 & 기초 조작 + MCP 설정
**수업일:** 2026-03-11 (화) 예정
**강의실:** 인하대학교 (60주년관)
**Duration:** ~3시간
**Status:** done
**리뷰 완료일:** 2026-04-05

---

## 1. Student Journey (학생 여정)

### 시작 상태 (Week 1 종료 시점)
- 무드보드 완성, 자신의 로봇/캐릭터 컨셉 1차 결정됨
- Blender 미설치 상태 (일부는 사전 설치)
- 3D 소프트웨어 경험 거의 없음

### 끝 상태 (Week 2 종료 시점)
- [ ] Blender 5.0 설치 완료 및 Preferences 설정
- [ ] 뷰포트 4개 영역의 역할 설명 가능
- [ ] Numpad 1/3/7로 뷰 전환, MMB로 Orbit 자유롭게 가능
- [ ] G/R/S + 축 제한으로 오브젝트 이동/회전/스케일 가능
- [ ] 3D Cursor, Origin 개념 이해 및 사용 가능
- [ ] Apply Transform (Ctrl+A) 적용 가능
- [ ] Join/Separate 기본 사용 가능
- [ ] Blender MCP 연결 완료 + 기본 명령 실행 성공
- [ ] Discord #week02-assignment 제출 완료

### 핵심 전환점 ("아하!" 모먼트)
1. **G+X, G+Y, G+Z 축 고정이 작동할 때** — "오, 이렇게 정밀하게 이동하는구나"
2. **Blender MCP로 Claude 명령이 Blender 씬에 즉시 반영될 때** — "AI랑 같이 3D를 만들 수 있구나"
3. **Origin을 이동하니 G/R/S 기준점이 달라질 때** — 3D 커서/Origin 개념이 손에 잡히는 순간

---

## 2. Stuck Map (예상 막힘 지점)

| Step | 예상 막힘 | 원인 | 대응 |
|------|----------|------|------|
| 설치 | Apple Silicon인데 인텔 버전 설치 | 다운로드 페이지 혼동 | "Apple Silicon(M1·M2·M3)" 버전 명시 안내 |
| Preferences | Emulate 3 Button Mouse 위치 못 찾음 | Preferences 창 낯섦 | Edit → Preferences → Input 탭 직접 시연 |
| 뷰 전환 | 노트북 사용자 Numpad 없음 | 키보드 배열 | Emulate Numpad 설정 안내 |
| Orbit | 마우스 가운데 버튼 없음 | 노트북 트랙패드 | Emulate 3 Button Mouse로 Alt+LMB 대체 |
| G/R/S | 숫자 입력 후 Enter 안 눌러서 취소됨 | 습관 미형성 | 반드시 LMB 클릭 또는 Enter로 확정 명시 |
| 3D Cursor | Shift+RMB 했는데 오브젝트가 이상해짐 | 3D Cursor 이동 혼동 | "빨간 십자가 = 커서. Shift+S > Cursor to World Origin으로 리셋" |
| Origin | Origin 이동 후 Mirror Modifier가 이상함 | Origin 위치 변경 효과 | "Mirror는 Origin 기준. Apply Transform 후 작업" 명시 |
| Apply Transform | Scale이 (1,1,1)이 아닌데 모르고 진행 | 확인 습관 미형성 | N 패널 > Item 탭 > Scale 확인 스크린샷 supplement |
| MCP 설치 | Blender MCP addon 설치 오류 | 버전 불일치, 경로 오류 | GitHub 링크 + 설치 단계별 스크린샷 supplement 필요 |
| MCP 연결 | Claude와 연결은 됐는데 명령이 안 작동 | 포트 충돌, addon 미활성화 | 콘솔 로그 확인 + Discord 질문 유도 |
| 과제 내용 혼란 | "로우폴리 소품을 만드는 건지, 기본 도형 배치인지" | curriculum.js vs assignment.md 불일치 → **P0 수정 필요** | 수업 중 명확히 안내 (기본 도형 배치 + MCP) |

---

## 3. 시간 배분 (3시간 수업)

| 시간 | 내용 | 비율 |
|------|------|------|
| 00:00-00:15 | 인트로, 지난주 무드보드 공유 (2-3명 발표) | 8% |
| 00:15-00:40 | Blender 설치 + Preferences 설정 (실습) | 14% |
| 00:40-01:00 | UI 구조 강의 (4개 영역, 5.0 변경점) | 11% |
| 01:00-01:30 | 뷰포트 조작 실습 (Orbit/Pan/Zoom/Numpad) | 17% |
| 01:30-02:00 | **점심/중간 휴식** | - |
| 02:00-02:30 | G/R/S + 축 제한 + Apply Transform 실습 | 17% |
| 02:30-02:45 | 3D Cursor / Origin / Transform Pivot 설명 | 8% |
| 02:45-03:00 | MCP 설치 + 연결 테스트 + 과제 안내 | 8% |

> 실제 수업은 점심 없이 3시간 연속일 수 있음 (일정 확인 필요). 3시간 연속이라면 중간 10분 휴식 삽입 권고.

**실습 : 강의 비율** = 약 55% : 45%

> ⚠️ **현실성 주의:** Blender 설치 문제(Apple Silicon 혼동, 설치 오류)로 15-20분 추가 소요 가능. MCP 설치 실습은 시간 초과 위험 — 수업 중 시연만 하고 설치는 과제로 넘기는 옵션 고려. Join/Separate/Bridge는 lecture-note에 있으나 시간 계획 외 내용 — 빠르게 언급하거나 Week 3으로 이월 고려.

---

## 4. 평가 정합성 (Assignment Alignment)

### 과제
> 기본 도형 5개 이상 배치한 씬 스크린샷 + Blender MCP 연결 테스트 스크린샷 + 한줄 코멘트

### 학습 목표 ↔ 수업 Step ↔ 과제 매핑

| 학습 목표 | 수업 Step | 과제 검증 |
|----------|-----------|----------|
| 뷰포트 조작 & Transform | G/R/S + Numpad 실습 | 도형 5개 이상, 다양한 위치·크기 |
| 기본 도형 배치 | 기본 도형으로 씬 만들기 | 의도를 가진 씬 구성 |
| MCP 연결 | MCP 설치 + 테스트 | MCP 연결 성공 스크린샷 |

### ⚠️ SSOT 불일치 발견 (P0)

| 파일 | 과제 제목 | 내용 |
|------|----------|------|
| `curriculum.js` | 간단한 로우폴리 소품 만들기 | 완성 이미지 2장 + .blend 파일 + 사용 도구 3개 이상 목록 |
| `assignment.md` | 기본 도형 배치 + MCP 테스트 | 스크린샷 2장(도형 배치 + MCP 연결) + 한줄 코멘트 |
| `slides.md` | 과제 안내 | 스크린샷 1장(도형 5개), MCP 연결 테스트, 한줄 코멘트 |
| `lecture-note.md` | 과제 | 무드보드 이미지 2장 + 컨셉 한줄 설명 (← Week 1 과제 그대로! 별도 수정 필요) |

**결론:** curriculum.js는 "로우폴리 소품", assignment.md+slides.md는 "기본 도형 배치+MCP"로 불일치. lecture-note.md의 과제 섹션은 Week 1 내용이 그대로 복붙되어 있음. 모두 P0 수정 필요.

### 채점 기준
- 도구 활용 (40%) — Transform, 뷰 조작, MCP 연결
- 완성도 (30%) — 의도를 가진 씬 구성
- 창의성 (30%) — 독창적인 구성 시도

---

## 5. 의존성 체크

### 전주차 연결
- Week 1 무드보드 컨셉 → Week 2 씬 배치에 방향 제공 ✅
- Blender 미설치 학생 다수 예상 → 수업 시작 15-20분 설치 대기 가능 ⚠️ (버퍼 확인 필요)

### 다음 주차 연결 (Week 3: Edit Mode + Modifier)
- Apply Transform (Ctrl+A) 습관 → Week 3 Modifier 작업에 필수 ⚠️ (이 주에 반드시 습관화)
- G/R/S 축 제한 숙달 → Week 3 기본형 모델링에 직접 연결
- Join/Separate 개념 → Week 3에서 파츠 관리 시 필요 (이 주에 소개, Week 3에서 심화)

---

## 6. 콘텐츠 공백 (Gap Analysis)

### 검토 완료 항목
- [x] Blender 5.0 UI 변경사항 설명 → slides.md에 Pill 탭, Workspace 통합 명시 ✅
- [x] Apple Silicon 안내 → lecture-note 설치 섹션에 명시 ✅
- [x] MCP 연결 오류 대응 → "콘솔 로그 확인 + Discord 질문" 안내 있음 ✅
- [x] Emulate 설정 안내 → Preferences 표에 포함 ✅

### 추가 필요 항목
- [ ] **curriculum.js 과제 수정** (P0): "간단한 로우폴리 소품" → "기본 도형 배치 + MCP 테스트"로 수정
- [ ] **lecture-note.md 과제 섹션 수정** (P0): Week 1 과제 내용이 복붙된 상태 — Week 2 과제 내용으로 교체
- [ ] **MCP 설치 Supplement 카드** (P1): 단계별 스크린샷 포함 설치 가이드 — 현재 링크만 있음
- [ ] **Join/Separate 포지셔닝 명확화** (P1): 이 주에 "소개" 수준인지 Week 3에서 "심화"인지 모호함

---

## 7. Rubric 자가 평가 (1-5점)

> Content Lead 리뷰 — 2026-04-05

| 차원 | 점수 | 근거 |
|------|------|------|
| 1. 학습 목표 구체성 | 3 | 9개 학습 목표가 명확하나 분량이 많아 3시간 내 달성 가능성 불확실. MCP 목표는 "연결 성공"까지만 범위를 명시해야 함. |
| 2. 전제 명시 | 3 | Week 1 무드보드 컨셉 연결은 언급됨. 그러나 "일부 학생은 Blender 미설치" 상태임을 수업 플랜에 명시하지 않아 강사가 설치 소요 시간을 예측하기 어려움. |
| 3. Stuck Map 완성도 | 3 | 주요 막힘 포인트 커버됨. MCP 연결 실패 시 구체적 대응(포트 번호, addon 재시작) 가이드 부족. lecture-note.md 과제 복붙 오류는 Stuck Map 외 P0 이슈. |
| 4. 시간 배분 현실성 | 2 | 설치 + UI + 뷰 조작 + Transform + Origin + MCP를 3시간 안에 모두 소화하는 것은 타이트함. 특히 MCP 설치 변수 감안 시 현실적으로 마지막 20분이 위험. 컨텐츠 분할 또는 MCP를 과제로 이월 고려 필요. |
| 5. 평가 정합성 | 1 | **Major mismatch 2건:** curriculum.js 과제 내용 불일치, lecture-note.md에 Week 1 과제가 그대로 있음. 모두 P0. |

**총점: 12/25**

---

## 8. 개선 액션

### P0 — 즉시 반영 필요

- [ ] **curriculum.js Week 2 과제 수정:** `assignment.title` → "기본 도형 배치 + MCP 테스트", `assignment.description` + `checklist` → assignment.md 기준으로 통일.
- [ ] **lecture-note.md 과제 섹션 교체:** 현재 Week 1 내용 복붙 상태 → Week 2 과제 내용(스크린샷 2장 + MCP + 한줄 코멘트)으로 교체.

### P1 — 이번 주 내 반영 권고

- [ ] **MCP 설치 Supplement 가이드:** 단계별 스크린샷 포함 문서 추가 또는 lecture-note에 상세 단계 추가.
- [ ] **시간 배분 재조정:** MCP 연결 실습을 수업 시연만 하고 설치를 과제로 이월하는 옵션을 강사 노트에 명시.
- [ ] **Join/Separate 포지셔닝:** 이 주는 "개념 소개", Week 3은 "실전 적용"으로 명시.

### P2 — 차기 주차 리뷰 전 반영

- [ ] 학습 목표 개수 조정: 9개 → 우선순위 5개로 압축 (Transform, 뷰포트 조작, Origin, Apply Transform, MCP 연결).
- [ ] 채점 기준 slides.md ↔ assignment.md 일치 확인 (현재 일치함).
