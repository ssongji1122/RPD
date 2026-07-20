#!/usr/bin/env bash
# audit-contrast.sh — WCAG AA 텍스트 대비 4.5:1 하드 게이트
#
# 규칙 SoT: web/src/styles/tokens.css (2026-07-18 가독성 감사 교정, studio.soluta PR #344 패턴 이식)
#   - 라이트: ink / ink-2 / ink-3 / accent-text × bg, bg-2 → 4.5:1 이상
#   - 다크 ([data-theme="dark"]): ink / ink-2 / ink-3 / accent-text × bg(#181816 계열) → 4.5:1 이상
#
# 계산: WCAG 2.x relative luminance 공식, node -e 인라인.
#
# 사용:
#   scripts/audit-contrast.sh
set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TOKENS_CSS="$ROOT/src/styles/tokens.css"

if [ ! -f "$TOKENS_CSS" ]; then
  echo "tokens.css를 찾을 수 없습니다: $TOKENS_CSS" >&2
  exit 1
fi

TOKENS_CSS="$TOKENS_CSS" node -e '
  const fs = require("fs");
  const css = fs.readFileSync(process.env.TOKENS_CSS, "utf8");

  function extractBlock(pattern) {
    const m = css.match(pattern);
    return m ? m[1] : null;
  }

  function extractVar(block, name) {
    if (!block) return null;
    const re = new RegExp(name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "\\s*:\\s*(#[0-9A-Fa-f]{6})");
    const m = block.match(re);
    return m ? m[1] : null;
  }

  const rootBlock = extractBlock(/:root\s*\{([\s\S]*?)\n\}/);
  const darkBlock = extractBlock(/\[data-theme="dark"\]\s*\{([\s\S]*?)\n\}/);

  if (!rootBlock) {
    console.error("tokens.css에서 :root 블록을 찾지 못했습니다.");
    process.exit(1);
  }
  if (!darkBlock) {
    console.error("tokens.css에서 [data-theme=\"dark\"] 블록을 찾지 못했습니다.");
    process.exit(1);
  }

  function hexToRgb(hex) {
    const n = parseInt(hex.slice(1), 16);
    return { r: (n >> 16) & 255, g: (n >> 8) & 255, b: n & 255 };
  }

  function channelLum(c) {
    const s = c / 255;
    return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
  }

  function relativeLuminance(hex) {
    const { r, g, b } = hexToRgb(hex);
    return 0.2126 * channelLum(r) + 0.7152 * channelLum(g) + 0.0722 * channelLum(b);
  }

  function contrastRatio(hexA, hexB) {
    const l1 = relativeLuminance(hexA);
    const l2 = relativeLuminance(hexB);
    const lighter = Math.max(l1, l2);
    const darker = Math.min(l1, l2);
    return (lighter + 0.05) / (darker + 0.05);
  }

  const MIN_RATIO = 4.5;
  const violations = [];

  function check(label, textHex, bgHex, bgLabel) {
    if (!textHex || !bgHex) {
      violations.push(`${label} — 토큰을 찾지 못함 (text=${textHex}, bg=${bgHex})`);
      return;
    }
    const ratio = contrastRatio(textHex, bgHex);
    if (ratio < MIN_RATIO) {
      violations.push(`${label} on ${bgLabel} — ${textHex} / ${bgHex} = ${ratio.toFixed(2)}:1 (< ${MIN_RATIO}:1)`);
    }
  }

  // ---------- 라이트 (root = 기본값) ----------
  const lightBg = extractVar(rootBlock, "--c-bg");
  const lightBg2 = extractVar(rootBlock, "--c-bg-2");
  const lightInk = extractVar(rootBlock, "--c-ink");
  const lightInk2 = extractVar(rootBlock, "--c-ink-2");
  const lightInk3 = extractVar(rootBlock, "--c-ink-3");
  const lightAccentText = extractVar(rootBlock, "--c-accent-text");

  for (const [label, hex] of [
    ["--c-ink", lightInk],
    ["--c-ink-2", lightInk2],
    ["--c-ink-3", lightInk3],
    ["--c-accent-text", lightAccentText],
  ]) {
    check(`[light] ${label}`, hex, lightBg, "--c-bg");
    check(`[light] ${label}`, hex, lightBg2, "--c-bg-2");
  }

  // ---------- 다크 ([data-theme="dark"]) ----------
  const darkBg = extractVar(darkBlock, "--c-bg");
  const darkInk = extractVar(darkBlock, "--c-ink");
  const darkInk2 = extractVar(darkBlock, "--c-ink-2");
  const darkInk3 = extractVar(darkBlock, "--c-ink-3");
  const darkAccentText = extractVar(darkBlock, "--c-accent-text");

  for (const [label, hex] of [
    ["--c-ink", darkInk],
    ["--c-ink-2", darkInk2],
    ["--c-ink-3", darkInk3],
    ["--c-accent-text", darkAccentText],
  ]) {
    check(`[dark] ${label}`, hex, darkBg, "--c-bg");
  }

  if (violations.length > 0) {
    console.error("대비 4.5:1 미달 발견 — web/src/styles/tokens.css 참조:");
    for (const v of violations) console.error("  " + v);
    process.exit(1);
  }
  process.exit(0);
'
exit $?
