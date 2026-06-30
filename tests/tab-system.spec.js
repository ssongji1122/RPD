// @ts-check
const { test, expect } = require('@playwright/test');

const TAB_MAP = [
  { path: '/index.html', activeTab: 'archive' },
  { path: '/library.html', activeTab: 'showme' },
  { path: '/shortcuts.html', activeTab: 'archive' },
  { path: '/inha.html', activeTab: 'class' },
  { path: '/week.html?week=3', activeTab: 'class' },
  { path: '/final-projects.html', activeTab: 'final' },
  { path: '/studio.html', activeTab: 'studio' },
];

for (const { path, activeTab } of TAB_MAP) {
  test(`${path} highlights ${activeTab} tab`, async ({ page }) => {
    await page.goto(path);
    const activeLink = page.locator(`.app-tab[data-tab-target="${activeTab}"]`);
    await expect(activeLink).toHaveClass(/is-active/);
  });
}

test.describe('tab navigation', () => {
  test.skip(({ viewport }) => viewport.width < 720, 'desktop only');

  test('Class tab href points to inha.html', async ({ page }) => {
    await page.goto('/index.html');
    const href = await page.locator('.app-tab[data-tab-target="class"]').getAttribute('href');
    expect(href).toContain('inha.html');
  });

  test('Final tab href points to final-projects.html', async ({ page }) => {
    await page.goto('/index.html');
    const href = await page.locator('.app-tab[data-tab-target="final"]').getAttribute('href');
    expect(href).toContain('final-projects.html');
  });

  test('My Studio tab href points to studio.html', async ({ page }) => {
    await page.goto('/index.html');
    const href = await page.locator('.app-tab[data-tab-target="studio"]').getAttribute('href');
    expect(href).toContain('studio.html');
  });
});
