# Week 6 기획 심화 (Design Doc)

> **목적:** curriculum.js의 콘텐츠가 아닌, 수업 기획 자체의 질을 검증하기 위한 문서.
> Content Lead + CPO가 Rubric 기반으로 주차별 기획을 심층 리뷰할 때 사용한다.

**주제:** AI 메쉬 Remesh 정리 + Material & Shader Node
**수업일:** 2026-04-07 (화) 10:00-15:00
**강의실:** 60주년관 908호
**Status:** active (현재 주차)
**리뷰 완료일:** 2026-04-05

---

## 1. Student Journey (학생 여정)

### 시작 상태 (Week 5 종료 시점)
- AI 3D 생성 + Sculpting으로 로봇 모델 형태 완성
- Mesh 기본 정리 (Decimate/Mesh Cleaner 간략 체험) 상태 — **토폴로지 심화 정리는 오늘 Step 1에서**
- 색상 없는 회색(Default) 상태

### 끝 상태 (Week 6 종료 시점)
- [ ] Remesh(Voxel/Quad/QRemeshify/Mesh Cleaner 2)로 AI 메쉬를 Material 적용 가능한 상태로 정리
- [ ] Remesh 전후 폴리곤 수 Statistics 비교 스크린샷 제출
- [ ] 로봇에 최소 3개 부위 Material 할당 가능
- [ ] Principled BSDF의 Metallic/Roughness 슬라이더 자유 조작
- [ ] Shader Node Editor에서 Noise Texture 1개 연결 성공
- [ ] Thin Film Iridescence로 무지개빛 효과 1회 구현
- [ ] Viewport Shading 4모드 전환 (Z 키)

### 핵심 전환점 ("아하!" 모먼트)
1. **Remesh 후 Statistics로 폴리곤 수 차이를 확인할 때** — "AI 메쉬가 이렇게 지저분했구나, 이제 작업 가능해졌다"
2. **Metallic 슬라이더를 0→1로 움직일 때** — 플라스틱에서 금속으로 즉각 바뀜
3. **Noise Texture를 Base Color에 연결할 때** — 깨끗한 표면에 질감이 입혀짐
4. **Z 키로 Rendered 모드 진입** — 작업물이 최종 결과로 보이는 순간

---

## 2. Stuck Map (예상 막힘 지점)

| Step | 예상 막힘 | 원인 | 대응 |
|------|----------|------|------|
| Step 1 (Remesh) | Remesh 후 쉐이더 깨짐 | 노멀 방향 문제 | "Mesh Cleaner 2 재실행 또는 Edit Mode → Normals → Recalculate Outside" |
| Step 1 (Remesh) | Decimate 후 형태 붕괴 | Ratio 너무 낮음 | "0.3~0.5에서 멈추기, Apply 전에 Preview 확인" |
| Step 1 (Remesh) | Before/After 비교 불가 | 앵글이 달라짐 | "Numpad 1 고정 앵글로 Before/After 동일 앵글 촬영" |
| Step 2 (Material) | Material 슬롯이 보이지 않음 | Properties 패널 축소됨 | 스크린샷 supplement 카드 |
| Step 2 (Material) | Assign 버튼 비활성 | Edit Mode 미진입 / Face 미선택 | 체크리스트 (Tab → Face select → Assign) |
| Step 3 (BSDF) | 변화가 안 보임 | Viewport가 Solid 모드 | Step 6 선행 또는 "Z를 눌러 Material Preview로" 힌트 |
| Step 3 (BSDF) | Transmission 올려도 투명 안 됨 | Blend Mode 미설정 | supplement 카드: "투명 재질 설정 3단계" |
| Step 3 (BSDF) | 유리가 검게 보임 | 주변 환경(HDRI) 없음 | "지금은 HDRI 없으니 Material Preview에서 확인" 안내 |
| Step 3 (BSDF) | Emission이 Material Preview에서 약하게 보임 | 렌더러 차이 | "Rendered 모드에서 Bloom 켜야 빛남" 명시 |
| Step 4 (Shader) | Node Editor 창이 안 열림 | 기본 Layout에는 숨김 | "Shading 워크스페이스 탭 클릭" 안내 |
| Step 4 (Shader) | 노드 연결선 안 이어짐 | 드래그 시작점이 socket 밖 | GIF supplement |
| Step 4 (Shader) | 노드 연결이 안 됨 | 소켓 타입 불일치 (Color ≠ Value) | "소켓 색이 같은 것끼리: 노란색↔노란색, 회색↔회색" 안내 |
| Step 5 (Texture) | Noise Texture 적용해도 밋밋 | Scale/Detail 기본값 | 추천 값 preset 제시 (Scale 5, Detail 2) |
| Step 6 (Viewport) | Rendered 모드에서 검게 보임 | 조명 없음 (Week 9 내용) | "지금은 Material Preview가 정답" 명확히 |
| Thin Film | Thin Film 효과가 안 보임 | Metallic이 1이 아님 | "Thin Film은 Metallic=1 재질에서만 두드러짐" 명시 |

---


## 3. 평가 정합성 (Assignment Alignment)

### 과제
> 로봇/캐릭터에 3가지 이상 서로 다른 재질 적용 후 렌더 이미지 제출

### 학습 목표 ↔ 수업 Step ↔ 과제 매핑

| 학습 목표 | 수업 Step | 과제 검증 |
|----------|-----------|----------|
| AI 메쉬 Remesh 정리 | Step 1 | Remesh 전후 폴리곤 수 비교 스크린샷 (Statistics) |
| Material 생성/할당 | Step 2 | 최소 3개 Material 슬롯, 부위별 Assign 확인 |
| Principled BSDF 이해 | Step 3 | 금속/플라스틱/유리 각 1개 이상 (Metallic/Roughness 차이 시각 확인) |
| Shader Node Editor 사용 | Step 4-5 | 최소 1개 부위에 Noise 또는 Texture 노드 연결 스크린샷 |
| Thin Film Iridescence 5.0 | 이론+Thin Film 데모 | Bonus: 금속 파츠에 Thin Film 적용 시 가점 |

