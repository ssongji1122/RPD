---
name: rpd-research
description: 블렌더/디자인 교안 콘텐츠 리서치. 공식 문서 + 커뮤니티 혼란 포인트 수집, 크로스팩트체크 후 검증된 브리프 생성. Use before /rpd-content-write or /showme to ensure content accuracy.
---

# RPD Research — 교안 콘텐츠 리서치 스킬

## 호출

```
/rpd-research {tool-id}              # 단일 도구 리서치
/rpd-research {tool-id} --deep       # 연관 개념 재귀 탐색 (깊이 2)
/rpd-research week {N}               # 주차 전체 리서치
```

## 출력

`claudedocs/research/{tool-id}-brief.md`

## 모드 분기

**`{tool-id}`**: 단일 도구/개념 리서치 → Phase 1~4 실행
**`{tool-id} --deep`**: 단일 리서치 + 연관 개념 재귀 (최대 깊이 2, 각 재귀는 병렬 Agent)
**`week {N}`**: curriculum.js에서 주차 N의 showme ID 추출 → 각 ID별 병렬 리서치 → week summary 생성
**인자 없음**: 이 도움말 출력

---

## Phase 1: 공식 소스 수집 (정확성)

> Phase 1 내부는 모두 **병렬 실행**

### 1-1. Blender 공식 문서 (WebFetch)

대상 URL을 도구 유형에 따라 선택:

| 카테고리 | URL 패턴 |
|----------|----------|
| Generate 모디파이어 | `https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/{name}.html` |
| Deform 모디파이어 | `https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/{name}.html` |
| Mesh 도구 | `https://docs.blender.org/manual/en/latest/modeling/meshes/tools/{tool}.html` |
| Edge 편집 | `https://docs.blender.org/manual/en/latest/modeling/meshes/editing/edge/{tool}.html` |
| Mesh 편집 | `https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/{tool}.html` |
| Sculpt 도구 | `https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/{tool}.html` |
| 조명 | `https://docs.blender.org/manual/en/latest/render/lights/{type}.html` |
| 셰이더 노드 | `https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/{node}.html` |
| UV | `https://docs.blender.org/manual/en/latest/modeling/meshes/uv/{tool}.html` |
| Compositing | `https://docs.blender.org/manual/en/latest/compositing/types/{category}/{node}.html` |
| Armature/Rigging | `https://docs.blender.org/manual/en/latest/animation/armatures/{section}.html` |

추출 항목:
- 공식 정의 (영어 원문)
- 파라미터 테이블 (이름, 기본값, 설명)
- 관련 단축키
- See Also / Related 링크
- Blender 버전별 변경사항 (있으면)

### 1-2. Blender Python API (Context7 MCP — `--c7`)

```
resolve-library-id "blender" → query-docs "{tool-id}"
```

추출 항목:
- API에서의 정확한 이름/경로 (예: `bpy.ops.mesh.loopcut_slide`)
- 프로그래밍적 접근 시 파라미터명

### 1-3. 릴리즈 노트 (WebFetch)

최근 3개 버전의 변경사항 확인:
```
https://wiki.blender.org/wiki/Reference/Release_Notes/4.x
```

해당 도구와 관련된 변경사항만 추출.

---

## Phase 2: 학생 혼란 포인트 수집 (공감)

> Phase 2 내부도 모두 **병렬 실행**

### 2-1. 영어 커뮤니티 (WebSearch)

병렬 검색 3개:
```
"{tool-name} blender" site:reddit.com/r/blender
"{tool-name}" site:blender.stackexchange.com
"{tool-name} blender tutorial common mistake"
```

### 2-2. 한글 커뮤니티 (WebSearch)

```
"블렌더 {한글명}" site:cafe.naver.com OR site:clien.net OR site:arca.live
```

### 수집 기준

- 상위 **5-10개** 반복 질문 패턴 식별
- 각 질문에 **출처 URL 기록** (검증 가능하도록)
- 우선 수집 패턴:
  - "why doesn't..." / "왜 안 되죠?"
  - "how do I..." / "이해가 안 돼요"
  - "what's the difference..." / "차이가 뭐예요?"
- **"뭘 모르길래 이 질문을 하는가?"** 를 항상 분석 → Phase 3 연관 개념 그래프 입력

---

## Phase 3: 크로스체크 + 연관 개념 그래프

### 3-1. 팩트체크

Phase 2 커뮤니티 답변 × Phase 1 공식 정보 대조:

| 검증 결과 | 처리 |
|-----------|------|
| ✅ 정확 | 그대로 채택, 출처 기록 |
| ⚠️ 부분 정확 | 정정 사항 명시 + 올바른 정보 |
| ❌ 오류 | 올바른 정보로 대체 + 왜 틀린지 설명 |

### 3-2. 연관 개념 그래프 구성

Phase 2 질문에서 역추적하여 세 가지 레이어 구성:

**선수 지식** (이걸 모르면 이해 불가):
- "이 질문을 하려면 뭘 몰라야 하는가?" 역추적
- 예: Loop Cut 질문 → 점·선·면 위계를 모름

**연결 개념** (함께 쓰이는 것):
- 이 도구와 자주 조합되는 다른 도구/기능
- 예: Loop Cut + Subdivision Surface

**심화** (알면 이해가 깊어지는 원리):
- 수학적/기하학적 원리, 내부 동작
- 예: N-gon → Circle 근사, R값과 해상도 관계

