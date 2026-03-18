# RPD Sync Guide

## Operating Model

RPD는 이제 `Notion-first`가 아니라 `repo-first`로 운영합니다.

1. `weeks/site-data.json`이 canonical curriculum입니다.
2. `tools/content_pipeline.py build`가 공개 사이트용 데이터를 생성합니다.
3. 관리자 서버는 canonical data를 수정하고, 저장 시 public data를 다시 생성합니다.
4. Notion은 두 가지 용도로만 사용합니다.
   - 읽기 전용 스냅샷 보관: `course-site/data/curriculum-notion.json`
   - 선택적 publish 대상

## Source Map

```text
weeks/site-data.json                canonical curriculum
weeks/contracts.schema.json        versioned contracts
course-site/data/curriculum.json   generated public JSON
course-site/data/curriculum.js     generated public JS
course-site/data/curriculum-notion.json   Notion snapshot only
tools/admin-server.py              private admin API
tools/content_pipeline.py          validation/build/public packaging
tools/notion-sync.py               Notion snapshot fetch
tools/curriculum-push.py           canonical curriculum -> Notion push
```

## Environment

`.env.example` 기준으로 아래 값을 설정합니다.

```bash
export ADMIN_KEY="change-me"
export NOTION_TOKEN="ntn_..."
export HOST="127.0.0.1"
export PORT="8765"
```

중요:

- `ADMIN_KEY`가 없으면 관리자 서버는 시작하지 않습니다.
- `NOTION_TOKEN`은 Notion fetch/push 작업에서만 필요합니다.
- 시크릿은 `course-site/data/*.json`에 저장하지 않습니다.

## Local Admin Flow

```bash
ADMIN_KEY=change-me ./start-admin.sh
```

관리자 UI 흐름:

1. 로그인
2. 주차 수정
3. 이미지/영상 업로드
4. `변경 미리보기`로 diff 확인
5. 저장
6. 필요하면 `Notion Push` 실행

서버는 기본적으로 `127.0.0.1`에만 바인딩됩니다.

## Notion Snapshot

```bash
NOTION_TOKEN=... python3 tools/notion-sync.py --fetch-only
```

이 명령은 `course-site/data/curriculum-notion.json`만 갱신합니다.
public data나 canonical curriculum은 변경하지 않습니다.

## Notion Publish

```bash
NOTION_TOKEN=... python3 tools/curriculum-push.py
NOTION_TOKEN=... python3 tools/curriculum-push.py --week 3
```

push 소스는 항상 `weeks/site-data.json`입니다.

## Public Build

```bash
python3 tools/content_pipeline.py check
python3 tools/content_pipeline.py sync-from-markdown
python3 tools/content_pipeline.py build-public --output dist/public-site
```

public build는 아래 파일이 포함되면 실패합니다.

- `admin.html`
- `data/notion-config.json`
- `data/notion-config.local.json`
- `data/students.js`
- `data/students.json`
- `data/curriculum-notion.json`
- `data/overrides.json`

또한 토큰/세션 헤더/학생 roster 흔적을 스캔합니다.

`python3 tools/content_pipeline.py sync-from-markdown` 은
lecture-note의 관리 블록과 assignment.md를 읽어 canonical curriculum을 다시 만들 수 있는 검증/복구 경로입니다.

## CI Expectations

- `python3 tools/content_pipeline.py check`
- `python3 tools/content_pipeline.py build`
- `python3 tools/content_pipeline.py build-public --output dist/public-site`
- `python3 -m unittest discover -s tools/tests -p 'test_*.py'`
- `PYTHONPATH=tools/lessonforge/src python3 -m pytest tools/lessonforge/tests -q`

## Audit Log

관리자 서버는 주요 쓰기 작업을 `tmp/admin-audit.log`에 JSONL 형식으로 기록합니다.

- 로그인/로그아웃
- 커리큘럼 저장
- 상태 변경
- 파일 업로드
- Notion push

## Remote Access

원격 노출은 기본 비활성입니다.

```bash
ALLOW_REMOTE_TUNNEL=1 ADMIN_KEY=... ./tools/start-admin.sh
```

이 값이 없으면 터널 스크립트는 종료됩니다.
