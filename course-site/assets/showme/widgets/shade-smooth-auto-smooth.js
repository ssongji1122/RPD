// ============================================================
// Widget: shade-smooth-auto-smooth
// ============================================================
// Interactive angle slider showing Flat / Shade Smooth / Auto Smooth
// (with angle threshold) side by side on a stylised mesh cross-section.
// SVG only, no live 3D.

(function () {
  var SVG_NS = "http://www.w3.org/2000/svg";

  function el(tag, attrs) {
    var node = document.createElementNS(SVG_NS, tag);
    if (attrs) Object.keys(attrs).forEach(function (k) { node.setAttribute(k, attrs[k]); });
    return node;
  }

  function htmlEl(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text != null) node.textContent = text;
    return node;
  }

  function clearChildren(node) {
    while (node.firstChild) node.removeChild(node.firstChild);
  }

  // Build a 16-segment 2D arc (semi-circle) representing a faceted
  // mesh cross-section. Apex angle between adjacent facets is roughly
  // (180° / 16) ≈ 11.25°.
  // mode: "flat" | "smooth" | "auto"
  // threshold: degrees — only used in "auto" mode
  var FACET_COUNT = 16;
  var FACET_ANGLE_DEG = 180 / FACET_COUNT;

  function renderMesh(svg, mode, threshold) {
    clearChildren(svg);
    svg.setAttribute("viewBox", "0 0 220 140");

    svg.appendChild(el("rect", { x: "0", y: "0", width: "220", height: "140", fill: "#17181a", rx: "8" }));

    var cx = 110, cy = 110, r = 80;

    // Compute vertex positions on the semi-arc
    var pts = [];
    for (var i = 0; i <= FACET_COUNT; i++) {
      var t = i / FACET_COUNT; // 0..1
      var ang = Math.PI * (1 - t); // π (left) → 0 (right), top semi-circle
      pts.push({ x: cx + r * Math.cos(ang), y: cy - r * Math.sin(ang) });
    }

    // Determine which facet seams are "sharp" (drawn) per mode.
    // flat: all seams sharp
    // smooth: no seams sharp
    // auto: seams sharp only if facet angle > threshold
    function isSeamSharp(seamIdx) {
      if (mode === "flat") return true;
      if (mode === "smooth") return false;
      // auto: facet angle is constant FACET_ANGLE_DEG; threshold gate
      return FACET_ANGLE_DEG > threshold;
    }

    // For a curved appearance, in smooth/auto-with-no-seams cases, draw
    // a smooth quadratic spline through the points. Otherwise draw
    // straight line segments and seam ticks at each vertex.
    var allSharp = pts.length >= 2 && Array.from({ length: FACET_COUNT }, function (_, i) { return isSeamSharp(i); }).every(Boolean);
    var allSmooth = pts.length >= 2 && Array.from({ length: FACET_COUNT }, function (_, i) { return isSeamSharp(i); }).every(function (v) { return !v; });

    if (allSmooth) {
      // Draw single smooth curve (the underlying geometry is still faceted,
      // but shading hides facets entirely).
      var d = "M" + pts[0].x + " " + pts[0].y;
      for (var j = 1; j < pts.length; j++) {
        d += " L" + pts[j].x + " " + pts[j].y;
      }
      svg.appendChild(el("path", {
        d: d,
        fill: "none",
        stroke: "#8ec5ff",
        "stroke-width": "2.4",
        "stroke-linejoin": "round",
        "stroke-linecap": "round",
      }));
    } else {
      // Draw faceted polyline; angled corners visible at each vertex.
      var d2 = "M" + pts[0].x + " " + pts[0].y;
      for (var k = 1; k < pts.length; k++) {
        d2 += " L" + pts[k].x + " " + pts[k].y;
      }
      svg.appendChild(el("path", {
        d: d2,
        fill: "none",
        stroke: "#8ec5ff",
        "stroke-width": "2",
        "stroke-linejoin": "miter",
        "stroke-linecap": "butt",
      }));
      // Seam ticks: short orange marks at each internal vertex if sharp.
      for (var s = 0; s < FACET_COUNT - 1; s++) {
        if (!isSeamSharp(s)) continue;
        var p = pts[s + 1];
        // Compute outward normal direction at this vertex
        var ang2 = Math.atan2(cy - p.y, p.x - cx);
        var nx = Math.cos(ang2);
        var ny = -Math.sin(ang2);
        svg.appendChild(el("line", {
          x1: String(p.x + nx * 2),
          y1: String(p.y + ny * 2),
          x2: String(p.x + nx * 8),
          y2: String(p.y + ny * 8),
          stroke: "#f59e0b",
          "stroke-width": "1.2",
        }));
      }
    }

    // Base (ground line)
    svg.appendChild(el("line", {
      x1: "20", y1: "110", x2: "200", y2: "110",
      stroke: "#3b3d42", "stroke-width": "1",
    }));

    // Light source indicator (top-right)
    svg.appendChild(el("circle", { cx: "190", cy: "20", r: "5", fill: "#fbbf24" }));
    var rays = [
      [185, 24, 170, 38],
      [192, 26, 180, 42],
      [198, 24, 200, 44],
    ];
    rays.forEach(function (r) {
      svg.appendChild(el("line", {
        x1: String(r[0]), y1: String(r[1]),
        x2: String(r[2]), y2: String(r[3]),
        stroke: "#fbbf24", "stroke-width": "0.8", opacity: "0.6",
      }));
    });

    // Mode label inside SVG
    var label = el("text", {
      x: "12", y: "20",
      fill: "#cbd5e1",
      "font-size": "11",
      "font-family": "system-ui,-apple-system,sans-serif",
      "font-weight": "600",
    });
    label.textContent = (
      mode === "flat" ? "Flat" :
      mode === "smooth" ? "Shade Smooth" :
      "Auto Smooth · " + threshold.toFixed(0) + "°"
    );
    svg.appendChild(label);
  }

  function renderColumn(mode, getThreshold) {
    var col = htmlEl("div", "shade-col");

    var svg = document.createElementNS(SVG_NS, "svg");
    svg.setAttribute("width", "100%");
    svg.setAttribute("height", "auto");
    svg.setAttribute("class", "shade-result");
    renderMesh(svg, mode, getThreshold());
    col.appendChild(svg);

    var caption = htmlEl("div", "shade-caption",
      mode === "flat" ? "모든 면 각진 그대로" :
      mode === "smooth" ? "전체를 부드럽게 보간" :
      "각도가 작은 모서리는 부드럽게, 큰 건 살림"
    );
    col.appendChild(caption);

    return { col: col, svg: svg, mode: mode };
  }

  function injectStyles() {
    if (document.getElementById("shade-smooth-widget-styles")) return;
    var style = document.createElement("style");
    style.id = "shade-smooth-widget-styles";
    style.textContent = (
      ".shade-smooth-widget{display:flex;flex-direction:column;gap:18px;max-width:780px;margin:0 auto;padding:8px 0}" +
      ".shade-smooth-widget .shade-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px}" +
      ".shade-smooth-widget .shade-col{display:flex;flex-direction:column;gap:8px;padding:12px;border-radius:10px;border:1px solid var(--line,rgba(255,255,255,.08));background:var(--surface,#17181a)}" +
      ".shade-smooth-widget .shade-result{display:block;width:100%;border-radius:6px}" +
      ".shade-smooth-widget .shade-caption{font-size:.82rem;color:var(--muted-strong,#d4d4d8);text-align:center;line-height:1.5;word-break:keep-all}" +
      ".shade-smooth-widget .shade-control{display:flex;flex-direction:column;gap:6px;padding:14px;border-radius:10px;border:1px solid var(--line,rgba(255,255,255,.08));background:var(--surface,#17181a)}" +
      ".shade-smooth-widget .shade-control-label{display:flex;justify-content:space-between;align-items:baseline;color:var(--muted-strong,#d4d4d8);font-size:.85rem}" +
      ".shade-smooth-widget .shade-control-value{color:var(--key-soft,#8ec5ff);font-weight:700;font-variant-numeric:tabular-nums}" +
      ".shade-smooth-widget input[type=range]{width:100%;accent-color:var(--key,#0a84ff)}" +
      ".shade-smooth-widget .shade-note{margin:0;color:var(--muted,#a1a1aa);font-size:.85rem;line-height:1.6;word-break:keep-all}"
    );
    document.head.appendChild(style);
  }

  function mount(target) {
    clearChildren(target);
    injectStyles();

    var state = { threshold: 30 };
    function get() { return state.threshold; }

    var container = htmlEl("div", "shade-smooth-widget");

    var control = htmlEl("div", "shade-control");
    var controlLabel = htmlEl("label", "shade-control-label");
    controlLabel.appendChild(htmlEl("span", null, "Auto Smooth 각도 임계값"));
    var valueSpan = htmlEl("span", "shade-control-value", state.threshold + "°");
    controlLabel.appendChild(valueSpan);
    control.appendChild(controlLabel);

    var slider = document.createElement("input");
    slider.type = "range";
    slider.min = "0";
    slider.max = "90";
    slider.step = "1";
    slider.value = String(state.threshold);
    control.appendChild(slider);

    container.appendChild(control);

    var grid = htmlEl("div", "shade-grid");
    var flat = renderColumn("flat", get);
    var smooth = renderColumn("smooth", get);
    var auto = renderColumn("auto", get);
    grid.appendChild(flat.col);
    grid.appendChild(smooth.col);
    grid.appendChild(auto.col);
    container.appendChild(grid);

    container.appendChild(htmlEl("p", "shade-note",
      "Auto Smooth는 인접한 면 사이 각도가 임계값보다 작으면 부드럽게 잇고, 크면 모서리를 살려요. " +
      "이 데모 메쉬의 면 사이 각도는 약 " + FACET_ANGLE_DEG.toFixed(1) + "°. 임계값을 " +
      FACET_ANGLE_DEG.toFixed(0) + "° 아래로 낮추면 Flat처럼 보이고, 위로 올리면 Shade Smooth와 같아져요."
    ));

    slider.addEventListener("input", function () {
      state.threshold = Number(slider.value);
      valueSpan.textContent = state.threshold + "°";
      renderMesh(auto.svg, "auto", state.threshold);
    });

    target.appendChild(container);
  }

  function init() {
    var mounts = document.querySelectorAll('.widget-mount[data-widget="shade-smooth-auto-smooth"]');
    mounts.forEach(mount);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
