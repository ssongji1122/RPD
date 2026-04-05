# Navigation Label Unification — Design

**Date:** 2026-04-06
**Scope:** B2 (shared nav-config, no layout/CSS changes)
**Deferred to future spec:** IA redesign (primary/secondary split, mobile menu, 5-item topbar)

## Problem

The course-site has **4 different topbar implementations** scattered across 7 pages, causing:

1. **Label mismatch for the same URL (`index.html`)**
   - `inha.html`, `admin.html`, `week.html` → "Archive"
   - `index.html`, `library.html`, `shortcuts.html`, `studio.html` → "홈"
2. **Semantic drift from recent rename** — commit `26afb05` changed `index.html` title to "Edu Home" but 5 locations still label the link "Archive"
3. **Path style inconsistency** — per commit `9f8720b`, the project standardized on **relative paths** (no leading `/`) for GH Pages sub-path deployment. `inha.html`, `admin.html`, `week.html` still have some absolute paths (`/index.html`) in their hardcoded topbars that need to be normalized to relative

### Root cause

Navigation is generated in 4 places with no single source of truth:

| Page | Pattern | Topbar label |
|------|---------|--------------|
| index, library, shortcuts, studio | `data-shell` + `shell.js` injection | 홈 |
| admin | `<div class="app">` + hardcoded HTML | Archive |
| inha | `<div class="page-shell">` + hardcoded HTML | Archive |
| week | `<header class="topbar">` + hardcoded HTML | Archive |

## Goal

**Single source of truth for topbar navigation labels and hrefs**, without touching layout CSS or page DOM structure.

**Non-goals** (explicitly deferred):
- IA redesign (5-item topbar, primary/secondary split)
- Mobile menu restructure
- Replacing "Blender Archive" content in hero copy across i18n.js
- Layout/CSS changes
- Active state visual improvements
- Unifying the 4 shell patterns into one

## Architecture

```
┌─────────────────────────────────────────────┐
│         assets/nav-config.js                │
│   window.RPDNavConfig.getTopbarItems(lang)  │
│   → [{href, tabTarget, label}, ...]         │
└─────────────────────────────────────────────┘
          ↓                        ↓
  ┌──────────────┐        ┌────────────────┐
  │  shell.js    │        │ topbar-sync.js │
  │  (injects    │        │  (updates      │
  │   new DOM)   │        │   existing     │
  │              │        │   .app-tabs)   │
  └──────────────┘        └────────────────┘
          ↓                        ↓
  data-shell pages           hardcoded pages
  (index, library,           (inha, admin,
   shortcuts, studio)         week)
```

**Two output paths share one input.** Both read from `RPDNavConfig` but render differently based on page pattern:
- `shell.js` builds fresh DOM (unchanged structure, just reads items from config)
- `topbar-sync.js` finds existing `.app-tabs` containers and replaces their anchor children

## Components

### New: `course-site/assets/nav-config.js`

Single source of truth for topbar nav items. Pure data module, no DOM side effects.

**API:**
```js
window.RPDNavConfig.getTopbarItems(lang: 'ko' | 'en'): NavItem[]
```

**NavItem shape:**
```js
{
  href: string,        // relative path (e.g., 'index.html') — matches shell.js convention after commit 9f8720b
  tabTarget: string,   // matches body[data-tab] values ('archive'|'class'|'studio')
  label: string        // localized display text
}
```

**Initial items (3, matching current shell.js output after commit 9f8720b):**
| href | tabTarget | ko | en |
|------|-----------|-----|-----|
| `index.html` | `archive` | 홈 | Home |
| `inha.html` | `class` | Class | Class |
| `studio.html` | `studio` | My Studio | My Studio |

**Path convention rationale:** Relative paths (no leading `/`) required for GitHub Pages sub-path deployment. An absolute `/index.html` would break when the site is hosted at `username.github.io/RPD/` because it would resolve to `username.github.io/index.html`. Relative paths resolve correctly regardless of deployment base path.

**Rationale:** Keep `tabTarget: 'archive'` for backward compatibility with `tab-system.js` and existing CSS selectors (`body[data-tab="archive"]`). Changing tabTarget would cascade into CSS and the rail system.

### New: `course-site/assets/topbar-sync.js`

Replaces anchors inside any `.app-tabs` container with nav items from `RPDNavConfig`. Used by pages that have hardcoded topbars in their HTML.

**Behavior:**
- On `DOMContentLoaded` (or immediately if DOM already loaded)
- If `window.RPDNavConfig` is missing, no-op
- Reads current language from `document.documentElement.getAttribute('data-lang')` (defaults `'ko'`)
- Reads active tab from `document.body.dataset.tab`
- Queries all `.app-tabs` elements on the page, clears their innerHTML, appends fresh anchors
- **MUST set `.is-active` class itself** because it runs AFTER `tab-system.js` has already run, and replacing the anchors discards any `.is-active` classes `tab-system.js` applied

**Idempotent:** safe to load multiple times or re-run.

**No dependencies** beyond `window.RPDNavConfig`.

**Timing rationale:** `tab-system.js` is an IIFE that runs synchronously on script execution; `topbar-sync.js` runs on DOMContentLoaded. So when topbar-sync runs, tab-system has already assigned `.is-active` to the hardcoded anchors. topbar-sync then replaces those anchors entirely, which would leave them without active state unless topbar-sync applies it itself.

### Modified: `course-site/assets/shell.js`

Refactor lines 54-61. Remove inline hardcoded items array, read from `RPDNavConfig` instead.

**Before:** 3 hardcoded `el('a', ...)` calls with inline label logic.
**After:** Iterate `RPDNavConfig.getTopbarItems(lang)`, map to `el('a', ...)` calls.

