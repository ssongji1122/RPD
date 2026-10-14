// @ts-check
const { test, expect } = require('@playwright/test');

test('week reference video embeds a preview and opens the original source', async ({ page }) => {
  await page.goto('/week.html?week=1');

  const reference = page.locator('details.ref-accordion');
  await reference.locator('summary').click();

  const card = reference.locator('.source-video-preview');
  await expect(card).toHaveCount(1);
  await expect(card.locator('video')).toHaveAttribute('src', /\.mp4$/);
  await expect(card.locator('.source-video-preview-hit')).toHaveAttribute(
    'href',
    'https://studio.blender.org/training/blender-2-8-fundamentals/first-steps/',
  );
  await expect(card.locator('.source-video-preview-hit')).toHaveAttribute('target', '_blank');
  const hasHorizontalOverflow = await page.evaluate(
    () => document.documentElement.scrollWidth > document.documentElement.clientWidth,
  );
  expect(hasHorizontalOverflow).toBe(false);
});
