---
name: rpd-week-review
description: "주차 검수", "내용 확인", "보완", "다듬어줘", "리뷰", "week review", "라이팅 봐줘" 요청 시 호출. 콘텐츠 완성도, 카피 품질, 접근성, 반응형 검수. Use after completing or before publishing a week's content.
---

# RPD Week Review

## 검수 대상
- `weeks/site-data.json` — 해당 주차 canonical 데이터
- `course-site/week.html?week=N` — 렌더링 결과
- `course-site/data/overrides.json` — 어드민 덮어쓰기 (summary 일치 확인용)

## 절차 (순서 중요)

### 1. 자동 검증 먼저
사람 손은 톤·교육학에만. 형식 검증은 코드로.

```bash
python3 tools/content_pipeline.py check     # 스키마 검증
/rpd-check week N                            # 콘텐츠 검사
```

자동 검증 통과한 항목은 다시 보지 않는다.

### 2. 리서치 브리프 일치 확인
`claudedocs/research/{주차-id}-brief.md` 존재 여부 확인:
- 있으면: 비유·실수·단축키가 site-data.json에 반영됐는지 점검
- 없으면: warning 출력. (의무는 아님)

### 3. 사람이 봐야 하는 4가지 (자동화 불가)

**카피 톤** — ~해요/~이에요, 결론 먼저, 과장 없음, 비유 포함

**Bloom 매핑** — `rpd-content-write` 스킬의 Bloom 표 참조 (단일 출처)

**일관성** — site-data.json 내부 + overrides.json 사이
- `subtitle`의 "·" 항목 수 == `steps` 개수
- `step.done`의 "N가지" == `tasks` 개수가 그걸 받쳐줌
- `summary`가 `overrides.json`의 같은 주차 summary와 일치
- 한국어 조사 (특히 영문+은/는, 이/가)

**시각·a11y 빠른 체크** — Claude Preview로 `week.html?week=N` 로드
- step 카드, shortcuts 테이블, 과제 카드, 이전/다음 링크 정상 렌더
- 1280 / 720 / 375px 반응형 잘림 없음
- 포커스 outline 보이고, 이미지 alt 채워졌고, heading 순서 맞음
- (정식 a11y는 분기별 `/rpd-a11y-audit`)

### 4. 발견 시 수정 경로

| 문제 유형 | 수정 위치 |
|-----------|----------|
| copy / task / shortcut / mistake | `weeks/site-data.json` (admin.html UI 또는 Edit) |
| status / 빠른 image hotfix | `course-site/data/overrides.json` |
| 이미지 누락 | `course-site/assets/images/weekNN/` 추가 후 site-data.json 경로 연결 |
| showme 카드 | `course-site/assets/showme/{slug}.html` + site-data.json `showme` 필드 |

수정 후:
```bash
python3 tools/content_pipeline.py build
NOTION_TOKEN=... python3 tools/curriculum-push.py --week N   # 학생 노션 미러링
```

## 검수 결과 보고 형식

```markdown
# N주차 검수
## ✅ 자동 검증 통과
## 🟡 라이팅·내용 보완
- {필드}: {현재} → {제안} (이유)
## 🔴 일관성 불일치
- {필드 A} vs {필드 B}: {차이} → {조치}
## 시각/반응형
- {뷰포트}: {결과}
```

## 참고 문서
- `tools/SYNC_GUIDE.md` — repo-first 흐름
- `.claude/skills/rpd-content-write/SKILL.md` — 톤·스키마·Bloom 단일 출처
- `course-site/CONTENT_GUIDE.md`
- `docs/COURSE_SITE_STYLE_GUIDE_2026-03-13.md`

## Gotchas ⚠️

1. **summary 두 곳 충돌** — site-data.json과 overrides.json에 모두 summary가 있어 sync 깨지면 어긋남. 검수 1순위.
2. **subtitle ≠ step 개수** — subtitle 항목 추가 없이 step만 늘리면 누락됨. 9주차에서 발생한 사례.
3. **step.done 카운트 ≠ task 개수** — "3가지 분위기"라 했는데 task가 2개. done 문장의 숫자와 task 개수 항상 비교.
4. **받침 없는 영문 단어 + 조사** — "Light은/Cube은" 흔함. 검수 시 본문·mistakes 한 번 grep 권장.
5. **Notion이 SoT가 아니다** — Notion에서 본 내용이 사이트와 다르면 site-data.json이 정답. Notion은 push 대상.
