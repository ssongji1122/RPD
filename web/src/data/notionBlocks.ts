import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { url } from '../lib/url';

export interface RichText {
  plain_text?: string;
  text?: { content?: string; link?: { url: string } | null };
  href?: string | null;
  annotations?: Partial<Record<'bold' | 'italic' | 'code' | 'strikethrough' | 'underline', boolean>>;
}
interface BlockData {
  rich_text?: RichText[];
  caption?: RichText[];
  cells?: RichText[][];
  type?: string;
  external?: { url: string };
  file?: { url: string };
  url?: string;
  name?: string;
  title?: string;
  language?: string;
  checked?: boolean;
  is_toggleable?: boolean;
  has_column_header?: boolean;
  has_row_header?: boolean;
  icon?: { type?: string; emoji?: string } | null;
  page_id?: string;
  database_id?: string;
}
export interface NotionBlock {
  id: string;
  type: string;
  children?: NotionBlock[];
  local_url?: string;
  linked_page_title?: string;
  linked_page_url?: string;
  _resolved_title?: string;
  [key: string]: BlockData | string | NotionBlock[] | undefined;
}
export const blockData = (b: NotionBlock): BlockData => (b[b.type] as BlockData) ?? {};
export const plainText = (spans: RichText[] = []): string => spans.map(s => s.plain_text ?? s.text?.content ?? '').join('');
const escape = (text: string): string => text.replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]!);

const formerSculptImagePath = '/ssongji1122/RPD/claude/dazzling-nash/course-site/assets/images/week05/';
const sculptImageFolder = '/assets/images/week05/';
const sculptImageAlt = new Map([
  ['sculpt-draw.png', 'Blender 조각 모드에서 Draw 브러시로 면을 솟아오르게 한 모습'],
  ['sculpt-grab.png', 'Blender 조각 모드에서 Grab 브러시로 모양을 잡아당긴 모습'],
  ['sculpt-smooth.png', 'Blender 조각 모드에서 Smooth 브러시로 표면을 고른 모습'],
  ['sculpt-clay-strips.png', 'Blender 조각 모드의 Clay Strips 브러시 화면'],
  ['sculpt-crease.png', 'Blender 조각 모드의 Crease 브러시 화면'],
  ['sculpt-inflate.png', 'Blender 조각 모드의 Inflate 브러시 화면'],
  ['sculpt-snake-hook.png', 'Blender 조각 모드의 Snake Hook 브러시 화면'],
  ['qremeshify-github.png', 'QRemeshify의 GitHub 배포 페이지'],
  ['instant-meshes-github.png', 'Instant Meshes의 GitHub 저장소'],
]);
const modifiersReferenceHeadingBlock = '3051a68d-f696-4f58-871f-26692d6580db';
const correctedReferences = new Map<string, { href: string; label?: string }>([
  ['https://suno.com/og.png', { href: 'https://cdn-o.suno.com/meta-preview.jpg', label: 'Suno 공식 미리보기 이미지' }],
  ['https://docs.blender.org/manual/en/latest/modeling/meshes/tools/bevel.html', { href: 'https://docs.blender.org/manual/en/5.0/modeling/meshes/editing/edge/bevel.html' }],
  ['https://docs.blender.org/manual/en/latest/modeling/modifiers/modify/weighted_normal.html', { href: 'https://docs.blender.org/manual/en/5.0/modeling/modifiers/normals/weighted_normal.html' }],
  ['https://docs.blender.org/manual/en/latest/addons/rigging/rigify/index.html', { href: 'https://docs.blender.org/manual/en/latest/addons/rigify/index.html' }],
  ['https://docs.blender.org/manual/en/latest/addons/rigging/rigify/basics.html', { href: 'https://docs.blender.org/manual/en/latest/addons/rigify/basics.html' }],
  ['https://www.youtube.com/watch?v=0Dy3MkEzBNk', { href: 'https://studio.blender.org/training/blender-fundamentals-45-lts/blender_4-5_lts_modifiers/', label: 'Blender Studio 모디파이어 기초 영상' }],
  ['https://www.youtube.com/watch?v=8FjBBFX_bKs', { href: 'https://docs.blender.org/manual/en/5.0/modeling/modifiers/index.html', label: 'Blender 공식 모디파이어 목록' }],
  ['http://skybox.blockadelabs.com/', { href: 'https://www.blockadelabs.com/skyboxes', label: 'Skybox AI 공식 페이지' }],
  ['https://antigravity.codes/tutorial', { href: 'https://antigravity.google/docs/ide-getting-started' }],
  ['https://antigravity.codes/mcp', { href: 'https://antigravity.google/docs/ide/mcp', label: 'Google Antigravity 공식 MCP 안내' }],
  ['https://antigravity.codes/mcp/blender', { href: 'https://github.com/ageless-h/blender-mcp/blob/master/docs/clients/antigravity.md', label: 'Antigravity에서 Blender에 연결하는 예시' }],
]);

