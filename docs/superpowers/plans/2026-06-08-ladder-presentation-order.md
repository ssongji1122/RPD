# 사다리타기 발표순서 추첨 + 바이브코딩 예제 — 구현 플랜

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Week 15 발표순서를 뽑는 동작하는 사다리타기 게임 페이지를 만들고, 그것을 14주차 "AI 바이브코딩" 튜토리얼 예제로 연결한다.

**Architecture:** 바닐라 HTML/CSS/JS 독립형 페이지. 순수 로직(`window.Ladder`)을 IIFE로 노출해 Playwright `page.evaluate()`로 TDD. SVG로 사다리 렌더 + 경로 추적 애니메이션. SSoT 파이프라인(week.html 렌더러) 무관. 튜토리얼은 Notion connector append.

**Tech Stack:** Vanilla JS (IIFE, ES5 style `var`), SVG, `tokens.css`/`components.css`, Playwright E2E, Notion connector.

**설계 문서:** [2026-06-08-ladder-presentation-order-design.md](../specs/2026-06-08-ladder-presentation-order-design.md)

---

## 파일 구조

| 파일 | 책임 | 신규/수정 |
|------|------|-----------|
| `course-site/ladder.html` | 마크업, 상태 컨테이너, CSS/JS 로드 | 신규 |
| `course-site/assets/ladder.js` | 로직(`window.Ladder`) + DOM 바인딩 | 신규 |
| `course-site/assets/page-ladder.css` | 페이지 스타일 (Flat Outline 토큰) | 신규 |
| `tests/ladder.spec.js` | Playwright: 로직 + UI 플로우 | 신규 |
| `claudedocs/research/week14-ladder-tutorial.md` | 튜토리얼 초안(프롬프트 회고) | 신규 |
| 14주차 Notion 페이지 | ⑦포트폴리오 섹션에 예제 append | 수정(connector) |

**알고리즘 결정 (사다리타기 = Amidakuji):**
- 하단 발표순번은 **1~N 고정 배치**. 셔플 효과는 *가로줄 랜덤화*가 담당(전통 사다리타기 방식). 설계 문서의 "하단 셔플" 표현보다 이쪽이 정확 — 이중 랜덤 불필요.
- 가로줄 충돌 방지(한 층에서 인접 가로줄 동시 금지)로 **bijection(일대일 대응)** 보장 → 두 참가자가 같은 순번을 받지 않음.

---

## Task 1: 페이지 스캐폴드 + 테스트 하니스

**Files:**
- Create: `course-site/ladder.html`
- Create: `course-site/assets/ladder.js`
- Test: `tests/ladder.spec.js`

- [ ] **Step 1: 실패하는 테스트 작성** — `tests/ladder.spec.js`

```js
// @ts-check
const { test, expect } = require('@playwright/test');

test('ladder.html loads and exposes window.Ladder', async ({ page }) => {
  await page.goto('/ladder.html');
  const hasNs = await page.evaluate(() => typeof window.Ladder === 'object' && window.Ladder !== null);
  expect(hasNs).toBe(true);
});
```

- [ ] **Step 2: 실패 확인**

Run: `npx playwright test tests/ladder.spec.js --project=desktop -g "exposes window.Ladder"`
Expected: FAIL (ladder.html 404 / window.Ladder undefined)

- [ ] **Step 3: 최소 스캐폴드 작성** — `course-site/ladder.html` (head는 shortcuts.html 패턴 따름)

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>발표순서 사다리타기 — RPD</title>
  <meta name="description" content="기말 발표순서 추첨 사다리타기 — Robot Product Design" />
  <link rel="icon" type="image/svg+xml" href="assets/favicon.svg" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700&display=swap">
  <link rel="stylesheet" href="assets/tokens.css" />
  <link rel="stylesheet" href="assets/components.css" />
  <link rel="stylesheet" href="assets/page-ladder.css" />
  <script>/* FOUC */ (function(){var t=localStorage.getItem('rpd-theme');if(t)document.documentElement.setAttribute('data-theme',t);})()</script>
</head>
<body>
  <main class="ladder-page" id="main">
    <a class="ladder-back" href="index.html">← RPD</a>
    <header class="ladder-head">
      <h1 class="ladder-title">발표순서 사다리타기</h1>
      <p class="ladder-sub">이름을 넣고 사다리를 타서 발표 순서를 정하세요.</p>
    </header>
    <section class="ladder-stage" id="stage"><!-- JS render --></section>
  </main>
  <script src="assets/ladder.js"></script>
</body>
</html>
```

`course-site/assets/ladder.js`:

```js
/* course-site/assets/ladder.js
   발표순서 사다리타기 게임 — 로직(window.Ladder) + UI */
