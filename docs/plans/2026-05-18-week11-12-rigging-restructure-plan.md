# Week 11-12 Rigging Restructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** W11/W12 커리큘럼을 design doc(2026-05-18-week11-12-rigging-restructure-design.md)에 정의된 새 구조로 Notion에서 재작성하고, 저장소에 동기화.

**Architecture:** Notion이 SoT. Notion MCP로 W11/W12 페이지 블록 수정 → `notion-sync.py`로 canonical/public 데이터 재생성 → `/rpd-check`로 검증 → 브라우저 시각 확인.

**Tech Stack:** Notion API (MCP), Python 3.12 (notion-sync.py / content_pipeline.py), 정적 사이트(vanilla JS), Playwright 검증.

**참고 설계 문서:** [docs/plans/2026-05-18-week11-12-rigging-restructure-design.md](2026-05-18-week11-12-rigging-restructure-design.md)

---

## Notion 페이지 ID

- **W11**: `31354d6549718135a3c2d960d69a7fb3`
- **W12**: `31354d6549718174bb74c528a6913fc0`

## 사전 조건

- `NOTION_TOKEN` 환경 변수 설정
- Notion MCP 연결 (`mcp__ed9f2562-...__notion-fetch`, `notion-update-page`, `notion-create-pages` 등)
- 작업 디렉토리: `/Users/ssongji/Developer/Workspace/RPD/.claude/worktrees/admiring-hermann-4c6e3c`

## 작업 흐름 원칙 (필독)

1. **Notion은 SoT**: 모든 콘텐츠 변경은 Notion에서 먼저. Repo curriculum.json/js 직접 수정 금지.
2. **append > edit > destructive**: 신규 step은 페이지 끝에 append. 기존 step 수정은 user 확인 후 edit. 기존 step 삭제(Weight Paint step)는 archive 처리.
3. **사용자 확인 게이트**: edit/destructive 동작 전 diff 요약 표시 → 1회 OK 받고 진행.
4. **CONTENT_GUIDE 톤 준수**: ~해요/~이에요, 결론 먼저, 비유는 학생 경험 기반.
5. **이모지 금지**: 본문/제목 모두 이모지 없음.

---

## File Structure

### 수정 대상
- **Notion 페이지** (W11/W12) — 콘텐츠 본체
- `course-site/data/curriculum-notion.json` — Notion 스냅샷 (자동 생성)
- `course-site/data/curriculum.json` — public JSON (자동 생성)
- `course-site/data/curriculum.js` — public JS (자동 생성)
- `course-site/data/notion-blocks/week11.json`, `week12.json` — Notion 블록 트리 (자동 생성)
- `course-site/assets/notion-images/week11/`, `week12/` — 이미지 캐시 (자동 생성)

### 검증 도구
- `tools/notion-sync.py` — Notion → repo 동기화
- `tools/content_pipeline.py` — 빌드/검증
- `/rpd-check week 11` 및 `/rpd-check week 12` — 콘텐츠 검증

---

## Phase 1 — W11 Notion 페이지 재구성

### Task 1: W11 현재 상태 캡처

**Files:**
- Read: Notion page `31354d6549718135a3c2d960d69a7fb3`
- Write: `claudedocs/research/w11-before-snapshot.json` (작업 시작 시점 스냅샷)

- [ ] **Step 1: Notion W11 페이지 전체 fetch**

ToolSearch로 `notion-fetch` 로드 후 호출:

```
mcp__ed9f2562-...__notion-fetch(
  urls=["https://www.notion.so/31354d6549718135a3c2d960d69a7fb3"]
)
```

- [ ] **Step 2: 응답 구조 확인**

확인 항목:
- title, subtitle 위치
- topics 리스트 블록
- 기존 4개 step 블록 (toggle/heading 패턴)
- shortcuts, mistakes, assignment, explore, videos, docs 블록
- Weight Paint step의 블록 ID (Task 8에서 archive 대상)

- [ ] **Step 3: 스냅샷 저장**

응답 JSON을 `claudedocs/research/w11-before-snapshot.json`에 저장. 롤백 시 참조용.

- [ ] **Step 4: 사용자 확인 게이트**

발견된 step 구조와 design doc의 6 step 매핑을 사용자에게 표시:

```
현재 W11 구조 (Notion):
  Step 1: "Armature 추가와 본 만들기" → 유지 (design Step 2로 흡수)
  Step 2: "메쉬와 연결 (Skinning)" → 유지 (design Step 3로 매핑)
  Step 3: "Pose Mode로 포즈 잡기" → 유지 (design Step 4로 매핑)
  Step 4: "Weight Paint 수정" → 제거 (W12로 이동)

신규 추가:
  Step 1 (앞에 삽입): "Armature 개념"
  Step 5: "AI 자동 리깅 도구 인지"
  Step 6: "AI 학습 보조 활용"

진행할까요? (Y/N)
```

