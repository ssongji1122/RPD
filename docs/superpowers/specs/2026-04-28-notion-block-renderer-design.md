# Notion Block Renderer — Design Spec

**Date:** 2026-04-28  
**Status:** Approved  
**Branch:** claude/elated-sanderson-b8a2b8  

---

## 1. Background

Notion is the SSoT for RPD course content (decided 2026-04-06). The previous session built the body-mirror infrastructure (PR #68): `notion-sync.py --weeks N` fetches the full Notion block tree and saves it to `course-site/data/notion-blocks/weekN.json`, with Notion-hosted images cached to `course-site/assets/notion-images/weekN/`.

**Step 4 (this spec):** make `week.html` render those blocks as the primary page content, replacing the curriculum.js-driven content area.

---

## 2. Goals

- `week.html` renders Notion blocks (headings, paragraphs, callouts, toggles, code, images, etc.) as the main content when `notion-blocks/weekN.json` is present.
- Sidebar (videos, shortcuts, docs) continues to pull from `curriculum.js` — that data is not in Notion.
- Weeks without a `notion-blocks/weekN.json` fall back silently to the existing `buildPage()` renderer.
- No new dependencies; pure vanilla JS + CSS.

---

## 3. Architecture

### 3.1 New files

| File | Purpose |
|------|---------|
| `course-site/assets/notion-renderer.js` | Block rendering module (~350 lines) |
| `course-site/assets/notion-blocks.css` | Notion block styles (`.nb-*` prefix) |

### 3.2 week.html changes (minimal)

Add two `<script>` / `<link>` tags and change the init flow:

**Before:**
```js
buildPage(weekData);
```

**After:**
```js
fetch(`data/notion-blocks/week${String(weekNum).padStart(2,'0')}.json`)
  .then(r => r.ok ? r.json() : Promise.reject())
  .then(data => {
    if (!data.blocks?.length) throw new Error('empty');
    renderNotionPage(data, weekData);
  })
  .catch(() => buildPage(weekData));
```

### 3.3 Module API (`notion-renderer.js`)

```js
// Public
window.renderNotionPage(notionData, weekMeta)
  // notionData: { week, page_id, blocks[] }
  // weekMeta:   curriculum.js week object (for title, status, sidebar data)

// Internal
renderBlocks(blocks, container)   // entry point for a block list
renderBlock(block)                // dispatches by block.type → returns HTMLElement
renderRichText(rich_text[])       // returns DocumentFragment with inline markup
groupLists(blocks)                // wraps consecutive list items into <ul>/<ol>
```

### 3.4 Data flow

```
URL: week.html?week=9
  │
  ├─ fetch('data/notion-blocks/week09.json')
  │     ├─ 200 OK + blocks present
  │     │    └─ renderNotionPage(data, weekMeta)
  │     │         ├─ renderBlocks(data.blocks, #week-content)
  │     │         └─ buildSidebar(weekMeta)   ← curriculum.js videos/shortcuts/docs
  │     └─ 404 / error / empty blocks
  │          └─ buildPage(weekMeta)           ← existing curriculum.js renderer
  │
  └─ shell, auth, theme, i18n, showme — unchanged
```

---

## 4. Block Type Support

### 4.1 Block dispatch table

| Notion type | HTML output | Notes |
|-------------|-------------|-------|
| `heading_1` | `<h1 class="nb-h1">` | |
| `heading_2` | `<h2 class="nb-h2">` | |
| `heading_3` | `<h3 class="nb-h3">` | |
| `paragraph` | `<p class="nb-p">` | empty rich_text → `<br>` spacer |
| `bulleted_list_item` | `<ul class="nb-ul"><li>` | consecutive items auto-grouped |
| `numbered_list_item` | `<ol class="nb-ol"><li>` | consecutive items auto-grouped |
| `toggle` | `<details class="nb-toggle"><summary>…</summary>` + children | recursive render |
| `callout` | `<div class="nb-callout nb-callout--{color}">` | icon span + rich text |
| `code` | `<pre class="nb-code"><code class="language-{lang}">` | copy button top-right |
| `image` | `<figure class="nb-image"><img><figcaption>` | `local_url` preferred |
| `video` | YouTube → `<iframe>`, other → `<video controls>` | |
| `divider` | `<hr class="nb-divider">` | |
| `table` | `<table class="nb-table">` | first row = `<thead>` if `has_column_header` |
| `table_row` | `<tr><td>` / `<tr><th>` | rendered by table handler |
| `quote` | `<blockquote class="nb-quote">` | |
| `to_do` | `<label class="nb-todo"><input type="checkbox" disabled>` | reflects Notion state |
| `link_to_page` | `<a class="nb-link-page" href="#">` | href TBD (no page map yet) |
| unknown | `<!-- notion-block: {type} -->` | silent skip, no visible output |

### 4.2 Rich text annotations

Each `rich_text` object may have any combination of:

| Annotation | Output |
|------------|--------|
| `bold` | `<strong>` |
| `italic` | `<em>` |
| `code` | `<code>` |
| `strikethrough` | `<s>` |
| `underline` | `<span style="text-decoration:underline">` |
| `color ≠ default` | `<span class="nb-color-{color}">` |
| `href` | `<a href="{url}" target="_blank" rel="noopener">` |

Annotations nest outward (link wraps all others when present).

### 4.3 Notion colors → CSS

Notion supports 13 named colors (default, gray, brown, orange, yellow, green, blue, purple, pink, red + `*_background` variants). CSS maps them to tokens:

```css
.nb-color-blue           { color: var(--key); }
.nb-color-red            { color: var(--c-error, #ef4444); }
.nb-color-gray           { color: var(--muted); }
.nb-color-orange_background { background: rgba(249,115,22,.15); padding: .1em .3em; border-radius: .25em; }
/* … etc */
```

---

## 5. CSS Design

**File:** `course-site/assets/notion-blocks.css`  
**Loaded via:** `<link>` in `week.html` `<head>`  
**Prefix:** `.nb-*` — no collision with existing `.rpd-*`, `.card-*` classes

### Key rules

```
nb-callout     left border 3px + subtle bg tint, icon 1.2em before text
nb-toggle      summary { cursor: pointer; list-style: none }
               summary::before { content: '▶'; transition: transform }
               details[open] summary::before { transform: rotate(90deg) }
nb-code        font: monospace; bg: var(--bg-2); position: relative
               copy button: absolute top-right, opacity 0 → 1 on hover
nb-image       img { max-width: 100%; border-radius: var(--radius) }
nb-table       width: 100%; border-collapse: collapse; th bg: var(--bg-2)
nb-color-*     13 text + 13 background variants mapped to token palette
```

All values use `tokens.css` variables → dark/light mode automatic.

---

## 6. Sidebar (unchanged)

The existing sidebar rendering code **stays in `week.html`** and is refactored into a standalone `buildSidebar(weekMeta)` function (still in week.html, not moved to notion-renderer.js). Both `renderNotionPage()` and the fallback `buildPage()` call it, so sidebar logic lives in exactly one place.

It renders:
- Videos panel (from `weekMeta.videos`)
- Shortcuts panel (from `weekMeta.shortcuts`)
- Docs/references panel (from `weekMeta.docs`)

---

## 7. Fallback Rules

| Condition | Behavior |
|-----------|----------|
| `notion-blocks/weekN.json` absent (404) | Silent fallback to `buildPage()` |
| fetch network error | Silent fallback to `buildPage()` |
| JSON present but `blocks` is empty | Silent fallback to `buildPage()` |
| Unknown block type | Skip block, emit HTML comment `<!-- notion-block: {type} -->` |
| Image `local_url` absent | Use Notion external URL directly |
| Video URL not YouTube | `<video controls src="…">` |

---

## 8. Out of Scope

- **i18n of Notion content** — Notion blocks are Korean-only for now; language toggle will not re-render block content (only sidebar labels)
- **Progress tracking / checkboxes on Notion `to_do` blocks** — rendered read-only; Notion is authoritative
- **Live Notion sync in browser** — content is served from static JSON; no client-side Notion API calls
- **Syntax highlighting** — code blocks render with language class (`language-python` etc.) for future Prism.js integration; no highlighting bundled now
- **`link_to_page` resolution** — rendered as a non-functional link; full page map is deferred

---

## 9. Testing Plan

1. **Unit**: `notion-renderer.js` renders fixture blocks without week.html (node or browser console)
2. **Integration**: open `week.html?week=9` with local server → verify all 273 blocks render without JS errors
3. **Fallback**: rename `week09.json` temporarily → week 9 falls back to `buildPage()` correctly
4. **Other weeks**: open `week.html?week=1` → no regression (no JSON file → fallback)
5. **Dark/light**: toggle theme → `.nb-*` colors update correctly
6. **Toggle blocks**: expand/collapse Notion toggle blocks
7. **Images**: Notion-hosted images load from `/assets/notion-images/week09/`

---

## 10. File Change Summary

| File | Change |
|------|--------|
| `course-site/assets/notion-renderer.js` | **NEW** — block renderer module |
| `course-site/assets/notion-blocks.css` | **NEW** — block styles |
| `course-site/week.html` | **MODIFY** — add `<link>`, `<script>`, change init to fetch-first |
