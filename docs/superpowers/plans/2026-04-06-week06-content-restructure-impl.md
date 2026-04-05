# Week 06 콘텐츠 재구성 — 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Week 6 Notion 페이지를 공통구조(Part 0~4)로 재구성하고 Week 7 브릿지(Image Texture + PBR 맵 + 로봇 과제)를 구축한다.

**Architecture:**
1단계 — ShowMe 카드 4개 신규 작성 + 기존 3개 보강 (course-site repo).
2단계 — Notion Week 6 페이지 백업 → 블록 재구성 → 검증 (Notion MCP API).
3단계 — Notion Week 9 prereq 문구 업데이트.

**Tech Stack:**
- ShowMe 카드: HTML (self-contained, 기존 `material-basics.html` 패턴)
- Registry: `course-site/assets/showme/_registry.js` (JS object)
- Notion: `mcp__notion__*` MCP 도구
- Git: 주차별 커밋, 기존 `feat/nav-label-unification` 또는 신규 브랜치

**Design Spec:** `docs/superpowers/specs/2026-04-06-week06-content-restructure-design.md`

---

## 사전 준비

### Task 0: 작업 브랜치 결정 및 설정

**Files:** (없음 — git만)

- [ ] **Step 1: 현재 브랜치 확인**

Run: `git status && git branch --show-current`
Expected: 현재 `feat/nav-label-unification` 브랜치에 이미 Week 6 spec 커밋돼 있음

- [ ] **Step 2: 브랜치 전략 확정 (사용자 확인)**

선택지:
- (a) 현재 `feat/nav-label-unification`에서 계속 작업 (nav 작업과 섞임)
- (b) 신규 브랜치 `feat/week06-restructure` 생성 (권장)

Run (선택 b인 경우):
```bash
git checkout -b feat/week06-restructure
```

- [ ] **Step 3: 작업 디렉터리 상태 확인**

Run: `git status`
Expected: Clean working tree (또는 관련 untracked만)

---

## Phase 1: ShowMe 카드 4개 신규 작성

### Task 1: `color-ramp` 카드 작성 (🟡 권장)

**Files:**
- Create: `course-site/assets/showme/color-ramp.html`

- [ ] **Step 1: 기존 카드 템플릿 확인**

Read: `course-site/assets/showme/material-basics.html` (구조/스타일 참조용)

- [ ] **Step 2: `color-ramp.html` 작성**

내용 가이드:
- **제목**: "Color Ramp — 단색을 그라데이션으로"
- **아날로지**: "그래픽 에디터의 그라디언트 도구와 같아요"
- **핵심 3가지**:
  1. Fac 입력(0~1 값) → 색 팔레트로 변환
  2. 색상 stop 추가/제거 (+/- 버튼)
  3. Interpolation 모드 (Linear/Constant/Ease)
- **Before/After**: 단색 Base Color → Color Ramp 연결 후 그라데이션
- **혼란 해결**:
  - "색이 안 바뀌어요" → Fac 입력에 뭔가 연결돼야 함 (상수 0.5면 하나의 색만)
  - "중간색이 안 나와요" → Interpolation을 Linear로
- **연결 예시**: `Noise Texture (Fac) → Color Ramp → Principled BSDF (Base Color)`

기존 `material-basics.html`의 HTML/CSS 그대로 복사 후 본문만 교체.

- [ ] **Step 3: 로컬 미리보기**

Run preview_start if needed, open `course-site/assets/showme/color-ramp.html`, verify 렌더링 OK.

- [ ] **Step 4: 커밋**

```bash
git add course-site/assets/showme/color-ramp.html
git commit -m "feat(showme): add color-ramp card for Week 6"
```

---

### Task 2: `noise-texture` 카드 작성 (🟡 권장)

**Files:**
- Create: `course-site/assets/showme/noise-texture.html`

- [ ] **Step 1: 카드 내용 작성**

내용 가이드:
- **제목**: "Noise Texture — 수식으로 만드는 무늬"
- **아날로지**: "난수 생성기가 만드는 구름 모양 패턴"
- **핵심 파라미터**:
  - **Scale**: 무늬 크기 (작으면 촘촘, 크면 성김)
  - **Detail**: 세부 디테일 반복 횟수
  - **Roughness**: 디테일 강도
  - **Distortion**: 패턴 왜곡
