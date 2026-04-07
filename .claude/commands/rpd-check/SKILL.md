---
description: "사이트 콘텐츠 검증. 예: /rpd-check, /rpd-check week 5, /rpd-check all, /rpd-check showme, /rpd-check --fix. DO NOT use for: 코드 품질 검증(/quality 사용), 배포 확인(/deploy 사용)"
allowed-tools: Read, Glob, Grep, Bash(ls:*), Bash(wc:*), Bash(stat:*), Bash(npx serve:*), Bash(git diff:*), Agent, Write, Edit
---

## Context

- 워크트리 위치: !`git worktree list 2>/dev/null | head -3`
- 전체 주차 수: !`python3 -c "import json; d=json.load(open('course-site/data/curriculum.json')); print(len(d))" 2>/dev/null || echo "?"`
- 이미지 파일 수: !`find course-site/assets/images -type f ! -name '.gitkeep' 2>/dev/null | wc -l | tr -d ' '`
- ShowMe 카드 수: !`ls course-site/assets/showme/*.html 2>/dev/null | grep -v _template | wc -l | tr -d ' '`
- Registry 항목 수: !`grep -c '"label"' course-site/assets/showme/_registry.js 2>/dev/null || echo 0`
- Supplement 항목 수: !`python3 -c "import json; d=json.load(open('course-site/assets/showme/_supplements.json')); print(len(d))" 2>/dev/null || echo "?"`

## Task

인자: `$ARGUMENTS`

---

## 모드 분기

| 인자 | 동작 |
|------|------|
| (없음) | Phase 1 전체 데이터 검증 |
| `week {N}` | Phase 1 + Phase 2 해당 주차 |
| `all` | Phase 1 + Phase 2 전체 (15주) |
| `showme` | ShowMe 카드 시스템만 집중 검증 |
| `--fix` | 검증 + 자동 수정 가능 항목 수정 (다른 인자와 조합 가능) |

### Smart Scoping (인자 없을 때)

인자 없이 `/rpd-check` 실행 시, 최근 변경 파일 기반으로 관련 검증을 우선 실행:

| 변경 패턴 | 우선 검증 |
|----------|----------|
| `course-site/assets/showme/` | 1.3 ShowMe 카드 체인 |
| `course-site/assets/images/` | 1.1 이미지 검증 |
| `course-site/data/curriculum*` 또는 `overrides.json` | 1.4 데이터 구조 + 1.8 동기화 |
| 변경 없음 | Phase 1 전체 |

우선 검증 결과를 먼저 출력한 뒤, 나머지 Phase 1 항목도 실행.

---

## Phase 1: Data Audit

curriculum.json을 읽고 아래 7개 카테고리를 검증한다.
결과를 내부 리스트에 수집하며, 각 이슈에 severity를 부여한다: `critical` / `warning` / `info`.

### 1.1 이미지 검증 (critical)

1. `curriculum.json` 읽기
2. 각 week → 각 step에서 `image` (string) 또는 `images` (array) 필드 추출
3. 각 경로에 대해 `course-site/` 기준으로 Glob 또는 Read로 파일 존재 확인
4. 파일 없으면 → `[CRITICAL] 이미지 누락: {path} ← week {N} step "{title}"`
5. 파일 크기 0이면 → `[CRITICAL] 빈 이미지: {path}`

### 1.2 텍스트 완전성 (warning)

1. 각 step: `title`과 `copy` 필드가 존재하고 빈 문자열이 아닌지
2. 각 task: `label` 필드가 존재하고 빈 문자열이 아닌지
3. 깨진 문자 패턴 감지: `□`, `\ufffd`, `???` 포함 여부
4. 문제 시 → `[WARNING] 빈 텍스트: week {N} step "{title}" → {field}`

### 1.3 ShowMe 카드 체인 (critical/warning)

**전체 체인 검증 — 4단계:**

1. curriculum.json에서 모든 showme ID 수집 (step.showme + step.widgets[].id)
2. 각 ID에 대해:
   - `_registry.js`의 SHOWME_REGISTRY에 키 존재? → 없으면 `[CRITICAL]`
   - `course-site/assets/showme/{id}.html` 파일 존재? → 없으면 `[CRITICAL]`
   - `_supplements.json`에 키 존재? → 없으면 `[WARNING]`
   - supplement에 필수 필드 (analogy, before_after, confusion, takeaway) 모두 존재? → 없으면 `[WARNING]`
3. `_catalog.json`의 categoryMap에서 모든 registry ID가 최소 1개 카테고리에 포함되어 있는지 → 없으면 `[INFO]`

### 1.4 데이터 구조 (critical)

1. 각 week 객체: `week`, `title`, `steps` 필드 존재
2. 각 step 객체: `title`, `copy` 필드 존재 (tasks는 없을 수 있음)
3. task가 있으면: `id`, `label` 필드 존재
4. task ID 형식: `/^w\d+-t\d+$/` 패턴 매칭
5. 전체 task ID 유니크 확인 (중복 시 `[CRITICAL]`)
6. week 번호 1~15 연속 확인 (빠진 주차 시 `[WARNING]`)

### 1.5 링크/URL (warning)

1. `docs[].url`, `videos[].url` → `https://` 시작하는지 형식 확인
2. `task.url` 필드 존재 시 형식 확인
3. `downloads` 필드의 파일 경로 → 파일 존재 확인
4. **주의**: 외부 URL에 실제 HTTP 요청은 보내지 않는다 (속도 문제). 형식만 검증.

### 1.6 클립/비디오 (warning)

1. `clips` 필드 → 파일 경로 존재 확인
2. `video` 필드 → URL 형식 유효 확인

