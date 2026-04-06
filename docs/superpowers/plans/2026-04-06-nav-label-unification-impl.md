# Navigation Label Unification — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Unify topbar navigation labels across all 7 course-site pages by introducing a single source of truth (`nav-config.js`) that both the shell.js injection and hardcoded-topbar pages read from.

**Architecture:** Two output paths share one data source. `nav-config.js` exports `window.RPDNavConfig.getTopbarItems(lang)` returning an array of nav items. `shell.js` (data-shell pages) builds fresh DOM from it. New `topbar-sync.js` (hardcoded-topbar pages) replaces anchors inside existing `.app-tabs` containers. No CSS or layout changes.

**Tech Stack:** Vanilla JS (no bundler), Playwright for integration tests, static HTML served via `serve`

**Related Spec:** `docs/superpowers/specs/2026-04-06-nav-label-unification-design.md`

---

## File Structure

**New files:**
- `course-site/assets/nav-config.js` — pure data module exposing `window.RPDNavConfig.getTopbarItems(lang)`. Single responsibility: define topbar nav items.
- `course-site/assets/topbar-sync.js` — runtime DOM sync for pages with hardcoded topbars. Single responsibility: replace anchors inside `.app-tabs` containers with nav-config items.
- `tests/nav-unification.spec.js` — Playwright integration test. Single responsibility: verify every page renders the correct topbar tabs.

**Modified files:**
- `course-site/assets/shell.js` (lines 54-61) — refactor hardcoded tab array to read from `RPDNavConfig`.
- `course-site/assets/i18n.js` (line 309) — update `listLabel: "Archive"` → `"홈"`.
- `course-site/index.html`, `library.html`, `shortcuts.html`, `studio.html` — add `<script src="assets/nav-config.js">` before `shell.js`.
- `course-site/inha.html`, `admin.html`, `week.html` — add `<script src="assets/nav-config.js">` + `<script src="assets/topbar-sync.js">` after existing scripts.

---

## Task 1: Write failing integration test for unified topbar

**Files:**
- Create: `tests/nav-unification.spec.js`

- [ ] **Step 1: Write the failing Playwright test**

Create `tests/nav-unification.spec.js` with the following content:

```js
// @ts-check
const { test, expect } = require('@playwright/test');

const PAGES = [
  { path: '/index.html', activeTab: 'archive' },
  { path: '/library.html', activeTab: 'archive' },
  { path: '/shortcuts.html', activeTab: 'archive' },
  { path: '/studio.html', activeTab: 'studio' },
  { path: '/inha.html', activeTab: 'class' },
  { path: '/week.html?week=3', activeTab: 'class' },
  { path: '/admin.html', activeTab: null }, // no tab matches 'admin'
];

const EXPECTED_TABS = [
  { label: '홈', href: 'index.html', tabTarget: 'archive' },
  { label: 'Class', href: 'inha.html', tabTarget: 'class' },
  { label: 'My Studio', href: 'studio.html', tabTarget: 'studio' },
];

for (const pg of PAGES) {
  test(`${pg.path} has unified topbar with 3 tabs`, async ({ page }) => {
    await page.goto(pg.path);
    await page.waitForLoadState('domcontentloaded');
    // Wait for topbar-sync.js (DOMContentLoaded handler) to run
    await page.waitForTimeout(100);

    const tabs = await page.$$eval('.app-tabs .app-tab', (els) =>
      els.map((el) => ({
        label: (el.textContent || '').trim(),
        href: el.getAttribute('href'),
        tabTarget: el.getAttribute('data-tab-target'),
        isActive: el.classList.contains('is-active'),
      }))
    );

    expect(tabs.length).toBe(3);
    for (let i = 0; i < 3; i++) {
      expect(tabs[i].label).toBe(EXPECTED_TABS[i].label);
      expect(tabs[i].href).toBe(EXPECTED_TABS[i].href);
      expect(tabs[i].tabTarget).toBe(EXPECTED_TABS[i].tabTarget);
    }

    // Verify active tab (skip for admin.html which has no matching tab)
    if (pg.activeTab) {
      const activeTab = tabs.find((t) => t.tabTarget === pg.activeTab);
      expect(activeTab?.isActive).toBe(true);
    }
  });
}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `npx playwright test tests/nav-unification.spec.js --project=desktop`

Expected: FAIL. Reasons:
- `inha.html`, `admin.html`, `week.html`: first tab label is "Archive" not "홈"
- Other pages may pass partially but admin also has relative-path inconsistency

---

## Task 2: Create nav-config.js data module

**Files:**
- Create: `course-site/assets/nav-config.js`

- [ ] **Step 1: Write the nav-config.js module**

Create `course-site/assets/nav-config.js` with the following content:

```js
/* course-site/assets/nav-config.js
   Single source of truth for topbar navigation items.
   Consumed by shell.js (data-shell pages) and topbar-sync.js (hardcoded pages). */
