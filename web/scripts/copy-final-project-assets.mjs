import { cp, mkdir, stat } from 'node:fs/promises';
import { resolve } from 'node:path';

const projectRoot = resolve(import.meta.dirname, '..', '..');

const copies = [
  {
    label: 'final project assets',
    source: resolve(projectRoot, 'course-site', 'assets', 'final-projects'),
    target: resolve(projectRoot, 'web', 'dist', 'assets', 'final-projects'),
  },
  {
    label: 'Show Me cards',
    source: resolve(projectRoot, 'course-site', 'assets', 'showme'),
    target: resolve(projectRoot, 'web', 'dist', 'showme'),
  },
];

for (const item of copies) {
  await stat(item.source);
  await mkdir(resolve(item.target, '..'), { recursive: true });
  await cp(item.source, item.target, { recursive: true, force: true });
  console.log(`Copied ${item.label}: ${item.source} -> ${item.target}`);
}
