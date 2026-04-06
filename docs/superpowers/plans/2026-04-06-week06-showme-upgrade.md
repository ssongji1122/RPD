# Week 06 ShowMe 카드 리디자인 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 6주차 ShowMe 카드 4개를 표준화·업그레이드하고 학습 경로를 연결한다.

**Architecture:** 각 카드는 독립 HTML 파일(CSS 인라인, JS 인라인). material-basics.html의 CSS를 공통 템플릿으로 복사. 카드 간 연결은 "언제 쓰나요?" 탭 하단 tip-box로 처리.

**Tech Stack:** HTML5 Canvas, Vanilla JS, CSS Variables (dark theme)

**Spec:** `docs/superpowers/specs/2026-04-06-week06-showme-upgrade-design.md`

---

## Task 1: material-basics 학습경로 링크 추가

**Files:**
- Modify: `course-site/assets/showme/material-basics.html` (panel-when 섹션)

- [ ] **Step 1: 학습경로 tip-box 추가**

`material-basics.html`의 `panel-when` 섹션에서 마지막 `.tip-box.warn` 다음, `.doc-ref` 앞에 추가:

```html
<div class="tip-box" style="margin-top:10px;border-color:rgba(16,185,129,.2);background:rgba(16,185,129,.06)">
  <strong style="color:var(--success-soft)">다음 단계:</strong> Base Color·Metallic·Roughness만으로 부족할 때 → <strong>Principled BSDF</strong> 카드에서 Subsurface, Emission, Transmission 등 고급 파라미터를 알아보세요.
</div>
```

- [ ] **Step 2: 프리뷰 검증**

Run: preview server에서 `material-basics.html` → "언제 쓰나요?" 탭 스크롤 하단에 초록색 "다음 단계" tip-box 표시 확인

- [ ] **Step 3: 커밋**

```bash
git add course-site/assets/showme/material-basics.html
git commit -m "feat(showme): material-basics 학습경로 링크 추가"
```

---

## Task 2: principled-bsdf 전체 업그레이드

**Files:**
- Modify: `course-site/assets/showme/principled-bsdf.html` (전체 재작성)

- [ ] **Step 1: CSS 섹션 작성**

`material-basics.html`의 전체 `<style>` 블록을 복사하되, 다음 추가 CSS를 포함:

```css
/* ── Modifier Panel (material-basics에 이미 있음) ── */
.modifier-panel { ... }
.mp-row { ... }
.mp-label { ... }
.mp-slider { ... }
.mp-value { ... }
.mp-stat { ... }
.preset-row { ... }

/* ── Concept Visual ── */
.concept-visual { ... }
.cv-grid { ... }
.cv-item { ... }
```

material-basics.html과 remesh-decimate.html에서 이 CSS 클래스들을 가져온다.

- [ ] **Step 2: 탭 구조 + 개념 이해 탭 작성**

```html
<nav class="tabs" role="tablist">
  <button class="tab is-active" data-tab="concept" role="tab" aria-selected="true">개념 이해</button>
  <button class="tab" data-tab="visual" role="tab" aria-selected="false">interaction</button>
  <button class="tab" data-tab="when" role="tab" aria-selected="false">언제 쓰나요?</button>
  <button class="tab" data-tab="quiz" role="tab" aria-selected="false">퀴즈</button>
</nav>
```

개념 카드 4개:
1. Principled BSDF란? (badge-blue) — 만능 셰이더, 고급 파라미터 소개
2. Subsurface (badge-green) — 피하산란, 피부/왁스/우유
3. Emission & Transmission (badge-amber) — 발광·투과·IOR
4. 다른 BSDF도 있어요 — Principled Hair BSDF 존재 안내

개념 시각화: canvas 3개 (cv-subsurface, cv-emission, cv-transmission)으로 구체 비교

단축키: Shader Editor 열기 등

doc-ref: `https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/principled.html`

- [ ] **Step 3: interaction 탭 작성**

Canvas 구체 렌더링 (material-basics의 `renderSphere()` 함수 확장):
- Blinn-Phong 기반 + Subsurface(피부톤 블렌딩), Emission(additive 발광), Transmission(투명도+굴절 시뮬)

