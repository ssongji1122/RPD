#!/usr/bin/env node

/**
 * Deprecated compatibility wrapper.
 *
 * Canonical 운영 경로는 Python 구현(`tools/notion-sync.py`)입니다.
 * 이 스크립트는 기존 호출 지점을 깨지 않기 위해 유지되며,
 * 더 이상 overrides.json을 직접 갱신하지 않습니다.
 */

const path = require("path");
const { spawnSync } = require("child_process");

const root = path.resolve(__dirname, "..");
const pythonScript = path.join(root, "tools", "notion-sync.py");
const args = process.argv.slice(2);

if (args.includes("--week") || args.includes("--all")) {
  console.warn("⚠ node tools/notion-sync.js 의 주차 단위 옵션은 더 이상 지원되지 않습니다.");
  console.warn("  전체 Notion 스냅샷만 갱신합니다.");
}

console.warn("⚠ node tools/notion-sync.js 는 deprecated 입니다.");
console.warn("  대신 `python3 tools/notion-sync.py --fetch-only` 를 사용하세요.\n");

const result = spawnSync("python3", [pythonScript, "--fetch-only"], {
  cwd: root,
  env: process.env,
  stdio: "inherit",
});

if (result.error) {
  console.error(`❌ Python wrapper 실행 실패: ${result.error.message}`);
  process.exit(1);
}

process.exit(result.status == null ? 1 : result.status);