- **Before/After**: 단색 Roughness 1.0 → Noise Texture → Color Ramp → Roughness 연결로 "녹슨" 느낌
- **혼란 해결**:
  - "무늬가 안 보여요" → Material Preview 모드 확인 + Scale 값 키우기
  - "너무 거칠거나 밋밋해요" → Detail + Roughness 조합
- **연결 예시**: `Noise Texture (Fac) → ColorRamp → Principled BSDF (Roughness)`

- [ ] **Step 2: HTML 작성 (material-basics 템플릿 복사)**

Create file with identical structure to `material-basics.html`, body 교체.

- [ ] **Step 3: 로컬 미리보기**

- [ ] **Step 4: 커밋**

```bash
git add course-site/assets/showme/noise-texture.html
git commit -m "feat(showme): add noise-texture card for Week 6"
```

---

### Task 3: `texture-types` 카드 작성 (🔴 필수)

**Files:**
- Create: `course-site/assets/showme/texture-types.html`

- [ ] **Step 1: 카드 내용 작성**

내용 가이드:
- **제목**: "Procedural vs Image Texture — 언제 뭘 쓸까"
- **아날로지**: "수채화 vs 사진 붙이기"
- **비교표 (핵심)**:

| 항목 | Procedural (Noise/Musgrave) | Image Texture |
|---|---|---|
| 소스 | 수식 (실시간 계산) | 파일 (jpg/png/exr) |
| 해상도 | 무한 확대 OK | 픽셀 한계 있음 |
| 용량 | 0 byte | 수 MB |
| 강점 | 노이즈·잡음·자연 패턴 | 구체적 디테일 (벽돌, 나무결) |
| UV 필요 | ❌ | ✅ (없으면 왜곡) |

- **Before/After**: "녹슨 금속" 시뮬레이션:
  - Procedural: Noise+ColorRamp → 수식으로
  - Image: Poly에서 "rusty metal" PBR 맵 → 사실적 사진
- **혼란 해결**:
  - "이미지 텍스처가 늘어나요" → UV가 없어서. Week 7에서 해결
  - "어느 쪽을 써야 해요?" → 빠른 실험/추상 = Procedural, 사실성 = Image

- [ ] **Step 2: HTML 작성 (비교표는 `<table>` 사용)**

- [ ] **Step 3: 로컬 미리보기 — 테이블 스타일 확인**

- [ ] **Step 4: 커밋**

```bash
git add course-site/assets/showme/texture-types.html
git commit -m "feat(showme): add texture-types card (Procedural vs Image)"
```

---

### Task 4: `image-texture-pbr` 카드 작성 (🔴 필수)

**Files:**
- Create: `course-site/assets/showme/image-texture-pbr.html`

- [ ] **Step 1: 카드 내용 작성**

내용 가이드:
- **제목**: "Image Texture & PBR 맵 — Poly로 AI 텍스처 붙이기"
- **아날로지**: "재료 상자 — 색/거칠기/요철 3장을 세트로 씀"
- **PBR 맵 3종**:
  - **Color (Diffuse)**: 표면 색 정보 — sRGB
  - **Roughness**: 얼마나 거친지 (흑백 이미지) — Non-Color
  - **Normal**: 표면 요철 (파란 이미지) — Non-Color
