// @ts-check
const { test, expect } = require('@playwright/test');

test('ladder.html loads and exposes window.Ladder', async ({ page }) => {
  await page.goto('/ladder.html');
  const hasNs = await page.evaluate(() => typeof window.Ladder === 'object' && window.Ladder !== null);
  expect(hasNs).toBe(true);
});

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

test('generateLadder shape: rungs per row, no adjacent collision', async ({ page }) => {
  await page.goto('/ladder.html');
  const ok = await page.evaluate(() => {
    var L = window.Ladder.generateLadder(6, 12);
    if (L.n !== 6 || L.rungs.length !== 12) return false;
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

test('tracePath + computeResults: bijection + default outcomes', async ({ page }) => {
  await page.goto('/ladder.html');
  const r = await page.evaluate(() => {
    var names = ['A', 'B', 'C', 'D', 'E', 'F', 'G'];
    var L = window.Ladder.generateLadder(names.length);
    var outcomes = names.map(function (_, i) { return (i + 1) + '번'; });
    var res = window.Ladder.computeResults(L, names, outcomes);
    var uniq = {}; res.forEach(function (x) { uniq[x.endCol] = 1; });
    return { uniqCount: Object.keys(uniq).length, count: res.length, sampleOutcome: res[0].outcome };
  });
  expect(r.count).toBe(7);
  expect(r.uniqCount).toBe(7); // endCol 일대일 → bijection
  expect(typeof r.sampleOutcome).toBe('string'); // outcome 라벨
});

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
  await expect(page.locator('.result-row')).toHaveCount(3); // 경로 애니 후 등장 대기
  const outs = await page.locator('.result-row .result-slot').allInnerTexts();
  expect(new Set(outs.map(s => s.trim())).size).toBe(3); // 1번/2번/3번 유니크
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
  await expect(page.locator('.result-row')).toHaveCount(4); // 경로 애니 후 결과 등장
  const slots = await page.locator('.result-row .result-slot').allInnerTexts();
  expect(slots.length).toBe(4);
  expect(new Set(slots).size).toBe(4); // 중복 없음
});

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
  await expect(page.locator('#stage svg .ladder-path')).toHaveCount(1);
  await expect(page.locator('.result-row')).toHaveCount(1); // 경로 애니 후 결과 등장
});

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
  await expect(page.locator('.result-row')).toHaveCount(24); // 경로 애니 후 결과 등장
  const slots = await page.locator('.result-row .result-slot').allInnerTexts();
  expect(new Set(slots).size).toBe(24);
});

test('reveal path follows ladder orthogonally (no diagonal segments)', async ({ page }) => {
  await page.goto('/ladder.html');
  await page.fill('#names', 'A\nB\nC\nD\nE');
  await page.click('#buildBtn');
  await page.click('#drawAllBtn');
  const diagonal = await page.evaluate(() => {
    var pls = document.querySelectorAll('.ladder-path');
    for (var i = 0; i < pls.length; i++) {
      var pts = pls[i].getAttribute('points').trim().split(/\s+/).map(function (s) {
        var a = s.split(','); return { x: +a[0], y: +a[1] };
      });
      for (var k = 1; k < pts.length; k++) {
        var dx = Math.abs(pts[k].x - pts[k - 1].x);
        var dy = Math.abs(pts[k].y - pts[k - 1].y);
        if (dx > 0.5 && dy > 0.5) return true; // 한 구간에서 x,y 둘 다 변함 = 대각선
      }
    }
    return false;
  });
  expect(diagonal).toBe(false); // 모든 구간이 수평 또는 수직
});

test('25 long names: labels do not overlap, ladder rendered at natural width', async ({ page, viewport }) => {
  test.skip(!!viewport && viewport.width < 720, 'desktop only (mobile fits to width)');
  await page.goto('/ladder.html');
  const names = Array.from({ length: 25 }, (_, i) => '학생' + (i + 1) + ' (122424' + String(i + 1).padStart(2, '0') + ')').join('\n');
  await page.fill('#names', names);
  await page.click('#buildBtn');
  const m = await page.evaluate(() => {
    var nm = document.querySelectorAll('.ladder-name');
    var overlaps = 0;
    for (var k = 0; k < nm.length - 1; k++) {
      var a = nm[k].getBoundingClientRect(), b = nm[k + 1].getBoundingClientRect();
      if (b.left < a.right - 0.5) overlaps++;
    }
    var svg = document.querySelector('.ladder-svg').getBoundingClientRect();
    return { overlaps: overlaps, svgW: Math.round(svg.width), n: nm.length };
  });
  expect(m.n).toBe(25);
  expect(m.overlaps).toBe(0); // 인접 이름 라벨이 겹치지 않아야
  expect(m.svgW).toBeGreaterThanOrEqual(25 * 60); // 자연 폭(축소 금지): 최소 줄간격 * N
});

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

test('mobile: ladder fits viewport width (no horizontal scroll)', async ({ page, viewport }) => {
  test.skip(!!viewport && viewport.width >= 720, 'mobile only');
  await page.goto('/ladder.html');
  await page.fill('#names', 'A\nB\nC\nD\nE\nF\nG');
  await page.click('#buildBtn');
  const m = await page.evaluate(() => {
    var b = document.getElementById('board');
    return { scroll: b.scrollWidth, client: b.clientWidth };
  });
  expect(m.scroll).toBeLessThanOrEqual(m.client + 2); // 폰: 가로 스크롤 없이 화면에 맞음
});
