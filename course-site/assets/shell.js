/* course-site/assets/shell.js
   Shared topbar + rail injection for new pages (data-shell only) */
(function () {
  'use strict';
  var app = document.querySelector('.app[data-shell]');
  if (!app) return;

  var currentTab = document.body.dataset.tab || 'archive';

  // --- Helper: parse inline SVG string into DOM element ---
  // innerHTML is safe here: SVG strings are hardcoded constants, not user input.
  function svgIcon(svgStr) {
    var temp = document.createElement('div');
    temp.innerHTML = svgStr;
    return temp.firstChild;
  }

  // --- SVG icon constants (Lucide, 18x18, stroke-width 2) ---
  var ICONS = {
    home: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg>',
    search: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>',
    keyboard: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 8h.01"/><path d="M12 12h.01"/><path d="M14 8h.01"/><path d="M16 12h.01"/><path d="M18 8h.01"/><path d="M6 8h.01"/><path d="M7 16h10"/><path d="M8 12h.01"/><rect width="20" height="16" x="2" y="4" rx="2"/></svg>',
    layers: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m2 12 8.58 3.91a2 2 0 0 0 1.66 0L21 12"/><path d="m2 17 8.58 3.91a2 2 0 0 0 1.66 0L21 17"/></svg>',
    package: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 21.73a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73z"/><path d="M12 22V12"/><path d="m3.3 7 7.703 4.734a2 2 0 0 0 1.994 0L20.7 7"/></svg>',
    barChart: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" x2="18" y1="20" y2="10"/><line x1="12" x2="12" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="14"/></svg>',
    settings: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>',
    graduationCap: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.42 10.922a1 1 0 0 0-.019-1.838L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0z"/><path d="M22 10v6"/><path d="M6 12.5V16a6 3 0 0 0 12 0v-3.5"/></svg>',
    user: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>'
  };

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
        { href: '/index.html', svg: ICONS.home, text: '홈' },
        { href: '/library.html', svg: ICONS.search, text: '카드 찾기' },
        { href: '/shortcuts.html', svg: ICONS.keyboard, text: '단축키' }
      ],
      class: [
        { href: '/inha.html', svg: ICONS.graduationCap, text: '수업 개요' }
      ],
      studio: [
        { href: '/studio.html', svg: ICONS.package, text: '내 덱' },
        { href: '/studio.html#progress', svg: ICONS.barChart, text: '진도' },
        { href: '/studio.html#settings', svg: ICONS.settings, text: '설정' }
      ]
    };

    var tabItems = items[tab] || items.archive;
    tabItems.forEach(function (item) {
      var iconSpan = el('span', { className: 'rail-icon' });
      iconSpan.appendChild(svgIcon(item.svg));
      container.appendChild(
        el('a', { className: 'rail-item', href: item.href }, [
          iconSpan,
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
  var userAvatarEl = el('div', { className: 'rail-user-avatar', id: 'userAvatar' });
  userAvatarEl.appendChild(svgIcon(ICONS.user));
  var userProfile = el('div', { className: 'rail-user', id: 'userProfile', onclick: 'toggleUserMenu()' }, [
    userAvatarEl,
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
