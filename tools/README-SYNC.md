# RPD Sync Overview

현재 canonical 저장은 `repo-first`지만, 실무 편집 흐름은 `notion-first`로 운영할 수 있습니다.

- 공개 사이트의 소스 오브 트루스: `weeks/site-data.json`
- 생성 산출물: `course-site/data/curriculum.json`, `course-site/data/curriculum.js`
- Notion 역할: 읽기 전용 스냅샷(`course-site/data/curriculum-notion.json`) + 선택적 publish 대상
- 관리자 API 역할: 로컬에서만 실행되는 비공개 편집/업로드/배포 도구

추가로, 실무 운영에서 Notion을 먼저 수정하고 repo를 따라오게 하고 싶다면 `notion-first 운영 모드`를 사용할 수 있습니다.

- 콘텐츠 수정: Notion
- 웹 전용 보강: `course-site/data/overrides.json`
- 반영 명령: `NOTION_TOKEN=... python3 tools/notion-sync.py --apply`

이 명령은 `curriculum-notion.json` 스냅샷을 갱신한 뒤, `overrides.json`과 병합해서 `weeks/site-data.json` 및 생성 산출물까지 한 번에 갱신합니다.

## Quick Start

```bash
# 1) 환경변수 준비
cp .env.example .env

# 2) canonical curriculum 검증 + 생성
python3 tools/content_pipeline.py check
python3 tools/content_pipeline.py sync-from-markdown
python3 tools/content_pipeline.py build

# 3) 관리자 서버 실행 (반드시 환경변수로 비밀번호 주입)
ADMIN_KEY=change-me python3 tools/admin-server.py --host 127.0.0.1 --port 8765

# 4) Notion 스냅샷만 가져오기
NOTION_TOKEN=... python3 tools/notion-sync.py --fetch-only

# 4-1) Notion 스냅샷을 canonical/generated outputs에 바로 반영하기
NOTION_TOKEN=... python3 tools/notion-sync.py --apply

# 5) canonical curriculum을 Notion으로 push
NOTION_TOKEN=... python3 tools/curriculum-push.py
```

## Secrets

- `ADMIN_KEY`, `NOTION_TOKEN`은 파일이 아니라 환경변수로만 주입합니다.
- `course-site/data/notion-config.json` 같은 평문 시크릿 파일은 더 이상 사용하지 않습니다.
- 원격 터널이 필요하면 `ALLOW_REMOTE_TUNNEL=1`을 명시적으로 설정해야 합니다.

## Public vs Private

- GitHub Pages에는 `tools/content_pipeline.py build-public --output dist/public-site` 결과만 배포합니다.
- 아래 파일들은 public artifact에 포함되면 안 됩니다.
  - `course-site/admin.html`
  - `course-site/data/notion-config*.json`
  - `course-site/data/students.*`
  - `course-site/data/curriculum-notion.json`
  - `course-site/data/overrides.json`

## Main Commands

- `python3 tools/content_pipeline.py check`
  - canonical curriculum 유효성 검사
- `python3 tools/content_pipeline.py build`
  - public data 파일 생성
- `python3 tools/content_pipeline.py sync-from-markdown`
  - lecture-note 관리 블록과 assignment.md를 읽어 canonical curriculum 복구/검증
- `python3 tools/content_pipeline.py build-public --output dist/public-site`
  - 배포 산출물 생성 + 민감 데이터 스캔
- `python3 tools/notion-sync.py --fetch-only`
  - Notion 스냅샷 갱신
- `python3 tools/notion-sync.py --apply`
  - Notion 스냅샷 + overrides를 canonical curriculum과 생성 산출물에 반영
- `python3 tools/curriculum-push.py --week 3`
  - 특정 주차만 Notion으로 push

## Tests

```bash
python3 -m unittest discover -s tools/tests -p 'test_*.py'
python3 -m pip install -e ./tools/lessonforge[dev]
PYTHONPATH=tools/lessonforge/src python3 -m pytest tools/lessonforge/tests -q
```

세부 운영 절차는 [tools/SYNC_GUIDE.md](/Users/ssongji/Developer/Workspace/RPD/tools/SYNC_GUIDE.md)를 보면 됩니다.
