// @ts-check
const { test, expect } = require('@playwright/test');

test.describe('sidebar (desktop only)', () => {
  test.skip(({ viewport }) => viewport.width < 720, 'desktop only');

  test('archive pages show sidebar links', async ({ page }) => {
    await page.goto('/index.html');
    const rail = page.locator('.rail');
    await expect(rail).toBeVisible();
    await expect(rail.locator('a[href="library.html"], a[href="/library.html"]')).toBeVisible();
    await expect(rail.locator('a[href="shortcuts.html"], a[href="/shortcuts.html"]')).toBeVisible();
  });

  test('sidebar toggle expands and collapses', async ({ page }) => {
    await page.goto('/index.html');
    const rail = page.locator('.rail');

    // Initially collapsed (56px)
    const initialWidth = await rail.evaluate(el => el.offsetWidth);
    expect(initialWidth).toBeLessThanOrEqual(60);

    // Click toggle to expand
    await page.click('.rail-toggle');
    await page.waitForTimeout(300);
    const expandedWidth = await rail.evaluate(el => el.offsetWidth);
    expect(expandedWidth).toBeGreaterThan(100);

    // Click toggle to collapse
    await page.click('.rail-toggle');
    await page.waitForTimeout(300);
    const collapsedWidth = await rail.evaluate(el => el.offsetWidth);
    expect(collapsedWidth).toBeLessThanOrEqual(60);
  });

  test('user profile visible when sidebar expanded', async ({ page }) => {
    await page.goto('/index.html');
    await page.click('.rail-toggle');
    await page.waitForTimeout(300);

    const profile = page.locator('.rail-user');
    await expect(profile).toBeVisible();
    await expect(page.locator('.rail-user-name')).toContainText(/게스트/);
  });
});