(function (win) {
  'use strict';
  win.RPDNavConfig = {
    /**
     * Returns the topbar nav items for the given language.
     * @param {'ko'|'en'} lang
     * @returns {Array<{href:string, tabTarget:string, label:string}>}
     */
    getTopbarItems: function (lang) {
      var isKo = (lang || 'ko') === 'ko';
      return [
        { href: 'index.html', tabTarget: 'archive', label: isKo ? '홈' : 'Home' },
        { href: 'inha.html', tabTarget: 'class', label: 'Class' },
        { href: 'studio.html', tabTarget: 'studio', label: 'My Studio' }
      ];
    }
  };
})(window);
```

- [ ] **Step 2: Verify syntax is valid JS**

Run: `node -e "const fs=require('fs');eval(fs.readFileSync('course-site/assets/nav-config.js','utf8').replace('window','globalThis'));console.log(JSON.stringify(globalThis.RPDNavConfig.getTopbarItems('ko')))"`

Expected output:
```
[{"href":"index.html","tabTarget":"archive","label":"홈"},{"href":"inha.html","tabTarget":"class","label":"Class"},{"href":"studio.html","tabTarget":"studio","label":"My Studio"}]
```

If `node` command is unavailable, skip this step. The browser will validate on first load.

---

## Task 3: Refactor shell.js to read from RPDNavConfig

**Files:**
- Modify: `course-site/assets/shell.js` (lines 54-61)

- [ ] **Step 1: Read the current shell.js lines 54-61 to confirm state**

Run: `sed -n '54,61p' course-site/assets/shell.js`

Expected current content (post-commit 9f8720b):
```js
  // --- Topbar — centered tabs + theme toggle ---
  var topbar = el('header', { className: 'app-topbar' });

  topbar.appendChild(el('div', { className: 'app-tabs' }, [
    el('a', { className: 'app-tab', href: 'index.html', 'data-tab-target': 'archive', textContent: (document.documentElement.getAttribute('data-lang') || document.documentElement.lang || 'ko') === 'ko' ? '홈' : 'Home' }),
    el('a', { className: 'app-tab', href: 'inha.html', 'data-tab-target': 'class', textContent: 'Class' }),
    el('a', { className: 'app-tab', href: 'studio.html', 'data-tab-target': 'studio', textContent: 'My Studio' })
  ]));
```

- [ ] **Step 2: Replace lines 54-61 with config-driven version**

Use Edit tool to replace the block exactly:

**Old:**
```js
  // --- Topbar — centered tabs + theme toggle ---
  var topbar = el('header', { className: 'app-topbar' });

  topbar.appendChild(el('div', { className: 'app-tabs' }, [
    el('a', { className: 'app-tab', href: 'index.html', 'data-tab-target': 'archive', textContent: (document.documentElement.getAttribute('data-lang') || document.documentElement.lang || 'ko') === 'ko' ? '홈' : 'Home' }),
    el('a', { className: 'app-tab', href: 'inha.html', 'data-tab-target': 'class', textContent: 'Class' }),
    el('a', { className: 'app-tab', href: 'studio.html', 'data-tab-target': 'studio', textContent: 'My Studio' })
  ]));
