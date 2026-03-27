/* course-site/assets/sync.js
   RPD Sync — localStorage 덱을 Supabase로 마이그레이션
   첫 로그인 시 1회만 실행. 이후에는 Supabase가 소스 오브 트루스. */
(function () {
  'use strict';

  var MIGRATION_KEY = 'rpd-synced-uid'; // 마이그레이션 완료 uid 저장
  var LOCAL_KEY     = 'rpd-decks';

  window.RPDSync = {
    /**
     * 첫 로그인 직후 호출.
     * 이미 마이그레이션된 계정이면 스킵.
     * localStorage에 덱이 있으면 Supabase로 upsert.
     */
    migrateIfNeeded: function (userId) {
      if (!window.SUPABASE_CONFIGURED) return;
      if (!window.RPDAuth || !window.RPDAuth.supabase) return;

      var donePreviously = localStorage.getItem(MIGRATION_KEY);
      if (donePreviously === userId) return; // 이미 완료

      var raw = localStorage.getItem(LOCAL_KEY);
      var decks;
      try { decks = raw ? JSON.parse(raw) : []; } catch (e) { decks = []; }
      if (!Array.isArray(decks) || decks.length === 0) {
        localStorage.setItem(MIGRATION_KEY, userId); // 마이그레이션할 것 없음
        return;
      }

      var supabase = window.RPDAuth.supabase;
      var rows = decks.map(function (d) {
        return {
          id:          d.id,
          user_id:     userId,
          name:        d.name        || '이름 없음',
          description: d.description || '',
          items:       d.items       || [],
          created_at:  d.createdAt   || new Date().toISOString(),
          updated_at:  d.updatedAt   || new Date().toISOString(),
        };
      });

      supabase.from('decks').upsert(rows, { onConflict: 'id' }).then(function (result) {
        if (result.error) {
          console.warn('[RPDSync] 마이그레이션 실패:', result.error.message);
          return;
        }
        localStorage.setItem(MIGRATION_KEY, userId);
        console.info('[RPDSync] 덱 ' + rows.length + '개를 Supabase로 이전했어요.');
        // 이후 DeckStore는 Supabase 모드로 전환됨 (deck-store.js 체크)
      });
    },

    /**
     * Supabase에서 덱 목록 가져오기.
     * DeckStore.getDecks() 대신 사용.
     * Returns: Promise<deck[]>
     */
    fetchDecks: function () {
      if (!window.SUPABASE_CONFIGURED || !window.RPDAuth || !window.RPDAuth.supabase) {
        return Promise.resolve(null); // null → DeckStore가 localStorage 사용
      }
      return window.RPDAuth.getUser().then(function (user) {
        if (!user) return null;
        return window.RPDAuth.supabase
          .from('decks')
          .select('*')
          .order('created_at', { ascending: true })
          .then(function (r) {
            if (r.error) { console.warn('[RPDSync] fetchDecks:', r.error.message); return null; }
            return (r.data || []).map(function (row) {
              return {
                id: row.id, preset: false,
                name: row.name, description: row.description,
                items: row.items || [],
                createdAt: row.created_at, updatedAt: row.updated_at,
              };
            });
          });
      });
    },

    /** Supabase에 덱 저장 (create/update 공용) */
    saveDeck: function (deck, userId) {
      if (!window.SUPABASE_CONFIGURED || !window.RPDAuth || !window.RPDAuth.supabase) return Promise.resolve();
      return window.RPDAuth.supabase.from('decks').upsert({
        id:          deck.id,
        user_id:     userId,
        name:        deck.name,
        description: deck.description || '',
        items:       deck.items || [],
        updated_at:  new Date().toISOString(),
      }, { onConflict: 'id' });
    },

    /** Supabase에서 덱 삭제 */
    deleteDeck: function (deckId) {
      if (!window.SUPABASE_CONFIGURED || !window.RPDAuth || !window.RPDAuth.supabase) return Promise.resolve();
      return window.RPDAuth.supabase.from('decks').delete().eq('id', deckId);
    },
  };
})();
