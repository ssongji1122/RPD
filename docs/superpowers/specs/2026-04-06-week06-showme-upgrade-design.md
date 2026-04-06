# Week 06 ShowMe 카드 리디자인

**날짜:** 2026-04-06
**범위:** 6주차 ShowMe 카드 전체 업그레이드 + 신규 카드 1개
**상태:** Approved

---

## 1. 목표

6주차(Material & Shader) ShowMe 카드를 표준화하고, 카드 간 학습 경로를 연결하여 Material → BSDF → Shader Editor → Texture Nodes 순서의 자연스러운 학습 흐름을 만든다.

## 2. 대상 카드

| # | 카드 ID | 작업 | 현재 상태 |
|---|---------|------|----------|
| 1 | `remesh-decimate` | 신규 완료 | ✅ 완료 |
| 2 | `material-basics` | 업그레이드 완료 + 학습경로 링크 추가 | ✅ 완료 (링크만 추가) |
| 3 | `principled-bsdf` | 전체 업그레이드 | 🔧 대상 |
| 4 | `shader-editor` | 전체 업그레이드 | 🔧 대상 |
| 5 | `texture-nodes` | 신규 생성 | 🆕 대상 |

## 3. 공통 표준화 규칙

- **탭 2 라벨:** `interaction` (현재 `시각적 비교` → 변경)
- **컨트롤 스타일:** `modifier-panel` (`.mp-row` + range slider + `.mp-value`)
- **퀴즈:** 5문제, 75% 통과, 표준 `initQuiz()` + `postMessage`
- **doc-ref:** Blender 공식 문서 링크 필수
- **모바일:** `@media (max-width: 600px)` 반응형
- **터치:** `touchend` with `preventDefault` 지원

## 4. 학습 경로 연결

각 카드의 "언제 쓰나요?" 탭 하단에 `tip-box` 스타일로 "다음 단계" 안내 1줄 추가. 카드 자체는 독립적으로 완결.

```
material-basics  →  "더 정밀한 재질 표현이 필요할 때 → Principled BSDF"
principled-bsdf  →  "노드를 직접 연결해 복합 재질을 만들고 싶을 때 → Shader Editor"
shader-editor    →  "이미지 텍스처를 매핑하고 싶을 때 → Texture Nodes"
```

## 5. 카드별 상세 설계

### 5.1 material-basics (링크 추가만)

- "언제 쓰나요?" 탭 하단에 학습경로 tip-box 추가
- 그 외 변경 없음 (이미 업그레이드 완료)

### 5.2 principled-bsdf (전체 업그레이드)

**탭 1 — 개념 이해**

개념 카드 4개:
1. **Principled BSDF란?** — Blender 만능 셰이더. Base Color/Metallic/Roughness 외에 고급 파라미터로 거의 모든 재질 표현 가능
2. **Subsurface (피하산란)** — 피부, 왁스, 우유처럼 빛이 표면 아래를 통과하는 재질. Subsurface Weight + Subsurface Color로 제어
3. **Emission & Transmission** — Emission: 자체 발광 (네온, LED). Transmission: 빛 투과 (유리, 액체). IOR로 굴절률 조절
4. **다른 BSDF도 있어요** — Principled Hair BSDF(머리카락 전용), Glass BSDF(단순 유리) 등 존재 안내. Week 6에서는 Principled BSDF에 집중

개념 시각화: 파라미터별 구체 3개 비교 (canvas)
- Subsurface 적용 (피부톤)
- Emission 적용 (발광 초록)
- Transmission 적용 (투명 유리)

단축키 목록: Shader Editor 열기, 파라미터 접근법

doc-ref: `https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/principled.html`

**탭 2 — interaction**

구체 렌더링 (material-basics의 Blinn-Phong 확장):
- 기존 Base Color, Metallic, Roughness 슬라이더 유지
- 추가: Subsurface, Emission, Transmission, IOR 슬라이더
- modifier-panel 스타일 컨트롤

프리셋 버튼 7개:
| 프리셋 | Base Color | Metal | Rough | Subsurface | Emission | Transmission | IOR |
|--------|-----------|-------|-------|------------|----------|-------------|-----|
| 피부 | #d4a07a | 0 | 0.5 | 0.5 | 0 | 0 | 1.45 |
| 유리 | #ffffff | 0 | 0.02 | 0 | 0 | 1.0 | 1.45 |
| 자동차 | #cc0000 | 0.9 | 0.15 | 0 | 0 | 0 | 1.5 |
| 네온 | #00ff88 | 0 | 0.5 | 0 | 1.0 | 0 | 1.45 |
| 대리석 | #f0e6d3 | 0 | 0.3 | 0.3 | 0 | 0 | 1.45 |
| 꿀 | #cc8800 | 0 | 0.2 | 0.6 | 0 | 0.4 | 1.5 |
| 벨벳 | #800020 | 0 | 0.95 | 0.3 | 0 | 0 | 1.45 |

프리셋 클릭 시: 슬라이더 자동 세팅 + mp-stat 영역에 "이 조합의 핵심: Subsurface로 피하산란 표현" 같은 설명 표시

