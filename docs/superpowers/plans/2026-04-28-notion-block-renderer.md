# Notion Block Renderer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `week.html` renders Notion block tree (`data/notion-blocks/weekN.json`) as primary page content, falling back to `curriculum.js` renderer when JSON is absent.

**Architecture:** New `notion-renderer.js` module handles all block-to-HTML rendering; `notion-blocks.css` provides `.nb-*` styles; `week.html` gets a fetch-first init that calls `renderNotionPage()` when JSON exists. Sidebar (videos, shortcuts, docs) is extracted from `buildPage()` into `buildSidebar()` and shared by both render paths.

**Tech Stack:** Vanilla JS (ES5-compatible IIFE), CSS custom properties from existing `tokens.css`, static JSON fetch via `window.fetch`.

**Spec:** `docs/superpowers/specs/2026-04-28-notion-block-renderer-design.md`

**Working directory:** `course-site/` (all paths below are relative to repo root)

---

## Task 1: Create `notion-blocks.css`

**Files:**
- Create: `course-site/assets/notion-blocks.css`

- [ ] **Step 1: Create the CSS file with all `.nb-*` styles**

Create `course-site/assets/notion-blocks.css`:

```css
/* Notion block renderer styles — prefix: .nb-* */

/* ── Headings ──────────────────────────────────────────── */
.nb-h1 { font-size: var(--fs-4, 1.75rem); font-weight: 700; margin: 2rem 0 .75rem; line-height: 1.25; }
.nb-h2 { font-size: var(--fs-3, 1.375rem); font-weight: 700; margin: 1.75rem 0 .6rem; line-height: 1.3; }
.nb-h3 { font-size: var(--fs-2, 1.125rem); font-weight: 600; margin: 1.5rem 0 .5rem; line-height: 1.35; }

/* ── Paragraph / Quote ─────────────────────────────────── */
.nb-p { margin: .5rem 0; line-height: 1.75; }
.nb-p:empty { display: none; }
.nb-spacer { display: block; height: .75rem; }
.nb-quote { border-left: 3px solid var(--key); padding: .5rem 1rem; margin: 1rem 0; color: var(--muted); font-style: italic; }

/* ── Lists ─────────────────────────────────────────────── */
.nb-ul, .nb-ol { margin: .5rem 0 .5rem 1.5rem; padding: 0; }
.nb-ul > li, .nb-ol > li { margin: .3rem 0; line-height: 1.7; }
.nb-ul > li > .nb-children,
.nb-ol > li > .nb-children { margin-top: .3rem; }

/* ── To-do ─────────────────────────────────────────────── */
.nb-todo { display: flex; align-items: flex-start; gap: .5rem; margin: .3rem 0; cursor: default; line-height: 1.7; }
.nb-todo input[type="checkbox"] { margin-top: .25rem; flex-shrink: 0; accent-color: var(--key); }
.nb-todo--checked .nb-todo-text { text-decoration: line-through; color: var(--muted); }

/* ── Toggle ────────────────────────────────────────────── */
.nb-toggle { margin: .5rem 0; }
.nb-toggle > summary {
  cursor: pointer;
  list-style: none;
  display: flex;
  align-items: flex-start;
  gap: .5rem;
  font-weight: 500;
  padding: .25rem 0;
  user-select: none;
}
.nb-toggle > summary::-webkit-details-marker { display: none; }
.nb-toggle > summary::before {
  content: "▶";
  font-size: .7em;
  margin-top: .35rem;
  flex-shrink: 0;
  transition: transform .2s;
  color: var(--muted);
}
.nb-toggle[open] > summary::before { transform: rotate(90deg); }
.nb-toggle-body { padding-left: 1.5rem; margin-top: .25rem; }

/* ── Callout ───────────────────────────────────────────── */
.nb-callout {
  display: flex;
  gap: .75rem;
  padding: .75rem 1rem;
  border-radius: var(--radius, 6px);
  margin: .75rem 0;
  background: var(--bg-2, rgba(255,255,255,.04));
  border-left: 3px solid var(--key);
}
.nb-callout--gray   { border-color: var(--muted); }
.nb-callout--red    { border-color: #ef4444; background: rgba(239,68,68,.08); }
.nb-callout--orange { border-color: #f97316; background: rgba(249,115,22,.08); }
.nb-callout--yellow { border-color: #eab308; background: rgba(234,179,8,.08); }
.nb-callout--green  { border-color: #22c55e; background: rgba(34,197,94,.08); }
.nb-callout--blue   { border-color: var(--key); background: rgba(0,191,165,.08); }
.nb-callout--purple { border-color: #a855f7; background: rgba(168,85,247,.08); }
.nb-callout--pink   { border-color: #ec4899; background: rgba(236,72,153,.08); }
.nb-callout--brown  { border-color: #92400e; background: rgba(146,64,14,.08); }
.nb-callout-icon { font-size: 1.2em; flex-shrink: 0; line-height: 1.75; }
.nb-callout-body { flex: 1; min-width: 0; }
.nb-callout-body .nb-p { margin: 0; }

/* ── Code ──────────────────────────────────────────────── */
.nb-code-wrap { position: relative; margin: 1rem 0; }
.nb-code-lang {
  position: absolute;
  top: .4rem;
  left: .75rem;
  font-size: .7rem;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: .05em;
  pointer-events: none;
}
.nb-code-copy {
  position: absolute;
  top: .4rem;
  right: .5rem;
  padding: .15rem .5rem;
  font-size: .7rem;
  border: 1px solid var(--border, rgba(255,255,255,.12));
  border-radius: 4px;
  background: transparent;
  color: var(--muted);
  cursor: pointer;
  opacity: 0;
  transition: opacity .2s;
}
.nb-code-wrap:hover .nb-code-copy { opacity: 1; }
.nb-code-wrap:hover .nb-code-copy:hover { color: var(--text); }
pre.nb-code {
  background: var(--bg-2, #111);
  border: 1px solid var(--border, rgba(255,255,255,.08));
  border-radius: var(--radius, 6px);
  padding: 2.2rem .9rem .9rem;
  overflow-x: auto;
  margin: 0;
  font-size: .875rem;
  line-height: 1.6;
}
pre.nb-code code { font-family: 'JetBrains Mono', 'Fira Code', ui-monospace, monospace; }

/* ── Image ─────────────────────────────────────────────── */
figure.nb-image { margin: 1rem 0; }
figure.nb-image img { max-width: 100%; border-radius: var(--radius, 6px); display: block; }
figure.nb-image figcaption { font-size: .8rem; color: var(--muted); margin-top: .4rem; text-align: center; }

/* ── Video ─────────────────────────────────────────────── */
.nb-video-wrap { position: relative; padding-top: 56.25%; margin: 1rem 0; border-radius: var(--radius, 6px); overflow: hidden; background: #000; }
.nb-video-wrap iframe,
.nb-video-wrap video { position: absolute; inset: 0; width: 100%; height: 100%; border: none; }

/* ── Divider ───────────────────────────────────────────── */
hr.nb-divider { border: none; border-top: 1px solid var(--border, rgba(255,255,255,.1)); margin: 1.5rem 0; }

/* ── Table ─────────────────────────────────────────────── */
.nb-table-wrap { overflow-x: auto; margin: 1rem 0; }
table.nb-table { width: 100%; border-collapse: collapse; font-size: .9rem; }
table.nb-table th, table.nb-table td { border: 1px solid var(--border, rgba(255,255,255,.1)); padding: .5rem .75rem; text-align: left; }
table.nb-table thead th { background: var(--bg-2, rgba(255,255,255,.04)); font-weight: 600; }

/* ── Inline color annotations ──────────────────────────── */
.nb-color-gray         { color: var(--muted); }
.nb-color-brown        { color: #92400e; }
.nb-color-orange       { color: #f97316; }
.nb-color-yellow       { color: #eab308; }
.nb-color-green        { color: #22c55e; }
.nb-color-blue         { color: var(--key); }
.nb-color-purple       { color: #a855f7; }
.nb-color-pink         { color: #ec4899; }
.nb-color-red          { color: #ef4444; }
.nb-color-gray_background         { background: rgba(161,161,170,.15); padding: .1em .3em; border-radius: .25em; }
.nb-color-brown_background        { background: rgba(146,64,14,.15); padding: .1em .3em; border-radius: .25em; }
.nb-color-orange_background       { background: rgba(249,115,22,.15); padding: .1em .3em; border-radius: .25em; }
.nb-color-yellow_background       { background: rgba(234,179,8,.15); padding: .1em .3em; border-radius: .25em; }
.nb-color-green_background        { background: rgba(34,197,94,.15); padding: .1em .3em; border-radius: .25em; }
.nb-color-blue_background         { background: rgba(0,191,165,.15); padding: .1em .3em; border-radius: .25em; }
.nb-color-purple_background       { background: rgba(168,85,247,.15); padding: .1em .3em; border-radius: .25em; }
.nb-color-pink_background         { background: rgba(236,72,153,.15); padding: .1em .3em; border-radius: .25em; }
.nb-color-red_background          { background: rgba(239,68,68,.15); padding: .1em .3em; border-radius: .25em; }

/* ── Children container ────────────────────────────────── */
.nb-children { padding-left: 1.25rem; }
```

