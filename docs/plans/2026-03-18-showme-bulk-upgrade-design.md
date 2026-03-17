# ShowMe Bulk Upgrade Design
Date: 2026-03-18

## Goal
1. Connect 18 unconnected ShowMe cards to curriculum.js
2. Enhance 35 basic-pattern cards with interactive visualization

## Scope
- 57 total showme cards → 6 already enhanced → 51 remaining
- 35 connected+basic → visualization upgrade only
- 18 not-connected → curriculum placement + visualization upgrade

## Phase 1 — Curriculum Connection (1 agent)
Connect 18 cards to appropriate weeks/steps in curriculum.js:
box-rounding, build-modifier, curve-to-tube, edge-split-modifier, mask-modifier,
multiresolution-modifier, origin-vs-3dcursor, poly-circle, proportional-editing,
scatter-on-surface, screw-modifier, simple-deform, skin-modifier, snap,
triangulate-modifier, volume-to-mesh, weld-modifier, wireframe-modifier

Strategy: match card topic to existing curriculum steps or create new showme steps.

## Phase 2 — Visualization Enhancement (5 parallel agents)
Batch assignment (~7 cards each):

**Agent A**: armature-basics, array-modifier, bevel-modifier, bevel-tool, blender-preferences, boolean-modifier, compositing-basics
**Agent B**: decimate-modifier, edit-mode, edit-mode-tools, extrude, graph-editor, hdri-lighting, image-reference
**Agent C**: inset, keyframe-basics, light-types, loop-cut, material-basics, mirror-modifier, principled-bsdf
**Agent D**: remesh-modifier, render-settings, sculpt-basics, shader-editor, solidify-modifier, three-point-light, transform-grs
**Agent E**: uv-editor, uv-unwrapping, viewport-navigation, weight-paint, weighted-normal, xray-opacity

## Quality Standard
- Target: Full quality (scenario-nav + canvas + cause-effect)
- Allowed: Agent decides based on card topic suitability
- Reference: origin-vs-3dcursor.html as pattern example

## Success Criteria
- All 57 cards have scenario-nav pattern
- All 53 non-reference cards connected to curriculum
- No broken HTML/JS
