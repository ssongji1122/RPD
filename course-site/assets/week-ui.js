(function(win) {
  var DEFAULT_CONFIG = {
    version: 1,
    defaultPreset: "inha-rpd",
    presets: {
      base: {
        labels: {
          school: { ko: "인하대학교", en: "Inha University" },
          program: { ko: "Robot Product Design", en: "Robot Product Design" },
          heroEyebrow: { ko: "Blender Archive · 인하대학교", en: "Blender Archive · Inha University" },
          summaryTitle: { ko: "이번 주", en: "This week" },
          courseSnapshotTitle: { ko: "수업 스냅샷", en: "Course snapshot" },
          courseSnapshotWeeks: { ko: "총 주차", en: "Weeks" },
          courseSnapshotActive: { ko: "현재 주차", en: "Current week" },
          metricPractice: { ko: "실습", en: "practice" },
          metricShowMe: { ko: "Show Me", en: "Show Me" },
          metricTasks: { ko: "체크", en: "tasks" },
          metricRefs: { ko: "참고", en: "refs" }
        },
        courseHero: {
          snapshotItems: ["weeks", "active"],
          emphasis: "active"
        },
        weekCard: {
          metrics: ["practice", "showme", "tasks"],
          previewSource: "topics",
          previewMaxItems: 3,
          activePreviewMaxItems: 5,
          highlightMode: "status"
        },
        weekHero: {
          iconMode: "week",
          subtitleMode: "subtitle",
          subtitleMetrics: ["practice", "tasks", "showme"],
          showUtilityRow: false
        },
        weekSummary: {
          showProgress: true,
          itemSource: "topics",
          maxItems: 8,
          desktopColumns: 2,
          mobileColumns: 1
        }
      },
      "inha-rpd": {
        extends: "base"
      }
    }
  };

  var state = {
    config: DEFAULT_CONFIG,
    presetName: DEFAULT_CONFIG.defaultPreset,
    preset: null,
    explicitPreset: false,
    ready: false
  };
  var loadPromise = null;

  function isPlainObject(value) {
    return Boolean(value) && Object.prototype.toString.call(value) === "[object Object]";
  }

  function cloneValue(value) {
    if (Array.isArray(value)) {
      return value.map(cloneValue);
    }
    if (isPlainObject(value)) {
      var next = {};
      Object.keys(value).forEach(function(key) {
        next[key] = cloneValue(value[key]);
      });
      return next;
    }
    return value;
  }

  function mergeConfig(base, extra) {
    var target = cloneValue(base);
    if (!isPlainObject(extra)) return target;
    Object.keys(extra).forEach(function(key) {
      var nextValue = extra[key];
      if (Array.isArray(nextValue)) {
        target[key] = nextValue.slice();
        return;
      }
      if (isPlainObject(nextValue) && isPlainObject(target[key])) {
        target[key] = mergeConfig(target[key], nextValue);
        return;
      }
      target[key] = cloneValue(nextValue);
    });
    return target;
  }

  function resolvePreset(config, presetName, seen) {
    var presets = (config && config.presets) || {};
    var name = presetName && presets[presetName] ? presetName : (config.defaultPreset || DEFAULT_CONFIG.defaultPreset);
    var preset = presets[name] || {};
    var nextSeen = seen || {};
    if (!preset.extends || nextSeen[name]) {
      return mergeConfig({}, preset);
    }
    nextSeen[name] = true;
    var parent = resolvePreset(config, preset.extends, nextSeen);
    var child = mergeConfig({}, preset);
    delete child.extends;
    return mergeConfig(parent, child);
  }

  function localize(value, lang, fallback) {
    if (typeof value === "string") return value;
    if (!isPlainObject(value)) return fallback || "";
    return value[lang] || value.en || value.ko || fallback || "";
  }

  function readRequestedPreset() {
    try {
      return new URLSearchParams(win.location.search).get("preset") || "";
    } catch (error) {
      return "";
    }
  }

  function applyState(rawConfig, requestedPreset) {
    var config = mergeConfig(DEFAULT_CONFIG, rawConfig || {});
    var presetName = requestedPreset && config.presets && config.presets[requestedPreset]
      ? requestedPreset
      : (config.defaultPreset || DEFAULT_CONFIG.defaultPreset);
    state.config = config;
    state.presetName = presetName;
    state.preset = resolvePreset(config, presetName);
    state.explicitPreset = Boolean(requestedPreset);
    state.ready = true;
    if (win.document && win.document.documentElement) {
      win.document.documentElement.setAttribute("data-ui-preset", presetName);
    }
    return getState();
  }

  function getState() {
    if (!state.preset) {
      state.preset = resolvePreset(state.config, state.presetName);
    }
    return {
      config: state.config,
      presetName: state.presetName,
      preset: state.preset,
      explicitPreset: state.explicitPreset,
      ready: state.ready
    };
  }

  function init(options) {
    var opts = options || {};
    var requestedPreset = opts.requestedPreset || readRequestedPreset();
    if (loadPromise) return loadPromise;
    loadPromise = fetch(opts.url || "data/week-ui.json", { credentials: "same-origin" })
      .then(function(response) {
        if (!response.ok) throw new Error("Failed to load week UI config");
        return response.json();
      })
      .catch(function() {
        return null;
      })
      .then(function(rawConfig) {
        return applyState(rawConfig, requestedPreset);
      })
      .finally(function() {
        loadPromise = null;
      });
    return loadPromise;
  }

  function shouldCarryPreset() {
    return state.explicitPreset || state.presetName !== (state.config.defaultPreset || DEFAULT_CONFIG.defaultPreset);
  }

  function withPreset(href) {
    if (!href || href.charAt(0) === "#") return href;
    try {
      var url = new URL(href, win.location.href);
      if (url.origin !== win.location.origin) return href;
      if (shouldCarryPreset()) url.searchParams.set("preset", state.presetName);
      else url.searchParams.delete("preset");
      return url.pathname + url.search + url.hash;
    } catch (error) {
      return href;
    }
  }

  win.RPDWeekUI = {
    init: init,
    getState: getState,
    getPreset: function() { return getState().preset; },
    getPresetName: function() { return getState().presetName; },
    localize: function(value, lang, fallback) {
      return localize(value, lang || ((win.RPDI18n && win.RPDI18n.getLanguage && win.RPDI18n.getLanguage()) || "ko"), fallback);
    },
    withPreset: withPreset
  };
}(window));
