#!/bin/bash
# sync-wiki.sh: Obsidian wiki/raw + memory에서 핵심 포인터를 추출해 AGENTS.md에 주입
# Usage: ./scripts/sync-wiki.sh [--dry-run]

set -e

VAULT="$HOME/Documents/Obsidian Vault"
MEMORY_DIR="$HOME/.claude/projects/-Users-ssongji-Developer-Workspace/memory"
AGENTS="AGENTS.md"
DRY_RUN=false
[[ "$1" == "--dry-run" ]] && DRY_RUN=true

[[ ! -f "$AGENTS" ]] && { echo "❌ AGENTS.md 없음. agent-init부터 실행"; exit 1; }
[[ -L "$AGENTS" ]] && { echo "❌ AGENTS.md가 symlink. 실제 파일 위치에서 실행"; exit 1; }

# === Wiki pointers (wiki/_index.md 우선, 없으면 raw/ 파일 목록) ===
WIKI_INDEX="$VAULT/wiki/_index.md"
WIKI_RAW="$VAULT/raw"
if [[ -f "$WIKI_INDEX" ]]; then
  WIKI_CONTENT=$(grep -E '^- ' "$WIKI_INDEX" | head -20 || true)
  WIKI_SOURCE="wiki/_index.md"
elif [[ -d "$WIKI_RAW" ]]; then
  WIKI_CONTENT=$(ls "$WIKI_RAW" 2>/dev/null | sed 's/^/- /' | head -20 || true)
  WIKI_SOURCE="raw/ (wiki 미생성)"
else
  WIKI_CONTENT="(Obsidian Vault 비어있음)"
  WIKI_SOURCE="없음"
fi

# === Recent decisions (memory/decision_log.md 마지막 10개 항목) ===
DECISION_LOG="$MEMORY_DIR/decision_log.md"
if [[ -f "$DECISION_LOG" ]]; then
  # 테이블 행 추출: | 로 시작하고, 헤더행(|---|)과 날짜헤더 제외
  DECISIONS=$(grep '^|' "$DECISION_LOG" | grep -v '^|---' | grep -v '^| 날\|^| Date\|^| 항목' | tail -10 || true)
else
  DECISIONS="(decision_log.md 없음)"
fi

TS=$(date +%Y-%m-%d)

if $DRY_RUN; then
  echo "=== DRY RUN: 주입될 내용 ==="
  echo "[WIKI from: $WIKI_SOURCE]"
  echo "$WIKI_CONTENT"
  echo ""
  echo "[DECISIONS last 10]"
  echo "$DECISIONS"
  exit 0
fi

# === Python으로 마커 교체 (env vars로 안전하게 전달) ===
WIKI_CONTENT="$WIKI_CONTENT" \
DECISIONS="$DECISIONS" \
TS="$TS" \
AGENTS_PATH="$AGENTS" \
python3 << 'PYEOF'
import os, re, pathlib

p = pathlib.Path(os.environ["AGENTS_PATH"])
content = p.read_text()
ts = os.environ["TS"]
wiki = os.environ["WIKI_CONTENT"]
decisions = os.environ["DECISIONS"]

wiki_block = f"""<!-- BEGIN:WIKI -->
_last sync: {ts}_

{wiki}
<!-- END:WIKI -->"""

decisions_block = f"""<!-- BEGIN:DECISIONS -->
_last sync: {ts}_

{decisions}
<!-- END:DECISIONS -->"""

def replace_or_append(text, pattern, replacement, label):
    if re.search(pattern, text, flags=re.DOTALL):
        return re.sub(pattern, replacement, text, flags=re.DOTALL)
    else:
        print(f"  ℹ️  {label} 마커 없음 → 파일 끝에 추가")
        return text.rstrip() + "\n\n" + replacement + "\n"

content = replace_or_append(
    content,
    r'<!-- BEGIN:WIKI -->.*?<!-- END:WIKI -->',
    wiki_block,
    "WIKI"
)
content = replace_or_append(
    content,
    r'<!-- BEGIN:DECISIONS -->.*?<!-- END:DECISIONS -->',
    decisions_block,
    "DECISIONS"
)
p.write_text(content)
print("✅ AGENTS.md 갱신 완료")
PYEOF