승인 받기 전 다음 Task 진행 금지.

---

### Task 2: W11 title/subtitle/topics 업데이트

**Files:**
- Modify: Notion page `31354d6549718135a3c2d960d69a7fb3` (title/subtitle/topics)

- [ ] **Step 1: 변경 사항**

| 필드 | 변경 전 | 변경 후 |
|------|---------|---------|
| title | "Rigging 기초" | "Rigging 기초" (유지) |
| subtitle | "Armature · 본 구조 · 웨이트 페인팅 · 포즈" | "Armature 개념 · 수동 본 얹기 · AI 리깅 도구 소개" |
| topics | 6개 (기존) | 6개 (Weight Paint 제거, AI 도구 인지/AI 학습 보조 추가) |

신규 topics:
```
1. Armature 추가와 구조
2. Bone 편집 (Extrude/Subdivide)
3. Mesh Parenting (Automatic Weights)
4. Pose Mode로 포즈 잡기
5. AI 자동 리깅 도구 인지 (AccuRIG, Mixamo)
6. AI 학습 보조 활용 (멀티모달 챗)
```

- [ ] **Step 2: Notion MCP 호출**

```
mcp__ed9f2562-...__notion-update-page(
  data={
    "page_id": "31354d6549718135a3c2d960d69a7fb3",
    "command": "update_properties",
    "properties": {"title": "Rigging 기초"}
  }
)
```

subtitle/topics는 페이지 본문 블록이므로 별도 update_blocks 호출 필요. 정확한 블록 ID는 Task 1 Step 1에서 확보한 fetch 결과로 식별.

- [ ] **Step 3: 검증 fetch**

다시 페이지 fetch해서 변경 적용 확인. 변경 안 됐으면 Step 2 재시도.

- [ ] **Step 4: 사용자 확인**

변경된 title/subtitle/topics를 캡처해서 표시 후 OK 받기.

---

### Task 3: W11 Step 1 신규 추가 — "Armature 개념"

**Files:**
- Modify: Notion page `31354d6549718135a3c2d960d69a7fb3` (페이지 본문 블록 prepend)

- [ ] **Step 1: 블록 콘텐츠 작성**

design doc §3 Step 1 그대로 사용:

```markdown
## Step 1. Armature 개념

**copy**: 메쉬 안에 뼈대(Armature)를 넣어서 뼈를 움직이면 메쉬가 따라오게 만드는 거예요. 인형 안의 철사 골격과 같아요.

**goal**:
- Bone, Parent, Rest Pose 개념을 안다
- 메쉬와 Armature의 관계를 안다

**done**:
- Armature가 무엇이고 왜 필요한지 설명할 수 있다

**tasks**:
- Armature/Bone/Parent 슬라이드 보기
- 본 하나 = Head + Tail + Roll 구조 이해
```

- [ ] **Step 2: 기존 Step 1 위치 식별**

기존 "Armature 추가와 본 만들기" 블록의 위치 확보. 새 Step 1은 이 블록 바로 앞에 삽입.

- [ ] **Step 3: Notion 블록 삽입**

```
mcp__ed9f2562-...__notion-update-page(
  data={
    "command": "insert_content",
    "selection_with_ellipsis": "<현재 Step 1 첫 줄... ellipsis>",
    "new_str": "<신규 Step 1 markdown>",
    "position": "before"
  }
)
```

- [ ] **Step 4: 검증**

페이지 fetch 후 새 Step 1이 기존 Step 1 앞에 위치한 것 확인.

- [ ] **Step 5: 사용자 확인**

미리보기 캡처 표시 후 OK.

---

### Task 4: W11 Step 2 수정 — "수동 본 만들기"

**Files:**
- Modify: Notion page W11 기존 "Armature 추가와 본 만들기" 블록

- [ ] **Step 1: 변경 사항 표시 (edit 게이트)**

| 항목 | 변경 전 | 변경 후 |
|------|---------|---------|
| 제목 | "Armature 추가와 본 만들기" | "수동 본 만들기" |
| copy | "마리오네트 인형에 철사 뼈대를 넣는 것처럼..." | design doc §3 Step 2 copy |
| goal | 2개 항목 | 2개 항목 (이름 규칙 강조) |
| done | 1개 항목 | 2개 항목 (이름 규칙 포함) |
| tasks | 4개 (w11-t1~t4) | 4개 (Shift+A/E/Properties/Names 켜기) |

- [ ] **Step 2: 사용자 OK 게이트**

변경 사항 사용자에게 표시 후 진행 확인. NO면 중단.

- [ ] **Step 3: 블록 update**

각 필드별 `notion-update-page`로 blockwise edit. 정확한 호출은 Task 1 Step 1의 fetch 결과로 블록 ID 식별 후 결정.

