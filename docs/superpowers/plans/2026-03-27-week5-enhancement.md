# Week 5 Enhancement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 5주차 커리큘럼을 Sculpt-first로 재배치하고, 무드보드→AI 러프 생성 스텝과 showme 카드 3장을 추가한다.

**Architecture:** curriculum.js의 week 5 steps 배열 순서를 변경하고, 신규 스텝 2개를 삽입한다. showme 카드 3개의 standalone HTML을 기존 template 패턴으로 생성하고, _catalog.json에 등록한다. assignment와 mistakes도 업데이트한다.

**Tech Stack:** Vanilla HTML/CSS/JS (showme 카드), JSON (catalog), JS data file (curriculum.js)

---

## File Map

| Action | File | Responsibility |
|--------|------|---------------|
| Modify | `course-site/data/curriculum.js:1552-1834` | Week 5 steps 재배치 + 신규 스텝 삽입 + assignment/mistakes 교체 |
| Modify | `course-site/assets/showme/_catalog.json` | 신규 카드 3장 등록 (manualSectionMap, categoryMap, cardOverrides) |
| Create | `course-site/assets/showme/sculpt-brushes.html` | 인터랙티브 Sculpt 브러시 카드 (5탭, Canvas 샌드박스) |
| Create | `course-site/assets/showme/ai-prompt-design.html` | AI 프롬프트 설계 카드 (4탭) |
| Create | `course-site/assets/showme/ai-3d-generation.html` | AI 3D 생성 워크플로우 카드 (4탭) |

---

### Task 1: curriculum.js — Week 5 steps 재배치

**Files:**
- Modify: `course-site/data/curriculum.js:1552-1834`

- [ ] **Step 1: topics 순서 변경**

`course-site/data/curriculum.js`에서 week 5 객체의 `topics` 배열을 다음으로 교체:

```js
"topics": [
  "Sculpt Mode 기초 브러시",
  "Sculpt 브러시 심화 (Clay/Crease/Inflate/Snake Hook)",
  "Remesh·Decimate·메쉬 정리 애드온",
  "무드보드 → AI 프롬프트 설계",
  "AI 3D 생성 (Meshy/Tripo)",
  "AI 메쉬 Import 및 실전 정리"
],
```

- [ ] **Step 2: steps 배열 순서 변경**

기존 steps 배열의 5개 항목을 다음 순서로 재배치:

1. 기존 Step 3 ("Sculpt Mode 기초") → 새 Step 1
2. 기존 Step 4 ("Sculpt 브러시 심화") → 새 Step 2
3. 기존 Step 5 ("Remesh와 마무리") + 기존 Step 2 ("AI 메쉬 정리")를 합쳐서 → 새 Step 3 "Remesh + Decimate + 메쉬 정리"
4. 신규 Step 4 "무드보드 → AI 프롬프트 설계" 삽입
5. 기존 Step 1 ("AI 3D 생성 체험") 수정 → 새 Step 5
6. 신규 Step 6 "AI 메쉬 정리 실전" 삽입

구체적으로:

**새 Step 1 (기존 Step 3 이동)** — Sculpt Mode 기초: 변경 없이 위치만 이동. `showme: "sculpt-basics"` 유지.

**새 Step 2 (기존 Step 4 이동 + 확장)** — Sculpt 브러시 심화:
- tasks에 Snake Hook 추가:
```js
{
  "id": "w5-t-snake",
  "label": "Snake Hook으로 뿔이나 촉수 끌어내기",
  "detail": "끝점이 따라오며 길게 늘어나요"
}
```
- `showme: "sculpt-brushes"` 추가 (신규 카드)
- image 유지: `"assets/images/week05/sculpt-brushes.png"`

**새 Step 3 (기존 Step 5 + Step 2 합치기)** — Remesh + Decimate + 메쉬 정리:
```js
{
  "title": "Remesh + Decimate + 메쉬 정리",
  "copy": "Sculpt를 하다 보면 메쉬가 늘어나서 찌그러지는 곳이 생겨요. Remesh로 고르게 나누고, Decimate로 줄이고, Mesh Cleaner로 정리해요. 이 도구들은 나중에 AI 메쉬 정리에도 그대로 쓸 거예요.",
  "goal": [
    "Remesh의 역할을 이해한다",
    "Decimate로 폴리곤을 줄인다",
    "Mesh Cleaner 2 애드온을 설치하고 사용한다"
  ],
  "done": [
    "Remesh 후 메쉬가 고르게 정리됐다",
    "Decimate로 폴리곤 수가 절반 이하로 줄었다",
    "Mesh Cleaner로 중복 버텍스가 제거됐다"
  ],
  "tasks": [
    {
      "id": "w5-t15",
      "label": "Sculpt Mode → Remesh 버튼 또는 Ctrl+R",
      "detail": "Voxel Size를 조절해서 해상도 맞추기"
    },
    {
      "id": "w5-t16",
      "label": "Remesh 전후 비교해보기",
      "detail": "메쉬가 고르게 나뉘었는지 확인"
    },
    {
      "id": "w5-t4",
      "label": "Viewport Overlay에서 폴리곤 수 확인",
      "detail": "Statistics 켜기"
    },
    {
      "id": "w5-t5",
      "label": "Decimate Modifier 추가 후 Ratio 조절",
      "detail": "0.3~0.5 정도에서 형태 유지되는 지점 찾기"
    },
    {
      "id": "w5-t-mc",
      "label": "Mesh Cleaner 2 애드온 설치 및 실행",
      "detail": "Preferences → Add-ons에서 설치 후 one-click 정리",
      "url": "https://decoded.gumroad.com/l/meshcleaner"
    },
    {
      "id": "w5-t-qr",
      "label": "QRemeshify로 쿼드 리메시 체험",
      "detail": "트라이앵글 → 쿼드 변환, 선택적 사용",
      "url": "https://ksami.gumroad.com/l/QRemeshify"
    }
  ],
  "image": "assets/images/week05/remesh.png",
  "showme": ["remesh-modifier", "decimate-modifier"],
  "widgets": [
    { "type": "showme", "id": "mask-modifier" },
    { "type": "showme", "id": "multiresolution-modifier" }
  ]
}
```