- [ ] **Step 2: Verify the file exists**

```bash
wc -l course-site/assets/notion-blocks.css
```

Expected: ~120+ lines

- [ ] **Step 3: Commit**

```bash
git add course-site/assets/notion-blocks.css
git commit -m "feat(notion-renderer): notion-blocks.css 블록 스타일"
```

---

## Task 2: Create `notion-renderer.js` — scaffold + `renderRichText()`

**Files:**
- Create: `course-site/assets/notion-renderer.js`

- [ ] **Step 1: Create the module scaffold with `renderRichText`**

Create `course-site/assets/notion-renderer.js`:

```js
(function () {
  'use strict';

  // ---------------------------------------------------------------------------
  // Rich text → inline HTML
  // ---------------------------------------------------------------------------
  function renderRichText(richText) {
    if (!Array.isArray(richText) || richText.length === 0) return '';
    return richText.map(function (span) {
      var content = span.plain_text || '';
      if (!content) return '';
      // Escape HTML entities
      content = content
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
      var ann = span.annotations || {};
      // Apply href wrapping first (outermost)
      var href = (span.href) || (span.text && span.text.link && span.text.link.url) || '';
      if (ann.code) content = '<code>' + content + '</code>';
      if (ann.bold) content = '<strong>' + content + '</strong>';
      if (ann.italic) content = '<em>' + content + '</em>';
      if (ann.strikethrough) content = '<s>' + content + '</s>';
      if (ann.underline) content = '<span style="text-decoration:underline">' + content + '</span>';
      if (ann.color && ann.color !== 'default') {
        content = '<span class="nb-color-' + ann.color + '">' + content + '</span>';
      }
      if (href) content = '<a href="' + href + '" target="_blank" rel="noopener">' + content + '</a>';
      return content;
    }).join('');
  }

  // ---------------------------------------------------------------------------
  // Placeholder for remaining functions (filled in subsequent tasks)
  // ---------------------------------------------------------------------------

  function renderNotionPage(notionData, weekMeta) {
    // Stub — will be completed in Task 8
    console.warn('renderNotionPage: stub');
  }

  window.renderNotionPage = renderNotionPage;
  window._nbRenderRichText = renderRichText; // exposed for manual testing
}());
```

