// course-site/assets/final-projects → web/public/assets/final-projects 빌드타임 동기화.
// 미디어 SoT는 course-site 하나만 유지한다 (수동 복사본 드리프트로 라이브 404가 났던 원인 제거).
// package.json 의 predev/prebuild 훅으로 자동 실행된다.
import { cpSync, rmSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const src = resolve(here, '../../course-site/assets/final-projects');
const dest = resolve(here, '../public/assets/final-projects');

if (!existsSync(src)) {
  console.error(`[sync-final-assets] source not found: ${src}`);
  process.exit(1);
}

rmSync(dest, { recursive: true, force: true });
cpSync(src, dest, { recursive: true });
console.log(`[sync-final-assets] synced ${src} -> ${dest}`);
