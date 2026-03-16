# Show Me 도구 라이브러리 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** `library.html` — showme 카드 전체를 실시간 검색 + 카테고리 탭으로 필터링하고, 클릭 시 모달로 여는 독립 페이지 구현

**Architecture:** `_registry.js`를 그대로 재활용해 카드 그리드를 동적 렌더링. `library.html` 내 인라인 카테고리 매핑으로 탭 필터 구성. 모달은 week.html의 showme 모달 디자인을 복제.

**Tech Stack:** Vanilla HTML/CSS/JS, `assets/tokens.css`, `assets/showme/_registry.js`

---

## Task 1: `library.html` 기본 셸 생성

**Files:**
- Create: `course-site/library.html`

**Step 1: 파일 생성 — HTML 셸 + tokens.css 연결**

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>도구 라이브러리 — RPD</title>
  <link rel="stylesheet" href="assets/tokens.css" />
</head>
<body>
  <div class="page-shell">
    <p style="color:var(--muted);padding:40px">라이브러리 준비 중</p>
  </div>
  <script src="assets/showme/_registry.js"></script>
</body>
</html>
```

**Step 2: 브라우저에서 확인**

`course-site/library.html`을 브라우저로 열어 배경색(#0a0a0a 다크)과 "라이브러리 준비 중" 텍스트가 보이는지 확인.

**Step 3: Commit**

```bash
git add course-site/library.html
git commit -m "feat: library.html 기본 셸 생성"
```

---

## Task 2: 헤더 + 검색바 UI

**Files:**
- Modify: `course-site/library.html`

**Step 1: 헤더 HTML 추가**

`<body>` 내 `.page-shell` 안에 교체:

```html
<div class="page-shell">
  <header class="lib-header">
    <div class="lib-header-inner">
      <a href="index.html" class="lib-back">← 홈</a>
      <div>
        <h1 class="lib-title">도구 라이브러리</h1>
        <p class="lib-subtitle">Blender 도구·모디파이어 개념 카드 모음</p>
      </div>
      <div class="lib-search-wrap">
        <input
          class="lib-search"
          id="libSearch"
          type="search"
          placeholder="예: Array, Mirror, UV..."
          autocomplete="off"
        />
        <span class="lib-count" id="libCount"></span>
      </div>
    </div>
  </header>
  <main class="lib-main" id="libMain"></main>