- [ ] **Step 2: Verify rich text in browser console**

Open `week.html?week=9` in a browser with a local server running from `course-site/` (or repo root). In the console:

```js
window._nbRenderRichText([
  { plain_text: 'Hello ', annotations: { bold: true, italic: false, code: false, strikethrough: false, underline: false, color: 'default' }, href: null, text: { content: 'Hello ', link: null } },
  { plain_text: 'world', annotations: { bold: false, italic: true, code: false, strikethrough: false, underline: false, color: 'blue' }, href: null, text: { content: 'world', link: null } }
])
// Expected: '<strong>Hello </strong><em><span class="nb-color-blue">world</span></em>'
```

- [ ] **Step 3: Commit**

```bash
git add course-site/assets/notion-renderer.js
git commit -m "feat(notion-renderer): 모듈 scaffold + renderRichText"
```

---

## Task 3: Add heading, paragraph, divider, quote renderers

**Files:**
- Modify: `course-site/assets/notion-renderer.js`

Replace the comment `// Placeholder for remaining functions` block and the `renderNotionPage` stub with the code below. Keep the IIFE wrapper and `renderRichText` untouched.

- [ ] **Step 1: Add the four renderers inside the IIFE, before `renderNotionPage`**

```js
  // ---------------------------------------------------------------------------
  // Block renderers — simple
  // ---------------------------------------------------------------------------

  function renderHeading(block, level) {
    var tag = 'h' + level;
    var cls = 'nb-h' + level;
    var key = 'heading_' + level;
    var rt = (block[key] && block[key].rich_text) || [];
    return '<' + tag + ' class="' + cls + '">' + renderRichText(rt) + '</' + tag + '>';
  }

  function renderParagraph(block) {
    var rt = (block.paragraph && block.paragraph.rich_text) || [];
    var inner = renderRichText(rt);
    if (!inner.trim()) return '<span class="nb-spacer"></span>';
    var html = '<p class="nb-p">' + inner + '</p>';
    // Render children (indented text under paragraph)
    if (block.children && block.children.length) {
      html += '<div class="nb-children">' + renderBlockList(block.children) + '</div>';
    }
    return html;
  }

  function renderDivider() {
    return '<hr class="nb-divider">';
  }

  function renderQuote(block) {
    var rt = (block.quote && block.quote.rich_text) || [];
    return '<blockquote class="nb-quote">' + renderRichText(rt) + '</blockquote>';
  }
```

- [ ] **Step 2: Add `renderBlockList` stub (needed by `renderParagraph`)**

```js
  // Forward declaration — full implementation in Task 7
  function renderBlockList(blocks) {
    return blocks.map(function (b) { return renderBlock(b); }).join('');
  }

  // Forward declaration — full implementation in Task 7
  function renderBlock(block) {
    return '<!-- notion-block: ' + (block.type || 'unknown') + ' -->';
  }
```

- [ ] **Step 3: Update the `renderNotionPage` stub (keep it, just ensure it still exists)**

The `renderNotionPage` stub from Task 2 remains unchanged for now.

- [ ] **Step 4: Commit**

```bash
git add course-site/assets/notion-renderer.js
git commit -m "feat(notion-renderer): heading/paragraph/divider/quote 렌더러"
```

---

## Task 4: Add list renderers + `groupLists()`

**Files:**
- Modify: `course-site/assets/notion-renderer.js`

Add the following functions inside the IIFE, after `renderQuote` and before the `renderBlockList` stub.

- [ ] **Step 1: Add list item renderers**

