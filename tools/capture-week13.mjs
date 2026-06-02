// Week 13 Blender docs 캡처 (node @playwright/test 기반)
// 🔴 one-off 도구: python playwright 미설치 환경의 응급 캡처용. 정식 도구는 /capture (capture_screenshots.py).
//    이미지 파일만 생성하며 curriculum/Notion은 건드리지 않는다. step↔이미지 연결은 Notion(정석) 또는 overrides.json.
// Python capture_screenshots.py의 _crop_figures / take_screenshot 로직을 재현.
// figure/img를 크롭, 없으면 콘텐츠 영역 fullpage fallback.
import { chromium } from '@playwright/test';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const OUT_DIR = path.join(ROOT, 'course-site', 'assets', 'images', 'week13');

// (filename, [후보 URL들 — 첫 성공 URL 사용])
const TARGETS = [
  ['camera-setup', [
    'https://docs.blender.org/manual/en/latest/render/cameras.html',
  ]],
  ['eevee-render', [
    'https://docs.blender.org/manual/en/latest/render/eevee/introduction.html',
    'https://docs.blender.org/manual/en/latest/render/eevee/index.html',
  ]],
  ['cycles-render', [
    'https://docs.blender.org/manual/en/latest/render/cycles/introduction.html',
    'https://docs.blender.org/manual/en/latest/render/cycles/index.html',
  ]],
  ['video-sequencer', [
    'https://docs.blender.org/manual/en/latest/video_editing/introduction.html',
    'https://docs.blender.org/manual/en/latest/video_editing/index.html',
    'https://docs.blender.org/manual/en/latest/editors/video_sequencer/introduction.html',
  ]],
];

const CLEAN_JS = () => {
  const hide = ['[class*="sidebar"]', '[class*="toc"]', 'nav', 'header', 'footer',
    '.mobile-header', '.related-pages', '.prev-next'];
  hide.forEach(sel => document.querySelectorAll(sel).forEach(el => { el.style.display = 'none'; }));
  const art = document.querySelector('article') || document.querySelector('.bd-content') || document.body;
  art.style.cssText += 'max-width:860px;margin:0 auto;padding:32px;';
  document.body.style.background = '#111';
  return 'ok';
};

async function cropFigures(page, outPath) {
  let locator = page.locator('article figure, .bd-content figure');
  let count = await locator.count();
  if (count === 0) {
    locator = page.locator('article img, .bd-content img');
    count = await locator.count();
  }
  const boxes = [];
  for (let i = 0; i < Math.min(count, 3); i++) {
    try {
      const box = await locator.nth(i).boundingBox();
      if (box && box.width > 150 && box.height > 80) boxes.push(box);
    } catch { /* skip */ }
  }
  if (boxes.length === 0) return false;
  const x1 = Math.min(...boxes.map(b => b.x));
  const y1 = Math.min(...boxes.map(b => b.y));
  const x2 = Math.max(...boxes.map(b => b.x + b.width));
  const y2 = Math.max(...boxes.map(b => b.y + b.height));
  const pad = 16;
  const clip = {
    x: Math.max(0, x1 - pad),
    y: Math.max(0, y1 - pad),
    width: (x2 - x1) + pad * 2,
    height: (y2 - y1) + pad * 2,
  };
  await page.screenshot({ path: outPath, clip, fullPage: true });
  return true;
}

async function capture(page, fname, urls) {
  for (const url of urls) {
    try {
      const resp = await page.goto(url, { timeout: 25000, waitUntil: 'networkidle' });
      if (!resp || resp.status() >= 400) {
        console.log(`  ⚠ ${resp ? resp.status() : 'no-resp'} — ${url}`);
        continue;
      }
      await page.evaluate(CLEAN_JS);
      await page.waitForTimeout(700);
      const outPath = path.join(OUT_DIR, `${fname}.png`);
      const cropped = await cropFigures(page, outPath);
      if (cropped) {
        console.log(`  ✓ cropped → week13/${fname}.png  (${url})`);
      } else {
        await page.screenshot({ path: outPath, fullPage: false });
        console.log(`  ✓ fullpage → week13/${fname}.png  (${url})`);
      }
      return true;
    } catch (e) {
      console.log(`  ✗ ${url}: ${e.message.split('\n')[0]}`);
    }
  }
  return false;
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 820 }, colorScheme: 'dark' });
  const page = await ctx.newPage();
  console.log(`총 ${TARGETS.length}개 캡처 시도\n`);
  let ok = 0;
  for (const [fname, urls] of TARGETS) {
    const success = await capture(page, fname, urls);
    if (success) ok++;
  }
  await browser.close();
  console.log(`\n완료: ${ok}/${TARGETS.length} 성공`);
})();
