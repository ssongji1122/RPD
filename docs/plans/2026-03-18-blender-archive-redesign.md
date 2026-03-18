# Blender Archive Redesign Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** `library.html`을 블렌더 아카이브 메인으로 승격 (주차 필터 추가), `week.html`은 핵심 실습 가이드로 슬림화 (부가 섹션들을 "이번 주 참고자료" 아코디언으로 통합)

**Architecture:**
- `_registry.js`에 `week` 메타데이터 추가 → library의 주차 필터가 이 데이터를 읽음
- `library.html`에 주차 필터 UI 추가 (카테고리 탭 위에 주차 칩 행)
- `week.html`에서 shortcuts/explore/mistakes/videos/docs 5개 섹션을 `<details>` 아코디언 하나로 통합, 내부를 서브섹션으로 목차화

**Tech Stack:** Vanilla JS, HTML/CSS, `course-site/assets/tokens.css`, `course-site/assets/showme/_registry.js`, `course-site/data/curriculum.js`

---

## Phase 1: `_registry.js` — week 메타데이터 추가

**파일:** `course-site/assets/showme/_registry.js`

현재 `{ label, icon }` → `{ label, icon, week }` 으로 확장.
`week`는 숫자 (주요 주차). 특정 주차 없는 카드는 `0` (일반 개념).

### Task 1: _registry.js에 week 필드 추가

**Step 1: 백업 없이 직접 수정 — 각 항목에 week 추가**

```js
// BEFORE
"image-reference": { label: "이미지 레퍼런스 설정", icon: "🖼️" },

// AFTER
"image-reference": { label: "이미지 레퍼런스 설정", icon: "🖼️", week: 3 },
```

주차별 매핑 기준:
| week | 카드 IDs |
|------|---------|
| 2 | blender-preferences, viewport-navigation, transform-grs, transform-orientation, pivot-point, snap, viewport-shading, xray-opacity, edit-mode |
| 3 | image-reference, edit-mode-tools, extrude, loop-cut, inset, bevel-tool, array-modifier, bevel-modifier, boolean-modifier, mirror-modifier, solidify-modifier, subdivision-surface, weighted-normal, proportional-editing, transform-apply, simple-deform, join-separate |
| 4 | build-modifier, curve-to-tube, decimate-modifier, edge-split-modifier, mask-modifier, multiresolution-modifier, remesh-modifier, scatter-on-surface, screw-modifier, skin-modifier, triangulate-modifier, volume-to-mesh, weld-modifier, wireframe-modifier |
| 5 | sculpt-basics |
| 6 | material-basics, principled-bsdf, shader-editor |
| 7 | uv-unwrapping, uv-editor |
| 9 | light-types, hdri-lighting, three-point-light |
| 10 | keyframe-basics, graph-editor |
| 11 | armature-basics, weight-paint |
| 13 | render-settings, compositing-basics |
| 0 | origin-vs-3dcursor, poly-circle, box-rounding, bevel-tool-vs-modifier |

**Step 2: 검증 — 브라우저 콘솔에서 확인**
```js
Object.values(SHOWME_REGISTRY).filter(v => v.week === undefined)
// 결과: [] (빈 배열이어야 함)
```

**Step 3: Commit**
```bash
git add course-site/assets/showme/_registry.js
git commit -m "feat: add week metadata to showme registry"
```

---

## Phase 2: `library.html` — 주차 필터 추가

**파일:** `course-site/library.html`

### Task 2: 주차 필터 UI (칩 행) 추가

현재 구조: `lib-header` → `lib-tabs(카테고리)` → `lib-main`
변경 후: `lib-header` → `lib-week-filter(주차 칩)` → `lib-tabs(카테고리)` → `lib-main`

**Step 1: CSS — `.lib-week-filter` 스타일 추가** (`<style>` 블록 안에)

```css
.lib-week-filter {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 12px 20px 0;
  display: flex; gap: 6px; flex-wrap: wrap;
}
.lib-week-chip {
  padding: 4px 12px;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: none;
  color: var(--muted); font-size: .78rem; font-family: inherit;
  cursor: pointer; white-space: nowrap;
  transition: border-color .14s, color .14s, background .14s;
}
.lib-week-chip:hover { color: var(--muted-strong); border-color: var(--line-strong); }
.lib-week-chip.is-active {
  border-color: var(--key);
  color: var(--key-soft);
  background: rgba(10,132,255,.08);
}
```

**Step 2: HTML — `<nav class="lib-week-filter">` 삽입** (`lib-tabs` 위에)

```html
<nav class="lib-week-filter" id="libWeekFilter" aria-label="주차 필터"></nav>
```

