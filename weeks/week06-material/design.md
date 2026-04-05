# Week 6 기획 심화 (Design Doc)

> **목적:** curriculum.js의 콘텐츠가 아닌, 수업 기획 자체의 질을 검증하기 위한 문서.
> Content Lead + CPO가 Rubric 기반으로 주차별 기획을 심층 리뷰할 때 사용한다.

**주제:** Material & Shader Node
**수업일:** 2026-04-07 (화) 10:00-15:00
**강의실:** 60주년관 908호
**Status:** active (현재 주차)
**리뷰 완료일:** 2026-04-05

---

## 1. Student Journey (학생 여정)

### 시작 상태 (Week 5 종료 시점)
- AI 3D 생성 + Sculpting으로 로봇 모델 형태 완성
- Mesh 정리 (Decimate, Mesh Cleaner) 적용된 상태
- 색상 없는 회색(Default) 상태

### 끝 상태 (Week 6 종료 시점)
- [ ] 로봇에 최소 3개 부위 Material 할당 가능
- [ ] Principled BSDF의 Metallic/Roughness 슬라이더 자유 조작
- [ ] Shader Node Editor에서 Noise Texture 1개 연결 성공
- [ ] Thin Film Iridescence로 무지개빛 효과 1회 구현
- [ ] Viewport Shading 4모드 전환 (Z 키)

### 핵심 전환점 ("아하!" 모먼트)
1. **Metallic 슬라이더를 0→1로 움직일 때** — 플라스틱에서 금속으로 즉각 바뀜
2. **Noise Texture를 Base Color에 연결할 때** — 깨끗한 표면에 질감이 입혀짐
3. **Z 키로 Rendered 모드 진입** — 작업물이 최종 결과로 보이는 순간

---

## 2. Stuck Map (예상 막힘 지점)

| Step | 예상 막힘 | 원인 | 대응 |
|------|----------|------|------|
| Step 1 | Material 슬롯이 보이지 않음 | Properties 패널 축소됨 | 스크린샷 supplement 카드 |
| Step 1 | Assign 버튼 비활성 | Edit Mode 미진입 / Face 미선택 | 체크리스트 (Tab → Face select → Assign) |
| Step 2 | 변화가 안 보임 | Viewport가 Solid 모드 | Step 5 선행 또는 "Z를 눌러 Material Preview로" 힌트 |
| Step 2 | Transmission 올려도 투명 안 됨 | Blend Mode 미설정 | supplement 카드: "투명 재질 설정 3단계" |
| Step 2 | 유리가 검게 보임 | 주변 환경(HDRI) 없음 | "지금은 HDRI 없으니 Material Preview에서 확인" 안내 |
| Step 2 | Emission이 Material Preview에서 약하게 보임 | 렌더러 차이 | "Rendered 모드에서 Bloom 켜야 빛남" 명시 |
| Step 3 | Node Editor 창이 안 열림 | 기본 Layout에는 숨김 | "Shading 워크스페이스 탭 클릭" 안내 |
| Step 3 | 노드 연결선 안 이어짐 | 드래그 시작점이 socket 밖 | GIF supplement |
| Step 3 | 노드 연결이 안 됨 | 소켓 타입 불일치 (Color ≠ Value) | "소켓 색이 같은 것끼리: 노란색↔노란색, 회색↔회색" 안내 |
| Step 4 | Noise Texture 적용해도 밋밋 | Scale/Detail 기본값 | 추천 값 preset 제시 (Scale 5, Detail 2) |
| Step 5 | Rendered 모드에서 검게 보임 | 조명 없음 (Week 9 내용) | "지금은 Material Preview가 정답" 명확히 |
| Thin Film | Thin Film 효과가 안 보임 | Metallic이 1이 아님 | "Thin Film은 Metallic=1 재질에서만 두드러짐" 명시 |

---

## 3. 시간 배분 (5시간 수업)

| 시간 | 내용 | 비율 |
|------|------|------|
| 10:00-10:15 | 인트로, 지난주 복습, 오늘 목표 | 5% |
| 10:15-10:45 | 이론 강의 (Material, PBR, Principled BSDF) | 10% |
| 10:45-11:30 | Step 1-2 실습 (Material 할당 + BSDF 탐색) | 15% |
| 11:30-12:00 | 질의응답 + 트러블슈팅 | 10% |
| 12:00-13:00 | **점심** | - |
| 13:00-13:45 | Step 3 실습 (Shader Node Editor) | 15% |
| 13:45-14:15 | Step 4 실습 (Noise Texture) | 10% |
| 14:15-14:35 | Step 5 실습 (Viewport Shading) | 7% |
| 14:35-14:50 | Thin Film 5.0 신기능 데모 + 로봇 적용 | 5% |
| 14:50-15:00 | 과제 안내 + 마무리 | 3% |

**실습 : 강의 비율** = 약 60% : 40% (목표 달성)

> ⚠️ **현실성 주의:** Poly Haven 텍스처 활용(lecture-note Step: 15분)은 시간 계획에 없음. 이 섹션은 **선택 심화 자료**로 명시 변경 권고. Thin Film은 15분으로 매우 타이트 — 강사 데모 중심으로 진행하고 학생 적용은 과제로 유도.

---

## 4. 평가 정합성 (Assignment Alignment)

