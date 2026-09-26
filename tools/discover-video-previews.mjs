#!/usr/bin/env node

import { readFile, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';

const ROOT = resolve(import.meta.dirname, '..');
const CANONICAL_PATH = resolve(ROOT, 'weeks/site-data.json');
const WRITE = process.argv.includes('--write');
const BLENDER_STUDIO_HOST = 'studio.blender.org';
const LINK_ONLY_VIDEO_URLS = new Set([
  'https://docs.polyhaven.com/en/guides/blender-addon',
  'https://www.youtube.com/@BlenderOfficial',
]);
const REPLACEMENT_URLS = new Map([
  ['https://studio.blender.org/training/blender-2-8-fundamentals/modifiers/', 'https://studio.blender.org/training/blender-fundamentals-45-lts/blender_4-5_lts_modifiers/'],
  ['https://studio.blender.org/training/blender-2-8-fundamentals/materials-and-shading/', 'https://studio.blender.org/training/blender-2-8-fundamentals/intro-shading/'],
  ['https://studio.blender.org/training/blender-2-8-fundamentals/lighting/', 'https://studio.blender.org/training/blender-2-8-fundamentals/light-types/'],
  ['https://studio.blender.org/training/blender-2-8-fundamentals/animation/', 'https://studio.blender.org/training/blender-2-8-fundamentals/keyframes/'],
  ['https://studio.blender.org/training/blender-2-8-fundamentals/armature-and-rigging/', 'https://studio.blender.org/training/blender-2-8-fundamentals/rigging-intro/'],
  ['https://studio.blender.org/training/blender-2-8-fundamentals/importing/', 'https://studio.blender.org/training/character-animation/5ce4067c75e1fd8da56e0933/'],
  ['https://studio.blender.org/training/blender-2-8-fundamentals/rendering/', 'https://studio.blender.org/training/blender-2-8-fundamentals/render-settings-introduction/'],
]);

function youtubeVideoId(url) {
  const host = url.hostname.replace(/^www\./, '');
  if (host === 'youtu.be') return url.pathname.split('/').filter(Boolean)[0] || '';
  if (!['youtube.com', 'm.youtube.com'].includes(host)) return '';
  if (url.pathname === '/watch') return url.searchParams.get('v') || '';
  return url.pathname.match(/^\/(?:embed|shorts|live)\/([^/]+)/)?.[1] || '';
}

async function blenderPreviewUrl(sourceUrl) {
  const response = await fetch(sourceUrl);
  if (!response.ok) throw new Error(`${sourceUrl}: HTTP ${response.status}`);
  const html = await response.text();
  const match = html.match(/href="\/download-source\/(files\/[^"]+\.mp4)"/i)
    || html.match(/<source src="https:\/\/studio\.blender\.org\/(files\/[^"?]+\.mp4)\?/i);
  if (!match) throw new Error(`${sourceUrl}: stable MP4 download path not found`);
  return new URL(`/download-source/${match[1]}`, sourceUrl).toString();
}

const curriculum = JSON.parse(await readFile(CANONICAL_PATH, 'utf8'));
let discovered = 0;

for (const week of curriculum) {
  const retainedVideos = [];
  const restoredLinks = (week.docs || []).filter((item) => LINK_ONLY_VIDEO_URLS.has(item.url));
  if (restoredLinks.length > 0) {
    week.videos = [...(week.videos || []), ...restoredLinks];
    week.docs = (week.docs || []).filter((item) => !LINK_ONLY_VIDEO_URLS.has(item.url));
  }
  for (const video of week.videos || []) {
    if (REPLACEMENT_URLS.has(video.url)) video.url = REPLACEMENT_URLS.get(video.url);
    const source = new URL(video.url);
    const isChannel = source.hostname.includes('youtube.com') && source.pathname.startsWith('/@');
    if (source.hostname === 'docs.polyhaven.com' || isChannel) {
      retainedVideos.push(video);
      continue;
    }

    if (source.hostname === BLENDER_STUDIO_HOST && !video.preview_url) {
      video.preview_url = await blenderPreviewUrl(video.url);
      discovered += 1;
    }

    const hasPreview = Boolean(video.preview_url) || Boolean(youtubeVideoId(source));
    if (!hasPreview) throw new Error(`${video.url}: embeddable preview not found`);
    retainedVideos.push(video);
  }

  week.videos = retainedVideos;
}

if (WRITE) {
  await writeFile(CANONICAL_PATH, `${JSON.stringify(curriculum, null, 2)}\n`);
}

console.log(JSON.stringify({
  mode: WRITE ? 'write' : 'dry-run',
  discovered,
  remainingVideos: curriculum.reduce((sum, week) => sum + (week.videos || []).length, 0),
}));
