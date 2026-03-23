# Week 4 카드 품질 업그레이드 + W4-W5 혼합 Design

> Created: 2026-03-23
> Status: Approved
> Branch: main

## Context

- W4부터 커리큘럼을 따라가되 자기 모델에 적용하는 학생들이 있음 (병행 진행)
- W5의 AI 3D 생성 + Decimate를 W4에 미리 노출시켜 더 많은 도구를 제공
- W8 중간고사까지 역산하면, AI 도구를 1주 일찍 주는 게 학생들에게 유리
- W5의 sculpt + remesh 아크는 유지 (hard-surface vs organic 테마 분리)

## Decision: Approach B — Decimate + AI 미리보기를 W4에 추가

### Why
1. Decimate는 "정리" 도구 → W4 "디테일 & 정리" 테마에 자연스럽게 부합
2. AI 파츠 생성 → Decimate 경량화 → Boolean 합치기 = W4 기법만으로 완결
3. Sculpt/Remesh는 유기체 테마 → W5에 유지하는 게 학습 아크에 맞음
4. W8 중간고사 전에 AI 도구를 1주 일찍 제공

### What changes

**W4 커리큘럼 (curriculum.json):**
- 기존 스텝 1-4 유지
- 신규 스텝 5 삽입: "AI 파츠 생성 & 메시 정리"
  - AI 3D 생성 체험 (Meshy/Tripo)
  - Decimate로 AI 메시 경량화
  - Boolean으로 자기 모델에 합치기
  - showme: decimate-modifier
- 기존 스텝 5(마무리 점검) → 스텝 6으로 이동

**W5 영향 (최소 변경):**
- AI 3D 생성 체험 스텝은 W4에도 존재하지만, W5에서 "AI + Sculpt 하이브리드"로 심화
- decimate-modifier showme 참조는 W4와 W5 모두에서 가능 (중복 허용)
- sculpt-basics, remesh-modifier는 W5 그대로 유지

## Implementation Phases

### Phase 1: _supplements.json 보충 콘텐츠 (기존 plan 유지)
- Task 1: 핵심 4개 (boolean, bevel, weighted-normal, join-separate)
- Task 2: 보조 14개 (edge-split, triangulate, weld, build, decimate, remesh, screw, skin, wireframe, mask, multiresolution, volume-to-mesh, curve-to-tube, scatter-on-surface)

### Phase 2: 핵심 카드 HTML 보강 (기존 plan 유지)
- Task 3: boolean-modifier.html — 원인→결과 + 흔한 실수
- Task 4: bevel-modifier.html — 원인→결과 + 흔한 실수 + 쓰지 말 것
- Task 5: weighted-normal.html — 개념 보강 + 원인→결과 + 흔한 실수

### Phase 3: 커리큘럼 변경 (신규)
- Task 7: curriculum.json W4에 스텝 5 추가 (AI 파츠 + Decimate)
- Task 8: W5 순서 정리 (decimate 참조 위치 확인, AI 스텝 심화로 전환)

### Phase 4: 전체 검증
- Task 9: JSON 유효성, HTML 구문, 시각 확인

## References
- 기존 카드 품질 plan: docs/plans/2026-03-23-week4-card-quality-upgrade.md
- 커리큘럼 소스: course-site/data/curriculum.json
- 보충 콘텐츠: course-site/assets/showme/_supplements.json
