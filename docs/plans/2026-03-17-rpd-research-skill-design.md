# RPD Research Skill 설계

**날짜**: 2026-03-17
**상태**: 승인됨
**스킬명**: `/rpd-research`

## 목적

블렌더/디자인 교안 콘텐츠의 **정확성과 품질을 보장하는 리서치 전용 스킬**.
기존 작성 스킬(`/rpd-content-write`, `/showme`)에 검증된 소스를 공급한다.

## 핵심 원칙

- 공식 문서 우선, 커뮤니티 혼란 포인트 보완
- "왜?"까지 파는 연관 개념 그래프
- 크로스팩트체크 로그 필수

## 호출 방식

```
/rpd-research loop-cut              # 단일 도구 리서치
/rpd-research loop-cut --deep       # 연관 개념 재귀 탐색 (깊이 2)
/rpd-research week 3                # 주차 전체 리서치
```

## 출력

파일 위치: `claudedocs/research/{tool-id}-brief.md`

### 브리프 구조

```markdown
# 리서치 브리프: {한글 이름} ({영문 이름})

## 1. 공식 정의
- Blender Docs 원문 (영어)
- 한글 번역 + 쉬운 풀이
- 공식 문서 URL

## 2. 핵심 파라미터
| 파라미터 | 기본값 | 설명 | 학생에게 중요한 이유 |

## 3. 단축키
| 키 | 동작 | 버전 | 비고 |

## 4. 연관 개념 그래프
### 선수 지식 (이걸 모르면 이해 불가)
### 연결 개념 (함께 쓰이는 것)
### 심화 (알면 이해가 깊어지는 것)

## 5. 학생 혼란 포인트 (커뮤니티 기반)
| 질문 (실제 포럼) | 출처 | 검증된 답변 |

## 6. 흔한 실수 & 해결
- 증상 → 원인 → 해결

## 7. 추천 비유 후보
- 비유 1: {일상 경험} — {왜 이 비유가 맞는지}

## 8. 크로스체크 로그
| 주장 | 소스 | 검증 결과 |
```

## 리서치 파이프라인

### Phase 1: 공식 소스 수집 (정확성)

| 도구 | 대상 |
|------|------|
| Context7 MCP | Blender Python API 문서 |
| WebFetch | docs.blender.org 해당 도구 페이지 직접 파싱 |
| WebFetch | wiki.blender.org 릴리즈 노트 (버전별 변경) |

- ① Context7, ② WebFetch 병렬 실행
- 정의, 파라미터, 단축키 추출

### Phase 2: 학생 혼란 포인트 수집 (공감)

| 도구 | 검색 쿼리 |
|------|----------|
| WebSearch | `"{tool}" blender why` site:reddit.com |
| WebSearch | `"{tool}"` site:blender.stackexchange.com |
| WebSearch | `"블렌더 {한글명}"` 한글 커뮤니티 |

- 세 검색 병렬 실행
- 상위 5-10개 반복 질문 패턴 식별

### Phase 3: 크로스체크

- Phase 2 질문을 Phase 1 공식 정보와 대조
- 틀린 커뮤니티 답변 표시 + 정정
- 연관 개념 그래프 구성:
  - 선수지식: "뭘 모르길래 이걸 물어보는가?" 역추적
  - 심화: 공식 문서 관련 항목 링크

### Phase 4: 교안용 가공

- CONTENT_GUIDE.md 톤 규칙 적용
- 비유 후보 생성 (일상 경험 기반)
- 흔한 실수 "증상 → 해결" 형식 변환
- 브리프 Markdown 파일 생성

## 모드 상세

### `--deep` 모드

연관 개념을 재귀적으로 리서치 (최대 깊이 2):

```
loop-cut 리서치
  ├── 선수지식: "점·선·면 위계"
  │   └── 재귀 → vertex-edge-face-brief.md (깊이 1)
  ├── 연관 파라미터: "R값과 세분화"
  │   └── 재귀 → subdivision-concept-brief.md (깊이 1)
  └── 깊이 2 → 중단, 참조 링크만
```

각 재귀는 병렬 에이전트로 실행.

### `week N` 모드

1. curriculum.js에서 week N의 showme ID 추출
2. 각 ID별 병렬 리서치 에이전트 실행
3. 결과 통합:
   - 개별 브리프 파일들
   - `week{NN}-summary.md`: 주차 전체 요약 + 개념 간 연결고리 + 학습 순서 권장

## 기존 스킬 연동

### 브리프 자동 감지

`/rpd-content-write`와 `/showme` 실행 시 `claudedocs/research/{id}-brief.md` 존재 여부 확인:
- 있으면 → 자동 참조 (비유, 실수, 단축키 가져옴)
- 없으면 → 경고: "리서치 브리프가 없습니다. /rpd-research 먼저 실행하시겠어요?"

### 연동 흐름

```
/rpd-research mirror-modifier     → brief.md 생성
/rpd-content-write week 3         → brief.md 참조하여 curriculum.js 작성
/showme mirror-modifier           → brief.md 참조하여 개념탭/퀴즈탭 채움
/rpd-week-review week 3           → brief 대비 정확성 검증
```

## 소스 신뢰도 우선순위

1. Blender 공식 문서 (docs.blender.org) — 1차 소스
2. Blender 릴리즈 노트/위키 — 버전별 변경사항
3. Blender Stack Exchange — 검증된 답변 (투표 기반)
4. Reddit r/blender — 실무 팁, 흔한 실수 패턴
5. YouTube 튜토리얼 — 비유/설명 참고 (사실 검증 필수)
