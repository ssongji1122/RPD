// course-site 정적 자산 → web/public 빌드타임 동기화.
// 자산 SoT는 course-site 하나만 유지한다 — 수동 복사본 드리프트로 라이브 404가 났던
// 원인 제거 (final-projects 미디어 PR #114, showme 위젯 JS 2026-07-07 사례).
// package.json 의 predev/prebuild 훅으로 자동 실행된다.
import { cpSync, rmSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const PAIRS = [
  ['../../course-site/assets/final-projects', '../public/assets/final-projects'],
  ['../../course-site/assets/showme', '../public/showme'],
  ['../../course-site/assets/images', '../public/assets/images'],
];

for (const [srcRel, destRel] of PAIRS) {
  const src = resolve(here, srcRel);
  const dest = resolve(here, destRel);
  if (!existsSync(src)) {
    console.error(`[sync-final-assets] source not found: ${src}`);
    process.exit(1);
  }
  rmSync(dest, { recursive: true, force: true });
  cpSync(src, dest, { recursive: true });
  console.log(`[sync-final-assets] synced ${src} -> ${dest}`);
}