export function loadNotionWeek(week: number): { blocks: NotionBlock[]; pageId: string } {
  const name = `week${String(week).padStart(2, '0')}.json`;
  const file = [resolve(process.cwd(), '../course-site/data/notion-blocks', name), resolve(process.cwd(), 'course-site/data/notion-blocks', name)].find(existsSync);
  if (!file) return { blocks: [], pageId: '' };
  const data = JSON.parse(readFileSync(file, 'utf8'));
  const pageId = typeof data.page_id === 'string' ? data.page_id.replace(/-/g, '') : '';
  return {
    blocks: Array.isArray(data.blocks) ? data.blocks : [],
    pageId: /^[a-f0-9]{32}$/i.test(pageId) ? pageId : '',
  };
}

/** Reject executable URLs and expired Notion storage links. */
export function safeUrl(value = ''): string {
  const src = value.trim();
  if (!src || /prod-files-secure/i.test(src) || /[\u0000-\u001f\u007f]/.test(src)) return '';
  const correctedReference = correctedReferences.get(src);
  if (correctedReference) return correctedReference.href;
  if (/^https?:\/\//i.test(src)) {
    try {
      const parsed = new URL(src);
      if (parsed.hostname === 'raw.githubusercontent.com' && parsed.pathname.startsWith(formerSculptImagePath)) {
        const name = parsed.pathname.slice(formerSculptImagePath.length);
        if (sculptImageAlt.has(name)) return url(sculptImageFolder + name);
      }
      if (parsed.hostname === 'ssongji1122.github.io' && parsed.pathname.startsWith('/RPD/')) {
        if (parsed.pathname.startsWith('/RPD/assets/showme/')) return url(parsed.pathname.replace('/RPD/assets/showme/', '/showme/') + parsed.search + parsed.hash);
        const card = parsed.searchParams.get('showme');
        if (parsed.pathname === '/RPD/week.html' && card && /^[a-z0-9-]+$/.test(card)) return url(`/showme/${card}.html`);
      }
      return src;
    } catch { return ''; }
  }
  if (/^(mailto:|tel:|#)/i.test(src)) return src;
  if (/^[a-z][a-z\d+.-]*:/i.test(src) || src.startsWith('//') || src.includes('\\')) return '';
  return url('/' + src.replace(/^\.?\//, '').replace(/^RPD\//, '').replace(/^assets\/showme\//, 'showme/'));
}
export function richText(spans: RichText[] = []): string {
  return spans.map(span => {
    const source = span.href ?? span.text?.link?.url ?? '';
    const label = correctedReferences.get(source)?.label ?? plainText([span]);
    let html = escape(label);
    const annotations = span.annotations ?? {};
    for (const [key, tag] of Object.entries({ code: 'code', bold: 'strong', italic: 'em', strikethrough: 's', underline: 'u' })) {
      if (annotations[key as keyof typeof annotations]) html = `<${tag}>${html}</${tag}>`;
    }
    const href = safeUrl(source);
    return href ? `<a href="${escape(href)}" target="_blank" rel="noopener noreferrer">${html}</a>` : html;
  }).join('');
}
function mediaSrc(block: NotionBlock): string {
  const data = blockData(block);
  if (block.local_url) {
    const relative = block.local_url.replace(/^\/?(?:RPD\/)?/, '');
    const candidates = [resolve(process.cwd(), '../course-site', relative), resolve(process.cwd(), 'course-site', relative)];
    return candidates.some(existsSync) ? safeUrl(block.local_url) : '';
  }
  return safeUrl(data.type === 'external' ? data.external?.url : '');
}
function youtube(src: string): string {
  try {
    const u = new URL(src);
    const host = u.hostname.replace(/^www\./, '');
    const id = host === 'youtu.be' ? u.pathname.slice(1) : ['youtube.com', 'm.youtube.com', 'youtube-nocookie.com'].includes(host) ? u.searchParams.get('v') || u.pathname.match(/^\/(?:embed|shorts)\/([^/]+)/)?.[1] : '';
    return id && /^[\w-]{11}$/.test(id) ? `https://www.youtube.com/embed/${id}` : '';
  } catch { return ''; }
}
const iframe = (src: string, title: string) => `<iframe src="${escape(src)}" title="${escape(title)}" loading="lazy" allow="fullscreen; encrypted-media" allowfullscreen></iframe>`;

const officialAttachments = new Map([
  ['blenderkit-v3.18.1.251219.zip', ['BlenderKit 3.18.1 공식 배포 페이지', 'https://github.com/BlenderKit/Blendkit/releases/tag/v3.18.1.251219']],
  ['QRemeshify-1.1.0-windows.zip', ['QRemeshify 1.1.0 (Windows) 공식 다운로드', 'https://github.com/ksami/QRemeshify/releases/download/1.1.0/QRemeshify-1.1.0-windows.zip']],
  ['QRemeshify-1.1.0-macos.zip', ['QRemeshify 1.1.0 (macOS) 공식 다운로드', 'https://github.com/ksami/QRemeshify/releases/download/1.1.0/QRemeshify-1.1.0-macos.zip']],
  ['instant-meshes-macos.zip', ['Instant Meshes (macOS) 공식 다운로드 안내', 'https://github.com/wjakob/instant-meshes#pre-compiled-binaries']],
  ['instant-meshes-master.zip', ['Instant Meshes 공식 소스 코드', 'https://github.com/wjakob/instant-meshes']],
  ['add-on-paint-system-v2.1.10.zip', ['Paint System 2.1.10 공식 배포 페이지', 'https://github.com/natapol2547/paintsystem/releases/tag/v2.1.10']],
  ['dream-textures-main.zip', ['Dream Textures 공식 설치 파일', 'https://github.com/carson-katri/dream-textures/releases']],
]);
const skyboxSamplePack = 'Skybox+AI+Asset+Sample+Pack.zip';
const skyboxSampleGuide = 'https://docs.blockadelabs.com/web/workspace.html#help-menu';
const courseVideoTitles = new Map([
  ['31f54d65-4971-8085-ab04-e5a883597ed4', '뷰포트 변환 설정'],
  ['31f54d65-4971-800b-bc85-e1b93b05ce2c', '뷰포트 표시와 셰이딩 설정'],
  ['32654d65-4971-80f4-8e21-dede197ceb8b', '로봇 참고 이미지 배치'],
  ['32654d65-4971-80d9-99d4-f2153081e9be', '로봇 머리 대칭 모델링'],
  ['33354d65-4971-80d4-b805-ce55c7c1af15', 'Meshy 실습'],
  ['33354d65-4971-80c4-bf5d-eb15a43e70b4', 'Tripo 실습'],
  ['33354d65-4971-80ff-9282-d470cfae438d', 'Hyper3D 실습'],
  ['35054d65-4971-8042-8993-c21297e97600', 'HDRI 조명 회전'],
  ['36554d65-4971-80f9-8773-db13092ba48b', '리깅 뼈대에 뼈 추가'],
  ['36554d65-4971-80c5-b3f2-c35f61217d11', '모델을 뼈에 연결'],
  ['36554d65-4971-8045-adfc-ecb98c881846', '포즈 모드에서 연결 확인'],
  ['36554d65-4971-80cb-9ab5-db9ceb5a1404', '리깅 뼈 모양 바꾸기'],
  ['36b54d65-4971-80f4-adff-de4d2b2b3dc2', 'Mixamo 자동 리깅 결과'],
  ['36b54d65-4971-8013-abc8-eec88fd6ec1b', 'Mixamo 애니메이션 미리보기'],
  ['37254d65-4971-80a7-95cb-e60e3b59954f', '카메라 초점 거리 설정'],
  ['37254d65-4971-805a-b972-ff8b60676c3c', '카메라 피사계 심도 설정'],
  ['37354d65-4971-80b4-be10-db42ee65f048', 'Veo 로봇 얼굴 클로즈업 예제'],
  ['37a54d65-4971-80bd-a617-eb27f2a0a900', '포트폴리오 페이지 제작 예제'],
]);
const childPageCourseVideos = new Map([
  ['37a54d65-4971-809c-8c5a-fc66a0e238d1', '37a54d65-4971-80bd-a617-eb27f2a0a900'],
]);

function courseVideoLink(pageId: string, blockId: string): string {
  const page = pageId.replace(/-/g, '');
  const id = blockId.replace(/-/g, '');
  if (!/^[a-f0-9]{32}$/i.test(page) || !/^[a-f0-9]{32}$/i.test(id)) return '';
  const title = courseVideoTitles.get(blockId);
  const label = title ? `${title} 영상 보기` : '영상 보기';
  return `<a class="nb-course-video" href="https://www.notion.so/${page}#${id}">${escape(label)} (수강생용 노션)</a>`;
}

/** Recursive build-time renderer. All source text and attributes are escaped. */
export function renderBlocks(blocks: NotionBlock[], pageId: string): string {
  let html = '';
  for (let i = 0; i < blocks.length; i++) {
    const block = blocks[i];
    if (['bulleted_list_item', 'numbered_list_item'].includes(block.type)) {
      const tag = block.type === 'bulleted_list_item' ? 'ul' : 'ol';
      let items = '';
      do {
        const item = blocks[i];
        items += `<li>${richText(blockData(item).rich_text)}${renderBlocks(item.children ?? [], pageId)}</li>`;
        i++;
      } while (i < blocks.length && blocks[i].type === block.type);
      i--;
      html += `<${tag} class="nb-list">${items}</${tag}>`;
    } else html += renderBlock(block, pageId);
  }
  return html;
}
function renderBlock(block: NotionBlock, pageId: string): string {
  const data = blockData(block);
  const text = block.id === modifiersReferenceHeadingBlock ? '모디파이어 참고 영상과 문서' : richText(data.rich_text);
  const children = () => renderBlocks(block.children ?? [], pageId);
  const caption = richText(data.caption);
  if (/^heading_[1-4]$/.test(block.type)) {
    const level = block.type.slice(-1);
    return data.is_toggleable
      ? `<details class="nb-toggle"><summary class="nb-h${level}">${text}</summary>${children()}</details>`
      : `<h${level} class="nb-h${level}">${text}</h${level}>${children()}`;
  }
  switch (block.type) {
    case 'paragraph': return `<p>${text || '<br>'}</p>${children()}`;
    case 'divider': return '<hr>';
    case 'quote': return `<blockquote>${text}${children()}</blockquote>`;
    case 'toggle': return `<details class="nb-toggle"><summary>${text}</summary><div class="nb-toggle-body">${children()}</div></details>`;
    case 'callout': return `<aside class="nb-callout"><div><p>${text}</p>${children()}</div></aside>`;
    case 'to_do': return `<div class="nb-todo"><label><input type="checkbox" disabled${data.checked ? ' checked' : ''}><span>${text}</span></label>${children()}</div>`;
    case 'code': return `<div class="nb-code-wrap"><span class="nb-code-lang">${escape(data.language ?? '')}</span><button class="prompt-copy" type="button" data-copy aria-label="코드 복사" title="코드 복사"><svg aria-hidden="true" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="8" y="8" width="12" height="12" rx="2"></rect><path d="M16 8V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2"></path></svg></button><span class="copy-status" role="status"></span><pre><code>${escape(plainText(data.rich_text))}</code></pre>${caption ? `<p>${caption}</p>` : ''}</div>`;
    case 'table': {
      const rows = (block.children ?? []).filter(b => b.type === 'table_row');
      const row = (b: NotionBlock, header = false) => `<tr>${(blockData(b).cells ?? []).map((cell, i) => {
        const tag = header || (data.has_row_header && i === 0) ? 'th' : 'td';
        return `<${tag}${tag === 'th' ? ` scope="${header ? 'col' : 'row'}"` : ''}>${richText(cell)}</${tag}>`;
      }).join('')}</tr>`;
      return `<div class="nb-table-wrap" tabindex="0" role="region" aria-label="표"><table>${data.has_column_header && rows.length ? `<thead>${row(rows[0], true)}</thead>` : ''}<tbody>${rows.slice(data.has_column_header ? 1 : 0).map(b => row(b)).join('')}</tbody></table></div>`;
    }
    case 'table_row': return '';
    case 'column_list': return `<div class="nb-columns">${children()}</div>`;
    case 'column': return `<div class="nb-column">${children()}</div>`;
    case 'synced_block': return children();
    case 'image': {
      const src = mediaSrc(block);
      const restoredAlt = src.startsWith(url(sculptImageFolder)) ? sculptImageAlt.get(src.slice(url(sculptImageFolder).length)) : '';
      const alt = plainText(data.caption) || restoredAlt || '';
      return src ? `<figure><img src="${escape(src)}" alt="${escape(alt)}" loading="lazy">${caption ? `<figcaption>${caption}</figcaption>` : ''}</figure>` : '';
    }
    case 'video': {
      const src = mediaSrc(block);
      if (data.type === 'file' && (!src || courseVideoTitles.has(block.id))) {
        const link = courseVideoLink(pageId, block.id);
        if (link) return `<p>${link}${caption ? `<br>${caption}` : ''}</p>`;
      }
      return src ? `<figure class="nb-video">${youtube(src) ? iframe(youtube(src), plainText(data.caption) || '영상') : `<video src="${escape(src)}" controls preload="metadata"></video>`}${caption ? `<figcaption>${caption}</figcaption>` : ''}</figure>` : `<p>영상을 현재 열 수 없습니다.${caption ? ` ${caption}` : ''}</p>`;
    }
    case 'file': {
      const official = data.name ? officialAttachments.get(data.name) : undefined;
      if (official) {
        const [label, href] = official;
        return `<p><a href="${escape(href)}">${escape(label)}</a>${caption ? `<br>${caption}` : ''}</p>`;
      }
      if (data.name === skyboxSamplePack) {
        return `<p><a href="${skyboxSampleGuide}">Skybox AI 샘플팩 공식 안내</a><br>제작자 안내에서 샘플팩을 다운로드할 수 없어요.${caption ? `<br>${caption}` : ''}</p>`;
      }
      const src = mediaSrc(block);
      return src ? `<p><a href="${escape(src)}" download rel="noopener">${escape(data.name || src.split('?')[0].split('/').pop() || '파일 다운로드')}</a>${caption ? `<br>${caption}` : ''}</p>` : `<p>첨부파일을 현재 열 수 없습니다.${data.name ? ` (${escape(data.name)})` : ''}</p>`;
    }
    case 'embed': {
      const src = safeUrl(data.url);
      return src ? `<figure class="nb-embed${src.includes('/showme/') ? ' nb-embed-showme' : ''}">${iframe(youtube(src) || src, plainText(data.caption) || '삽입 자료')}<figcaption><a href="${escape(src)}" target="_blank" rel="noopener noreferrer">자료 새 창에서 열기</a>${caption ? ` — ${caption}` : ''}</figcaption></figure>` : '';
    }
    case 'bookmark': {
      const src = safeUrl(data.url);
      return src ? `<p class="nb-bookmark"><a href="${escape(src)}" target="_blank" rel="noopener noreferrer">${caption || escape(src)}</a></p>` : '';
    }
    case 'child_page':
    case 'link_to_page': {
      const id = block.type === 'child_page' ? block.id : data.page_id || data.database_id;
      const href = safeUrl(block.linked_page_url || (id ? `https://www.notion.so/${id.replace(/-/g, '')}` : ''));
      if (!href) return '';
      const videoId = childPageCourseVideos.get(block.id);
      const videoLink = id && videoId ? courseVideoLink(id, videoId) : '';
      return `<p><a href="${escape(href)}" target="_blank" rel="noopener noreferrer">${escape(data.title || block.linked_page_title || block._resolved_title || 'Notion 페이지에서 열기')}</a>${videoLink ? `<br>${videoLink}` : ''}</p>`;
    }
    default: return '';
  }
}

export function hasSection(blocks: NotionBlock[], pattern: RegExp): boolean {
  return blocks.some(b => (/^heading_/.test(b.type) && pattern.test(plainText(blockData(b).rich_text))) || hasSection(b.children ?? [], pattern));
}