### 1.7 Orphan 감지 (info)

1. `course-site/assets/images/week*/` 내 모든 파일 목록 수집 (`.gitkeep` 제외)
2. curriculum.json에서 참조되는 이미지 경로 목록과 비교
3. 참조 안 되는 파일 → `[INFO] Orphan 이미지: {path}`
4. `course-site/assets/showme/*.html` 중 `_template.html` 제외, registry에 없는 ID → `[INFO]`
5. `_supplements.json` 키 중 registry에 없는 ID → `[INFO]`

---

### 1.8 동기화 상태 검증 (warning/critical)

1. `curriculum-notion.json` 파일의 마지막 git commit 시간 확인:
   ```bash
   git log -1 --format="%ci" -- course-site/data/curriculum-notion.json
   ```
   - 30분 이상 경과 시 → `[INFO] Notion snapshot이 오래됨 — /curriculum sync 권장`
   - 24시간 이상 경과 시 → `[WARNING] Notion snapshot이 매우 오래됨`

2. overrides.json의 week/step 인덱스가 curriculum-notion.json 구조와 매칭되는지:
   - curriculum-notion.json 읽기 → 각 week의 steps 배열 길이 확인
   - overrides.json 읽기 → 각 week의 steps 키(인덱스) 확인
   - step 인덱스가 curriculum-notion.json의 steps 범위를 초과하면
     → `[CRITICAL] overrides step 인덱스 불일치: week {N} step {idx} — Notion에서 step이 추가/삭제됨`

3. curriculum-notion.json + overrides.json을 수동 merge한 결과와 현재 curriculum.json 비교:
   - 두 파일을 읽고 merge 로직 적용 (overrides 필드가 notion 필드를 덮어씀)
   - 현재 curriculum.json과 비교
   - 불일치 시 → `[WARNING] curriculum.json이 stale — /curriculum sync 필요`

---

### 최종 판정

PASS: critical 0건            → "✅ PASS (0 critical / N warning / N info)"
WARN: critical 0 + warning ≤5 → "⚠️ WARN (0 critical / N warning / N info)"
FAIL: critical ≥1             → "❌ FAIL (N critical / N warning / N info)"

판정 결과를 리포트 맨 마지막 줄에 출력.

---

## Phase 2: Browser Verify

`week {N}` 또는 `all` 인자가 있을 때만 실행. 상세: `references/browser-verify.md`

---

## Phase 3: Report + Fix

### 리포트 출력

모든 이슈를 severity별로 정렬하여 터미널에 출력:

```
=== RPD Check Report ===
스캔: 전체 15주 / 2026-03-31

[CRITICAL] 이미지 누락 (3건)
  week 5 step "AI 메쉬 정리" → assets/images/week05/mesh-cleanup.png
  week 5 step "Sculpt 브러시 심화" → assets/images/week05/sculpt-brushes.png
  week 5 step "Remesh와 마무리" → assets/images/week05/remesh.png

[CRITICAL] ShowMe HTML 누락 (0건)
  (없음)

[WARNING] ShowMe supplement 누락 (N건)
  sculpt-brushes: _supplements.json에 없음

[WARNING] 테마 불일치 (N건)
  showme/remesh-modifier.html: 다크 모드에서 라이트 iframe

[INFO] Orphan 파일 (N건)
  assets/images/week03/unused-image.png

──────────────────────────
Summary: X critical / Y warning / Z info
```

### JSON 리포트 저장

`claudedocs/rpd-check-report.json`에 구조화된 결과 저장:
```json
{
  "timestamp": "2026-03-31T...",
  "mode": "full | week:5 | showme",
  "issues": [
    {
      "severity": "critical",
      "category": "image",
      "week": 5,
      "step": "AI 메쉬 정리",
      "message": "이미지 누락: assets/images/week05/mesh-cleanup.png",
      "path": "assets/images/week05/mesh-cleanup.png"
    }
  ],
  "summary": { "critical": 3, "warning": 2, "info": 1 }
}
```

### --fix 자동 수정

--fix 자동 수정 규칙과 재검증 루프: `references/fix-rules.md`

---

## 실행 로그

```bash
echo "[$(date '+%Y-%m-%d %H:%M')] mode=$MODE result=$RESULT quality=$QUALITY critical=$CRITICAL warning=$WARNING info=$INFO" >> .claude/skill-logs/rpd-check.log
```

## Gotchas

<!-- 실행 시마다 새로운 발견을 이 목록에 추가 (날짜 포함). 오래된 항목은 유지. -->

1. curriculum.json은 ~3800줄이므로 전체를 한 번에 읽는다 (분할 불필요)
2. `_registry.js`는 JS 파일이므로 JSON 파싱 불가 — Grep으로 키를 추출하거나 전체 읽기 후 파싱
3. Phase 2 브라우저 검증 시 서버가 이미 떠 있으면 재기동하지 않는다
4. 외부 URL에 HTTP 요청을 보내지 않는다 (속도/안정성)
5. showme 모달 클릭 시 iframe 로드 시간이 필요하므로 짧은 대기 필요
6. 이미지 테마 검증 시 iframe cross-origin 제한으로 내부 스타일 직접 접근 불가 — 배경색만 확인

## 금지 사항

- 테스트 결과를 조작하거나 이슈를 무시하지 말 것
- Phase 1에서 발견된 critical 이슈가 있으면 반드시 리포트에 포함
- `--fix`로 이미지를 플레이스홀더로 생성하지 말 것 (품질 저하)
- curriculum.json 구조를 임의로 변경하지 말 것
