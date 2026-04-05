// @ts-check
const { test, expect } = require('@playwright/test');

const PAGES = [
  { path: '/index.html', activeTab: 'archive' },
  { path: '/library.html', activeTab: 'archive' },
  { path: '/shortcuts.html', activeTab: 'archive' },
  { path: '/studio.html', activeTab: 'studio' },
  { path: '/inha.html', activeTab: 'class' },
  { path: '/week.html?week=3', activeTab: 'class' },
  { path: '/admin.html', activeTab: null }, // no tab matches 'admin'
];

const EXPECTED_TABS = [
  { label: '홈', href: 'index.html', tabTarget: 'archive' },
  { label: 'Class', href: 'inha.html', tabTarget: 'class' },
  { label: 'My Studio', href: 'studio.html', tabTarget: 'studio' },
];

for (const pg of PAGES) {
  test(`${pg.path} has unified topbar with 3 tabs`, async ({ page }) => {
    await page.goto(pg.path);
    await page.waitForLoadState('domcontentloaded');
    // Wait for topbar-sync.js (DOMContentLoaded handler) to run
    await page.waitForTimeout(100);

    const tabs = await page.$$eval('.app-tabs .app-tab', (els) =>
      els.map((el) => ({
        label: (el.textContent || '').trim(),
        href: el.getAttribute('href'),
        tabTarget: el.getAttribute('data-tab-target'),
        isActive: el.classList.contains('is-active'),
      }))
    );

    expect(tabs.length).toBe(3);
    for (let i = 0; i < 3; i++) {
      expect(tabs[i].label).toBe(EXPECTED_TABS[i].label);
      expect(tabs[i].href).toBe(EXPECTED_TABS[i].href);
      expect(tabs[i].tabTarget).toBe(EXPECTED_TABS[i].tabTarget);
    }

    // Verify active tab (skip for admin.html which has no matching tab)
    if (pg.activeTab) {
      const activeTab = tabs.find((t) => t.tabTarget === pg.activeTab);
      expect(activeTab?.isActive).toBe(true);
    }
  });
}