**Step 3: JS — 주차 칩 빌드 함수 추가**

`buildTabs()` 위에 추가:

```js
// 주차 칩
const WEEKS_WITH_CARDS = [0, 2, 3, 4, 5, 6, 7, 9, 10, 11, 13];
const WEEK_LABELS = { 0: "일반 개념" };

function buildWeekFilter() {
  var el = document.getElementById("libWeekFilter");
  var allChip = document.createElement("button");
  allChip.className = "lib-week-chip is-active";
  allChip.textContent = "전체 주차";
  allChip.dataset.week = "all";
  allChip.setAttribute("aria-pressed", "true");
  allChip.addEventListener("click", function() { selectWeekChip(allChip); });
  el.appendChild(allChip);

  WEEKS_WITH_CARDS.forEach(function(w) {
    var btn = document.createElement("button");
    btn.className = "lib-week-chip";
    btn.textContent = w === 0 ? "일반 개념" : "Week " + w;
    btn.dataset.week = w;
    btn.setAttribute("aria-pressed", "false");
    btn.addEventListener("click", function() { selectWeekChip(btn); });
    el.appendChild(btn);
  });
}

function selectWeekChip(chip) {
  document.querySelectorAll(".lib-week-chip").forEach(function(c) {
    c.classList.remove("is-active");
    c.setAttribute("aria-pressed", "false");
  });
  chip.classList.add("is-active");
  chip.setAttribute("aria-pressed", "true");
  if (typeof filterCards === "function") filterCards();
}

buildWeekFilter();
```

**Step 4: JS — `filterCards()` 에 주차 필터 조건 추가**

기존 `filterCards()` 함수에서:

```js
// BEFORE
var matchCat = activeCat === "전체" || cat === activeCat;
var matchQuery = ...;
card.style.display = (matchCat && matchQuery) ? "" : "none";

// AFTER
var activeWeekEl = document.querySelector(".lib-week-chip.is-active");
var activeWeek = activeWeekEl ? activeWeekEl.dataset.week : "all";
var cardWeek = String(SHOWME_REGISTRY[id].week ?? 0);

var matchCat   = activeCat === "전체" || cat === activeCat;
var matchWeek  = activeWeek === "all" || cardWeek === activeWeek;
var matchQuery = !query
  || meta.label.toLowerCase().includes(query)
  || id.toLowerCase().includes(query);

card.style.display = (matchCat && matchWeek && matchQuery) ? "" : "none";
```

**Step 5: 카드에 week 배지 추가** (`buildCards()` 함수에서 card 생성 부분)

```js
// idEl 다음에 추가
var weekVal = SHOWME_REGISTRY[id].week;
if (weekVal && weekVal > 0) {
  var weekBadge = document.createElement("span");
  weekBadge.className = "lib-card-week";
  weekBadge.textContent = "W" + weekVal;
  card.appendChild(weekBadge);
}
```

CSS 추가:
```css
.lib-card-week {
  font-size: .68rem; color: var(--muted);
  background: var(--overlay-white);
  border: 1px solid var(--line);
  border-radius: 999px;
  padding: 1px 6px;
  margin-top: 2px;
}
```

**Step 6: 검증 — 브라우저에서 library.html 열기**
- Week 2 칩 클릭 → 9개 카드만 표시
- Week 3 클릭 → 17개 카드 표시
- 검색 + 주차 필터 조합 동작 확인

**Step 7: Commit**
```bash
git add course-site/library.html course-site/assets/showme/_registry.js
git commit -m "feat: add week filter to library archive"
```

---

## Phase 3: `week.html` — 참고자료 섹션 통합

**파일:** `course-site/week.html`

현재 개별 섹션: `shortcutsHtml`, `exploreHtml`, `mistakesHtml`, `videosHtml`, `docsHtml`
→ 하나의 `<details>` 아코디언 `refHtml`로 통합

### Task 3: 참고자료 렌더 함수 작성

현재 위치: `renderResourceSection()` 정의 아래 (line ~595)

**Step 1: `videosHtml`, `docsHtml` 개별 변수를 `refHtml`로 교체**

기존 코드 (lines ~593-594):
```js
const videosHtml = renderResourceSection("공식 영상 튜토리얼", "▶", videos);
const docsHtml = renderResourceSection("공식 문서", "📄", docs);
```

