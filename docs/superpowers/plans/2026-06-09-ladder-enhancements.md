# 사다리타기 고도화 1단계 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** v1 사다리 게임에 결과 커스터마이즈(범용화) + 경로 색상 구분 + 도착 가림→공개 긴장감을 추가한다.

**Architecture:** 기존 `window.Ladder`(IIFE) 확장. `computeResults`에 `outcomes` 인자 추가(`slot` 숫자 → `outcome` 문자열). 색상은 HSL 균등 생성, 가림은 하단 슬롯 텍스트 토글. SVG/Flat Outline 유지, 색상은 게임 한정 예외.

**Tech Stack:** Vanilla JS(IIFE, ES5), SVG, Playwright, tokens.css.

**설계 문서:** [2026-06-09-ladder-enhancements-design.md](../specs/2026-06-09-ladder-enhancements-design.md)

---

## 파일 구조
| 파일 | 변경 |
|------|------|
| `course-site/ladder.html` | 결과 토글 + textarea 마크업 |
| `course-site/assets/ladder.js` | outcomes 로직·computeResults 시그니처·색상·가림/공개 |
| `course-site/assets/page-ladder.css` | 결과 dot·가림 `?`·토글 스타일, `.result-slot::after` 제거 |
| `tests/ladder.spec.js` | 신규 테스트 + 기존 `slot`→`outcome` 갱신 |

**호환성 주의:** `computeResults`가 `slot`(숫자)에서 `outcome`(문자열)으로 바뀌므로, 이를 쓰는 기존 테스트 3개(bijection, draw reveals, large group)를 **endCol 기반**으로 갱신한다. bijection 불변식은 `endCol` 유니크로 검증(문자열 정렬 회피).

---

## Task 1: 결과 커스터마이즈 + outcomes (computeResults 시그니처 변경)

**Files:** `course-site/ladder.html`, `course-site/assets/ladder.js`, `tests/ladder.spec.js`

- [ ] **Step 1: 기존 bijection 테스트를 endCol 기반 + outcome으로 갱신**

`tests/ladder.spec.js`의 `'tracePath + computeResults: bijection (no duplicate slot)'` 테스트 본문을 교체:

```js
test('tracePath + computeResults: bijection + default outcomes', async ({ page }) => {
  await page.goto('/ladder.html');
  const r = await page.evaluate(() => {
    var names = ['A', 'B', 'C', 'D', 'E', 'F', 'G'];
    var L = window.Ladder.generateLadder(names.length);
    var outcomes = names.map(function (_, i) { return (i + 1) + '번'; });
    var res = window.Ladder.computeResults(L, names, outcomes);
    var ends = res.map(function (x) { return x.endCol; }).sort(function (a, b) { return a - b; });
    var uniq = {}; res.forEach(function (x) { uniq[x.endCol] = 1; });
    return { ends: ends, uniqCount: Object.keys(uniq).length, count: res.length, sampleOutcome: res[0].outcome };
  });
  expect(r.count).toBe(7);
  expect(r.uniqCount).toBe(7); // endCol 일대일 → bijection
  expect(typeof r.sampleOutcome).toBe('string'); // outcome 라벨
});
```

- [ ] **Step 2: 실패 확인**

Run: `npx playwright test tests/ladder.spec.js -g "bijection" --project=desktop`
Expected: FAIL (computeResults가 3번째 인자 무시, `x.outcome` undefined)

- [ ] **Step 3: computeResults 시그니처 변경** — `ladder.js`

기존 `Ladder.computeResults` 함수를 교체:

```js
  // 하단 outcomes[endCol] 매핑. outcome = 문자열 라벨(기본 "N번" 또는 커스텀)
  Ladder.computeResults = function (ladder, participants, outcomes) {
    return participants.map(function (name, i) {
      var t = Ladder.tracePath(ladder, i);
      return { name: name, startCol: i, endCol: t.endCol, outcome: outcomes[t.endCol], path: t.path };
    });
  };
```

- [ ] **Step 4: 통과 확인**