- **Poly 워크플로우** (6단계):
  1. [withpoly.com](https://withpoly.com) 가입
  2. 프롬프트 작성 (예: "rusty painted metal")
  3. PBR 4종 맵 다운로드 (Color/Normal/Rough/AO)
  4. Blender Shader Editor에 Image Texture 3개 추가
  5. 각 맵을 BSDF에 연결 (Normal은 Normal Map 노드 경유)
  6. Color Space 설정 확인 (Color=sRGB, 나머지=Non-Color)
- **연결 다이어그램** (ASCII):
```
[Image:Color]    → [Principled BSDF: Base Color]
[Image:Rough]    → [Principled BSDF: Roughness]
[Image:Normal]   → [Normal Map] → [Principled BSDF: Normal]
```
- **혼란 해결**:
  - "Normal 맵이 이상해요" → Color Space가 sRGB로 돼있음. Non-Color로
  - "색이 바랬어요" → Color 맵의 Color Space가 Non-Color로 돼있음. sRGB로
  - "이미지가 늘어나요" → UV 없음 (Week 7 해결)

- [ ] **Step 2: HTML 작성**

- [ ] **Step 3: 로컬 미리보기**

- [ ] **Step 4: 커밋**

```bash
git add course-site/assets/showme/image-texture-pbr.html
git commit -m "feat(showme): add image-texture-pbr card (Poly PBR workflow)"
```

---

## Phase 2: _registry.js 업데이트 + 기존 카드 보강

### Task 5: `_registry.js` 업데이트 (신규 4 + viewport-shading 태그)

**Files:**
- Modify: `course-site/assets/showme/_registry.js`

- [ ] **Step 1: 기존 registry 확인**

Read: `course-site/assets/showme/_registry.js` (Week 6 섹션 찾기)

- [ ] **Step 2: 신규 4개 + viewport-shading Week 6 태그 추가**

Edit `_registry.js`, Week 6 섹션에 추가 (예: 기존 `shader-editor` 다음 줄):

```js
  "shader-editor":          { label: "Shader Editor 이해",      icon: "🔌", week: 6 },
  "color-ramp":             { label: "Color Ramp 단색→그라데이션", icon: "🌈", week: 6 },
  "noise-texture":          { label: "Noise Texture 무늬 만들기",  icon: "🌀", week: 6 },
  "texture-types":          { label: "Procedural vs Image",      icon: "🎨", week: 6 },
  "image-texture-pbr":      { label: "Image Texture & PBR 맵",   icon: "🖼️", week: 6 },
  "viewport-shading":       { label: "뷰포트 Shading 4모드",     icon: "🎨", week: 6 },
```

참고: `viewport-shading`이 이미 다른 week에 등록돼있으면 해당 라인 수정 (중복 등록 금지).

- [ ] **Step 3: JS 문법 검증**

Run: `node -e "require('./course-site/assets/showme/_registry.js')"` 또는 브라우저에서 import 확인

- [ ] **Step 4: 커밋**

```bash
git add course-site/assets/showme/_registry.js
git commit -m "feat(showme): register 4 new Week 6 cards + viewport-shading tag"
```

---

### Task 6: `shader-editor` 카드 보강 (기존 업데이트)

**Files:**
- Modify: `course-site/assets/showme/shader-editor.html`

- [ ] **Step 1: 현재 내용 감사**

Read: `course-site/assets/showme/shader-editor.html`

체크 항목:
- 레고 블록 비유 포함 여부
- 소켓 색깔 매칭(노랑/회색/보라) 설명 여부
- Material Output 필수 언급 여부

- [ ] **Step 2: 누락된 부분 보강**

편집 방침:
- 레고 비유 없으면 상단 analogy 섹션에 추가
- 소켓 색 매칭 confusion 항목 추가:
  - "소켓이 연결이 안 돼요" → 색깔이 다르면 타입 불일치
  - 색 대응표: 노란색=Color, 회색=Value, 보라=Vector
- Material Output이 마지막 종착점임을 명시

- [ ] **Step 3: 로컬 미리보기로 변경 확인**

- [ ] **Step 4: 커밋**

```bash
git add course-site/assets/showme/shader-editor.html
git commit -m "feat(showme): enhance shader-editor card (Lego analogy + socket colors)"
```

---

### Task 7: `principled-bsdf` 카드 감사 (Emission 포함 확인)

**Files:**
- Modify: `course-site/assets/showme/principled-bsdf.html` (필요 시)

- [ ] **Step 1: 현재 내용 감사**

Read: `course-site/assets/showme/principled-bsdf.html`

체크 항목:
- Metallic, Roughness, Transmission, **Emission** 4개 모두 설명되어있는지
- "유리가 검게 보여요 → HDRI 필요" confusion 포함 여부

- [ ] **Step 2: Emission 누락 시 추가**

(필요한 경우에만) Emission 파라미터 설명 추가:
- Emission Color + Strength
- Rendered 모드에서만 보임
- 용도: 램프, LED, 모니터 화면

- [ ] **Step 3: 커밋 (변경 있는 경우)**

```bash
git add course-site/assets/showme/principled-bsdf.html
git commit -m "feat(showme): ensure Emission coverage in principled-bsdf card"
```

---

## Phase 3: Notion Week 6 페이지 백업

### Task 8: Week 6 페이지 백업 복사본 생성

**Files:** (없음 — Notion 작업)

- [ ] **Step 1: 현재 Week 6 전체 블록 덤프 저장 (안전망)**

Run:
```
mcp__notion__API-get-block-children(block_id: "31354d65-4971-818c-8cb5-e7814445e3eb", page_size: 100)
```
저장 경로: `.tmp/week06-backup-2026-04-06.json`

백업 파일 수동 저장 (Write tool 사용)

- [ ] **Step 2: Notion에 archive 페이지 생성 (수동)**

사용자에게 요청:
> "Notion UI에서 Week 6 페이지를 복제해서 'Week 06 BACKUP 2026-04-06' 이름으로 archive 폴더에 두시겠어요? API로도 가능하지만 수동이 안전해요."

또는 API로 신규 페이지 생성 + 블록 복사 (복잡) — 수동 권장.

- [ ] **Step 3: 백업 완료 확인**

사용자 확인 후 다음 단계 진행.

- [ ] **Step 4: 커밋 (백업 JSON)**

```bash
mkdir -p .tmp
git add .tmp/week06-backup-2026-04-06.json
git commit -m "chore(backup): Week 6 Notion blocks dump before restructure"
```

(`.tmp/`이 `.gitignore`에 있으면 커밋 생략)

---

## Phase 4: Notion Week 6 페이지 재구성

**전략:** 기존 블록을 순서대로 **위에서부터** 수정 + 새 블록 append. 한 Part 작업 완료 후 커밋 체크포인트 없음(Notion은 git 아님) → 각 Part 완료 시 **사용자 시각 확인** 필수.

### Task 9: 페이지 제목 + Part 0 (오리엔테이션) 작성

**Files:** (Notion 작업만)

- [ ] **Step 1: 페이지 제목 업데이트**

Run:
```
mcp__notion__API-patch-page(
  page_id: "31354d65-4971-818c-8cb5-e7814445e3eb",
  properties: {
    title: [{ text: { content: "Week 06: Material & Shader Node + AI PBR Texture" }}]
  }
)
```

- [ ] **Step 2: 기존 "학습 목표" heading_2 블록 ID 찾기**

이전 백업 JSON에서 첫 번째 heading_2(학습 목표) 블록 ID 확인.

- [ ] **Step 3: 페이지 최상단에 Part 0 블록들 append (신규)**

순서:
1. heading_2: "🔗 이전 주차 복습"
2. paragraph: "Week 5에서 AI(Meshy/Tripo)로 생성한 로봇 모델을 이번 주에 재질을 입혀 완성체로 만들어요. Week 5 Step 6에서 저장한 .blend 파일이 오늘의 재료예요."
3. heading_2: "✅ 수업 시작 체크리스트"
4. to_do 4개:
   - "Week 5 .blend 파일 열려있다"
   - "Blender 5.0.1 이상"
   - "Poly (withpoly.com) 가입 완료"
   - "Material Preview 모드로 현재 로봇 상태 확인"
5. heading_2: "🎯 학습 목표"
6. bulleted_list_item 5개 (spec Part 0 학습 목표 참조)

Run: `mcp__notion__API-patch-block-children` with 위 블록들을 `children` 배열로.

⚠️ Notion API는 블록 순서를 "append at end"만 지원. 페이지 최상단 배치가 필요하면 **기존 블록을 모두 지우고 재생성**하거나 **신규 블록이 맨 아래로 가도 OK로 수용**.

**결정 필요**: 사용자에게 확인:
- (a) 블록 전체 지우고 새 순서로 재생성 (파괴적, 정확)
- (b) 기존 블록 유지 + 신규 Part 0 맨 아래 append + 수동으로 Notion UI에서 순서 조정
- (c) 기존 heading_2를 in-place 수정(append 없이) + 새 heading_2는 맨 아래 append → 결과물 수동 정렬

**권장: (a) 파괴적 재생성** (백업 있으므로 안전). 이후 모든 Task 9~13은 (a) 전제로 진행.

- [ ] **Step 4: (a) 택한 경우) 기존 블록 전부 archive/delete**