```

**New:**
```js
  // --- Topbar — centered tabs + theme toggle ---
  var topbar = el('header', { className: 'app-topbar' });

  var lang = document.documentElement.getAttribute('data-lang') || document.documentElement.lang || 'ko';
  var navItems = (window.RPDNavConfig && window.RPDNavConfig.getTopbarItems(lang)) || [];
  var tabEls = navItems.map(function (item) {
    return el('a', {
      className: 'app-tab',
      href: item.href,
      'data-tab-target': item.tabTarget,
      textContent: item.label
    });
  });
  topbar.appendChild(el('div', { className: 'app-tabs' }, tabEls));
```

Note: `.is-active` class is NOT set here — `tab-system.js` handles it after shell.js runs.

- [ ] **Step 3: Verify the file still parses**

Run: `node --check course-site/assets/shell.js`

Expected: no output (success). If `node` unavailable, proceed — browser will validate.

---

## Task 4: Add nav-config.js script tag to data-shell pages

**Files:**
- Modify: `course-site/index.html` (before `shell.js`)
- Modify: `course-site/library.html` (before `shell.js`)
- Modify: `course-site/shortcuts.html` (before `shell.js`)
- Modify: `course-site/studio.html` (before `shell.js`)

- [ ] **Step 1: Add script tag to index.html**

Find the line: `<script src="assets/shell.js"></script>` in `course-site/index.html`.

Replace with:
```html
<script src="assets/nav-config.js"></script>
  <script src="assets/shell.js"></script>
```

(Keep the existing indentation of `<script src="assets/shell.js">`.)

- [ ] **Step 2: Add script tag to library.html**

Find the line: `<script src="assets/shell.js"></script>` in `course-site/library.html`.

Replace with:
```html
<script src="assets/nav-config.js"></script>
  <script src="assets/shell.js"></script>
```

- [ ] **Step 3: Add script tag to shortcuts.html**

Find the line: `<script src="assets/shell.js"></script>` in `course-site/shortcuts.html`.

Replace with:
```html
<script src="assets/nav-config.js"></script>
  <script src="assets/shell.js"></script>
```

- [ ] **Step 4: Add script tag to studio.html**

Find the line: `<script src="assets/shell.js"></script>` in `course-site/studio.html`.

Replace with:
```html
<script src="assets/nav-config.js"></script>
  <script src="assets/shell.js"></script>
```

---

## Task 5: Verify data-shell pages pass the new test

**Files:**
- No file changes (verification step)

- [ ] **Step 1: Run the test for data-shell pages**

Run: `npx playwright test tests/nav-unification.spec.js --project=desktop --grep "index.html|library.html|shortcuts.html|studio.html"`

Expected: PASS for all 4 pages (index, library, shortcuts, studio). Each should show the 3-tab topbar with 홈/Class/My Studio.

If FAIL: check the browser console via `npx playwright test --debug` or inspect the page in preview.

- [ ] **Step 2: Run the full test suite to confirm data-shell pages pass; hardcoded pages still fail**

Run: `npx playwright test tests/nav-unification.spec.js --project=desktop`

Expected: 4 passing (index/library/shortcuts/studio), 3 failing (inha/admin/week). This is expected at this checkpoint.

- [ ] **Step 3: Commit the foundation**

Run:
```bash
git add course-site/assets/nav-config.js course-site/assets/shell.js \
        course-site/index.html course-site/library.html \
        course-site/shortcuts.html course-site/studio.html \
        tests/nav-unification.spec.js
git commit -m "$(cat <<'EOF'
feat(nav): add nav-config.js as single source of truth for topbar

shell.js now reads topbar items from window.RPDNavConfig.getTopbarItems(lang)
instead of hardcoding them. Data-shell pages (index, library, shortcuts,
studio) load nav-config.js before shell.js.