**새 Step 4 (신규)** — 무드보드 → AI 프롬프트 설계:
```js
{
  "title": "무드보드 → AI 프롬프트 설계",
  "copy": "1주차에 만든 무드보드, 기억하죠? 오늘 그걸 3D로 만들기 시작해요. AI한테 잘 설명하려면 이미지 느낌을 단어로 번역하는 과정이 필요해요.",
  "goal": [
    "무드보드 이미지를 텍스트 키워드로 변환할 수 있다",
    "AI 3D 생성용 프롬프트를 작성할 수 있다"
  ],
  "done": [
    "프롬프트 초안이 노션에 기록되었다",
    "최소 2가지 프롬프트 변형을 준비했다"
  ],
  "tasks": [
    {
      "id": "w5-t-mood1",
      "label": "Notion에서 내 무드보드 열기",
      "detail": "1주차에 저장한 Mixboard 링크와 이미지 확인"
    },
    {
      "id": "w5-t-mood2",
      "label": "핵심 키워드 5개 이내로 추출",
      "detail": "형태 1~2개, 스타일 1개, 재질감 1~2개"
    },
    {
      "id": "w5-t-mood3",
      "label": "Meshy용 프롬프트 초안 작성",
      "detail": "[형태] + [스타일] + [재질감] + 3D model 패턴으로"
    }
  ],
  "showme": "ai-prompt-design"
}
```

**새 Step 5 (기존 Step 1 수정)** — 본인 프로젝트 AI 러프 생성:
- copy 변경: `"내 아이디어의 초벌을 AI가 잡아줘요. 완벽하지 않아도 괜찮아요 — 오늘은 방향을 확인하는 게 목적이에요."`
- task w5-t1 label 변경: `"Meshy에서 내 프롬프트로 생성"`
- task w5-t2 label 변경: `"키워드 하나 바꿔서 재생성 — 어느 쪽이 내 의도에 더 가까운지 선택"`
- task w5-t3 유지
- `showme: "ai-3d-generation"` 추가
- image 유지: `"assets/images/week05/ai-3d-generation.png"`

**새 Step 6 (신규)** — AI 메쉬 정리 실전:
```js
{
  "title": "AI 메쉬 정리 실전",
  "copy": "Step 3에서 배운 Mesh Cleaner와 Decimate를 AI가 만든 내 메쉬에 직접 써봐요. Import한 그대로는 폴리곤이 너무 많아서 이후 작업이 힘들어요.",
  "goal": [
    "AI 메쉬의 폴리곤 문제를 직접 해결한다"
  ],
  "done": [
    "AI 생성 메쉬의 폴리곤이 원본 대비 절반 이하로 줄었다",
    "형태가 크게 무너지지 않았다"
  ],
  "tasks": [
    {
      "id": "w5-t-clean1",
      "label": "Import한 AI 메쉬에 Mesh Cleaner 실행",
      "detail": "중복 버텍스, 빈 구멍, 뒤집힌 노멀 한번에 정리"
    },
    {
      "id": "w5-t-clean2",
      "label": "Decimate로 폴리곤 줄이기",
      "detail": "Ratio 0.3~0.5, 형태 유지되는 지점 찾기"
    },
    {
      "id": "w5-t6",
      "label": "Ctrl+A로 Scale 정리 후 원점 확인",
      "detail": "Import 메쉬는 크기가 제각각이에요"
    },
    {
      "id": "w5-t-clean3",
      "label": "최종 형태 Object Mode에서 확인 후 스크린샷",
      "detail": "정리 전후를 비교할 수 있게 저장"
    }
  ]
}
```

- [ ] **Step 3: assignment 교체**

기존 assignment를 다음으로 교체:

```js
"assignment": {
  "title": "내 프로젝트 첫 3D 러프",
  "description": "1주차 무드보드를 바탕으로 AI 러프를 뽑고, 메쉬를 정리한 결과물을 제출해요. 완성도보다 방향이 맞는지가 중요해요.",
  "checklist": [
    "내 무드보드에서 추출한 프롬프트 키워드 (텍스트)",
    "AI 생성 원본 스크린샷",
    "메쉬 정리 후 스크린샷",
    "한 문장: '나는 앞으로 ___을 만들 예정이에요'",
    "완성 렌더 이미지 1장 이상"
  ]
},
```

- [ ] **Step 4: mistakes 업데이트**

기존 mistakes 배열 끝에 2개 추가:

```js
"프롬프트가 너무 짧음 → 형태+스타일+재질 키워드를 넣어야 원하는 결과가 나와요",
"AI 메쉬를 정리 없이 바로 작업 → Mesh Cleaner 먼저 돌리고 시작하기"
```

- [ ] **Step 5: docs 배열에 애드온 링크 추가**

기존 docs 배열 끝에 추가:

```js
{
  "title": "Mesh Cleaner 2",
  "url": "https://decoded.gumroad.com/l/meshcleaner"
},
{
  "title": "QRemeshify",
  "url": "https://ksami.gumroad.com/l/QRemeshify"
}
```

- [ ] **Step 6: 로컬 프리뷰에서 week 5 페이지 확인**

Run: 브라우저에서 `http://localhost:8772/week.html?week=5` 새로고침
Expected: 스텝 순서가 Sculpt 기초 → 브러시 심화 → Remesh+Decimate → 무드보드 → AI 러프 → AI 정리 순으로 표시

- [ ] **Step 7: Commit**

```bash
git add course-site/data/curriculum.js
git commit -m "feat(week5): reorder steps (Sculpt-first) + add moodboard/AI rough steps"
```

---

### Task 2: _catalog.json — 신규 카드 3장 등록

**Files:**
- Modify: `course-site/assets/showme/_catalog.json`

- [ ] **Step 1: manualSectionMap에 3개 추가**

`"sculpt-basics": "sculpting-painting"` 줄 뒤에 추가:

```json
"sculpt-brushes": "sculpting-painting",
"ai-prompt-design": "sculpting-painting",
"ai-3d-generation": "sculpting-painting",
```

