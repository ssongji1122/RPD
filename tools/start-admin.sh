#!/bin/bash
# RPD Admin 서버 + Cloudflare Tunnel 실행

PORT=8765
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

# .env 로드
if [ -f "$REPO_ROOT/.env" ]; then
  export $(grep -v '^#' "$REPO_ROOT/.env" | xargs)
fi

# admin server 시작 (백그라운드)
echo "🚀 Admin 서버 시작 중 (port $PORT)..."
cd "$REPO_ROOT"
python3 tools/admin-server.py --port $PORT &
ADMIN_PID=$!

# 서버 뜰 때까지 대기
sleep 1

# Cloudflare Tunnel 시작
echo "🌐 Cloudflare Tunnel 연결 중..."
echo "   URL이 아래에 표시됩니다 (https://....trycloudflare.com)"
echo "   종료하려면 Ctrl+C"
echo ""

cleanup() {
  echo ""
  echo "종료 중..."
  kill $ADMIN_PID 2>/dev/null
  exit 0
}
trap cleanup INT TERM

cloudflared tunnel --url http://localhost:$PORT
