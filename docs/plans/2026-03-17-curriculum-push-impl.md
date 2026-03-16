# curriculum.js → Notion Push Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** curriculum.js를 소스오브트루스로 하여 Notion에 단방향 push하는 CLI + Admin UI 구현

**Architecture:** sync_week_to_notion() (기존 notion_api.py 함수)를 공유 코어로 사용. CLI(curriculum-push.py)와 admin-server(/api/notion-push-all)가 독립적으로 이 함수를 호출. Admin HTML에 전체 push 버튼 + 결과 로그 추가.

**Tech Stack:** Python 3 (stdlib only), vanilla JS, 기존 notion_api.py

---

## 주요 파일 위치

- 핵심 함수: tools/notion_api.py — sync_week_to_notion(week, token)
- 기존 CLI 참고: tools/notion-sync.py (Notion→web 방향, 구조 참고)
- Admin 서버: tools/admin-server.py (1177줄) — 673번째 줄 근처에 notion-push 라우트
- Admin UI: course-site/admin.html — 606번째 줄에 notionGroup, 1625번째 줄에 notionPullBtn 이벤트

---

## Task 1: CLI tools/curriculum-push.py 작성

**Files:**
- Create: tools/curriculum-push.py

**Step 1: 파일 생성**

tools/curriculum-push.py 를 아래 내용으로 작성:

```
#!/usr/bin/env python3
"""
curriculum-push.py — curriculum.js → Notion 단방향 push
=========================================================
Usage:
    python3 tools/curriculum-push.py              # 전체 15주
    python3 tools/curriculum-push.py --week 3     # Week 3만
    python3 tools/curriculum-push.py --weeks 1 2 3  # 복수 주차

Exit codes:
    0: 성공 (1개 이상 push)
    1: 에러
    2: push할 주차 없음
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from notion_api import get_notion_token, load_notion_mapping, sync_week_to_notion

ROOT = Path(__file__).resolve().parent.parent
CURRICULUM_JS = ROOT / "course-site" / "data" / "curriculum.js"


def load_curriculum() -> list[dict]:
    text = CURRICULUM_JS.read_text(encoding="utf-8")
    match = re.search(r"const CURRICULUM\s*=\s*(\[.*?\])\s*;", text, re.DOTALL)
    if not match:
        raise ValueError("curriculum.js에서 CURRICULUM 배열을 찾을 수 없음")
    return json.loads(match.group(1))


def push_weeks(weeks: list[dict], token: str) -> tuple[int, int]:
    mapping = load_notion_mapping()
    ok = 0
    fail = 0
    for week in weeks:
        week_num = str(week.get("week", ""))
        if week_num not in mapping:
            print(f"⚠ Week {week_num}: notion-mapping.json에 매핑 없음, 건너뜀")
            continue
        try:
            sync_week_to_notion(week, token)
            title = week.get("title", "(untitled)")
            print(f"✓ Week {week_num.zfill(2)}: {title}")
            ok += 1
        except Exception as exc:
            print(f"✗ Week {week_num}: {exc}", file=sys.stderr)
            fail += 1
    return ok, fail


def main() -> int:
    parser = argparse.ArgumentParser(description="curriculum.js → Notion push")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--week", type=int, metavar="N", help="특정 주차만 push")
    group.add_argument("--weeks", type=int, nargs="+", metavar="N", help="복수 주차 push")
    args = parser.parse_args()

    token = get_notion_token()
    if not token:
        print("Error: NOTION_TOKEN 환경변수가 설정되지 않음", file=sys.stderr)
        return 1

    try:
        all_weeks = load_curriculum()
    except Exception as exc:
        print(f"Error: curriculum.js 읽기 실패 — {exc}", file=sys.stderr)
        return 1

    if args.week:
        target_nums = {args.week}
    elif args.weeks:
        target_nums = set(args.weeks)
    else:
        target_nums = None

    if target_nums is not None:
        weeks_to_push = [w for w in all_weeks if w.get("week") in target_nums]
        missing = target_nums - {w.get("week") for w in weeks_to_push}
        for n in sorted(missing):
            print(f"⚠ Week {n}: curriculum.js에 없음", file=sys.stderr)
    else:
        weeks_to_push = all_weeks

    if not weeks_to_push:
        print("push할 주차가 없습니다.")
        return 2

    print(f"Pushing {len(weeks_to_push)} week(s) to Notion...")
    ok, fail = push_weeks(weeks_to_push, token)
    print(f"\nDone — {ok} succeeded, {fail} failed.")
    return 0 if ok > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
```

