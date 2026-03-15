# 커리큘럼 15주 전체 데이터 자동 채우기

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** curriculum.js의 shortcuts[], docs[], showme, image 빈 필드를 15주차 전체에 걸쳐 채우기

**Architecture:** 4단계 파이프라인. Phase A(shortcuts+docs)와 B(images)는 curriculum.js 직접 편집. Phase C(showme 카드)는 /showme 패턴으로 병렬 HTML 생성. Phase D는 curriculum.js showme 필드 연결.

**Tech Stack:** curriculum.js (JS-wrapped JSON), Playwright (스크린샷), standalone HTML (Show Me 카드)

---

## 현재 상태 요약

| 필드 | 채워진 주차 | 비어있는 주차 |
|------|------------|-------------|
| `shortcuts[]` | 3, 4 | 1, 2, 5~15 (13개) |
| `docs[]` | 3, 4, 5, 9 (일부) | 1, 2, 6, 7, 8, 10~15 (11개) |
| `showme` | 2, 3 | 1, 4~15 (13개) |
| `image` (누락 step) | — | W5-S1, W7-S3, W12-S1 |

---

## Task 1: Phase A — shortcuts[] 채우기 (11개 주차)

**Files:**
- Modify: `course-site/data/curriculum.js`

**대상 주차 및 추가할 단축키:**

### Week 1 — 수업 시작 준비
→ shortcuts 불필요 (설치 주차). 스킵.

### Week 2 — Blender 인터페이스 · 기초
```json
"shortcuts": [
  { "keys": "MMB Drag", "action": "Orbit (시점 회전)" },
  { "keys": "Shift + MMB", "action": "Pan (시점 이동)" },
  { "keys": "Scroll / Ctrl + MMB", "action": "Zoom (확대/축소)" },
  { "keys": "Numpad 1/3/7", "action": "Front/Right/Top View" },
  { "keys": "G / R / S", "action": "Grab / Rotate / Scale" },
  { "keys": "G + X/Y/Z", "action": "축 고정 이동" },
  { "keys": "Tab", "action": "Object ↔ Edit Mode 전환" }
]
```

### Week 5 — AI 3D + Sculpting
```json
"shortcuts": [
  { "keys": "Ctrl + Tab", "action": "Sculpt Mode 전환" },
  { "keys": "F", "action": "브러시 크기 조절" },
  { "keys": "Shift + F", "action": "브러시 강도 조절" },
  { "keys": "Ctrl", "action": "브러시 반전 (파내기)" },
  { "keys": "Shift", "action": "Smooth 브러시 임시 전환" },
  { "keys": "Ctrl + Z", "action": "되돌리기 (Sculpt에서 자주 사용)" }
]
```

### Week 6 — Material & Shader Node
```json
"shortcuts": [
  { "keys": "Z", "action": "Shading Mode 전환 (Wireframe/Solid/Material/Rendered)" },
  { "keys": "Shift + A", "action": "Shader Editor에서 노드 추가" },
  { "keys": "Ctrl + Shift + Click", "action": "Viewer Node 연결 (미리보기)" },
  { "keys": "Ctrl + T", "action": "Texture Mapping 노드 자동 연결" },
  { "keys": "M", "action": "Shader Editor에서 Frame 그룹 만들기" },
  { "keys": "H", "action": "노드 숨기기/접기" }
]
```

### Week 7 — UV Unwrapping + Texture
```json
"shortcuts": [
  { "keys": "U", "action": "UV Unwrap 메뉴 열기" },
  { "keys": "Ctrl + E → Mark Seam", "action": "UV Seam 지정" },
  { "keys": "L", "action": "UV Editor에서 Island 선택" },
  { "keys": "P", "action": "UV Editor에서 Pin 고정" },
  { "keys": "A", "action": "UV Editor에서 전체 선택" },
  { "keys": "S + X/Y + 0", "action": "UV Island 정렬" }
]
```

### Week 8 — 중간 프로젝트
→ shortcuts 불필요 (발표 주차). 스킵.

### Week 9 — Lighting
```json
"shortcuts": [
  { "keys": "Shift + A → Light", "action": "조명 추가 메뉴" },
  { "keys": "Z → Rendered", "action": "렌더 미리보기 모드" },
  { "keys": "Shift + Z", "action": "Rendered/Solid 토글" },
  { "keys": ".", "action": "Properties에서 Light Radius 조절" },
  { "keys": "Ctrl + Numpad 0", "action": "현재 시점을 카메라로 설정" },
  { "keys": "Numpad 0", "action": "카메라 뷰 전환" }
]
```