</div>
```

**Step 2: 헤더 스타일 추가 (`<style>` 태그를 `<head>` 안에)**

```css
/* ── Layout ── */
.lib-header {
  position: sticky; top: 0; z-index: 10;
  background: rgba(10,10,10,.85);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--line);
  padding: 0 20px;
}
.lib-header-inner {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 18px 0;
  display: flex; flex-direction: column; gap: 14px;
}
.lib-back {
  color: var(--muted); font-size: .84rem;
  transition: color .14s;
}
.lib-back:hover { color: var(--text); }
.lib-title {
  margin: 0; font-size: clamp(1.4rem, 3vw, 2rem);
  font-family: var(--font-display); font-weight: 650;
  letter-spacing: -.02em;
}
.lib-subtitle {
  margin: 4px 0 0; color: var(--muted-strong); font-size: .9rem;
}
.lib-search-wrap {
  display: flex; align-items: center; gap: 12px;
}
.lib-search {
  flex: 1; padding: 10px 14px;
  border-radius: 999px;
  border: 1px solid var(--line-strong);
  background: rgba(255,255,255,.05);
  color: var(--text); font: inherit; font-size: .9rem;
  outline: none; transition: border-color .14s;
}
.lib-search:focus { border-color: var(--key); }
.lib-search::placeholder { color: var(--muted); }
.lib-count {
  font-size: .8rem; color: var(--muted); white-space: nowrap;
}
.lib-main {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 24px 20px 80px;
}
```

**Step 3: 브라우저 확인**

스티키 헤더, 검색바, 홈 링크가 보이는지 확인. 다크 배경 유지.

**Step 4: Commit**

```bash
git add course-site/library.html
git commit -m "feat: 도구 라이브러리 헤더 + 검색바 UI"
```

---

## Task 3: 카테고리 탭 UI

**Files:**
- Modify: `course-site/library.html`

**Step 1: 카테고리 탭 HTML을 `<main>` 위에 추가**

```html
<nav class="lib-tabs" id="libTabs" role="tablist"></nav>
```

`.lib-main` 바로 위, `.page-shell` 안.

**Step 2: 탭 스타일 추가**

```css
.lib-tabs {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 20px;
  display: flex; gap: 0;
  overflow-x: auto;
  border-bottom: 1px solid var(--line);
}
.lib-tabs::-webkit-scrollbar { display: none; }
.lib-tab {
  padding: 12px 16px;
  font-size: .84rem; font-weight: 500;
  color: var(--muted); cursor: pointer;
  border: none; border-bottom: 2px solid transparent;
  white-space: nowrap;
  transition: color .14s, border-color .14s;
  background: none; font-family: inherit;
}
.lib-tab:hover { color: var(--muted-strong); }
.lib-tab.is-active {
  color: var(--key-soft);
  border-bottom-color: var(--key);
}
```

**Step 3: 탭 데이터 JS (카테고리 매핑)**

`<script>` 태그 안에 (반드시 `_registry.js` 로드 후):

```js
// 카테고리 매핑 — ID → 카테고리명
const CATEGORY_MAP = {
  "viewport-navigation": "Edit Mode",
  "transform-grs":       "Edit Mode",
  "edit-mode":           "Edit Mode",
  "edit-mode-tools":     "Edit Mode",
  "extrude":             "Edit Mode",
  "loop-cut":            "Edit Mode",
  "inset":               "Edit Mode",
  "bevel-tool":          "Edit Mode",

  "array-modifier":          "Generate Modifiers",
  "bevel-modifier":          "Generate Modifiers",
  "boolean-modifier":        "Generate Modifiers",
  "build-modifier":          "Generate Modifiers",
  "curve-to-tube":           "Generate Modifiers",
  "decimate-modifier":       "Generate Modifiers",
  "edge-split-modifier":     "Generate Modifiers",
  "mask-modifier":           "Generate Modifiers",
  "mirror-modifier":         "Generate Modifiers",
  "multiresolution-modifier":"Generate Modifiers",
  "remesh-modifier":         "Generate Modifiers",
  "scatter-on-surface":      "Generate Modifiers",
  "screw-modifier":          "Generate Modifiers",
  "skin-modifier":           "Generate Modifiers",
  "solidify-modifier":       "Generate Modifiers",
  "subdivision-surface":     "Generate Modifiers",
  "triangulate-modifier":    "Generate Modifiers",
  "volume-to-mesh":          "Generate Modifiers",
  "weld-modifier":           "Generate Modifiers",
  "wireframe-modifier":      "Generate Modifiers",

  "weighted-normal":    "Normals",

  "transform-apply":    "기타",
  "simple-deform":      "기타",
  "bevel-tool-vs-modifier": "기타",
  "join-separate":      "기타",
  "origin-vs-3dcursor": "기타",

  "sculpt-basics":      "Sculpting",

  "material-basics":    "Material",
  "principled-bsdf":    "Material",
  "shader-editor":      "Material",

  "uv-unwrapping":      "UV",
  "uv-editor":          "UV",

  "light-types":        "Lighting",
  "hdri-lighting":      "Lighting",
  "three-point-light":  "Lighting",

  "keyframe-basics":    "Animation",
  "graph-editor":       "Animation",

  "armature-basics":    "Rigging",
  "weight-paint":       "Rigging",

  "render-settings":    "Rendering",
  "compositing-basics": "Rendering",
};

const CATEGORY_ORDER = [
  "전체", "Edit Mode", "Generate Modifiers", "Normals",
  "Sculpting", "Material", "UV", "Lighting",
  "Animation", "Rigging", "Rendering", "기타"
];

