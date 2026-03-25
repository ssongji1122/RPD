/* course-site/assets/shell.js
   Shared topbar + rail injection for new pages (data-shell only) */
(function () {
  'use strict';
  var app = document.querySelector('.app[data-shell]');
  if (!app) return;

  var currentTab = document.body.dataset.tab || 'archive';

  // --- Helper: create element with attrs and children ---
  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (key) {
        if (key === 'className') node.className = attrs[key];
        else if (key === 'textContent') node.textContent = attrs[key];
        else if (key === 'onclick') node.setAttribute('onclick', attrs[key]);
        else node.setAttribute(key, attrs[key]);
      });
    }
    if (children) {
      children.forEach(function (child) {
        if (typeof child === 'string') {
          node.appendChild(document.createTextNode(child));
        } else if (child) {
          node.appendChild(child);
        }
      });
    }
    return node;
  }

  // --- Topbar — centered tabs + theme toggle ---
  var topbar = el('header', { className: 'app-topbar' });
  topbar.style.justifyContent = 'center';
  topbar.style.position = 'relative';

  topbar.appendChild(el('div', { className: 'app-tabs' }, [
    el('a', { className: 'app-tab', href: '/index.html', 'data-tab-target': 'archive', textContent: 'Archive' }),
    el('a', { className: 'app-tab', href: '/inha.html', 'data-tab-target': 'class', textContent: 'Class' }),
    el('a', { className: 'app-tab', href: '/studio.html', 'data-tab-target': 'studio', textContent: 'My Studio' })
  ]));

  var topbarRight = el('div', { className: 'app-topbar-right' });
  topbarRight.style.position = 'absolute';
  topbarRight.style.right = '20px';
  topbarRight.appendChild(el('button', { className: 'theme-toggle', onclick: 'toggleTheme()', 'aria-label': '테마 전환', textContent: '🌙' }));
  topbar.appendChild(topbarRight);

  // --- Rail content per tab ---
  function createRailItems(tab) {
    var container = el('div', { className: 'rail-context', 'data-tab': tab });

    var items = {
      archive: [
        { href: '/index.html', icon: '☗', text: '홈' },
        { href: '/library.html', icon: '🔍', text: '카드 찾기' },
        { href: '/shortcuts.html', icon: '⌨', text: '단축키' }
      ],
      class: [
        { href: '/inha.html', icon: '🏫', text: '수업 개요' }
      ],
      studio: [
        { href: '/studio.html', icon: '📦', text: '내 덱' },
        { href: '/studio.html#progress', icon: '📊', text: '진도' },
        { href: '/studio.html#settings', icon: '⚙', text: '설정' }
      ]
    };

    var tabItems = items[tab] || items.archive;
    tabItems.forEach(function (item) {
      container.appendChild(
        el('a', { className: 'rail-item', href: item.href }, [
          el('span', { className: 'rail-icon', textContent: item.icon }),
          el('span', { className: 'rail-text', textContent: item.text })
        ])
      );
    });

    // Add week sub-items for class tab
    if (tab === 'class') {
      var sub = el('div', { className: 'rail-sub' });
      for (var w = 1; w <= 15; w++) {
        var weekNum = w < 10 ? '0' + w : '' + w;
        sub.appendChild(
          el('a', { className: 'rail-sub-item', href: '/week.html?week=' + w }, [
            el('span', { className: 'rail-sub-dot' }),
            document.createTextNode('Week ' + weekNum)
          ])
        );
      }
      container.appendChild(sub);
    }

    return container;
  }

  // --- Rail ---
  var rail = el('nav', { className: 'rail', id: 'sideRail', 'aria-label': '사이드 탐색' });

  // Add all tab contexts (tab-system.js will show/hide them)
  ['archive', 'class', 'studio'].forEach(function (tab) {
    rail.appendChild(createRailItems(tab));
  });

  // Spacer
  rail.appendChild(el('div', { className: 'rail-spacer' }));

  // User profile
  var userProfile = el('div', { className: 'rail-user', id: 'userProfile', onclick: 'toggleUserMenu()' }, [
    el('div', { className: 'rail-user-avatar', id: 'userAvatar', textContent: '👤' }),
    el('div', { className: 'rail-user-info' }, [
      el('div', { className: 'rail-user-name', id: 'userName', textContent: '게스트' }),
      el('div', { className: 'rail-user-role', id: 'userRole', textContent: '로그인하세요' })
    ]),
    el('div', { className: 'rail-user-menu', id: 'userMenu' }, [
      el('a', { className: 'rail-user-menu-item', href: '/studio.html#settings', textContent: '⚙ 설정' }),
      el('a', { className: 'rail-user-menu-item', href: '/studio.html#progress', textContent: '📊 내 진도' }),
      el('div', { className: 'rail-user-menu-divider' }),
      el('a', { className: 'rail-user-menu-item', href: '/admin.html', 'data-admin': '', textContent: '🔧 관리자 패널' }),
      el('button', { className: 'rail-user-menu-item', onclick: 'changeUserName()', textContent: '✏️ 이름 변경' })
    ])
  ]);
  rail.appendChild(userProfile);

  // Toggle button
  rail.appendChild(
    el('button', { className: 'rail-toggle', onclick: 'toggleRail()' }, [
      el('span', { className: 'rail-toggle-arrow', textContent: '▶' }),
      el('span', { className: 'rail-text', textContent: '접기' })
    ])
  );

  // --- Assemble ---
  var main = app.querySelector('.main') || app.querySelector('main');
  // Clear app but keep main
  while (app.firstChild) app.removeChild(app.firstChild);
  app.appendChild(topbar);
  app.appendChild(rail);
  if (main) app.appendChild(main);

  // Mobile overlay
  var overlay = el('div', { className: 'rail-overlay', id: 'railOverlay', onclick: 'toggleMobileRail()' });
  document.body.appendChild(overlay);

  // Rail toggle function
  window.toggleRail = function () {
    var r = document.getElementById('sideRail');
    if (r) r.classList.toggle('is-expanded');
  };
})();