### Week 10 — Animation
```json
"shortcuts": [
  { "keys": "I", "action": "Insert Keyframe 메뉴" },
  { "keys": "Alt + I", "action": "Delete Keyframe" },
  { "keys": "Space", "action": "Timeline 재생/정지" },
  { "keys": "← / →", "action": "이전/다음 프레임" },
  { "keys": "Shift + ← / →", "action": "시작/끝 프레임으로 이동" },
  { "keys": "T", "action": "Keyframe Interpolation 변경" }
]
```

### Week 11 — Rigging
```json
"shortcuts": [
  { "keys": "Shift + A → Armature", "action": "Armature(뼈대) 추가" },
  { "keys": "Ctrl + P → Armature Deform", "action": "메쉬에 Armature 연결" },
  { "keys": "E", "action": "Edit Mode에서 Bone 확장" },
  { "keys": "Shift + I", "action": "Bone 추가 (선택 끝에서)" },
  { "keys": "Alt + P", "action": "Parent 해제" },
  { "keys": "Ctrl + Tab", "action": "Pose Mode 전환" }
]
```

### Week 12 — Mixamo
```json
"shortcuts": [
  { "keys": "Ctrl + J", "action": "오브젝트 합치기 (Join)" },
  { "keys": "Ctrl + A → All Transforms", "action": "Transform 적용 (Import 후 필수)" },
  { "keys": "NLA Editor", "action": "여러 애니메이션 레이어 관리" },
  { "keys": "Shift + Ctrl + M", "action": "Merge by Distance (중복 버텍스 정리)" }
]
```

### Week 13 — Rendering
```json
"shortcuts": [
  { "keys": "F12", "action": "이미지 렌더링" },
  { "keys": "Ctrl + F12", "action": "애니메이션 렌더링" },
  { "keys": "F11", "action": "마지막 렌더 결과 보기" },
  { "keys": "Z → Rendered", "action": "실시간 렌더 미리보기" },
  { "keys": "Ctrl + B (카메라 뷰)", "action": "렌더 영역 지정" },
  { "keys": "N → Output", "action": "출력 설정 패널" }
]
```

### Week 14-15 — 최종 프로젝트/발표
→ shortcuts 불필요 (발표 주차). 스킵.

**실행:** 에이전트 1개가 curriculum.js를 읽고, 위 데이터를 각 주차에 삽입.

---

## Task 2: Phase A — docs[] 채우기 (빈 주차)

**Files:**
- Modify: `course-site/data/curriculum.js`

**대상 주차 및 추가할 docs:**

### Week 1
```json
"docs": [
  { "title": "Blender 설치 가이드", "url": "https://docs.blender.org/manual/en/latest/getting_started/installing/index.html" }
]
```

### Week 2
```json
"docs": [
  { "title": "3D Navigation", "url": "https://docs.blender.org/manual/en/latest/editors/3dview/navigate/introduction.html" },
  { "title": "Object Mode", "url": "https://docs.blender.org/manual/en/latest/scene_layout/object/introduction.html" },
  { "title": "Edit Mode", "url": "https://docs.blender.org/manual/en/latest/modeling/meshes/editing/introduction.html" },
  { "title": "Extrude Region", "url": "https://docs.blender.org/manual/en/latest/modeling/meshes/tools/extrude_region.html" },
  { "title": "Bevel", "url": "https://docs.blender.org/manual/en/latest/modeling/meshes/tools/bevel.html" }
]
```

### Week 6
```json
"docs": [
  { "title": "Materials", "url": "https://docs.blender.org/manual/en/latest/render/materials/introduction.html" },
  { "title": "Principled BSDF", "url": "https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/principled.html" },
  { "title": "Shader Editor", "url": "https://docs.blender.org/manual/en/latest/editors/shader_editor.html" },
  { "title": "Texture Nodes", "url": "https://docs.blender.org/manual/en/latest/render/shader_nodes/textures/index.html" }
]
```

### Week 7
```json
"docs": [
  { "title": "UV Unwrapping", "url": "https://docs.blender.org/manual/en/latest/modeling/meshes/uv/unwrapping/index.html" },
  { "title": "UV Editor", "url": "https://docs.blender.org/manual/en/latest/editors/uv/introduction.html" },
  { "title": "Texture Painting", "url": "https://docs.blender.org/manual/en/latest/sculpt_paint/texture_paint/index.html" }
]
```