Run: `npx playwright test tests/ladder.spec.js -g "bijection" --project=desktop`
Expected: PASS

- [ ] **Step 5: 결과 토글 마크업 추가** — `ladder.html`의 `#setup` 안, `.ladder-actions` 앞에 삽입

기존:
```html
        <div class="ladder-actions">
          <button type="button" class="btn-primary" id="buildBtn">사다리 만들기</button>
```
교체:
```html
        <button type="button" class="ladder-toggle" id="resultToggle" aria-expanded="false">결과 직접 입력 (벌칙·역할 등, 비우면 발표순서)</button>
        <textarea id="results-input" class="ladder-input" rows="4" hidden placeholder="치킨&#10;꽝&#10;커피&#10;..."></textarea>
        <div class="ladder-actions">
          <button type="button" class="btn-primary" id="buildBtn">사다리 만들기</button>
```

- [ ] **Step 6: outcomes 계산 + 토글 + 개수검증을 build/init에 반영** — `ladder.js`

`build` 함수를 교체:

```js
  function build() {
    var names = Ladder.parseParticipants(el('names').value);
    if (names.length < 2) { el('hint').textContent = '최소 2명이 필요합니다.'; return; }
    var outcomes;
    var ri = el('results-input');
    var custom = ri && !ri.hidden ? Ladder.parseParticipants(ri.value) : [];
    if (custom.length > 0) {
      if (custom.length !== names.length) {
        el('hint').textContent = '결과를 ' + names.length + '개 입력하세요 (현재 ' + custom.length + '개)';
        return;
      }
      outcomes = custom;
    } else {
      outcomes = names.map(function (_, i) { return (i + 1) + '번'; });
    }
    el('hint').textContent = '';
    var ladder = Ladder.generateLadder(names.length);
    state = { names: names, ladder: ladder, outcomes: outcomes, results: Ladder.computeResults(ladder, names, outcomes) };
    el('results').textContent = ''; el('results').hidden = true;
    renderBoard();
    el('resetBtn').hidden = false;
  }
```

`init` 함수에 토글 핸들러 추가 (기존 `init` 내부, `resetBtn` 줄 다음):

```js
    var rt = el('resultToggle');
    if (rt) rt.addEventListener('click', function () {
      var ri = el('results-input');
      var open = ri.hidden;
      ri.hidden = !open;
      rt.setAttribute('aria-expanded', open ? 'true' : 'false');
      rt.classList.toggle('is-open', open);
    });
```

- [ ] **Step 6b: renderResults를 outcome 기반으로 갱신 + ::after 제거**

`ladder.js` `renderResults`를 교체(문자열 outcome 표시, 정렬·중복키 endCol — 문자열 정렬 회피):

```js
  function renderResults(list) {
    list = list || state.results;
    var box = el('results');
    var existing = {};
    Array.prototype.forEach.call(box.querySelectorAll('.result-row'), function (row) {
      existing[row.getAttribute('data-slot')] = true;
    });
    list.slice().sort(function (a, b) { return a.endCol - b.endCol; }).forEach(function (r) {
      if (existing[r.endCol]) return;
      var row = document.createElement('div'); row.className = 'result-row';
      row.setAttribute('data-slot', r.endCol);
      var slot = document.createElement('span'); slot.className = 'result-slot'; slot.textContent = r.outcome;
      var name = document.createElement('span'); name.className = 'result-name'; name.textContent = r.name;
      row.appendChild(slot); row.appendChild(name);
      box.appendChild(row);
    });
    box.hidden = false;
  }
```

`page-ladder.css`에서 `.result-slot::after { content: '번'; ... }` 줄 **삭제**(outcome에 "번" 포함).

- [ ] **Step 7: 결과 커스텀/자동/검증 테스트 추가** — `tests/ladder.spec.js`