```js
  // ---------------------------------------------------------------------------
  // Block renderers — lists
  // ---------------------------------------------------------------------------

  function renderBulletedListItem(block) {
    var rt = (block.bulleted_list_item && block.bulleted_list_item.rich_text) || [];
    var inner = renderRichText(rt);
    if (block.children && block.children.length) {
      inner += '<div class="nb-children">' + renderBlockList(block.children) + '</div>';
    }
    return '<li>' + inner + '</li>';
  }

  function renderNumberedListItem(block) {
    var rt = (block.numbered_list_item && block.numbered_list_item.rich_text) || [];
    var inner = renderRichText(rt);
    if (block.children && block.children.length) {
      inner += '<div class="nb-children">' + renderBlockList(block.children) + '</div>';
    }
    return '<li>' + inner + '</li>';
  }

  // Groups consecutive list items into <ul>/<ol> wrappers.
  // Input:  flat array of Notion block objects (may be mixed types)
  // Output: array where consecutive list blocks are replaced by a single
  //         { _grouped: true, tag: 'ul'|'ol', items: [block, ...] } object
  function groupLists(blocks) {
    var result = [];
    var i = 0;
    while (i < blocks.length) {
      var b = blocks[i];
      if (b.type === 'bulleted_list_item' || b.type === 'numbered_list_item') {
        var tag = b.type === 'bulleted_list_item' ? 'ul' : 'ol';
        var group = { _grouped: true, tag: tag, items: [] };
        while (i < blocks.length && blocks[i].type === b.type) {
          group.items.push(blocks[i]);
          i++;
        }
        result.push(group);
      } else {
        result.push(b);
        i++;
      }
    }
    return result;
  }
```

- [ ] **Step 2: Commit**

```bash
git add course-site/assets/notion-renderer.js
git commit -m "feat(notion-renderer): 리스트 렌더러 + groupLists"
```

---

## Task 5: Add toggle, callout, to_do renderers

**Files:**
- Modify: `course-site/assets/notion-renderer.js`

Add inside the IIFE, after the list renderers from Task 4.

- [ ] **Step 1: Add the three renderers**

```js
  // ---------------------------------------------------------------------------
  // Block renderers — toggle, callout, to_do
  // ---------------------------------------------------------------------------

  function renderToggle(block) {
    var rt = (block.toggle && block.toggle.rich_text) || [];
    var summary = '<summary>' + renderRichText(rt) + '</summary>';
    var body = '';
    if (block.children && block.children.length) {
      body = '<div class="nb-toggle-body">' + renderBlockList(block.children) + '</div>';
    }
    return '<details class="nb-toggle">' + summary + body + '</details>';
  }

  function renderCallout(block) {
    var data = block.callout || {};
    var rt = data.rich_text || [];
    var icon = '';
    if (data.icon) {
      if (data.icon.type === 'emoji') icon = data.icon.emoji || '';
      else if (data.icon.type === 'external') icon = '<img src="' + (data.icon.external && data.icon.external.url || '') + '" style="width:1.2em;height:1.2em;vertical-align:middle">';
    }
    var color = (data.color && data.color !== 'default') ? data.color.replace('_background', '') : '';
    var colorClass = color ? ' nb-callout--' + color : '';
    var bodyHtml = '<p class="nb-p">' + renderRichText(rt) + '</p>';
    if (block.children && block.children.length) {
      bodyHtml += renderBlockList(block.children);
    }
    return '<div class="nb-callout' + colorClass + '">' +
      (icon ? '<span class="nb-callout-icon">' + icon + '</span>' : '') +
      '<div class="nb-callout-body">' + bodyHtml + '</div>' +
      '</div>';
  }

  function renderTodo(block) {
    var data = block.to_do || {};
    var rt = data.rich_text || [];
    var checked = Boolean(data.checked);
    return '<label class="nb-todo' + (checked ? ' nb-todo--checked' : '') + '">' +
      '<input type="checkbox" disabled' + (checked ? ' checked' : '') + '>' +
      '<span class="nb-todo-text">' + renderRichText(rt) + '</span>' +
      '</label>';
  }
```

- [ ] **Step 2: Commit**

```bash
git add course-site/assets/notion-renderer.js
git commit -m "feat(notion-renderer): toggle/callout/to_do 렌더러"
```

---

## Task 6: Add code, image, video, table renderers

**Files:**
- Modify: `course-site/assets/notion-renderer.js`

Add inside the IIFE, after the to_do renderer.

- [ ] **Step 1: Add the four renderers**