기존 63개 블록 중 페이지 직접 자식 블록만 archive:
```
For each child block id in Week 6:
  mcp__notion__API-update-a-block(block_id, archived: true)
```

- [ ] **Step 5: Part 0 블록들 새로 append**

`mcp__notion__API-patch-block-children` 호출 (위 Step 3 내용)

- [ ] **Step 6: 사용자 시각 확인**

> "Notion에서 Week 6 페이지 열어서 Part 0(이전주차복습/시작체크리스트/학습목표)이 잘 보이는지 확인해주세요. OK면 Part 1 진행합니다."

---

### Task 10: Part 1 (이론 5 토픽) 작성

**Files:** (Notion 작업만)

- [ ] **Step 1: Part 1 구분자 heading_1 추가**

```
heading_1: "═══ Part 1: 이론 ═══"
```

또는 Notion divider + heading_2 조합:
- divider
- heading_2: "📖 Part 1 — 이론"

- [ ] **Step 2: 1.1 Material이란 블록 추가**

- heading_3: "1.1 Material이란 무엇인가"
- paragraph (spec 본문 서술 복붙)
- callout: "💡 ShowMe 카드: material-basics" + 링크

- [ ] **Step 3: 1.2 ~ 1.5 동일 패턴으로 추가**

각 토픽별:
- heading_3 (제목)
- paragraph (본문 서술 3~5줄)
- callout (ShowMe 카드 링크)