modifier-panel 컨트롤:
```html
<div class="modifier-panel">
  <div class="mp-title">Principled BSDF</div>
  <div class="mp-row">
    <span class="mp-label">Base Color</span>
    <input type="color" class="mp-color" id="sliderColor" value="#3b82f6">
    <span style="flex:1"></span>
    <span class="mp-value" id="matTypeLabel" style="width:auto;padding:3px 10px">...</span>
  </div>
  <!-- Metallic, Roughness, Subsurface, Emission, Transmission, IOR 슬라이더 -->
</div>
```

프리셋 버튼 7개: 피부, 유리, 자동차, 네온, 대리석, 꿀, 벨벳
- 각 프리셋 값은 스펙 §5.2의 프리셋 테이블 참조
- 클릭 시 mp-stat에 "핵심: Subsurface로 피하산란 표현" 같은 설명 표시

renderSphere 확장 로직:
```javascript
// Subsurface: 빛이 표면 아래를 통과하는 효과
// diffuse에 subsurface color를 블렌드
var sssBlend = subsurface;
r = r * (1 - sssBlend) + (sssR/255 * (ambient + diff * 0.9)) * sssBlend;

// Emission: additive light
r += emissionR * emission;

// Transmission: alpha blending with background
var alpha = 1 - transmission;
r = r * alpha + bgR * (1 - alpha);
```

- [ ] **Step 4: 언제 쓰나요? + 퀴즈 탭 작성**

언제 쓰나요?:
- usage-grid: "고급 파라미터가 필요한 경우" vs "기본 3속성으로 충분한 경우"
- combo-grid: Subsurface+피부, Emission+네온, Transmission+유리, Hair BSDF+머리카락
- 학습경로 tip-box: "노드를 직접 연결해 복합 재질을 만들고 싶을 때 → Shader Editor"
- doc-ref

퀴즈 5문제 (표준 initQuiz + postMessage):
1. Subsurface 파라미터 용도
2. Emission vs Transmission 차이
3. IOR 의미 (Index of Refraction)
4. "유리 프리셋에서 가장 중요한 파라미터는?" (Transmission=1 + IOR)
5. Principled Hair BSDF 존재 인지

- [ ] **Step 5: 프리뷰 검증**

Run: preview server → principled-bsdf.html
확인 항목:
1. 4탭 모두 렌더링 정상
2. 개념 시각화 구체 3개 표시
3. interaction 슬라이더 반응 정상 (7개 파라미터)
4. 프리셋 버튼 클릭 → 구체 변화 + 설명 표시
5. 퀴즈 5문제 + postMessage 전송
6. 모바일 반응형

- [ ] **Step 6: 커밋**

```bash
git add course-site/assets/showme/principled-bsdf.html
git commit -m "feat(showme): principled-bsdf 전체 업그레이드 (고급 파라미터 + 프리셋)"
```

---

## Task 3: shader-editor 전체 업그레이드

**Files:**
- Modify: `course-site/assets/showme/shader-editor.html` (전체 재작성)

- [ ] **Step 1: CSS 섹션 작성**

material-basics.html에서 전체 CSS 복사 + modifier-panel CSS 포함.

- [ ] **Step 2: 개념 이해 탭 작성**

개념 카드 3개:
1. 노드란? — Input → Processing → Output, 소켓 연결로 데이터 흐름
2. Socket 색상 규칙 — 노랑=Color, 회색=Value, 보라=Vector, 초록=Shader
3. 필수 노드 3종 — Principled BSDF, Image Texture, Mapping

개념 시각화: 정적 canvas에 노드 연결 다이어그램 그리기
- drawNode() 함수: 노드 박스 + 타이틀바 + 소켓 원 + 텍스트
- drawWire() 함수: 소켓 간 베지어 커브 연결
- 노드 체인: Image Texture → Mapping → Principled BSDF → Material Output