### 채점 기준
- Material 활용 다양성 (40%) — 3가지 이상, 재질 간 차이가 시각적으로 명확
- 완성도 (30%) — Material 할당 정확, 파라미터 조절 적절
- 창의성 (30%) — 재질 조합이 로봇 컨셉과 어울리는가

---

## 4. 의존성 체크

### 전주차 연결
- Week 5 완료 모델 필요 → **미완성 학생 대응**: Primitive(Cube) 대체 가능 명시됨 ✅
- **Week 6 Step 1에서 Remesh 심화 실시** (2026-04-05 변경): Voxel Remesh, Quad Remesh, QRemeshify, Mesh Cleaner 2 → Week 5에서 간략 체험 → Week 6에서 본격 학습
- Mesh 정리 (Normal, 겹침) 필요 → lecture-note에 언급 있음 ✅
- **Eevee 렌더러 설정** → 투명도/Emission 동작에 영향. 수업 시작 시 Eevee 확인 필요 ⚠️ (추가 필요)
- **Blender 5.0 버전 확인** → Thin Film은 5.0 전용. 버전 확인 안내 없음 ⚠️ (추가 필요)

### 다음 주차 연결 (Week 7: UV + AI Texture)
- Material 할당 → UV 좌표 필요
- Texture 노드 기초 → AI Texture 생성/적용으로 확장

---

## 5. 콘텐츠 공백 (Gap Analysis)

### 검토 완료 항목
- [x] supplement 카드 존재 여부 → lecture-note에 "흔한 실수" 섹션 있음. 별도 카드 불필요.
- [x] Poly Haven / BlenderKit 링크 최신성 → polyhaven.com 링크 정상
- [x] 5.0 신기능 Thin Film Iridescence 설명 → lecture-note에 Film Thickness nm 단위 설명 포함됨
- [x] Blend Mode (Alpha Blend vs Hashed) 차이 설명 → lecture-note 흔한 실수 #3에 포함됨
- [x] "자주 막히는 지점" 카드 → curriculum.js mistakes 섹션 및 lecture-note에 존재

### 추가 필요 항목
- [ ] 수업 시작 체크리스트: Eevee 렌더러 확인, Blender 5.0 버전 확인
- [ ] Thin Film 결과 예시 이미지 (효과 미리보기) — 현재 없음
- [ ] Poly Haven 섹션 → "선택 심화" 명시로 변경 (현재 실습 step으로 오인 가능)

---

## 6. Rubric 자가 평가 (1-5점)

> Content Lead 리뷰 — 2026-04-05

| 차원 | 점수 | 근거 |
|------|------|------|
| 1. 학습 목표 구체성 | 4 | Remesh 끝 상태 기준 추가로 명확성 향상. AI 메쉬 → Remesh → Material 흐름이 구체적으로 정의됨. |
| 2. 전제 명시 | 3 | Week 5 연결 및 Primitive 대체 안 좋음. Eevee 렌더러 설정·Blender 5.0 버전 확인이 누락되어 Thin Film/투명 재질 실습 시 오류 발생 가능. |
| 3. Stuck Map 완성도 | 4 | Remesh 3개 항목 추가 포함 총 14개 항목. 주요 막힘 커버. |
| 4. 평가 정합성 | 3 | Remesh Step 과제 검증 매핑 추가. curriculum.js ↔ assignment.md 체크리스트 통일 필요. |

**총점: 14/20** *(Remesh Step 1 신설로 이전 12점에서 향상)*

---

## 7. 개선 액션

### P0 — 수업 전 즉시 반영 필요 (2026-04-07 이전)

- [x] **과제 내용 통일** (curriculum.js 수정 완료): "구 5개 샘플러" → 로봇/캐릭터 기반 3가지 이상 재질 과제로 통일. checklist도 assignment.md 기준으로 일치시킴.
- [x] **전제 조건 추가** (lecture-note.md 수업 시작 체크리스트): Blender 5.0 버전 확인, Eevee 렌더러 확인, Material Preview 모드 확인 3개 항목 추가 완료 (2026-04-05).
- [x] **Week 6 Step 1 신설 — AI 메쉬 Remesh 정리** (2026-04-05): curriculum.js에 Voxel Remesh · Quad Remesh · Decimate · QRemeshify · Mesh Cleaner 2 포함한 Step 1 추가. design.md 반영 완료.

### P1 — 이번 주 내 반영 권고

- [ ] **Stuck Map 4항목 추가**: 유리 검은 화면(HDRI 없음), Emission 모드 차이, 노드 소켓 타입 불일치, Thin Film 미동작(Metallic=1 필요). → Stuck Map 섹션 업데이트 완료(이 문서).
- [ ] **Poly Haven 섹션 위상 정리**: lecture-note에서 "선택 심화 (시간 있을 때)" 레이블 추가. 시간 계획에서 제거하거나 explore 섹션으로 이동.
- [ ] **Thin Film 예시 이미지 추가**: assets/images/week06/thin-film-example.png 추가 또는 외부 링크 제공.

### P2 — 차기 주차 리뷰 전 반영

- [ ] 학습 목표에서 "Specular 슬라이더 자유 조작" → "Metallic/Roughness로 금속·플라스틱·유리 재질 구현" 로 교체 (실제 수업 강조점 반영).
- [ ] 채점 기준 slides.md ↔ assignment.md 동일하게 유지 (현재 동일하나 design.md 기준과 약간 다름 — 이 문서가 기준).
