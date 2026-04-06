#!/bin/bash
# remind_submissions.py 자동 실행 래퍼
# crontab에서 호출: run_remind.sh [class_num]
#   class_num: 1 또는 2

CLASS="${1:-1}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
LOG_FILE="$PROJECT_DIR/tools/remind_${CLASS}.log"

cd "$PROJECT_DIR" || exit 1

# .env에서 환경변수 로드
if [ -f "$PROJECT_DIR/.env" ]; then
    export $(grep -v '^#' "$PROJECT_DIR/.env" | xargs)
fi

echo "=============================" >> "$LOG_FILE"
echo "$(date '+%Y-%m-%d %H:%M:%S') - ${CLASS}반 리마인더 시작" >> "$LOG_FILE"

python3 "$SCRIPT_DIR/remind_submissions.py" --class "$CLASS" >> "$LOG_FILE" 2>&1
EXIT_CODE=$?

echo "$(date '+%Y-%m-%d %H:%M:%S') - 완료 (exit: $EXIT_CODE)" >> "$LOG_FILE"
exit $EXIT_CODE
