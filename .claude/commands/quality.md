---
description: "테스트 실행", "품질 검증", "quality", "lint" 요청 시 호출. E2E 테스트 + 코드 품질 검증 통합.
allowed-tools: Read, Glob, Grep, Bash(python3:*), Bash(npx:*), Bash(ls:*), Agent
---

# Quality — 품질 검증

## 모드 분기

| 인자 | 동작 |
|------|------|
| (없음) | 전체 테스트 + lint 실행 |
| e2e | E2E 테스트만 실행 |
| lint | HTML/CSS/JS lint만 실행 |
| {파일} | 특정 파일 관련 테스트만 실행 |

## 테스트 실행

### E2E 테스트
```bash
cd tools && python3 -m pytest tests/ -v --tb=short 2>&1
```

### HTML 검증
- `course-site/*.html` 대상
- 깨진 링크, 누락 alt 속성, 중복 id 확인

### CSS 검증
- `course-site/assets/*.css` 대상
- 미사용 변수, 중복 선언 확인

## 결과 출력
```
📋 품질 검증 결과
─────────────────
E2E: ✅ X passed / ❌ X failed
HTML: ✅ X clean / ⚠️ X warnings
CSS: ✅ X clean / ⚠️ X warnings
```

## 실행 로그
실행 완료 시:
```bash
echo "[$(date '+%Y-%m-%d %H:%M')] mode=$MODE e2e=$E2E_RESULT html=$HTML_RESULT css=$CSS_RESULT" >> .claude/skill-logs/quality.log
```

## Gotchas ⚠️
> Claude가 이 스킬을 쓸 때 실수했던 것들. 새 함정 발견 시 여기에 추가.

1. (아직 없음 — 사용하면서 추가)

## 금지 사항
- 🔴 테스트 실패 시 테스트 코드를 수정하지 말 것 — 소스 코드를 고쳐야 함
- 🔴 lint 경고를 무시하고 넘어가지 말 것