1.5는 ShowMe 카드 없음 → callout 대신 "→ Week 7에서 depth 보강" 안내.

- [ ] **Step 4: 사용자 시각 확인 + 커밋 체크포인트 없음 (Notion)**

> "Notion에서 Part 1 이론 섹션 확인해주세요. 5 토픽이 순서대로 있고, ShowMe 링크가 잘 보이나요?"

---

### Task 11: Part 2 (실습 7 Steps) 작성

**Files:** (Notion 작업만)

- [ ] **Step 1: Part 2 구분자 + heading_2 추가**

- divider
- heading_2: "🔧 Part 2 — 실습"

- [ ] **Step 2: Step 1 (Remesh로 작업 준비) 작성**

- heading_3: "Step 1: Remesh로 작업 준비"
- paragraph (목표 1줄)
- to_do 4개 (spec Step 1 참조)
- callout: ShowMe remesh-modifier, decimate-modifier 링크

- [ ] **Step 3: Step 2 (Material 할당 + BSDF) 작성**

- heading_3: "Step 2: Material 할당 + Principled BSDF 탐색"
- paragraph (목표 1줄)
- to_do 7개 (spec Step 2 참조)

- [ ] **Step 4: Step 3 (Shader Editor + Color Ramp) 작성**

- heading_3: "Step 3: Shader Editor + Color Ramp"
- paragraph
- to_do 4개
- callout: color-ramp ShowMe

- [ ] **Step 5: Step 4 (Procedural Texture) 작성**

- heading_3: "Step 4: Procedural Texture (Noise)"
- paragraph
- to_do 4개
- callout: noise-texture ShowMe

- [ ] **Step 6: Step 5 (Image Texture + Poly PBR) 작성 ⭐ 신규**

- heading_3: "Step 5: Image Texture + Poly PBR 4종 맵"
- paragraph (목표 1줄)
- to_do 7개 (spec Step 5 참조)
- callout (경고/안내): "이미지가 로봇에 이상하게 늘어나 보이나요? 정상이에요 — UV가 없어서. Week 7에서 배워요."
- callout: image-texture-pbr ShowMe

- [ ] **Step 7: Step 6 (로봇 3개 복제 & 재질 적용) 작성 ⭐ 신규**

- heading_3: "Step 6: 로봇 3개 복제 & 재질 적용"
- paragraph
- to_do 5개 (spec Step 6 참조)

- [ ] **Step 8: Step 7 (MCP 맛보기) 작성 ⭐ 신규 선택**

- heading_3: "Step 7 (선택): MCP로 Material 자동 생성 맛보기"
- paragraph (목표 1줄 + 선택 사항 표시)
- to_do 5개 (spec Step 7 참조)
- callout: "MCP는 Week 9에서 조명 연출로 본격 다뤄요. 이번 주는 맛보기."

- [ ] **Step 9: 사용자 시각 확인**

> "Notion에서 Part 2 실습 7 Steps 확인. Step 5/6/7 신규 내용 문제없나요?"

---

### Task 12: Part 3 (정리) 작성

**Files:** (Notion 작업만)