교체 후:
```js
// 실습 영상 / 공식 튜토리얼 분리
const practiceVideos = videos.filter(v => v.title.includes("[실습]"));
const officialVideos = videos.filter(v => !v.title.includes("[실습]"));

const refSubsections = [
  practiceVideos.length ? `
    <div class="ref-group">
      <h4 class="ref-group-title">📹 실습 영상</h4>
      <div class="ref-video-list">
        ${practiceVideos.map(v => `
          <a class="ref-video-item" href="${v.url}" target="_blank" rel="noopener noreferrer">
            <span class="ref-video-title">${v.title.replace("[실습] ", "")} ↗</span>
            ${v.description ? `<span class="ref-video-desc">${v.description}</span>` : ""}
          </a>`).join("")}
      </div>
    </div>` : "",

  officialVideos.length ? `
    <div class="ref-group">
      <h4 class="ref-group-title">📚 공식 튜토리얼</h4>
      <div class="doc-links-row">
        ${officialVideos.map(v => `
          <a class="doc-link" href="${v.url}" target="_blank" rel="noopener noreferrer">
            <span class="doc-link-main">▶ ${v.title} ↗</span>
          </a>`).join("")}
      </div>
    </div>` : "",

  docs.length ? `
    <div class="ref-group">
      <h4 class="ref-group-title">📄 공식 문서</h4>
      <div class="doc-links-row">
        ${docs.map(d => `
          <a class="doc-link" href="${d.url}" target="_blank" rel="noopener noreferrer">
            <span class="doc-link-main">📄 ${d.title} ↗</span>
          </a>`).join("")}
      </div>
    </div>` : "",

  w.shortcuts && w.shortcuts.length ? `
    <div class="ref-group">
      <h4 class="ref-group-title">⌨️ 단축키</h4>
      <div class="shortcuts-compact">
        ${w.shortcuts.map(s => `
          <div class="sc-row">
            <kbd class="sc-key">${s.keys}</kbd>
            <span class="sc-action">${s.action}</span>
          </div>`).join("")}
      </div>
    </div>` : "",

  w.explore && w.explore.length ? `
    <div class="ref-group">
      <h4 class="ref-group-title">💡 더 해보기</h4>
      <ul class="ref-list">
        ${w.explore.map(e => `<li><strong>${e.title}</strong>${e.hint ? ` — <span class="ref-hint">${e.hint}</span>` : ""}</li>`).join("")}
      </ul>
    </div>` : "",

  w.mistakes && w.mistakes.length ? `
    <div class="ref-group">
      <h4 class="ref-group-title">⚠️ 막히는 지점</h4>
      <ul class="ref-list">
        ${w.mistakes.map(m => `<li>${m}</li>`).join("")}
      </ul>
    </div>` : "",
].filter(Boolean).join("");

const hasRef = refSubsections.length > 0;
const refHtml = hasRef ? `
  <section class="content-block" id="section-reference">
    <details class="card ref-accordion">
      <summary class="ref-summary">
        <span class="ref-summary-title">이번 주 참고자료</span>
        <span class="ref-summary-meta">${[
          practiceVideos.length ? `실습 영상 ${practiceVideos.length}` : "",
          officialVideos.length ? `튜토리얼 ${officialVideos.length}` : "",
          docs.length ? `문서 ${docs.length}` : "",
          w.shortcuts?.length ? `단축키 ${w.shortcuts.length}` : "",
        ].filter(Boolean).join(" · ")}</span>
      </summary>
      <div class="ref-body">${refSubsections}</div>
    </details>
  </section>` : "";
```

**Step 2: 기존 5개 섹션 렌더를 refHtml 하나로 교체**

HTML 출력 부분 (line ~673 근처):
```js
// BEFORE
${shortcutsHtml}
${exploreHtml}
${mistakesHtml}
${videosHtml}
${docsHtml}
${assignmentHtml}

// AFTER
${refHtml}
${assignmentHtml}
```

**Step 3: 사이드바 네비게이션도 업데이트** (line ~1089 근처)

```js
// BEFORE
if (w.shortcuts && w.shortcuts.length)  sections.push({ id: "section-shortcuts",  label: "단축키",      group: "참고" });
if (w.explore   && w.explore.length)    sections.push({ id: "section-explore",    label: "더 해보기",   group: null });
if (w.mistakes  && w.mistakes.length)   sections.push({ id: "section-mistakes",   label: "막히는 지점", group: null });

// AFTER
if (hasRef) sections.push({ id: "section-reference", label: "참고자료", group: "참고" });
```

**Step 4: CSS 추가** — `tokens.css`에 추가

