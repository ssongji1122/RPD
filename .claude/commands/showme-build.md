---
name: showme-build
description: |
  Notion Card DB → ShowMe HTML 생성. 단일 카드/주차/전체 모드.
  카드 1개: /showme-build {card_id}
  주차 전체: /showme-build week N
  전체: /showme-build all
  사용 시점: Notion에서 카드 수정 후 사이트 발행 전, 새 카드 생성 후, 마이그레이션 후.
---

# /showme-build

Notion **ShowMe Cards** DB를 SSoT로 두고, 각 row를 `course-site/assets/showme/{card_id}.html` 로 빌드한다. 파생 인덱스 `_registry.js`, `_catalog.json` 도 함께 재생성.

## 호출 방식

- `/showme-build {card_id}` — 단일 카드. 예: `/showme-build array-modifier`
- `/showme-build week {N}` — 주차 N의 모든 카드. 예: `/showme-build week 3`
- `/showme-build all` — 전체 published 카드

## 실행 흐름

1. `tools/showme_db_ids.json` 존재 확인. 없으면 사용자에게 `tools/showme_create_dbs.py` 먼저 실행 안내.
2. argument 매칭에 따라 적절한 `python3 tools/showme_build.py` 명령 구성:
   - `{card_id}` → `--card {card_id}`
   - `week {N}` → `--week {N}`
   - `all` → `--all`
3. 실행. 출력 로그를 그대로 보여줌.
4. 오류 시 그대로 표기. 422 / 401 / 404 의 경우 토큰 또는 DB id 점검 안내.

## 사전 조건

- `NOTION_TOKEN` 환경변수 또는 `tools/notion-mapping.json` 의 token 필드 설정
- `tools/showme_db_ids.json` 존재 (없으면 `showme_create_dbs.py` 부트스트랩 필요)
- `course-site/assets/showme/_template.v2.html` 존재

## 후속

빌드 후 `/sync` 또는 `/rpd-check` 로 사이트 발행 + 검증.