- [ ] **Step 4: 검증 fetch + 사용자 확인**

---

### Task 5: W11 Step 3 수정 — "메쉬에 얹기 (Skinning)"

**Files:**
- Modify: Notion page W11 기존 "메쉬와 연결 (Skinning)" 블록

- [ ] **Step 1: 변경 사항**

| 항목 | 변경 전 | 변경 후 |
|------|---------|---------|
| 제목 | "메쉬와 연결 (Skinning)" | "메쉬에 얹기 (Skinning)" |
| copy | 현행 유지 (피부/뼈대 비유 OK) | design doc §3 Step 3 copy로 교체 (선택 순서 명확화) |
| goal | 2개 | 2개 (유지) |
| done | 1개 | 1개 |
| tasks | 3개 (w11-t5~t7) | 3개 (선택순서/Ctrl+P/Modifier 확인) |
| mistakes | 없음 | 3개 (선택 순서/In Front/Transform) |

- [ ] **Step 2-4: 게이트 → update → 검증** (Task 4와 동일 패턴)

---

### Task 6: W11 Step 4 수정 — "Pose Mode 동작 확인"

**Files:**
- Modify: Notion page W11 기존 "Pose Mode로 포즈 잡기" 블록

- [ ] **Step 1: 변경 사항**

| 항목 | 변경 전 | 변경 후 |
|------|---------|---------|
| 제목 | "Pose Mode로 포즈 잡기" | "Pose Mode 동작 확인" |
| copy | 피규어 관절 비유 (유지) | design doc §3 Step 4 copy |
| goal | 2개 | 2개 (전환/조작/리셋) |
| done | 2개 | 1개 (포즈 잡힘) |
| tasks | 3개 (w11-t8~t10) | 4개 (Ctrl+Tab/R/G/Alt+R) |
| shortcuts | Ctrl+Tab, R, Alt+R | Ctrl+Tab, R, G, Alt+R, Alt+G |

- [ ] **Step 2-4: 게이트 → update → 검증**

---

### Task 7: W11 Step 4 (구) Weight Paint 제거

**Files:**
- Modify: Notion page W11 기존 "Weight Paint 수정" 블록

- [ ] **Step 1: 사용자 확인 (destructive 게이트)**

```
W11 "Weight Paint 수정" step을 제거합니다 (내용은 W12로 이동).
처리 방식:
  A. 블록을 Notion archive (복구 가능)
  B. 블록을 별도 toggle "(이전 버전 보관)"로 이동
  C. 완전 삭제

추천: A (archive). 진행 방식 선택? (A/B/C)
```

OK 받기 전 다음 진행 금지.

- [ ] **Step 2: 선택 방식 적용**

A 선택 시:
```
mcp__ed9f2562-...__notion-update-page(
  data={
    "command": "archive"
    "block_id": "<weight paint step 블록 ID>"
  }
)
```

- [ ] **Step 3: 검증**

페이지에서 Weight Paint 블록 미노출 확인.

---

### Task 8: W11 Step 5 신규 추가 — "AI 자동 리깅 도구 인지"

**Files:**
- Modify: Notion page W11 (Step 4 뒤에 append)

- [ ] **Step 1: 블록 콘텐츠**

design doc §3 Step 5:

```markdown
## Step 5. AI 자동 리깅 도구 인지

**copy**: 수동 리깅만 있는 게 아니에요. 2026년에는 AccuRIG, Mixamo 같은 무료 AI 도구가 캐릭터를 1분 만에 리깅해줘요. 다음 주에 직접 써볼 거예요.

**goal**:
- AI 리깅 도구의 존재와 종류를 안다

**done**:
- AccuRIG, Mixamo가 뭔지 한 줄로 설명 가능

**tasks**:
- AccuRIG 90초 데모 영상 보기
- Mixamo 무료 라이브러리 미리보기

**참고 링크**:
- AccuRIG: https://actorcore.reallusion.com/auto-rig
- Mixamo: https://www.mixamo.com/
```

- [ ] **Step 2: append (Step 4 뒤)**

```
mcp__ed9f2562-...__notion-update-page(
  data={
    "command": "insert_content",
    "selection_with_ellipsis": "<Step 4 마지막 줄 ... ellipsis>",
    "new_str": "<신규 Step 5 markdown>",
    "position": "after"
  }
)
```

- [ ] **Step 3: 검증 + 사용자 확인**

---

### Task 9: W11 Step 6 신규 추가 — "AI 학습 보조 활용"

**Files:**
- Modify: Notion page W11 (Step 5 뒤에 append)

- [ ] **Step 1: 블록 콘텐츠**

design doc §3 Step 6:

```markdown
## Step 6. AI 학습 보조 활용

**copy**: 막혔을 때 스크린샷을 찍어서 ChatGPT나 Claude에게 보여주면 답을 알려줘요. "본을 회전시켰는데 메쉬가 안 움직여요" 같은 질문에 디버깅 도움을 받아요.

**goal**:
- 멀티모달 AI에 Blender 화면을 보내서 막힘을 푸는 방법을 안다

**done**:
- 본인이 겪은 문제 1개를 AI에게 질문해서 답을 받았다

**tasks**:
- 화면 캡처 (Shift+Cmd+4, Win+Shift+S)
- ChatGPT/Claude 웹에 이미지 + 질문 입력
- 답변 적용해보기
```

- [ ] **Step 2-3: append → 검증**

---

### Task 10: W11 shortcuts/mistakes/assignment/explore 업데이트

**Files:**
- Modify: Notion page W11 (관련 섹션 블록)

- [ ] **Step 1: shortcuts 검토**

기존 shortcuts 7개 유지 + 다음 항목 추가 검토:
- Ctrl+N (Roll 재계산, Edit Mode)
- Shift+D (본 복제, Edit Mode)

기존 shortcuts에서 제거할 항목:
- (Weight Paint 관련 단축키 없으면 변경 없음. 확인 필요)

- [ ] **Step 2: mistakes 업데이트**

신규 mistakes (Step 3 Skinning 섹션에서 가져옴):
- 선택 순서 오류 → Armature가 Active여야 함
- 본 안 보임 → In Front 체크
- Transform 미적용 → Ctrl+A → All Transforms

기존 mistakes 검토 후 Weight Paint 관련만 제거.

- [ ] **Step 3: assignment 업데이트**

신규 assignment:
```
title: "본인 학생 페이지에 업로드"
description: "W3-4 로봇/캐릭터에 본 체인을 얹고 포즈 2가지를 만들어요. AI에게 디버깅 질문 1번 시도."
checklist:
  - 뼈대 구조 스크린샷 1장 (Edit Mode)
  - 포즈 2가지 스크린샷
  - AI 디버깅 질문 + 답변 메모 1건
  - 리깅된 .blend 파일
```

- [ ] **Step 4: explore 업데이트**

신규 explore:
```
1. 본인 캐릭터에 손가락 본 추가
2. Bone Constraint(IK) 한 번 추가해보기
3. 대칭 리깅 (.L/.R 이름 + Symmetrize)
4. AI에게 본 이름 규칙 추천받기
```

- [ ] **Step 5: 사용자 게이트 → update → 검증**

---

## Phase 2 — W12 Notion 페이지 재구성

### Task 11: W12 현재 상태 캡처

**Files:**
- Read: Notion page `31354d6549718174bb74c528a6913fc0`
- Write: `claudedocs/research/w12-before-snapshot.json`

- [ ] **Step 1-4: Task 1과 동일 패턴**

현재 W12 4개 step:
1. 익스포트 준비
2. Mixamo 자동 리깅
3. 애니메이션 선택 및 임포트
4. NLA Editor로 애니메이션 관리

매핑:
- (1)/(2) → design Step 2 "AccuRIG 자동 리깅"으로 통합 (또는 별도 Mixamo Step 3)
- (3) → design Step 3 "Mixamo 애니메이션 적용"
- (4) → design Step 6 "NLA 시퀀스"

신규:
- Step 1 (앞): "2026 AI 리깅 도구 카탈로그"
- Step 2 (대체): "AccuRIG 자동 리깅"
- Step 4 (삽입): "Weight Paint 개념"
- Step 5 (삽입): "Weight Paint 부분 보정"

---

### Task 12: W12 title/subtitle/topics 업데이트

**Files:**
- Modify: Notion W12 title/subtitle/topics

- [ ] **Step 1: 변경 사항**

| 필드 | 변경 전 | 변경 후 |
|------|---------|---------|
| title | "AI 활용 리깅 (Mixamo)" | "AI 리깅과 애니메이션 시퀀스" |
| subtitle | "Mixamo 자동 리깅 · FBX 워크플로우 · NLA" | "AI 리깅 카탈로그 · AccuRIG/Mixamo · Weight Paint 보정 · NLA" |

신규 topics 6개:
```
1. 2026 AI 리깅 도구 카탈로그 (무료 5/유료 5)
2. AccuRIG 자동 리깅 워크플로우
3. Mixamo 애니메이션 라이브러리 적용
4. Weight Paint 개념과 색 의미
5. AI 결과 부분 보정 (Front Faces Only)
6. NLA Editor로 클립 시퀀스 만들기
```

- [ ] **Step 2-4: 게이트 → update → 검증**

---

### Task 13: W12 Step 1 신규 추가 — "2026 AI 리깅 도구 카탈로그"

**Files:**
- Modify: Notion W12 (페이지 본문 prepend)

- [ ] **Step 1: 블록 콘텐츠**