Hardcoded-topbar pages (inha, admin, week) still need topbar-sync.js —
coming in follow-up commit.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 6: Create topbar-sync.js

**Files:**
- Create: `course-site/assets/topbar-sync.js`

- [ ] **Step 1: Write the topbar-sync.js module**

Create `course-site/assets/topbar-sync.js` with the following content:

```js
/* course-site/assets/topbar-sync.js
   For pages with hardcoded .app-tabs in HTML. Replaces the inner anchors
   with items from window.RPDNavConfig so every page shows the same topbar.
   Runs on DOMContentLoaded; sets .is-active itself because tab-system.js
   has already run (and would otherwise have assigned .is-active to the
   anchors that this script discards). */
(function () {
  'use strict';
  function sync() {
    if (!window.RPDNavConfig) return;
    var lang = document.documentElement.getAttribute('data-lang') ||
               document.documentElement.lang || 'ko';
    var items = window.RPDNavConfig.getTopbarItems(lang);
    var activeTab = (document.body && document.body.dataset.tab) || '';
    var containers = document.querySelectorAll('.app-tabs');
    for (var i = 0; i < containers.length; i++) {
      var container = containers[i];
      container.innerHTML = '';
      for (var j = 0; j < items.length; j++) {
        var item = items[j];
        var a = document.createElement('a');
        a.className = 'app-tab' + (item.tabTarget === activeTab ? ' is-active' : '');
        a.href = item.href;
        a.setAttribute('data-tab-target', item.tabTarget);
        a.textContent = item.label;
        container.appendChild(a);
      }
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', sync);
  } else {
    sync();
  }
})();
```

- [ ] **Step 2: Verify file syntax**

Run: `node --check course-site/assets/topbar-sync.js`

Expected: no output (success). If `node` unavailable, skip.

---

## Task 7: Add scripts to hardcoded-topbar pages (inha, admin, week)

**Files:**
- Modify: `course-site/inha.html`
- Modify: `course-site/admin.html`
- Modify: `course-site/week.html`

- [ ] **Step 1: Add scripts to inha.html**

Find the last `<script src="assets/..."></script>` line in `course-site/inha.html` (around line 74, after `week-ui.js`). Add AFTER it:

```html
<script src="assets/nav-config.js"></script>
  <script src="assets/topbar-sync.js"></script>
```

To locate: search for `<script src="assets/week-ui.js"></script>` — add the two new lines on the next lines, matching existing indentation (2 spaces).

- [ ] **Step 2: Add scripts to admin.html**

Find `<script src="assets/site-shell.js?v=20260318a"></script>` in `course-site/admin.html` (around line 163). Add AFTER it:

```html
<script src="assets/nav-config.js"></script>
  <script src="assets/topbar-sync.js"></script>
```

- [ ] **Step 3: Add scripts to week.html**

Find `<script src="assets/site-shell.js?v=20260318a"></script>` in `course-site/week.html` (around line 158). Add AFTER it:

```html
<script src="assets/nav-config.js"></script>
  <script src="assets/topbar-sync.js"></script>
```

---

## Task 8: Verify all 7 pages pass the test

**Files:**
- No file changes (verification step)

- [ ] **Step 1: Run the full nav-unification test suite**

Run: `npx playwright test tests/nav-unification.spec.js --project=desktop`

Expected: All 7 tests PASS.

- [ ] **Step 2: If any test fails, inspect manually**

For each failing page, open it in the preview server and check:
- Does `.app-tabs` exist in the DOM?
- Did `nav-config.js` load (check Network tab)?
- Did `topbar-sync.js` run (check console for errors)?
- Is `body[data-tab]` set correctly?

Fix any issues and re-run the test.

- [ ] **Step 3: Run the existing page-load regression suite**

Run: `npx playwright test tests/pages-load.spec.js --project=desktop`

Expected: All existing tests still pass (no regressions from nav changes).