```js
test('custom outcomes appear in results', async ({ page }) => {
  await page.goto('/ladder.html');
  await page.fill('#names', 'A\nB\nC');
  await page.click('#resultToggle');
  await page.fill('#results-input', '치킨\n꽝\n커피');
  await page.click('#buildBtn');
  await page.click('#drawAllBtn');
  await expect(page.locator('.result-row')).toHaveCount(3);
  const outs = await page.locator('.result-row .result-slot').allInnerTexts();
  expect(outs.map(s => s.trim()).sort()).toEqual(['꽝', '치킨', '커피']);
});

test('mismatched outcome count blocks build with hint', async ({ page }) => {
  await page.goto('/ladder.html');
  await page.fill('#names', 'A\nB\nC');
  await page.click('#resultToggle');
  await page.fill('#results-input', '치킨\n꽝');
  await page.click('#buildBtn');
  await expect(page.locator('#hint')).toHaveText(/결과를 3개/);
  await expect(page.locator('#board')).toBeHidden();
});

test('empty results defaults to presentation order', async ({ page }) => {
  await page.goto('/ladder.html');
  await page.fill('#names', 'A\nB\nC');
  await page.click('#buildBtn');
  await page.click('#drawAllBtn');
  const outs = await page.locator('.result-row .result-slot').allInnerTexts();
  expect(new Set(outs.map(s => s.trim())).size).toBe(3); // 1번/2번/3번 유니크
});
```

- [ ] **Step 8: 통과 확인**

Run: `npx playwright test tests/ladder.spec.js -g "bijection|custom outcomes|mismatched|defaults to presentation" --project=desktop`
Expected: PASS (renderResults가 outcome 기반이라 custom/auto/mismatch 모두 green)

- [ ] **Step 9: 커밋**

```bash
git add course-site/ladder.html course-site/assets/ladder.js tests/ladder.spec.js
git commit -m "feat: custom outcomes + computeResults(outcomes) signature"
```

---

## Task 2: 경로 색상 구분

**Files:** `course-site/assets/ladder.js`, `course-site/assets/page-ladder.css`, `tests/ladder.spec.js`

- [ ] **Step 1: 색상 테스트 추가** — `tests/ladder.spec.js`

```js
test('each participant path has a distinct color', async ({ page }) => {
  await page.goto('/ladder.html');
  await page.fill('#names', 'A\nB\nC\nD\nE');
  await page.click('#buildBtn');
  await page.click('#drawAllBtn');
  const colors = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('.ladder-path')).map(function (p) {
      return p.style.stroke || getComputedStyle(p).stroke;
    });
  });
  expect(colors.length).toBe(5);
  expect(new Set(colors).size).toBe(5); // 5색 고유
});
```

- [ ] **Step 2: 실패 확인**

Run: `npx playwright test tests/ladder.spec.js -g "distinct color" --project=desktop`
Expected: FAIL (모든 경로가 CSS 단색 --key → Set size 1)

- [ ] **Step 3: 색상 생성 + drawPath 색 적용 + 결과 dot** — `ladder.js`

`colorFor` 헬퍼 추가(`reducedMotion` 함수 근처):

```js
  function colorFor(i, n) {
    return 'hsl(' + Math.round(i * 360 / Math.max(n, 1)) + ', 70%, 62%)';
  }
```

`drawPath`에 색 인자 추가 — 시그니처와 stroke 지정:

```js
  function drawPath(svg, result, animate, color) {
    var pl = document.createElementNS(NS, 'polyline');
    pl.setAttribute('class', 'ladder-path');
    pl.setAttribute('points', pathPoints(result));
    if (color) pl.style.stroke = color;
    svg.appendChild(pl);
    if (animate && !reducedMotion()) {
      var len = pl.getTotalLength();
      var dur = Math.min(3, Math.max(0.7, len / 600));
      pl.style.strokeDasharray = len;
      pl.style.strokeDashoffset = len;
      pl.getBoundingClientRect();
      pl.style.transition = 'stroke-dashoffset ' + dur + 's linear';
      pl.style.strokeDashoffset = '0';
    }
    return pl;
  }
```

`revealResult`에서 색 전달 (Task 1 이후 형태 기준 교체):

