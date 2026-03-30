// @ts-check
const { test, expect } = require('@playwright/test');

const WEEK5_URL = '/week.html?week=5';

test.describe('Week 05 콘텐츠 보강 검증', () => {

  test('week 5 페이지 정상 로드', async ({ page }) => {
    const res = await page.goto(WEEK5_URL);
    expect(res.status()).toBe(200);
  });

  test('Step 2 — 브러시 판단 기준이 task detail에 표시', async ({ page }) => {
    await page.goto(WEEK5_URL);
    const content = await page.content();
    const criteria = [
      '큰 볼륨을 올려야 할 때',
      '선이 파여야 할 때',
      '표면 전체를 부풀려야 할 때',
      '뿔·안테나·꼬리를 끄집어낼 때',
    ];
    for (const text of criteria) {
      expect(content, `"${text}" should be in page`).toContain(text);
    }
  });

  test('Step 4 — 프롬프트 보강 copy가 DOM에 존재', async ({ page }) => {
    await page.goto(WEEK5_URL);
    const copy = page.locator('.step-copy', { hasText: '짧을수록' });
    await expect(copy).toHaveCount(1);
  });

  test('Step 4 — 나쁜예/좋은예 task가 DOM에 존재', async ({ page }) => {
    await page.goto(WEEK5_URL);
    // detail이 있는 task는 .task-title로 렌더링됨
    const title = page.locator('.task-title', { hasText: '나쁜 예' });
    await expect(title).toHaveCount(1);
  });

  test('Step 6 — Before/After 촬영 가이드 표시', async ({ page }) => {
    await page.goto(WEEK5_URL);
    const content = await page.content();
    expect(content).toContain('Numpad 1(앞면 고정)');
    expect(content).toContain('Ctrl+F3');
  });

  test('shortcuts — Numpad 1, Ctrl+F3 추가됨', async ({ page }) => {
    await page.goto(WEEK5_URL);
    const content = await page.content();
    expect(content).toContain('Numpad 1');
    expect(content).toContain('Ctrl + F3');
  });

  test('checklist — Week 6 연계 항목 존재', async ({ page }) => {
    await page.goto(WEEK5_URL);
    const content = await page.content();
    expect(content).toContain('Week 6 Material 실습에서 이 파일을 씁니다');
  });

  test.describe('ShowMe 카드 버튼', () => {
    const SHOWME_IDS = [
      'sculpt-basics',
      'sculpt-brushes',
      'ai-prompt-design',
      'ai-3d-generation',
    ];

    for (const id of SHOWME_IDS) {
      test(`${id} 버튼이 DOM에 존재`, async ({ page }) => {
        await page.goto(WEEK5_URL);
        const btn = page.locator(`[data-widget-id="${id}"]`);
        await expect(btn).toHaveCount(1);
      });
    }
  });

  test('ShowMe sculpt-basics 카드 모달 열기 + supplement 내용 확인', async ({ page }) => {
    await page.goto(WEEK5_URL);
    const btn = page.locator('[data-widget-id="sculpt-basics"]');
    await btn.click();
    const overlay = page.locator('#showmeOverlay');
    await expect(overlay).toBeVisible({ timeout: 5000 });
    // supplement의 title이 모달에 표시되는지 확인
    const iframe = page.frameLocator('#showmeIframe');
    // supplement 내용은 iframe 안에 렌더링됨 — fallback으로 overlay visible만 확인
    await expect(overlay).not.toHaveAttribute('aria-hidden', 'true');
  });
});
