/* course-site/assets/admin-role.js
   RPD Admin Role — Supabase profiles.role 기반 admin 권한 확인
   미설정 시 현재 user-profile.js의 localStorage 기반 동작 유지. */
(function () {
  'use strict';

  var ADMIN_KEY     = window.RPD_KEYS.IS_ADMIN;  // 세션 캐시용 localStorage 키
  var ADMIN_DEV_KEY = window.RPD_KEYS.ADMIN_DEV; // 개발용 강제 설정 키

  window.RPDAdminRole = {
    /**
     * 현재 로그인된 유저의 role을 Supabase에서 확인.
     * Returns Promise<boolean>
     */
    checkIsAdmin: function () {
      if (!window.SUPABASE_CONFIGURED || !window.RPDAuth || !window.RPDAuth.supabase) {
        // 미설정: localStorage rpd-admin 값으로 fallback (개발용)
        return Promise.resolve(localStorage.getItem(ADMIN_DEV_KEY) === '1');
      }

      return window.RPDAuth.getUser().then(function (user) {
        if (!user) {
          localStorage.removeItem(ADMIN_KEY);
          return false;
        }
        return window.RPDAuth.supabase
          .from('profiles')
          .select('role')
          .eq('id', user.id)
          .single()
          .then(function (r) {
            var isAdmin = !r.error && r.data && r.data.role === 'admin';
            localStorage.setItem(ADMIN_KEY, isAdmin ? '1' : '0');
            return isAdmin;
          });
      });
    },

    /**
     * admin 여부에 따라 UI 업데이트.
     * .admin-only 클래스 요소를 show/hide.
     */
    applyAdminUI: function (isAdmin) {
      var els = document.querySelectorAll('.admin-only');
      for (var i = 0; i < els.length; i++) {
        els[i].hidden = !isAdmin;
      }
      // rail user role 텍스트 업데이트
      var roleEl = document.getElementById('userRole');
      if (roleEl && isAdmin) roleEl.textContent = '관리자';
    },

    /** checkIsAdmin + applyAdminUI 한 번에 실행 */
    init: function () {
      window.RPDAdminRole.checkIsAdmin().then(function (isAdmin) {
        window.RPDAdminRole.applyAdminUI(isAdmin);
      });
    },
  };

  // auth 이벤트에 연동
  if (window.RPDAuth && window.RPDAuth.onAuthStateChange) {
    window.RPDAuth.onAuthStateChange(function (event) {
      if (event === 'SIGNED_IN')  window.RPDAdminRole.init();
      if (event === 'SIGNED_OUT') window.RPDAdminRole.applyAdminUI(false);
    });
  }

  // 페이지 로드 시 1회 실행
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', window.RPDAdminRole.init);
  } else {
    window.RPDAdminRole.init();
  }
})();
