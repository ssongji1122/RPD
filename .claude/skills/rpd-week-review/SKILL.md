---
name: rpd-week-review
description: "주차 검수", "품질 검토", "week review" 요청 시 호출. 콘텐츠 완성도, 카피 품질, 접근성, 반응형 검수. Use after completing a week's content to verify quality before marking as done.
---

# RPD Week Review

## 검수 대상
- `course-site/data/curriculum.js` — 해당 주차 데이터
- `course-site/week.html?week=N` — 렌더링 결과

## 검수 기준

**데이터 완성도** — `week/status/title/subtitle/summary/duration` 채워짐, topics 4-6개, steps 최소 2개, 각 step에 title·copy·tasks, 각 task에 id(wN-tN 형식)·label, assignment(title·description·checklist) 완전함, mistakes 1개 이상("증상 → 해결" 형식)

**카피 품질** — title 15자 이내, copy 1-2문장(비유 또는 맥락 포함), ~해요/~이에요 톤, 결론 먼저, 과장 없음, task label 동사로 시작

**리소스** — docs URL이 Blender 공식 문서, videos URL 유효, step image 파일이 `assets/images/weekNN/`에 실제 존재

**시각** — JS 에러 없음, Hero 정보 정확, step 카드 렌더링 정상, shortcuts 테이블·과제 카드 표시 정상, 이전/다음 주차 링크 작동

**반응형** — 1280px(2열), 720px(1열), 375px(잘림 없음)

**Bloom's Taxonomy** — shortcuts→Remember, step.copy→Understand, step.tasks→Apply, mistakes→Analyze, topics→Evaluate, explore→Create

**교차 참조** — index.html 카드 정보 정확, 이전/다음 연결 자연스러움, status 올바름

## 검수 절차

1. `curriculum.js`에서 해당 주차 데이터 Read
2. 데이터·카피·리소스 점검
3. Claude Preview로 `week.html?week=N` 로드
4. 시각·반응형 점검
5. Bloom·교차참조 점검
6. 발견된 문제 리스트로 정리 후 수정

## 수정 반영 규칙

리뷰에서 발견된 문제를 수정할 때:

| 문제 유형 | 수정 위치 |
|-----------|----------|
| copy 톤/표현 수정 | Notion MCP → notion-sync.py --fetch-only |
| task label 수정 | Notion MCP → notion-sync.py --fetch-only |
| 이미지 누락/연결 | overrides.json |
| showme 연결 | overrides.json |
| done 체크리스트 수정 | overrides.json |

**주의**: curriculum.json/js를 직접 수정하지 않는다.

## 참고 문서
- `course-site/CONTENT_GUIDE.md` (섹션 6: 검증 체크리스트)
- `docs/COURSE_SITE_STYLE_GUIDE_2026-03-13.md`
- `docs/REFERENCE_RESEARCH_2026-03-15.md`

## Gotchas ⚠️
> Claude가 이 스킬을 쓸 때 실수했던 것들. 새 함정 발견 시 여기에 추가.

1. (아직 없음 — 사용하면서 추가)
