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
});