```js
  // ---------------------------------------------------------------------------
  // Block renderers — code, image, video, table
  // ---------------------------------------------------------------------------

  function renderCode(block) {
    var data = block.code || {};
    var rt = data.rich_text || [];
    var lang = data.language || '';
    var code = rt.map(function (s) { return s.plain_text || ''; }).join('');
    // Escape for HTML display
    var escaped = code
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
    var langClass = lang ? ' class="language-' + lang + '"' : '';
    var langLabel = lang ? '<span class="nb-code-lang">' + lang + '</span>' : '';
    var copyBtn = '<button class="nb-code-copy" type="button" onclick="(function(btn){var pre=btn.closest(\'.nb-code-wrap\').querySelector(\'code\');navigator.clipboard&&navigator.clipboard.writeText(pre.textContent).then(function(){btn.textContent=\'✓\';setTimeout(function(){btn.textContent=\'복사\'},1500)})})(this)">복사</button>';
    return '<div class="nb-code-wrap">' + langLabel + copyBtn +
      '<pre class="nb-code"><code' + langClass + '>' + escaped + '</code></pre></div>';
  }

  function renderImage(block) {
    var data = block.image || {};
    var src = block.local_url || '';
    if (!src) {
      if (data.type === 'file' && data.file) src = data.file.url || '';
      else if (data.type === 'external' && data.external) src = data.external.url || '';
    }
    if (!src) return '<!-- notion-block: image (no src) -->';
    var caption = (data.caption || []).map(function (s) { return s.plain_text || ''; }).join('');
    return '<figure class="nb-image"><img src="' + src + '" alt="' + (caption || 'image') + '" loading="lazy">' +
      (caption ? '<figcaption>' + caption + '</figcaption>' : '') + '</figure>';
  }

  function renderVideo(block) {
    var data = block.video || {};
    var src = '';
    if (data.type === 'external' && data.external) src = data.external.url || '';
    else if (data.type === 'file' && data.file) src = data.file.url || '';
    if (!src) return '<!-- notion-block: video (no src) -->';
    var ytMatch = src.match(/(?:youtu\.be\/|youtube\.com\/(?:watch\?v=|embed\/))([A-Za-z0-9_-]{11})/);
    if (ytMatch) {
      return '<div class="nb-video-wrap"><iframe src="https://www.youtube.com/embed/' + ytMatch[1] + '" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen title="video"></iframe></div>';
    }
    return '<div class="nb-video-wrap"><video controls preload="metadata"><source src="' + src + '"></video></div>';
  }

  function renderTable(block) {
    var hasHeader = block.table && block.table.has_column_header;
    var rows = (block.children || []).filter(function (b) { return b.type === 'table_row'; });
    var html = '<div class="nb-table-wrap"><table class="nb-table">';
    rows.forEach(function (row, idx) {
      var cells = (row.table_row && row.table_row.cells) || [];
      var isHeader = hasHeader && idx === 0;
      var tag = isHeader ? 'th' : 'td';
      html += '<tr>';
      cells.forEach(function (cellRt) {
        html += '<' + tag + '>' + renderRichText(cellRt) + '</' + tag + '>';
      });
      html += '</tr>';
    });
    if (hasHeader && rows.length > 0) {
      // Wrap first row in thead — rebuild
      html = '<div class="nb-table-wrap"><table class="nb-table"><thead>';
      var headerRow = rows[0];
      var headerCells = (headerRow.table_row && headerRow.table_row.cells) || [];
      html += '<tr>' + headerCells.map(function (c) { return '<th>' + renderRichText(c) + '</th>'; }).join('') + '</tr></thead><tbody>';
      rows.slice(1).forEach(function (row) {
        var cells = (row.table_row && row.table_row.cells) || [];
        html += '<tr>' + cells.map(function (c) { return '<td>' + renderRichText(c) + '</td>'; }).join('') + '</tr>';
      });
      html += '</tbody>';
    }
    html += '</table></div>';
    return html;
  }

  function renderLinkToPage(block) {
    var data = block.link_to_page || {};
    var label = data.page_id ? '→ 페이지 링크' : '→ 데이터베이스 링크';
    return '<p class="nb-p"><a class="nb-link-page" href="#">' + label + '</a></p>';
  }
```

- [ ] **Step 2: Commit**

```bash
git add course-site/assets/notion-renderer.js
git commit -m "feat(notion-renderer): code/image/video/table 렌더러"
```

---

## Task 7: Implement `renderBlock()`, `renderBlockList()`, and `renderBlocks()`

**Files:**
- Modify: `course-site/assets/notion-renderer.js`

Replace the two stub functions (`renderBlockList` and `renderBlock`) added in Task 3 with the full implementations below.

- [ ] **Step 1: Replace stubs with full implementations**

Find and replace this block in the file:

```js
  // Forward declaration — full implementation in Task 7
  function renderBlockList(blocks) {
    return blocks.map(function (b) { return renderBlock(b); }).join('');
  }

  // Forward declaration — full implementation in Task 7
  function renderBlock(block) {
    return '<!-- notion-block: ' + (block.type || 'unknown') + ' -->';
  }
```

Replace with:

```js
  // ---------------------------------------------------------------------------
  // Core dispatcher
  // ---------------------------------------------------------------------------

  function renderBlock(block) {
    var type = block.type;
    switch (type) {
      case 'heading_1':  return renderHeading(block, 1);
      case 'heading_2':  return renderHeading(block, 2);
      case 'heading_3':  return renderHeading(block, 3);
      case 'paragraph':  return renderParagraph(block);
      case 'bulleted_list_item': return renderBulletedListItem(block);
      case 'numbered_list_item': return renderNumberedListItem(block);
      case 'toggle':     return renderToggle(block);
      case 'callout':    return renderCallout(block);
      case 'to_do':      return renderTodo(block);
      case 'code':       return renderCode(block);
      case 'image':      return renderImage(block);
      case 'video':      return renderVideo(block);
      case 'table':      return renderTable(block);
      case 'table_row':  return ''; // rendered by renderTable
      case 'quote':      return renderQuote(block);
      case 'divider':    return renderDivider();
      case 'link_to_page': return renderLinkToPage(block);
      default:
        return '<!-- notion-block: ' + type + ' -->';
    }
  }

  // Renders a flat array of blocks, grouping consecutive list items.
  function renderBlockList(blocks) {
    var grouped = groupLists(blocks);
    return grouped.map(function (item) {
      if (item._grouped) {
        var cls = item.tag === 'ul' ? 'nb-ul' : 'nb-ol';
        return '<' + item.tag + ' class="' + cls + '">' +
          item.items.map(function (b) { return renderBlock(b); }).join('') +
          '</' + item.tag + '>';
      }
      return renderBlock(item);
    }).join('');
  }

  // Renders blocks into a DOM container element.
  function renderBlocks(blocks, container) {
    container.innerHTML = renderBlockList(blocks);
  }
```