### Week 8
```json
"docs": []
```
_(중간고사 — 빈 배열 유지)_

### Week 10
```json
"docs": [
  { "title": "Keyframes", "url": "https://docs.blender.org/manual/en/latest/animation/keyframes/introduction.html" },
  { "title": "Dope Sheet", "url": "https://docs.blender.org/manual/en/latest/editors/dope_sheet/introduction.html" },
  { "title": "Graph Editor", "url": "https://docs.blender.org/manual/en/latest/editors/graph_editor/introduction.html" }
]
```

### Week 11
```json
"docs": [
  { "title": "Armatures", "url": "https://docs.blender.org/manual/en/latest/animation/armatures/index.html" },
  { "title": "Skinning", "url": "https://docs.blender.org/manual/en/latest/animation/armatures/skinning/index.html" },
  { "title": "Weight Paint", "url": "https://docs.blender.org/manual/en/latest/sculpt_paint/weight_paint/index.html" }
]
```

### Week 12
```json
"docs": [
  { "title": "Import/Export", "url": "https://docs.blender.org/manual/en/latest/files/import_export/index.html" },
  { "title": "NLA Editor", "url": "https://docs.blender.org/manual/en/latest/editors/nla/index.html" }
]
```

### Week 13
```json
"docs": [
  { "title": "Cycles Renderer", "url": "https://docs.blender.org/manual/en/latest/render/cycles/index.html" },
  { "title": "EEVEE", "url": "https://docs.blender.org/manual/en/latest/render/eevee/index.html" },
  { "title": "Render Output", "url": "https://docs.blender.org/manual/en/latest/render/output/index.html" },
  { "title": "Compositing", "url": "https://docs.blender.org/manual/en/latest/compositing/index.html" }
]
```

### Week 14-15
```json
"docs": []
```
_(최종 프로젝트/발표 — 빈 배열 유지)_

**실행:** Task 1과 동일 에이전트에서 같이 처리.

---

## Task 3: Phase B — 누락 이미지 캡처

**Files:**
- Create: `course-site/assets/images/week05/ai-3d-import.png`
- Create: `course-site/assets/images/week07/texture-paint.png`
- Create: `course-site/assets/images/week12/mixamo-upload.png`
- Modify: `course-site/data/curriculum.js` (image 필드 추가)

**캡처 대상:**

| Week | Step | 파일명 | URL (또는 대체) |
|------|------|--------|----------------|
| 5 | Step 1 | ai-3d-import.png | _(AI 도구 — 공식 문서 없음. Blender Import 문서로 대체)_ `https://docs.blender.org/manual/en/latest/files/import_export/index.html` |
| 7 | Step 3 | texture-paint.png | `https://docs.blender.org/manual/en/latest/sculpt_paint/texture_paint/index.html` |
| 12 | Step 1 | mixamo-upload.png | _(Mixamo 외부 서비스 — Blender Import 문서로 대체)_ `https://docs.blender.org/manual/en/latest/files/import_export/index.html` |

**절차:** Playwright MCP로 각 URL → 사이드바 제거 JS → 스크린샷 → 저장 → curriculum.js image 필드 업데이트

---

## Task 4: Phase C — Show Me 카드 생성 (Week 4~13)

**Files:**
- Create: `course-site/assets/showme/*.html` (새 카드들)
- Modify: `course-site/assets/showme/_registry.js` (새 항목 등록)

**필요한 새 카드 목록:**

