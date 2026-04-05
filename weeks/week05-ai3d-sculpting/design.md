# Week 5 기획 심화 (Design Doc)

> **목적:** curriculum.js의 콘텐츠가 아닌, 수업 기획 자체의 질을 검증하기 위한 문서.
> Content Lead + CPO가 Rubric 기반으로 주차별 기획을 심층 리뷰할 때 사용한다.

**주제:** AI 3D 생성 + Sculpting (Remesh 심화는 Week 6로 이동)
**수업일:** 2026-04-01 (화) 예정
**강의실:** 인하대학교 (60주년관)
**Duration:** ~3시간
**Status:** done (이미 보강 완료된 주차 — 정합성 확인 위주)
**리뷰 완료일:** 2026-04-05

---

## 1. Student Journey (학생 여정)

### 시작 상태 (Week 4 종료 시점)
- 로봇 기본형 + 디테일 1곳 이상 완성
- Bevel, Weighted Normal, Apply Transform 경험
- AI 도구로 이미지 생성 경험(Week 1)은 있으나 AI 3D 생성은 처음

### 끝 상태 (Week 5 종료 시점)
- [ ] Meshy AI(Text to 3D) 또는 Tripo AI(Image to 3D)로 3D 모델 생성 가능
- [ ] AI 모델을 Blender에 GLB 임포트 가능 (스케일 조정, Origin 설정, Apply Transform)
- [ ] Sculpt Mode 기본 브러시(Draw, Smooth, Grab, Clay Strips) 사용 가능
- [ ] Dyntopo로 스컬프팅 중 자동 폴리곤 생성 체험 가능
- [ ] Before/After 비교 스크린샷 제출 가능
- [ ] **Remesh 심화 (Voxel/Quad/QRemeshify/Mesh Cleaner 2)는 Week 6 Step 1에서 학습**
- [ ] (optional) Blender MCP로 씬 자동 생성 경험
- [ ] Discord #week05-assignment 제출 완료
- [ ] **Week 6 Material 실습용 .blend 파일 저장 완료** (curriculum.js 명시 항목)

### 핵심 전환점 ("아하!" 모먼트)
1. **AI가 3D 모델을 실시간으로 생성하는 순간** — "텍스트 몇 줄로 이게 나온다고?"
2. **Sculpt Mode에서 Smooth 브러시로 AI 모델 표면이 정리될 때** — "내가 직접 고칠 수 있구나"
3. **Before/After 비교할 때 차이가 눈에 보일 때** — "AI + Blender 조합이 이런 거구나"

---

## 2. Stuck Map (예상 막힘 지점)

| Step | 예상 막힘 | 원인 | 대응 |
|------|----------|------|------|
| Meshy 접속 | 로그인 오류 | 계정 미생성 | Google 계정으로 빠른 가입 안내 |
| Meshy 생성 | 크레딧 부족 | 무료 크레딧 소진 | Tripo AI(월 500 크레딧)로 전환 안내 |
| GLB 임포트 | 모델이 너무 크거나 작음 | GLB 스케일 100배 문제 | "S 키로 스케일 조정, Apply Transform 필수" |
| GLB 임포트 | 텍스처가 없는 회색 모델로 들어옴 | 텍스처 미포함 GLB | "Week 5는 형태만 사용, 텍스처는 Week 6에서" 안내 |
| GLB 임포트 | 모델이 여러 파츠로 쪼개져 들어옴 | AI 모델 파츠 분리 | "Ctrl+J로 Join 후 작업" 안내 |
| Sculpt Mode | 브러시가 너무 작거나 큰 효과 | 브러시 크기/강도 미조정 | "F키 = 크기, Shift+F = 강도" 안내 |
| Sculpt Mode | 브러시가 전체에 영향을 줌 | Mask 없이 전체 조각 | "Mask 브러시로 보호 영역 먼저" |
| Sculpt Mode | Ctrl 눌렀는데 이상한 효과 | Draw 브러시에서 Ctrl = Subtract | "Ctrl로 더하기/빼기 전환됨" 안내 |
| Sculpt Mode | 메쉬가 너무 무거워 버벅임 | AI 모델 고폴리 | "Decimate Modifier 적용 후 Sculpt" 안내 |
| 과제 내용 혼란 | curriculum.js와 assignment.md 체크리스트 다름 | 불일치 → **P1 수정 권고** | 수업 중 구두 안내 (curriculum.js 기준 체크리스트로 통일) |