---

## Task 9: Update i18n.js listLabel

**Files:**
- Modify: `course-site/assets/i18n.js` (line 309)

- [ ] **Step 1: Read the current line to confirm**

Run: `sed -n '307,311p' course-site/assets/i18n.js`

Expected current content includes: `listLabel: "Archive",`

- [ ] **Step 2: Update the label**

Use Edit tool:

**Old:** `listLabel: "Archive",`

**New:** `listLabel: "홈",`

Note: this is the `ko` localization block (around line 309). Do NOT change the `en` block's `listLabel` — leave that as `"Archive"` or update if the spec was to change both. Per spec, only the `ko` variant needs updating.

Verify by running: `grep -n 'listLabel' course-site/assets/i18n.js`

Expected output:
```
309:        listLabel: "홈",
...
```
(The `en` block at a similar line offset may have its own `listLabel`.)

- [ ] **Step 3: Verify week.html footer still renders**

Open `http://localhost:8771/week.html?week=3` in the browser. Scroll to the footer. The "← Archive" text (previously labeled via `listLabel`) should now show "← 홈".

---

## Task 10: Final regression sweep

**Files:**
- No file changes (verification step)

- [ ] **Step 1: Run all Playwright tests**

Run: `npx playwright test --project=desktop`

Expected: All tests pass (includes pages-load, theme, sidebar, tab-system, mobile, week05-enrichment, nav-unification).

- [ ] **Step 2: Run mobile viewport tests**

Run: `npx playwright test tests/nav-unification.spec.js --project=mobile`

Expected: Same 7 tests pass. Nav-unification doesn't change CSS, so mobile should work identically.

- [ ] **Step 3: Visual spot-check in preview browser**

Start the preview server (if not running): `python3 -m http.server 8773 --directory course-site` or existing course-site-preview.

Open each page and visually confirm:
- `http://localhost:8773/index.html` — topbar: 홈 / Class / My Studio, 홈 active
- `http://localhost:8773/library.html` — topbar: 홈 / Class / My Studio, 홈 active
- `http://localhost:8773/shortcuts.html` — topbar: 홈 / Class / My Studio, 홈 active
- `http://localhost:8773/studio.html` — topbar: 홈 / Class / My Studio, My Studio active
- `http://localhost:8773/inha.html` — topbar: 홈 / Class / My Studio, Class active
- `http://localhost:8773/week.html?week=3` — topbar: 홈 / Class / My Studio, Class active
- `http://localhost:8773/admin.html` — topbar: 홈 / Class / My Studio, no active tab

Check browser console on each page for errors.

---

## Task 11: Final commit

**Files:**
- No file changes (commit step)

- [ ] **Step 1: Review staged files**

Run: `git status`

Expected: modified inha.html, admin.html, week.html, i18n.js; new topbar-sync.js.

- [ ] **Step 2: Commit the sync layer**

Run:
```bash
git add course-site/assets/topbar-sync.js course-site/assets/i18n.js \
        course-site/inha.html course-site/admin.html course-site/week.html
git commit -m "$(cat <<'EOF'
feat(nav): sync hardcoded topbars via topbar-sync.js

inha/admin/week had hardcoded "Archive" topbars. topbar-sync.js runs on
DOMContentLoaded, reads from RPDNavConfig, and replaces anchors inside
.app-tabs with unified items (홈/Class/My Studio). Sets .is-active itself
because tab-system.js has already run.

Also updates i18n.js listLabel "Archive" → "홈" for week.html footer
consistency.

All 7 pages now show identical topbar labels/hrefs from single source of
truth (nav-config.js).

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 3: Show final git log**

Run: `git log --oneline -5`

Expected: two new commits on top of `96c9441` (the spec commit).

---

## Rollback Plan

If issues arise after merging, revert with:
```bash
git revert HEAD~1..HEAD
```

This removes both implementation commits. The spec commit (`96c9441`) stays as a record of the design.
