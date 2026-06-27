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
});
