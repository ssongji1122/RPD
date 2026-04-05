/* course-site/assets/nav-config.js
   Single source of truth for topbar navigation items.
   Consumed by shell.js (data-shell pages) and topbar-sync.js (hardcoded pages). */
(function (win) {
  'use strict';
  win.RPDNavConfig = {
    /**
     * Returns the topbar nav items for the given language.
     * @param {'ko'|'en'} lang
     * @returns {Array<{href:string, tabTarget:string, label:string}>}
     */
    getTopbarItems: function (lang) {
      var isKo = (lang || 'ko') === 'ko';
      return [
        { href: 'index.html', tabTarget: 'archive', label: isKo ? '홈' : 'Home' },
        { href: 'inha.html', tabTarget: 'class', label: 'Class' },
        { href: 'studio.html', tabTarget: 'studio', label: 'My Studio' }
      ];
    }
  };
})(window);
