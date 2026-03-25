/* course-site/assets/tab-system.js
   Tab activation + search placeholder per tab */
(function () {
  'use strict';
  var currentTab = document.body.dataset.tab || 'archive';

  // Highlight active tab
  var tabs = document.querySelectorAll('.app-tab[data-tab-target]');
  for (var i = 0; i < tabs.length; i++) {
    if (tabs[i].dataset.tabTarget === currentTab) {
      tabs[i].classList.add('is-active');
    }
  }

  // Show only matching rail-context sections
  var contexts = document.querySelectorAll('.rail-context');
  for (var j = 0; j < contexts.length; j++) {
    contexts[j].hidden = contexts[j].dataset.tab !== currentTab;
  }

  // Update search placeholder per tab
  var search = document.querySelector('.app-search');
  if (search) {
    var placeholders = {
      archive: '카드 검색... (Extrude, Boolean, UV...)',
      class: '주차 검색... (Week 3, Mirror...)',
      studio: '내 덱 검색...'
    };
    search.placeholder = placeholders[currentTab] || placeholders.archive;
  }

  // Highlight active rail-item based on current URL path
  var path = location.pathname.replace(/^\//, '');
  var params = location.search;
  var railItems = document.querySelectorAll('.rail-context:not([hidden]) .rail-item[href]');
  for (var k = 0; k < railItems.length; k++) {
    var href = railItems[k].getAttribute('href').replace(/^\//, '');
    if (href === path || (path === '' && href === 'index.html')) {
      railItems[k].classList.add('is-active');
    }
  }

  // Highlight active week in rail-sub
  var weekMatch = params.match(/week=(\d+)/);
  if (weekMatch) {
    var weekNum = weekMatch[1];
    var subItems = document.querySelectorAll('.rail-sub-item[href]');
    for (var m = 0; m < subItems.length; m++) {
      if (subItems[m].getAttribute('href').indexOf('week=' + weekNum) !== -1) {
        subItems[m].classList.add('is-active');
      }
    }
  }
})();
