---
description: "인지부하 기반 UI 단순화와 페이지 리디자인 + 디자인 시스템 검증. 예: /design-agent audit library, /design-agent pre-check '레일 폰트 변경', /design-agent post-verify, /design-agent system-check"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(node:*), Bash(ls:*), Bash(wc:*), Bash(curl:*), Agent, mcp__Claude_Preview__preview_start, mcp__Claude_Preview__preview_stop, mcp__Claude_Preview__preview_screenshot, mcp__Claude_Preview__preview_snapshot, mcp__Claude_Preview__preview_eval, mcp__Claude_Preview__preview_resize, mcp__Claude_Preview__preview_inspect, mcp__Claude_Preview__preview_console_logs
---

## Context

- 프로젝트 루트: !`git rev-parse --show-toplevel 2>/dev/null`
- 주요 페이지: !`ls course-site/*.html 2>/dev/null | xargs -I{} basename {} | tr '\n' ' '`
- ShowMe 카드 수: !`ls course-site/assets/showme/*.html 2>/dev/null | grep -v _template | wc -l | tr -d ' '`개
- 스타일 가이드: !`ls docs/COURSE_SITE_STYLE_GUIDE_2026-03-13.md docs/COGNITIVE_UI_GUIDE_2026-03-18.md docs/DESIGN_SYSTEM.md 2>/dev/null | tr '\n' ' '`
- 디자인 시스템 설계: !`ls docs/plans/2026-03-19-design-system-director-design.md 2>/dev/null`

## Task

인자: `$ARGUMENTS`

---

## 최신 근거 수집 규칙

사용자가 `최신`, `current`, `2026`, `근거`, `검증`, `공신력`을 언급하면 수정 전에 먼저 웹에서 확인한다.

출처 우선순위:
1. **W3C / WAI / WCAG**
2. **정부 디자인 시스템·매뉴얼** (GOV.UK, USWDS, DfE)
3. **플랫폼 공식 가이드** (Apple HIG, Material Design, Microsoft Fluent)
4. **동료심사 HCI / Human Factors 연구**
5. 블로그·에이전시 글은 보조 참고만 허용

2026-03-18 기준 직접 확인한 현재 출처:
- W3C Cognitive Accessibility at W3C — 2024-04-25 업데이트
- W3C Content Usable / Clear Content / WCAG 2.2 Consistent Help
- W3C Cognitive Accessibility Research Modules — 2026-02-05 공개 버전
- GOV.UK Service Manual — Writing for user interfaces
- USWDS Design principles / Accessibility / Progress easily
- DfE Accessibility Manual — COGA guidelines

---

## 모드 분기

### `pre-check "변경 설명"` — 변경 전 영향 분석

수정을 시작하기 전에 호출한다. 변경이 디자인 시스템을 위반하는지, 연쇄 수정이 필요한지 판단.

흐름:
1. 변경 설명 파싱 → 영향받는 CSS/HTML 파일 식별
2. `docs/DESIGN_SYSTEM.md` (없으면 `docs/plans/2026-03-19-design-system-director-design.md`) 규칙 대조
3. 영향받는 다른 페이지 목록 생성
4. 위반 없음 → "✅ 진행하세요"
   위반 있음 → "⚠️ [규칙] 위반. 연쇄 수정 필요: [파일 목록]"

### `post-verify` — 변경 후 전체 검증

수정 완료 후 호출한다. 모든 퍼블릭 페이지를 스크린샷으로 검증.

흐름:
1. preview_start → 모든 퍼블릭 페이지 순회 (index, library, shortcuts, prototype, week/deck)
2. 각 페이지 desktop(1280x800) + mobile(375x812) 스크린샷
3. 아래 체크리스트 대조:
   - 스페이싱 스케일 준수? (4/8/12/16/24/32/48/64px만 허용)
   - border-radius 스케일 준수? (8/12/16/20/24/999px)
   - font-weight 스케일 준수? (400/500/600/700)
   - 컬러 규칙 준수? (키컬러 = 블루만, 덱 컬러 = dot/아이콘만)
   - 카드 정보 밀도 1축?
   - 터치 타겟 44px?
   - focus-visible 있음?
4. **비율/스케일링 검증** (아래 "시각 비율 검증" 섹션 참조)
5. **벤치마크 비율 검증** (`docs/plans/2026-03-20-benchmark-design-rules.md` 참조)
   - 레일 비율: 56/220px (Linear 기준 ±10px)
   - 카드 그리드 갭: 16px (Vercel 기준)
   - 본문 폰트: 탐색 14px / 학습 16px
   - 배경 3-layer 밝기 차이: OKLCH 10-12 단위
   - 탐색 모드 = 쿨톤, 학습 모드 = 웜톤 확인
   - 스페이싱 스케일 준수: 4/8/12/16/24/32/48/64px만 허용