design doc §6 카탈로그 (무료 표/유료 표/선택 가이드) 전체를 Step 1 본문으로 삽입. 단축 버전:

```markdown
## Step 1. 2026 AI 리깅 도구 카탈로그

**copy**: AI 리깅 도구는 무료부터 유료까지 다양해요. 무료 도구로 시작해서 필요할 때 유료를 검토하세요. 인체형이면 AccuRIG, 무료 애니메이션이 필요하면 Mixamo가 기본이에요.

**goal**:
- 무료/유료 AI 리깅 도구를 분류한다
- 상황별 도구 선택 기준을 안다

**done**:
- 본인 프로젝트에 어떤 도구를 쓸지 정할 수 있다

### 무료 도구 (5종)

| 도구 | 장점 | 단점 |
|------|------|------|
| Reallusion AccuRIG 2.0 | 1분 자동 리깅, 인체형+사족 | Reallusion 계정 필요 |
| Mixamo (Adobe) | 2500+ 애니메이션, 무한 무료 | 2021 이후 정체, T-pose 강제 |
| Blender Rigify | 내장, 메타리그 커스터마이즈 | AI 아님, 메타리그 수동 배치 |
| BlenRig 6 | 오픈소스, 50%+ 자동화 | 학습곡선 가파름 |
| Cascadeur Free | AutoPosing AI 포즈 보조 | 리깅 아닌 애니메이션 보조 |

### 유료 도구 (5종)

| 도구 | 가격 | 장점 |
|------|------|------|
| Auto-Rig Pro | $40 일회성 | Blender 내부, 프로 표준 |
| Meshy | Free 100크/월, Pro 1000 | 텍스트→3D + 자동 리깅 |
| Hyper3D Rodin | Free $1.5/크, Education $15/월 | 고품질 3D 생성 |
| Everything Universe | B2B 비공개 | 비인체형(동물·사물) |
| Reallusion iClone 8 | $599 일회성 | 풀 캐릭터 파이프라인 |

### 선택 가이드

| 상황 | 추천 |
|------|------|
| 인체형 처음 시도 | AccuRIG 2.0 |
| 무료 애니메이션 풍부히 | Mixamo |
| Blender 안에서만 | Rigify 또는 BlenRig |
| 동물·로봇·식물 | 수동 + Rigify 메타리그 |
| AI로 모델까지 생성 | Meshy (Free 100크) |
| 졸업 후 실무 | Auto-Rig Pro $40 |

**tasks**:
- 무료 5종 비교표 학습
- 유료 5종 인지 (가격 + 핵심 장점)
- 본인 프로젝트에 맞는 도구 1개 선택
```

- [ ] **Step 2-3: prepend → 검증 + 사용자 확인**

---

### Task 14: W12 Step 2 — "AccuRIG 자동 리깅" (기존 Mixamo 자동 리깅 step 대체)

**Files:**
- Modify: Notion W12 기존 "Mixamo 자동 리깅" 블록 (제목/copy/tasks 모두 변경)

- [ ] **Step 1: 변경 사항**

| 항목 | 변경 전 (Mixamo) | 변경 후 (AccuRIG) |
|------|---------|---------|
| 제목 | "Mixamo 자동 리깅" | "AccuRIG 자동 리깅" |
| copy | "AI가 메쉬를 분석해서..." | design doc §4 Step 2 copy |
| goal | "Mixamo 자동 리깅 워크플로우를 안다" | "AccuRIG로 캐릭터를 자동 리깅한다" |
| done | Mixamo 미리보기 확인 | AccuRIG 결과 Blender 임포트 |
| tasks | Mixamo 업로드/마커/미리보기 | FBX export/AccuRIG 업로드/마커/Auto Rig/Blender Import |
| mistakes | (기존 W12 mistakes 분산) | 업로드 실패→메쉬 단일화/법선, 스케일→Ctrl+A |

- [ ] **Step 2: 사용자 OK 게이트 (edit destructive)**

기존 "Mixamo 자동 리깅" step을 통째로 "AccuRIG 자동 리깅"으로 치환하는 큰 변경. 사용자 확인 필수.

대안 옵션 제시:
```
A. AccuRIG 자동 리깅으로 치환 (Mixamo는 Step 3 "Mixamo 애니메이션 적용"으로 분리)
B. AccuRIG step을 별도 새 step으로 추가, Mixamo 자동 리깅 유지

추천: A (design doc 흐름과 일치).
```

- [ ] **Step 3-4: update → 검증**

---

### Task 15: W12 Step 3 — "Mixamo 애니메이션 적용" (기존 step 활용)

**Files:**
- Modify: Notion W12 기존 "애니메이션 선택 및 임포트" 블록

- [ ] **Step 1: 변경 사항**

