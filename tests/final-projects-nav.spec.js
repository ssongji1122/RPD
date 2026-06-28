// @ts-check
const { test, expect } = require('@playwright/test');

test('final-projects tab navigates from home', async ({ page }) => {
  await page.goto('/index.html');
  await page.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(200);

  const worksTab = page.locator('.app-tab[data-tab-target="final"]');
  await expect(worksTab).toHaveCount(1);
  await worksTab.click();
  await page.waitForURL('**/final-projects.html');
  expect(page.url()).toContain('final-projects.html');
});

test('gallery rail spans viewport width', async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto('/final-projects.html');
  await page.waitForLoadState('domcontentloaded');
  await page.waitForSelector('.final-gallery-rail .final-gallery-panel');

  const metrics = await page.evaluate(function () {
    var rail = document.querySelector('.final-gallery-rail');
    var panels = Array.prototype.slice.call(document.querySelectorAll('.final-gallery-panel'));
    var railRect = rail ? rail.getBoundingClientRect() : { width: 0, left: 0, right: 0 };
    var panelRects = panels.map(function (panel) {
      return panel.getBoundingClientRect();
    });
    var leftmost = panelRects.length ? Math.min.apply(null, panelRects.map(function (r) { return r.left; })) : 0;
    var rightmost = panelRects.length ? Math.max.apply(null, panelRects.map(function (r) { return r.right; })) : 0;
    return {
      viewport: window.innerWidth,
      railWidth: railRect.width,
      spanWidth: rightmost - leftmost,
      panelCount: panels.length
    };
  });

  expect(metrics.panelCount).toBeGreaterThan(0);
  expect(metrics.railWidth).toBeGreaterThan(metrics.viewport * 0.9);
  expect(metrics.spanWidth).toBeGreaterThan(metrics.viewport * 0.85);
});

test('gallery panel opens detail view', async ({ page }) => {
  await page.goto('/final-projects.html');
  await page.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(300);

  const panel = page.locator('.final-gallery-panel').first();
  await expect(panel).toHaveCount(1);
  await panel.click();
  await page.waitForTimeout(200);

  await expect(page.locator('.final-layout')).toHaveAttribute('data-view', 'detail');
  await expect(page.locator('.final-detail-sheet')).toBeVisible();
  await expect(page.locator('.final-media-main')).toBeVisible();
});

test('detail view shows AI section when process media exists', async ({ page }) => {
  await page.goto('/final-projects.html#project-10');
  await page.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(300);

  await expect(page.locator('.final-layout')).toHaveAttribute('data-view', 'detail');
  await expect(page.locator('.final-section-ai')).toBeVisible();
  await expect(page.locator('.final-ai-card')).toHaveCount(7);
});

test('detail view embeds Google Slides presentation', async ({ page }) => {
  await page.goto('/final-projects.html#project-23');
  await page.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(300);

  await expect(page.locator('.final-section-presentation')).toBeVisible();
  await expect(page.locator('.final-presentation-frame iframe')).toHaveAttribute('src', /docs\.google\.com\/presentation/);
  await expect(page.locator('.final-web-embed-open')).toHaveAttribute('href', /\/presentation\/d\/.*\/edit/);
});

test('AI card opens full-size viewer', async ({ page }) => {
  await page.goto('/final-projects.html#project-10');
  await page.waitForLoadState('domcontentloaded');
  await page.waitForSelector('.final-ai-card');

  await page.locator('.final-ai-card').first().click();
  await expect(page.locator('.final-ai-viewer')).toBeVisible();
  await expect(page.locator('.final-ai-viewer-image')).toBeVisible();
});