| Week | Step | 카드 ID | 주제 | 이미 존재? |
|------|------|---------|------|-----------|
| 4 | Step 1 | `transform-apply` | Apply Scale/Rotation 이해 | ❌ 새로 생성 |
| 4 | Step 2 | `boolean-modifier` | Boolean 모디파이어 | ✅ 있음 |
| 4 | Step 3 | `bevel-modifier` | Bevel + Weighted Normal | ✅ 있음 |
| 4 | Step 4 | `array-modifier` | Array 고급 | ✅ 있음 |
| 4 | Step 5 | `simple-deform` | Simple Deform 모디파이어 | ❌ 새로 생성 |
| 5 | Step 2 | `sculpt-basics` | Sculpt Mode 기초 브러시 | ❌ 새로 생성 |
| 6 | Step 1 | `material-basics` | Material 시스템 기초 | ❌ 새로 생성 |
| 6 | Step 2 | `principled-bsdf` | Principled BSDF 노드 | ❌ 새로 생성 |
| 6 | Step 3 | `shader-editor` | Shader Editor 사용법 | ❌ 새로 생성 |
| 7 | Step 1 | `uv-unwrapping` | UV Seam + Unwrap | ❌ 새로 생성 |
| 7 | Step 2 | `uv-editor` | UV Editor 조작 | ❌ 새로 생성 |
| 9 | Step 1 | `light-types` | 4가지 Light 종류 | ❌ 새로 생성 |
| 9 | Step 2 | `hdri-lighting` | HDRI 환경 조명 | ❌ 새로 생성 |
| 9 | Step 3 | `three-point-light` | 3점 조명법 | ❌ 새로 생성 |
| 10 | Step 1 | `keyframe-basics` | 키프레임 기초 | ❌ 새로 생성 |
| 10 | Step 2 | `graph-editor` | Dope Sheet + Graph Editor | ❌ 새로 생성 |
| 11 | Step 1 | `armature-basics` | Armature 구조 이해 | ❌ 새로 생성 |
| 11 | Step 2 | `weight-paint` | Weight Paint + Skinning | ❌ 새로 생성 |
| 13 | Step 1 | `render-settings` | Cycles vs EEVEE | ❌ 새로 생성 |
| 13 | Step 2 | `compositing-basics` | 컴포지팅 기초 | ❌ 새로 생성 |

**새로 생성해야 할 카드: 17개**
**이미 존재하는 카드 재활용: 3개** (boolean, bevel, array)

**실행:** /showme 패턴으로 병렬 에이전트 실행. 각 에이전트에게:
1. mirror-modifier.html 전체 CSS 참조
2. 해당 Blender 기능의 개념/단축키/사용 사례
3. 4탭 구조 + initQuiz + postMessage + doc-ref 필수

---

## Task 5: Phase D — curriculum.js showme 필드 연결

**Files:**
- Modify: `course-site/data/curriculum.js`

**연결 매핑:**

```
Week 4 Step 1: showme: "transform-apply"
Week 4 Step 2: showme: "boolean-modifier"
Week 4 Step 3: showme: "bevel-modifier"
Week 4 Step 4: showme: "array-modifier"
Week 4 Step 5: showme: "simple-deform"
Week 5 Step 2: showme: "sculpt-basics"
Week 6 Step 1: showme: "material-basics"
Week 6 Step 2: showme: "principled-bsdf"
Week 6 Step 3: showme: "shader-editor"
Week 7 Step 1: showme: "uv-unwrapping"
Week 7 Step 2: showme: "uv-editor"
Week 9 Step 1: showme: "light-types"
Week 9 Step 2: showme: "hdri-lighting"
Week 9 Step 3: showme: "three-point-light"
Week 10 Step 1: showme: "keyframe-basics"
Week 10 Step 2: showme: "graph-editor"
Week 11 Step 1: showme: "armature-basics"
Week 11 Step 2: showme: "weight-paint"
Week 13 Step 1: showme: "render-settings"
Week 13 Step 2: showme: "compositing-basics"
```

---

## Task 6: 검증

**Step 1:** 전체 파일 카운트 확인
```bash
ls course-site/assets/showme/*.html | grep -v _template | wc -l
# Expected: 39+ (기존 22 + 신규 17)
```

**Step 2:** curriculum.js 무결성
```bash
node -e "const c = require('./course-site/data/curriculum.js'); console.log(c.length + ' weeks'); c.forEach(w => console.log('Week', w.week, ':', w.shortcuts?.length || 0, 'shortcuts,', w.docs?.length || 0, 'docs,', w.steps?.filter(s => s.showme).length || 0, 'showme'))"
```

**Step 3:** 브라우저 검증
```bash
cd course-site && python3 -m http.server 8080
# Week 4~13 각 페이지에서 Show Me 버튼 + 단축키 + 문서 링크 확인
```

---

## 실행 전략

- **Task 1+2**: 1개 에이전트 (curriculum.js shortcuts + docs 편집)
- **Task 3**: Playwright MCP로 3장 캡처
- **Task 4**: 병렬 에이전트 4~5개 (카드 17개를 3~4개씩 분배)
- **Task 5**: 1개 에이전트 (curriculum.js showme 필드 편집)
- **Task 6**: 검증

**병렬 가능**: Task 1+2 ∥ Task 3 ∥ Task 4 → Task 5 → Task 6
