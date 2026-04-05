/* course-site/assets/topbar-sync.js
   For pages with hardcoded .app-tabs in HTML. Replaces the inner anchors
   with items from window.RPDNavConfig so every page shows the same topbar.
   Runs on DOMContentLoaded; sets .is-active itself because tab-system.js
   has already run (and would otherwise have assigned .is-active to the
   anchors that this script discards). */
(function () {
  'use strict';
  function sync() {
    if (!window.RPDNavConfig) return;
    var lang = document.documentElement.getAttribute('data-lang') ||
               document.documentElement.lang || 'ko';
    var items = window.RPDNavConfig.getTopbarItems(lang);
    var activeTab = (document.body && document.body.dataset.tab) || '';
    var containers = document.querySelectorAll('.app-tabs');
    for (var i = 0; i < containers.length; i++) {
      var container = containers[i];
      container.innerHTML = '';
      for (var j = 0; j < items.length; j++) {
        var item = items[j];
        var a = document.createElement('a');
        a.className = 'app-tab' + (item.tabTarget === activeTab ? ' is-active' : '');
        a.href = item.href;
        a.setAttribute('data-tab-target', item.tabTarget);
        a.textContent = item.label;
        container.appendChild(a);
      }
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', sync);
  } else {
    sync();
  }
})();