---

## Phase 4: 교안용 가공

### 4-1. CONTENT_GUIDE.md 톤 적용

참조: `course-site/CONTENT_GUIDE.md`

규칙:
- ~해요/~이에요 존댓말
- 결론 먼저, 설명은 그 다음
- 비유는 학생이 이미 경험한 것에서

### 4-2. 브리프 파일 생성

`claudedocs/research/{tool-id}-brief.md` 작성:

```markdown
# 리서치 브리프: {한글 이름} ({영문 이름})
> 생성일: {YYYY-MM-DD} | Blender {버전} 기준

## 1. 공식 정의
- **영문**: {Blender Docs 원문}
- **한글 풀이**: {쉬운 설명}
- **공식 문서**: [{페이지 제목}]({URL})

## 2. 핵심 파라미터
| 파라미터 | 기본값 | 설명 | 학생에게 중요한 이유 |
|---------|-------|------|-------------------|

## 3. 단축키
| 키 | 동작 | 컨텍스트 | 비고 |
|----|------|---------|------|

## 4. 연관 개념 그래프
### 선수 지식 (이걸 모르면 이해 불가)
- **{개념}**: {왜 필요한지 한 줄}

### 연결 개념 (함께 쓰이는 것)
- **{개념}**: {조합 시 효과}

### 심화 (알면 이해가 깊어지는 것)
- **{개념}**: {원리 설명}

## 5. 학생 혼란 포인트
| # | 질문 (실제) | 출처 | 핵심 원인 | 검증된 답변 |
|---|-----------|------|----------|-----------|

## 6. 흔한 실수 & 해결
| 증상 | 원인 | 해결 |
|------|------|------|

## 7. 추천 비유 후보
1. **{비유}** — {왜 이 비유가 맞는지}
2. **{비유}** — {왜 이 비유가 맞는지}

## 8. 크로스체크 로그
| 주장 | 소스 | 검증 | 결과 |
|------|------|------|------|
```

---

## `--deep` 모드 추가 동작

Phase 3에서 식별된 **선수 지식** 각각에 대해:

1. `claudedocs/research/{concept}-brief.md` 이미 존재하는지 확인
2. 없으면 → **병렬 Agent**로 해당 개념 리서치 (깊이+1)
3. **깊이 2 도달 시 중단**, 참조 링크만 기록

```
/rpd-research loop-cut --deep
  ├── loop-cut-brief.md (깊이 0)
  ├── vertex-edge-face-brief.md (깊이 1, 병렬 Agent)
  ├── subdivision-concept-brief.md (깊이 1, 병렬 Agent)
  └── 깊이 2 → 중단, 참조만
```

---

## `week N` 모드 추가 동작

1. `course-site/data/curriculum.js` 읽기
2. week N의 모든 step에서 `showme` 필드 추출
3. 각 showme ID별 **병렬 Agent**로 개별 리서치
4. 완료 후 `claudedocs/research/week{NN}-summary.md` 생성:

```markdown
# Week {N} 리서치 요약: {주차 제목}

## 개념 흐름
{카드 A → B → C 관계 설명}

## 학습 순서 권장
{선수지식 기반 권장 순서와 이유}

## 주차 공통 혼란 포인트
{여러 카드에서 반복되는 패턴}

## 개별 브리프
- [{card-id}](./{card-id}-brief.md)
```

---

## 기존 스킬 연동

### 자동 감지 규칙

`/rpd-content-write`와 `/showme` 실행 시:

1. 작업 대상의 `claudedocs/research/{id}-brief.md` 존재 여부 확인
2. **있으면** → 자동 참조:
   - 비유 → 브리프 §7에서 가져오기
   - 단축키 → 브리프 §3 검증된 데이터 사용
   - 퀴즈 → 브리프 §5 학생혼란포인트에서 출제
   - 실수 → 브리프 §6 "증상→해결" 활용
3. **없으면** → 경고 출력:
   ```
   ⚠️ {id} 리서치 브리프가 없습니다.
   /rpd-research {id} 를 먼저 실행하면 더 정확한 콘텐츠를 만들 수 있어요.
   ```

---

## 병렬 처리 요약

| 단계 | 병렬 대상 |
|------|----------|
| Phase 1 내부 | WebFetch(공식문서) + Context7(API) + WebFetch(릴리즈노트) |
| Phase 2 내부 | WebSearch(Reddit) + WebSearch(StackExchange) + WebSearch(한글) |
| `--deep` | 선수지식 개념별 Agent |
| `week N` | showme ID별 Agent |

Phase 3~4는 Phase 1+2 결과에 의존하므로 **순차 실행**.

---

## 참고 파일

| 파일 | 역할 |
|------|------|
| `course-site/CONTENT_GUIDE.md` | 톤/문체 마스터 레퍼런스 |
| `docs/REFERENCE_RESEARCH_2026-03-15.md` | 교육학 섹션 |
| `course-site/data/curriculum.js` | 주차별 showme 필드 (week 모드) |
| `docs/plans/2026-03-17-rpd-research-skill-design.md` | 설계 문서 |

## Gotchas ⚠️
> Claude가 이 스킬을 쓸 때 실수했던 것들. 새 함정 발견 시 여기에 추가.

1. (아직 없음 — 사용하면서 추가)
