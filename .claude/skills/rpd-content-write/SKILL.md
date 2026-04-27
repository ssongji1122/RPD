---
name: rpd-content-write
description: "콘텐츠 작성", "curriculum 편집", "톤 교정" 요청 시 호출. curriculum.js 주차 데이터 추가/수정/톤 교정. Use when editing curriculum.js week data, writing step copy, or tasks.
---

# RPD Content Write

## 리서치 브리프 참조

작업 시작 전 `claudedocs/research/{관련-id}-brief.md` 존재 여부 확인:
- **있으면** → 비유(§7), 실수(§6), 단축키(§3)를 브리프에서 가져와 curriculum.js에 반영
- **없으면** → `⚠️ {id} 리서치 브리프가 없습니다. /rpd-research {id} 먼저 실행을 권장합니다.`

## 수정 경로

콘텐츠 수정은 Notion을 통해 수행한다. curriculum.json/js는 generated file이므로 직접 수정하지 않는다.

| 필드 | 수정 위치 | 방법 |
|------|----------|------|
| step title, copy, tasks, goal, assignment | Notion | Notion MCP (mcp__notion__update-page) |
| shortcuts, mistakes, docs | Notion | Notion MCP |
| image, showme, done, status | overrides.json | Edit tool |

### Notion 수정 절차
1. `tools/notion-mapping.json`에서 대상 week의 Notion page ID 확인
2. Notion MCP로 해당 페이지의 블록 수정
3. `python3 tools/notion-sync.py --fetch-only` 실행
4. curriculum.json 재생성 확인
5. `/rpd-check week {N}` 검증

### 참고 파일
- `course-site/data/curriculum.json` — 읽기 전용, 현재 상태 확인용
- `course-site/data/overrides.json` — 코드 에셋 필드 수정용
- `tools/notion-mapping.json` — week → Notion page ID

## 데이터 스키마

```js
{
  week: Number,           // 1-15
  status: "done|active|upcoming",
  title: String,          // 15자 이내, 행동/인지 목표 느낌
  subtitle: String,       // 핵심 개념 나열
  summary: String,        // 1문장 요약
  duration: String,       // "~N시간"
  topics: String[],       // 4-6개, 이번 주 학습 주제
  steps: [{
    title: String,        // 짧고 명확, 행동 중심
    copy: String,         // 1-2문장, 비유 포함 권장
    image: String,        // "assets/images/weekNN/step-N.png" (선택)
    link: String,         // 이미지 클릭 시 이동 URL (선택)
    goal: String[],       // 학습 목표
    done: String[],       // 완료 기준
    tasks: [{
      id: String,         // "wN-tN" 형식 (예: "w3-t1")
      label: String,      // 동사로 시작 (예: "Mirror 적용 후 대칭 확인")
      detail: String      // 힌트 또는 단축키 (선택)
    }]
  }],
  assignment: {
    title: String,
    description: String,
    checklist: String[]
  },
  mistakes: String[],     // "증상 → 해결" 형식
  shortcuts: [{           // 선택
    keys: String,         // "Ctrl + R" 형식
    action: String
  }],
  explore: [{             // 선택
    title: String,
    hint: String
  }],
  videos: [{ title, url }],  // 선택, 공식 Blender만
  docs: [{ title, url }]     // 선택, 공식 문서만
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

curriculum.js의 각 섹션이 Bloom's 단계에 대응:
| 섹션 | Bloom's 레벨 | 동사 예시 |
|------|-------------|-----------|
| shortcuts | Remember | 기억하기, 찾기 |
| step.copy | Understand | 이해하기, 설명하기 |
| step.tasks | Apply | 적용하기, 실행하기 |
| mistakes | Analyze | 진단하기, 비교하기 |
| topics (self-check) | Evaluate | 확인하기, 검증하기 |
| explore | Create | 설계하기, 만들기 |

**태스크 label은 Apply 동사로**: "~적용", "~만들기", "~실행", "~확인"

## 검증 체크리스트

콘텐츠 작성/수정 후:
1. [ ] `week` 번호와 `status` 맞는지
2. [ ] `title` 15자 이내
3. [ ] `topics` 4-6개
4. [ ] `steps` 마다 `tasks` 2-5개, ID 형식 `wN-tN`
5. [ ] `copy`에 비유 또는 맥락 설명 포함
6. [ ] `mistakes` "증상 → 해결" 형식
7. [ ] `assignment` 필드 모두 채워짐
8. [ ] 금지 표현 없음 (~합니다, 과장 표현)
9. [ ] URL은 공식 Blender 문서만 사용
10. [ ] JSON 문법 오류 없음 (trailing comma 등)

## 참고 문서
- `course-site/CONTENT_GUIDE.md` (마스터 레퍼런스)
- `docs/REFERENCE_RESEARCH_2026-03-15.md` (교육학 섹션)

## Gotchas ⚠️
> Claude가 이 스킬을 쓸 때 실수했던 것들. 새 함정 발견 시 여기에 추가.

1. (아직 없음 — 사용하면서 추가)