- [ ] **Step 2: Commit**

```bash
git add course-site/assets/notion-renderer.js
git commit -m "feat(notion-renderer): renderBlock/renderBlockList/renderBlocks 구현"
```

---

## Task 8: Implement `renderNotionPage()`

**Files:**
- Modify: `course-site/assets/notion-renderer.js`

Replace the `renderNotionPage` stub with the full implementation.

- [ ] **Step 1: Replace stub**

Find this stub:

```js
  function renderNotionPage(notionData, weekMeta) {
    // Stub — will be completed in Task 8
    console.warn('renderNotionPage: stub');
  }
```

Replace with:

```js
  // ---------------------------------------------------------------------------
  // Page entry point
  // ---------------------------------------------------------------------------

  // Renders the full Notion block page into #pageContent.
  // notionData: { week, page_id, blocks[] }
  // weekMeta:   raw curriculum.js week object (for title, sidebar data, nav links)
  function renderNotionPage(notionData, weekMeta) {
    var w = weekMeta;
    var blocks = notionData.blocks || [];

    // Page title
    document.title = 'Week ' + w.week + ' — ' + w.title + ' | Blender Archive';
    var brandBadge = document.getElementById('brandBadge');
    var brandTitle = document.getElementById('brandTitle');
    if (brandBadge) brandBadge.textContent = String(w.week).padStart(2, '0');
    if (brandTitle) brandTitle.textContent = 'Week ' + String(w.week).padStart(2, '0');

    // Hero section (reuse existing buildPage hero pattern)
    var heroHtml = '<section class="hero" id="hero-section">' +
      '<div class="hero-card rpd-panel rpd-panel--soft">' +
      '<div class="hero-header">' +
      '<span class="hero-week-well rpd-icon-well">' + String(w.week).padStart(2, '0') + '</span>' +
      '<div class="hero-copy">' +
      '<span class="hero-kicker">Week ' + String(w.week).padStart(2, '0') + '</span>' +
      '<h1>Week ' + String(w.week).padStart(2, '0') + ' · ' + (w.title || '') + '</h1>' +
      (w.subtitle ? '<p>' + w.subtitle + '</p>' : '') +
      '</div></div></div></section>';

    // Main content: Notion blocks
    var contentHtml = '<section class="content-block" id="notion-body">' +
      renderBlockList(blocks) +
      '</section>';

    // Sidebar (references) — uses buildSidebar() defined in week.html
    var refHtml = (typeof buildSidebar === 'function') ? buildSidebar(w) : '';

    // Prev/next navigation
    var CURRICULUM = window.CURRICULUM || [];
    var prev = CURRICULUM.find(function (item) { return item.week === w.week - 1; });
    var next = CURRICULUM.find(function (item) { return item.week === w.week + 1; });
    var prevLink = prev
      ? '<a href="week.html?week=' + prev.week + '">← Week ' + prev.week + '</a>'
      : '<a href="inha.html?panel=weeks">홈으로</a>';
    var nextLink = next
      ? '<a href="week.html?week=' + next.week + '">Week ' + next.week + ' →</a>'
      : '<span style="opacity:.4">마지막 주차</span>';
    var navHtml = '<section class="content-block"><div class="week-nav">' +
      prevLink +
      '<a href="inha.html?panel=weeks" style="color:var(--muted)">전체 목록</a>' +
      nextLink +
      '</div></section>';

    var pageContent = document.getElementById('pageContent');
    if (pageContent) {
      pageContent.innerHTML = heroHtml + contentHtml + refHtml + navHtml + '<div style="height:28px"></div>';
    }
  }
```

Also remove the `window._nbRenderRichText = renderRichText;` line added in Task 2 (it was only for testing). The final line should be:

```js
  window.renderNotionPage = renderNotionPage;
```

- [ ] **Step 2: Commit**

```bash
git add course-site/assets/notion-renderer.js
git commit -m "feat(notion-renderer): renderNotionPage 구현 완료"
```

---

## Task 9: Modify `week.html` — extract `buildSidebar()` + fetch-first init

**Files:**
- Modify: `course-site/week.html`

This task has three sub-steps: add CSS/JS links, extract `buildSidebar`, and switch to fetch-first init.

- [ ] **Step 1: Add `<link>` and `<script>` tags**

In `week.html`, find the existing CSS links block in `<head>`. Add after the last `<link rel="stylesheet">` tag:

```html
    <link rel="stylesheet" href="assets/notion-blocks.css">
```

Near the bottom of `<body>`, find the existing script tags that load `data/curriculum.js`. Add **after** that script tag:

```html
    <script src="assets/notion-renderer.js"></script>
```

- [ ] **Step 2: Extract `buildSidebar(w)` from `buildPage(w)`**

Read `week.html` lines 825–899. This block builds `refSubsections`, `refMetaParts`, and `refHtml`. Extract it as a standalone function.