### 과제
> 로봇/캐릭터에 3가지 이상 서로 다른 재질 적용 후 렌더 이미지 제출

### 학습 목표 ↔ 수업 Step ↔ 과제 매핑

| 학습 목표 | 수업 Step | 과제 검증 |
|----------|-----------|----------|
| Material 생성/할당 | Step 1 | 최소 3개 Material 슬롯, 부위별 Assign 확인 |
| Principled BSDF 이해 | Step 2 | 금속/플라스틱/유리 각 1개 이상 (Metallic/Roughness 차이 시각 확인) |
| Shader Node Editor 사용 | Step 3-4 | 최소 1개 부위에 Noise 또는 Texture 노드 연결 스크린샷 |
| Thin Film Iridescence 5.0 | 이론+Thin Film 데모 | Bonus: 금속 파츠에 Thin Film 적용 시 가점 |

### 채점 기준
- Material 활용 다양성 (40%) — 3가지 이상, 재질 간 차이가 시각적으로 명확
- 완성도 (30%) — Material 할당 정확, 파라미터 조절 적절
- 창의성 (30%) — 재질 조합이 로봇 컨셉과 어울리는가

---

## 5. 의존성 체크

### 전주차 연결
- Week 5 완료 모델 필요 → **미완성 학생 대응**: Primitive(Cube) 대체 가능 명시됨 ✅
- Mesh 정리 (Normal, 겹침) 필요 → lecture-note에 언급 있음 ✅
- **Eevee 렌더러 설정** → 투명도/Emission 동작에 영향. 수업 시작 시 Eevee 확인 필요 ⚠️ (추가 필요)
- **Blender 5.0 버전 확인** → Thin Film은 5.0 전용. 버전 확인 안내 없음 ⚠️ (추가 필요)

### 다음 주차 연결 (Week 7: UV + AI Texture)
- Material 할당 → UV 좌표 필요
- Texture 노드 기초 → AI Texture 생성/적용으로 확장

---

## 6. 콘텐츠 공백 (Gap Analysis)

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

## 7. Rubric 자가 평가 (1-5점)

> Content Lead 리뷰 — 2026-04-05

| 차원 | 점수 | 근거 |
|------|------|------|
| 1. 학습 목표 구체성 | 4 | 끝 상태 기준이 명확하고 측정 가능. 단, "Specular 자유 조작"은 실제 수업에서 강조점이 아니므로 Metallic/Roughness로 교체. |
| 2. 전제 명시 | 3 | Week 5 연결 및 Primitive 대체 안 좋음. Eevee 렌더러 설정·Blender 5.0 버전 확인이 누락되어 Thin Film/투명 재질 실습 시 오류 발생 가능. |
| 3. Stuck Map 완성도 | 3 | 8개 항목으로 좋은 출발. 유리 검은 화면, Emission 모드 차이, 노드 소켓 타입 불일치, Thin Film 미동작(Metallic 미설정) 4개 추가 필요. |
| 4. 시간 배분 현실성 | 3 | 실습:강의 60:40 목표 달성. Poly Haven(15분)이 공식 플랜에 없어 강사가 즉흥 진행 위험. Thin Film 15분은 데모 중심으로만 가능. 기술 이슈 버퍼 없음. |
| 5. 평가 정합성 | 2 | **Major mismatch:** curriculum.js 과제("구 5개 샘플러")와 assignment.md·design.md·slides("로봇 3가지 재질")가 불일치. 채점 기준도 두 문서 간 항목이 다름. P0 수정 필요. |

**총점: 15/25**

---

## 8. 개선 액션

### P0 — 수업 전 즉시 반영 필요 (2026-04-07 이전)

- [x] **과제 내용 통일** (curriculum.js 수정 완료): "구 5개 샘플러" → 로봇/캐릭터 기반 3가지 이상 재질 과제로 통일. checklist도 assignment.md 기준으로 일치시킴.
- [x] **전제 조건 추가** (lecture-note.md 수업 시작 체크리스트): Blender 5.0 버전 확인, Eevee 렌더러 확인, Material Preview 모드 확인 3개 항목 추가 완료 (2026-04-05).

### P1 — 이번 주 내 반영 권고

- [ ] **Stuck Map 4항목 추가**: 유리 검은 화면(HDRI 없음), Emission 모드 차이, 노드 소켓 타입 불일치, Thin Film 미동작(Metallic=1 필요). → Stuck Map 섹션 업데이트 완료(이 문서).
- [ ] **Poly Haven 섹션 위상 정리**: lecture-note에서 "선택 심화 (시간 있을 때)" 레이블 추가. 시간 계획에서 제거하거나 explore 섹션으로 이동.
- [ ] **Thin Film 예시 이미지 추가**: assets/images/week06/thin-film-example.png 추가 또는 외부 링크 제공.

### P2 — 차기 주차 리뷰 전 반영

- [ ] 학습 목표에서 "Specular 슬라이더 자유 조작" → "Metallic/Roughness로 금속·플라스틱·유리 재질 구현" 로 교체 (실제 수업 강조점 반영).
- [ ] 채점 기준 slides.md ↔ assignment.md 동일하게 유지 (현재 동일하나 design.md 기준과 약간 다름 — 이 문서가 기준).