- [ ] **Step 2: categoryMap에 3개 추가**

`"sculpt-basics": "Sculpting"` 줄 뒤에 추가:

```json
"sculpt-brushes": "Sculpting",
"ai-prompt-design": "기타",
"ai-3d-generation": "기타",
```

- [ ] **Step 3: cardOverrides에 3개 추가**

`"sculpt-basics"` 오버라이드 블록 뒤에 추가:

```json
"sculpt-brushes": {
  "officialVideos": [
    {
      "label": "Blender Studio - Sculpting Brushes",
      "url": "https://studio.blender.org/training/sculpting-in-blender/brushes/"
    }
  ],
  "keywords": ["clay strips", "crease", "inflate", "snake hook", "brush comparison"],
  "prerequisites": ["sculpt-basics"],
  "audienceNeed": "기본 3개는 써봤는데 다른 브러시들은 뭐가 다른 건지 감이 안 올 때"
},
"ai-prompt-design": {
  "keywords": ["prompt", "AI", "keyword", "moodboard", "text to 3d"],
  "audienceNeed": "AI한테 뭘 어떻게 써야 내가 원하는 모양이 나오는지 모르겠을 때"
},
"ai-3d-generation": {
  "keywords": ["meshy", "tripo", "AI 3D", "glb", "import", "mesh cleaner"],
  "audienceNeed": "Meshy/Tripo에서 만들고 Blender로 가져오는 흐름이 안 잡힐 때"
},
```

- [ ] **Step 4: Commit**

```bash
git add course-site/assets/showme/_catalog.json
git commit -m "feat(showme): register sculpt-brushes, ai-prompt-design, ai-3d-generation in catalog"
```

---

### Task 3: sculpt-brushes.html — 인터랙티브 Sculpt 브러시 카드

**Files:**
- Create: `course-site/assets/showme/sculpt-brushes.html`
- Reference: `course-site/assets/showme/_template.html` (CSS/구조 베이스)
- Reference: `course-site/assets/showme/sculpt-basics.html` (Canvas 패턴, 퀴즈 엔진)

- [ ] **Step 1: 기본 HTML 셸 생성**

`_template.html`의 CSS를 복사하여 `sculpt-brushes.html` 생성. 탭 5개 설정:
- 브러시 도감 (`concept`)
- 직접 해보기 (`sandbox`)
- 비교 (`visual`)
- 레시피 (`recipe`)
- 퀴즈 (`quiz`)

탭 바:
```html
<nav class="tabs" role="tablist">
  <button class="tab is-active" data-tab="concept" role="tab" aria-selected="true" aria-controls="panel-concept">브러시 도감</button>
  <button class="tab" data-tab="sandbox" role="tab" aria-selected="false" aria-controls="panel-sandbox">직접 해보기</button>
  <button class="tab" data-tab="visual" role="tab" aria-selected="false" aria-controls="panel-visual">비교</button>
  <button class="tab" data-tab="recipe" role="tab" aria-selected="false" aria-controls="panel-recipe">레시피</button>
  <button class="tab" data-tab="quiz" role="tab" aria-selected="false" aria-controls="panel-quiz">퀴즈</button>
</nav>
```

- [ ] **Step 2: 탭 1 — 브러시 도감 (concept)**

8종 브러시를 concept-grid 카드로 배치. 각 카드에 브러시명, 비유, 용도, 단축키, Ctrl 반전 설명:

```html
<section class="panel is-active" id="panel-concept" role="tabpanel">
  <div class="concept-grid">
    <div class="concept-card">
      <h3>Draw <span class="badge badge-blue">기본</span></h3>
      <p>크레파스로 칠하듯이 표면을 올려요. <span class="kbd">X</span>로 빠른 선택, <span class="kbd">Ctrl</span> 누르면 파내기.</p>
      <div class="analogy">크레파스로 칠하기 — 가장 기본적인 올리기/내리기</div>
    </div>
    <div class="concept-card">
      <h3>Clay Strips <span class="badge badge-green">덧붙이기</span></h3>
      <p>찰흙 띠를 붙이듯이 넓은 면에 층층이 쌓아요. 큰 형태를 빠르게 잡을 때 좋아요.</p>
      <div class="analogy">찰흙 띠 붙이기 — 넓은 면을 빠르게 채우기</div>
    </div>
    <div class="concept-card">
      <h3>Clay <span class="badge badge-green">밀어붙이기</span></h3>
      <p>손바닥으로 찰흙을 누르듯이 밀면서 쌓아요. Draw보다 평탄한 결과가 나와요.</p>
      <div class="analogy">손바닥으로 누르기 — 평평하게 밀면서 쌓기</div>
    </div>
    <div class="concept-card">
      <h3>Inflate <span class="badge badge-amber">부풀리기</span></h3>
      <p>풍선처럼 바깥으로 부풀려요. 볼이나 근육을 강조할 때 유용해요.</p>
      <div class="analogy">풍선 부풀리기 — 표면을 바깥으로 밀어내기</div>
    </div>
    <div class="concept-card">
      <h3>Crease <span class="badge badge-amber">홈 파기</span></h3>
      <p>송곳으로 긋듯이 깊고 날카로운 주름을 만들어요. 관절, 눈, 입 라인에 활용. <span class="kbd">Shift</span>+<span class="kbd">C</span>로 빠른 선택.</p>
      <div class="analogy">송곳으로 긋기 — 날카로운 홈과 주름</div>
    </div>
    <div class="concept-card">
      <h3>Grab <span class="badge badge-blue">잡아 당기기</span></h3>
      <p>찰흙을 잡고 끌어당겨요. 큰 형태를 이동할 때 필수. <span class="kbd">G</span>로 빠른 선택.</p>
      <div class="analogy">찰흙 잡아 당기기 — 큰 덩어리를 이동</div>
    </div>
    <div class="concept-card">
      <h3>Snake Hook <span class="badge badge-amber">끌어내기</span></h3>
      <p>찰흙 끝을 잡고 길게 늘여요. 뿔, 촉수, 머리카락 표현에 좋아요. <span class="kbd">K</span>로 빠른 선택.</p>
      <div class="analogy">찰흙 꼬리 끌기 — 끝점만 따라오며 길게 늘어남</div>
    </div>
    <div class="concept-card">
      <h3>Smooth <span class="badge badge-blue">정리</span></h3>
      <p>손가락으로 쓸듯이 울퉁불퉁한 표면을 정리해요. <span class="kbd">Shift</span> 누르고 있으면 어디서든 임시 Smooth.</p>
      <div class="analogy">손가락으로 쓸기 — 불균일 제거</div>
    </div>
  </div>
  <div class="shortcut-list">
    <h4>공통 단축키</h4>
    <div class="shortcut-row"><span class="shortcut-keys"><span class="kbd">F</span></span><span>브러시 크기 조절</span></div>
    <div class="shortcut-row"><span class="shortcut-keys"><span class="kbd">Shift</span>+<span class="kbd">F</span></span><span>브러시 강도 조절</span></div>
    <div class="shortcut-row"><span class="shortcut-keys"><span class="kbd">Ctrl</span></span><span>브러시 반전 (올리기↔파내기)</span></div>
    <div class="shortcut-row"><span class="shortcut-keys"><span class="kbd">Shift</span></span><span>임시 Smooth 전환</span></div>
  </div>
  <div class="doc-ref">
    <a href="https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/index.html" target="_blank" rel="noopener">Blender 공식 문서 — Sculpt Brushes</a>
  </div>
</section>
```

