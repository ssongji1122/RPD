(function(global) {
  var DIFFICULTY_LABELS = {
    beginner: "입문",
    intermediate: "중급",
    advanced: "심화"
  };

  function getCatalog() {
    return global.SHOWME_CATALOG || {};
  }

  function getShowMeCategoryOrder() {
    var catalog = getCatalog();
    return Array.isArray(catalog.categoryOrder) && catalog.categoryOrder.length
      ? catalog.categoryOrder.slice()
      : ["전체", "기타"];
  }

  function getShowMeEntry(id) {
    var registry = global.SHOWME_REGISTRY || {};
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
    if (typeof global.SHOWME_SUPPLEMENTS === "undefined") return null;
    for (var key in global.SHOWME_SUPPLEMENTS) {
      if (!Object.prototype.hasOwnProperty.call(global.SHOWME_SUPPLEMENTS, key)) continue;
      var supplement = global.SHOWME_SUPPLEMENTS[key];
      if (supplement.targets && supplement.targets.indexOf(widgetId) !== -1) return supplement;
    }
    return null;
  }

  function buildSupplementConfusionBlock(doc, confusionItems) {
    if (!Array.isArray(confusionItems) || confusionItems.length === 0) return null;

    var wrap = doc.createElement("div");
    wrap.style.cssText = "margin:12px 0 0;display:grid;gap:10px;";

    var title = doc.createElement("div");
    title.style.cssText = "font-size:.82rem;font-weight:700;color:#fcd34d;";
    title.textContent = "헷갈리는 포인트";
    wrap.appendChild(title);

    confusionItems.forEach(function(item) {
      var card = doc.createElement("div");
      card.style.cssText = "padding:12px 14px;border-radius:12px;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);";

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
    wrap.style.cssText = "margin-top:20px;border:1px solid rgba(245,158,11,.18);border-radius:18px;overflow:hidden;background:rgba(245,158,11,.04);";

    var toggle = doc.createElement("button");
    toggle.style.cssText = "display:flex;align-items:center;gap:8px;width:100%;padding:14px 16px;border:none;background:none;color:#fbbf24;font:inherit;font-size:.88rem;font-weight:600;cursor:pointer;text-align:left;";
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
      analogyDiv.style.cssText = "margin-bottom:12px;padding:12px 14px;border-radius:12px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.06);";

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
      beforeDiv.style.cssText = "padding:12px;border-radius:12px;background:rgba(239,68,68,.06);border:1px solid rgba(239,68,68,.15);";
      var beforeLabel = doc.createElement("div");
      beforeLabel.style.cssText = "font-size:.76rem;font-weight:600;color:#fca5a5;margin-bottom:4px;text-transform:uppercase;letter-spacing:.04em;";
      beforeLabel.textContent = "WITHOUT";
      beforeDiv.appendChild(beforeLabel);
      var beforeText = doc.createElement("div");
      beforeText.style.cssText = "font-size:.84rem;color:#d4d4d8;line-height:1.6;";
      beforeText.textContent = supplement.before_after.before;
      beforeDiv.appendChild(beforeText);

      var afterDiv = doc.createElement("div");
      afterDiv.style.cssText = "padding:12px;border-radius:12px;background:rgba(16,185,129,.06);border:1px solid rgba(16,185,129,.15);";
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
      takeawayDiv.style.cssText = "margin-top:12px;padding:10px 14px;border-radius:12px;background:rgba(10,132,255,.08);border:1px solid rgba(10,132,255,.18);font-size:.86rem;color:#8ec5ff;font-weight:500;";
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
    wrap.style.cssText = "margin:20px 0 0;padding:16px 18px;border-radius:18px;border:1px solid rgba(10,132,255,.18);background:rgba(255,255,255,.02);";

    var title = doc.createElement("div");
    title.className = "section-divider";
    title.style.marginTop = "0";
    title.textContent = "개념 이해 시각화";
    wrap.appendChild(title);

    if (activeScenario) {
      var chip = doc.createElement("div");
      chip.style.cssText = "display:inline-flex;align-items:center;padding:4px 10px;border-radius:999px;background:rgba(10,132,255,.12);color:#8ec5ff;font-size:.76rem;font-weight:600;margin-bottom:10px;";
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

  function normalizeShowMeLayout(iframe) {
    try {
      var doc = iframe.contentDocument;
      if (!doc || doc.body.dataset.showmeLayoutNormalized === "true") return;

      var conceptPanel = doc.getElementById("panel-concept");
      var visualPanel = doc.getElementById("panel-visual");
      var visualTab = doc.querySelector('.tab[data-tab="visual"]');
      if (!conceptPanel || !visualPanel) return;

      var hasDedicatedInteractiveDemo = !!visualPanel.querySelector(".demo-wrap");
      var hasLegacyComparisonDemo = !hasDedicatedInteractiveDemo && hasLegacyInteractiveDemo(visualPanel);
      var hasInteractiveDemo = hasDedicatedInteractiveDemo || hasLegacyComparisonDemo;
      var hasVisualExplainer = Array.from(visualPanel.children).some(isVisualExplainerBlock);

      if (hasInteractiveDemo && visualTab) {
        visualTab.textContent = "interaction";
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

      doc.body.dataset.showmeLayoutNormalized = "true";
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
  global.getShowMeEntry = getShowMeEntry;
  global.getShowMeDifficultyLabel = getShowMeDifficultyLabel;
  global.getShowMeTooltipText = getShowMeTooltipText;
  global.collectShowMeIdsFromStep = collectShowMeIdsFromStep;
  global.findShowMeSupplement = findShowMeSupplement;
  global.buildShowMeSupplementAccordion = buildShowMeSupplementAccordion;
  global.normalizeShowMeLayout = normalizeShowMeLayout;
  global.injectShowMeSupplement = injectShowMeSupplement;
})(typeof window !== "undefined" ? window : globalThis);
