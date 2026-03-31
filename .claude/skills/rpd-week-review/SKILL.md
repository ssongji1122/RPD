---
name: rpd-week-review
description: "주차 검수", "품질 검토", "week review" 요청 시 호출. 콘텐츠 완성도, 카피 품질, 접근성, 반응형 검수. Use after completing a week's content to verify quality before marking as done.
---

# RPD Week Review

## 검수 대상
- `course-site/data/curriculum.js` — 해당 주차 데이터
- `course-site/week.html?week=N` — 렌더링 결과

## 검수 체크리스트

### 1. 데이터 완성도
- [ ] `week`, `status`, `title`, `subtitle`, `summary`, `duration` 모두 채워짐
- [ ] `topics` 4-6개
- [ ] `steps` 최소 2개 이상
- [ ] 각 step에 `title`, `copy`, `tasks` 있음
- [ ] 각 task에 `id`(wN-tN 형식), `label` 있음
- [ ] `assignment` 완전함 (title, description, checklist)
- [ ] `mistakes` 1개 이상, "증상 → 해결" 형식

### 2. 카피 품질
- [ ] `title` 15자 이내, 행동/인지 목표 느낌
- [ ] `copy` 1-2문장, 비유 또는 맥락 설명 포함
- [ ] ~해요/~이에요 톤 사용 (금지: ~합니다/~습니다)
- [ ] 결론 먼저, 설명 나중
- [ ] 과장 표현 없음 ("혁신적", "완벽한", "무한한")
- [ ] task label이 동사로 시작

### 3. 리소스 확인
- [ ] `docs` URL이 유효한 Blender 공식 문서인지
- [ ] `videos` URL이 유효한지
- [ ] step `image` 경로에 실제 파일이 있는지 (`assets/images/weekNN/`)
- [ ] 이미지 alt 텍스트가 의미 있는지 (step.title 이상의 설명)

### 4. 시각 확인 (브라우저에서)
- [ ] `week.html?week=N` 로드 시 JS 에러 없음
- [ ] Hero 정보 올바름 (주차 번호, 제목, 메타칩)
- [ ] 토픽 체크리스트 표시 정상
- [ ] 모든 step 카드 렌더링 정상
- [ ] 체크박스 클릭 → 진도 업데이트 작동
- [ ] 단축키 테이블 표시 정상 (해당 주차에 shortcuts 있을 경우)
- [ ] 과제 카드 표시 정상
- [ ] 이전/다음 주차 링크 작동

### 5. 반응형 확인
- [ ] 1280px: 2열 토픽 그리드, 넓은 카드
- [ ] 720px: 1열 레이아웃, 사이드바 오버레이
- [ ] 375px: 모든 요소 잘림 없음, 텍스트 가독성

### 6. Bloom's Taxonomy 매핑 확인
- [ ] shortcuts → Remember 단계 (있으면)
- [ ] step.copy → Understand (왜 하는지 설명)
- [ ] step.tasks → Apply (직접 실행)
- [ ] mistakes → Analyze (진단)
- [ ] topics → Evaluate (자기 확인)
- [ ] explore → Create (창작, 있으면)

### 7. 교차 참조
- [ ] `index.html`에서 해당 주차 카드가 올바른 정보 표시
- [ ] 이전/다음 주차와 연결 자연스러움
- [ ] status가 올바른지 (done/active/upcoming)

## 검수 절차

1. `curriculum.js`에서 해당 주차 데이터를 Read로 확인
2. 체크리스트 1-3 (데이터, 카피, 리소스) 점검
3. 로컬 서버 또는 Claude Preview로 week.html?week=N 로드
4. 체크리스트 4-5 (시각, 반응형) 점검
5. 체크리스트 6-7 (교육학, 교차참조) 점검
6. 발견된 문제를 리스트로 정리 후 수정

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
