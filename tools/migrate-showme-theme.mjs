#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const ROOT = process.cwd();
const SHOWME_DIR = path.join(ROOT, "course-site", "assets", "showme");
const THEME_LINK = '<link rel="stylesheet" href="./theme.css">';

const PAPER_ROOT = `:root {
  --bg:            #F6F3EE;
  --bg-soft:       #ECE6DC;
  --surface:       #FFFDF8;
  --surface-strong:#ECE6DC;
  --line:          #E3DCD2;
  --line-strong:   rgba(27, 23, 24, .18);
  --key:           #00bfa5;
  --key-rgb:       0, 191, 165;
  --key-strong:    #009e8a;
  --key-soft:      #14a894;
  --success:       #3F706D;
  --success-rgb:   63, 112, 109;
  --success-soft:  #3F706D;
  --warn:          #A66629;
  --danger:        #B64A4A;
  --danger-soft:   #B64A4A;
  --warn-soft:     #A66629;
  --warn-medium:   #8E5520;
  --text:          #1B1718;
  --muted:         #8F8982;
  --muted-strong:  #514B47;
  --radius-sm:     4px;
  --radius-md:     8px;
  --radius-lg:     12px;
  --font: "Pretendard Variable", Pretendard, -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", sans-serif;
}`;

const INLINE_REPLACEMENTS = [
  [/--bg:\s*#0a0a0a/g, "--bg: #F6F3EE"],
  [/--bg:#0a0a0a/g, "--bg:#F6F3EE"],
  [/--bg-soft:\s*#111214/g, "--bg-soft: #ECE6DC"],
  [/--bg-soft:#111214/g, "--bg-soft:#ECE6DC"],
  [/--surface:\s*#17181a/g, "--surface: #FFFDF8"],
  [/--surface:#17181a/g, "--surface:#FFFDF8"],
  [/--surface-strong:\s*#1c1d20/g, "--surface-strong: #ECE6DC"],
  [/--surface-strong:#1c1d20/g, "--surface-strong:#ECE6DC"],
  [/--line:\s*rgba\(255,255,255,\.08\)/g, "--line: #E3DCD2"],
  [/--line:rgba\(255,255,255,\.08\)/g, "--line:#E3DCD2"],
  [/--line-strong:\s*rgba\(255,255,255,\.14\)/g, "--line-strong: rgba(27, 23, 24, .18)"],
  [/--key-soft:\s*#6ee8d8/g, "--key-soft: #14a894"],
  [/--key:\s*#0a84ff/g, "--key: #00bfa5"],
  [/--text:\s*#f5f5f7/g, "--text: #1B1718"],
  [/--text:#f5f5f7/g, "--text:#1B1718"],
  [/"Noto Sans KR"/g, '"Pretendard Variable", Pretendard'],
  [/Standalone Dark Theme/g, "Show Me Widget — Paper Theme"],
  [/rgba\(16,185,129,/g, "rgba(63,112,109,"],
  [/rgba\(245,158,11,/g, "rgba(166,102,41,"],
  [/#fbbf24/g, "var(--warn-soft)"],
  [/rgba\(255,255,255,\.025\)/g, "var(--showme-tint, rgba(27, 23, 24, .035))"],
  [/rgba\(255,255,255,\.03\)/g, "var(--showme-tint, rgba(27, 23, 24, .035))"],
  [/rgba\(255,255,255,\.04\)/g, "var(--showme-tint, rgba(27, 23, 24, .035))"],
  [/rgba\(255,255,255,\.06\)/g, "var(--showme-tint-hover, rgba(27, 23, 24, .07))"],
  [/rgba\(255,255,255,\.08\)/g, "var(--line)"],
  [/rgba\(255,255,255,\.09\)/g, "var(--showme-tint-hover, rgba(27, 23, 24, .07))"],
  [/rgba\(255,255,255,\.14\)/g, "var(--line-strong)"],
];

function migrateFile(filePath) {
  let html = fs.readFileSync(filePath, "utf8");
  let changed = false;

  if (html.includes(":root{") && html.includes("#0a0a0a")) {
    html = html.replace(/:root\{[^}]+\}/g, PAPER_ROOT.replace(/\n/g, "").replace(/  /g, ""));
    changed = true;
  }

  if (html.includes(":root {") && html.includes("#0a0a0a")) {
    html = html.replace(/:root\s*\{[\s\S]*?\}/m, PAPER_ROOT);
    changed = true;
  }

  INLINE_REPLACEMENTS.forEach(function([pattern, replacement]) {
    if (pattern.test(html)) {
      html = html.replace(pattern, replacement);
      changed = true;
    }
  });

  if (!html.includes(THEME_LINK)) {
    html = html.replace("</head>", `${THEME_LINK}\n</head>`);
    changed = true;
  }

  if (changed) {
    fs.writeFileSync(filePath, html, "utf8");
  }

  return changed;
}

const files = fs.readdirSync(SHOWME_DIR)
  .filter(function(name) { return name.endsWith(".html"); })
  .map(function(name) { return path.join(SHOWME_DIR, name); });

let updated = 0;
files.forEach(function(filePath) {
  if (migrateFile(filePath)) {
    updated += 1;
    console.log("updated:", path.basename(filePath));
  }
});

console.log(`\nDone. ${updated}/${files.length} files updated.`);