// 탭 렌더링
function buildTabs() {
  const tabsEl = document.getElementById("libTabs");
  CATEGORY_ORDER.forEach(function(cat, i) {
    var btn = document.createElement("button");
    btn.className = "lib-tab" + (i === 0 ? " is-active" : "");
    btn.textContent = cat;
    btn.dataset.cat = cat;
    btn.setAttribute("role", "tab");
    btn.addEventListener("click", function() {
      document.querySelectorAll(".lib-tab").forEach(function(t) {
        t.classList.remove("is-active");
      });
      btn.classList.add("is-active");
      filterCards();
    });
    tabsEl.appendChild(btn);
  });
}
buildTabs();
```

**Step 4: 브라우저 확인**

탭이 가로로 늘어서 보이고, "전체"가 파란 밑줄 활성 상태인지 확인.

**Step 5: Commit**

```bash
git add course-site/library.html
git commit -m "feat: 도구 라이브러리 카테고리 탭"
```

---

## Task 4: 카드 그리드 렌더링 + 필터 로직

**Files:**
- Modify: `course-site/library.html`

**Step 1: 카드 그리드 스타일 추가**

```css
.lib-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 12px;
  margin-top: 20px;
}
.lib-card {
  display: flex; flex-direction: column; align-items: center;
  gap: 8px; padding: 18px 12px;
  border-radius: var(--radius-md);
  border: 1px solid var(--line);
  background: var(--surface);
  cursor: pointer;
  transition: border-color .14s, background .14s;
  text-align: center;
}
.lib-card:hover {
  border-color: var(--key);
  background: rgba(10,132,255,.06);
}
.lib-card-icon { font-size: 2rem; line-height: 1; }
.lib-card-label {
  font-size: .84rem; font-weight: 500; color: var(--text); line-height: 1.4;
}
.lib-card-id {
  font-size: .72rem; color: var(--muted);
}
.lib-empty {
  grid-column: 1 / -1;
  padding: 60px 0; text-align: center; color: var(--muted);
  font-size: .9rem;
}
```

**Step 2: 카드 렌더링 + 필터 JS**

`<script>` 태그 안에 추가:

```js
// 카드 빌드
function buildCards() {
  var main = document.getElementById("libMain");
  var grid = document.createElement("div");
  grid.className = "lib-grid";
  grid.id = "libGrid";
  main.appendChild(grid);

  Object.keys(SHOWME_REGISTRY).forEach(function(id) {
    var meta = SHOWME_REGISTRY[id];
    var card = document.createElement("div");
    card.className = "lib-card";
    card.dataset.id = id;
    card.dataset.cat = CATEGORY_MAP[id] || "기타";

    var icon = document.createElement("span");
    icon.className = "lib-card-icon";
    icon.textContent = meta.icon;

    var label = document.createElement("span");
    label.className = "lib-card-label";
    label.textContent = meta.label;

    var idEl = document.createElement("span");
    idEl.className = "lib-card-id";
    idEl.textContent = id;

    card.appendChild(icon);
    card.appendChild(label);
    card.appendChild(idEl);
    card.addEventListener("click", function() { openShowMe(id); });
    grid.appendChild(card);
  });

  updateCount();
}

// 필터
function filterCards() {
  var query = document.getElementById("libSearch").value.toLowerCase().trim();
  var activeCat = document.querySelector(".lib-tab.is-active").dataset.cat;
  var cards = document.querySelectorAll(".lib-card");
  var visible = 0;

  cards.forEach(function(card) {
    var id    = card.dataset.id;
    var meta  = SHOWME_REGISTRY[id];
    var cat   = card.dataset.cat;

    var matchCat   = activeCat === "전체" || cat === activeCat;
    var matchQuery = !query
      || meta.label.toLowerCase().includes(query)
      || id.toLowerCase().includes(query);

    card.style.display = (matchCat && matchQuery) ? "" : "none";
    if (matchCat && matchQuery) visible++;
  });

  updateCount(visible);

  // 결과 없음 안내
  var grid = document.getElementById("libGrid");
  var empty = grid.querySelector(".lib-empty");
  if (visible === 0) {
    if (!empty) {
      var el = document.createElement("p");
      el.className = "lib-empty";
      el.textContent = "검색 결과가 없습니다";
      grid.appendChild(el);
    }
  } else {
    if (empty) empty.remove();
  }
}