6. 위반 리포트 출력 — 문제가 있으면 **반드시 지적**

### `audit {target}` — 정보 과밀도 + 시각 비율 감사

지정한 페이지나 컴포넌트의 인지부하와 시각 비율을 점검한다.

**인지부하 점검:**
- 반복 카드에 한 번에 몇 개의 정보 축이 노출되는지
- 제목, 검색, 필터, 상태 배지 중 무엇이 첫 시선 경로를 끊는지
- 클릭 전에 꼭 필요한 정보와 클릭 후로 미뤄도 되는 정보가 섞여 있는지
- 모바일에서 한 화면에 보이는 선택지가 과도하게 시끄럽지 않은지
- 도움말, 탐색, 닫기 위치가 페이지 간 일관된지
- 정보가 한 번에 너무 큰 덩어리로 제시되지 않는지

**시각 비율 점검** (아래 "시각 비율 검증" 섹션 참조)

출력은 아래 우선순위를 따른다:
1. 학생이 바로 헷갈리는 문제
2. 비율/가독성 문제 (너무 작거나 큰 요소)
3. 시선 분산을 만드는 문제
4. 일관성/접근성 문제

**의도된 결과물이라도 문제가 보이면 반드시 지적한다.** "이전 세션에서 만든 거니까 맞겠지"로 넘어가지 않는다.

### `simplify {target}` — 저잡음 리디자인 적용

대상 페이지를 실제로 수정한다.

핵심 원칙:
1. **한 카드 = 한 결정** — 12개 이상이면 기본 상태 = 이름만
2. **검색 전 스캔 가능** — 훑어보기 먼저, 검색은 그 다음
3. **점진적 공개** — 설명은 hover/모달/패널로
4. **한 페이지 한 강조** — 강조 색 역할 하나만
5. **일관된 예측 가능성** — 버튼/닫기/필터/위계 동일

### `apply {target}` — 감사 + 수정 + 검증

1. `audit` 수행
2. 가장 큰 인지부하 원인 1~3개 제거
3. 모바일/키보드/빈 검색 결과 상태 확인
4. 바뀐 이유를 `docs/COGNITIVE_UI_GUIDE_2026-03-18.md` 기준으로 짧게 기록

### `system-check` — 디자인 시스템 vs 코드 불일치 감지

1. `docs/DESIGN_SYSTEM.md` (없으면 설계 문서) 파싱 → 규칙 목록 추출
2. tokens.css + components.css + page-*.css 스캔
3. HTML 인라인 스타일 스캔
4. 불일치 리포트:
   - 문서에 없는 토큰이 코드에 있음
   - 코드에서 금지 값 사용 (중간 스페이싱, 비표준 font-weight 등)
   - 컴포넌트 카탈로그에 없는 패턴 사용
   - **상대 단위 vs 절대 단위 혼용** 지적

### `compact library` — 라이브러리 전용 규칙

`course-site/library.html`에는 아래를 기본으로 적용한다:
- 카드에는 이름만 노출
- 검색창과 카테고리 필터는 유지
- 상세 정보는 모달 안 ShowMe 카드에서만 제공
- 카드 정렬은 스캔하기 쉬운 단순 패턴 우선

---

## 시각 비율 검증 🔴

audit, post-verify 모드에서 반드시 점검. preview 스크린샷을 찍어서 육안 확인.

### 반응형 스케일링
- 레이아웃 요소(레일, 카드, 헤더)가 뷰포트에 비례하여 적절한 비율을 유지하는지
- 고정 px만 쓰면 큰 화면에서 너무 작아지고 작은 화면에서 넘침 → **rem, clamp(), vw 혼용 권장**
- 사이드 레일: 접힘 시 뷰포트의 ~4-5%, 펼침 시 ~15-18% 권장
- 메인 콘텐츠: max-width 제한하되 좁은 화면에서는 100% 채움

### 폰트 크기 비율
- 가장 작은 텍스트(캡션/칩): 최소 0.7rem (≈11.2px) 이상
- 본문: 0.86~0.94rem
- 카드 제목: 0.88~1rem
- 섹션 제목: 1~1.2rem (clamp 사용)
- 페이지 제목: clamp(1.5rem, 3vw, 2rem)
- **아이콘과 라벨의 크기 비율**: 아이콘이 라벨보다 시각적으로 1.2~1.5배 커야 인식 가능

