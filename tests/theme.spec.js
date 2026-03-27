// @ts-check
const { test, expect } = require('@playwright/test');

test('theme toggle switches to light', async ({ page }) => {
  await page.goto('/index.html');

  // Click theme toggle
  await page.click('.theme-toggle');
  await page.waitForTimeout(200);

  const theme = await page.evaluate(() =>
    document.documentElement.getAttribute('data-theme')
  );
  expect(theme).toBe('light');
});

test('theme toggle returns to dark', async ({ page }) => {
  await page.goto('/index.html');

  // Toggle twice: dark → light → dark
  await page.click('.theme-toggle');
  await page.waitForTimeout(200);
  await page.click('.theme-toggle');
  await page.waitForTimeout(200);

  const theme = await page.evaluate(() =>
    document.documentElement.getAttribute('data-theme')
  );
  // After double toggle, should be dark or null (both mean dark)
  expect(theme === 'dark' || theme === null).toBeTruthy();
});

test('theme persists across navigation', async ({ page }) => {
  await page.goto('/index.html');

  // Switch to light
  await page.click('.theme-toggle');
  await page.waitForTimeout(200);

  // Navigate to another page
  await page.goto('/library.html');

  const theme = await page.evaluate(() =>
    document.documentElement.getAttribute('data-theme')
  );
  expect(theme).toBe('light');
});