```javascript
function drawNode(ctx, x, y, w, h, title, color, inputs, outputs) {
  // 노드 박스
  ctx.fillStyle = 'rgba(40,40,45,0.95)';
  ctx.strokeStyle = 'rgba(255,255,255,0.15)';
  ctx.beginPath(); ctx.roundRect(x, y, w, h, 6); ctx.fill(); ctx.stroke();
  // 타이틀바
  ctx.fillStyle = color;
  ctx.beginPath(); ctx.roundRect(x, y, w, 22, [6,6,0,0]); ctx.fill();
  ctx.fillStyle = '#fff'; ctx.font = 'bold 10px sans-serif';
  ctx.textAlign = 'center'; ctx.fillText(title, x + w/2, y + 15);
  // 소켓
  inputs.forEach(function(inp, i) {
    var sy = y + 34 + i * 18;
    ctx.beginPath(); ctx.arc(x, sy, 4, 0, Math.PI*2);
    ctx.fillStyle = inp.color; ctx.fill();
    ctx.fillStyle = '#aaa'; ctx.font = '9px sans-serif'; ctx.textAlign = 'left';
    ctx.fillText(inp.name, x + 8, sy + 3);
  });
  outputs.forEach(function(out, i) {
    var sy = y + 34 + i * 18;
    ctx.beginPath(); ctx.arc(x + w, sy, 4, 0, Math.PI*2);
    ctx.fillStyle = out.color; ctx.fill();
  });
}
```

doc-ref: `https://docs.blender.org/manual/en/latest/editors/shader_editor.html`

- [ ] **Step 3: interaction 탭 — Mix Shader 데모**

Canvas: 구체 렌더링 (material-basics의 renderSphere 재활용)
- 두 색상/속성을 Mix Factor로 블렌딩

modifier-panel:
```html
<div class="modifier-panel">
  <div class="mp-title">Mix Shader</div>
  <div class="mp-row">
    <span class="mp-label">Shader A</span>
    <input type="color" class="mp-color" id="colorA" value="#3b82f6">
  </div>
  <div class="mp-row">
    <span class="mp-label">Shader B</span>
    <input type="color" class="mp-color" id="colorB" value="#d4a855">
  </div>
  <div class="mp-row">
    <span class="mp-label">Mix Factor</span>
    <input type="range" class="mp-slider" id="mixFactor" min="0" max="100" value="50">
    <span class="mp-value" id="mixVal">0.50</span>
  </div>
  <div class="mp-row">
    <span class="mp-label">Roughness A</span>
    <input type="range" class="mp-slider" id="roughA" min="0" max="100" value="50">
    <span class="mp-value" id="roughAVal">0.50</span>
  </div>
  <div class="mp-row">
    <span class="mp-label">Roughness B</span>
    <input type="range" class="mp-slider" id="roughB" min="0" max="100" value="30">
    <span class="mp-value" id="roughBVal">0.30</span>
  </div>
</div>
```

블렌딩 로직:
```javascript
// Mix two materials by factor
var f = mixFactor;
var mixedColor = {
  r: rgbA.r * (1-f) + rgbB.r * f,
  g: rgbA.g * (1-f) + rgbB.g * f,
  b: rgbA.b * (1-f) + rgbB.b * f
};
var mixedRough = roughnessA * (1-f) + roughnessB * f;
var mixedMetal = metallicA * (1-f) + metallicB * f;
```

프리셋 3개: 금속+녹(부식), 페인트+금속(자동차 칩), 무광+광택(표면 변화)

- [ ] **Step 4: 언제 쓰나요? + 퀴즈 탭**

언제 쓰나요?:
- usage-grid: Shader Editor 필요한 경우 vs Material Properties만으로 충분한 경우
- combo-grid: Mix Shader, Color Ramp, Mapping Node 활용
- 학습경로: "이미지 텍스처를 매핑하고 싶을 때 → Texture Nodes"
- doc-ref

퀴즈 5문제:
1. 노드 데이터 흐름 방향 (왼→오)
2. 노랑 소켓의 의미 (Color)
3. Mix Shader Factor 0 = 어떤 결과?
4. Material Output 노드 역할
5. Shader Editor 여는 방법

- [ ] **Step 5: 프리뷰 검증**

확인 항목:
1. 개념 탭 노드 다이어그램 렌더링
2. interaction 탭 Mix 슬라이더 정상 작동
3. 프리셋 버튼 반응
4. 퀴즈 5문제 + postMessage
5. 모바일 반응형

- [ ] **Step 6: 커밋**

```bash
git add course-site/assets/showme/shader-editor.html
git commit -m "feat(showme): shader-editor 전체 업그레이드 (Mix Shader 데모 + 노드 다이어그램)"
```