### 여백과 밀도
- 카드 내부 패딩: 최소 12px, 권장 16px
- 카드 간 간격: 최소 8px, 권장 12~16px
- 레일 아이템 높이: 최소 40px (터치 타겟 고려)
- 레일 아이콘: 접힘 상태에서 최소 20px, 권장 24px

### 뷰포트별 확인
- **desktop (1280+)**: 레일 + 메인 비율이 자연스러운지
- **tablet (768~1279)**: 레일이 너무 좁거나 콘텐츠 가림 없는지
- **mobile (≤720)**: 하단 탭바로 전환, 탭 아이콘 최소 24px, 라벨 최소 0.6rem

### 문제 발견 시
- "좀 작아 보이지만 괜찮다" → ❌ 무조건 지적
- 비율 문제는 구체적 수치와 함께 보고 (현재값 → 권장값)
- preview_inspect로 실제 computed 값 확인 후 판단

---

## 연구 기반 판단 규칙

### 1. Extraneous load 제거
- 반복적 장식/메타 정보는 학습에 도움이 되지 않으면 제거
- 같은 정보를 여러 형태로 중복 노출하지 않음
- W3C COGA `Support Simplification` 준수

### 2. Choice complexity 관리
- 한 번에 비교할 차원을 줄임
- 많은 카드는 `이름`, `필터`, `검색` 중심
- 복잡한 조건은 `간단한 질문 흐름`으로

### 3. Visual complexity 관리
- 카드 내부 요소 수를 줄여 검색 속도와 기억 성능 확보
- 그림, 배지, 보조 텍스트는 "찾기 속도"를 올릴 때만
- cluttered layout 피하고 중요 정보에만 시각적 위계

### 4. Focus-first 흐름
- 사용자가 읽지 않고 훑어본다는 가정
- 중요한 단어를 앞에, 설명보다 라벨을 먼저

### 5. Cognitive accessibility
- 일관된 위치, 예측 가능한 인터랙션, 짧은 문장
- mid-task 방해 요소 제거
- WCAG 2.2 Consistent Help / USWDS Progress easily 준수

---

## 검증 체크리스트

수정 후 반드시 확인:
- [ ] 첫 화면 3초 안에 "여기서 뭘 할 수 있는지" 보이는지
- [ ] 카드 하나에 기본 정보가 1개 축만 남았는지
- [ ] 검색 없이도 5~10개 항목을 빠르게 훑을 수 있는지
- [ ] 모바일에서 터치 타겟이 44px 근처인지
- [ ] 키보드 focus가 보이는지
- [ ] 빈 결과 / 긴 이름 / 다국어 상태가 깨지지 않는지
- [ ] **데스크톱/태블릿/모바일에서 비율이 자연스러운지** (스크린샷 확인)
- [ ] **폰트 크기가 뷰포트에 비례하여 가독성 유지하는지**
- [ ] **레일/카드/여백 비율이 디자인 시스템 스케일에 맞는지**

---

## 참조 파일

| 파일 | 역할 |
|------|------|
| `docs/DESIGN_SYSTEM.md` | 디자인 시스템 source of truth |
| `docs/plans/2026-03-19-design-system-director-design.md` | 디자인 시스템 설계 문서 |
| `docs/COGNITIVE_UI_GUIDE_2026-03-18.md` | 인지부하 기반 설계 근거 |
| `docs/COURSE_SITE_STYLE_GUIDE_2026-03-13.md` | RPD 시각 언어 기준 |
| `.claude/skills/rpd-site-improve/SKILL.md` | 사이트 수정 제약 |
| `.claude/skills/rpd-a11y-audit/SKILL.md` | 접근성 점검 기준 |
| `course-site/assets/tokens.css` | 디자인 토큰 |
| `course-site/assets/components.css` | 공유 컴포넌트 |
| `docs/plans/2026-03-20-benchmark-design-rules.md` | 벤치마크 디자인 규칙 (Linear+Brilliant+Vercel) |

## Gotchas ⚠️
> Claude가 이 스킬을 쓸 때 실수했던 것들. 새 함정 발견 시 여기에 추가.

1. prototype.html에 사이드 레일 CSS/HTML이 있었는데 뷰포트가 좁아 모바일 탭바로 보임 → preview 뷰포트를 1280+ 으로 확인할 것
2. 이전 세션 결과물이라도 비율/스케일링 문제를 그냥 넘기지 말 것 — "설계대로 구현됨"이 아니라 실제 사용성을 평가할 것
3. 설계 문서(DESIGN_SYSTEM.md, 설계 플랜)를 반드시 Read한 후 검증할 것 — 문서 만들어놓고 안 따르면 안 됨
