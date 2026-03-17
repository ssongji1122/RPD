#!/bin/bash
# RPD Admin Server 시작 스크립트 + 동기화 도구
# 사용법:
#   ./start-admin.sh              # 관리자 서버 시작
#   ./start-admin.sh sync-from-notion    # Notion → 웹 동기화
#   ./start-admin.sh sync-to-notion      # 웹 → Notion 동기화
#   ./start-admin.sh sync-all            # 양방향 동기화
#
# 비밀번호 설정: 이 파일을 열고 ADMIN_KEY= 뒤에 원하는 비밀번호를 입력하세요.
# (이 파일은 .gitignore에 추가 권장)

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
ADMIN_KEY="5059"

# 동기화 명령 처리
case "$1" in
  sync-from-notion)
    # Notion → overrides.json 동기화
    echo "📥 Notion 데이터를 웹으로 동기화 중..."
    node "$SCRIPT_DIR/tools/notion-sync.js" --all
    exit $?
    ;;

  sync-to-notion)
    # 학생 진행도를 Notion에 동기화
    echo "📤 학생 진행도를 Notion에 동기화 중..."
    node "$SCRIPT_DIR/tools/web-to-notion.js" --all
    exit $?
    ;;

  sync-all)
    # 양방향 동기화
    echo "🔄 양방향 동기화 시작..."

    echo ""
    echo "📥 Step 1: Notion → 웹"
    node "$SCRIPT_DIR/tools/notion-sync.js" --all
    SYNC_FROM_STATUS=$?

    echo ""
    echo "📤 Step 2: 웹 → Notion"
    node "$SCRIPT_DIR/tools/web-to-notion.js" --all
    SYNC_TO_STATUS=$?

    if [ $SYNC_FROM_STATUS -eq 0 ] && [ $SYNC_TO_STATUS -eq 0 ]; then
      echo ""
      echo "✓ 양방향 동기화 완료"
      exit 0
    else
      echo ""
      echo "⚠ 일부 동기화가 실패했습니다"
      exit 1
    fi
    ;;

  *)
    # 기본: 관리자 서버 시작
    ADMIN_KEY="$ADMIN_KEY" \
    python3 "$SCRIPT_DIR/tools/admin-server.py" "$@"
    exit $?
    ;;
esac
