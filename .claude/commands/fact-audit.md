---
description: "사실 검증", "fact-audit", "콘텐츠 감사" 요청 시 호출. 주차 수업자료의 깨진 자산·노후 사실을 검증하는 감사.
allowed-tools: Read, Glob, Grep, Bash(python3:*), Bash(curl:*), Bash(git:*), Agent
---

# Fact Audit — 주차 콘텐츠 사실 검증

## 목적

주차 수업자료(lecture-note.md, site-data.json, overrides.json)에서 깨진 자산 참조와 노후된 사실 주장(도구명·가격·크레딧·버전·단축키·기능)을 찾아 검증하고, 명백한 오류는 즉시 반영·판단이 필요한 항목은 결재 큐로 분리한다.

## 사용

```
/fact-audit W05
```

주차 번호를 인자로 받는다. 인자가 없으면 어느 주차를 감사할지 되묻는다.

## 절차

### L1 — 기계 검사

- 해당 주차 `lecture-note.md`, `weeks/site-data.json`에 포함된 외부 URL을 `curl -sI`로 상태 코드 확인
- `course-site/assets/images/week##/` 아래 이미지 중 15KB 미만 파일을 플레이스홀더 의심으로 표시, Read로 육안 판정
- `weeks/site-data.json`·`course-site/data/overrides.json`·`course-site/data/curriculum.js`에서 해당 주차 image 필드가 실존 자산을 가리키는지 대조

### L2 — 사실 검증

- lecture-note.md에서 도구명·가격·크레딧·버전·단축키·기능 주장을 추출
- 항목별로 웹서치 기반 검증(공식 소스 우선) — 서브에이전트(fact-checker) 병렬 투입 가능
- 각 판정에 결과 + 근거 URL + 확인 기준일을 남긴다

### L3 — 반영

| 유형 | 처리 |
|------|------|
| 깨진 참조(플레이스홀더 이미지, 404 링크) | 즉시 제거·수정 |
| 환각 기능(존재하지 않는 기능 서술) | 즉시 삭제 |
| 잘못된 단축키 | 즉시 공식 문서 기준으로 교정 |
| 수치·가격·크레딧 변경 | `docs/content-audit/YYYY-MM-DD-w##-pending-updates.md` 결재 큐로 |
| 도구 교체 판단(서비스 중단·대체 필요) | 결재 큐로 |

### 수정 반영 경로

- `lecture-note.md`는 repo에서 직접 수정 후 notion-push 워크플로우로 Notion 반영
- step 구조·이미지는 `course-site/data/overrides.json` 또는 `course-site/data/curriculum.js`가 아니라 **`weeks/site-data.json`(canonical)을 수정** 후 `python3 tools/content_pipeline.py build`로 재생성 — `curriculum.js`는 자동 생성 파일이라 직접 편집 금지
- `notion-sync`(30분 주기)가 덮어쓰는 파일(`weeks/site-data.json`의 notion 동기화분, `curriculum-notion.json`, `notion-blocks/`)은 sync 타이밍에 따라 되돌아갈 수 있으므로, notion 쪽에도 결재된 수정을 반영해야 한다

## 주의

- 로컬 main이 뒤처져 있을 수 있으므로 `git fetch origin` 후 `origin/main` 기준 worktree에서 작업
- overrides.json은 `load_notion_first_curriculum` 경로(Notion 동기화)에서만 적용되고 일반 `build` 명령에는 반영되지 않는다 — canonical 데이터는 `weeks/site-data.json`
- lecture-note.md의 `<!-- AUTO:CURRICULUM-SYNC:START -->` 블록은 `content_pipeline.py build` 실행 시 curriculum.js 기준으로 자동 덮어써진다 — 이 블록을 손으로 고치지 말 것

## 검증

```bash
python3 tools/content_pipeline.py check
python3 tools/content_pipeline.py build
python3 -c "import json; json.load(open('course-site/data/overrides.json'))"
```

## 결과 출력

```
Fact Audit 결과 — W##
─────────────────
L1 기계 검사: 깨진 참조 N건
L2 사실 검증: 검증 항목 N건 (즉시 반영 N / 결재 대기 N)
L3 반영: docs/content-audit/YYYY-MM-DD-w##-pending-updates.md 생성
```

## Gotchas

> Claude가 이 스킬을 쓸 때 실수했던 것들. 새 함정 발견 시 여기에 추가.

1. overrides.json을 수정해도 일반 build에는 반영되지 않는다 — canonical은 weeks/site-data.json (2026-07-20 W05 감사에서 확인)
2. curriculum.js는 자동 생성 파일이라 직접 편집하면 다음 build에서 덮어써진다

## 금지 사항

- weeks/site-data.json 외의 파일(overrides.json, curriculum.js)을 canonical로 착각해 수정하지 말 것
- lecture-note.md AUTO:CURRICULUM-SYNC 블록을 수동으로 편집하지 말 것 — build가 덮어쓴다
- notion-sync가 관리하는 파일에 결재 없이 직접 write하지 말 것