function updateCount(n) {
  var total = Object.keys(SHOWME_REGISTRY).length;
  var shown = (n === undefined) ? total : n;
  document.getElementById("libCount").textContent =
    shown === total ? total + "개 도구" : shown + " / " + total + "개";
}

// 이벤트 연결
document.getElementById("libSearch").addEventListener("input", filterCards);

buildCards();
```

**Step 3: 브라우저 확인**

- 카드 그리드가 표시되는지
- 검색창에 "array" 입력 시 Array 카드만 보이는지
- 탭 클릭 시 해당 카테고리 카드만 보이는지
- 탭 + 검색 동시에 AND 필터 동작하는지

**Step 4: Commit**

```bash
git add course-site/library.html
git commit -m "feat: 도구 카드 그리드 렌더링 + 실시간 검색/카테고리 필터"
```

---

## Task 5: showme 모달 추가

**Files:**
- Modify: `course-site/library.html`

**Step 1: 모달 HTML 추가 (`</div>` — `.page-shell` 닫기 전)**

```html
<!-- Show Me Modal (week.html과 동일 디자인) -->
<div class="showme-overlay" id="showmeOverlay" aria-hidden="true">
  <div class="showme-modal">
    <div class="showme-modal-header">
      <span class="showme-modal-title" id="showmeTitle"></span>
      <button class="showme-close" id="showmeClose" aria-label="닫기" type="button">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
          <path d="M4 4L12 12M12 4L4 12" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
        </svg>
      </button>
    </div>
    <iframe class="showme-iframe" id="showmeIframe"
            sandbox="allow-scripts allow-same-origin"
            title="Show Me Widget"></iframe>
  </div>
</div>
```

**Step 2: 모달 스타일 추가 (week.html에서 복사)**

```css
.showme-overlay {
  display: none; position: fixed; inset: 0;
  z-index: 100;
  background: rgba(0,0,0,.72);
  backdrop-filter: blur(8px);
  justify-content: center; align-items: center;
  padding: 20px;
}
.showme-overlay.is-open { display: flex; }
.showme-modal {
  width: min(720px, 100%);
  height: min(85vh, 640px);
  border-radius: var(--radius-lg);
  border: 1px solid rgba(255,255,255,.12);
  background: var(--surface);
  box-shadow: 0 24px 80px rgba(0,0,0,.6);
  display: flex; flex-direction: column;
  overflow: hidden;
  animation: showme-in .22s ease;
}
@keyframes showme-in {
  from { opacity: 0; transform: scale(.97) translateY(8px); }
  to   { opacity: 1; transform: scale(1) translateY(0); }
}
.showme-modal-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 14px 18px;
  border-bottom: 1px solid var(--line);
  flex-shrink: 0;
}
.showme-modal-title { font-size: .9rem; font-weight: 600; color: var(--text); }
.showme-close {
  display: grid; place-items: center;
  width: 32px; height: 32px; border-radius: 8px;
  border: 1px solid var(--line);
  background: rgba(255,255,255,.04);
  color: var(--muted-strong); cursor: pointer;
  transition: background .14s, color .14s;
}
.showme-close:hover { background: rgba(255,255,255,.09); color: var(--text); }
.showme-iframe { flex: 1; width: 100%; border: none; background: var(--bg); }
@media (max-width: 720px) {
  .showme-overlay { padding: 0; }
  .showme-modal { width: 100%; height: 100%; border-radius: 0; border: none; }
}
```

**Step 3: 모달 JS 추가**

```js
function openShowMe(widgetId) {
  var meta = SHOWME_REGISTRY[widgetId] || { label: widgetId, icon: "📖" };
  document.getElementById("showmeTitle").textContent = meta.icon + " " + meta.label;
  document.getElementById("showmeIframe").src =
    "assets/showme/" + widgetId + ".html?wid=" + widgetId;
  var overlay = document.getElementById("showmeOverlay");
  overlay.classList.add("is-open");
  overlay.setAttribute("aria-hidden", "false");
}

