---
name: rpd-content-write
description: "콘텐츠 작성", "curriculum 편집", "톤 교정", "보완", "다듬어줘" 요청 시 호출. weeks/site-data.json 주차 데이터 추가/수정/톤 교정. Use when editing site-data.json week data, writing step copy, or tasks.
---

# RPD Content Write

## SoT 매트릭스 (이 표가 단일 진실)

이 리포는 **repo-first**다. `weeks/site-data.json`이 canonical이고 Notion은 publish 대상.

| 필드 | 수정 위치 | 방법 |
|------|----------|------|
| step title/copy/tasks/goal/done, assignment, mistakes, shortcuts, docs/videos, summary, subtitle, topics, title, status | `weeks/site-data.json` | Edit tool 또는 admin.html UI |
| image, showme | `weeks/site-data.json`(직접) 또는 `course-site/data/overrides.json`(어드민 일시 덮어쓰기) | 정상 흐름은 site-data.json. overrides는 hotfix용 |
| 학생 roster, Notion 페이지 ID | `tools/notion-mapping.json` | 직접 편집 |

**금지**: `course-site/data/curriculum.json` / `curriculum.js`는 generated artifact — 직접 편집 금지.

## 편집 → 빌드 → 배포 파이프라인

```bash
# 1. 편집 (택1)
ADMIN_KEY=change-me ./tools/start-admin.sh   # GUI 편집 (권장)
# 또는 weeks/site-data.json 직접 Edit

# 2. 검증
python3 tools/content_pipeline.py check

# 3. 빌드 (public 데이터 생성)
python3 tools/content_pipeline.py build

# 4. 검수
/rpd-check week N

# 5. (선택) Notion 미러링 — 학생 공유용
NOTION_TOKEN=... python3 tools/curriculum-push.py --week N
```

## 리서치 브리프 참조

작업 시작 전 `claudedocs/research/{관련-id}-brief.md` 존재 여부 확인:
- **있으면** → 비유(§7), 실수(§6), 단축키(§3)를 브리프에서 가져와 site-data.json에 반영
- **없으면** → `⚠️ {id} 리서치 브리프가 없습니다. /rpd-research {id} 먼저 실행을 권장합니다.`

## 데이터 스키마

스키마는 `weeks/contracts.schema.json`이 ground truth. 요약:

```js
{
  week: Number,           // 1-15
  status: "done|active|upcoming",
  title: String,          // 15자 이내, 행동/인지 목표 느낌
  subtitle: String,       // step과 1:1 매핑되도록 (검수 시 step.title 개수 확인)
  summary: String,        // 1문장 요약, overrides.json과 일치해야 함
  duration: String,       // "~N시간"
  topics: String[],       // 4-6개, 이번 주 학습 주제
  steps: [{
    title: String,        // 짧고 명확, 행동 중심
    copy: String,         // 1-2문장, 비유 포함 권장
    image: String,        // "assets/images/weekNN/step-N.png" (선택)
    link: String,         // 이미지 클릭 시 이동 URL (선택)
    goal: String[],       // 학습 목표
    done: String[],       // 완료 기준 — task에서 구체적 카운트 일치 필요
    tasks: [{
      id: String,         // "wN-tN" 형식, 주차 내 unique
      label: String,      // 동사로 시작
      detail: String      // 힌트 또는 단축키 (선택)
    }]
  }],
  assignment: { title, description, checklist },
  mistakes: String[],     // "증상 → 해결" 형식
  shortcuts: [{ keys, action }],
  explore: [{ title, hint }],
  videos: [{ title, url }],  // 공식 Blender만
  docs: [{ title, url }]     // 공식 문서만
}
```

## 톤 규칙

### 문체
- **~해요/~이에요** 체 사용 (친근한 존댓말)
- ~합니다/~습니다 금지
- 결론을 먼저, 설명은 그 다음
- 문장은 짧게, 한 문단 2-3문장 이내