(function () {
  'use strict';

  var Ladder = {};
  window.Ladder = Ladder;

  // 이후 Task에서 Ladder.* 함수 추가, DOM 바인딩은 파일 하단 init()에서.

})();
```

- [ ] **Step 4: 통과 확인**

Run: `npx playwright test tests/ladder.spec.js --project=desktop -g "exposes window.Ladder"`
Expected: PASS

- [ ] **Step 5: 커밋**

```bash
git add course-site/ladder.html course-site/assets/ladder.js tests/ladder.spec.js
git commit -m "feat: scaffold ladder game page + test harness"
```

---

## Task 2: parseParticipants (이름 파싱)

**Files:** Modify `course-site/assets/ladder.js`, `tests/ladder.spec.js`

- [ ] **Step 1: 실패 테스트 추가** — `tests/ladder.spec.js`

```js
test('parseParticipants trims, drops blanks, keeps order', async ({ page }) => {
  await page.goto('/ladder.html');
  const r = await page.evaluate(() => window.Ladder.parseParticipants('  A \n\n B\nC \n   '));
  expect(r).toEqual(['A', 'B', 'C']);
});

test('parseParticipants keeps duplicates (동명이인)', async ({ page }) => {
  await page.goto('/ladder.html');
  const r = await page.evaluate(() => window.Ladder.parseParticipants('김민수\n김민수'));
  expect(r).toEqual(['김민수', '김민수']);
});
```

- [ ] **Step 2: 실패 확인**

Run: `npx playwright test tests/ladder.spec.js -g "parseParticipants" --project=desktop`
Expected: FAIL (parseParticipants is not a function)

- [ ] **Step 3: 구현** — `ladder.js` IIFE 안 `Ladder` 정의 뒤에 추가

```js
  Ladder.parseParticipants = function (text) {
    return String(text || '')
      .split('\n')
      .map(function (s) { return s.trim(); })
      .filter(function (s) { return s.length > 0; });
  };
```

- [ ] **Step 4: 통과 확인**

Run: `npx playwright test tests/ladder.spec.js -g "parseParticipants" --project=desktop`
Expected: PASS (2 tests)

- [ ] **Step 5: 커밋**

```bash
git add course-site/assets/ladder.js tests/ladder.spec.js
git commit -m "feat: parseParticipants — trim/dedupe-keep/blank-drop"
```

---

## Task 3: generateLadder + bijection 보장

**Files:** Modify `course-site/assets/ladder.js`, `tests/ladder.spec.js`

- [ ] **Step 1: 실패 테스트 추가**

```js
test('generateLadder shape: rungs per row, no adjacent collision', async ({ page }) => {
  await page.goto('/ladder.html');
  const ok = await page.evaluate(() => {
    var L = window.Ladder.generateLadder(6, 12);
    if (L.n !== 6 || L.rungs.length !== 12) return false;
    // 각 row에서 인접 가로줄(i, i+1 동시) 없어야 함
    for (var r = 0; r < L.rungs.length; r++) {
      var row = L.rungs[r].slice().sort(function (a, b) { return a - b; });
      for (var k = 1; k < row.length; k++) {
        if (row[k] - row[k - 1] < 2) return false; // 인접 → 충돌
      }
      for (var j = 0; j < row.length; j++) {
        if (row[j] < 0 || row[j] > L.n - 2) return false; // 범위 밖
      }
    }
    return true;
  });
  expect(ok).toBe(true);
});
```

- [ ] **Step 2: 실패 확인**

Run: `npx playwright test tests/ladder.spec.js -g "generateLadder" --project=desktop`
Expected: FAIL (generateLadder is not a function)

- [ ] **Step 3: 구현**

```js
  // rungs[r] = [i, ...] : row r에서 col i 와 col i+1 사이 가로줄
  Ladder.generateLadder = function (n, rows) {
    rows = rows || Math.max(n * 2, 6);
    var rungs = [];
    for (var r = 0; r < rows; r++) {
      var row = [];
      var i = 0;
      while (i < n - 1) {
        if (Math.random() < 0.5) {
          row.push(i);
          i += 2; // 인접 충돌 방지: i+1 건너뜀
        } else {
          i += 1;
        }
      }
      rungs.push(row);
    }
    return { n: n, rows: rows, rungs: rungs };
  };
```

- [ ] **Step 4: 통과 확인**

Run: `npx playwright test tests/ladder.spec.js -g "generateLadder" --project=desktop`
Expected: PASS

- [ ] **Step 5: 커밋**

```bash
git add course-site/assets/ladder.js tests/ladder.spec.js
git commit -m "feat: generateLadder with adjacency-safe rungs"
```

---

## Task 4: tracePath + computeResults (핵심 — 중복 없는 매핑)

**Files:** Modify `course-site/assets/ladder.js`, `tests/ladder.spec.js`

- [ ] **Step 1: 실패 테스트 추가**

```js
test('tracePath + computeResults: bijection (no duplicate slot)', async ({ page }) => {
  await page.goto('/ladder.html');
  const r = await page.evaluate(() => {
    var names = ['A', 'B', 'C', 'D', 'E', 'F', 'G'];
    var L = window.Ladder.generateLadder(names.length);
    var res = window.Ladder.computeResults(L, names);
    var slots = res.map(function (x) { return x.slot; }).sort(function (a, b) { return a - b; });
    var expected = names.map(function (_, i) { return i + 1; }); // [1..7]
    return { slots: slots, expected: expected, count: res.length };
  });
  expect(r.count).toBe(7);
  expect(r.slots).toEqual(r.expected); // 1..N 정확히 한 번씩 → 일대일
});