In `week.html`, find the line (approx. line 825):

```js
      var practiceVideos = videos.filter(function(video) {
```

This line is inside `buildPage(w)`. The extraction creates a new function `buildSidebar(w)` placed **before** `buildPage(w)` (i.e., before line 612). Add the following new function at approximately line 611 (just before `function buildPage(w) {`):

```js
    // Builds and returns the reference sidebar HTML string from curriculum.js data.
    // Used by both buildPage() and renderNotionPage().
    function buildSidebar(w) {
      var text = getWeekText();
      var isKo = window.RPDI18n.getLanguage() === "ko";
      var videos = Array.isArray(w.videos) ? w.videos : [];
      var docs = Array.isArray(w.docs) ? w.docs : [];
      var shortcuts = Array.isArray(w.shortcuts) ? w.shortcuts : [];
      var explore = Array.isArray(w.explore) ? w.explore : [];
      var mistakes = Array.isArray(w.mistakes) ? w.mistakes : [];
      var referenceSummaryTitle = isKo ? "이번 주 참고자료" : "Week resources";
      var practiceVideoTitle = isKo ? "실습 영상" : "Practice videos";
      function renderReferenceLink(label, url, desc) {
        return '<a class="doc-link" href="' + url + '" target="_blank" rel="noopener noreferrer">' +
          '<span class="doc-link-main">' + label + ' ↗</span>' +
          (desc ? '<span class="doc-link-desc">' + desc + '</span>' : '') +
          '</a>';
      }
      function stripPracticePrefix(title) {
        return String(title || "").replace(/^\[실습\]\s*/, "");
      }
      var practiceVideos = videos.filter(function(video) {
        return /^\[실습\]/.test(String(video.title || ""));
      });
      var officialVideos = videos.filter(function(video) {
        return !/^\[실습\]/.test(String(video.title || ""));
      });
      var refSubsections = [
        practiceVideos.length ? '<div class="ref-group"><h4 class="ref-group-title">📹 ' + practiceVideoTitle + '</h4><div class="ref-video-list">' +
          practiceVideos.map(function(video) {
            return '<a class="ref-video-item" href="' + video.url + '" target="_blank" rel="noopener noreferrer">' +
              '<span class="ref-video-title">' + stripPracticePrefix(video.title) + '</span>' +
              (video.description ? '<span class="ref-video-desc">' + video.description + '</span>' : '') + '</a>';
          }).join("") + '</div></div>' : "",
        officialVideos.length ? '<div class="ref-group"><h4 class="ref-group-title">📚 ' + text.sectionVideos + '</h4><div class="doc-links-row">' +
          officialVideos.map(function(video) { return renderReferenceLink("▶ " + video.title, video.url, video.description || ""); }).join("") +
          '</div></div>' : "",
        docs.length ? '<div class="ref-group"><h4 class="ref-group-title">📄 ' + text.sectionDocs + '</h4><div class="doc-links-row">' +
          docs.map(function(doc) { return renderReferenceLink("📄 " + doc.title, doc.url, doc.description || ""); }).join("") +
          '</div></div>' : "",
        shortcuts.length ? '<div class="ref-group"><h4 class="ref-group-title">⌨ ' + text.sectionShortcuts + '</h4><div class="shortcuts-compact">' +
          shortcuts.map(function(shortcut) {
            return '<div class="sc-row"><kbd class="sc-key">' + shortcut.keys + '</kbd><span class="sc-action">' + shortcut.action + '</span></div>';
          }).join("") + '</div></div>' : "",
        explore.length ? '<div class="ref-group"><h4 class="ref-group-title">💡 ' + text.sectionExplore + '</h4><ul class="ref-list">' +
          explore.map(function(item) {
            return '<li><strong>' + item.title + '</strong>' + (item.hint ? ' — <span class="ref-hint">' + item.hint + '</span>' : '') + '</li>';
          }).join("") + '</ul></div>' : "",
        mistakes.length ? '<div class="ref-group"><h4 class="ref-group-title">⚠ ' + text.sectionMistakes + '</h4><ul class="ref-list">' +
          mistakes.map(function(mistake) { return '<li>' + mistake + '</li>'; }).join("") + '</ul></div>' : ""
      ].filter(Boolean).join("");
      var refMetaParts = [
        practiceVideos.length ? practiceVideoTitle + " " + practiceVideos.length : "",
        officialVideos.length ? text.sectionVideos + " " + officialVideos.length : "",
        docs.length ? text.sectionDocs + " " + docs.length : "",
        shortcuts.length ? text.sectionShortcuts + " " + shortcuts.length : ""
      ].filter(Boolean).join(" · ");
      var hasRef = refSubsections.length > 0;
      currentWeekHasReference = hasRef;
      if (!hasRef) return "";
      return '<section class="content-block" id="section-reference">' +
        '<details class="card ref-accordion"><summary class="ref-summary">' +
        '<span class="ref-summary-title">' + referenceSummaryTitle + '</span>' +
        '<span class="ref-summary-meta">' + refMetaParts + '</span></summary>' +
        '<div class="ref-body">' + refSubsections + '</div></details></section>';
    }
```

- [ ] **Step 3: Remove the duplicated sidebar code from `buildPage()`**