| 항목 | 변경 전 | 변경 후 |
|------|---------|---------|
| 제목 | "애니메이션 선택 및 임포트" | "Mixamo 애니메이션 적용" |
| copy | "Mixamo에서 걷기, 달리기..." | design doc §4 Step 3 copy (간소화) |
| goal | "Mixamo 애니메이션을 Blender에서 재생" | (유지) |
| done | "캐릭터가 걷거나 뛰는 애니메이션 재생" | (유지) |
| tasks | 4개 (w12-t7~t10) | 5개 (업로드/선택/다운로드/임포트/재생) |
| mistakes | (기존) | 회전→Manual Orientation, 슬로우모션→24fps |

- [ ] **Step 2-4: 게이트 → update → 검증**

---

### Task 16: W12 Step 4 신규 추가 — "Weight Paint 개념"

**Files:**
- Modify: Notion W12 (Step 3 뒤에 insert)

- [ ] **Step 1: 블록 콘텐츠**

design doc §4 Step 4 그대로:

```markdown
## Step 4. Weight Paint 개념

**copy**: AI가 만든 결과가 완벽하지 않을 때가 있어요. 팔을 올렸는데 몸통이 같이 늘어난다면 Weight Paint로 영향 범위를 수정해요. 빨강은 강한 영향, 파랑은 영향 없음이에요.

**goal**:
- Vertex Group과 Weight 의미를 안다
- 빨강/파랑 색 코드를 안다

**done**:
- AI 리깅 결과에서 어색한 부위 1군데를 찾았다

**tasks**:
- Ctrl+Tab → Weight Paint Mode
- Properties → Vertex Groups에서 본별 그룹 확인
- Pose Mode로 가서 팔/다리 돌려보며 어색한 곳 체크
```

- [ ] **Step 2-3: insert → 검증**

---

### Task 17: W12 Step 5 신규 추가 — "Weight Paint 부분 보정"

**Files:**
- Modify: Notion W12 (Step 4 뒤에 insert)

- [ ] **Step 1: 블록 콘텐츠**

design doc §4 Step 5 그대로 (단축키, mistakes 포함).

```markdown
## Step 5. Weight Paint 부분 보정

**copy**: 문제 있는 부위 본의 Vertex Group을 선택하고 브러시로 칠해요. 빼고 싶으면 Ctrl+클릭으로 Subtract, 부드럽게 섞고 싶으면 Shift+클릭으로 Blur를 써요. Front Faces Only를 켜야 반대쪽이 같이 칠해지지 않아요.

**goal**:
- 특정 부위의 Weight를 수동 조정한다

**done**:
- 어색하던 부위가 자연스럽게 움직인다

**tasks**:
- Ctrl+Shift+클릭으로 본 선택 (Blender 4.0+ 단축키)
- Front Faces Only 켜기
- 브러시 Weight·Radius·Strength 조절
- 칠하기 → Pose Mode 확인 반복

**mistakes**:
- 반대쪽 같이 칠해짐 → Front Faces Only 체크
- Auto Normalize 끔 → 합 1 보장 안 됨
- Lock 무시됨 → Normalize All 사용 시 주의
```

- [ ] **Step 2-3: insert → 검증**

---

### Task 18: W12 Step 6 — "NLA 시퀀스" (기존 step 강화)

**Files:**
- Modify: Notion W12 기존 "NLA Editor로 애니메이션 관리" 블록

- [ ] **Step 1: 변경 사항**

| 항목 | 변경 전 | 변경 후 |
|------|---------|---------|
| 제목 | "NLA Editor로 애니메이션 관리" | "NLA 시퀀스" |
| copy | "NLA Editor는 애니메이션 클립을..." | design doc §4 Step 6 copy (영상편집 타임라인 비유 강화) |
| goal | "NLA Editor의 기본 개념 이해" | "NLA 개념을 안다 / 2개 이상 Action을 스트립으로 이어붙인다" |
| done | "2개 이상 애니메이션 클립 확인" | "걷기 → 정지 → 인사 시퀀스 재생" |
| tasks | 2개 | 5개 (Editor 전환/Push Down/이동/추가/재생) |
| shortcuts | (기존) | Push Down/G/S 명시 |

- [ ] **Step 2: NLA 정의 강조 (FAQ-style 블록)**

페이지에 다음 callout 추가:

```
> **NLA란?** Non-Linear Animation. 영상 편집 타임라인과 같은 개념. 키프레임 묶음 하나 = "Action", Action을 스트립으로 만들어 시간순으로 이어붙여 긴 시퀀스 완성.
```

- [ ] **Step 3-4: 게이트 → update → 검증**

---

### Task 19: W12 기존 "익스포트 준비" Step 처리

**Files:**
- Modify: Notion W12 기존 "익스포트 준비" 블록

- [ ] **Step 1: 처리 방식 결정**