function closeShowMe() {
  var overlay = document.getElementById("showmeOverlay");
  overlay.classList.remove("is-open");
  overlay.setAttribute("aria-hidden", "true");
  document.getElementById("showmeIframe").src = "";
}

document.getElementById("showmeClose").addEventListener("click", closeShowMe);
document.getElementById("showmeOverlay").addEventListener("click", function(e) {
  if (e.target === this) closeShowMe();
});
document.addEventListener("keydown", function(e) {
  if (e.key === "Escape") closeShowMe();
});
```

**Step 4: 브라우저 확인**

- 카드 클릭 시 모달 열리는지
- 제목에 아이콘 + 한글 라벨 표시되는지
- iframe에 카드 내용 로드되는지
- ESC / X버튼 / 배경 클릭으로 닫히는지

**Step 5: Commit**

```bash
git add course-site/library.html
git commit -m "feat: showme 모달 연동"
```

---

## Task 6: week.html 네비게이션 링크 추가

**Files:**
- Modify: `course-site/week.html`

**Step 1: week.html footer 링크 옆에 라이브러리 링크 추가**

`week.html`의 `<footer class="page-footer">` 찾아서:

```html
<!-- 기존 -->
<div>Robot Product Design 2026 · <a href="index.html" style="color:var(--key-soft)">← 전체 목록</a></div>

<!-- 변경 후 -->
<div>
  Robot Product Design 2026 ·
  <a href="index.html" style="color:var(--key-soft)">← 전체 목록</a>
  · <a href="library.html" style="color:var(--key-soft)">도구 라이브러리</a>
</div>
```

**Step 2: 브라우저 확인**

week.html 하단에 "도구 라이브러리" 링크가 표시되고, 클릭 시 library.html로 이동하는지 확인.

**Step 3: Commit**

```bash
git add course-site/week.html
git commit -m "feat: week.html footer에 도구 라이브러리 링크 추가"
```

---

## Task 7: 반응형 + 최종 점검

**Files:**
- Modify: `course-site/library.html`

**Step 1: 모바일 반응형 스타일 추가**

```css
@media (max-width: 600px) {
  .lib-grid { grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 8px; }
  .lib-card { padding: 14px 8px; }
  .lib-card-icon { font-size: 1.6rem; }
  .lib-card-label { font-size: .78rem; }
  .lib-card-id { display: none; }
  .lib-main { padding: 16px 12px 60px; }
}
```

**Step 2: 최종 점검 체크리스트**

- [ ] 전체 카드 표시 (56개)
- [ ] 검색 "mirror" → Mirror Modifier 카드만 표시
- [ ] 탭 "UV" → uv-unwrapping, uv-editor 2장만 표시
- [ ] 탭 "Generate Modifiers" + 검색 "bevel" → Bevel Modifier 1개
- [ ] 검색어 지우면 탭 기준 전체 복원
- [ ] 카드 클릭 → 모달 열림, iframe 내용 로드
- [ ] ESC로 모달 닫힘
- [ ] 모바일(375px)에서 레이아웃 깨지지 않음

**Step 3: Commit**

```bash
git add course-site/library.html
git commit -m "feat: 도구 라이브러리 반응형 스타일 완성"
```

---

## Task 8: PR 생성

```bash
git push -u origin claude/cool-burnell
gh pr create \
  --title "feat: Show Me 도구 라이브러리 페이지 (library.html)" \
  --body "## 변경 사항
- \`course-site/library.html\` 신규: showme 카드 전체 검색/브라우징 페이지
- 실시간 텍스트 검색 + 카테고리 탭 필터 (AND 조건)
- 카드 클릭 시 모달로 위젯 열기 (기존 week.html 모달 디자인 재사용)
- week.html footer에 라이브러리 링크 추가
- \`_registry.js\` 무수정 — 카드 추가 시 자동 반영"
```