In `buildPage(w)`, find and **remove** the lines from `var practiceVideos = ...` to `var refHtml = hasRef ? ...` (approximately lines 825–899). Replace that entire block with a single call:

```js
      var refHtml = buildSidebar(w);
```

Also remove the now-redundant inline `renderReferenceLink` and `stripPracticePrefix` helper functions from inside `buildPage()` — they are now defined inside `buildSidebar()`.

- [ ] **Step 4: Add fetch-first init to `renderWeekPage()`**

Find `renderWeekPage()` at approximately line 591:

```js
    function renderWeekPage() {
      applyWeekChrome();
      if (!weekData) {
        renderMissingWeek();
        return;
      }
      buildPage(window.RPDI18n.localizeWeekData(weekData));
      renderShowMeBrowser();
      updateShowMeBadges();
      maybeOpenRequestedShowMe();
    }
```

Replace with:

```js
    function renderWeekPage() {
      applyWeekChrome();
      if (!weekData) {
        renderMissingWeek();
        return;
      }
      var jsonPath = "data/notion-blocks/week" + String(weekNum).padStart(2, "0") + ".json";
      fetch(jsonPath)
        .then(function(r) { return r.ok ? r.json() : Promise.reject(new Error("not found")); })
        .then(function(data) {
          if (!data.blocks || !data.blocks.length) throw new Error("empty blocks");
          window.renderNotionPage(data, weekData);
          renderShowMeBrowser();
          updateShowMeBadges();
          maybeOpenRequestedShowMe();
        })
        .catch(function() {
          buildPage(window.RPDI18n.localizeWeekData(weekData));
          renderShowMeBrowser();
          updateShowMeBadges();
          maybeOpenRequestedShowMe();
        });
    }
```

- [ ] **Step 5: Commit**

```bash
git add course-site/week.html
git commit -m "feat(week.html): buildSidebar 분리 + fetch-first Notion 렌더 init"
```

---

## Task 10: Integration test + bug fixes

**Files:**
- Read: `course-site/data/notion-blocks/week09.json` (reference)
- Modify: any file with bugs found

- [ ] **Step 1: Start a local server**

```bash
cd course-site && python3 -m http.server 8080
```

Or from repo root:

```bash
python3 -m http.server 8080 --directory course-site
```

- [ ] **Step 2: Open week 9 and verify Notion blocks render**

Open `http://localhost:8080/week.html?week=9`

Check in browser:
- No JS errors in console
- Page title shows "Week 09 — Lighting 기초..."
- Headings (h1/h2/h3) render with proper sizing
- Paragraphs have line-height spacing
- Callout blocks show colored left border + icon
- Toggle blocks open/close on click
- Code blocks have copy button (visible on hover)
- Images load (local paths from `assets/notion-images/week09/`)
- Numbered/bulleted lists group correctly (no nested `<ul>` inside `<ul>`)
- Reference sidebar (videos, shortcuts) appears from curriculum.js

- [ ] **Step 3: Test fallback — week 1 should use curriculum.js renderer**

Open `http://localhost:8080/week.html?week=1`

Expected: renders normally using existing `buildPage()` with no JS errors.

- [ ] **Step 4: Test dark/light toggle**

Toggle theme on week 9 — all `.nb-*` colors should update via CSS variable inheritance.

- [ ] **Step 5: Fix any bugs found**

Common things to check if broken:
- `renderNotionPage is not a function` → `notion-renderer.js` script tag not loading; check `<script>` placement
- Images show 404 → verify `local_url` in week09.json starts with `assets/notion-images/...` (not absolute path)
- Copy button onclick error → quotes conflict; verify the onclick string uses mixed `'` and `"`
- Sidebar not rendering → `buildSidebar` is not in scope from `notion-renderer.js`; confirm it's defined in `week.html` and the `renderNotionPage` call is inside the same script scope

- [ ] **Step 6: Commit any fixes**

```bash
git add -u
git commit -m "fix(notion-renderer): 통합 테스트 버그 수정"
```

---

## Task 11: Push + PR

- [ ] **Step 1: Push the branch**

```bash
git push
```

- [ ] **Step 2: Verify PR #68 is updated (same branch)**

```bash
gh pr view 68 --web
```

The commits from this implementation are added to the existing PR `claude/elated-sanderson-b8a2b8` which created PR #68.

---

## Self-Review Checklist

- [x] **Spec Section 2 (Architecture):** fetch-first init in Task 9, `renderNotionPage()` in Task 8, `buildSidebar()` extraction in Task 9
- [x] **Spec Section 4 (Block types):** all 14 block types covered across Tasks 3–7
- [x] **Spec Section 4.2 (Rich text):** `renderRichText()` in Task 2 handles all 6 annotation types + href
- [x] **Spec Section 5 (CSS):** Task 1 covers all `.nb-*` classes including callout colors, code, toggle, table
- [x] **Spec Section 6 (Sidebar):** `buildSidebar()` extracted in Task 9, called from both paths
- [x] **Spec Section 7 (Fallback):** `.catch(() => buildPage())` in Task 9 Step 4; empty blocks check in same
- [x] **Type consistency:** `renderBlockList` and `renderBlock` stubs added in Task 3, replaced in Task 7 — no name drift
- [x] **No placeholders:** all steps have complete code
