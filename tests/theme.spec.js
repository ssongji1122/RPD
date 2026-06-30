// @ts-check
const { test, expect } = require('@playwright/test');

test('theme toggle switches to dark', async ({ page }) => {
  await page.goto('/index.html');

  await page.click('.theme-toggle');
  await page.waitForTimeout(200);

  const theme = await page.evaluate(() =>
    document.documentElement.getAttribute('data-theme')
  );
  expect(theme).toBe('dark');
});

test('theme toggle returns to default light', async ({ page }) => {
  await page.goto('/index.html');

  await page.click('.theme-toggle');
  await page.waitForTimeout(200);
  await page.click('.theme-toggle');
  await page.waitForTimeout(200);

  const theme = await page.evaluate(() =>
    document.documentElement.getAttribute('data-theme')
  );
  expect(theme).toBe(null);
});

test('theme persists across navigation', async ({ page }) => {
  await page.goto('/index.html');

  await page.click('.theme-toggle');
  await page.waitForTimeout(200);

  // Navigate to another page
  await page.goto('/library.html');

  const theme = await page.evaluate(() =>
    document.documentElement.getAttribute('data-theme')
  );
  expect(theme).toBe('dark');
});
