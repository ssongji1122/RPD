// @ts-check
const { test, expect } = require('@playwright/test');

const PAGES = [
  { path: '/index.html', title: /Blender Archive|RPD/ },
  { path: '/library.html', title: /카드 라이브러리|Show Me/ },
  { path: '/shortcuts.html', title: /단축키/ },
  { path: '/inha.html', title: /인하|RPD/ },
  { path: '/week.html?week=3', title: /Week/ },
  { path: '/studio.html', title: /My Studio/ },
  { path: '/admin.html', title: /Admin/ },
];

// Known non-critical JS errors to ignore
const KNOWN_ERRORS = [
  'getComputedStyle',  // library.html sidebar observer
  'sidebarToggle',     // index.html legacy reference
];

for (const pg of PAGES) {
  test(`${pg.path} loads with 200 status`, async ({ page }) => {
    const res = await page.goto(pg.path);
    expect(res.status()).toBe(200);
  });

  test(`${pg.path} has matching title`, async ({ page }) => {
    await page.goto(pg.path);
    await expect(page).toHaveTitle(pg.title);
  });

  test(`${pg.path} has no critical JS errors`, async ({ page }) => {
    const errors = [];
    page.on('pageerror', (err) => {
      const isKnown = KNOWN_ERRORS.some(k => err.message.includes(k));
      if (!isKnown) errors.push(err.message);
    });
    await page.goto(pg.path);
    expect(errors).toEqual([]);
  });
}
