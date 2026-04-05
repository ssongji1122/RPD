# Week 6 기획 감사 확장 리포트

**감사일:** 2026-04-05
**감사 대상:** Week 6 (Material & Shader Node) — 연속성 · Notion 정합 · 아카이브 사이트
**수업일:** 2026-04-07 (화)
**감사자:** Content Lead (RPD-1 확장)

---

## 1. 이전 주차 연속성 분석 (Week 1-5 → Week 6)

### 1-1. 학습 진행 요약

| Week | 제목 | 핵심 스킬 전달 |
|------|------|----------------|
| 1 | 수업 시작 준비 | Mixboard 컨셉 설정. Blender 미설치. 실습 없음. |
| 2 | Blender 인터페이스 · 기초 | G/R/S 변형, Extrude/Bevel/LoopCut. Material Preview 첫 언급(Week2 Step5). |
| 3 | 기초 모델링 1 — Edit + Modifier | Mirror/SubD/Solidify/Array/Boolean, Bevel Modifier, Weighted Normal, Decimate(선택). |
| 4 | 기초 모델링 2 — 로봇 조립 | 몸통/팔다리/관절 조립, Duplicate/Array, Join/Separate/Apply. |
| 5 | AI 3D 생성 + Sculpting | AI 모델 생성, Sculpt 수정, Remesh/Decimate, Mesh Cleaner. |
| **6** | **Material & Shader Node** | **Material 할당, Principled BSDF, Shader Node Editor, Thin Film.** |

### 1-2. Week 6 전제 조건 충족 여부

| 전제 | 소스 주차 | 충족도 | 비고 |
|------|----------|--------|------|
| 로봇 모델 확보 | Week 4-5 | ✅ | Primitive 대체 안 명시됨 (W6 lecture-note에 언급) |
| Mesh 정리 (Decimate) | Week 3(선택), Week 5 | ✅ | Week 5에 Decimate + Remesh 핵심으로 다룸 |
| Weighted Normal / Normal 개념 | Week 3 | ✅ | Week 3에서 Bevel + Weighted Normal 쌍으로 필수 처리 |
| Viewport Shading 모드 | Week 2 | ⚠️ | Week 2 Step5에서 짧게 언급. 복습 없이 Week 6에서 전체 4모드 강조 — 주의 |
| Eevee 렌더러 설정 | 없음 | ❌ | **누락.** Eevee는 Week 1부터 기본이지만 명시적 선택/확인 스텝 없음. 투명도·Emission 동작이 달라져 Week 6 혼란 유발 가능. |
| Shader Node 개념 | 없음 | ⚠️ | Week 6에서 첫 등장 — Cold 도입. 기대 수준 낮게 설정 필요. |
| Blender 5.0 버전 확인 | 없음 | ❌ | Thin Film은 5.0 전용. 버전 불일치 시 섹션 전체 실패. |

**핵심 전제 위험:** Eevee 렌더러 + Blender 5.0 버전 확인이 수업 시작 전 명시적으로 필요.

### 1-3. Mesh 정리 강조도 추적

- **Week 3:** Decimate은 "선택" 항목. Non-Manifold(Merge by Distance) 개념 1회 언급.
- **Week 5:** Decimate Modifier가 핵심 실습 (Ratio 0.1~0.3), Remesh 강조, Mesh Cleaner 언급.
- **결론:** Week 5가 실질적 Mesh 정리 주차. Week 6 기준 "Mesh 정리 완료" 전제는 Week 5 과제 완료자에게는 유효.

---

## 2. Notion ↔ 사이트 정합성

### 2-1. SSOT 아키텍처 현황

- **계획 (2026-03-31):** Notion을 SSOT로, curriculum.js를 generated file로 전환. overrides.json으로 코드 에셋(image/showme/status) 분리.
- **현실:** 계획 미완성. curriculum.js/curriculum.json이 직접 수정되고 있음. NOTION_TOKEN 없이 운영 중.

### 2-2. Week 6 과제 불일치 (P0, 이번 세션에서 수정됨)

| 파일 | 수정 전 | 수정 후 |
|------|--------|--------|
| `course-site/data/curriculum.js` | "재질 스타일 샘플러" (구 5개) | "로봇 재질 적용" (3가지 이상) ✅ |
| `course-site/data/curriculum.json` | "재질 스타일 샘플러" (구 5개) | "로봇 재질 적용" (3가지 이상) ✅ |
| `weeks/week06-material/assignment.md` | 로봇 기반 (올바름) | 변경 없음 ✅ |
| `weeks/week06-material/slides.md` | 로봇 기반 (올바름) | 변경 없음 ✅ |
| `course-site/data/curriculum-notion.json` | "재질 스타일 샘플러" (구 5개) | **미수정 ⚠️** NOTION_TOKEN 필요 |

