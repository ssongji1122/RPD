(function(win) {
  function getLanguage() {
    if (win.RPDI18n && typeof win.RPDI18n.getLanguage === "function") {
      return win.RPDI18n.getLanguage();
    }
    return win.document && win.document.documentElement
      ? (win.document.documentElement.getAttribute("data-lang") || win.document.documentElement.lang || "ko")
      : "ko";
  }

  function resolvePresetName(explicitPresetName) {
    if (typeof explicitPresetName === "string" && explicitPresetName.trim()) {
      return explicitPresetName.trim();
    }
    try {
      var searchPreset = new URLSearchParams(win.location.search).get("preset");
      if (typeof searchPreset === "string" && searchPreset.trim()) {
        return searchPreset.trim();
      }
    } catch (error) {
      // Ignore invalid location values and keep falling back.
    }
    if (win.RPDWeekUI && typeof win.RPDWeekUI.getState === "function") {
      var state = win.RPDWeekUI.getState();
      if (state && state.presetName && (state.explicitPreset || (state.config && state.presetName !== state.config.defaultPreset))) {
        return state.presetName;
      }
    }
    return "";
  }

  function withPreset(href, explicitPresetName) {
    if (!href || href.charAt(0) === "#") return href;
    if (!explicitPresetName && win.RPDWeekUI && typeof win.RPDWeekUI.withPreset === "function") {
      return win.RPDWeekUI.withPreset(href);
    }
    try {
      var url = new URL(href, win.location.href);
      if (url.origin !== win.location.origin) return href;
      var presetName = resolvePresetName(explicitPresetName);
      if (presetName) url.searchParams.set("preset", presetName);
      else url.searchParams.delete("preset");
      return url.pathname.replace(/^\//, "") + url.search + url.hash;
    } catch (error) {
      return href;
    }
  }

  function getPublicLinks(options) {
    var opts = options || {};
    var lang = opts.lang || getLanguage();
    var presetName = opts.presetName || "";
    var isKo = lang === "ko";
    return {
      home: {
        href: withPreset("index.html", presetName),
        label: isKo ? "홈" : "Home"
      },
      collection: {
        href: withPreset("inha.html?panel=weeks", presetName),
        label: isKo ? "인하대 수업" : "Inha RPD"
      },
      library: {
        href: withPreset("library.html", presetName),
        label: isKo ? "카드 라이브러리" : "Card Library"
      },
      shortcuts: {
        href: withPreset("shortcuts.html", presetName),
        label: isKo ? "단축키 DB" : "Shortcut DB"
      },
      admin: {
        href: withPreset("admin.html", presetName),
        label: isKo ? "관리자" : "Admin"
      }
    };
  }

  var THEME_KEY = win.RPD_KEYS.THEME;

  function toggleTheme() {
    if (!win.document || !win.document.documentElement) return "";
    var root = win.document.documentElement;
    var current = root.getAttribute("data-theme");
    var next = current === "light" ? "" : "light";
    if (next) {
      root.setAttribute("data-theme", next);
      win.localStorage.setItem(THEME_KEY, next);
    } else {
      root.removeAttribute("data-theme");
      win.localStorage.removeItem(THEME_KEY);
    }
    return next;
  }

  function bindThemeToggle(node) {
    if (!node || node.dataset.themeBound === "1") return;
    node.dataset.themeBound = "1";
    node.addEventListener("click", function() {
      toggleTheme();
    });
  }

  win.RPDAppShell = {
    getLanguage: getLanguage,
    withPreset: withPreset,
    getPublicLinks: getPublicLinks,
    toggleTheme: toggleTheme,
    bindThemeToggle: bindThemeToggle
  };
}(window));
