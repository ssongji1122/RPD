// ============================================================
// Widget: modifier-stack-order
// ============================================================
// Side-by-side comparison of three Modifier stack orderings.
// Renders 3 SVG illustrations showing how the same base mesh
// ends up differently depending on Mirror/Boolean/Subdivision
// order. Pedagogical, no live 3D — static SVG with annotations.

(function () {
  var SVG_NS = "http://www.w3.org/2000/svg";

  function el(tag, attrs, children) {
    var node = document.createElementNS(SVG_NS, tag);
    if (attrs) Object.keys(attrs).forEach(function (k) { node.setAttribute(k, attrs[k]); });
    (children || []).forEach(function (c) { node.appendChild(c); });
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

  function renderResult(svg, kind) {
    clearChildren(svg);
    svg.setAttribute("viewBox", "0 0 200 160");

    svg.appendChild(el("rect", { x: "0", y: "0", width: "200", height: "160", fill: "#17181a", rx: "8" }));

    svg.appendChild(el("path", {
      d: "M30 30 Q50 20 100 22 L100 138 Q60 140 30 130 Z",
      fill: kind === "boolean-before-mirror" ? "#3b3d42" : "#5a6068",
      stroke: "#8ec5ff",
      "stroke-width": "1.5",
    }));
    svg.appendChild(el("path", {
      d: "M100 22 Q150 20 170 30 L170 130 Q140 140 100 138 Z",
      fill: "#5a6068",
      stroke: "#8ec5ff",
      "stroke-width": "1.5",
    }));

    var creaseColor = kind === "subdiv-first" ? "#f59e0b" : "#0a84ff";
    svg.appendChild(el("path", {
      d: "M100 22 L100 138",
      stroke: creaseColor,
      "stroke-width": kind === "subdiv-first" ? "2.4" : "1",
      "stroke-dasharray": kind === "subdiv-first" ? "4 3" : "0",
      opacity: kind === "correct" ? "0.4" : "0.85",
    }));

    if (kind === "correct") {
      svg.appendChild(el("circle", { cx: "70", cy: "80", r: "11", fill: "#0a0a0a", stroke: "#10b981", "stroke-width": "1.5" }));
      svg.appendChild(el("circle", { cx: "130", cy: "80", r: "11", fill: "#0a0a0a", stroke: "#10b981", "stroke-width": "1.5" }));
    } else if (kind === "subdiv-first") {
      svg.appendChild(el("path", {
        d: "M59 80 Q65 70 70 70 Q78 71 81 80 Q79 88 70 90 Q63 89 59 80",
        fill: "#0a0a0a",
        stroke: "#ef4444",
        "stroke-width": "1.5",
        "stroke-linejoin": "miter",
      }));
      svg.appendChild(el("path", {
        d: "M119 80 Q125 70 130 70 Q138 71 141 80 Q139 88 130 90 Q123 89 119 80",
        fill: "#0a0a0a",
        stroke: "#ef4444",
        "stroke-width": "1.5",
        "stroke-linejoin": "miter",
      }));
    } else if (kind === "boolean-before-mirror") {
      svg.appendChild(el("circle", { cx: "130", cy: "80", r: "11", fill: "#0a0a0a", stroke: "#ef4444", "stroke-width": "1.5" }));
    }
  }

  function renderColumn(orderLabels, verdict, kind) {
    var col = htmlEl("div", "stack-col");

    var orderList = htmlEl("ol", "stack-order");
    orderLabels.forEach(function (label) {
      orderList.appendChild(htmlEl("li", "stack-step", label));
    });
    col.appendChild(orderList);

    var svg = document.createElementNS(SVG_NS, "svg");
    svg.setAttribute("class", "stack-result");
    svg.setAttribute("width", "100%");
    svg.setAttribute("height", "auto");
    renderResult(svg, kind);
    col.appendChild(svg);

    col.appendChild(htmlEl(
      "div",
      "stack-verdict " + (kind === "correct" ? "is-ok" : "is-warn"),
      verdict
    ));

    return col;
  }

  function injectStyles() {
    if (document.getElementById("modifier-stack-widget-styles")) return;
    var style = document.createElement("style");
    style.id = "modifier-stack-widget-styles";
    style.textContent = (
      ".modifier-stack-widget{display:flex;flex-direction:column;gap:18px;max-width:780px;margin:0 auto;padding:8px 0}" +
      ".modifier-stack-widget .stack-lead{margin:0;color:var(--text,#f5f5f7);font-size:.95rem;line-height:1.7;word-break:keep-all}" +
      ".modifier-stack-widget .stack-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}" +
      ".modifier-stack-widget .stack-col{display:flex;flex-direction:column;gap:10px;padding:14px;border-radius:10px;border:1px solid var(--line,rgba(255,255,255,.08));background:var(--surface,#17181a)}" +
      ".modifier-stack-widget .stack-order{margin:0;padding-left:18px;color:var(--muted-strong,#d4d4d8);font-size:.85rem;line-height:1.6}" +
      ".modifier-stack-widget .stack-step{margin:2px 0}" +
      ".modifier-stack-widget .stack-result{display:block;width:100%;border-radius:6px}" +
      ".modifier-stack-widget .stack-verdict{font-size:.82rem;font-weight:600;padding:6px 10px;border-radius:6px;text-align:center}" +
      ".modifier-stack-widget .stack-verdict.is-ok{color:var(--success,#10b981);background:rgba(16,185,129,.12)}" +
      ".modifier-stack-widget .stack-verdict.is-warn{color:var(--warn-soft,#fbbf24);background:rgba(245,158,11,.12)}" +
      ".modifier-stack-widget .stack-note{margin:0;color:var(--muted,#a1a1aa);font-size:.85rem;line-height:1.6;word-break:keep-all}"
    );
    document.head.appendChild(style);
  }

  function mount(target) {
    clearChildren(target);
    injectStyles();

    var container = htmlEl("div", "modifier-stack-widget");
    container.appendChild(htmlEl("p", "stack-lead",
      "같은 Modifier도 순서가 다르면 결과가 달라져요. 세 가지 순서를 비교해보세요."
    ));

    var grid = htmlEl("div", "stack-grid");
    grid.appendChild(renderColumn(
      ["Mirror", "Boolean", "Subdivision"],
      "권장 — 깔끔한 결과",
      "correct"
    ));
    grid.appendChild(renderColumn(
      ["Subdivision", "Boolean", "Mirror"],
      "Boolean 가장자리 지저분",
      "subdiv-first"
    ));
    grid.appendChild(renderColumn(
      ["Boolean", "Mirror", "Subdivision"],
      "구멍이 한쪽에만",
      "boolean-before-mirror"
    ));
    container.appendChild(grid);

    container.appendChild(htmlEl("p", "stack-note",
      "Subdivision은 거의 항상 마지막. Mirror가 Boolean보다 먼저 와야 양쪽 대칭이 유지돼요."
    ));

    target.appendChild(container);
  }

  function init() {
    var mounts = document.querySelectorAll('.widget-mount[data-widget="modifier-stack-order"]');
    mounts.forEach(mount);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