- [ ] **Step 3: 탭 2 — 직접 해보기 (sandbox) — CSS 추가**

`<style>` 블록에 sandbox 전용 CSS 추가:

```css
/* ── Sandbox ── */
.sandbox-toolbar {
  display: flex; gap: 6px; padding: 12px;
  flex-wrap: wrap; align-items: center;
  border-bottom: 1px solid var(--line);
  background: var(--bg-soft);
}
.brush-btn {
  padding: 6px 12px; border-radius: 999px;
  border: 1px solid var(--line-strong);
  background: rgba(255,255,255,.04);
  color: var(--muted-strong);
  font: inherit; font-size: .78rem;
  cursor: pointer; transition: background .14s, color .14s;
}
.brush-btn:hover { background: rgba(255,255,255,.09); color: var(--text); }
.brush-btn.is-active {
  background: rgba(10,132,255,.14);
  color: var(--key-soft);
  border-color: rgba(10,132,255,.3);
}
.sandbox-canvas-wrap {
  position: relative;
  border-radius: var(--radius-md);
  border: 1px solid var(--line);
  background: var(--surface);
  overflow: hidden; margin: 14px 0;
}
.sandbox-canvas-wrap canvas { display: block; width: 100%; cursor: crosshair; }
.sandbox-info {
  display: flex; justify-content: space-between; padding: 8px 12px;
  font-size: .78rem; color: var(--muted);
  border-top: 1px solid var(--line);
}
.sandbox-reset {
  padding: 6px 16px; border-radius: 999px;
  border: 1px solid var(--line-strong);
  background: rgba(255,255,255,.04);
  color: var(--muted-strong);
  font: inherit; font-size: .8rem;
  cursor: pointer;
}
.sandbox-reset:hover { background: rgba(255,255,255,.09); }
```

- [ ] **Step 4: 탭 2 — 직접 해보기 (sandbox) — HTML**

```html
<section class="panel" id="panel-sandbox" role="tabpanel">
  <div class="sandbox-canvas-wrap">
    <div class="sandbox-toolbar">
      <button class="brush-btn is-active" data-brush="draw">Draw</button>
      <button class="brush-btn" data-brush="clay">Clay Strips</button>
      <button class="brush-btn" data-brush="inflate">Inflate</button>
      <button class="brush-btn" data-brush="crease">Crease</button>
      <button class="brush-btn" data-brush="grab">Grab</button>
      <button class="brush-btn" data-brush="snakehook">Snake Hook</button>
      <button class="brush-btn" data-brush="smooth">Smooth</button>
      <span style="margin-left:auto"><button class="sandbox-reset" id="sandboxReset">Reset</button></span>
    </div>
    <canvas id="sandboxCanvas" width="400" height="400"></canvas>
    <div class="sandbox-info">
      <span id="brushInfo">Draw 브러시 · 드래그해서 칠해보세요</span>
      <span><span class="kbd">Ctrl</span>=반전 <span class="kbd">Shift</span>=Smooth</span>
    </div>
  </div>
  <div class="demo-hint">브러시를 바꿔가며 구를 얼굴 형태로 만들어 보세요</div>
</section>
```

- [ ] **Step 5: 탭 2 — 직접 해보기 (sandbox) — JavaScript**

Canvas 기반 2D 하이트맵 스컬프트 엔진:

```js
// ── Sculpt Sandbox Engine ──
(function() {
  var canvas = document.getElementById('sandboxCanvas');
  var ctx = canvas.getContext('2d');
  var SIZE = 100; // grid cells
  var height = []; // SIZE x SIZE float array
  var brushRadius = 8;
  var strength = 0.15;
  var currentBrush = 'draw';
  var isDrawing = false;
  var lastX = -1, lastY = -1;
  var ctrlHeld = false, shiftHeld = false;

  // Init heightmap with sphere bump in center
  function initHeightmap() {
    height = [];
    for (var y = 0; y < SIZE; y++) {
      height[y] = [];
      for (var x = 0; x < SIZE; x++) {
        var dx = x - SIZE/2, dy = y - SIZE/2;
        var dist = Math.sqrt(dx*dx + dy*dy);
        height[y][x] = Math.max(0, 1 - dist / (SIZE * 0.35));
      }
    }
  }

  function render() {
    var cw = canvas.width, ch = canvas.height;
    var cellW = cw / SIZE, cellH = ch / SIZE;
    var imgData = ctx.createImageData(cw, ch);
    for (var py = 0; py < ch; py++) {
      for (var px = 0; px < cw; px++) {
        var gx = Math.floor(px / cellW), gy = Math.floor(py / cellH);
        if (gx >= SIZE) gx = SIZE - 1;
        if (gy >= SIZE) gy = SIZE - 1;
        var h = Math.max(0, Math.min(1, height[gy][gx]));
        // Color: dark blue (low) → light gray (high)
        var r = Math.floor(30 + h * 200);
        var g = Math.floor(35 + h * 200);
        var b = Math.floor(50 + h * 180);
        var idx = (py * cw + px) * 4;
        imgData.data[idx] = r;
        imgData.data[idx+1] = g;
        imgData.data[idx+2] = b;
        imgData.data[idx+3] = 255;
      }
    }
    ctx.putImageData(imgData, 0, 0);
  }

  function applyBrush(gx, gy, brush, invert) {
    var r = brushRadius;
    var str = invert ? -strength : strength;
    for (var dy = -r; dy <= r; dy++) {
      for (var dx = -r; dx <= r; dx++) {
        var nx = gx + dx, ny = gy + dy;
        if (nx < 0 || nx >= SIZE || ny < 0 || ny >= SIZE) continue;
        var dist = Math.sqrt(dx*dx + dy*dy);
        if (dist > r) continue;
        var falloff = 1 - dist / r;

        switch (brush) {
          case 'draw':
            height[ny][nx] += str * falloff * 0.5;
            break;
          case 'clay':
            var target = height[gy][gx] + str * 0.3;
            height[ny][nx] += (target - height[ny][nx]) * falloff * 0.3;
            break;
          case 'inflate':
            height[ny][nx] += str * falloff * falloff * 0.4;
            break;
          case 'crease':
            var sharp = falloff * falloff * falloff;
            height[ny][nx] -= Math.abs(str) * sharp * 0.6 * (invert ? -1 : 1);
            break;
          case 'grab':
            // handled in mousemove with delta
            break;
          case 'snakehook':
            // handled in mousemove with delta
            break;
          case 'smooth':
            var sum = 0, cnt = 0;
            for (var sy = -1; sy <= 1; sy++) {
              for (var sx = -1; sx <= 1; sx++) {
                var snx = nx+sx, sny = ny+sy;
                if (snx >= 0 && snx < SIZE && sny >= 0 && sny < SIZE) {
                  sum += height[sny][snx]; cnt++;
                }
              }
            }
            height[ny][nx] += (sum/cnt - height[ny][nx]) * falloff * 0.5;
            break;
        }
      }
    }
  }

  function applyGrab(gx, gy, deltaX, deltaY) {
    var r = brushRadius;
    for (var dy = -r; dy <= r; dy++) {
      for (var dx = -r; dx <= r; dx++) {
        var nx = gx + dx, ny = gy + dy;
        if (nx < 0 || nx >= SIZE || ny < 0 || ny >= SIZE) continue;
        var dist = Math.sqrt(dx*dx + dy*dy);
        if (dist > r) continue;
        var falloff = 1 - dist / r;
        var sx = Math.round(nx - deltaX * falloff * 0.5);
        var sy = Math.round(ny - deltaY * falloff * 0.5);
        if (sx >= 0 && sx < SIZE && sy >= 0 && sy < SIZE) {
          height[ny][nx] = height[sy][sx];
        }
      }
    }
  }

  function getGridPos(e) {
    var rect = canvas.getBoundingClientRect();
    var px = (e.clientX - rect.left) * (canvas.width / rect.width);
    var py = (e.clientY - rect.top) * (canvas.height / rect.height);
    return { x: Math.floor(px / (canvas.width / SIZE)), y: Math.floor(py / (canvas.height / SIZE)) };
  }

  canvas.addEventListener('mousedown', function(e) {
    isDrawing = true;
    var pos = getGridPos(e);
    lastX = pos.x; lastY = pos.y;
    var brush = shiftHeld ? 'smooth' : currentBrush;
    if (brush !== 'grab' && brush !== 'snakehook') {
      applyBrush(pos.x, pos.y, brush, ctrlHeld);
    }
    render();
  });

  canvas.addEventListener('mousemove', function(e) {
    if (!isDrawing) return;
    var pos = getGridPos(e);
    var brush = shiftHeld ? 'smooth' : currentBrush;
    if (brush === 'grab' || brush === 'snakehook') {
      applyGrab(lastX, lastY, lastX - pos.x, lastY - pos.y);
    } else {
      applyBrush(pos.x, pos.y, brush, ctrlHeld);
    }
    lastX = pos.x; lastY = pos.y;
    render();
  });

  canvas.addEventListener('mouseup', function() { isDrawing = false; });
  canvas.addEventListener('mouseleave', function() { isDrawing = false; });

  // Touch support
  canvas.addEventListener('touchstart', function(e) {
    e.preventDefault();
    var t = e.touches[0];
    canvas.dispatchEvent(new MouseEvent('mousedown', { clientX: t.clientX, clientY: t.clientY }));
  }, { passive: false });
  canvas.addEventListener('touchmove', function(e) {
    e.preventDefault();
    var t = e.touches[0];
    canvas.dispatchEvent(new MouseEvent('mousemove', { clientX: t.clientX, clientY: t.clientY }));
  }, { passive: false });
  canvas.addEventListener('touchend', function() {
    canvas.dispatchEvent(new MouseEvent('mouseup'));
  });

  // Keyboard modifiers
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Control') ctrlHeld = true;
    if (e.key === 'Shift') shiftHeld = true;
  });
  document.addEventListener('keyup', function(e) {
    if (e.key === 'Control') ctrlHeld = false;
    if (e.key === 'Shift') shiftHeld = false;
  });

  // Brush selection
  var brushNames = {
    draw: 'Draw 브러시 · 드래그해서 칠해보세요',
    clay: 'Clay Strips · 넓은 면에 찰흙 띠를 붙여보세요',
    inflate: 'Inflate · 풍선처럼 부풀려보세요',
    crease: 'Crease · 홈을 파보세요',
    grab: 'Grab · 잡아서 끌어보세요',
    snakehook: 'Snake Hook · 끝을 잡고 늘여보세요',
    smooth: 'Smooth · 울퉁불퉁한 곳을 쓸어보세요'
  };
  document.querySelectorAll('.brush-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      document.querySelectorAll('.brush-btn').forEach(function(b) { b.classList.remove('is-active'); });
      btn.classList.add('is-active');
      currentBrush = btn.dataset.brush;
      document.getElementById('brushInfo').textContent = brushNames[currentBrush] || '';
    });
  });

  // Reset
  document.getElementById('sandboxReset').addEventListener('click', function() {
    initHeightmap();
    render();
  });

  initHeightmap();
  render();
})();
```