기존 W12 Step 1 "익스포트 준비"는 Mixamo 워크플로우 전용. 새 구조에서:
- AccuRIG에도 동일하게 FBX export 필요 → Step 2 "AccuRIG 자동 리깅" tasks에 흡수
- 별도 step으로 유지하기엔 짧음

옵션:
```
A. archive (Step 2 tasks에 흡수)
B. Step 2 "AccuRIG 자동 리깅"의 prep 섹션으로 흡수
C. 별도 step 유지

추천: B (워크플로우 자연스러움)
```

- [ ] **Step 2-3: 사용자 결정 → 적용 → 검증**

---

### Task 20: W12 shortcuts/mistakes/assignment/explore 업데이트

**Files:**
- Modify: Notion W12 관련 섹션 블록

- [ ] **Step 1: shortcuts 업데이트**

추가:
- Ctrl+Shift+LMB (Weight Paint 본 선택, 4.0+)
- F / Shift+F (브러시 Radius/Strength)
- Ctrl+LMB (Subtract)
- Shift+LMB (Blur)

기존 유지: Ctrl+J, Ctrl+A, Merge by Distance, Space, Shift+N

- [ ] **Step 2: mistakes 통합**

기존 5개 + Weight Paint 관련 3개 (Task 17 mistakes에서 가져옴).

- [ ] **Step 3: assignment 업데이트**

신규:
```
title: "본인 학생 페이지에 업로드"
description: "AccuRIG 또는 Mixamo로 리깅된 캐릭터에 Weight Paint 1군데 보정 + 2개 애니메이션 클립 NLA로 연결."
checklist:
  - AI 리깅 과정 스크린샷 (AccuRIG 마커 또는 Mixamo)
  - Weight Paint 보정 전/후 비교
  - 2개 클립 NLA 시퀀스 재생 영상 또는 GIF
  - .blend 파일
```

- [ ] **Step 4: explore 업데이트**

신규:
```
1. 본인 캐릭터에 AccuRIG + Mixamo 풀 워크플로우
2. Meshy 무료 100 크레딧으로 모델→리깅 체험
3. AI 리깅 결과 vs W11 수동 리깅 비교 메모
4. Anything World로 비인체형(동물) 리깅 도전
```

- [ ] **Step 5: 게이트 → update → 검증**

---

## Phase 3 — 동기화 및 검증

### Task 21: Notion → canonical 동기화

**Files:**
- Modify: `course-site/data/curriculum-notion.json` (자동 생성)
- Modify: `course-site/data/notion-blocks/week11.json`, `week12.json` (자동 생성)
- Modify: `course-site/assets/notion-images/week11/`, `week12/` (자동 생성)

- [ ] **Step 1: Notion snapshot fetch**

```bash
cd /Users/ssongji/Developer/Workspace/RPD/.claude/worktrees/admiring-hermann-4c6e3c
python3 tools/notion-sync.py --weeks 11
python3 tools/notion-sync.py --weeks 12
```

Expected exit code: 0 (changes detected) 또는 2 (no changes).

- [ ] **Step 2: 결과 확인**

```bash
git diff course-site/data/curriculum-notion.json
git diff course-site/data/notion-blocks/week11.json
git diff course-site/data/notion-blocks/week12.json
```

W11 4 steps → 6 steps, W12 4 steps → 6 steps로 변경되었는지 확인.

- [ ] **Step 3: canonical 반영**

```bash
python3 tools/notion-sync.py --apply --weeks 11
python3 tools/notion-sync.py --apply --weeks 12
```

- [ ] **Step 4: commit (스냅샷)**

```bash
git add course-site/data/curriculum-notion.json course-site/data/notion-blocks/ course-site/assets/notion-images/
git commit -m "sync(week11-12): Notion → canonical for rigging restructure"
```

---

### Task 22: Public 빌드

**Files:**
- Modify: `course-site/data/curriculum.json`, `curriculum.js` (자동 생성)

- [ ] **Step 1: content_pipeline build 실행**

```bash
python3 tools/content_pipeline.py build
```

Expected: success, curriculum.json/js 재생성.

- [ ] **Step 2: 빌드 결과 확인**

```bash
git diff course-site/data/curriculum.json | head -200
```

W11/W12 step 수와 내용이 Notion 변경과 일치하는지 확인.

- [ ] **Step 3: commit**

```bash
git add course-site/data/curriculum.json course-site/data/curriculum.js
git commit -m "build(week11-12): regenerate public curriculum"
```

---

### Task 23: 자동 검증 (/rpd-check)

**Files:**
- Read only

- [ ] **Step 1: W11 검증**

```
/rpd-check week 11
```

체크 항목:
- 6개 step 모두 있음
- 톤(~해요/~이에요) 일관
- 단축키 정확
- 이미지 경로 유효
- 이모지 없음
- 외부 링크 click 가능

- [ ] **Step 2: W12 검증**

