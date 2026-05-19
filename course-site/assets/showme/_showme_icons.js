// ============================================================
// ShowMe Lucide icon bundle — inline SVG for new SSoT cards
// ============================================================
// Phase 2+ cards store icon as Lucide kebab-case name.
// Legacy 79 cards keep emoji strings.
//
// Consumer pattern (library.html, week.html, _helpers.js):
//   window.SHOWME_ICONS.apply(iconElement, iconName);
//
// SVG source: Lucide v0.469 (https://lucide.dev), 24x24, stroke 2,
// stroke-linecap/linejoin round, currentColor fill. All path data
// is static and authored in this file — no untrusted input.

(function () {
  // Path data per Lucide icon name. Static, author-controlled.
  var paths = {
    "folder-tree": [
      "M20 10a1 1 0 0 0 1-1V6a1 1 0 0 0-1-1h-2.5a1 1 0 0 1-.8-.4l-.9-1.2A1 1 0 0 0 15 3h-2a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1Z",
      "M20 21a1 1 0 0 0 1-1v-3a1 1 0 0 0-1-1h-2.9a1 1 0 0 1-.88-.55l-.42-.85a1 1 0 0 0-.92-.6H13a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1Z",
      "M3 5a2 2 0 0 0 2 2h3",
      "M3 3v13a2 2 0 0 0 2 2h3",
    ],
    "layers": [
      "m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z",
      "m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65",
      "m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65",
    ],
    "sparkles": [
      "M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0Z",
      "M20 3v4",
      "M22 5h-4",
      "M4 17v2",
      "M5 18H3",
    ],
    "combine": [
      "M10 18H5a3 3 0 0 1-3-3v-1",
      "M14 2a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2",
      "M20 2a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2",
      "m7 21 3-3-3-3",
    ],
    "git-merge": [
      "M6 21V9a9 9 0 0 0 9 9",
    ],
    "copy-plus": [
      "M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2",
    ],
    "flip-horizontal": [
      "M8 3H5a2 2 0 0 0-2 2v14c0 1.1.9 2 2 2h3",
      "M16 3h3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-3",
      "M12 20v2",
      "M12 14v2",
      "M12 8v2",
      "M12 2v2",
    ],
    "archive-restore": [
      "M4 8v11a2 2 0 0 0 2 2h2",
      "M20 8v11a2 2 0 0 1-2 2h-2",
      "m9 15 3-3 3 3",
      "M12 12v9",
    ],
  };

  // Extra shapes per icon (rects, circles, lines) — kept separate from
  // path[] to avoid mixing element types in one array.
  var shapes = {
    "combine": [
      { tag: "rect", attrs: { x: "14", y: "14", width: "8", height: "8", rx: "2" } },
      { tag: "rect", attrs: { x: "2", y: "2", width: "8", height: "8", rx: "2" } },
    ],
    "git-merge": [
      { tag: "circle", attrs: { cx: "18", cy: "18", r: "3" } },
      { tag: "circle", attrs: { cx: "6", cy: "6", r: "3" } },
    ],
    "copy-plus": [
      { tag: "line", attrs: { x1: "15", y1: "12", x2: "15", y2: "18" } },
      { tag: "line", attrs: { x1: "12", y1: "15", x2: "18", y2: "15" } },
      { tag: "rect", attrs: { width: "14", height: "14", x: "8", y: "8", rx: "2", ry: "2" } },
    ],
    "archive-restore": [
      { tag: "rect", attrs: { width: "20", height: "5", x: "2", y: "3", rx: "1" } },
    ],
  };

  var SVG_NS = "http://www.w3.org/2000/svg";

  function makeSvg(name) {
    var svg = document.createElementNS(SVG_NS, "svg");
    svg.setAttribute("width", "20");
    svg.setAttribute("height", "20");
    svg.setAttribute("viewBox", "0 0 24 24");
    svg.setAttribute("fill", "none");
    svg.setAttribute("stroke", "currentColor");
    svg.setAttribute("stroke-width", "2");
    svg.setAttribute("stroke-linecap", "round");
    svg.setAttribute("stroke-linejoin", "round");
    svg.setAttribute("aria-hidden", "true");

    (shapes[name] || []).forEach(function (shape) {
      var el = document.createElementNS(SVG_NS, shape.tag);
      Object.keys(shape.attrs).forEach(function (k) {
        el.setAttribute(k, shape.attrs[k]);
      });
      svg.appendChild(el);
    });

    (paths[name] || []).forEach(function (d) {
      var p = document.createElementNS(SVG_NS, "path");
      p.setAttribute("d", d);
      svg.appendChild(p);
    });

    return svg;
  }

  function isLucideName(s) {
    return typeof s === "string" && /^[a-z][a-z0-9-]+$/.test(s);
  }

  function apply(el, icon) {
    if (!el) return;
    // Clear existing content via DOM API
    while (el.firstChild) el.removeChild(el.firstChild);

    if (icon && isLucideName(icon) && paths[icon]) {
      el.appendChild(makeSvg(icon));
      return;
    }
    // Fallback: legacy emoji string or default
    el.appendChild(document.createTextNode(icon || "📖"));
  }

  function has(name) {
    return Object.prototype.hasOwnProperty.call(paths, name);
  }

  // Serialize an SVG element to an HTML string for innerHTML-only callers
  // (e.g. week.html renderShowMeIcon). Path data is static and author-
  // controlled — no untrusted input enters this path.
  function htmlString(name) {
    if (!has(name)) return "";
    var svg = makeSvg(name);
    return new XMLSerializer().serializeToString(svg);
  }

  window.SHOWME_ICONS = {
    apply: apply,
    has: has,
    htmlString: htmlString,
    isLucideName: isLucideName,
    names: Object.keys(paths),
  };
})();
