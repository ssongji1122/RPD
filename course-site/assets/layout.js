/* =====================================================================
   course-site/assets/layout.js
   공통 레이아웃 셸 — 레일 토글 + 현재 페이지 하이라이트
   ===================================================================== */

(function () {
  'use strict';

  /* ── Rail toggle ── */
  var RAIL_KEY = window.RPD_KEYS.RAIL;
  var rail = document.getElementById('sideRail');
  var toggle = document.getElementById('railToggle');
  if (rail && toggle) {
    toggle.addEventListener('click', function () {
      rail.classList.toggle('is-expanded');
      localStorage.setItem(RAIL_KEY, rail.classList.contains('is-expanded') ? 'open' : 'closed');
    });
    // Restore saved state (desktop only)
    if (window.innerWidth > 720 && localStorage.getItem(RAIL_KEY) === 'open') {
      rail.classList.add('is-expanded');
    }
  }

  /* ── Highlight current page in rail ── */
  var path = location.pathname.split('/').pop() || 'index.html';
  var links = document.querySelectorAll('.rail-item[data-page]');
  links.forEach(function (link) {
    if (link.getAttribute('data-page') === path) {
      link.classList.add('is-active');
    }
  });
})();
