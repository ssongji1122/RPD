// ============================================================
// Show Me 위젯 레지스트리
// 위젯 ID → 메타데이터 매핑
// week.html에서 버튼 라벨/아이콘 조회에 사용
// ============================================================

const SHOWME_REGISTRY = {
  // ── Week 3: Reference Setup ──
  "image-reference":        { label: "이미지 레퍼런스 설정",      icon: "🖼️" },

  // ── Week 2: Interface & Fundamentals ──
  "blender-preferences":    { label: "Preferences 설정",        icon: "⚙️" },
  "viewport-navigation":    { label: "화면 조작 원리",          icon: "🧭" },
  "transform-grs":          { label: "G/R/S 변형 이해",         icon: "↔️" },
  "transform-orientation":  { label: "Transform Orientation 이해", icon: "🧭" },
  "pivot-point":            { label: "Pivot Point 이해",        icon: "🎯" },
  "snap":                   { label: "Snapping 이해",           icon: "🧲" },
  "viewport-shading":       { label: "Viewport Shading 이해",   icon: "💡" },
  "xray-opacity":           { label: "X-Ray 투명도 조절",        icon: "🔍" },
  "edit-mode":              { label: "Edit Mode 이해",          icon: "✏️", toolName: "Edit Mode", iconKey: "edit-mode" },

  // ── Edit Mode Tools (기능별 라이브러리) ──
  "edit-mode-tools":        { label: "Edit Mode 도구 전체",     icon: "🛠️", toolName: "Toolset", iconKey: "edit-mode" },
  "extrude":                { label: "Extrude 작동 원리",       icon: "📐", toolName: "Extrude", iconKey: "extrude" },
  "loop-cut":               { label: "Loop Cut 이해",           icon: "🔪", toolName: "Loop Cut", iconKey: "loop-cut" },
  "inset":                  { label: "Inset 작동 원리",         icon: "⬜", toolName: "Inset", iconKey: "inset" },
  "bevel-tool":             { label: "Bevel Tool 이해",         icon: "🔧", toolName: "Bevel", iconKey: "bevel" },

  // ── Generate Modifiers (기능별 라이브러리) ──
  "array-modifier":         { label: "Array Modifier 이해",     icon: "🔁" },
  "bevel-modifier":         { label: "Bevel Modifier 이해",     icon: "🔶" },
  "boolean-modifier":       { label: "Boolean 작동 원리",       icon: "✂️" },
  "build-modifier":         { label: "Build Modifier 이해",     icon: "🏗️" },
  "curve-to-tube":          { label: "Curve to Tube 이해",      icon: "🔄" },
  "decimate-modifier":      { label: "Decimate 이해",           icon: "📉" },
  "edge-split-modifier":    { label: "Edge Split 이해",         icon: "🔀" },
  "mask-modifier":          { label: "Mask Modifier 이해",      icon: "🎭" },
  "mirror-modifier":        { label: "Mirror Modifier 이해",    icon: "🪞" },
  "mirror-workflow":        { label: "Mirror 작업 흐름",        icon: "🔄" },
  "mirror-origin-mode":     { label: "Mirror·Origin·모드 이해", icon: "🔀" },
  "multiresolution-modifier": { label: "Multiresolution 이해",  icon: "🔍" },
  "remesh-modifier":        { label: "Remesh 이해",             icon: "🔲" },
  "scatter-on-surface":     { label: "Scatter on Surface 이해", icon: "🌿" },
  "screw-modifier":         { label: "Screw Modifier 이해",     icon: "🌀" },
  "skin-modifier":          { label: "Skin Modifier 이해",      icon: "🦠" },
  "solidify-modifier":      { label: "Solidify 이해",           icon: "📦" },
  "subdivision-surface":    { label: "Subdivision Surface 이해", icon: "🫧" },
  "triangulate-modifier":   { label: "Triangulate 이해",        icon: "🔺" },
  "volume-to-mesh":         { label: "Volume to Mesh 이해",     icon: "💨" },
  "weld-modifier":          { label: "Weld Modifier 이해",      icon: "⚡" },
  "wireframe-modifier":     { label: "Wireframe 이해",          icon: "🕸️" },

  // ── Normals ──
  "weighted-normal":        { label: "Weighted Normal 이해",    icon: "💡" },

  // ── Week 3–4: Transform & Cleanup ──
  "proportional-editing":   { label: "Proportional Editing 이해", icon: "〰️" },
  "transform-apply":        { label: "Apply Transform 이해",    icon: "✅" },
  "simple-deform":          { label: "Simple Deform 이해",      icon: "🌀" },
  "bevel-tool-vs-modifier": { label: "Bevel 비교",              icon: "⚖️" },
  "join-separate":          { label: "Join/Separate 이해",      icon: "🔗" },

  // ── Week 5: Sculpting ──
  "sculpt-basics":          { label: "Sculpt Mode 기초",        icon: "🎨" },

  // ── Week 6: Material & Shader ──
  "material-basics":        { label: "Material 시스템 기초",     icon: "🎨" },
  "principled-bsdf":        { label: "Principled BSDF 이해",    icon: "🎭" },
  "shader-editor":          { label: "Shader Editor 이해",      icon: "🔌" },

  // ── Week 7: UV ──
  "uv-unwrapping":          { label: "UV Unwrapping 이해",      icon: "📐" },
  "uv-editor":              { label: "UV Editor 조작",          icon: "🗺️" },

  // ── Week 9: Lighting ──
  "light-types":            { label: "4가지 Light 종류",         icon: "💡" },
  "hdri-lighting":          { label: "HDRI 환경 조명",           icon: "🌅" },
  "three-point-light":      { label: "3점 조명법",               icon: "🎬" },

  // ── Week 10: Animation ──
  "keyframe-basics":        { label: "키프레임 기초",            icon: "⏱️" },
  "graph-editor":           { label: "Graph Editor 이해",       icon: "📈" },

  // ── Week 11: Rigging ──
  "armature-basics":        { label: "Armature 이해",           icon: "🦴" },
  "weight-paint":           { label: "Weight Paint 이해",       icon: "🖌️" },

  // ── Week 13: Rendering ──
  "render-settings":        { label: "Cycles vs EEVEE",         icon: "🖥️" },
  "compositing-basics":     { label: "컴포지팅 기초",            icon: "🎞️" },

  // ── Concepts ──
  "origin-vs-3dcursor":     { label: "Origin vs 3D Cursor",    icon: "🎯" },
  "poly-circle":            { label: "다각형으로 원 만들기",       icon: "⭕", toolName: "Poly Circle", iconKey: "poly-circle" },
  "box-rounding":           { label: "박스 모서리 라운딩",          icon: "📦" },
};

if (typeof window !== "undefined") window.SHOWME_REGISTRY = SHOWME_REGISTRY;
if (typeof globalThis !== "undefined") globalThis.SHOWME_REGISTRY = SHOWME_REGISTRY;