---


## 3. 평가 정합성 (Assignment Alignment)

### 과제
> AI 도구로 3D 생성 + Sculpt Mode 수정 후 Before/After 스크린샷 2장 + AI 도구 이름 + 한줄 코멘트

### 학습 목표 ↔ 수업 Step ↔ 과제 매핑

| 학습 목표 | 수업 Step | 과제 검증 |
|----------|-----------|----------|
| AI 3D 도구 활용 | Meshy/Tripo 생성 실습 | AI 도구 이름 명시 |
| Blender 임포트 | 임포트 + 스케일 + Apply | Before 스크린샷 (원본 상태) |
| Sculpt Mode 수정 | Smooth, Grab, Draw 브러시 | After 스크린샷 (수정 후) |
| 워크플로우 이해 | 전체 흐름 | 한줄 코멘트 (한계점 + 느낀점) |

### ⚠️ SSOT 불일치 발견 (P1)

| 파일 | 과제 제목 | 주요 체크리스트 |
|------|----------|--------------|
| `curriculum.js` | 내 프로젝트 첫 3D 러프 | 무드보드 프롬프트 키워드, AI 원본 스크린샷, 메쉬 정리 후 스크린샷, 한 문장 선언, 완성 렌더 이미지, **완성 .blend 파일 저장 (Week 6에서 씀)** |
| `assignment.md` | AI 3D + Sculpt 수정 | Before(AI 원본) / After(Sculpt 수정) 이미지 2장, AI 도구 이름, 한줄 코멘트 |
| `slides.md` | 과제 안내 (Before/After) | 이미지 2장, AI 도구 이름, 한줄 코멘트 |

**결론:** curriculum.js 체크리스트가 더 구체적이며 "Week 6에서 이 파일을 씁니다" 연결이 포함되어 있음. assignment.md+slides.md는 더 간략함. curriculum.js 기준이 더 좋음 → assignment.md+slides.md를 curriculum.js 수준으로 업그레이드 필요. P1 수정.

### 채점 기준
- AI 도구 활용 (30%) — 적절한 프롬프트, 도구 효과적 사용
- Sculpt 수정 품질 (40%) — 표면 정리, 형태 개선 정도
- 창의성 (30%) — 독창적 컨셉, AI 한계를 넘은 수정 시도

---

## 4. 의존성 체크

### 전주차 연결
- Week 1 무드보드 컨셉 이미지 → Tripo AI Image to 3D 입력 재료 → **Week 1 파일 필요** ⚠️
- Week 3-4 모델링 기법 → AI 모델 Edit Mode 수정 시 활용
- Apply Transform (Ctrl+A) → AI 모델 임포트 후 필수 단계 ✅ (lecture-note에 명시)

### 다음 주차 연결 (Week 6: Material & Shader Node)
- Week 5 완성 .blend 파일 → **Week 6 Step 1 Remesh + Material 실습에 직접 사용** → 반드시 저장 안내 필요
- Week 5는 AI 메쉬를 Mesh Cleaner + Decimate로 기본 정리만 → **Week 6 Step 1에서 Voxel Remesh / Quad Remesh / QRemeshify 심화**
- **curriculum.js에는 "Week 6 Material 실습에서 이 파일을 씁니다" 명시되어 있으나 assignment.md+slides.md에는 없음** → P1 불일치

---

## 5. 콘텐츠 공백 (Gap Analysis)

