/* course-site/assets/auth.js
   RPD Auth — Google OAuth via Supabase
   미설정 시 (supabase-config.js 미완료) 자동으로 게스트 모드로 동작.
   설정 후에는 Google 로그인 → 세션 자동 저장 → user-profile.js와 연동. */
(function () {
  'use strict';

  /* ── 미설정 가드 ─────────────────────────────────────── */
  if (!window.SUPABASE_CONFIGURED) {
    window.RPDAuth = {
      isConfigured: false,
      signInWithGoogle: function () {
        alert('Supabase 설정이 필요해요.\nassets/supabase-config.js 에서 URL과 Anon Key를 입력해 주세요.');
      },
      signOut: function () {},
      getSession: function () { return Promise.resolve(null); },
      getUser: function () { return Promise.resolve(null); },
      onAuthStateChange: function () {},
    };
    return;
  }

  /* ── Supabase 클라이언트 초기화 ──────────────────────── */
  // Supabase JS v2 CDN — 각 HTML에서 supabase-js CDN 로드 필요
  var supabase = window.supabase
    ? window.supabase.createClient(window.SUPABASE_URL, window.SUPABASE_ANON)
    : null;

  if (!supabase) {
    console.warn('[RPDAuth] Supabase JS SDK가 로드되지 않았어요. CDN 스크립트를 확인해 주세요.');
    return;
  }

  /* ── Auth 콜백 처리 (OAuth redirect 후) ──────────────── */
  // Supabase v2는 URL hash의 access_token을 자동으로 처리함
  // 추가 처리 불필요 — supabase.auth.getSession()으로 바로 확인 가능

  /* ── 세션 복원 + user-profile.js 동기화 ─────────────── */
  supabase.auth.getSession().then(function (result) {
    var session = result.data && result.data.session;
    if (session) {
      syncUserProfile(session.user);
      // 첫 로그인 후 localStorage 덱 마이그레이션
      if (window.RPDSync) window.RPDSync.migrateIfNeeded(session.user.id);
    }
  });

  supabase.auth.onAuthStateChange(function (event, session) {
    if (event === 'SIGNED_IN' && session) {
      syncUserProfile(session.user);
      updateAuthUI(true, session.user);
      if (window.RPDSync) window.RPDSync.migrateIfNeeded(session.user.id);
    } else if (event === 'SIGNED_OUT') {
      updateAuthUI(false, null);
    }
  });

  /* ── user-profile.js 동기화 ──────────────────────────── */
  var USER_NAME_KEY = window.RPD_KEYS.USER_NAME;

  function syncUserProfile(user) {
    if (!user) return;
    var displayName = (user.user_metadata && user.user_metadata.full_name) || user.email || '사용자';
    localStorage.setItem(USER_NAME_KEY, displayName);
    // admin 체크는 admin-role.js가 담당
    var nameEl = document.getElementById('userName');
    var roleEl = document.getElementById('userRole');
    if (nameEl) nameEl.textContent = displayName;
    if (roleEl) roleEl.textContent = '수강생';
  }

  function updateAuthUI(isLoggedIn, user) {
    var loginBtn  = document.getElementById('authLoginBtn');
    var logoutBtn = document.getElementById('authLogoutBtn');
    var userSection = document.getElementById('userProfile');
    if (loginBtn)  loginBtn.hidden  = isLoggedIn;
    if (logoutBtn) logoutBtn.hidden = !isLoggedIn;
    if (userSection) userSection.dataset.loggedIn = isLoggedIn ? '1' : '0';
  }

  /* ── Public API ───────────────────────────────────────── */
  window.RPDAuth = {
    isConfigured: true,
    supabase: supabase,

    /** Google OAuth 팝업 로그인 */
    signInWithGoogle: function () {
      var redirectTo = window.location.origin + '/index.html';
      return supabase.auth.signInWithOAuth({
        provider: 'google',
        options: { redirectTo: redirectTo }
      });
    },

    /** 로그아웃 */
    signOut: function () {
      return supabase.auth.signOut().then(function () {
        localStorage.removeItem(USER_NAME_KEY);
        var nameEl = document.getElementById('userName');
        var roleEl = document.getElementById('userRole');
        if (nameEl) nameEl.textContent = '게스트';
        if (roleEl) roleEl.textContent = '로그인하세요';
      });
    },

    /** 현재 세션 반환 (Promise) */
    getSession: function () {
      return supabase.auth.getSession().then(function (r) {
        return r.data && r.data.session;
      });
    },

    /** 현재 유저 반환 (Promise) */
    getUser: function () {
      return supabase.auth.getUser().then(function (r) {
        return r.data && r.data.user;
      });
    },

    /** auth 상태 변화 구독 */
    onAuthStateChange: function (cb) {
      return supabase.auth.onAuthStateChange(cb);
    },
  };
})();
