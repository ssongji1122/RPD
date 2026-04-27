---
description: "Notion sync", "노션 반영", "수동 동기화", "즉시 배포" 요청 시 호출. Notion 편집 내용을 GitHub Actions로 즉시 트리거하여 사이트에 반영.
allowed-tools: Bash(gh:*), Bash(sleep:*)
---

# Sync — Notion → 사이트 즉시 반영

## 실행

```bash
gh workflow run notion-sync.yml --repo ssongji1122/RPD
```

성공하면 3초 대기 후 실행 상태 확인:

```bash
sleep 3 && gh run list --workflow=notion-sync.yml --repo ssongji1122/RPD --limit 1 --json databaseId,status,conclusion,url
```

## 결과 출력

```
🔄 Notion Sync 트리거 완료
─────────────────────────
Run: [#{id}]({url})
상태: 실행 중 (보통 1~2분 소요)
배포: 완료 후 GitHub Pages 추가 1~2분
```

실행 ID를 클릭 가능한 링크로 제공한다.

## 실패 시

```bash
gh run view {run_id} --log-failed --repo ssongji1122/RPD
```

에러 내용을 요약해서 사용자에게 보고한다.
