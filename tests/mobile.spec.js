// @ts-check
const { test, expect } = require('@playwright/test');

test.describe('mobile layout', () => {
  test.skip(({ viewport }) => viewport.width > 720, 'mobile only');

  test('tabs visible on mobile', async ({ page }) => {
    await page.goto('/index.html');
    await expect(page.locator('.app-tabs')).toBeVisible();
  });

  test('sidebar hidden on mobile', async ({ page }) => {
    await page.goto('/index.html');
    const rail = page.locator('.rail');
    const box = await rail.boundingBox();
    if (box) {
      expect(box.x).toBeLessThan(0);
    }
  });

  test('deeplink week.html?week=3 loads', async ({ page }) => {
    await page.goto('/week.html?week=3');
    await expect(page).toHaveTitle(/Week 3/);
    const heading = page.locator('#hero-section .hero-copy h1');
    await expect(heading).toBeVisible();
    await expect(heading).toContainText('기초 모델링');
  });
});
