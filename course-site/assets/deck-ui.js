/* course-site/assets/deck-ui.js
   My Studio — Deck UI rendering, modal, card picker
   Security: all user-supplied strings are escaped through escHtml()
   before any innerHTML assignment. No untrusted HTML is injected. */
(function () {
  'use strict';

  /* ── HTML escaping ────────────────────────────────────── */
  function escHtml(str) {
    return String(str == null ? '' : str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  /* ── setHtml: wrapper that documents intent ───────────── */
  // All callers must sanitize via escHtml() before passing to this.
  function setHtml(el, safeHtml) {
    if (el) el.innerHTML = safeHtml; // safe: all dynamic values escaped
  }

  /* ── Card catalog helpers ─────────────────────────────── */
  function getCatalogEntries() {
    if (typeof SHOWME_CATALOG === 'undefined') return [];
    // Card slugs live in categoryMap (slug → category name)
    var catMap = SHOWME_CATALOG.categoryMap || {};
    return Object.keys(catMap)
      .map(function (slug) {
        return { slug: slug, label: slugToLabel(slug), category: catMap[slug] || '' };
      })
      .sort(function (a, b) { return a.label.localeCompare(b.label); });
  }

  function slugToLabel(slug) {
    return slug.replace(/-/g, ' ').replace(/\b\w/g, function (c) { return c.toUpperCase(); });
  }

  /* ── Inline SVG icons ─────────────────────────────────── */
  var ICON_DECK   = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/></svg>';
  var ICON_EDIT   = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>';
  var ICON_DELETE = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/></svg>';
  var ICON_CLONE  = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>';
  var ICON_PLUS   = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>';

  var STATUS_LABEL = { done: '완료', 'in-progress': '진행 중', upcoming: '예정' };

  /* ── Render single deck card HTML ─────────────────────── */
  function renderDeckCard(deck) {
    var isPreset = deck.preset;
    var cardCount = (deck.items || []).filter(function (i) { return i.type === 'card'; }).length;
    // deck.id is auto-generated (alphanumeric + hyphens) — safe as attribute value
    var safeId = escHtml(deck.id);

    var badgeHtml = isPreset
      ? '<span class="deck-card-badge badge-preset">' + escHtml(STATUS_LABEL[deck.status] || '예정') + '</span>'
      : '';

    var actionsHtml = isPreset
      ? '<button class="deck-btn" data-clone="' + safeId + '">' + ICON_CLONE + ' 복제</button>'
      : '<button class="deck-btn" data-edit="' + safeId + '">' + ICON_EDIT + ' 편집</button>' +
        '<span class="deck-btn-spacer"></span>' +
        '<button class="deck-btn deck-btn-danger" data-delete="' + safeId + '">' + ICON_DELETE + ' 삭제</button>';

    var descHtml = deck.description
      ? '<p class="deck-card-desc">' + escHtml(deck.description) + '</p>'
      : '';

    return '<div class="deck-card' + (isPreset ? ' is-preset' : '') + '" data-deck-id="' + safeId + '">' +
      '<div class="deck-card-top">' +
        '<h3 class="deck-card-name">' + escHtml(deck.name) + '</h3>' +
        badgeHtml +
      '</div>' +
      descHtml +
      '<div class="deck-card-meta">' +
        '<span class="deck-card-count">' + ICON_DECK + ' ' + escHtml(String(cardCount)) + '개 카드</span>' +
      '</div>' +
      '<div class="deck-card-actions">' + actionsHtml + '</div>' +
    '</div>';
  }

  function renderNewButton() {
    return '<button class="deck-card-new" id="deckNewBtn" type="button" aria-label="새 덱 만들기">' +
      ICON_PLUS + '<span>새 덱 만들기</span></button>';
  }

  /* ── Render deck grid ─────────────────────────────────── */
  function renderDeckGrid() {
    var grid = document.getElementById('deckGrid');
    var countEl = document.getElementById('deckCount');
    if (!grid) return;

    var decks = DeckStore.getDecks();
    if (countEl) countEl.textContent = decks.length ? decks.length + '개' : '';

    if (decks.length === 0) {
      setHtml(grid,
        '<div class="studio-empty-state">' +
          '<p class="studio-empty-text">아직 만든 덱이 없어요.</p>' +
          '<p class="studio-empty-hint">프리셋 덱을 복제하거나 새로 만들어 보세요.</p>' +
          '<button class="btn btn-primary studio-create-btn" id="deckNewBtnEmpty" type="button">+ 첫 번째 덱 만들기</button>' +
        '</div>'
      );
      var emptyBtn = document.getElementById('deckNewBtnEmpty');
      if (emptyBtn) emptyBtn.addEventListener('click', openCreateModal);
    } else {
      setHtml(grid, decks.map(renderDeckCard).join('') + renderNewButton());
      var newBtn = document.getElementById('deckNewBtn');
      if (newBtn) newBtn.addEventListener('click', openCreateModal);
    }

    grid.addEventListener('click', function (e) {
      var editBtn   = e.target.closest('[data-edit]');
      var deleteBtn = e.target.closest('[data-delete]');
      var cloneBtn  = e.target.closest('[data-clone]');
      if (editBtn)   openEditModal(editBtn.dataset.edit);
      if (deleteBtn) confirmDelete(deleteBtn.dataset.delete);
      if (cloneBtn)  clonePreset(cloneBtn.dataset.clone);
    });
  }

  /* ── Render preset grid ───────────────────────────────── */
  function renderPresetGrid() {
    var grid = document.getElementById('presetGrid');
    if (!grid) return;
    var presets = DeckStore.getPresets();
    if (!presets.length) {
      setHtml(grid, '<p class="card-picker-empty">커리큘럼 데이터를 불러올 수 없어요.</p>');
      return;
    }
    setHtml(grid, presets.map(renderDeckCard).join(''));
    grid.addEventListener('click', function (e) {
      var cloneBtn = e.target.closest('[data-clone]');
      if (cloneBtn) clonePreset(cloneBtn.dataset.clone);
    });
  }

  function clonePreset(presetId) {
    DeckStore.clonePreset(presetId);
    renderDeckGrid();
  }

  function confirmDelete(deckId) {
    var decks = DeckStore.getDecks();
    var deck = decks.find(function (d) { return d.id === deckId; });
    if (!deck) return;
    // confirm() is synchronous native dialog — no XSS risk
    if (!window.confirm('"' + deck.name.replace(/"/g, '\\"') + '" 덱을 삭제할까요?')) return;
    DeckStore.deleteDeck(deckId);
    renderDeckGrid();
  }

  /* ── Modal state ──────────────────────────────────────── */
  var _editingId = null;
  var _selectedCards = [];
  var _catalogEntries = null;

  function getCatalog() {
    if (!_catalogEntries) _catalogEntries = getCatalogEntries();
    return _catalogEntries;
  }

  function openCreateModal() {
    _editingId = null;
    _selectedCards = [];
    document.getElementById('deckModalTitle').textContent = '새 덱 만들기';
    document.getElementById('deckNameInput').value = '';
    document.getElementById('deckDescInput').value = '';
    document.getElementById('cardPickerSearch').value = '';
    renderCardPicker('');
    openModal();
    document.getElementById('deckNameInput').focus();
  }

  function openEditModal(deckId) {
    var decks = DeckStore.getDecks();
    var deck = decks.find(function (d) { return d.id === deckId; });
    if (!deck) return;
    _editingId = deckId;
    _selectedCards = (deck.items || [])
      .filter(function (i) { return i.type === 'card'; })
      .map(function (i) { return i.id; });
    document.getElementById('deckModalTitle').textContent = '덱 편집';
    document.getElementById('deckNameInput').value = deck.name;
    document.getElementById('deckDescInput').value = deck.description || '';
    document.getElementById('cardPickerSearch').value = '';
    renderCardPicker('');
    openModal();
    document.getElementById('deckNameInput').focus();
  }

  function openModal() {
    var overlay = document.getElementById('deckModalOverlay');
    if (overlay) overlay.removeAttribute('hidden');
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    var overlay = document.getElementById('deckModalOverlay');
    if (overlay) overlay.setAttribute('hidden', '');
    document.body.style.overflow = '';
    _editingId = null;
    _selectedCards = [];
  }

  /* ── Card picker ──────────────────────────────────────── */
  function renderCardPicker(query) {
    var list = document.getElementById('cardPickerList');
    if (!list) return;

    var entries = getCatalog();
    var q = (query || '').toLowerCase();
    var filtered = q
      ? entries.filter(function (e) {
          return e.label.toLowerCase().indexOf(q) !== -1 ||
                 e.slug.toLowerCase().indexOf(q) !== -1 ||
                 e.category.toLowerCase().indexOf(q) !== -1;
        })
      : entries;

    if (!filtered.length) {
      setHtml(list, '<div class="card-picker-empty">검색 결과가 없어요.</div>');
    } else {
      setHtml(list, filtered.map(function (e) {
        // e.slug comes from catalog keys (ASCII), e.label/category are escaped
        var checked = _selectedCards.indexOf(e.slug) !== -1;
        return '<label class="card-picker-item" role="option" aria-selected="' + checked + '">' +
          '<input type="checkbox" value="' + escHtml(e.slug) + '"' + (checked ? ' checked' : '') + '>' +
          '<span class="card-picker-item-name">' + escHtml(e.label) + '</span>' +
          '<span class="card-picker-item-cat">' + escHtml(e.category) + '</span>' +
        '</label>';
      }).join(''));
    }

    updateChipCount();

    list.querySelectorAll('input[type="checkbox"]').forEach(function (cb) {
      cb.addEventListener('change', function () {
        if (cb.checked) {
          if (_selectedCards.indexOf(cb.value) === -1) _selectedCards.push(cb.value);
        } else {
          _selectedCards = _selectedCards.filter(function (id) { return id !== cb.value; });
        }
        updateChipCount();
      });
    });
  }

  function updateChipCount() {
    var el = document.getElementById('pickerChipCount');
    if (!el) return;
    var n = _selectedCards.length;
    el.textContent = n + '개 선택됨';
    el.classList.toggle('has-items', n > 0);
  }

  /* ── Save ─────────────────────────────────────────────── */
  function handleSave() {
    var nameInput = document.getElementById('deckNameInput');
    var name = (nameInput.value || '').trim();
    if (!name) { nameInput.focus(); return; }
    var desc = (document.getElementById('deckDescInput').value || '').trim();
    var items = _selectedCards.map(function (id) { return { type: 'card', id: id }; });

    if (_editingId) {
      DeckStore.updateDeck(_editingId, { name: name, description: desc, items: items });
    } else {
      DeckStore.createDeck(name, desc, items);
    }
    closeModal();
    renderDeckGrid();
  }

  /* ── Init ─────────────────────────────────────────────── */
  function init() {
    renderDeckGrid();
    renderPresetGrid();

    var closeBtn  = document.getElementById('deckModalClose');
    var cancelBtn = document.getElementById('deckModalCancel');
    var saveBtn   = document.getElementById('deckModalSave');
    var overlay   = document.getElementById('deckModalOverlay');
    var search    = document.getElementById('cardPickerSearch');
    var nameInput = document.getElementById('deckNameInput');

    if (closeBtn)  closeBtn.addEventListener('click', closeModal);
    if (cancelBtn) cancelBtn.addEventListener('click', closeModal);
    if (saveBtn)   saveBtn.addEventListener('click', handleSave);

    if (overlay) {
      overlay.addEventListener('click', function (e) {
        if (e.target === overlay) closeModal();
      });
    }

    document.addEventListener('keydown', function (e) {
      var ov = document.getElementById('deckModalOverlay');
      if (e.key === 'Escape' && ov && !ov.hasAttribute('hidden')) closeModal();
    });

    if (nameInput) {
      nameInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') handleSave();
      });
    }

    if (search) {
      search.addEventListener('input', function () {
        renderCardPicker(search.value);
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