**Do NOT set `.is-active` here.** The existing behavior delegates active-state assignment to `tab-system.js`, which runs right after `shell.js` in HTML script order and queries `.app-tab[data-tab-target]` to add `.is-active`. Keep this delegation.

Fallback: if `window.RPDNavConfig` is missing, render empty topbar (fail-safe, no crash).

### Modified: HTML files (7 total)

**Pages using `data-shell` (index, library, shortcuts, studio):**
Add `<script src="assets/nav-config.js"></script>` **before** `<script src="assets/shell.js">`.

**Pages with hardcoded topbar (inha, admin, week):**
Add both scripts after existing scripts:
```html
<script src="assets/nav-config.js"></script>
<script src="assets/topbar-sync.js"></script>
```

Hardcoded `<a>Archive</a>` elements inside HTML are **left untouched** — topbar-sync.js replaces them at runtime.

### Modified: `course-site/assets/i18n.js`

Line 309: `listLabel: "Archive"` → `listLabel: "홈"`

This key is used by `week.html` footer "← Archive" button. Matching the topbar label keeps navigation copy consistent.

## Data Flow

### data-shell pages (index, library, shortcuts, studio)
1. Page loads, `nav-config.js` executes → `window.RPDNavConfig` defined
2. `shell.js` IIFE runs → calls `RPDNavConfig.getTopbarItems(lang)`
3. shell.js builds topbar DOM with localized labels
4. Topbar appended to `.app` container

### Hardcoded-topbar pages (inha, admin, week)
1. Page HTML contains `<div class="app-tabs"><a>Archive</a>...</div>` (static)
2. `nav-config.js` loads → `window.RPDNavConfig` defined
3. `topbar-sync.js` waits for DOMContentLoaded
4. Finds `.app-tabs`, clears it, appends new anchors from config
5. User sees "홈" not "Archive"

**Load order guarantee:**
- `nav-config.js` MUST load before `shell.js` (data-shell pages)
- `nav-config.js` MUST load before `topbar-sync.js` (hardcoded pages)
- Both guaranteed by script tag order in HTML

## Error Handling

| Scenario | Behavior |
|----------|----------|
| `nav-config.js` fails to load | `window.RPDNavConfig` undefined → topbar-sync no-ops, shell.js renders empty topbar |
| `body.dataset.tab` missing | Active tab comparison fails silently, no `.is-active` applied |
| `body.dataset.tab` = 'admin' (admin.html) | No tab matches archive/class/studio → no `.is-active`. Intentional: admin is not a primary nav destination, accessed via user profile menu |
| `.app-tabs` element missing on page | `querySelectorAll` returns empty NodeList, forEach is no-op |
| Duplicate `.app-tabs` elements | All get synced (intentional — supports legacy markup) |
| Invalid `lang` attribute | Defaults to `'ko'` (current behavior in shell.js) |

## Testing Strategy

### Manual browser verification (7 pages)
For each of index, library, shortcuts, studio, inha, admin, week:
1. Open page in browser
2. Verify topbar shows exactly 3 tabs: 홈 / Class / My Studio
3. Verify current page's tab has `.is-active` class applied
4. Click each tab, verify navigation works
5. Check browser console for errors

### Playwright regression (existing test)
`tests/pages-load.spec.js` already validates:
- 200 status for all 7 pages
- Page titles match
- No critical JS errors

Run this suite before and after, expect 0 regressions.

### Language switch verification
- Switch to `en` (if UI allows)
- Verify "홈" becomes "Home"
- Switch back to `ko`

## File Change Summary

| File | Action | Estimated size |
|------|--------|---------------|
| `course-site/assets/nav-config.js` | CREATE | ~20 lines |
| `course-site/assets/topbar-sync.js` | CREATE | ~30 lines |
| `course-site/assets/shell.js` | MODIFY (lines 54-61) | ~10 lines diff |
| `course-site/assets/i18n.js` | MODIFY (line 309) | 1 line diff |
| `course-site/index.html` | MODIFY (add script tag) | +1 line |
| `course-site/library.html` | MODIFY (add script tag) | +1 line |
| `course-site/shortcuts.html` | MODIFY (add script tag) | +1 line |
| `course-site/studio.html` | MODIFY (add script tag) | +1 line |
| `course-site/inha.html` | MODIFY (add 2 script tags) | +2 lines |
| `course-site/admin.html` | MODIFY (add 2 script tags) | +2 lines |
| `course-site/week.html` | MODIFY (add 2 script tags) | +2 lines |

**Total:** 2 new files, 9 modified files, ~73 lines changed.

## Independence from Notion SSOT

This refactor does not touch content managed by Notion SSOT:
- Notion sync operates on: `curriculum.json`, `references.json`, `showme` catalogs, week/step/task content
- UI shell (topbar labels, nav config) is NOT sourced from Notion
- Changes here are UI chrome only, independent of content pipeline
- No changes to `tools/notion-sync.py`, `tools/notion_api.py`, or any data files

## Success Criteria

1. All 7 pages display identical topbar: 홈 / Class / My Studio
2. Active tab highlighting works consistently (inha/week show Class active, others match body.dataset.tab, admin shows no tab active by design)
3. No JS console errors introduced
4. Existing `tests/pages-load.spec.js` passes
5. Changing a label requires editing only `nav-config.js` (single source of truth proven)
6. All topbar links use relative paths (no leading `/`), matching the convention from commit `9f8720b`. Pre-existing absolute paths in inha/admin/week hardcoded topbars get normalized when topbar-sync replaces the anchors