**Step 2: 실행 권한**

```bash
chmod +x tools/curriculum-push.py
```

**Step 3: 파싱 확인**

```bash
python3 -c "
import sys, json, re
from pathlib import Path
text = Path('course-site/data/curriculum.js').read_text()
m = re.search(r'const CURRICULUM\s*=\s*(\[.*?\])\s*;', text, re.DOTALL)
weeks = json.loads(m.group(1))
print(f'OK: {len(weeks)} weeks loaded')
"
```

Expected: `OK: 15 weeks loaded`

**Step 4: NOTION_TOKEN 없을 때 에러 확인**

```bash
python3 tools/curriculum-push.py --week 1
```

Expected: `Error: NOTION_TOKEN 환경변수가 설정되지 않음` (exit 1)

**Step 5: 커밋**

```bash
git add tools/curriculum-push.py
git commit -m "feat: curriculum.js → Notion push CLI 추가"
```

---

## Task 2: admin-server.py에 /api/notion-push-all 추가

**Files:**
- Modify: tools/admin-server.py

**Step 1: import 확인**

```bash
grep "load_notion_mapping" tools/admin-server.py
```

없으면 admin-server.py 상단 notion_api import에 load_notion_mapping 추가.

**Step 2: 라우트 추가**

admin-server.py 675번째 줄 근처 (notion-push 라우트 바로 아래):

현재:
```
# POST /api/notion-push/{weekNum}
notion_push_match = re.match(r"^/api/notion-push/(\d+)$", path)
if notion_push_match:
    week_num = int(notion_push_match.group(1))
    self._handle_notion_push(week_num)
    return

# POST /api/notion-pull/{weekNum}
```

변경 후 (notion-push 블록과 notion-pull 블록 사이에 추가):
```
# POST /api/notion-push-all
if path == "/api/notion-push-all":
    self._handle_notion_push_all()
    return
```

**Step 3: _handle_notion_push_all 메서드 추가**

_handle_notion_push 메서드(948번째 줄 근처) 바로 아래에 추가:

```
def _handle_notion_push_all(self) -> None:
    """Push all curriculum weeks to Notion."""
    if not NOTION_TOKEN:
        self._send_error_json(503, "NOTION_TOKEN not configured")
        return

    try:
        data = read_curriculum()
    except Exception as exc:
        self._send_error_json(500, f"Read failed: {exc}")
        return

    mapping = load_notion_mapping()
    results = []
    for week in data:
        week_num = week.get("week")
        if str(week_num) not in mapping:
            results.append({
                "week": week_num,
                "ok": False,
                "error": "no mapping",
                "title": week.get("title", ""),
            })
            continue
        try:
            sync_week_to_notion(week)
            results.append({"week": week_num, "ok": True, "title": week.get("title", "")})
        except Exception as exc:
            results.append({
                "week": week_num,
                "ok": False,
                "error": str(exc),
                "title": week.get("title", ""),
            })

    ok_count = sum(1 for r in results if r["ok"])
    self._send_json({"results": results, "ok": ok_count, "total": len(results)})
```

**Step 4: 서버 구문 오류 확인**

```bash
python3 -m py_compile tools/admin-server.py && echo "OK"
```

Expected: `OK`

**Step 5: NOTION_TOKEN 없이 API 테스트**

```bash
# 터미널 1
python3 tools/admin-server.py &
sleep 1

# 터미널 2
curl -s -X POST http://localhost:8000/api/notion-push-all | python3 -m json.tool
```

Expected: 503 + `{"error": "NOTION_TOKEN not configured"}`

```bash
kill %1  # 서버 종료
```

**Step 6: 커밋**

```bash
git add tools/admin-server.py
git commit -m "feat: admin-server에 /api/notion-push-all 엔드포인트 추가"
```

---

## Task 3: Admin UI — 버튼 + 결과 모달

**Files:**
- Modify: course-site/admin.html

**Step 1: 버튼 추가**

606번째 줄 notionGroup div 내부, notionPullBtn 바로 뒤에 버튼 추가:

현재:
```html
<button class="btn btn-ghost" id="notionPullBtn" type="button" title="Notion에서 동기화">&#128260; 지금 동기화</button>
```

추가 후:
```html
<button class="btn btn-ghost" id="notionPullBtn" type="button" title="Notion에서 동기화">&#128260; 지금 동기화</button>
<button class="btn btn-ghost" id="notionPushAllBtn" type="button" title="curriculum.js → Notion 전체 push">&#128640; 전체 Push</button>
```

**Step 2: 결과 모달 HTML 추가**

auth-overlay div 바로 아래(닫는 div 다음)에 추가:

```html
<!-- Notion Push All 결과 모달 -->
<div class="auth-overlay" id="pushAllOverlay" style="display:none">
  <div class="auth-card" style="max-width:480px;width:90%">
    <h2>Notion 전체 Push 결과</h2>
    <div id="pushAllLog" style="font-size:.85rem;line-height:1.8;max-height:320px;overflow-y:auto;margin:12px 0;font-family:monospace"></div>
    <button class="btn btn-primary" id="pushAllCloseBtn" type="button" style="width:100%;justify-content:center;">닫기</button>
  </div>
</div>
```

**Step 3: JS DOM ref 추가**

`var notionPullBtn = document.getElementById("notionPullBtn");` 바로 아래에:

```javascript
var notionPushAllBtn = document.getElementById("notionPushAllBtn");
var pushAllOverlay   = document.getElementById("pushAllOverlay");
var pushAllLog       = document.getElementById("pushAllLog");
var pushAllCloseBtn  = document.getElementById("pushAllCloseBtn");
```

**Step 4: JS 이벤트 핸들러 추가**

notionPullBtn.addEventListener(...) 블록 바로 아래에:

```javascript
notionPushAllBtn.addEventListener("click", async function() {
  pushAllLog.innerHTML = "<span style='color:#aaa'>전체 push 중...</span>";
  pushAllOverlay.style.display = "flex";
  notionPushAllBtn.disabled = true;

  try {
    var res = await fetch("/api/notion-push-all", {
      method: "POST",
      headers: apiHeaders(),
    });
    var data = await res.json();

    if (!res.ok) {
      pushAllLog.innerHTML = "<span style='color:#f66'>오류: " + esc(data.error || "Unknown") + "</span>";
      return;
    }

    var lines = data.results.map(function(r) {
      var icon = r.ok ? "✓" : "✗";
      var color = r.ok ? "#6f6" : "#f66";
      var detail = r.ok ? "" : " — " + esc(r.error || "");
      return "<span style='color:" + color + "'>" + icon + " Week " +
        String(r.week).padStart(2, "0") + ": " + esc(r.title) + detail + "</span>";
    });
    lines.push("");
    lines.push("<strong>완료: " + data.ok + "/" + data.total + " 성공</strong>");
    pushAllLog.innerHTML = lines.join("<br>");
  } catch(e) {
    pushAllLog.innerHTML = "<span style='color:#f66'>연결 실패: " + esc(e.message) + "</span>";
  } finally {
    notionPushAllBtn.disabled = false;
  }
});

pushAllCloseBtn.addEventListener("click", function() {
  pushAllOverlay.style.display = "none";
});
```

**Step 5: HTML 검증**

```bash
python3 -c "
from html.parser import HTMLParser
class Check(HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors = []
Check().feed(open('course-site/admin.html').read())
print('HTML parse OK')
"
```

Expected: `HTML parse OK`

**Step 6: 커밋**

```bash
git add course-site/admin.html
git commit -m "feat: admin UI에 전체 Notion Push 버튼 + 결과 모달 추가"
```

---

## 완료 기준

- [ ] python3 tools/curriculum-push.py — NOTION_TOKEN 없으면 에러 메시지 출력
- [ ] python3 tools/curriculum-push.py --week 1 --weeks 1 2 3 플래그 동작
- [ ] python3 -m py_compile tools/admin-server.py — 구문 오류 없음
- [ ] POST /api/notion-push-all — {"results": [...], "ok": N, "total": 15} 형태 반환
- [ ] Admin UI "전체 Push" 버튼 클릭 → 모달 표시
- [ ] 모달 "닫기" 버튼 동작