- [ ] **Step 6: 탭 3 — 비교 (visual)**

sculpt-basics.html의 시나리오 패턴을 재사용하되, 브러시 5종(Draw/Clay Strips/Inflate/Crease/Snake Hook) before-after 비교. Canvas 드로잉 함수는 sculpt-basics.html의 패턴을 따르되, 각 브러시에 맞게 after 이미지를 다르게 렌더링.

```html
<section class="panel" id="panel-visual" role="tabpanel">
  <div class="scenario-nav" id="scenarioNav2">
    <button class="scenario-btn active" data-scene2="clay">Clay Strips</button>
    <button class="scenario-btn" data-scene2="inflate">Inflate</button>
    <button class="scenario-btn" data-scene2="crease">Crease</button>
    <button class="scenario-btn" data-scene2="snakehook">Snake Hook</button>
  </div>
  <div class="scene-desc" id="scene-desc2">Clay Strips는 넓은 면 위에 찰흙 띠를 붙이듯이 층층이 쌓아요.</div>
  <div class="before-after">
    <div class="ba-panel"><canvas id="canvas-before2" width="280" height="160"></canvas><div class="ba-label">적용 전</div></div>
    <div class="ba-panel"><canvas id="canvas-after2" width="280" height="160"></canvas><div class="ba-label">적용 후</div></div>
  </div>
  <div class="cause-effect" id="cause-effect2"></div>
</section>
```

JavaScript: Canvas 드로잉 함수를 시나리오별로 구현. 패턴은 sculpt-basics.html의 `drawBaseSphere`, `drawDrawAfter` 등과 동일한 구조. 각 브러시에 맞는 시각적 표현:
- Clay Strips: 구 위에 가로 줄무늬 레이어
- Inflate: 구가 부풀어 오른 형태
- Crease: 구에 깊은 홈 라인
- Snake Hook: 구에서 뿔 모양으로 튀어나온 형태

- [ ] **Step 7: 탭 4 — 레시피 (recipe)**

```html
<section class="panel" id="panel-recipe" role="tabpanel">
  <h3 style="margin:0 0 14px;font-size:1rem">브러시 조합 워크플로우</h3>
  <div class="combo-section">
    <h4>얼굴 만들기</h4>
    <div class="combo-grid">
      <div class="combo-card"><div class="combo-name">1. Grab으로 큰 형태</div><div class="combo-desc">턱, 이마, 광대 위치를 잡아 당겨서 큰 비율을 정해요.</div></div>
      <div class="combo-card"><div class="combo-name">2. Clay Strips로 볼륨</div><div class="combo-desc">광대뼈, 이마 볼록한 부분에 찰흙을 층층이 쌓아요.</div></div>
      <div class="combo-card"><div class="combo-name">3. Crease로 디테일</div><div class="combo-desc">눈두덩, 코 옆 라인, 입술 경계를 날카롭게 잡아요.</div></div>
      <div class="combo-card"><div class="combo-name">4. Smooth로 마무리</div><div class="combo-desc">울퉁불퉁한 부분을 쓸어서 자연스럽게 정리해요.</div></div>
    </div>
  </div>
  <div class="combo-section">
    <h4>근육/관절 표현</h4>
    <div class="combo-grid">
      <div class="combo-card"><div class="combo-name">1. Inflate로 근육</div><div class="combo-desc">이두근, 허벅지 등 볼록한 부위를 부풀려요.</div></div>
      <div class="combo-card"><div class="combo-name">2. Crease로 경계</div><div class="combo-desc">근육과 근육 사이 홈, 관절 꺾임을 파요.</div></div>
      <div class="combo-card"><div class="combo-name">3. Clay로 보정</div><div class="combo-desc">부족한 볼륨을 밀어 쌓으며 채워요.</div></div>
      <div class="combo-card"><div class="combo-name">4. Smooth로 블렌딩</div><div class="combo-desc">경계를 자연스럽게 녹여요.</div></div>
    </div>
  </div>
  <div class="combo-section">
    <h4>뿔/촉수 만들기</h4>
    <div class="combo-grid">
      <div class="combo-card"><div class="combo-name">1. Snake Hook으로 끌기</div><div class="combo-desc">구 표면에서 길게 끌어내요.</div></div>
      <div class="combo-card"><div class="combo-name">2. Draw로 굵기 보정</div><div class="combo-desc">가늘어진 부분을 올려서 굵기를 맞춰요.</div></div>
      <div class="combo-card"><div class="combo-name">3. Crease로 질감</div><div class="combo-desc">표면에 비늘이나 줄무늬 느낌을 넣어요.</div></div>
      <div class="combo-card"><div class="combo-name">4. Smooth로 마감</div><div class="combo-desc">끝부분을 자연스럽게 정리해요.</div></div>
    </div>
  </div>
</section>
```

- [ ] **Step 8: 탭 5 — 퀴즈 (quiz)**

sculpt-basics.html의 `initQuiz()` 함수를 그대로 복사하고, 퀴즈 데이터만 변경:

```js
initQuiz([
  {
    question: "넓은 면에 찰흙을 층층이 쌓는 느낌의 브러시는?",
    options: ["Draw", "Clay Strips", "Inflate", "Crease"],
    answer: 1,
    explanation: "Clay Strips는 넓은 면 위에 평평한 찰흙 띠를 붙이듯이 작동합니다."
  },
  {
    question: "관절이나 눈 라인처럼 날카로운 홈을 파는 브러시는?",
    options: ["Smooth", "Grab", "Crease", "Inflate"],
    answer: 2,
    explanation: "Crease는 날카로운 홈과 주름을 만드는 전용 브러시입니다. Shift+C로 빠르게 선택할 수 있어요."
  },
  {
    question: "뿔이나 촉수처럼 끝을 잡고 길게 늘이는 브러시는?",
    options: ["Grab", "Snake Hook", "Draw", "Clay"],
    answer: 1,
    explanation: "Snake Hook은 끝점만 따라오며 길게 늘어나는 브러시입니다. K키로 빠르게 선택할 수 있어요."
  },
  {
    question: "Sculpt 중 어떤 브러시를 쓰든 Shift를 누르면?",
    options: ["브러시 크기가 커진다", "반전(파내기)된다", "임시 Smooth로 전환된다", "Grab으로 전환된다"],
    answer: 2,
    explanation: "Shift를 누르고 있으면 어떤 브러시를 사용 중이든 임시로 Smooth 브러시로 전환됩니다."
  },
  {
    question: "볼이나 근육을 풍선처럼 부풀리는 브러시는?",
    options: ["Draw", "Clay Strips", "Inflate", "Snake Hook"],
    answer: 2,
    explanation: "Inflate는 표면을 바깥으로 밀어내 부풀리는 효과를 줍니다."
  },
  {
    question: "얼굴 조각 순서로 가장 적절한 것은?",
    options: [
      "Crease → Smooth → Grab → Clay",
      "Grab → Clay Strips → Crease → Smooth",
      "Smooth → Draw → Inflate → Grab",
      "Draw → Snake Hook → Crease → Clay"
    ],
    answer: 1,
    explanation: "큰 형태(Grab) → 볼륨(Clay Strips) → 디테일(Crease) → 정리(Smooth) 순서가 일반적입니다."
  }
]);
```

- [ ] **Step 9: Tab switching JS + 전체 조립**

탭 전환 JS는 sculpt-basics.html과 동일 패턴. 모든 탭, 패널, 시나리오, 퀴즈 코드를 하나의 `sculpt-brushes.html` 파일로 조립.

- [ ] **Step 10: 브라우저에서 카드 확인**

Run: `http://localhost:8772/assets/showme/sculpt-brushes.html` 접속
Expected: 5개 탭 모두 동작, 특히 "직접 해보기" 탭에서 Canvas 드래그 시 하이트맵이 실시간 변경

- [ ] **Step 11: Commit**

```bash
git add course-site/assets/showme/sculpt-brushes.html
git commit -m "feat(showme): add sculpt-brushes card with interactive sandbox"
```

---

### Task 4: ai-prompt-design.html — AI 프롬프트 설계 카드

**Files:**
- Create: `course-site/assets/showme/ai-prompt-design.html`
- Reference: `course-site/assets/showme/_template.html`

- [ ] **Step 1: 전체 HTML 생성**

`_template.html` CSS 복사 + 4탭 구성 (개념 이해 / 시각적 비교 / 언제 쓰나요? / 퀴즈).

탭 1 "개념 이해": 프롬프트 공식 카드
```html
<div class="concept-grid">
  <div class="concept-card">
    <h3>프롬프트 공식</h3>
    <p><strong>[형태]</strong> + <strong>[스타일]</strong> + <strong>[재질감]</strong> + <strong>[색상]</strong> + <strong>3D model</strong></p>
    <div class="analogy">주문서 — AI한테 "이런 느낌으로 만들어줘"라고 최대한 구체적으로 쓰는 거예요</div>
  </div>
  <div class="concept-card">
    <h3>슬롯별 키워드 예시</h3>
    <ul>
      <li><strong>형태:</strong> humanoid robot, animal character, mechanical arm, organic creature</li>
      <li><strong>스타일:</strong> futuristic, steampunk, minimalist, cartoon, realistic</li>
      <li><strong>재질감:</strong> metallic, glossy plastic, matte ceramic, organic tissue</li>
      <li><strong>색상:</strong> teal and silver, warm orange, monochrome white</li>
    </ul>
  </div>
  <div class="concept-card">
    <h3>Bad → Good 변환</h3>
    <ul>
      <li><span style="color:var(--danger-soft)">Bad:</span> "robot" → <span style="color:var(--success-soft)">Good:</span> "humanoid robot, sleek futuristic design, metallic silver surface, 3D model"</li>
      <li><span style="color:var(--danger-soft)">Bad:</span> "cute animal" → <span style="color:var(--success-soft)">Good:</span> "round cat character, cartoon style, matte ceramic texture, pastel pink, 3D model"</li>
    </ul>
  </div>
</div>
```

탭 2 "시각적 비교": 프롬프트 길이에 따른 결과 차이를 cause-effect 패턴으로 표현.

탭 3 "언제 쓰나요?": 무드보드 → 키워드 추출 → 프롬프트 변환 3단계 workflow를 combo-grid로.

탭 4 "퀴즈":
```js
initQuiz([
  {
    question: "다음 중 AI 3D 생성 프롬프트로 가장 좋은 것은?",
    options: [
      "로봇",
      "로봇 만들어줘",
      "humanoid robot, sleek design, metallic surface, 3D model",
      "make a cool robot for me please"
    ],
    answer: 2,
    explanation: "형태+스타일+재질감+3D model 키워드를 영어로 구체적으로 넣을수록 결과가 좋아요."
  },
  {
    question: "무드보드에서 '반짝이는 청록색 로봇'을 발견했을 때, 재질감 키워드로 적절한 것은?",
    options: ["blue", "shiny", "glossy metallic", "teal color"],
    answer: 2,
    explanation: "'반짝이는' 느낌은 glossy metallic이 가장 정확하게 전달해요. 색상은 별도 슬롯으로 분리하세요."
  },
  {
    question: "같은 프롬프트로 결과가 마음에 안 들 때 가장 효과적인 방법은?",
    options: [
      "같은 프롬프트로 다시 생성",
      "완전히 새로운 프롬프트 작성",
      "키워드 하나만 바꿔서 재생성",
      "다른 AI 서비스로 변경"
    ],
    answer: 2,
    explanation: "키워드 하나만 바꾸면 어떤 단어가 결과에 영향을 주는지 비교할 수 있어요."
  }
]);
```