> **위험:** curriculum-notion.json이 Notion 실제 값을 반영. 다음 `python3 tools/notion-sync.py`가 실행되면 curriculum-notion.json → curriculum.js/json 덮어쓰기 발생 가능. overrides.json의 `assignment` 필드로 잠금 권고.

### 2-3. Notion ↔ curriculum.js 주요 불일치 항목

아래 항목들은 curriculum-notion.json과 curriculum.js/json 간 차이:

| 주차 | 필드 | curriculum-notion | curriculum.js | 판단 |
|------|------|-------------------|---------------|------|
| W6 | assignment.title | 재질 스타일 샘플러 | 로봇 재질 적용 | curriculum.js가 정답 — Notion 업데이트 필요 |
| W6 | assignment.checklist | [] (빈 배열) | 3개 항목 | curriculum.js가 정답 |

---

## 3. 아카이브 사이트 점검 (course-site/)

### 3-1. Week 6 에셋 누락

| 에셋 | 경로 | 상태 |
|------|------|------|
| Step 4 이미지 | `assets/images/week06/texture-node.png` | ❌ 없음 |
| Step 5 이미지 | `assets/images/week06/shading-modes.png` | ❌ 없음 |
| Step 4 showme | (없음) | ❌ 미연결 |
| Step 5 showme | (없음, `viewport-shading.html` 카드 존재) | ⚠️ 연결 가능 |

### 3-2. Week 5 showme 미연결 항목 (Week 6 연속성에 영향)

| Step 제목 | showme 상태 |
|-----------|------------|
| Addon/Extension 설치 및 활성화 | ❌ 없음 |
| LoopTools · Bool Tool 활용 | ❌ 없음 |
| BlenderKit 에셋 라이브러리 | ❌ 없음 |
| 외부 플러그인 & 메쉬 정리 도구 | ❌ 없음 |
| AI 메쉬 정리 실전 | ❌ 없음 |

> **맥락:** Week 5 Addon/BlenderKit/Mesh Cleaner showme 카드 부재는 Week 6 시작 전 보충할 방법이 없음. 학생이 복습 시 참조 불가.

### 3-3. 톤&매너 일관성

| 이슈 | 주차/Step | 내용 |
|------|----------|------|
| copy 너무 짧음 | Week 1 "Blender 설치" | 27자 — 감성 카피 없음 |
| copy 너무 짧음 | Week 2 "프리퍼런스 세팅" | 23자 — 설명이 아닌 제목 수준 |
| Week 6 전반 | 전체 | 다른 주차와 동일한 반말체·2인칭 유지 ✅ |
| image 플레이스홀더 | Week 6 Step 4-5 | 이미지 없으면 카드 레이아웃 빈칸 노출 가능 |

---

## 4. 즉시 대응 항목 요약

### P0 (수업 전, 2026-04-07)
- [x] curriculum.js 과제 수정 완료
- [x] curriculum.json 과제 수정 완료
- [ ] Notion Week 6 과제 업데이트 (NOTION_TOKEN 필요 — 사람 손)
- [ ] overrides.json Week 6에 `assignment` 잠금 추가 (sync 회귀 방지)

### P1 (이번 주)
- [ ] Week 6 Step 4-5 이미지 생성 (texture-node.png, shading-modes.png)
- [ ] Week 6 Step 5에 viewport-shading showme 연결
- [ ] Week 5 누락 showme 5개 생성 또는 기존 카드 연결

### P2 (차기 감사 전)
- [ ] Week 1 "Blender 설치", Week 2 "프리퍼런스 세팅" copy 보강
- [ ] 수업 시작 체크리스트 슬라이드 추가: Eevee 확인, Blender 5.0 확인
- [ ] Notion SSOT 완성: curriculum-notion.json 재생성 경로 정상화

---

## 5. 파일럿 감사 결론

**Week 6 기획 품질: 12/20 (60%)**

전반적으로 학습 목표는 명확하고 Stuck Map은 실용적이나, 두 개의 구조적 문제가 발견되었다:

1. **과제 파편화**: curriculum.js·assignment.md·slides.md가 서로 다른 과제를 기술하고 있었음. 이번 세션에서 P0 수정 완료.
2. **Notion 미동기화**: curriculum-notion.json이 아직 구 과제를 보유 — 다음 sync에 회귀 위험.

이 패턴은 다른 주차에도 잠재적으로 존재할 가능성이 높다. **Week 3-5 순차 감사 파일럿 확장을 권고.**
