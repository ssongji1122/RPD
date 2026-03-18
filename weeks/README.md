# Weeks Authoring Guide

## Source of Truth

RPD 공개 커리큘럼의 canonical source는 `weeks/site-data.json`입니다.

- 수정 대상: `weeks/site-data.json`
- 계약 정의: `weeks/contracts.schema.json`
- 사이트 스키마: `weeks/site-data.schema.json`
- 시작 템플릿: `weeks/templates/sample-course-template.json`

## Workflow

```bash
python3 tools/content_pipeline.py check
python3 tools/content_pipeline.py sync-from-markdown
python3 tools/content_pipeline.py build
python3 tools/content_pipeline.py build-public --output dist/public-site
```

관리자 UI를 사용할 때도 저장 결과는 다시 `weeks/site-data.json`으로 들어갑니다.
`sync-from-markdown`은 lecture-note의 관리 블록과 assignment.md를 읽어서 canonical JSON을 다시 세울 수 있는 복구/검증 경로입니다.

## Editing Rules

- 주차 번호는 고유해야 합니다.
- 각 주차는 최소 1개 이상의 `topic`, `step`, `assignment.checklist`를 가져야 합니다.
- 각 step은 최소 1개 이상의 `task`를 가져야 합니다.
- task id는 같은 주차 안에서 중복되면 안 됩니다.

## Publish

- Notion 스냅샷 fetch: `python3 tools/notion-sync.py --fetch-only`
- Notion publish: `python3 tools/curriculum-push.py`
- Markdown → canonical 검증: `python3 tools/content_pipeline.py sync-from-markdown`

중요:

- Notion은 source of truth가 아닙니다.
- 공개 배포는 `dist/public-site` 산출물만 사용합니다.
