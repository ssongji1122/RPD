# Curriculum 핵심 파일 경로

| 파일 | 역할 |
|------|------|
| `course-site/data/curriculum.json` | 최종 merge 결과 (GENERATED — 직접 수정 금지) |
| `course-site/data/curriculum-notion.json` | Notion snapshot (GENERATED — 직접 수정 금지) |
| `course-site/data/curriculum.js` | curriculum.json wrapper (GENERATED) |
| `course-site/data/overrides.json` | 코드 에셋 필드 (image, showme, status, videos, done) |
| `tools/notion-sync.py` | Notion fetch + merge 스크립트 |
| `tools/notion_api.py` | Notion API 공유 모듈 |
| `tools/notion-mapping.json` | week → Notion page ID 매핑 |
| `course-site/assets/images/weekNN/` | 주차별 이미지 디렉토리 |
| `course-site/assets/showme/` | Show Me 카드 HTML 파일들 |
| `course-site/assets/showme/_registry.js` | Show Me 위젯 레지스트리 |