```
/rpd-check week 12
```

동일 체크 항목.

- [ ] **Step 3: 발견된 이슈 수정**

이슈가 있으면 Notion으로 돌아가서 수정 후 Task 21-22 재실행.

이슈 없으면 Task 24로.

---

### Task 24: 브라우저 시각 확인

**Files:**
- Read only (dev 서버)

- [ ] **Step 1: 로컬 서버 기동**

```bash
cd /Users/ssongji/Developer/Workspace/RPD/.claude/worktrees/admiring-hermann-4c6e3c/course-site
python3 -m http.server 8000
```

- [ ] **Step 2: W11 페이지 시각 확인**

preview MCP 또는 브라우저로:
- `http://localhost:8000/week.html?w=11`
- 6개 step 토글, 단축키, mistakes, assignment, explore, 영상, 문서 모두 정상 렌더링
- AI 도구 링크(AccuRIG, Mixamo) 클릭 가능

- [ ] **Step 3: W12 페이지 시각 확인**

- `http://localhost:8000/week.html?w=12`
- 6개 step, AI 도구 카탈로그 표가 깨지지 않고 렌더링
- Weight Paint step 단축키 표 정상
- NLA 설명 callout 표시

- [ ] **Step 4: 스크린샷 캡처**

W11/W12 페이지 스크린샷을 `claudedocs/research/`에 저장하여 작업 완료 증빙.

- [ ] **Step 5: 사용자 최종 확인**

스크린샷 + 페이지 URL 사용자에게 표시. OK 받기.

---

### Task 25: 최종 commit + PR 준비 (선택)

**Files:**
- 변경된 모든 파일

- [ ] **Step 1: 최종 git status**

```bash
git status
git log --oneline -10
```

- [ ] **Step 2: 미커밋 변경 정리**

남은 변경이 있으면 의미 단위 commit:
```bash
git add <files>
git commit -m "<message>"
```

- [ ] **Step 3: 사용자에게 PR 생성 여부 확인**

```
W11/W12 재구성 완료. PR 생성할까요?
- Title: "feat(week11-12): rigging restructure with AI integration"
- Base: main
- Branch: claude/admiring-hermann-4c6e3c
```

OK이면 `gh pr create`, NO면 종료.

---

## Self-Review

### Spec coverage

design doc(2026-05-18-week11-12-rigging-restructure-design.md) 섹션별 매핑:

- §3 W11 6 steps → Task 3-9 (각 step별 task)
- §4 W12 6 steps → Task 13-18
- §5 흐름 검증 → Task 23-24 (`/rpd-check` + 시각)
- §6 AI 도구 카탈로그 → Task 13 Step 1 (블록 콘텐츠에 포함)
- §7 수정 위치 → Phase 3 전체 (Notion → canonical → public)
- §8 검증 체크리스트 → Task 23

미커버 항목: 없음

### Placeholder scan

- "TBD/TODO" 검색: 없음
- "implement later" 등 미완성 표현: 없음
- 추상 지시("적절히 수정"): 없음. 모든 변경 사항은 design doc 인용으로 명시
- 단, Notion 블록 ID는 Task 1/11에서 동적으로 확보 (사전에 알 수 없음) → "Task 1 Step 1 fetch 결과 참조" 패턴으로 명시

### Type consistency

- Notion MCP 도구 이름은 모두 `mcp__ed9f2562-...-notion-update-page` 형식 (일관)
- 파일 경로는 절대경로 또는 워크트리 기준 상대경로 일관
- step 번호는 design doc과 1:1 매칭 (Task 3-9 = W11 Step 1-6)

### 위험 요소

1. **Notion API 호출 실패 시**: 각 Task의 검증 step에서 fetch로 적용 여부 재확인 → 실패 시 재시도
2. **사용자 게이트 다수**: edit/destructive 동작이 많아 사용자 OK 요청 잦음 (10회+). 효율 위해 Phase 1/Phase 2 끝나면 일괄 묶음 확인 방식도 가능
3. **notion-sync.py 실패**: NOTION_TOKEN 환경 변수 확인 필요. 실패 시 stderr 메시지로 진단
4. **content_pipeline build 검증 실패**: 스키마(weeks/contracts.schema.json) 위반 시 빌드 거부. design doc 구조가 스키마와 맞는지 사전 확인 (Task 1.5 추가 고려)

---

## 실행 방식 선택

**1. Subagent-Driven (권장)** — Phase별 서브에이전트 디스패치 (W11 / W12 / Sync). 각 Phase 끝에 사용자 검토.

**2. Inline 실행** — 이 세션에서 executing-plans 스킬로 직접 실행. 체크포인트 = 각 Task의 사용자 게이트.

**3. Paperclip 위임** — /paperclip-issue로 이슈 생성 후 비동기 위임.

Which approach?
