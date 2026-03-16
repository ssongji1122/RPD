# curriculum.js → Notion Push 설계

**날짜:** 2026-03-17
**소스오브트루스:** `course-site/data/curriculum.js` (웹 기준)
**방향:** 웹 → 노션 단방향 push

---

## 배경

기존 `notion-sync.py`는 Notion → curriculum.js 방향이었음.
curriculum.js가 실제로 더 자주 수정되고, git으로 관리되므로 웹을 소스오브트루스로 확정.
노션은 학생/외부 공유용 뷰어로만 사용.

---

## 아키텍처

```
curriculum.js (소스오브트루스)
    ↓ CLI 또는 admin UI
sync_week_to_notion()  ← 기존 notion_api.py 함수 재사용
    ↓
Notion Pages (주차별)
```

---

## 구현 항목

### 1. `tools/curriculum-push.py` (신규)

```
python3 tools/curriculum-push.py           # 전체 15주
python3 tools/curriculum-push.py --week 3  # 특정 주차
python3 tools/curriculum-push.py --weeks 1 2 3  # 복수 주차
```

- `curriculum.js` 파싱 → 주차 데이터 추출
- `sync_week_to_notion()` 호출 (notion_api.py 재사용)
- 주차별 성공/실패 출력
- exit 0: 성공, exit 1: 에러, exit 2: 변경 없음

### 2. `tools/admin-server.py` 수정

엔드포인트 추가:
- `POST /api/notion-push-all` — 전체 주차 push, `{"results": [{"week": 1, "ok": true, "title": "..."}, ...]}` 반환

### 3. Admin UI 수정

- 기존 주차별 push 버튼 근처에 "전체 Notion Push" 버튼 추가
- 클릭 시 `/api/notion-push-all` 호출
- 결과를 주차별 ✓/✗ 리스트로 표시

---

## 파일 변경 목록

| 파일 | 변경 |
|------|------|
| `tools/curriculum-push.py` | 신규 생성 |
| `tools/admin-server.py` | `/api/notion-push-all` 엔드포인트 추가 |
| admin UI HTML (admin-server.py 내 인라인) | "전체 Push" 버튼 + 결과 로그 창 추가 |

---

## 재사용하는 기존 코드

- `notion_api.py: sync_week_to_notion(week, token)` — 주차 데이터를 Notion에 씀
- `notion_api.py: get_notion_token()` — NOTION_TOKEN 환경변수 읽기
- `notion_api.py: load_notion_mapping()` — week → Notion page ID 매핑