**탭 3 — 언제 쓰나요?**

사용 사례 그리드 + 콤보 카드 + 학습경로 안내

**탭 4 — 퀴즈**

5문제: Subsurface 용도, Emission vs Transmission 차이, IOR 의미, 프리셋 파라미터 추론, Hair BSDF 존재 인지

### 5.3 shader-editor (전체 업그레이드)

**탭 1 — 개념 이해**

개념 카드 3개:
1. **노드란?** — Input → Processing → Output 구조. 소켓을 연결해서 데이터 흐름 생성
2. **Socket 색상 규칙** — 노랑=Color, 회색=Value(숫자), 보라=Vector(좌표), 초록=Shader. 같은 색끼리만 연결 가능 (자동 변환도 있음)
3. **필수 노드 3종** — Principled BSDF(메인 셰이더), Image Texture(이미지 입력), Mapping(좌표 변환)

개념 시각화: 노드 연결 다이어그램 (정적 canvas)
- Image Texture → Mapping → Principled BSDF → Material Output 연결 그림
- 소켓 색상 강조

doc-ref: `https://docs.blender.org/manual/en/latest/editors/shader_editor.html`

**탭 2 — interaction**

Mix Shader 데모:
- 두 재질(Shader A / Shader B)을 Mix Factor 슬라이더로 블렌딩
- canvas: 구체에 블렌딩 결과 실시간 렌더링
- modifier-panel: Shader A Color, Shader B Color, Mix Factor, Roughness A, Roughness B
- Mix Factor 0 = 완전 Shader A, 1 = 완전 Shader B

프리셋:
- 금속 + 녹 (부식 표현)
- 페인트 + 금속 (자동차 칩)
- 무광 + 광택 (표면 변화)

**탭 3 — 언제 쓰나요?**

사용 사례 + "다음 → Texture Nodes" 안내

**탭 4 — 퀴즈**

5문제: 노드 연결 방향, 소켓 색상 의미, Mix Shader 용도, Material Output 역할, Shader Editor 접근법

### 5.4 texture-nodes (신규)

**위젯 ID:** `texture-nodes`
**레지스트리:** `{ label: "Texture Nodes 이해", icon: "🧩", week: 6 }`

**탭 1 — 개념 이해**

개념 카드 3개:
1. **Texture Node란?** — 이미지 또는 절차적 패턴을 생성하는 노드. Image Texture(사진), Noise(잡음), Checker(체크무늬), Wave(파도) 등
2. **Mapping Node** — Texture의 위치(Location), 크기(Scale), 회전(Rotation) 제어. 이 노드 없이는 텍스처 위치/크기 조절 불가
3. **UV vs Generated 좌표계** — UV: 수동으로 펼친 좌표 (정밀), Generated: 오브젝트 기반 자동 좌표 (빠르지만 제한적)

개념 시각화: "같은 Checker 텍스처 + 다른 Scale" 비교 3단 (canvas)

doc-ref: `https://docs.blender.org/manual/en/latest/render/shader_nodes/textures/index.html`

**탭 2 — interaction**

텍스처 패턴 데모:
- canvas에 2D 패턴 실시간 렌더링
- 텍스처 타입 전환 버튼: Checker, Noise, Wave
- modifier-panel: Scale X, Scale Y, Rotation, Distortion (Wave용)
- 각 텍스처 타입별 파라미터가 다르게 활성화

canvas 렌더링 방식: 각 픽셀의 UV 좌표를 계산하여 절차적 텍스처 함수 적용
- Checker: `floor(u*scale) + floor(v*scale) % 2`
- Noise: Perlin noise 기반
- Wave: `sin(u*scale + distortion*noise(u,v))`

**탭 3 — 언제 쓰나요?**

Image Texture vs Procedural 비교 그리드:
- Image: 사진 기반, 리얼리즘, UV 필요, 해상도 제한
- Procedural: 수학 기반, 무한 해상도, UV 없어도 됨, 커스터마이즈 자유

콤보: Noise+ColorRamp(자연 패턴), Checker+Mapping(정밀 격자), Image+Mapping(사진 매핑)

**탭 4 — 퀴즈**

5문제: Procedural vs Image 차이, Mapping Node 역할, UV vs Generated, Scale 효과, Wave Distortion 용도

## 6. 커리큘럼 연결

`course-site/data/curriculum.js` Week 6 Step 5에 `showme: "texture-nodes"` 추가.

## 7. 레지스트리 변경

`_registry.js`에 추가:
```javascript
"texture-nodes": { label: "Texture Nodes 이해", icon: "🧩", week: 6 },
```

## 8. 구현 순서

1. `material-basics` — 학습경로 tip-box 1줄 추가
2. `principled-bsdf` — 전체 업그레이드
3. `shader-editor` — 전체 업그레이드
4. `texture-nodes` — 신규 생성
5. `_registry.js` — texture-nodes 등록
6. `curriculum.js` — Step 5 showme 필드 추가
7. 전체 프리뷰 검증
