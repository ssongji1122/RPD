// ============================================================
// Show Me 위젯 레지스트리
// 위젯 ID → 메타데이터 매핑
// week.html에서 버튼 라벨/아이콘 조회에 사용
// ============================================================

const SHOWME_REGISTRY = {
  // ── Week 2: Interface & Fundamentals ──
  "viewport-navigation":    { label: "화면 조작 원리",          icon: "🧭" },
  "transform-grs":          { label: "G/R/S 변형 이해",         icon: "↔️" },
  "edit-mode":              { label: "Edit Mode 이해",          icon: "✏️" },

  // ── Week 2-3: Core Editing Tools ──
  "extrude":                { label: "Extrude 작동 원리",       icon: "📐" },
  "loop-cut":               { label: "Loop Cut 이해",           icon: "🔪" },
  "inset":                  { label: "Inset 작동 원리",         icon: "⬜" },
  "bevel-tool":             { label: "Bevel Tool 이해",         icon: "🔧" },

  // ── Week 3: Modifiers ──
  "mirror-modifier":        { label: "Mirror Modifier 이해",    icon: "🪞" },
  "subdivision-surface":    { label: "Subdivision Surface 이해", icon: "🫧" },
  "solidify-modifier":      { label: "Solidify 이해",           icon: "📦" },
  "array-modifier":         { label: "Array Modifier 이해",     icon: "🔁" },
  "boolean-modifier":       { label: "Boolean 작동 원리",       icon: "✂️" },
  "bevel-modifier":         { label: "Bevel Modifier 이해",     icon: "🔶" },
  "weighted-normal":        { label: "Weighted Normal 이해",    icon: "💡" },

  // ── Week 4: Detail & Cleanup ──
  "bevel-tool-vs-modifier": { label: "Bevel 비교",              icon: "⚖️" },
  "transform-apply":        { label: "Apply Transform 이해",    icon: "✅" },
  "join-separate":          { label: "Join/Separate 이해",      icon: "🔗" },

  // ── Week 5: Sculpting ──
  "sculpt-mode":            { label: "Sculpt Mode 이해",        icon: "🎨" },
  "remesh":                 { label: "Remesh 이해",             icon: "🔲" },

  // ── Week 6: Material & Shader ──
  "principled-bsdf":        { label: "Principled BSDF 이해",    icon: "🎭" },
  "shader-node-editor":     { label: "Shader Editor 이해",      icon: "🔌" },

  // ── Week 9: Lighting ──
  "three-point-lighting":   { label: "3점 조명 이해",           icon: "💡" },
  "hdri-setup":             { label: "HDRI 조명 이해",          icon: "🌅" },

  // ── Week 10: Animation ──
  "keyframe-insertion":     { label: "키프레임 이해",            icon: "🎬" },
  "graph-editor":           { label: "Graph Editor 이해",       icon: "📈" },

  // ── Week 11: Rigging ──
  "weight-painting":        { label: "Weight Paint 이해",       icon: "🖌️" },
  "armature-basics":        { label: "Armature 이해",           icon: "🦴" },

  // ── Concepts ──
  "origin-vs-3dcursor":     { label: "Origin vs 3D Cursor",    icon: "🎯" },
};
