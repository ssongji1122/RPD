(function(global) {
  var DIFFICULTY_LABELS = {
    beginner: "입문",
    intermediate: "중급",
    advanced: "심화"
  };

  function readShowMeGlobal(name) {
    if (global && global[name]) return global[name];
    try {
      if (global.parent && global.parent !== global && global.parent[name]) {
        return global.parent[name];
      }
    } catch (error) {}
    return null;
  }

  function getCatalog() {
    return readShowMeGlobal("SHOWME_CATALOG") || {};
  }

  function getRegistry() {
    return readShowMeGlobal("SHOWME_REGISTRY") || {};
  }

  function getSupplements() {
    return readShowMeGlobal("SHOWME_SUPPLEMENTS") || null;
  }

  function getShowMeCategoryOrder() {
    var catalog = getCatalog();
    return Array.isArray(catalog.categoryOrder) && catalog.categoryOrder.length
      ? catalog.categoryOrder.slice()
      : ["전체", "기타"];
  }

  function getShowMeManualSectionOrder() {
    var catalog = getCatalog();
    return Array.isArray(catalog.manualSectionOrder) && catalog.manualSectionOrder.length
      ? catalog.manualSectionOrder.slice()
      : ["getting-started", "user-interface", "modeling", "sculpting-painting", "materials-uv", "rendering", "animation-rigging"];
  }

  function getShowMeEntry(id) {
    var registry = getRegistry();
    var catalog = getCatalog();
    var base = registry[id] || { label: id, icon: "📖" };
    var categoryMap = catalog.categoryMap || {};
    var categoryDefaults = catalog.categoryDefaults || {};
    var overrides = (catalog.cardOverrides && catalog.cardOverrides[id]) || {};
    var category = overrides.category || categoryMap[id] || "기타";
    var defaults = categoryDefaults[category] || {};

    return Object.assign({
      id: id,
      category: category,
      difficulty: "intermediate",
      confusionLabel: "작업 흐름",
      stageLabel: "보조 개념",
      supplementPriority: "medium",
      visualPattern: "comparison",
      prerequisites: [],
      keywords: []
    }, base, defaults, overrides);
  }

  function getShowMeDifficultyLabel(difficulty) {
    return DIFFICULTY_LABELS[difficulty] || difficulty || "";
  }

  function getShowMeTooltipText(id) {
    var entry = getShowMeEntry(id);
    var parts = [
      entry.category,
      getShowMeDifficultyLabel(entry.difficulty),
      entry.confusionLabel
    ].filter(Boolean);
    return parts.join(" · ");
  }

  function getShowMeManualSectionFallback(category) {
    if (category === "Sculpting") return "sculpting-painting";
    if (category === "Material" || category === "UV") return "materials-uv";
    if (category === "Lighting" || category === "Rendering") return "rendering";
    if (category === "Animation" || category === "Rigging") return "animation-rigging";
    if (category === "Generate Modifiers" || category === "Normals") return "modeling";
    if (category === "Edit Mode") return "user-interface";
    return "getting-started";
  }

  function getShowMeManualSectionId(id) {
    var catalog = getCatalog();
    var map = catalog.manualSectionMap || {};
    if (map[id]) return map[id];
    var entry = getShowMeEntry(id);
    return getShowMeManualSectionFallback(entry.category || "기타");
  }

  function activateShowMeTab(doc, tabName) {
    if (!doc || !tabName) return;
    var tabs = Array.from(doc.querySelectorAll(".tab"));
    var panels = Array.from(doc.querySelectorAll(".panel"));
    tabs.forEach(function(tab) {
      var active = tab.dataset.tab === tabName;
      tab.classList.toggle("is-active", active);
      tab.setAttribute("aria-selected", active ? "true" : "false");
    });
    panels.forEach(function(panel) {
      panel.classList.toggle("is-active", panel.id === ("panel-" + tabName));
    });
    updateShowMeTabNavigation(doc);
  }

  function triggerShowMeTab(doc, tabName) {
    if (!doc || !tabName) return;
    var tab = doc.querySelector('.tab[data-tab="' + tabName + '"]');
    if (tab && typeof tab.click === "function") {
      tab.click();
      return;
    }
    activateShowMeTab(doc, tabName);
  }

  function bindShowMeTabs(doc) {
    if (!doc) return;
    Array.from(doc.querySelectorAll(".tab")).forEach(function(tab) {
      if (tab.dataset.rpdTabBound === "true") return;
      tab.dataset.rpdTabBound = "true";
      tab.setAttribute("aria-selected", tab.classList.contains("is-active") ? "true" : "false");
      tab.addEventListener("click", function() {
        activateShowMeTab(doc, tab.dataset.tab);
      });
    });
  }

  function getShowMeDocLang(doc) {
    try {
      if (global.parent && global.parent.RPDI18n && typeof global.parent.RPDI18n.getLanguage === "function") {
        return global.parent.RPDI18n.getLanguage();
      }
    } catch (error) {}
    if (doc && doc.documentElement) {
      return doc.documentElement.getAttribute("data-lang") || doc.documentElement.lang || "ko";
    }
    return "ko";
  }

  function getShowMeActionLabel(doc, key) {
    var lang = getShowMeDocLang(doc) === "en" ? "en" : "ko";
    var labels = {
      visual: { ko: "직접 해보기", en: "Try It" },
      quiz: { ko: "퀴즈 풀기", en: "Take Quiz" }
    };
    return labels[key] ? labels[key][lang] : "";
  }

  function getShowMeActionPromptCopy(doc, hasInteractiveDemo, hasQuiz) {
    var lang = getShowMeDocLang(doc) === "en" ? "en" : "ko";
    if (lang === "en") {
      return {
        aria: "Suggested actions",
        kicker: "Next",
        title: "You can continue right away.",
        body: hasInteractiveDemo && hasQuiz
          ? "Once the idea clicks, jump into the interactive demo or confirm it with a quick quiz."
          : (hasInteractiveDemo
            ? "Once the idea clicks, jump into the interactive demo."
            : "Once the idea clicks, confirm it with a quick quiz.")
      };
    }

    return {
      aria: "추천 액션",
      kicker: "다음 액션",
      title: "이어서 바로 해볼 수 있어요.",
      body: hasInteractiveDemo && hasQuiz
        ? "원리를 봤다면 직접 조작해보거나 짧은 퀴즈로 바로 확인해보세요."
        : (hasInteractiveDemo
          ? "원리를 봤다면 바로 직접 조작해보세요."
          : "원리를 봤다면 짧은 퀴즈로 바로 확인해보세요.")
    };
  }

  function getShowMeConceptMoreSummaryLabel(doc) {
    return getShowMeDocLang(doc) === "en" ? "Expand details" : "보충 설명 펼치기";
  }

  function getShowMeWidgetId(doc) {
    if (!doc || !doc.defaultView || !doc.defaultView.location) return "";
    try {
      var params = new URLSearchParams(doc.defaultView.location.search || "");
      var wid = params.get("wid");
      if (wid) return wid;
    } catch (error) {}

    var pathname = doc.defaultView.location.pathname || "";
    var match = pathname.match(/\/([^/]+)\.html$/);
    return match ? match[1] : "";
  }

  function getShowMeVideoSectionCopy(doc) {
    return getShowMeDocLang(doc) === "en"
      ? { label: "Official videos", icon: "▶" }
      : { label: "공식 영상", icon: "▶" };
  }

  function getShowMeTabArrowLabel(doc, direction) {
    var lang = getShowMeDocLang(doc) === "en" ? "en" : "ko";
    var labels = {
      prev: { ko: "이전 탭", en: "Previous tab" },
      next: { ko: "다음 탭", en: "Next tab" }
    };
    return labels[direction] ? labels[direction][lang] : "";
  }

  function isShowMeTabNavLocked(doc) {
    if (!doc || !doc.documentElement) return false;
    var lockUntil = Number(doc.documentElement.dataset.rpdTabNavLockUntil || 0);
    return lockUntil > Date.now();
  }

  function lockShowMeTabNav(doc) {
    if (!doc || !doc.documentElement) return;
    var unlockAt = Date.now() + 180;
    doc.documentElement.dataset.rpdTabNavLockUntil = String(unlockAt);
    global.setTimeout(function() {
      if (!doc.documentElement) return;
      var current = Number(doc.documentElement.dataset.rpdTabNavLockUntil || 0);
      if (current === unlockAt) {
        delete doc.documentElement.dataset.rpdTabNavLockUntil;
      }
    }, 220);
  }

  function ensureShowMeSharedStyles(doc) {
    if (!doc || !doc.head || doc.getElementById("rpd-showme-shared-styles")) return;

    var style = doc.createElement("style");
    style.id = "rpd-showme-shared-styles";
    style.textContent = [
      ".showme-tab-shell{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:12px;padding:12px 16px;border-bottom:1px solid rgba(255,255,255,.08);background:linear-gradient(180deg,rgba(17,18,20,.98),rgba(17,18,20,.9));backdrop-filter:blur(18px);}",
      ".showme-tab-nav{position:relative;flex:1;min-width:0;padding:0;}",
      ".showme-tab-nav::before,.showme-tab-nav::after{content:'';position:absolute;top:0;bottom:0;width:26px;pointer-events:none;z-index:2;}",
      ".showme-tab-nav::before{left:0;background:linear-gradient(90deg,rgba(17,18,20,.98),rgba(17,18,20,0));}",
      ".showme-tab-nav::after{right:0;background:linear-gradient(270deg,rgba(17,18,20,.98),rgba(17,18,20,0));}",
      ".showme-tab-arrow{width:40px;height:40px;display:grid;place-items:center;border:none;border-radius:999px;background:linear-gradient(180deg,rgba(255,255,255,.06),rgba(255,255,255,.025));box-shadow:inset 0 0 0 1px rgba(255,255,255,.08),0 8px 20px rgba(0,0,0,.22);color:rgba(237,240,246,.72);font:inherit;font-size:1.05rem;cursor:pointer;transition:transform .16s ease,background .16s ease,box-shadow .16s ease,color .16s ease,opacity .16s ease;flex-shrink:0;}",
      ".showme-tab-arrow:hover,.showme-tab-arrow:focus-visible{transform:translateY(-1px);background:linear-gradient(180deg,rgba(255,255,255,.1),rgba(255,255,255,.04));box-shadow:inset 0 0 0 1px rgba(255,255,255,.12),0 12px 24px rgba(0,0,0,.22);color:var(--text);outline:none;}",
      ".showme-tab-arrow[disabled]{opacity:.2;cursor:default;transform:none;}",
      ".showme-tab-arrow[disabled]:hover{background:linear-gradient(180deg,rgba(255,255,255,.06),rgba(255,255,255,.025));box-shadow:inset 0 0 0 1px rgba(255,255,255,.08),0 8px 20px rgba(0,0,0,.22);color:rgba(237,240,246,.72);}",
      ".tabs{display:flex !important;align-items:center;gap:4px !important;border-bottom:none !important;padding:4px !important;border-radius:22px;background:linear-gradient(180deg,rgba(255,255,255,.05),rgba(255,255,255,.024)) !important;box-shadow:inset 0 0 0 1px rgba(255,255,255,.06),inset 0 10px 24px rgba(255,255,255,.022);overflow-x:auto;scrollbar-width:none;scroll-behavior:smooth;}",
      ".tabs::-webkit-scrollbar{display:none;}",
      ".tab{position:relative;padding:11px 16px !important;border:none !important;border-bottom:none !important;border-radius:18px;background:transparent !important;color:rgba(233,236,242,.62) !important;font-size:.84rem !important;font-weight:600 !important;line-height:1.2;letter-spacing:-.01em;transition:background .18s ease,color .18s ease,box-shadow .18s ease,transform .18s ease;isolation:isolate;}",
      ".tab:hover{color:rgba(248,250,252,.92) !important;background:rgba(255,255,255,.04) !important;}",
      ".tab:focus{outline:none;}",
      ".tab:focus-visible{box-shadow:inset 0 0 0 1px rgba(255,255,255,.1);color:var(--text) !important;background:rgba(255,255,255,.05) !important;}",
      ".tab.is-active{color:#ffffff !important;background:#6f747d !important;box-shadow:inset 0 0 0 1px rgba(255,255,255,.1),0 6px 14px rgba(0,0,0,.18);text-shadow:none;}",
      ".tab.is-active::before{display:none;}",
      ".tab.is-active::after{display:none;}",
      ".tab.is-active:hover{background:#777d86 !important;}",
      ".showme-quick-actions{display:flex;align-items:flex-start;justify-content:space-between;gap:14px;margin:16px 0 0;padding:14px 16px;border-radius:18px;border:1px solid rgba(255,255,255,.08);background:linear-gradient(135deg,rgba(10,132,255,.1),rgba(255,255,255,.03));box-shadow:0 18px 38px rgba(0,0,0,.2);backdrop-filter:blur(14px);}",
      ".showme-quick-actions-copy{min-width:0;display:grid;gap:4px;}",
      ".showme-quick-actions-kicker{font-size:.66rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--key-soft);}",
      ".showme-quick-actions-title{font-size:.92rem;font-weight:600;line-height:1.35;color:var(--text);}",
      ".showme-quick-actions-meta{font-size:.8rem;line-height:1.65;color:var(--muted);max-width:42ch;}",
      ".showme-quick-action-list{display:flex;flex-wrap:wrap;justify-content:flex-end;gap:8px;}",
      ".showme-quick-link{display:inline-flex;align-items:center;gap:8px;padding:9px 12px;border:none;border-radius:999px;background:rgba(255,255,255,.055);box-shadow:inset 0 0 0 1px rgba(255,255,255,.09);color:var(--muted-strong);font:inherit;font-size:.82rem;font-weight:600;cursor:pointer;transition:transform .16s ease,background .16s ease,box-shadow .16s ease,color .16s ease;}",
      ".showme-quick-link:hover,.showme-quick-link:focus-visible{transform:translateY(-1px);background:rgba(255,255,255,.09);box-shadow:inset 0 0 0 1px rgba(255,255,255,.14);color:var(--text);outline:none;}",
      ".showme-quick-link.is-primary{background:rgba(10,132,255,.16);box-shadow:inset 0 0 0 1px rgba(10,132,255,.26);color:var(--key-soft);}",
      ".showme-quick-link-arrow{font-size:.9rem;opacity:.72;transition:transform .16s ease,opacity .16s ease;}",
      ".showme-quick-link:hover .showme-quick-link-arrow,.showme-quick-link:focus-visible .showme-quick-link-arrow{transform:translateX(2px);opacity:1;}",
      ".showme-video-ref-group{margin-top:16px;display:grid;gap:8px;}",
      ".showme-ref-section-label{font-size:.72rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);}",
      ".concept-more{margin-top:16px;padding:0 16px;border-radius:16px;border:1px solid rgba(255,255,255,.08);background:rgba(255,255,255,.025);}",
      ".concept-more summary{display:flex;align-items:center;gap:10px;padding:14px 0;color:var(--muted-strong);font-size:.82rem;font-weight:600;line-height:1.45;list-style:none;cursor:pointer;}",
      ".concept-more summary::-webkit-details-marker{display:none;}",
      ".concept-more summary::before{content:'+';display:grid;place-items:center;width:20px;height:20px;border-radius:999px;background:rgba(255,255,255,.05);box-shadow:inset 0 0 0 1px rgba(255,255,255,.1);color:var(--muted);font-size:.92rem;font-weight:500;flex-shrink:0;}",
      ".concept-more[open] summary::before{content:'-';background:rgba(10,132,255,.14);box-shadow:inset 0 0 0 1px rgba(10,132,255,.24);color:var(--key-soft);}",
      ".concept-more-body{margin:0;padding:0 0 14px 30px;color:var(--muted-strong);font-size:.84rem;line-height:1.72;}",
      "@media (max-width:640px){.showme-tab-shell{gap:8px;padding:8px 10px;}.showme-tab-arrow{width:34px;height:34px;font-size:.96rem;}.tab{padding:10px 12px !important;font-size:.8rem !important;}.showme-quick-actions{flex-direction:column;align-items:stretch;}.showme-quick-action-list{justify-content:flex-start;}.showme-quick-actions-meta{max-width:none;}.concept-more-body{padding-left:0;}}"
    ].join("");
    doc.head.appendChild(style);
  }

  function ensureShowMeTabNavigation(doc) {
    if (!doc) return;
    var tabs = doc.querySelector(".tabs");
    if (!tabs || tabs.dataset.rpdTabUiEnhanced === "true") return;
    tabs.dataset.rpdTabUiEnhanced = "true";

    var shell = doc.createElement("div");
    shell.className = "showme-tab-shell";

    var prev = doc.createElement("button");
    prev.type = "button";
    prev.className = "showme-tab-arrow is-prev";
    prev.setAttribute("aria-label", getShowMeTabArrowLabel(doc, "prev"));
    prev.setAttribute("data-tab-nav", "prev");
    prev.innerHTML = "&#x2039;";

    var nav = doc.createElement("div");
    nav.className = "showme-tab-nav";

    var next = doc.createElement("button");
    next.type = "button";
    next.className = "showme-tab-arrow is-next";
    next.setAttribute("aria-label", getShowMeTabArrowLabel(doc, "next"));
    next.setAttribute("data-tab-nav", "next");
    next.innerHTML = "&#x203A;";

    var parent = tabs.parentNode;
    if (!parent) return;
    parent.insertBefore(shell, tabs);
    shell.appendChild(prev);
    shell.appendChild(nav);
    nav.appendChild(tabs);
    shell.appendChild(next);

    prev.addEventListener("click", function(event) {
      event.preventDefault();
      event.stopPropagation();
      stepShowMeTab(doc, -1);
    });
    next.addEventListener("click", function(event) {
      event.preventDefault();
      event.stopPropagation();
      stepShowMeTab(doc, 1);
    });

    updateShowMeTabNavigation(doc);
  }

  function stepShowMeTab(doc, direction) {
    if (!doc || !direction) return;
    if (isShowMeTabNavLocked(doc)) return;
    var tabs = Array.from(doc.querySelectorAll(".tab"));
    if (!tabs.length) return;
    var currentIndex = tabs.findIndex(function(tab) { return tab.classList.contains("is-active"); });
    if (currentIndex === -1) currentIndex = 0;
    var nextIndex = Math.max(0, Math.min(tabs.length - 1, currentIndex + direction));
    if (nextIndex === currentIndex) {
      updateShowMeTabNavigation(doc);
      return;
    }
    var target = tabs[nextIndex];
    lockShowMeTabNav(doc);
    if (target && typeof target.click === "function") target.click();
  }

  function updateShowMeTabNavigation(doc) {
    if (!doc) return;
    var tabs = Array.from(doc.querySelectorAll(".tab"));
    if (!tabs.length) return;
    var currentIndex = tabs.findIndex(function(tab) { return tab.classList.contains("is-active"); });
    if (currentIndex === -1) currentIndex = 0;

    var activeTab = tabs[currentIndex];
    if (activeTab && typeof activeTab.scrollIntoView === "function") {
      try {
        activeTab.scrollIntoView({ behavior: "smooth", inline: "center", block: "nearest" });
      } catch (error) {}
    }

    var prev = doc.querySelector('.showme-tab-arrow[data-tab-nav="prev"]');
    var next = doc.querySelector('.showme-tab-arrow[data-tab-nav="next"]');
    if (prev) prev.disabled = currentIndex <= 0;
    if (next) next.disabled = currentIndex >= tabs.length - 1;
  }

  function refineShowMeConceptMore(doc) {
    if (!doc) return;
    Array.from(doc.querySelectorAll(".concept-more summary")).forEach(function(summary) {
      var text = summary.textContent ? summary.textContent.trim() : "";
      if (!text || text === "더보기" || text === "더 보기" || text === "More") {
        summary.textContent = getShowMeConceptMoreSummaryLabel(doc);
      }
    });
  }

  function injectShowMeOfficialVideos(doc) {
    var conceptPanel = doc && doc.getElementById("panel-concept");
    if (!conceptPanel || conceptPanel.querySelector(".showme-video-ref-group")) return;

    var widgetId = getShowMeWidgetId(doc);
    if (!widgetId) return;

    var entry = getShowMeEntry(widgetId);
    var videos = Array.isArray(entry.officialVideos) ? entry.officialVideos.filter(function(video) {
      return video && video.url;
    }) : [];
    if (!videos.length) return;

    var copy = getShowMeVideoSectionCopy(doc);
    var group = doc.createElement("div");
    group.className = "showme-video-ref-group";

    var label = doc.createElement("div");
    label.className = "showme-ref-section-label";
    label.textContent = copy.label;
    group.appendChild(label);

    var list = doc.createElement("div");
    list.className = "doc-ref-list";

    videos.forEach(function(video) {
      var item = doc.createElement("div");
      item.className = "doc-ref";

      var link = doc.createElement("a");
      link.href = video.url;
      link.target = "_blank";
      link.rel = "noopener";
      link.textContent = copy.icon + " " + (video.label || video.title || video.url);

      item.appendChild(link);
      list.appendChild(item);
    });

    group.appendChild(list);

    var refs = conceptPanel.querySelectorAll(".doc-ref-list, .doc-ref");
    if (refs.length) {
      refs[refs.length - 1].insertAdjacentElement("afterend", group);
    } else {
      conceptPanel.appendChild(group);
    }
  }

  function injectShowMeQuickActions(doc, hasInteractiveDemo) {
    var conceptPanel = doc.getElementById("panel-concept");
    if (!conceptPanel || conceptPanel.querySelector(".showme-quick-actions")) return;

    var actions = [];
    var hasQuiz = !!doc.querySelector('.tab[data-tab="quiz"]');
    if (hasInteractiveDemo && doc.querySelector('.tab[data-tab="visual"]')) {
      actions.push({ tab: "visual", label: getShowMeActionLabel(doc, "visual"), primary: true });
    }
    if (hasQuiz) {
      actions.push({ tab: "quiz", label: getShowMeActionLabel(doc, "quiz"), primary: !hasInteractiveDemo });
    }
    if (!actions.length) return;

    var wrap = doc.createElement("div");
    wrap.className = "showme-quick-actions";
    wrap.setAttribute("role", "region");
    wrap.setAttribute("aria-label", getShowMeActionPromptCopy(doc, hasInteractiveDemo, hasQuiz).aria);

    var copy = getShowMeActionPromptCopy(doc, hasInteractiveDemo, hasQuiz);
    var copyWrap = doc.createElement("div");
    copyWrap.className = "showme-quick-actions-copy";

    var kicker = doc.createElement("span");
    kicker.className = "showme-quick-actions-kicker";
    kicker.textContent = copy.kicker;
    copyWrap.appendChild(kicker);

    var title = doc.createElement("span");
    title.className = "showme-quick-actions-title";
    title.textContent = copy.title;
    copyWrap.appendChild(title);

    var meta = doc.createElement("span");
    meta.className = "showme-quick-actions-meta";
    meta.textContent = copy.body;
    copyWrap.appendChild(meta);

    wrap.appendChild(copyWrap);

    var list = doc.createElement("div");
    list.className = "showme-quick-action-list";

    actions.forEach(function(action) {
      var button = doc.createElement("button");
      button.type = "button";
      button.className = "showme-quick-link" + (action.primary ? " is-primary" : "");

      var label = doc.createElement("span");
      label.className = "showme-quick-link-label";
      label.textContent = action.label;
      button.appendChild(label);

      var arrow = doc.createElement("span");
      arrow.className = "showme-quick-link-arrow";
      arrow.setAttribute("aria-hidden", "true");
      arrow.textContent = "→";
      button.appendChild(arrow);

      button.addEventListener("click", function() {
        triggerShowMeTab(doc, action.tab);
      });
      list.appendChild(button);
    });

    wrap.appendChild(list);

    var intro = Array.from(conceptPanel.children).find(function(child) {
      return child.tagName === "P";
    });
    if (intro) {
      intro.insertAdjacentElement("afterend", wrap);
      return;
    }

    conceptPanel.insertBefore(wrap, conceptPanel.firstChild);
  }

  function collectShowMeIdsFromStep(step) {
    var ids = [];
    var seen = {};

    function pushId(id) {
      if (!id || seen[id]) return;
      seen[id] = true;
      ids.push(id);
    }

    if (step && step.showme) {
      (Array.isArray(step.showme) ? step.showme : [step.showme]).forEach(pushId);
    }

    if (step && Array.isArray(step.widgets)) {
      step.widgets.forEach(function(widget) {
        if (widget && widget.type === "showme" && widget.id) pushId(widget.id);
      });
    }

    return ids;
  }

  function findShowMeSupplement(widgetId) {
    var supplements = getSupplements();
    if (!supplements) return null;
    for (var key in supplements) {
      if (!Object.prototype.hasOwnProperty.call(supplements, key)) continue;
      var supplement = supplements[key];
      if (supplement.targets && supplement.targets.indexOf(widgetId) !== -1) return supplement;
    }
    return null;
  }

  function buildSupplementConfusionBlock(doc, confusionItems) {
    if (!Array.isArray(confusionItems) || confusionItems.length === 0) return null;

    var wrap = doc.createElement("div");
    wrap.style.cssText = "margin:12px 0 0;display:grid;gap:10px;";

    var title = doc.createElement("div");
    title.style.cssText = "font-size:.74rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);";
    title.textContent = "헷갈리는 포인트";
    wrap.appendChild(title);

    confusionItems.forEach(function(item) {
      var card = doc.createElement("div");
      card.style.cssText = "padding:12px 14px;border-radius:14px;background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.08);";

      var symptom = doc.createElement("div");
      symptom.style.cssText = "font-size:.84rem;font-weight:600;color:#f5f5f7;margin-bottom:6px;";
      symptom.textContent = "증상: " + item.symptom;
      card.appendChild(symptom);

      if (item.reason) {
        var reason = doc.createElement("div");
        reason.style.cssText = "font-size:.82rem;color:#d4d4d8;line-height:1.65;";
        reason.textContent = "원인: " + item.reason;
        card.appendChild(reason);
      }

      if (item.fix) {
        var fix = doc.createElement("div");
        fix.style.cssText = "margin-top:6px;font-size:.82rem;color:#8ec5ff;line-height:1.65;";
        fix.textContent = "해결: " + item.fix;
        card.appendChild(fix);
      }

      wrap.appendChild(card);
    });

    return wrap;
  }

  function buildShowMeSupplementAccordion(doc, supplement) {
    var wrap = doc.createElement("div");
    wrap.className = "showme-supplement";
    wrap.style.cssText = "margin-top:20px;border:1px solid rgba(255,255,255,.08);border-radius:14px;overflow:hidden;background:rgba(255,255,255,.02);";

    var toggle = doc.createElement("button");
    toggle.style.cssText = "display:flex;align-items:center;gap:8px;width:100%;padding:14px 16px;border:none;background:none;color:#f5f5f7;font:inherit;font-size:.86rem;font-weight:600;cursor:pointer;text-align:left;";
    toggle.textContent = "💡 " + (supplement.title || "아직 헷갈린다면?");

    var arrow = doc.createElement("span");
    arrow.style.cssText = "margin-left:auto;transition:transform .2s;font-size:.8rem;";
    arrow.textContent = "▼";
    toggle.appendChild(arrow);

    var content = doc.createElement("div");
    content.style.cssText = "display:none;padding:0 16px 16px;";

    var open = false;
    toggle.addEventListener("click", function() {
      open = !open;
      content.style.display = open ? "block" : "none";
      arrow.style.transform = open ? "rotate(180deg)" : "";
    });

    if (supplement.analogy) {
      var analogyDiv = doc.createElement("div");
      analogyDiv.style.cssText = "margin-bottom:12px;padding:12px 14px;border-radius:14px;background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.08);";

      var headlineEl = doc.createElement("div");
      headlineEl.style.cssText = "font-size:.9rem;font-weight:600;color:#f5f5f7;margin-bottom:6px;";
      headlineEl.textContent = (supplement.analogy.emoji || "") + " " + supplement.analogy.headline;
      analogyDiv.appendChild(headlineEl);

      var bodyEl = doc.createElement("div");
      bodyEl.style.cssText = "font-size:.85rem;color:#d4d4d8;line-height:1.7;";
      bodyEl.textContent = supplement.analogy.body;
      analogyDiv.appendChild(bodyEl);

      content.appendChild(analogyDiv);
    }

    if (supplement.before_after) {
      var baDiv = doc.createElement("div");
      baDiv.style.cssText = "display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px;";

      var beforeDiv = doc.createElement("div");
      beforeDiv.style.cssText = "padding:12px;border-radius:14px;background:rgba(239,68,68,.05);border:1px solid rgba(239,68,68,.14);";
      var beforeLabel = doc.createElement("div");
      beforeLabel.style.cssText = "font-size:.76rem;font-weight:600;color:#fca5a5;margin-bottom:4px;text-transform:uppercase;letter-spacing:.04em;";
      beforeLabel.textContent = "WITHOUT";
      beforeDiv.appendChild(beforeLabel);
      var beforeText = doc.createElement("div");
      beforeText.style.cssText = "font-size:.84rem;color:#d4d4d8;line-height:1.6;";
      beforeText.textContent = supplement.before_after.before;
      beforeDiv.appendChild(beforeText);

      var afterDiv = doc.createElement("div");
      afterDiv.style.cssText = "padding:12px;border-radius:14px;background:rgba(16,185,129,.05);border:1px solid rgba(16,185,129,.14);";
      var afterLabel = doc.createElement("div");
      afterLabel.style.cssText = "font-size:.76rem;font-weight:600;color:#6ee7b7;margin-bottom:4px;text-transform:uppercase;letter-spacing:.04em;";
      afterLabel.textContent = "WITH";
      afterDiv.appendChild(afterLabel);
      var afterText = doc.createElement("div");
      afterText.style.cssText = "font-size:.84rem;color:#d4d4d8;line-height:1.6;";
      afterText.textContent = supplement.before_after.after;
      afterDiv.appendChild(afterText);

      baDiv.appendChild(beforeDiv);
      baDiv.appendChild(afterDiv);
      content.appendChild(baDiv);
    }

    var confusionBlock = buildSupplementConfusionBlock(doc, supplement.confusion);
    if (confusionBlock) content.appendChild(confusionBlock);

    if (supplement.takeaway) {
      var takeawayDiv = doc.createElement("div");
      takeawayDiv.style.cssText = "margin-top:12px;padding:10px 14px;border-radius:12px;background:rgba(10,132,255,.05);border:1px solid rgba(10,132,255,.16);font-size:.84rem;color:#8ec5ff;font-weight:500;";
      takeawayDiv.textContent = "→ " + supplement.takeaway;
      content.appendChild(takeawayDiv);
    }

    wrap.appendChild(toggle);
    wrap.appendChild(content);
    return wrap;
  }

  function stripIdsFromClone(root) {
    if (!root || root.nodeType !== 1) return;
    if (root.hasAttribute("id")) root.removeAttribute("id");
    root.querySelectorAll("[id]").forEach(function(el) { el.removeAttribute("id"); });
  }

  function cloneCanvasState(sourceRoot, clonedRoot) {
    var sourceCanvases = sourceRoot.querySelectorAll("canvas");
    var clonedCanvases = clonedRoot.querySelectorAll("canvas");
    sourceCanvases.forEach(function(canvas, index) {
      var clonedCanvas = clonedCanvases[index];
      if (!clonedCanvas) return;
      clonedCanvas.width = canvas.width;
      clonedCanvas.height = canvas.height;
      if (canvas.style.width) clonedCanvas.style.width = canvas.style.width;
      if (canvas.style.height) clonedCanvas.style.height = canvas.style.height;
      try {
        var ctx = clonedCanvas.getContext("2d");
        if (ctx) ctx.drawImage(canvas, 0, 0, clonedCanvas.width, clonedCanvas.height);
      } catch (error) {}
    });
  }

  function isVisualExplainerBlock(el) {
    if (!el || el.nodeType !== 1) return false;
    if (el.matches(".scenario-nav, .before-after, .cause-effect, .scene-desc, .scene-desc-box, .scenario-desc")) return true;
    var id = el.id || "";
    return /Desc$/.test(id) || id === "xr-scene-desc" || id.indexOf("scene-desc") !== -1;
  }

  function isVisualDescriptionBlock(el) {
    if (!el || el.nodeType !== 1) return false;
    if (el.matches(".cause-effect, .scene-desc, .scene-desc-box, .scenario-desc")) return true;
    var id = el.id || "";
    return /Desc$/.test(id) || id === "xr-scene-desc" || id.indexOf("scene-desc") !== -1;
  }

  function hasLegacyInteractiveDemo(visualPanel) {
    if (!visualPanel) return false;
    return !!visualPanel.querySelector(".before-after canvas, .before-after svg, canvas, svg");
  }

  function buildConceptVisualizationSummary(doc, visualPanel) {
    var desc = visualPanel.querySelector(".scene-desc, .scene-desc-box, .scenario-desc, #scenarioDesc, #sceneDesc, #compDesc, #boolDesc, #xr-scene-desc, [id*='scene-desc'], [id$='Desc'], [id$='desc']");
    var beforeAfter = visualPanel.querySelector(".before-after");
    var causeEffect = visualPanel.querySelector(".cause-effect");
    var activeScenario = visualPanel.querySelector(".scenario-btn.active, .scenario-btn.is-active");
    if (!desc && !beforeAfter && !causeEffect) return null;

    var wrap = doc.createElement("div");
    wrap.className = "showme-concept-visual";
    wrap.style.cssText = "margin:20px 0 0;padding:16px 18px;border-radius:14px;border:1px solid rgba(255,255,255,.08);background:rgba(255,255,255,.02);";

    var title = doc.createElement("div");
    title.className = "section-divider";
    title.style.marginTop = "0";
    title.textContent = "개념 이해 시각화";
    wrap.appendChild(title);

    if (activeScenario) {
      var chip = doc.createElement("div");
      chip.style.cssText = "display:inline-flex;align-items:center;padding:0;border:none;background:none;color:var(--muted);font-size:.72rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;margin-bottom:10px;";
      chip.textContent = activeScenario.textContent.trim();
      wrap.appendChild(chip);
    }

    if (desc && desc.textContent.trim()) {
      var descEl = doc.createElement("p");
      descEl.style.cssText = "margin:0 0 12px;font-size:.86rem;line-height:1.7;color:var(--muted-strong);";
      descEl.textContent = desc.textContent.trim();
      wrap.appendChild(descEl);
    }

    if (beforeAfter) {
      var beforeAfterClone = beforeAfter.cloneNode(true);
      stripIdsFromClone(beforeAfterClone);
      cloneCanvasState(beforeAfter, beforeAfterClone);
      wrap.appendChild(beforeAfterClone);
    }

    if (causeEffect && causeEffect.children.length) {
      var causeEffectClone = causeEffect.cloneNode(true);
      stripIdsFromClone(causeEffectClone);
      causeEffectClone.style.marginTop = beforeAfter ? "12px" : "0";
      wrap.appendChild(causeEffectClone);
    }

    return wrap;
  }

  function normalizeShowMeDocument(doc) {
    if (!doc || !doc.body || doc.body.dataset.showmeLayoutNormalized === "true") return;

    var conceptPanel = doc.getElementById("panel-concept");
    var visualPanel = doc.getElementById("panel-visual");
    var visualTab = doc.querySelector('.tab[data-tab="visual"]');
    var quizTab = doc.querySelector('.tab[data-tab="quiz"]');
    if (!conceptPanel || !visualPanel) return;

    ensureShowMeSharedStyles(doc);
    ensureShowMeTabNavigation(doc);
    bindShowMeTabs(doc);
    refineShowMeConceptMore(doc);

    var hasDedicatedInteractiveDemo = !!visualPanel.querySelector(".demo-wrap");
    var hasLegacyComparisonDemo = !hasDedicatedInteractiveDemo && hasLegacyInteractiveDemo(visualPanel);
    var hasInteractiveDemo = hasDedicatedInteractiveDemo || hasLegacyComparisonDemo;
    var hasVisualExplainer = Array.from(visualPanel.children).some(isVisualExplainerBlock);

    if (hasInteractiveDemo && visualTab) {
      visualTab.textContent = getShowMeActionLabel(doc, "visual");
    }
    if (quizTab) {
      quizTab.textContent = getShowMeActionLabel(doc, "quiz");
    }

    if (hasInteractiveDemo && hasVisualExplainer && !conceptPanel.querySelector(".showme-concept-visual")) {
      var summary = buildConceptVisualizationSummary(doc, visualPanel);
      if (summary) {
        var anchor = conceptPanel.querySelector(".shortcut-list, .doc-ref-list, .doc-ref");
        if (anchor) conceptPanel.insertBefore(summary, anchor);
        else conceptPanel.appendChild(summary);

        Array.from(visualPanel.children).forEach(function(child) {
          if (!isVisualExplainerBlock(child)) return;
          if (hasDedicatedInteractiveDemo || isVisualDescriptionBlock(child)) {
            child.style.display = "none";
          }
        });
      }
    }

    injectShowMeOfficialVideos(doc);
    injectShowMeQuickActions(doc, hasInteractiveDemo);
    doc.body.dataset.showmeLayoutNormalized = "true";
  }

  function normalizeShowMeLayout(iframe) {
    try {
      normalizeShowMeDocument(iframe && iframe.contentDocument);
    } catch (error) {}
  }

  function normalizeStandaloneShowMeLayout(doc) {
    try {
      normalizeShowMeDocument(doc || (typeof document !== "undefined" ? document : null));
    } catch (error) {}
  }

  function injectShowMeSupplement(iframe, widgetId) {
    try {
      var doc = iframe.contentDocument;
      if (!doc) return;
      var supplement = findShowMeSupplement(widgetId);
      if (!supplement) return;
      var panel = doc.getElementById("panel-concept");
      if (!panel || panel.querySelector(".showme-supplement")) return;
      panel.appendChild(buildShowMeSupplementAccordion(doc, supplement));
    } catch (error) {}
  }

  global.getShowMeCategoryOrder = getShowMeCategoryOrder;
  global.getShowMeManualSectionOrder = getShowMeManualSectionOrder;
  global.getShowMeManualSectionId = getShowMeManualSectionId;
  global.getShowMeEntry = getShowMeEntry;
  global.getShowMeDifficultyLabel = getShowMeDifficultyLabel;
  global.getShowMeTooltipText = getShowMeTooltipText;
  global.collectShowMeIdsFromStep = collectShowMeIdsFromStep;
  global.findShowMeSupplement = findShowMeSupplement;
  global.buildShowMeSupplementAccordion = buildShowMeSupplementAccordion;
  global.normalizeShowMeLayout = normalizeShowMeLayout;
  global.normalizeStandaloneShowMeLayout = normalizeStandaloneShowMeLayout;
  global.injectShowMeSupplement = injectShowMeSupplement;
})(typeof window !== "undefined" ? window : globalThis);
