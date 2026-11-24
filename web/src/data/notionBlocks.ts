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

export function loadNotionBlocks(week: number): NotionBlock[] {
  const name = `week${String(week).padStart(2, '0')}.json`;
  const file = [resolve(process.cwd(), '../course-site/data/notion-blocks', name), resolve(process.cwd(), 'course-site/data/notion-blocks', name)].find(existsSync);
  if (!file) return [];
  const data = JSON.parse(readFileSync(file, 'utf8'));
  return Array.isArray(data.blocks) ? data.blocks : [];
}

/** Reject executable URLs and expired Notion storage links. */
export function safeUrl(value = ''): string {
  const src = value.trim();
  if (!src || /prod-files-secure/i.test(src) || /[\u0000-\u001f\u007f]/.test(src)) return '';
  if (/^https?:\/\//i.test(src)) {
    try {
      const parsed = new URL(src);
      if (parsed.hostname === 'ssongji1122.github.io' && parsed.pathname.startsWith('/RPD/assets/showme/')) return url(parsed.pathname.replace('/RPD/assets/showme/', '/showme/') + parsed.search + parsed.hash);
      return src;
    } catch { return ''; }
  }
  if (/^(mailto:|tel:|#)/i.test(src)) return src;
  if (/^[a-z][a-z\d+.-]*:/i.test(src) || src.startsWith('//') || src.includes('\\')) return '';
  return url('/' + src.replace(/^\.?\//, '').replace(/^RPD\//, '').replace(/^assets\/showme\//, 'showme/'));
}
export function richText(spans: RichText[] = []): string {
  return spans.map(span => {
    let html = escape(plainText([span]));
    const annotations = span.annotations ?? {};
    for (const [key, tag] of Object.entries({ code: 'code', bold: 'strong', italic: 'em', strikethrough: 's', underline: 'u' })) {
      if (annotations[key as keyof typeof annotations]) html = `<${tag}>${html}</${tag}>`;
    }
    const href = safeUrl(span.href ?? span.text?.link?.url ?? '');
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

/** Recursive build-time renderer. All source text and attributes are escaped. */
export function renderBlocks(blocks: NotionBlock[]): string {
  let html = '';
  for (let i = 0; i < blocks.length; i++) {
    const block = blocks[i];
    if (['bulleted_list_item', 'numbered_list_item'].includes(block.type)) {
      const tag = block.type === 'bulleted_list_item' ? 'ul' : 'ol';
      let items = '';
      do {
        const item = blocks[i];
        items += `<li>${richText(blockData(item).rich_text)}${renderBlocks(item.children ?? [])}</li>`;
        i++;
      } while (i < blocks.length && blocks[i].type === block.type);
      i--;
      html += `<${tag} class="nb-list">${items}</${tag}>`;
    } else html += renderBlock(block);
  }
  return html;
}
function renderBlock(block: NotionBlock): string {
  const data = blockData(block);
  const text = richText(data.rich_text);
  const children = () => renderBlocks(block.children ?? []);
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
      return src ? `<figure><img src="${escape(src)}" alt="${escape(plainText(data.caption))}" loading="lazy">${caption ? `<figcaption>${caption}</figcaption>` : ''}</figure>` : '';
    }
    case 'video': {
      const src = mediaSrc(block);
      return src ? `<figure class="nb-video">${youtube(src) ? iframe(youtube(src), plainText(data.caption) || '영상') : `<video src="${escape(src)}" controls preload="metadata"></video>`}${caption ? `<figcaption>${caption}</figcaption>` : ''}</figure>` : `<p>영상을 현재 열 수 없습니다.${caption ? ` ${caption}` : ''}</p>`;
    }
    case 'file': {
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
      return href ? `<p><a href="${escape(href)}" target="_blank" rel="noopener noreferrer">${escape(data.title || block.linked_page_title || block._resolved_title || 'Notion 페이지에서 열기')}</a></p>` : '';
    }
    default: return '';
  }
}

export function hasSection(blocks: NotionBlock[], pattern: RegExp): boolean {
  return blocks.some(b => (/^heading_/.test(b.type) && pattern.test(plainText(blockData(b).rich_text))) || hasSection(b.children ?? [], pattern));
}