```js
  function revealResult(r) {
    var color = colorFor(r.startCol, state.ladder.n);
    var pl = drawPath(svgEl(), r, true, color);
    var arrived = false;
    var onArrive = function () {
      if (arrived) return; arrived = true;
      highlightSlot(r.endCol);       // Task 3에서 revealSlot(가림 해제)로 교체
      renderResults([r], color);
    };
    if (reducedMotion() || !pl) { onArrive(); return; }
    pl.addEventListener('transitionend', onArrive);
  }
```

`renderResults`에 색 dot 추가 — 시그니처 `(list, color)`로 교체:

```js
  function renderResults(list, color) {
    list = list || state.results;
    var box = el('results');
    var existing = {};
    Array.prototype.forEach.call(box.querySelectorAll('.result-row'), function (row) {
      existing[row.getAttribute('data-slot')] = true;
    });
    list.slice().sort(function (a, b) { return a.endCol - b.endCol; }).forEach(function (r) {
      if (existing[r.endCol]) return;
      var row = document.createElement('div'); row.className = 'result-row';
      row.setAttribute('data-slot', r.endCol);
      var dot = document.createElement('span'); dot.className = 'result-dot';
      dot.style.background = color || colorFor(r.startCol, state.ladder.n);
      var slot = document.createElement('span'); slot.className = 'result-slot'; slot.textContent = r.outcome;
      var name = document.createElement('span'); name.className = 'result-name'; name.textContent = r.name;
      row.appendChild(dot); row.appendChild(slot); row.appendChild(name);
      box.appendChild(row);
    });
    box.hidden = false;
  }
```

> 변경점: `data-slot`/정렬 키를 `endCol`로(문자열 outcome 정렬 회피), `result-slot` 텍스트는 `r.outcome`, dot 추가.

- [ ] **Step 4: dot 스타일** — `page-ladder.css` (::after는 Task 1 Step 6b에서 이미 제거)

```css
.result-dot { width: 10px; height: 10px; border-radius: 50%; flex: 0 0 auto; }
```

(`.result-row`는 이미 flex; dot이 맨 앞 색 점)

- [ ] **Step 5: 통과 확인**

Run: `npx playwright test tests/ladder.spec.js -g "distinct color" --project=desktop`
Expected: PASS

- [ ] **Step 6: 커밋**

```bash
git add course-site/assets/ladder.js course-site/assets/page-ladder.css tests/ladder.spec.js
git commit -m "feat: per-participant path colors + result color dot"
```

---

## Task 3: 도착 가림 → 공개

**Files:** `course-site/assets/ladder.js`, `course-site/assets/page-ladder.css`, `tests/ladder.spec.js`

- [ ] **Step 1: 가림→공개 테스트 추가** — `tests/ladder.spec.js`

```js
test('outcomes hidden until arrival, then revealed', async ({ page }) => {
  await page.goto('/ladder.html');
  await page.fill('#names', 'A\nB\nC');
  await page.click('#buildBtn');
  // 빌드 직후 하단 슬롯은 ? 로 가림
  const hidden = await page.locator('.ladder-slot').allInnerTexts();
  expect(hidden.every(t => t.trim() === '?')).toBe(true);
  // 전체 공개 후엔 ? 가 사라지고 outcome 표시
  await page.click('#drawAllBtn');
  await expect(page.locator('.ladder-slot.is-hidden')).toHaveCount(0);
  const shown = await page.locator('.ladder-slot').allInnerTexts();
  expect(shown.some(t => t.trim() === '?')).toBe(false);
});
```

- [ ] **Step 2: 실패 확인**

Run: `npx playwright test tests/ladder.spec.js -g "hidden until arrival" --project=desktop`
Expected: FAIL (현재 하단 슬롯이 outcome 즉시 표시)

- [ ] **Step 3: 하단 슬롯 가림 렌더 + revealSlot** — `ladder.js`

`renderBoard`의 하단 순번 생성 루프를 교체(가림):

