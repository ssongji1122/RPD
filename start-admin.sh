#!/bin/bash
# RPD Admin Server 시작 스크립트 + 동기화 도구
# 사용법:
#   ADMIN_KEY=... ./start-admin.sh                            # 관리자 서버 시작
#   NOTION_TOKEN=... ./start-admin.sh sync-from-notion        # Notion 스냅샷 갱신 (Notion → repo)
#   NOTION_TOKEN=... ./start-admin.sh sync-all                # Notion snapshot 갱신만 실행
#   NOTION_TOKEN=... ./start-admin.sh sync-to-notion-force    # ⚠️ 위험: Notion 본문 덮어쓰기 (deprecated)
#
# Notion이 SoT(2026-04-06 결정). sync-to-notion은 안전상 비활성화됨.
# 비밀번호는 반드시 환경변수로 주입하세요.

set -euo pipefail

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

# 동기화 명령 처리
case "$1" in
  sync-from-notion)
    echo "📥 Notion 스냅샷을 가져오는 중..."
    python3 "$SCRIPT_DIR/tools/notion-sync.py" --fetch-only
    exit $?
    ;;

  sync-to-notion)
    echo "⚠️  sync-to-notion DEPRECATED — Notion이 SoT (2026-04-06 결정)" >&2
    echo "    이 명령은 Notion 페이지 본문을 덮어씁니다." >&2
    echo "    정말 필요하면: ./start-admin.sh sync-to-notion-force" >&2
    echo "    또는: python3 tools/curriculum-push.py --confirm-destructive" >&2
    exit 3
    ;;

  sync-to-notion-force)
    echo "🚨 DESTRUCTIVE: Notion 페이지 본문을 단순 구조로 덮어씁니다."
    python3 "$SCRIPT_DIR/tools/curriculum-push.py" --confirm-destructive
    exit $?
    ;;

  sync-all)
    echo "🔄 Notion snapshot 갱신 (Notion → repo, 단방향)"
    echo ""
    python3 "$SCRIPT_DIR/tools/notion-sync.py" --fetch-only
    exit $?
    ;;

  *)
    if [ -z "${ADMIN_KEY:-}" ]; then
      echo "ERROR: ADMIN_KEY 환경변수가 필요합니다." >&2
      echo "예: ADMIN_KEY=change-me ./start-admin.sh" >&2
      exit 1
    fi
    python3 "$SCRIPT_DIR/tools/admin-server.py" "$@"
    exit $?
    ;;
esac