---

## Task 4: texture-nodes 신규 생성

**Files:**
- Create: `course-site/assets/showme/texture-nodes.html`

- [ ] **Step 1: CSS + 탭 구조**

material-basics.html에서 전체 CSS 복사 + modifier-panel CSS.
4탭 표준 구조 생성.

- [ ] **Step 2: 개념 이해 탭**

개념 카드 3개:
1. Texture Node란? — Image Texture(사진), Noise(잡음), Checker(체크), Wave(파도)
2. Mapping Node — Location, Scale, Rotation 제어
3. UV vs Generated 좌표계 — UV=수동 정밀, Generated=자동 빠름

개념 시각화: canvas 3개에 Checker 텍스처 Scale 비교
```javascript
function drawChecker(ctx, w, h, scaleX, scaleY) {
  for (var y = 0; y < h; y++) {
    for (var x = 0; x < w; x++) {
      var u = x / w, v = y / h;
      var check = (Math.floor(u * scaleX) + Math.floor(v * scaleY)) % 2;
      ctx.fillStyle = check ? '#e0e0e0' : '#333';
      ctx.fillRect(x, y, 1, 1);
    }
  }
}
```

doc-ref: `https://docs.blender.org/manual/en/latest/render/shader_nodes/textures/index.html`

- [ ] **Step 3: interaction 탭 — 절차적 텍스처 데모**

Canvas 2D 패턴 렌더링. 텍스처 타입 전환 버튼 + modifier-panel 슬라이더.

텍스처 타입 3개:
```javascript
var textures = {
  checker: function(u, v, params) {
    var su = Math.floor(u * params.scaleX);
    var sv = Math.floor(v * params.scaleY);
    return (su + sv) % 2;
  },
  noise: function(u, v, params) {
    // Simplified Perlin noise
    return perlin2D(u * params.scaleX, v * params.scaleY);
  },
  wave: function(u, v, params) {
    var n = perlin2D(u * 5, v * 5) * params.distortion;
    return (Math.sin((u * params.scaleX + n) * Math.PI * 2) + 1) / 2;
  }
};
```

Perlin noise 구현 (simplified 2D):
```javascript
function perlin2D(x, y) {
  // Hash-based gradient noise
  var xi = Math.floor(x), yi = Math.floor(y);
  var xf = x - xi, yf = y - yi;
  var u = fade(xf), v = fade(yf);
  var aa = hash(xi, yi), ab = hash(xi, yi+1);
  var ba = hash(xi+1, yi), bb = hash(xi+1, yi+1);
  var x1 = lerp(grad(aa, xf, yf), grad(ba, xf-1, yf), u);
  var x2 = lerp(grad(ab, xf, yf-1), grad(bb, xf-1, yf-1), u);
  return (lerp(x1, x2, v) + 1) / 2;
}
function fade(t) { return t*t*t*(t*(t*6-15)+10); }
function lerp(a, b, t) { return a + t*(b-a); }
function hash(x, y) {
  var h = (x * 374761393 + y * 668265263 + 1274126177) & 0x7fffffff;
  h = ((h >> 13) ^ h) * 1274126177;
  return ((h >> 13) ^ h) & 0x7fffffff;
}
function grad(hash, x, y) {
  var h = hash & 3;
  var u = h < 2 ? x : y;
  var v = h < 2 ? y : x;
  return ((h & 1) ? -u : u) + ((h & 2) ? -v : v);
}
```

modifier-panel:
```html
<div class="modifier-panel">
  <div class="mp-title">Texture Properties</div>
  <div class="mp-row">
    <span class="mp-label">Scale X</span>
    <input type="range" class="mp-slider" id="scaleX" min="1" max="20" value="5">
    <span class="mp-value" id="scaleXVal">5</span>
  </div>
  <div class="mp-row">
    <span class="mp-label">Scale Y</span>
    <input type="range" class="mp-slider" id="scaleY" min="1" max="20" value="5">
    <span class="mp-value" id="scaleYVal">5</span>
  </div>
  <div class="mp-row">
    <span class="mp-label">Rotation</span>
    <input type="range" class="mp-slider" id="rotation" min="0" max="360" value="0">
    <span class="mp-value" id="rotVal">0°</span>
  </div>
  <div class="mp-row">
    <span class="mp-label">Distortion</span>
    <input type="range" class="mp-slider" id="distortion" min="0" max="100" value="0">
    <span class="mp-value" id="distVal">0.00</span>
  </div>
</div>
```