```js
    var bot = document.createElement('div'); bot.className = 'ladder-bottoms';
    for (var k = 0; k < state.ladder.n; k++) {
      var b = document.createElement('span'); b.className = 'ladder-slot is-hidden';
      b.textContent = '?'; b.style.left = pct(k);
      bot.appendChild(b);
    }
```

`highlightSlot`을 `revealSlot`으로 교체(가림 해제 + outcome 표시 + pop):

```js
  function revealSlot(col) {
    var slots = el('board').querySelectorAll('.ladder-slot');
    var s = slots[col];
    if (!s) return;
    s.textContent = state.outcomes[col];
    s.classList.remove('is-hidden');
    s.classList.add('is-hit');
  }
```

그리고 `revealResult`의 `highlightSlot(r.endCol)` 호출을 `revealSlot(r.endCol)`로 교체.

- [ ] **Step 4: 가림 스타일** — `page-ladder.css`

```css
.ladder-slot.is-hidden { color: var(--muted); }
```

(`.ladder-slot.is-hit` pop 규칙은 기존 유지)

- [ ] **Step 5: 전체 통과 확인 (Task 1·2·3 + 회귀)**

Run: `npx playwright test tests/ladder.spec.js`
Expected: 전체 PASS (desktop+mobile). 특히 Task 1의 custom/mismatch, Task 2 색상, Task 3 가림, 그리고 기존 회귀(직각·정렬·대규모·도착타이밍).

- [ ] **Step 6: 기존 회귀 테스트 outcome 갱신 확인**

`'draw reveals N result rows'` / `'large group (24)'` 테스트는 `.result-row .result-slot` 텍스트를 보는데, 이제 outcome("1번" 등)이라 `new Set(...).size` 검증은 그대로 유효(유니크). 만약 실패하면 해당 단언을 endCol 기준으로 점검. 변경 불필요면 그대로 둠.

- [ ] **Step 7: 커밋**

```bash
git add course-site/assets/ladder.js course-site/assets/page-ladder.css tests/ladder.spec.js
git commit -m "feat: hide outcomes until path arrival (suspense reveal)"
```

---

## Task 4: preview 시각 검증 + 스크린샷 갱신

**Files:** (임시) `tests/capture-ladder.spec.js`

- [ ] **Step 1: 캡처 스크립트로 색상·가림·커스텀 결과 확인**

7명 + 커스텀 결과로 빌드→전체공개 후 fullPage 캡처(viewport 넉넉). 색상 구분·가림 해제·dot 확인. Read로 검토.

- [ ] **Step 2: 문제 없으면 스크립트 삭제, 갱신된 result.png 커밋(선택)**

```bash
rm -f tests/capture-ladder.spec.js
git add course-site/assets/images/ladder/
git commit -m "assets: refresh ladder screenshots (colors + outcomes)"
```

---

## 완료 기준
1. 결과 비우면 발표순서(1~N번), 채우면 커스텀 outcome 매핑(중복 없는 endCol)
2. 결과 개수 불일치 시 hint + board 미생성
3. 참가자별 경로 색 고유, 결과행 색 dot
4. 빌드 직후 하단 `?` 가림 → 도착 시 해당 칸 공개(+pop)
5. `npx playwright test tests/ladder.spec.js` 전체 PASS(desktop+mobile)
6. XSS 안전(textContent), reduced-motion 존중

## Self-Review (작성자 체크)
- 스펙 커버리지: ①결과칸(T1) ②색상(T2) ③가림(T3) ④검증(T4) 매핑.
- 시그니처 일관: `computeResults(ladder,participants,outcomes)→{...,outcome}`, `drawPath(svg,result,animate,color)`, `renderResults(list,color)`, `revealSlot(col)`. 전 Task 동일.
- 기존 `slot`(숫자)→`outcome`(문자열)·`data-slot`=endCol으로 통일(문자열 정렬 회피).
- ::after "번" 제거 ↔ outcome에 "번" 포함 — 일관.
- 가림 reset: build가 renderBoard 재호출(새 slot=?), reset은 board 비움 — 일관.
