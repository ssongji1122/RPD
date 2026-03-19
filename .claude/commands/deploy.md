---
description: "배포", "deploy", "CI 확인", "GitHub Pages" 요청 시 호출. GitHub Pages 배포 상태 확인 + CI 파이프라인 모니터링.
allowed-tools: Read, Glob, Grep, Bash(gh:*), Bash(git:*), Bash(curl:*), Bash(ls:*)
---

# Deploy — 배포 & CI 확인

## 모드 분기

| 인자 | 동작 |
|------|------|
| (없음) | 현재 배포 상태 + CI 확인 |
| status | GitHub Pages 배포 상태만 확인 |
| ci | CI workflow 실행 상태만 확인 |
| logs | 최근 CI 실행 로그 확인 |

## 절차

### 배포 상태 확인
```bash
gh api repos/{owner}/{repo}/pages --jq '.status'
```

### CI 워크플로우 확인
```bash
gh run list --limit 5 --json status,conclusion,name,createdAt
```

### CI 실패 시 로그 확인
```bash
gh run view {run-id} --log-failed
```

## 결과 출력
```
📋 배포 상태
─────────────
Pages: ✅ built / ❌ errored
CI: ✅ passing / ❌ failing (run #{id})
마지막 배포: {timestamp}
```

## 실행 로그
실행 완료 시:
```bash
echo "[$(date '+%Y-%m-%d %H:%M')] mode=$MODE pages=$PAGES_STATUS ci=$CI_STATUS" >> .claude/skill-logs/deploy.log
```

## Gotchas ⚠️
> Claude가 이 스킬을 쓸 때 실수했던 것들. 새 함정 발견 시 여기에 추가.

1. (아직 없음 — 사용하면서 추가)

## 금지 사항
- 🔴 CI 실패를 무시하고 배포하지 말 것
- 🔴 force push로 배포 문제를 해결하지 말 것