```css
/* ── 참고자료 아코디언 ── */
.ref-accordion > summary { list-style: none; }
.ref-accordion > summary::-webkit-details-marker { display: none; }
.ref-summary {
  display: flex; justify-content: space-between; align-items: center;
  padding: 16px 20px; cursor: pointer;
  border-radius: var(--radius-md);
  transition: background .14s;
}
.ref-accordion[open] > .ref-summary { border-radius: var(--radius-md) var(--radius-md) 0 0; }
.ref-summary:hover { background: rgba(255,255,255,.04); }
.ref-summary-title { font-size: 1rem; font-weight: 600; color: var(--text); }
.ref-summary-meta { font-size: .78rem; color: var(--muted); }

.ref-body { padding: 0 20px 20px; display: flex; flex-direction: column; gap: 24px; }
.ref-group {}
.ref-group-title {
  font-size: .78rem; font-weight: 600; color: var(--muted-strong);
  text-transform: uppercase; letter-spacing: .06em;
  margin: 0 0 10px;
}
.ref-video-list { display: flex; flex-direction: column; gap: 6px; }
.ref-video-item {
  display: flex; flex-direction: column; gap: 2px;
  padding: 10px 14px; border-radius: var(--radius-sm);
  border: 1px solid var(--line);
  background: var(--overlay-white);
  transition: border-color .14s;
}
.ref-video-item:hover { border-color: var(--key); }
.ref-video-title { font-size: .86rem; color: var(--text); font-weight: 500; }
.ref-video-desc { font-size: .75rem; color: var(--muted); }
.ref-list { margin: 0; padding-left: 18px; color: var(--muted-strong); line-height: 1.9; font-size: .88rem; }
.ref-hint { color: var(--muted); }
.shortcuts-compact { display: flex; flex-direction: column; gap: 6px; }
.sc-row { display: flex; align-items: center; gap: 10px; font-size: .86rem; }
.sc-key {
  padding: 2px 8px; border-radius: 5px;
  border: 1px solid var(--line-strong);
  background: rgba(255,255,255,.07);
  font-family: var(--font-mono, monospace);
  font-size: .78rem; color: var(--text);
  white-space: nowrap; flex-shrink: 0;
}
.sc-action { color: var(--muted-strong); }
```

**Step 5: 검증 — `week.html?week=3` 브라우저 열기**
- 실습 카드 정상 표시 확인
- 하단에 "이번 주 참고자료" 아코디언 표시
- 클릭 시 펼쳐지며 📹 실습 영상, 📚 공식 튜토리얼, 📄 문서, ⌨️ 단축키 서브섹션 표시
- 사이드바에 "참고자료" 항목 표시

**Step 6: Commit**
```bash
git add course-site/week.html course-site/assets/tokens.css
git commit -m "feat: consolidate reference sections into collapsible accordion"
```

---

## Phase 4: `week.html` 기존 단축키 섹션 CSS 정리

기존 `shortcutsHtml` 렌더 코드 및 관련 CSS (`.shortcuts-table`, `.sc-grid` 등)는 아코디언 안으로 흡수되었으므로, 이전 독립 섹션 렌더 코드 삭제.

### Task 4: 기존 shortcutsHtml 렌더 코드 제거

**Step 1: `shortcutsHtml` 변수 생성 코드 찾아 삭제**

`week.html`에서 `shortcutsHtml` 변수를 만드는 블록 전체 삭제.
(`exploreHtml`, `mistakesHtml`도 마찬가지 — 이미 Phase 3에서 인라인으로 처리)

**Step 2: 검증 — `week.html?week=2` 열어서 오류 없음 확인**

**Step 3: Commit**
```bash
git add course-site/week.html
git commit -m "chore: remove legacy individual reference section renderers"
```

---

## Verification Checklist

1. **library.html**
   - [ ] 주차 칩 행 표시 (전체 주차 + Week 2~13)
   - [ ] Week 2 칩 클릭 → 9개 카드만 표시
   - [ ] Week 3 + "Generate Modifiers" 탭 조합 필터 동작
   - [ ] 검색어 + 주차 필터 동시 동작
   - [ ] 카드에 "W2", "W3" 배지 표시

2. **week.html**
   - [ ] 실습 카드 정상 렌더 (비디오, 이미지, showme)
   - [ ] 하단에 "이번 주 참고자료" 아코디언 (기본 닫힘)
   - [ ] 아코디언 안: 실습 영상 목록, 공식 튜토리얼, 문서, 단축키 서브섹션
   - [ ] 사이드바 네비게이션에 "참고자료" 항목
   - [ ] week=2, week=3 모두 정상 동작

---

## 주의사항

- `shortcutsHtml` 렌더러가 있는 기존 독립 섹션 코드(`section-shortcuts` ID)를 참조하는 사이드바 JS도 함께 제거
- `CATEGORY_MAP`은 library.html 인라인에 있으므로 수정 불필요 (week 필터와 독립적)
- 모든 `w.shortcuts` 접근은 optional chaining(`?.`) 또는 `&&` 체크 필수 (없는 주차 존재)
