# RPD Project Rules

## 콘텐츠 관리 규칙

### Generated Files — 직접 수정 금지
다음 파일은 자동 생성되므로 Edit/Write tool로 직접 수정하지 않는다:
- `course-site/data/curriculum.json`
- `course-site/data/curriculum-notion.json`
- `course-site/data/curriculum.js`

이 파일들을 수정하라는 요청을 받으면, 아래 수정 경로를 따른다.

### 수정 경로
| 수정 대상 | 수정 위치 | 도구 |
|-----------|----------|------|
| step title/copy/tasks/goal/assignment/shortcuts/mistakes/docs | Notion | Notion MCP (mcp__notion__*) |
| image, showme, status, videos, done, summary | overrides.json | Edit tool |
| showme 카드 HTML/supplement | course-site/assets/showme/ | /showme 스킬 |

### 수정 후 필수 절차
1. Notion 수정 시: `python3 tools/notion-sync.py --fetch-only` 실행
2. curriculum.json 재생성 확인
3. `/rpd-check` 검증
