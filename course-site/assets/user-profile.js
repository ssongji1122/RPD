/* course-site/assets/user-profile.js
   User profile management — localStorage based (Phase 1) */
(function () {
  'use strict';

  var STORAGE_KEY = 'rpd-user';
  var defaults = { name: '게스트', role: 'student', avatar: '👤' };

  function getUser() {
    try {
      var stored = JSON.parse(localStorage.getItem(STORAGE_KEY));
      var user = {};
      user.name = (stored && stored.name) || defaults.name;
      user.role = (stored && stored.role) || defaults.role;
      user.avatar = (stored && stored.avatar) || defaults.avatar;
      return user;
    } catch (e) {
      return { name: defaults.name, role: defaults.role, avatar: defaults.avatar };
    }
  }

  function saveUser(user) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(user));
  }

  function render() {
    var user = getUser();
    var nameEl = document.getElementById('userName');
    var roleEl = document.getElementById('userRole');
    var avatarEl = document.getElementById('userAvatar');

    if (nameEl) nameEl.textContent = user.name;
    if (roleEl) roleEl.textContent = user.role === 'admin' ? '관리자' : '학생';
    if (avatarEl) avatarEl.textContent = user.avatar;

    if (user.role === 'admin') {
      document.body.dataset.role = 'admin';
    }
  }

  // Dropdown toggle
  window.toggleUserMenu = function () {
    var menu = document.getElementById('userMenu');
    if (menu) menu.classList.toggle('is-open');
  };

  // Guest name change
  window.changeUserName = function () {
    var user = getUser();
    var name = prompt('이름을 입력하세요:', user.name);
    if (name && name.trim()) {
      user.name = name.trim();
      saveUser(user);
      render();
    }
    var menu = document.getElementById('userMenu');
    if (menu) menu.classList.remove('is-open');
  };

  // Close menu on outside click
  document.addEventListener('click', function (e) {
    var profile = document.getElementById('userProfile');
    var menu = document.getElementById('userMenu');
    if (menu && profile && !profile.contains(e.target)) {
      menu.classList.remove('is-open');
    }
  });

  // Admin role from URL param: ?role=admin
  var params = new URLSearchParams(location.search);
  if (params.get('role') === 'admin') {
    var user = getUser();
    user.role = 'admin';
    saveUser(user);
  }

  render();
})();