### 좋은 예
- "Blender를 처음 열면 옵션이 너무 많아서 압도돼요."
- "거울 앞에 서면 반대쪽이 똑같이 움직이죠? Mirror Modifier가 그거예요."

### 나쁜 예
- "창의적인 모델링의 시작" → 추상적
- "무한한 가능성을 열어보자" → 과장
- "이 기능은 매우 유용합니다" → ~합니다 문체

### 한국어 받침 검사
- "Light은" / "Cube은" 처럼 받침 없는 단어 + "은/이" 조사 오류 자주 발생 → "Light는", "Cube는"
- 영문 단어 끝 자음 발음 기준이지만 일반적으로 **자음+e로 끝나면 모음 발음 → 는/가**

### 비유 패턴 (주차별)
| 주차 | 비유 방향 |
|------|-----------|
| 01 | 집 꾸미기 전 가구 배치 구상 |
| 02 | 운전 배우기 (핸들, 기어, 페달) |
| 03-04 | 레고 조립 (파츠 끼우기, 깎기) |
| 05 | 점토 조각 (AI가 초벌, 내가 다듬기) |
| 06-07 | 옷 입히기 (재질 = 옷감, UV = 재단) |
| 09 | 사진관 조명 세팅 |
| 10-11 | 인형극 / 마리오네트 |
| 13 | 카메라 감독 + AI 편집실 |

## Bloom's Taxonomy 매핑

curriculum의 각 섹션이 Bloom's 단계에 대응:

| 섹션 | Bloom's 레벨 | 동사 예시 |
|------|-------------|-----------|
| shortcuts | Remember | 기억하기, 찾기 |
| step.copy | Understand | 이해하기, 설명하기 |
| step.tasks | Apply | 적용하기, 실행하기, 만들기 |
| mistakes | Analyze | 진단하기, 비교하기 |
| topics (self-check) | Evaluate | 확인하기, 검증하기 |
| explore | Create | 설계하기, 만들기 |

**태스크 label은 Apply 동사로**: "~적용", "~만들기", "~실행", "~확인"

## 일관성 검사 (자주 빠지는 항목)

- [ ] `subtitle`의 항목 수가 `steps` 개수와 맞는가
- [ ] `summary`가 `course-site/data/overrides.json`의 같은 주차 summary와 일치하는가
- [ ] `step.done`이 "N가지" 라고 하면 `tasks` 개수가 그 카운트를 받쳐주는가
- [ ] task `id`가 주차 내 unique이고 `wN-tN` 형식인가
- [ ] `mistakes` 모든 항목이 "증상 → 해결" 구조인가
- [ ] 외부 URL이 공식 Blender / Poly Haven 도메인인가

## 참고 문서
- `weeks/contracts.schema.json` — 스키마 ground truth
- `tools/SYNC_GUIDE.md` — repo-first 운영 모델 전체
- `course-site/CONTENT_GUIDE.md` — 톤·구조 가이드
- `docs/REFERENCE_RESEARCH_2026-03-15.md` — 교육학 섹션

## Gotchas ⚠️
> Claude가 이 스킬을 쓸 때 실수했던 것들. 새 함정 발견 시 여기에 추가.

1. **Notion 페이지를 SoT로 착각하지 말 것**. SYNC_GUIDE 전환 후 SoT는 `weeks/site-data.json`. Notion은 publish 대상.
2. **summary 충돌**: overrides.json과 site-data.json에 둘 다 summary가 있어 동기화 안 되면 site-data가 win. 수정 시 둘 다 맞춰야 안전.
3. **subtitle ≠ step 개수**: subtitle에 "·"로 항목 나열할 때 step 개수와 자주 어긋남. 검수 시 카운트 비교.
4. **받침 없는 영문 + 조사**: "Light은/Cube은" → "Light는/Cube는". 영문이 자주 나오는 본 코스 특성상 빈번한 함정.