test('tracePath path starts at start col, ends within bounds', async ({ page }) => {
  await page.goto('/ladder.html');
  const r = await page.evaluate(() => {
    var L = window.Ladder.generateLadder(5);
    var t = window.Ladder.tracePath(L, 0);
    return { startCol: t.path[0].col, endCol: t.endCol, n: L.n };
  });
  expect(r.startCol).toBe(0);
  expect(r.endCol).toBeGreaterThanOrEqual(0);
  expect(r.endCol).toBeLessThan(r.n);
});
```

- [ ] **Step 2: 실패 확인**

Run: `npx playwright test tests/ladder.spec.js -g "tracePath" --project=desktop`
Expected: FAIL

- [ ] **Step 3: 구현**

```js
  Ladder.tracePath = function (ladder, startCol) {
    var col = startCol;
    var path = [{ row: -1, col: col }];
    for (var r = 0; r < ladder.rows; r++) {
      var row = ladder.rungs[r];
      if (row.indexOf(col) !== -1) {
        col = col + 1;       // 오른쪽 가로줄 → 우이동
      } else if (row.indexOf(col - 1) !== -1) {
        col = col - 1;       // 왼쪽 가로줄 → 좌이동
      }
      path.push({ row: r, col: col });
    }
    return { endCol: col, path: path };
  };

  // 하단 순번 1..N 고정. participant[i] → 도착 col 의 (col+1)번
  Ladder.computeResults = function (ladder, participants) {
    return participants.map(function (name, i) {
      var t = Ladder.tracePath(ladder, i);
      return { name: name, startCol: i, endCol: t.endCol, slot: t.endCol + 1, path: t.path };
    });
  };
```

- [ ] **Step 4: 통과 확인**

Run: `npx playwright test tests/ladder.spec.js -g "tracePath" --project=desktop`
Expected: PASS (2 tests). bijection 테스트가 핵심.

- [ ] **Step 5: 커밋**

```bash
git add course-site/assets/ladder.js tests/ladder.spec.js
git commit -m "feat: tracePath + computeResults (bijection guaranteed)"
```

---

## Task 5: SVG 렌더 + UI 상태 머신 (setup→ready→result)

**Files:** Modify `course-site/assets/ladder.js`, `course-site/ladder.html`

상태 머신: `setup`(입력) → `ready`(사다리 렌더) → `result`(매핑 공개). DOM은 `#stage`에 렌더. 이름은 사용자 입력이므로 **textContent로만** 출력(XSS 방지, innerHTML 직접 금지).

- [ ] **Step 1: 실패 테스트 추가** — 입력 후 사다리 SVG 생성 검증

```js
test('build ladder renders SVG with N vertical lines', async ({ page }) => {
  await page.goto('/ladder.html');
  await page.fill('#names', 'A\nB\nC\nD');
  await page.click('#buildBtn');
  const cols = await page.locator('#stage svg .ladder-col').count();
  expect(cols).toBe(4);
});

test('draw reveals N result rows, no duplicate slots', async ({ page }) => {
  await page.goto('/ladder.html');
  await page.fill('#names', 'A\nB\nC\nD');
  await page.click('#buildBtn');
  await page.click('#drawAllBtn');
  const slots = await page.locator('.result-row .result-slot').allInnerTexts();
  expect(slots.length).toBe(4);
  expect(new Set(slots).size).toBe(4); // 중복 없음
});
```

- [ ] **Step 2: 실패 확인**