- [ ] **Step 1: Part 3 구분자 + heading_2 추가**

- divider
- heading_2: "🎯 Part 3 — 정리"

- [ ] **Step 2: 흔한 실수 (개념 오해) 추가**

- heading_3: "⚠️ 흔한 실수 (개념 오해)"
- numbered_list_item 5개 (spec Part 3.4.1 내용)

- [ ] **Step 3: 핵심 정리 5줄 요약 추가**

- heading_3: "✨ 핵심 정리"
- code block (language: plaintext, spec 5줄 요약 복붙)

- [ ] **Step 4: 과제 추가**

- heading_3: "📝 과제 — 로봇 3종 재질 챌린지"
- paragraph (과제 설명)
- heading_3 (h4 역할): "필수 (3개)"
- bulleted_list_item 3개 (로봇 A/B/C)
- heading_3: "도전 (선택)"
- bulleted_list_item 1개 (로봇 D MCP)
- heading_3: "제출물"
- to_do 4개
- heading_3: "평가 포인트"
- bulleted_list_item 3개

- [ ] **Step 5: 사용자 시각 확인**

---

### Task 13: Part 4 (학생 리소스) 작성

**Files:** (Notion 작업만)

- [ ] **Step 1: Part 4 구분자 + heading_2 추가**

- divider
- heading_2: "📚 Part 4 — 학생 리소스"

- [ ] **Step 2: 단축키 퀵 레퍼런스 추가**

- heading_3: "⌨️ 단축키 퀵 레퍼런스"
- code block (spec 단축키 블록 3섹션 복붙)

- [ ] **Step 3: 자주 막히는 지점 (실무 트러블슈팅) 추가**

- heading_3: "🔧 자주 막히는 지점"
- numbered_list_item 7개 (spec Part 4.5.2 내용 — 증상→해결)

- [ ] **Step 4: 공식 영상 + 공식 문서 추가**

- heading_3: "🎥 공식 영상"
- bulleted_list_item 2개
- heading_3: "📖 공식 문서"
- bulleted_list_item 5개 (Blender Manual 링크)

- [ ] **Step 5: 참고자료 추가**

- heading_3: "🔗 참고자료"
- heading_3 (h4): "AI 텍스처 도구"
- bulleted_list_item 3개 (Poly/Polycam/Substance)
- heading_3 (h4): "무료 PBR 텍스처 라이브러리"
- bulleted_list_item 3개 (Poly Haven/AmbientCG/Textures.com)
- heading_3 (h4): "HDRI"
- bulleted_list_item 1개 (Poly Haven HDRIs)

- [ ] **Step 6: Week 6 완료 체크리스트 추가**

- heading_3: "☑️ Week 6 완료 체크리스트"
- to_do 7개 (spec Part 4.5.5 내용)

- [ ] **Step 7: Week 7 예고 callout**

- callout: "💡 다음 주: Image Texture가 이상하게 늘어난다는 이슈, 기억나요? 다음 주 UV Unwrapping에서 해결합니다. Week 6 .blend 파일 꼭 저장해두세요."

- [ ] **Step 8: 사용자 전체 페이지 시각 확인**

> "Notion Week 6 페이지 전체 열어서 Part 0 → 1 → 2 → 3 → 4 순서대로 잘 보이는지 확인해주세요. 이상한 곳 있으면 알려주세요."

---

## Phase 5: Notion Week 9 prereq 문구 업데이트

### Task 14: Week 9 페이지 MCP prereq 톤 조정

**Files:** (Notion 작업만)

- [ ] **Step 1: Week 9 페이지 블록 덤프**

Run:
```
mcp__notion__API-get-block-children(block_id: "31354d65-4971-819a-8d55-c976c875a2a1")
```

- [ ] **Step 2: "MCP 첫 만남" 톤 블록 탐색**

키워드: "MCP 처음", "MCP란", "설치", "addon"

- [ ] **Step 3: 톤 수정**

"처음 만난다" → "Week 6 Step 7에서 만났던 MCP를 이번엔 조명 연출에 사용" 톤으로.

구체 패치:
- 해당 paragraph/callout 블록의 rich_text를 `mcp__notion__API-update-a-block`으로 수정
- 설치 가이드가 있으면 "Week 6 Step 7에서 이미 설치됐다면 스킵" 안내 추가