### 검토 완료 항목
- [x] AI 3D 도구 3종 비교 → lecture-note 표 있음 ✅
- [x] GLB 임포트 스케일 주의 → lecture-note에 명시 ✅
- [x] Sculpt 브러시 기본 4종 설명 → lecture-note에 포함 ✅
- [x] Dyntopo → Sculpt 브러시 심화 step에 포함 (2026-04-05 이동) ✅
- [x] Week 1 컨셉 이미지 활용 (Tripo Image to 3D) → assignment.md에 언급 ✅

### 추가 필요 항목
- [ ] **assignment.md + slides.md 업그레이드** (P1): curriculum.js 체크리스트(무드보드 키워드, .blend 저장, Week 6 연결 안내) 수준으로 내용 보강.
- [ ] **Week 6 파일 저장 체크리스트 강조** (P1): 마지막 과제 섹션에 "Week 6 Material 실습에서 이 파일을 씁니다 — 반드시 저장" 강조.
- [ ] **AI 생성 대기 시간 활용 안내** (P1): 수업 진행 가이드에 "Meshy 대기 중 Tripo Image to 3D 준비" 병렬 작업 흐름 명시.
- [ ] **Decimate 사용 가이드** (P2): 고폴리 AI 모델 버벅임 시 Decimate Modifier로 경량화하는 방법 supplement 추가.

---

## 6. Rubric 자가 평가 (1-5점)

> Content Lead 리뷰 — 2026-04-05

| 차원 | 점수 | 근거 |
|------|------|------|
| 1. 학습 목표 구체성 | 4 | AI 생성 → 임포트 → Sculpt 수정 흐름이 명확. Remesh 필요성 설명 있음. MCP는 "선택"으로 포지셔닝 명확. |
| 2. 전제 명시 | 4 | Week 1 무드보드 이미지, Week 3-4 모델링 기법 복습이 lecture-note에 명시됨. Week 4 파일 저장 전제가 암묵적이나 수업 흐름에서 자연스럽게 연결. |
| 3. Stuck Map 완성도 | 3 | AI 도구 크레딧 소진, GLB 스케일, Sculpt 브러시 주요 막힘 커버됨. 고폴리 모델 버벅임 대응, 파츠 분리 모델 처리 가이드 보완 필요. |
| 4. 평가 정합성 | 3 | curriculum.js가 assignment.md보다 더 구체적이고 Week 6 연결 안내 포함. 방향 불일치는 아니나 세부 체크리스트 통일 필요. P1 수준. |

**총점: 14/20**

---

## 7. 개선 액션

### P0 — 즉시 반영 필요

- 없음 (Week 5는 기존 보강 완료 주차, 정합성 비교적 양호)

### P1 — 이번 주 내 반영 권고

- [ ] **assignment.md 체크리스트 보강:** curriculum.js 기준으로 "무드보드 프롬프트 키워드", "완성 .blend 파일 저장 — Week 6 Step 1 Remesh + Material 실습에서 씁니다" 항목 추가.
- [ ] **slides.md 과제 안내 업데이트:** 동일 내용 추가.
- [ ] **AI 생성 대기 시간 활용 가이드:** lecture-note 강사 노트에 "Meshy 대기 중 Week 1 컨셉 이미지 준비 유도" 안내 추가.
- [x] **Remesh 심화 Week 6으로 이동 (2026-04-05):** "Remesh·Dyntopo·Decimate" 및 "외부 플러그인 & 메쉬 정리 도구" Step 삭제. Dyntopo는 Sculpt 브러시 심화 step에 유지.

### P2 — 차기 주차 리뷰 전 반영

- [ ] lecture-note.md에서 Remesh 섹션을 "기본 정리만" 수준으로 축약, Week 6 Remesh 심화 참고 안내 추가.
- [ ] 채점 기준 slides.md ↔ assignment.md 일치 확인 (현재 일치함).
