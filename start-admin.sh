#!/bin/bash
# RPD Admin Server 시작 스크립트 + 동기화 도구
# 사용법:
#   ADMIN_KEY=... ./start-admin.sh              # 관리자 서버 시작
#   NOTION_TOKEN=... ./start-admin.sh sync-from-notion    # Notion 스냅샷 갱신
#   NOTION_TOKEN=... ./start-admin.sh sync-to-notion      # canonical curriculum → Notion push
#   ADMIN_KEY=... NOTION_TOKEN=... ./start-admin.sh sync-all
#
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
    echo "📤 Canonical curriculum을 Notion에 push 중..."
    python3 "$SCRIPT_DIR/tools/curriculum-push.py"
    exit $?
    ;;

  sync-all)
    echo "🔄 스냅샷 갱신 + curriculum push 시작..."

    echo ""
    echo "📥 Step 1: Notion snapshot"
    python3 "$SCRIPT_DIR/tools/notion-sync.py" --fetch-only
    SYNC_FROM_STATUS=$?

    echo ""
    echo "📤 Step 2: Canonical curriculum push"
    python3 "$SCRIPT_DIR/tools/curriculum-push.py"
    SYNC_TO_STATUS=$?

    if [ $SYNC_FROM_STATUS -eq 0 ] && [ $SYNC_TO_STATUS -eq 0 ]; then
      echo ""
      echo "✓ 동기화 완료"
      exit 0
    else
      echo ""
      echo "⚠ 일부 동기화가 실패했습니다"
      exit 1
    fi
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
