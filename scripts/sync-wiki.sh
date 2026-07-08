#!/bin/bash
# sync-wiki.sh: Obsidian wiki/raw + memory에서 핵심 포인터를 추출해 AGENTS.md에 주입
# Usage: ./scripts/sync-wiki.sh [--dry-run]

set -e

VAULT="$HOME/Documents/Obsidian Vault"
# 이 프로젝트 자신의 Claude Code memory 디렉토리를 동적으로 찾는다 (하드코딩 시 다른
# 프로젝트 경로로 드리프트하기 쉬움 — thegoodfriends에서 실측 확인된 버그, PR #1060).
# worktree에서 실행될 수 있으므로 git-common-dir로 origin repo 루트를 찾는다
# (scripts/worktree-bootstrap.sh와 동일 패턴). Claude Code project slug 규칙:
# 절대경로에서 영숫자·하이픈이 아닌 문자(/, . 등)를 전부 "-"로 치환
# (경로에 "."이 오는 프로젝트, 예: studio.soluta, 에서 "/"만 치환하면 실제 슬러그와 어긋남).
GIT_COMMON_DIR="$(git rev-parse --git-common-dir 2>/dev/null || true)"
if [[ -n "$GIT_COMMON_DIR" ]]; then
  case "$GIT_COMMON_DIR" in
    /*) ;;
    *) GIT_COMMON_DIR="$(cd "$GIT_COMMON_DIR" && pwd)" ;;
  esac
  PROJECT_ROOT="$(dirname "$GIT_COMMON_DIR")"
else
  PROJECT_ROOT="$(pwd)"
fi
PROJECT_SLUG="${PROJECT_ROOT//[^A-Za-z0-9-]/-}"
MEMORY_DIR="$HOME/.claude/projects/${PROJECT_SLUG}/memory"
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
  # 표준 형식: "#... YYYY-MM-DD — 제목" 헤딩 단위 기록 (헤딩 레벨은 프로젝트마다
  # ##/### 등으로 다름 — RPD는 ##, thegoodfriends는 ### 실사용 확인).
  # 일부 프로젝트가 여전히 레거시 파이프 테이블(| 날짜 | 제목 | 상세 | 범위 |)을
  # 쓰므로, 헤딩이 하나도 없을 때만 그 형식으로 fallback한다.
  DECISIONS=$(grep -E '^#+ [0-9]{4}-[0-9]{2}-[0-9]{2} — ' "$DECISION_LOG" | sed -E 's/^#+ /- /' | tail -10 || true)
  if [[ -z "$DECISIONS" ]]; then
    DECISIONS=$(grep '^|' "$DECISION_LOG" | grep -v '^|---' | grep -v '^| 날\|^| Date\|^| 항목' | tail -10 || true)
  fi
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