- [ ] **Step 2: 브라우저 확인**

Run: `http://localhost:8772/assets/showme/ai-prompt-design.html`
Expected: 4탭 정상 표시, 퀴즈 작동

- [ ] **Step 3: Commit**

```bash
git add course-site/assets/showme/ai-prompt-design.html
git commit -m "feat(showme): add ai-prompt-design card"
```

---

### Task 5: ai-3d-generation.html — AI 3D 생성 워크플로우 카드

**Files:**
- Create: `course-site/assets/showme/ai-3d-generation.html`
- Reference: `course-site/assets/showme/_template.html`

- [ ] **Step 1: 전체 HTML 생성**

`_template.html` CSS 복사 + 4탭 구성.

탭 1 "개념 이해":
```html
<div class="concept-grid">
  <div class="concept-card">
    <h3>AI 3D 생성이란?</h3>
    <p>텍스트 프롬프트를 넣으면 AI가 3D 메쉬를 자동으로 생성해요. 완벽하지 않지만, 아이디어를 빠르게 3D로 확인하는 데 유용해요.</p>
    <div class="analogy">AI = 초벌 장인 — 큰 덩어리를 잡아주면 우리가 다듬기만 하면 돼요</div>
  </div>
  <div class="concept-card">
    <h3>Meshy vs Tripo</h3>
    <ul>
      <li><strong>Meshy</strong> — 텍스트→3D + 이미지→3D 모두 지원. 무료 크레딧 있음</li>
      <li><strong>Tripo</strong> — 빠른 생성 속도. 이미지→3D가 강점</li>
      <li>둘 다 .glb 파일로 다운로드 → Blender에서 Import</li>
    </ul>
  </div>
</div>
```

탭 2 "시각적 비교": 생성→다운로드→Import→정리 4단계를 combo-grid 워크플로우로.

탭 3 "언제 쓰나요?":
```html
<div class="concept-card">
  <h3>Import 후 체크리스트</h3>
  <ul>
    <li><strong>크기</strong> — S키로 적절한 크기로 맞추고 Ctrl+A → Scale 적용</li>
    <li><strong>원점</strong> — Right-click → Set Origin → Origin to Geometry</li>
    <li><strong>폴리곤 수</strong> — Viewport Overlay → Statistics로 확인. 수만 개 이상이면 Decimate 필요</li>
    <li><strong>노멀</strong> — Mesh Cleaner 2로 뒤집힌 노멀 자동 수정</li>
  </ul>
</div>
<div class="concept-card">
  <h3>애드온 설치법</h3>
  <ul>
    <li>Edit → Preferences → Add-ons → Install</li>
    <li>다운로드한 .zip 파일 선택 → 체크박스 활성화</li>
    <li>Mesh Cleaner: N패널 → Mesh Cleaner 탭에서 실행</li>
    <li>QRemeshify: Properties → Object Data → QRemeshify 패널</li>
  </ul>
</div>
```

탭 4 "퀴즈":
```js
initQuiz([
  {
    question: "Meshy에서 생성한 파일을 Blender로 가져오려면?",
    options: [
      "File → Open",
      "File → Import → glTF (.glb/.gltf)",
      "File → Append",
      "드래그 앤 드롭"
    ],
    answer: 1,
    explanation: "AI 생성 서비스는 보통 .glb 형식을 제공하고, Blender에서는 File → Import → glTF로 가져와요."
  },
  {
    question: "Import한 AI 메쉬의 크기가 너무 클 때 가장 먼저 할 일은?",
    options: [
      "Decimate 적용",
      "Sculpt Mode에서 줄이기",
      "S키로 크기 조절 후 Ctrl+A → Scale 적용",
      "새로 생성하기"
    ],
    answer: 2,
    explanation: "S키로 크기를 맞추고 Ctrl+A로 Scale을 적용해야 이후 Modifier가 정상 작동해요."
  },
  {
    question: "AI 메쉬 정리에서 Mesh Cleaner 2가 자동으로 처리하는 것이 아닌 것은?",
    options: [
      "중복 버텍스 제거",
      "뒤집힌 노멀 수정",
      "토폴로지를 쿼드로 변환",
      "미사용 Material 제거"
    ],
    answer: 2,
    explanation: "쿼드 리메시는 QRemeshify의 역할이에요. Mesh Cleaner는 정리, QRemeshify는 토폴로지 변환을 담당해요."
  }
]);
```

- [ ] **Step 2: 브라우저 확인**

Run: `http://localhost:8772/assets/showme/ai-3d-generation.html`
Expected: 4탭 정상 표시, 퀴즈 작동

- [ ] **Step 3: Commit**

```bash
git add course-site/assets/showme/ai-3d-generation.html
git commit -m "feat(showme): add ai-3d-generation card"
```

---

### Task 6: 전체 통합 검증

**Files:** (모두 이전 Task에서 수정/생성됨)

- [ ] **Step 1: week 5 페이지 프리뷰 확인**

Run: `http://localhost:8772/week.html?week=5` 새로고침
Expected:
- 스텝이 6개로 표시
- 순서: Sculpt 기초 → 브러시 심화 → Remesh+Decimate → 무드보드 → AI 러프 → AI 정리
- 각 스텝에 showme 카드 링크가 표시됨
- Assignment가 "내 프로젝트 첫 3D 러프"로 변경됨

- [ ] **Step 2: showme 카드 3장 각각 열어서 동작 확인**

- `sculpt-brushes.html`: 5탭 전환, Canvas 샌드박스 드래그 동작, 퀴즈 동작
- `ai-prompt-design.html`: 4탭 전환, 퀴즈 동작
- `ai-3d-generation.html`: 4탭 전환, 퀴즈 동작

- [ ] **Step 3: library 페이지에서 카드 검색 확인**

Run: `http://localhost:8772/library.html` → Sculpting 카테고리
Expected: `sculpt-brushes`가 Sculpting 카테고리에 표시

- [ ] **Step 4: 최종 Commit (필요시)**

통합 검증 중 발견된 수정 사항 반영 후 커밋.
