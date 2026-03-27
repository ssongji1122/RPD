/* course-site/assets/topbar-search.js
   Topbar search — tab-aware (Archive:카드, Class:주차, Studio:덱)
   Security: ALL dynamic values are run through escHtml() before any
   innerHTML assignment. setHtml() documents this invariant at each call
   site. No untrusted HTML is ever injected. */
(function () {
  'use strict';

  /* ── HTML escaping ─────────────────────────────────── */
  function escHtml(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  // setHtml: all callers must sanitize via escHtml() before calling.
  function setHtml(el, safeHtml) {
    if (el) el.innerHTML = safeHtml; // safe: all dynamic values escaped
  }
  function escHref(s) {
    // href values are relative paths — just guard against quote injection
    return String(s == null ? '' : s).replace(/"/g, '%22').replace(/</g, '%3C').replace(/>/g, '%3E');
  }
  function slugToLabel(slug) {
    return slug.replace(/-/g, ' ').replace(/\b\w/g, function (c) { return c.toUpperCase(); });
  }

  var currentTab = document.body.dataset.tab || 'archive';

  function init() {
    var input    = document.getElementById('topbarSearch');
    var dropdown = document.getElementById('topbarSearchDropdown');
    if (!input || !dropdown) return;

    // Placeholder per tab
    var placeholders = {
      archive: '카드 검색...',
      class:   '주차 검색...',
      studio:  '내 덱 검색...'
    };
    input.placeholder = placeholders[currentTab] || placeholders.archive;

    input.addEventListener('input', function () {
      var q = input.value.trim().toLowerCase();
      if (!q) { hide(dropdown); return; }
      render(dropdown, search(currentTab, q));
    });

    input.addEventListener('focus', function () {
      var q = input.value.trim().toLowerCase();
      if (q) render(dropdown, search(currentTab, q));
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { hide(dropdown); input.blur(); }
      if (e.key === 'Enter' && !dropdown.hidden) {
        var first = dropdown.querySelector('a.tsdr-item');
        if (first) window.location.href = first.href;
      }
    });

    document.addEventListener('click', function (e) {
      var wrap = document.querySelector('.app-topbar-search');
      if (wrap && !wrap.contains(e.target)) hide(dropdown);
    });
  }

  /* ── Data sources ──────────────────────────────────── */

  function search(tab, q) {
    if (tab === 'archive') return searchCards(q);
    if (tab === 'class')   return searchWeeks(q);
    if (tab === 'studio')  return searchDecks(q);
    return [];
  }

  function searchCards(q) {
    if (typeof SHOWME_CATALOG === 'undefined') return [];
    var catMap = SHOWME_CATALOG.categoryMap || {};
    var results = [];
    var keys = Object.keys(catMap);
    for (var i = 0; i < keys.length && results.length < 7; i++) {
      var slug = keys[i];
      var label = slugToLabel(slug);
      var cat = (catMap[slug] || '').toLowerCase();
      if (label.toLowerCase().indexOf(q) !== -1 || cat.indexOf(q) !== -1 || slug.indexOf(q) !== -1) {
        results.push({ label: label, sub: catMap[slug] || '', href: 'library.html#' + slug });
      }
    }
    return results;
  }

  function searchWeeks(q) {
    if (typeof CURRICULUM === 'undefined') return [];
    var results = [];
    for (var i = 0; i < CURRICULUM.length && results.length < 7; i++) {
      var w = CURRICULUM[i];
      var title = (w.title || '').toLowerCase();
      var sub   = (w.subtitle || '').toLowerCase();
      if (('week ' + w.week).indexOf(q) !== -1 || title.indexOf(q) !== -1 || sub.indexOf(q) !== -1) {
        results.push({
          label: 'Week ' + String(w.week).padStart(2, '0') + ' — ' + (w.title || ''),
          sub:   w.subtitle || '',
          href:  'week.html?week=' + w.week
        });
      }
    }
    return results;
  }

  function searchDecks(q) {
    if (typeof DeckStore === 'undefined') return [];
    var decks   = DeckStore.getDecks();
    var results = [];
    for (var i = 0; i < decks.length && results.length < 7; i++) {
      var d = decks[i];
      if (d.name.toLowerCase().indexOf(q) !== -1 ||
          (d.description || '').toLowerCase().indexOf(q) !== -1) {
        results.push({
          label: d.name,
          sub:   d.description || (d.items.length + '개 카드'),
          href:  'studio.html'
        });
      }
    }
    return results;
  }

  /* ── Render ────────────────────────────────────────── */

  function render(dropdown, results) {
    if (!results.length) { hide(dropdown); return; }
    // All values passed through escHtml() — safe to assign via setHtml()
    setHtml(dropdown, results.map(function (r) {
      return '<a class="tsdr-item" href="' + escHref(r.href) + '">' +
        '<span class="tsdr-label">' + escHtml(r.label) + '</span>' +
        (r.sub ? '<span class="tsdr-sub">' + escHtml(r.sub) + '</span>' : '') +
        '</a>';
    }).join(''));
    dropdown.removeAttribute('hidden');
  }

  function hide(dropdown) {
    if (dropdown) { dropdown.setAttribute('hidden', ''); dropdown.innerHTML = ''; }
  }

  /* ── Boot ──────────────────────────────────────────── */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
