/* course-site/assets/division-select.js
   RPD Division Select — 학생 분반 최초 선택 UI
   첫 로그인 시 profiles.division이 null이면 자동으로 모달 표시.
   이후 rail-user-menu의 "분반 변경" 버튼으로 재선택 가능. */
(function () {
  'use strict';

  var DIVISIONS = ['1분반', '2분반', '3분반', '4분반'];
  var MODAL_ID  = 'divisionModal';
  var LOCAL_DIV_KEY = 'rpd-division'; // 게스트 폴백용

  /* ── DOM 빌드 ──────────────────────────────────────────── */
  function buildModal() {
    if (document.getElementById(MODAL_ID)) return;

    var overlay = document.createElement('div');
    overlay.id = MODAL_ID;
    overlay.className = 'division-modal-overlay';
    overlay.hidden = true;
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-labelledby', 'divisionModalTitle');

    var options = DIVISIONS.map(function (d) {
      return '<button class="division-option" data-division="' + d + '" type="button">' + d + '</button>';
    }).join('');

    overlay.innerHTML =
      '<div class="division-modal">' +
        '<div class="division-modal-head">' +
          '<h2 class="division-modal-title" id="divisionModalTitle">분반 선택</h2>' +
        '</div>' +
        '<p class="division-modal-desc">본인 수업 분반을 선택해 주세요.<br>나중에 프로필 메뉴에서 변경할 수 있어요.</p>' +
        '<div class="division-options" id="divisionOptions">' + options + '</div>' +
        '<div class="division-modal-footer">' +
          '<button class="btn btn-ghost" id="divisionSkipBtn" type="button">나중에 선택</button>' +
        '</div>' +
      '</div>';

    document.body.appendChild(overlay);

    /* 옵션 클릭 */
    overlay.querySelector('#divisionOptions').addEventListener('click', function (e) {
      var btn = e.target.closest('.division-option');
      if (!btn) return;
      var division = btn.dataset.division;
      saveDivision(division);
    });

    /* 나중에 선택 */
    overlay.querySelector('#divisionSkipBtn').addEventListener('click', function () {
      close();
    });
  }

  /* ── Supabase에 분반 저장 ───────────────────────────────── */
  function saveDivision(division) {
    localStorage.setItem(LOCAL_DIV_KEY, division);
    updateDivisionUI(division);
    close();

    if (!window.SUPABASE_CONFIGURED || !window.RPDAuth || !window.RPDAuth.supabase) return;

    window.RPDAuth.getUser().then(function (user) {
      if (!user) return;
      window.RPDAuth.supabase
        .from('profiles')
        .update({ division: division })
        .eq('id', user.id)
        .then(function (r) {
          if (r.error) console.warn('[RPDDivisionSelect] 저장 실패:', r.error.message);
        });
    });
  }

  /* ── UI 업데이트 (userRole 표시) ────────────────────────── */
  function updateDivisionUI(division) {
    var roleEl = document.getElementById('userRole');
    if (roleEl && document.body.dataset.role !== 'admin') {
      roleEl.textContent = division ? division : '학생';
    }
    var divBtn = document.getElementById('menuDivisionBtn');
    if (divBtn) divBtn.textContent = division ? ('분반: ' + division + ' 변경') : '분반 선택';
  }

  /* ── 모달 열기/닫기 ────────────────────────────────────── */
  function open() {
    var overlay = document.getElementById(MODAL_ID);
    if (!overlay) return;
    overlay.hidden = false;
    /* 현재 선택된 분반 하이라이트 */
    var current = localStorage.getItem(LOCAL_DIV_KEY);
    var btns = overlay.querySelectorAll('.division-option');
    for (var i = 0; i < btns.length; i++) {
      btns[i].classList.toggle('is-selected', btns[i].dataset.division === current);
    }
  }

  function close() {
    var overlay = document.getElementById(MODAL_ID);
    if (overlay) overlay.hidden = true;
  }

  /* ── 초기화 ────────────────────────────────────────────── */
  function init() {
    buildModal();

    /* 로컬 저장값으로 UI 초기 반영 */
    var savedLocal = localStorage.getItem(LOCAL_DIV_KEY);
    if (savedLocal) updateDivisionUI(savedLocal);

    if (!window.SUPABASE_CONFIGURED || !window.RPDAuth) return;

    /* 로그인 이벤트 연동 */
    window.RPDAuth.onAuthStateChange(function (event, session) {
      if (event === 'SIGNED_IN' && session) {
        checkAndPrompt(session.user);
      }
      if (event === 'SIGNED_OUT') {
        updateDivisionUI(null);
      }
    });

    /* 페이지 로드 시 이미 로그인된 경우 */
    window.RPDAuth.getSession().then(function (session) {
      if (session && session.user) checkAndPrompt(session.user);
    });
  }

  /* ── profiles.division 확인 후 미선택이면 모달 표시 ────── */
  function checkAndPrompt(user) {
    if (!user) return;
    if (!window.RPDAuth.supabase) return;

    window.RPDAuth.supabase
      .from('profiles')
      .select('division')
      .eq('id', user.id)
      .single()
      .then(function (r) {
        if (r.error) return;
        var division = r.data && r.data.division;
        if (division) {
          localStorage.setItem(LOCAL_DIV_KEY, division);
          updateDivisionUI(division);
        } else {
          /* 분반 미선택 → 모달 표시 */
          open();
        }
      });
  }

  /* ── Login Gate 제어 ─────────────────────────────────── */
  function updateLoginGate(isLoggedIn) {
    var gate = document.getElementById('loginGate');
    var main = document.getElementById('my-decks');
    if (!gate || !window.SUPABASE_CONFIGURED) return;
    gate.hidden = isLoggedIn;
    if (main) main.hidden = !isLoggedIn;
  }

  /* ── auth rail-menu 표시/숨김 ────────────────────────── */
  function updateAuthRailMenu(isLoggedIn) {
    var guestEls  = document.querySelectorAll('.auth-guest-only');
    var loggedEls = document.querySelectorAll('.auth-loggedin-only');
    for (let i = 0; i < guestEls.length;  i++) guestEls[i].hidden  = isLoggedIn;
    for (let j = 0; j < loggedEls.length; j++) loggedEls[j].hidden = !isLoggedIn;
  }

  /* ── auth 이벤트 → login gate 연동 ──────────────────── */
  function bindLoginGate() {
    if (!window.SUPABASE_CONFIGURED || !window.RPDAuth) return;

    /* FOUC 방지: 세션 확인 전에 main을 즉시 숨김 */
    var mainEl = document.getElementById('my-decks');
    if (mainEl) mainEl.hidden = true;

    window.RPDAuth.getSession().then(function (session) {
      updateLoginGate(!!session);
    });

    window.RPDAuth.onAuthStateChange(function (event) {
      if (event === 'SIGNED_IN')  updateLoginGate(true);
      if (event === 'SIGNED_OUT') updateLoginGate(false);
    });

    /* auth 상태에 따라 rail-user-menu 항목 표시/숨김 */
    window.RPDAuth.onAuthStateChange(function (event) {
      updateAuthRailMenu(event === 'SIGNED_IN');
    });

    /* 초기 상태 반영 */
    window.RPDAuth.getSession().then(function (session) {
      updateAuthRailMenu(!!session);
    });
  }

  /* ── 공개 API ────────────────────────────────────────── */
  window.RPDDivisionSelect = { open: open, close: close, save: saveDivision };

  /* ── 실행 ────────────────────────────────────────────── */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { init(); bindLoginGate(); });
  } else {
    init();
    bindLoginGate();
  }
})();