- [ ] **Step 4: 사용자 시각 확인**

> "Notion Week 9 페이지에서 MCP 섹션이 Week 6 맛보기 이후 톤으로 자연스럽게 연결되는지 확인해주세요."

---

## Phase 6: 최종 검증 및 정리

### Task 15: 사이트 렌더링 검증 (ShowMe 카드)

**Files:** (없음)

- [ ] **Step 1: 로컬 dev server 실행**

Run: preview_start (또는 기존 방식)

- [ ] **Step 2: ShowMe 카드 4개 모두 브라우저에서 렌더링 확인**

각 카드 URL 방문:
- `/course-site/assets/showme/color-ramp.html`
- `/course-site/assets/showme/noise-texture.html`
- `/course-site/assets/showme/texture-types.html`
- `/course-site/assets/showme/image-texture-pbr.html`

체크:
- 스타일 깨짐 없음
- 이미지/링크 깨짐 없음
- 모바일 viewport (375px) 정상

- [ ] **Step 3: Week 6 커리큘럼 페이지 (있다면) 확인**

`course-site/curriculum/week-06/` 또는 유사 경로 존재 여부 확인. 있으면 ShowMe 카드 링크 반영 여부 체크.

- [ ] **Step 4: 문제 발견 시 수정 + 커밋**

---

### Task 16: 커밋 로그 정리 및 PR 준비

**Files:** (git)

- [ ] **Step 1: 전체 커밋 히스토리 확인**

Run: `git log --oneline feat/week06-restructure ^main | head -20`

Expected: Task 1~14의 커밋들이 순서대로

- [ ] **Step 2: 사용자에게 머지 방식 확인**

선택지:
- (a) PR 생성 → main 머지
- (b) 직접 main에 머지
- (c) 작업 브랜치 유지 (검토 더 필요)

- [ ] **Step 3: (선택) PR 생성**

Run (선택 a):
```bash
gh pr create --title "Week 06 콘텐츠 재구성 (공통구조 + Week 7 브릿지)" --body "$(cat <<'EOF'
## Summary
- Week 6 Notion 페이지를 공통구조 Part 0~4로 재구성
- ShowMe 카드 4개 신규 작성 (color-ramp, noise-texture, texture-types, image-texture-pbr)
- Week 7 브릿지 구축: Image Texture + PBR 맵 3종 + 로봇 3종 재질 챌린지 과제
- Week 9 MCP prereq 문구 업데이트

## Spec
`docs/superpowers/specs/2026-04-06-week06-content-restructure-design.md`

## Test plan
- [ ] Notion Week 6 페이지 렌더링 시각 확인
- [ ] ShowMe 카드 4개 브라우저 렌더링 OK
- [ ] Week 9 페이지 톤 자연스러움
- [ ] .blend 파일 Week 7 연결 언급 확인

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

---

## Open Questions (실행 중 사용자 결정 필요)

1. **Task 0 Step 2**: 브랜치 선택 (현재 `feat/nav-label-unification` vs 신규 `feat/week06-restructure`)
2. **Task 8**: Notion 백업 방식 (수동 UI 복제 vs API로 새 페이지 생성 후 블록 복사)
3. **Task 9 Step 3 결정**: 기존 블록 파괴적 재생성 (a) vs 순서 수동 조정 (b/c)
4. **Task 14**: Week 9 MCP 섹션 구체 위치 — 블록 ID 탐색 후 확인

---

## Rollback 전략

Notion 작업 실패 시:
1. 백업 JSON에서 원본 블록 구조 복원
2. 수동으로 Notion UI에서 백업 페이지 내용 복사 후 Week 6에 붙여넣기
3. git revert로 _registry.js 롤백

ShowMe 카드 문제 시:
1. git revert 해당 카드 커밋
2. Notion에서 해당 ShowMe 링크 제거

---

## 예상 작업 규모

- Phase 1~2 (ShowMe 카드): Task 1~7 = 7 커밋
- Phase 3 (백업): Task 8 = 1 커밋
- Phase 4 (Notion 재구성): Task 9~13 = Notion 작업(커밋 없음) + 사용자 확인 포인트 5회
- Phase 5 (Week 9): Task 14 = Notion 작업
- Phase 6 (검증): Task 15~16 = 검증 + 선택적 PR
