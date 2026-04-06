// ============================================================
// Show Me 위젯 레지스트리
// 위젯 ID → 메타데이터 매핑
// week.html에서 버튼 라벨/아이콘 조회에 사용
// ============================================================

const SHOWME_REGISTRY = {
  // ── Week 3: Reference Setup ──
  "image-reference":        { label: "이미지 레퍼런스 설정",      icon: "🖼️", week: 3 },

  // ── Week 2: Interface & Fundamentals ──
  "blender-preferences":    { label: "Preferences 설정",        icon: "⚙️", week: 2 },
  "viewport-navigation":    { label: "화면 조작 원리",          icon: "🧭", week: 2 },
  "transform-grs":          { label: "G/R/S 변형 이해",         icon: "↔️", week: 2 },
  "transform-orientation":  { label: "Transform Orientation 이해", icon: "🧭", week: 2 },
  "pivot-point":            { label: "Pivot Point 이해",        icon: "🎯", week: 2 },
  "snap":                   { label: "Snapping 이해",           icon: "🧲", week: 2 },
  "viewport-shading":       { label: "Viewport Shading 이해",   icon: "💡", week: 2 },
  "xray-opacity":           { label: "X-Ray 투명도 조절",        icon: "🔍", week: 2 },
  "edit-mode":              { label: "Edit Mode 이해",          icon: "✏️", week: 2, toolName: "Edit Mode", iconKey: "edit-mode" },

  // ── Edit Mode Tools (기능별 라이브러리) ──
  "edit-mode-tools":        { label: "Edit Mode 도구 전체",     icon: "🛠️", week: 3, toolName: "Toolset", iconKey: "edit-mode" },
  "extrude":                { label: "Extrude 작동 원리",       icon: "📐", week: 3, toolName: "Extrude", iconKey: "extrude" },
  "loop-cut":               { label: "Loop Cut 이해",           icon: "🔪", week: 3, toolName: "Loop Cut", iconKey: "loop-cut" },
  "inset":                  { label: "Inset 작동 원리",         icon: "⬜", week: 3, toolName: "Inset", iconKey: "inset" },
  "bevel-tool":             { label: "Bevel Tool 이해",         icon: "🔧", week: 3, toolName: "Bevel", iconKey: "bevel" },

  // ── Generate Modifiers (기능별 라이브러리) ──
  "array-modifier":         { label: "Array Modifier 이해",     icon: "🔁", week: 3 },
  "bevel-modifier":         { label: "Bevel Modifier 이해",     icon: "🔶", week: 3 },
  "boolean-modifier":       { label: "Boolean 작동 원리",       icon: "✂️", week: 3 },
  "build-modifier":         { label: "Build Modifier 이해",     icon: "🏗️", week: 4 },
  "curve-to-tube":          { label: "Curve to Tube 이해",      icon: "🔄", week: 4 },
  "decimate-modifier":      { label: "Decimate 이해",           icon: "📉", week: 4 },
  "edge-split-modifier":    { label: "Edge Split 이해",         icon: "🔀", week: 4 },
  "mask-modifier":          { label: "Mask Modifier 이해",      icon: "🎭", week: 4 },
  "mirror-modifier":        { label: "Mirror Modifier 이해",    icon: "🪞", week: 3 },
  "mirror-workflow":        { label: "Mirror 작업 흐름",        icon: "🔄", week: 3 },
  "mirror-origin-mode":     { label: "Mirror·Origin·모드 이해", icon: "🔀", week: 3 },
  "multiresolution-modifier": { label: "Multiresolution 이해",  icon: "🔍", week: 4 },
  "remesh-modifier":        { label: "Remesh 이해",             icon: "🔲", week: 4 },
  "remesh-decimate":        { label: "Remesh vs Decimate",      icon: "🔀", week: 5 },
  "scatter-on-surface":     { label: "Scatter on Surface 이해", icon: "🌿", week: 4 },
  "screw-modifier":         { label: "Screw Modifier 이해",     icon: "🌀", week: 4 },
  "skin-modifier":          { label: "Skin Modifier 이해",      icon: "🦠", week: 4 },
  "solidify-modifier":      { label: "Solidify 이해",           icon: "📦", week: 3 },
  "subdivision-surface":    { label: "Subdivision Surface 이해", icon: "🫧", week: 3 },
  "triangulate-modifier":   { label: "Triangulate 이해",        icon: "🔺", week: 4 },
  "volume-to-mesh":         { label: "Volume to Mesh 이해",     icon: "💨", week: 4 },
  "weld-modifier":          { label: "Weld Modifier 이해",      icon: "⚡", week: 4 },
  "wireframe-modifier":     { label: "Wireframe 이해",          icon: "🕸️", week: 4 },

  // ── Normals ──
  "weighted-normal":        { label: "Weighted Normal 이해",    icon: "💡", week: 3 },

  // ── Week 3–4: Transform & Cleanup ──
  "proportional-editing":   { label: "Proportional Editing 이해", icon: "〰️", week: 3 },
  "transform-apply":        { label: "Apply Transform 이해",    icon: "✅", week: 3 },
  "simple-deform":          { label: "Simple Deform 이해",      icon: "🌀", week: 3 },
  "bevel-tool-vs-modifier": { label: "Bevel 비교",              icon: "⚖️", week: 0 },
  "join-separate":          { label: "Join/Separate 이해",      icon: "🔗", week: 3 },

  // ── Week 5: Sculpting ──
  "sculpt-basics":          { label: "Sculpt Mode 기초",        icon: "🎨", week: 5 },
  "sculpt-brushes":         { label: "Sculpt 브러시 선택 기준",  icon: "🖌️", week: 5 },
  "ai-prompt-design":       { label: "AI 프롬프트 설계법",       icon: "✍️", week: 5 },
  "ai-3d-generation":       { label: "AI 3D 생성 워크플로우",    icon: "🤖", week: 5 },

  // ── Week 6: Material & Shader ──
  "material-basics":        { label: "Material 시스템 기초",     icon: "🎨", week: 6 },
  "principled-bsdf":        { label: "Principled BSDF 이해",    icon: "🎭", week: 6 },
  "shader-editor":          { label: "Shader Editor 이해",      icon: "🔌", week: 6 },
  "texture-nodes":          { label: "Texture Nodes 이해",      icon: "🧩", week: 6 },
  "color-ramp":             { label: "Color Ramp 이해",         icon: "🌈", week: 6 },
  "noise-texture":          { label: "Noise Texture 이해",      icon: "🌫️", week: 6 },
  "texture-types":          { label: "Procedural vs Image",     icon: "🔀", week: 6 },
  "image-texture-pbr":      { label: "Image Texture + PBR",     icon: "🖼️", week: 6 },

  // ── Week 7: UV ──
  "uv-unwrapping":          { label: "UV Unwrapping 이해",      icon: "📐", week: 7 },
  "uv-editor":              { label: "UV Editor 조작",          icon: "🗺️", week: 7 },
  "texture-painting":       { label: "Texture Painting 기초",   icon: "🖌️", week: 7 },

  // ── Week 9: Lighting ──
  "light-types":            { label: "4가지 Light 종류",         icon: "💡", week: 9 },
  "hdri-lighting":          { label: "HDRI 환경 조명",           icon: "🌅", week: 9 },
  "three-point-light":      { label: "3점 조명법",               icon: "🎬", week: 9 },
  "camera-setup":           { label: "카메라 세팅 이해",           icon: "📷", week: 9 },
  "depth-of-field":         { label: "Depth of Field 이해",       icon: "🎥", week: 9 },

  // ── Week 10: Animation ──
  "keyframe-basics":        { label: "키프레임 기초",            icon: "⏱️", week: 10 },
  "graph-editor":           { label: "Graph Editor 이해",       icon: "📈", week: 10 },
  "dope-sheet":             { label: "Dope Sheet 이해",         icon: "🎞️", week: 10 },

  // ── Week 11: Rigging ──
  "armature-basics":        { label: "Armature 이해",           icon: "🦴", week: 11 },
  "weight-paint":           { label: "Weight Paint 이해",       icon: "🖌️", week: 11 },

  // ── Week 12: NLA ──
  "nla-editor":             { label: "NLA Editor 이해",         icon: "🎬", week: 12 },

  // ── Week 13: Rendering ──
  "render-settings":        { label: "Cycles vs EEVEE",         icon: "🖥️", week: 13 },
  "compositing-basics":     { label: "컴포지팅 기초",            icon: "🎞️", week: 13 },

  // ── Concepts ──
  "origin-vs-3dcursor":     { label: "Origin vs 3D Cursor",    icon: "🎯", week: 0 },
  "poly-circle":            { label: "다각형으로 원 만들기",       icon: "⭕", week: 0, toolName: "Poly Circle", iconKey: "poly-circle" },
  "box-rounding":           { label: "박스 모서리 라운딩",          icon: "📦", week: 0 },
};

if (typeof window !== "undefined") window.SHOWME_REGISTRY = SHOWME_REGISTRY;
if (typeof globalThis !== "undefined") globalThis.SHOWME_REGISTRY = SHOWME_REGISTRY;