Run: `npx playwright test tests/ladder.spec.js -g "build ladder|draw reveals" --project=desktop`
Expected: FAIL (#names 없음)

- [ ] **Step 3: ladder.html `#stage` 비우고 setup 마크업 + JS 렌더 구현**

`ladder.html`의 `<section class="ladder-stage" id="stage">` 안에 setup 폼 추가:

```html
      <div class="ladder-setup" id="setup">
        <label class="ladder-label" for="names">참가자 (한 줄에 한 명)</label>
        <textarea id="names" class="ladder-input" rows="6" placeholder="홍길동&#10;김철수&#10;..."></textarea>
        <div class="ladder-actions">
          <button type="button" class="btn-primary" id="buildBtn">사다리 만들기</button>
          <button type="button" class="btn-ghost" id="resetBtn" hidden>처음부터</button>
        </div>
        <p class="ladder-hint" id="hint" role="status"></p>
      </div>
      <div class="ladder-board" id="board" hidden></div>
      <div class="ladder-results" id="results" aria-live="polite" hidden></div>
```

`ladder.js`에 렌더/상태 함수 추가(IIFE 안, `Ladder` 함수 정의 뒤):

```js
  var NS = 'http://www.w3.org/2000/svg';
  var GEO = { padX: 28, padY: 28, gapY: 22, colGap: 64 }; // 좌표 상수
  var state = null; // { names, ladder, results }

  function el(id) { return document.getElementById(id); }

  function colX(i) { return GEO.padX + i * GEO.colGap; }
  function rowY(r) { return GEO.padY + (r + 1) * GEO.gapY; } // r=-1 → top

  function buildLadderSVG(ladder) {
    var w = GEO.padX * 2 + (ladder.n - 1) * GEO.colGap;
    var h = GEO.padY * 2 + (ladder.rows + 1) * GEO.gapY;
    var svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
    svg.setAttribute('class', 'ladder-svg');
    svg.setAttribute('role', 'img');
    // 세로줄
    for (var c = 0; c < ladder.n; c++) {
      var v = document.createElementNS(NS, 'line');
      v.setAttribute('class', 'ladder-col');
      v.setAttribute('x1', colX(c)); v.setAttribute('x2', colX(c));
      v.setAttribute('y1', rowY(-1)); v.setAttribute('y2', rowY(ladder.rows - 1));
      svg.appendChild(v);
    }
    // 가로줄
    for (var r = 0; r < ladder.rows; r++) {
      ladder.rungs[r].forEach(function (i) {
        var hr = document.createElementNS(NS, 'line');
        hr.setAttribute('class', 'ladder-rung');
        hr.setAttribute('x1', colX(i)); hr.setAttribute('x2', colX(i + 1));
        hr.setAttribute('y1', rowY(r)); hr.setAttribute('y2', rowY(r));
        svg.appendChild(hr);
      });
    }
    return { svg: svg, w: w, h: h };
  }

  function renderBoard() {
    var board = el('board');
    board.textContent = '';
    var built = buildLadderSVG(state.ladder);
    var pct = function (c) { return (colX(c) / built.w * 100) + '%'; }; // 라벨↔줄 정렬 핵심
    // 상단 이름 라벨 — colX 기준 절대위치(중앙정렬은 CSS translateX). textContent=XSS 안전
    var top = document.createElement('div'); top.className = 'ladder-tops';
    state.names.forEach(function (name, idx) {
      var s = document.createElement('span'); s.className = 'ladder-name'; s.textContent = name;
      s.style.left = pct(idx);
      top.appendChild(s);
    });
    // 하단 순번 1..N — 같은 colX 기준
    var bot = document.createElement('div'); bot.className = 'ladder-bottoms';
    for (var k = 0; k < state.ladder.n; k++) {
      var b = document.createElement('span'); b.className = 'ladder-slot'; b.textContent = (k + 1) + '번';
      b.style.left = pct(k);
      bot.appendChild(b);
    }
    board.appendChild(top);
    board.appendChild(built.svg);
    board.appendChild(bot);
    board.appendChild(drawControls());
    board.hidden = false;
  }

  function drawControls() {
    var wrap = document.createElement('div'); wrap.className = 'ladder-actions';
    var all = document.createElement('button');
    all.type = 'button'; all.className = 'btn-primary'; all.id = 'drawAllBtn';
    all.textContent = '전체 공개';
    all.addEventListener('click', revealAll);
    wrap.appendChild(all);
    return wrap;
  }

  function renderResults() {
    var box = el('results');
    box.textContent = '';
    var sorted = state.results.slice().sort(function (a, b) { return a.slot - b.slot; });
    sorted.forEach(function (r) {
      var row = document.createElement('div'); row.className = 'result-row';
      var slot = document.createElement('span'); slot.className = 'result-slot'; slot.textContent = r.slot;
      var name = document.createElement('span'); name.className = 'result-name'; name.textContent = r.name;
      row.appendChild(slot); row.appendChild(name);
      box.appendChild(row);
    });
    box.hidden = false;
  }

  function revealAll() {
    renderResults(); // Task 6에서 애니메이션 추가
  }

  function build() {
    var names = Ladder.parseParticipants(el('names').value);
    if (names.length < 2) { el('hint').textContent = '최소 2명이 필요합니다.'; return; }
    el('hint').textContent = '';
    var ladder = Ladder.generateLadder(names.length);
    state = { names: names, ladder: ladder, results: Ladder.computeResults(ladder, names) };
    renderBoard();
    el('resetBtn').hidden = false;
  }

  function reset() {
    state = null;
    el('board').hidden = true; el('board').textContent = '';
    el('results').hidden = true; el('results').textContent = '';
    el('resetBtn').hidden = true;
  }

  function init() {
    if (!el('buildBtn')) return;
    el('buildBtn').addEventListener('click', build);
    el('resetBtn').addEventListener('click', reset);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else { init(); }
```

- [ ] **Step 4: 통과 확인**

Run: `npx playwright test tests/ladder.spec.js -g "build ladder|draw reveals" --project=desktop`
Expected: PASS

- [ ] **Step 5: 커밋**

```bash
git add course-site/ladder.html course-site/assets/ladder.js tests/ladder.spec.js
git commit -m "feat: SVG ladder render + build/reveal state machine"
```

---

## Task 6: 경로 추적 애니메이션 + reduced-motion + 한 명씩 공개

**Files:** Modify `course-site/assets/ladder.js`, `course-site/assets/page-ladder.css`(애니메이션 일부)

기능: `revealAll`을 경로 stroke 드로잉으로. 추가로 상단 이름 클릭 시 그 한 명만 경로 추적(한 명씩 공개). `prefers-reduced-motion`이면 즉시 표시.

- [ ] **Step 1: 실패 테스트 추가** — reduced-motion 비활성 환경에서 경로 polyline 생성 검증

```js
test('reveal draws a highlight path polyline per participant', async ({ page }) => {
  await page.goto('/ladder.html');
  await page.fill('#names', 'A\nB\nC');
  await page.click('#buildBtn');
  await page.click('#drawAllBtn');
  await expect(page.locator('#stage svg .ladder-path')).toHaveCount(3);
});

test('clicking a name reveals only that participant result', async ({ page }) => {
  await page.goto('/ladder.html');
  await page.fill('#names', 'A\nB\nC');
  await page.click('#buildBtn');
  await page.locator('.ladder-name', { hasText: 'A' }).click();
  // 단일 공개: 결과 행 1개 이상, 경로 1개
  await expect(page.locator('#stage svg .ladder-path')).toHaveCount(1);
});
```

- [ ] **Step 2: 실패 확인**

Run: `npx playwright test tests/ladder.spec.js -g "reveal draws|clicking a name" --project=desktop`
Expected: FAIL

- [ ] **Step 3: 구현** — `ladder.js`

`buildLadderSVG`가 반환하는 `svg`에 경로를 그리는 함수들을 추가하고, **`revealAll`은 Task 5 버전을 교체(replace)** 한다 (append 아님):

```js
  function reducedMotion() {
    return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function pathPoints(result) {
    // result.path: [{row,col}] → SVG 좌표 문자열
    return result.path.map(function (p) {
      return colX(p.col) + ',' + (p.row < 0 ? rowY(-1) : rowY(p.row));
    }).join(' ');
  }

  function drawPath(svg, result, animate) {
    var pl = document.createElementNS(NS, 'polyline');
    pl.setAttribute('class', 'ladder-path');
    pl.setAttribute('points', pathPoints(result));
    svg.appendChild(pl);
    if (animate && !reducedMotion()) {
      var len = pl.getTotalLength();
      pl.style.strokeDasharray = len;
      pl.style.strokeDashoffset = len;
      // 강제 reflow 후 transition
      pl.getBoundingClientRect();
      pl.style.transition = 'stroke-dashoffset .8s ease';
      pl.style.strokeDashoffset = '0';
    }
    return pl;
  }

  function svgEl() { return el('board').querySelector('svg'); }

  function revealOne(result) {
    drawPath(svgEl(), result, true);
    renderResults([result]);            // 누적 공개
  }

  function revealAll() {
    var svg = svgEl();
    state.results.forEach(function (r) { drawPath(svg, r, true); });
    renderResults(state.results);
  }
```

아래 `renderResults`도 **Task 5 버전을 교체(replace)** — 인자(부분 리스트)를 받아 누적 공개:

```js
  function renderResults(list) {
    list = list || state.results;
    var box = el('results');
    // 누적: 이미 있는 slot 은 건너뜀
    var existing = {};
    Array.prototype.forEach.call(box.querySelectorAll('.result-row'), function (row) {
      existing[row.getAttribute('data-slot')] = true;
    });
    list.slice().sort(function (a, b) { return a.slot - b.slot; }).forEach(function (r) {
      if (existing[r.slot]) return;
      var row = document.createElement('div'); row.className = 'result-row'; row.setAttribute('data-slot', r.slot);
      var slot = document.createElement('span'); slot.className = 'result-slot'; slot.textContent = r.slot;
      var name = document.createElement('span'); name.className = 'result-name'; name.textContent = r.name;
      row.appendChild(slot); row.appendChild(name);
      box.appendChild(row);
    });
    box.hidden = false;
  }
```

renderBoard의 이름 span 생성 루프를 아래로 **교체(replace)** — 정렬용 `s.style.left`(Task 5)는 유지하고 클릭/키보드만 추가:

```js
    state.names.forEach(function (name, idx) {
      var s = document.createElement('span'); s.className = 'ladder-name'; s.textContent = name;
      s.style.left = pct(idx); // Task 5 정렬 유지
      s.setAttribute('role', 'button'); s.setAttribute('tabindex', '0');
      s.addEventListener('click', function () { revealOne(state.results[idx]); });
      s.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); revealOne(state.results[idx]); } });
      top.appendChild(s);
    });
```

- [ ] **Step 4: 통과 확인**

Run: `npx playwright test tests/ladder.spec.js -g "reveal draws|clicking a name" --project=desktop`
Expected: PASS

- [ ] **Step 5: 커밋**

```bash
git add course-site/assets/ladder.js course-site/assets/page-ladder.css tests/ladder.spec.js
git commit -m "feat: path-trace animation + per-name reveal + reduced-motion"
```

---

## Task 7: 스타일 (page-ladder.css — Flat Outline 토큰)

**Files:** Create `course-site/assets/page-ladder.css`

DESIGN.md 토큰만 사용. gradient/blur/glow 금지. 숫자 `tabular-nums`, 한글 `keep-all`. (토큰명 `--sp-*`/`--radius-sm`/`--key*`/`--surface`/`--line*`/`--warn` 등은 tokens.css 실재 확인 완료.)

- [ ] **Step 1: 작성** — `course-site/assets/page-ladder.css`

```css
/* course-site/assets/page-ladder.css — 발표순서 사다리타기 (Flat Outline) */
.ladder-page {
  max-width: 960px;
  margin: 0 auto;
  padding: var(--sp-8) var(--sp-6) var(--sp-16);
  color: var(--text);
  word-break: keep-all;
  overflow-wrap: break-word;
}
.ladder-back {
  display: inline-block;
  color: var(--muted);
  text-decoration: none;
  font-size: .82rem;
  margin-bottom: var(--sp-6);
}
.ladder-back:hover { color: var(--key-soft); }
.ladder-title { font-size: clamp(1.5rem, 2.4vw, 2rem); font-weight: 700; margin: 0 0 var(--sp-2); }
.ladder-sub { color: var(--muted); font-size: .9rem; margin: 0 0 var(--sp-8); }

.ladder-setup { max-width: 420px; }
.ladder-label { display: block; font-size: .82rem; color: var(--muted-strong); margin-bottom: var(--sp-2); }
.ladder-input {
  width: 100%;
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: var(--radius-sm);
  color: var(--text);
  padding: var(--sp-3);
  font-family: inherit; font-size: .9rem; line-height: 1.6;
  resize: vertical;
}
.ladder-input:focus { outline: none; border-color: var(--key-border); }
.ladder-actions { display: flex; gap: var(--sp-3); margin-top: var(--sp-4); }
.ladder-hint { color: var(--warn); font-size: .8rem; min-height: 1.2em; margin-top: var(--sp-2); }

.ladder-board { margin-top: var(--sp-8); }
/* 라벨은 colX() 기준 절대위치 — SVG 줄과 정확히 정렬(flexbox 금지). JS가 style.left=% 지정 */
.ladder-tops, .ladder-bottoms { position: relative; height: 2.2em; }
.ladder-name, .ladder-slot {
  position: absolute; transform: translateX(-50%);
  font-size: .82rem; text-align: center; white-space: nowrap; top: 0;
}
.ladder-name { color: var(--text); cursor: pointer; padding: var(--sp-1) var(--sp-2); border-radius: var(--radius-sm); }
.ladder-name:hover { color: var(--key-soft); background: var(--surface); }
.ladder-name:focus-visible { outline: 2px solid var(--key-border); }
.ladder-slot { color: var(--muted-strong); font-variant-numeric: tabular-nums; }

.ladder-svg { width: 100%; height: auto; display: block; }
.ladder-col, .ladder-rung { stroke: var(--line-strong); stroke-width: 2; }
.ladder-path { fill: none; stroke: var(--key); stroke-width: 3; stroke-linejoin: round; stroke-linecap: round; }

.ladder-results { margin-top: var(--sp-8); display: grid; gap: var(--sp-2); max-width: 420px; }
.result-row {
  display: flex; align-items: center; gap: var(--sp-3);
  background: var(--surface); border: 1px solid var(--line);
  border-radius: var(--radius-sm); padding: var(--sp-3) var(--sp-4);
}
.result-slot {
  font-variant-numeric: tabular-nums; font-weight: 700; color: var(--key-soft);
  min-width: 2.2em;
}
.result-slot::after { content: '번'; font-weight: 400; color: var(--muted); font-size: .8rem; margin-left: 2px; }
.result-name { color: var(--text); font-weight: 500; }
```

> 주의: `.result-slot::after`가 "번"을 붙이므로 Task 5/6의 `result-slot` textContent는 숫자만(`r.slot`) — 이미 일치. 확인할 것.

- [ ] **Step 2: 시각 확인 (preview)**

preview_start로 `course-site` 서빙 → `/ladder.html` → 이름 4개 입력 → 사다리 만들기 → 전체 공개 → `preview_screenshot`. gradient/glow 없는 Flat Outline인지, 민트 경로/순번 정렬 확인.

- [ ] **Step 3: 커밋**

```bash
git add course-site/assets/page-ladder.css
git commit -m "style: page-ladder.css flat-outline tokens"
```

---

## Task 8: 엣지케이스 + 접근성 보강

**Files:** Modify `course-site/assets/ladder.js`, `tests/ladder.spec.js`

- [ ] **Step 1: 실패 테스트 추가**

```js
test('under 2 names shows hint, no board', async ({ page }) => {
  await page.goto('/ladder.html');
  await page.fill('#names', 'A');
  await page.click('#buildBtn');
  await expect(page.locator('#hint')).toHaveText(/최소 2명/);
  await expect(page.locator('#board')).toBeHidden();
});

test('reset clears board and results', async ({ page }) => {
  await page.goto('/ladder.html');
  await page.fill('#names', 'A\nB\nC');
  await page.click('#buildBtn');
  await page.click('#drawAllBtn');
  await page.click('#resetBtn');
  await expect(page.locator('#board')).toBeHidden();
  await expect(page.locator('#results')).toBeHidden();
});

test('large group (24) still bijection via UI', async ({ page }) => {
  await page.goto('/ladder.html');
  const names = Array.from({ length: 24 }, (_, i) => 'S' + (i + 1)).join('\n');
  await page.fill('#names', names);
  await page.click('#buildBtn');
  await page.click('#drawAllBtn');
  const slots = await page.locator('.result-row .result-slot').allInnerTexts();
  expect(new Set(slots).size).toBe(24);
});
```

- [ ] **Step 2: 실패 확인 → 필요한 보강 구현**

Run: `npx playwright test tests/ladder.spec.js -g "under 2 names|reset clears|large group" --project=desktop`
대부분 Task 5~6에서 충족될 수 있음. FAIL 항목만 `ladder.js` 보강:
- reset 버튼이 board/results 숨김 (Task 5 `reset()` 확인)
- 대규모: `renderBoard`에서 `state.ladder.n > 20`이면 board에 `is-dense` 클래스 부여(가로 스크롤은 Task 9 CSS)

```js
  // renderBoard 마지막에:
  el('board').classList.toggle('is-dense', state.ladder.n > 20);
```

- [ ] **Step 3: 통과 확인**

Run: `npx playwright test tests/ladder.spec.js --project=desktop`
Expected: 전체 PASS

- [ ] **Step 4: 커밋**

```bash
git add course-site/assets/ladder.js tests/ladder.spec.js
git commit -m "feat: edge cases (min 2, reset, large group) + a11y hooks"
```

---

## Task 9: 반응형 + dense 레이아웃 + 모바일 검증

**Files:** Modify `course-site/assets/page-ladder.css`, `tests/ladder.spec.js`

- [ ] **Step 1: CSS 추가** — `page-ladder.css` 하단

```css
.ladder-board.is-dense { overflow-x: auto; }
.ladder-board.is-dense .ladder-svg { min-width: 720px; }

@media (max-width: 720px) {
  .ladder-page { padding: var(--sp-6) var(--sp-4) var(--sp-12); }
  .ladder-setup, .ladder-results { max-width: 100%; }
  .ladder-name, .ladder-slot { font-size: .74rem; }
}
@media (prefers-reduced-motion: reduce) {
  .ladder-path { transition: none !important; }
}
```

- [ ] **Step 2: 모바일 프로젝트 테스트 통과 확인**

Run: `npx playwright test tests/ladder.spec.js --project=mobile`
Expected: PASS (mobile viewport에서도 build/draw 동작)

- [ ] **Step 3: preview 반응형 확인**

preview_resize로 375px / 1280px 확인, `preview_screenshot` 각 1장.

- [ ] **Step 4: 커밋**

```bash
git add course-site/assets/page-ladder.css tests/ladder.spec.js
git commit -m "style: responsive + dense-scroll for large groups"
```

---

## Task 10: 전체 회귀 + index 진입점 + 최종 preview

**Files:** Modify `course-site/index.html`(또는 적절한 진입 링크 위치), `tests/ladder.spec.js`

> 진입점: 게임을 사이트에서 찾아갈 수 있어야 함. `index.html`에 카드/링크 1개 추가하거나, 최소한 직접 URL 안내. **실제 위치는 index.html 구조 확인 후 결정** — 기존 카드 그리드가 있으면 거기에 동일 패턴으로 1개 추가.

- [ ] **Step 1: index.html 링크 추가** — 기존 카드 패턴 grep 후 동일 컴포넌트로 "발표순서 사다리타기" 항목 1개 추가 (이모지 금지, Lucide 아이콘 사용)

- [ ] **Step 2: 전체 테스트 통과**

Run: `npx playwright test tests/ladder.spec.js`
Expected: desktop + mobile 전체 PASS

- [ ] **Step 3: 최종 preview 스크린샷** — setup / ready / result 3장 (튜토리얼용으로 보관)

- [ ] **Step 4: 커밋**

```bash
git add course-site/index.html tests/ladder.spec.js
git commit -m "feat: link ladder game from index"
```

---

## Task 11: 바이브코딩 튜토리얼 초안 (산출물 ②-a)

**Files:** Create `claudedocs/research/week14-ladder-tutorial.md`

게임 완성 후 **실제로 쓴 프롬프트를 회고**로 정리. A안 형식: 단계별 프롬프트 + 우리 게임 스크린샷 자리 + 도구 캡처 placeholder + "어느 도구든 이 프롬프트" 안내 + 게임 링크.

- [ ] **Step 1: 작성** — 아래 구조로 (프롬프트는 Task 1~9 실제 작업 기반으로 채움)

```markdown
# 예제: AI로 발표순서 사다리타기 만들기 (14주차 포트폴리오)

> 강사가 AI 바이브코딩으로 실제로 만든 도구입니다. 같은 프롬프트를 14주차 비교표의
> 어떤 도구(Lovable·v0·bolt 등)에 붙여넣어도 비슷하게 만들 수 있습니다.
> 완성본: [발표순서 사다리타기](https://<pages-url>/ladder.html)

## 1단계 — 무엇을 만들지 한 문장으로
프롬프트: "참가자 이름을 입력하면 사다리타기로 발표 순서를 뽑아주는 웹페이지를 만들어줘."
[게임 스크린샷: setup]
[도구 화면: __강사 테스트 후 첨부__]

## 2단계 — 핵심 로직 요청
프롬프트: "사다리타기는 두 사람이 같은 순서를 받으면 안 돼. 일대일로 배정되게 해줘."
...
(3~6단계: SVG 그리기 / 줄 따라 내려가는 애니메이션 / 디자인 / 예외처리)

## 따라 할 때 팁
- 한 번에 다 말고 한 기능씩 추가 요청
- "안 되는 부분"을 그대로 붙여넣고 고쳐달라고 하기
```

- [ ] **Step 2: 스크린샷 연결** — Task 10에서 저장한 setup/ready/result 스크린샷 경로를 본문에 반영

- [ ] **Step 3: 커밋**

```bash
git add claudedocs/research/week14-ladder-tutorial.md
git commit -m "docs: week14 ladder vibecoding tutorial draft"
```

---

## Task 12: Notion 14주차 ⑦포트폴리오 섹션 append (산출물 ②-b)

**Files:** 14주차 Notion 페이지 (connector)

> **선행 조건:** Task 11 초안 확정 + 게임이 Pages에 배포되어 URL 확정. **사용자 확인 후 진행**(외부 반영 작업).

- [ ] **Step 1:** [[notion-mcp-access]] 경로로 14주차 페이지 fetch (편집 직전 재fetch — 충돌 회피)

- [ ] **Step 2:** ⑦포트폴리오 섹션 하단에 connector `insert_content`(append)로 "예제: AI로 사다리타기 만들기" 블록 + 게임 링크 추가. **기존 텍스트 수정 금지(append만)**. 이미지는 `raw.githubusercontent.com` hotlink 패턴(기존 14건 방식).

- [ ] **Step 3:** re-fetch로 반영 확인. 사이트 반영은 ~30분 cron sync 후 (`NOTION_TOKEN` 로컬 401이므로 즉시 불가) — 사용자에게 안내.

- [ ] **Step 4:** 작업 기록을 메모리 [[rpd-2026-06-content-audit]]에 한 줄 추가.

---

## 완료 기준 (Acceptance Criteria)

1. `/ladder.html`에서 이름 입력 → 사다리 생성 → 발표순서가 **중복 없이** 1~N 배정. 각 이름 라벨이 자기 줄 바로 위(하단 순번은 줄 바로 아래)에 **중앙 정렬** — 375px·1280px 모두.
2. 경로 추적 애니메이션 동작, `prefers-reduced-motion`에서 즉시 표시.
3. 2명 미만/대규모(24명) 엣지 처리, 모바일 동작.
4. `npx playwright test tests/ladder.spec.js` desktop+mobile 전체 PASS.
5. Flat Outline 준수(gradient/glow/blur 0), 이름 출력 XSS 안전(textContent).
6. 튜토리얼 초안 작성, Notion append 완료(사용자 확인 후).

## Self-Review 메모 (작성자 체크 완료)
- Spec 커버리지: 게임 흐름(3.3)·알고리즘(3.4)·SVG(3.5)·디자인(3.6)·모션(3.7)·데이터/보안(3.8)·엣지(3.9)·a11y(3.10)·튜토리얼(4)·검증(5) → Task 1~12 매핑됨.
- 타입 일관성: `generateLadder→{n,rows,rungs}`, `tracePath→{endCol,path}`, `computeResults→[{name,startCol,endCol,slot,path}]`, `result-slot` textContent=숫자(+CSS `::after`로 "번"). 전 Task 일관.
- 설계의 "하단 셔플"은 구현상 "하단 1~N 고정 + 가로줄 랜덤"으로 명확화(파일 구조 절에 기록).
- 정렬(advisor 지적): 상/하단 라벨을 `colX()` 절대위치로 SVG 줄과 정합 — flexbox 금지. Task 5(JS `style.left`)+Task 7(CSS absolute). 완료기준 1에 정렬 검증 추가.
- 토큰명: `--sp-*`·`--radius-sm`·`--key*`·`--surface`·`--line*`·`--warn` 모두 tokens.css 실재 확인.
- aria-live는 `#stage`(전체) 아닌 `#results`에만 — 설계 3.10 일치.
- 3.3 "자동 순차 공개"는 미구현(YAGNI): "한 명씩"=이름 클릭, "전체"=버튼으로 충족. 의도적 드롭.
```