텍스처 전환 버튼: Checker, Noise, Wave (demo-btn, is-active 토글)

Rotation 적용:
```javascript
function rotateUV(u, v, angleDeg) {
  var rad = angleDeg * Math.PI / 180;
  var cu = u - 0.5, cv = v - 0.5;
  return {
    u: cu * Math.cos(rad) - cv * Math.sin(rad) + 0.5,
    v: cu * Math.sin(rad) + cv * Math.cos(rad) + 0.5
  };
}
```

- [ ] **Step 4: 언제 쓰나요? + 퀴즈 탭**

언제 쓰나요?:
- usage-grid: Image Texture(사진 기반, UV 필요) vs Procedural(수학, 무한 해상도)
- combo-grid: Noise+ColorRamp, Checker+Mapping, Image+Mapping
- doc-ref

퀴즈 5문제:
1. Procedural vs Image Texture 차이
2. Mapping Node 역할
3. UV vs Generated 좌표계
4. Scale 올리면 패턴이 어떻게 변하나? (작아짐/촘촘해짐)
5. Wave Distortion 효과

- [ ] **Step 5: 프리뷰 검증**

확인 항목:
1. Checker/Noise/Wave 전환 정상
2. 슬라이더 조절 시 패턴 실시간 변화
3. Rotation 적용 시 패턴 회전
4. 퀴즈 5문제 + postMessage
5. 모바일 반응형

- [ ] **Step 6: 커밋**

```bash
git add course-site/assets/showme/texture-nodes.html
git commit -m "feat(showme): texture-nodes 신규 카드 (절차적 텍스처 데모)"
```

---

## Task 5: 레지스트리 + 커리큘럼 연결

**Files:**
- Modify: `course-site/assets/showme/_registry.js`
- Modify: `course-site/data/curriculum.js`

- [ ] **Step 1: _registry.js에 texture-nodes 등록**

```javascript
// ── Week 6: Material & Shader ── 섹션에 추가
"texture-nodes":          { label: "Texture Nodes 이해",      icon: "🧩", week: 6 },
```

- [ ] **Step 2: curriculum.js Step 5에 showme 연결**

Week 6 Step 5 (w6-t12 ~ w6-t14 영역)에서 해당 step 객체에 `showme: "texture-nodes"` 필드 추가.

curriculum.js에서 `w6-t12` step을 찾아 showme 필드 추가:
```javascript
// 기존
{ id: "w6-t12", ... }
// 변경
{ id: "w6-t12", ..., showme: "texture-nodes" }
```

- [ ] **Step 3: 커밋**

```bash
git add course-site/assets/showme/_registry.js course-site/data/curriculum.js
git commit -m "feat(showme): texture-nodes 레지스트리 등록 + 커리큘럼 Step 5 연결"
```

---

## Task 6: 전체 프리뷰 검증 + 최종 커밋

- [ ] **Step 1: 전체 카드 순차 검증**

preview server에서 각 카드 순회:
1. `material-basics.html` — 학습경로 링크 표시
2. `principled-bsdf.html` — 4탭 + 7개 프리셋 + 구체 렌더링
3. `shader-editor.html` — 4탭 + Mix Shader 데모 + 노드 다이어그램
4. `texture-nodes.html` — 4탭 + 3종 텍스처 패턴 데모

각 카드 확인 항목:
- [ ] initQuiz 포함
- [ ] postMessage 포함
- [ ] doc-ref 포함
- [ ] data-tab 4개 (concept, visual, when, quiz)
- [ ] 모바일 반응형
- [ ] 콘솔 에러 없음

- [ ] **Step 2: 학습경로 체인 확인**

material-basics → principled-bsdf → shader-editor → texture-nodes 순서로 "다음 단계" 링크가 이어지는지 확인

- [ ] **Step 3: 스킬 로그 기록**

```bash
echo "[$(date '+%Y-%m-%d %H:%M')] mode=upgrade result=success target=material-basics,principled-bsdf,shader-editor,texture-nodes" >> .claude/skill-logs/showme.log
```
