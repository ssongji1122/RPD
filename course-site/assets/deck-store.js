/* course-site/assets/deck-store.js
   My Studio — Deck data management (localStorage, Phase 1) */
(function () {
  'use strict';

  var STORAGE_KEY = 'rpd-decks';

  /* ── Helpers ─────────────────────────────────────────── */
  function uid() {
    return 'deck-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 7);
  }

  function now() {
    return new Date().toISOString();
  }

  /* ── Storage ─────────────────────────────────────────── */
  function loadDecks() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      var parsed = raw ? JSON.parse(raw) : [];
      return Array.isArray(parsed) ? parsed : [];
    } catch (e) {
      return [];
    }
  }

  function saveDecks(decks) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(decks));
    } catch (e) {
      console.warn('[DeckStore] localStorage write failed', e);
    }
  }

  /* ── Preset deck generation ───────────────────────────── */
  function buildPresets() {
    var presets = [];
    var catalog = (typeof SHOWME_CATALOG !== 'undefined') ? SHOWME_CATALOG : null;
    var curriculum = (typeof CURRICULUM !== 'undefined') ? CURRICULUM : null;
    if (!curriculum) return presets;

    curriculum.forEach(function (week) {
      // collect showme ids referenced in steps
      var cardIds = [];
      (week.steps || []).forEach(function (step) {
        var showme = step.showme;
      var ids = Array.isArray(showme) ? showme : (showme ? [showme] : []);
      ids.forEach(function (id) {
          if (typeof id === 'string' && cardIds.indexOf(id) === -1) cardIds.push(id);
        });
      });

      presets.push({
        id: 'preset-week-' + week.week,
        preset: true,
        name: 'Week ' + String(week.week).padStart(2, '0') + ' — ' + week.title,
        description: week.subtitle || '',
        week: week.week,
        status: week.status || 'upcoming',
        items: cardIds.map(function (id) { return { type: 'card', id: id }; }),
        createdAt: null,
        updatedAt: null,
      });
    });
    return presets;
  }

  /* ── Public API ───────────────────────────────────────── */

  /** Returns all user-created decks from localStorage */
  function getDecks() {
    return loadDecks();
  }

  /** Returns preset decks generated from CURRICULUM */
  function getPresets() {
    return buildPresets();
  }

  /** Create a new deck. Returns the created deck. */
  function createDeck(name, description, items) {
    var decks = loadDecks();
    var deck = {
      id: uid(),
      preset: false,
      name: (name || '새 덱').trim(),
      description: (description || '').trim(),
      items: Array.isArray(items) ? items : [],
      createdAt: now(),
      updatedAt: now(),
    };
    decks.push(deck);
    saveDecks(decks);
    return deck;
  }

  /** Update an existing deck by id. Returns updated deck or null. */
  function updateDeck(id, changes) {
    var decks = loadDecks();
    var idx = decks.findIndex(function (d) { return d.id === id; });
    if (idx === -1) return null;
    var deck = Object.assign({}, decks[idx]);
    if (changes.name !== undefined) deck.name = String(changes.name).trim();
    if (changes.description !== undefined) deck.description = String(changes.description).trim();
    if (changes.items !== undefined) deck.items = changes.items;
    deck.updatedAt = now();
    decks[idx] = deck;
    saveDecks(decks);
    return deck;
  }

  /** Delete a deck by id. Returns true if deleted. */
  function deleteDeck(id) {
    var decks = loadDecks();
    var next = decks.filter(function (d) { return d.id !== id; });
    if (next.length === decks.length) return false;
    saveDecks(next);
    return true;
  }

  /** Clone a preset deck into a user-editable copy. */
  function clonePreset(presetId) {
    var presets = buildPresets();
    var preset = presets.find(function (p) { return p.id === presetId; });
    if (!preset) return null;
    return createDeck(
      preset.name + ' (복사본)',
      preset.description,
      preset.items.slice()
    );
  }

  /* ── Export ───────────────────────────────────────────── */
  window.DeckStore = {
    getDecks: getDecks,
    getPresets: getPresets,
    createDeck: createDeck,
    updateDeck: updateDeck,
    deleteDeck: deleteDeck,
    clonePreset: clonePreset,
  };
})();
