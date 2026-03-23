# Week 4 카드 품질 업그레이드 + W4-W5 혼합 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Week 4 Show Me 카드 19개의 보충 콘텐츠를 채우고, 핵심 3개 카드 HTML을 보강하며, W5의 AI 파츠+Decimate를 W4 커리큘럼에 추가한다.

**Architecture:** `_supplements.json`에 18개 엔트리 추가(Phase 1) → `boolean-modifier.html`, `bevel-modifier.html`, `weighted-normal.html` HTML 보강(Phase 2) → `curriculum.json` W4에 AI 파츠 스텝 삽입(Phase 3). 각 보충 콘텐츠는 analogy/before_after/confusion/takeaway 구조.

**Tech Stack:** JSON (supplements, curriculum), HTML/CSS (카드)

**Design Doc:** `docs/plans/2026-03-23-w4-quality-and-w4w5-mixing-design.md`
**Detailed Card Content:** `docs/plans/2026-03-23-week4-card-quality-upgrade.md` (Phase 1-2 콘텐츠 원본)

---

## Phase 1: 보충 콘텐츠 (_supplements.json)

### Task 1: 핵심 카드 4개 보충 콘텐츠 추가

**Files:**
- Modify: `course-site/assets/showme/_supplements.json`

**Step 1: 현재 상태 확인**

Run: `python3 -c "import json; d=json.load(open('course-site/assets/showme/_supplements.json')); print(f'Current: {len(d)} entries'); print('Has boolean:', 'boolean-modifier' in d)"`
Expected: `Current: 15 entries`, `Has boolean: False`

**Step 2: boolean-modifier, bevel-modifier, weighted-normal, join-separate 4개 엔트리 추가**

`_supplements.json`의 마지막 `}` 앞에 4개 엔트리 추가. 콘텐츠는 `docs/plans/2026-03-23-week4-card-quality-upgrade.md`의 Task 1 Step 2-5에 있는 JSON을 그대로 사용.

각 엔트리 구조:
- `title`: 문제 상황 제목
- `analogy`: emoji + headline + body
- `before_after`: before + after
- `confusion`: [{symptom, reason, fix}, ...]
- `takeaway`: 한 줄 정리
- `targets`: [카드 id]

**Step 3: JSON 유효성 검증**

Run: `python3 -c "import json; json.load(open('course-site/assets/showme/_supplements.json')); print('OK')"`
Expected: `OK`

**Step 4: Commit**

```bash
git add course-site/assets/showme/_supplements.json
git commit -m "content: add supplements for 4 core Week 4 cards (boolean, bevel, weighted-normal, join-separate)"
```

---

### Task 2: 보조 카드 14개 보충 콘텐츠 추가

**Files:**
- Modify: `course-site/assets/showme/_supplements.json`

**Step 1: 14개 엔트리 추가**

콘텐츠는 `docs/plans/2026-03-23-week4-card-quality-upgrade.md`의 Task 2 Step 1-4에 있는 JSON을 그대로 사용.

추가 대상 (14개):
1. edge-split-modifier
2. triangulate-modifier
3. weld-modifier
4. build-modifier
5. decimate-modifier
6. remesh-modifier
7. screw-modifier
8. skin-modifier
9. wireframe-modifier
10. mask-modifier
11. multiresolution-modifier
12. volume-to-mesh
13. curve-to-tube
14. scatter-on-surface

**Step 2: JSON 유효성 + 카운트 검증**

Run: `python3 -c "import json; d=json.load(open('course-site/assets/showme/_supplements.json')); print(f'Total: {len(d)} entries'); print('OK')"`
Expected: `Total: 33 entries` (15 기존 + 4 핵심 + 14 보조), `OK`

**Step 3: Commit**

```bash
git add course-site/assets/showme/_supplements.json
git commit -m "content: add supplements for 14 auxiliary Week 4 cards"
```

---

## Phase 2: 핵심 카드 HTML 보강

### Task 3: boolean-modifier.html — 원인→결과 + 흔한 실수

**Files:**
- Modify: `course-site/assets/showme/boolean-modifier.html`
- Reference: `course-site/assets/showme/transform-apply.html` (cause-effect CSS 패턴)

**Step 1: transform-apply.html에서 cause-effect CSS 패턴 확인**

Read `transform-apply.html`에서 `.cause-effect`, `.ce-row`, `.ce-cause`, `.ce-result`, `.ce-arrow`, `.ce-label`, `.result-warn`, `.result-success`, `.section-divider` CSS를 찾아 복사 준비.

**Step 2: boolean-modifier.html Usage 탭에 원인→결과 섹션 삽입**

Usage 탭(panel-when) 내부, `<div class="combo-section">` 앞에 삽입. 콘텐츠는 기존 plan의 Task 3 Step 1 HTML을 사용.

4개 행:
- Scale 미적용 → 비대칭 구멍 (warn)
- 커터 삭제 → Boolean 무효화 (warn)
- Overlap Threshold 미조정 → Z-fighting (warn)
- Apply Scale + Exact Solver → 깨끗한 결과 (success)

**Step 3: combo-section을 "흔한 실수 & 해결법"으로 교체**

기존 combo-section 내용을 기존 plan Task 3 Step 2의 HTML로 교체. 4개 카드.

**Step 4: cause-effect CSS가 없으면 추가**

boolean-modifier.html의 `<style>` 블록에 cause-effect 관련 CSS가 없으면 transform-apply.html에서 복사.

**Step 5: Commit**

```bash
git add course-site/assets/showme/boolean-modifier.html
git commit -m "content(boolean): add cause-effect section and common mistakes to usage tab"
```

---

### Task 4: bevel-modifier.html — 원인→결과 + 흔한 실수 + 쓰지 말 것

**Files:**
- Modify: `course-site/assets/showme/bevel-modifier.html`

**Step 1: Usage 탭에 원인→결과 섹션 삽입**

combo-section 앞에 삽입. 기존 plan Task 4 Step 1의 HTML 사용. 4개 행.

**Step 2: combo-section을 "흔한 실수 & 해결법"으로 교체**

기존 plan Task 4 Step 2의 HTML 사용. 4개 카드.

**Step 3: "쓰지 말 것" 항목 2개 추가**

Usage 탭의 "사용하지 말아야 할 때" 리스트에 추가:
- "유기체 모델링에는 Subdivision Surface가 더 적합"
- "모서리 하나만 깎을 때는 Bevel Tool(Ctrl+B)이 더 빠름"

**Step 4: cause-effect CSS 확인 및 추가** (Task 3과 동일 패턴)

**Step 5: Commit**

```bash
git add course-site/assets/showme/bevel-modifier.html
git commit -m "content(bevel): add cause-effect, common mistakes, expand usage-not items"
```

---

### Task 5: weighted-normal.html — 개념 보강 + 원인→결과 + 흔한 실수

**Files:**
- Modify: `course-site/assets/showme/weighted-normal.html`

**Step 1: 개념 탭에 3번째 개념 카드 추가**

기존 2개 concept-card 뒤에 "Auto Smooth와의 관계" 카드 추가. 기존 plan Task 5 Step 1의 HTML 사용.

**Step 2: 단축키 섹션 수정**

Ctrl+1~5 항목 제거 → 정확한 접근 경로로 교체. 기존 plan Task 5 Step 2의 HTML 사용.

**Step 3: Usage 탭에 원인→결과 섹션 삽입**

기존 plan Task 5 Step 3의 HTML 사용. 4개 행.

**Step 4: 흔한 실수 & 해결법 섹션 추가**

기존 plan Task 5 Step 4의 HTML 사용. 4개 카드.

**Step 5: cause-effect CSS 확인 및 추가**

**Step 6: Commit**

```bash
git add course-site/assets/showme/weighted-normal.html
git commit -m "content(weighted-normal): add concept card, fix shortcuts, add cause-effect and common mistakes"
```

---

## Phase 3: 커리큘럼 변경

### Task 6: curriculum.json W4에 "AI 파츠 생성 & 메시 정리" 스텝 삽입

**Files:**
- Modify: `course-site/data/curriculum.json`

**Step 1: 현재 W4 스텝 구조 확인**

Run: `python3 -c "import json; w4=[w for w in json.load(open('course-site/data/curriculum.json')) if w['week']==4][0]; print(f'Steps: {len(w4[\"steps\"])}'); [print(f'  {i+1}. {s[\"title\"]}') for i,s in enumerate(w4['steps'])]"`
Expected: 5 steps, 마지막이 "Apply 시점과 최종 점검"

**Step 2: W4 topics에 AI 관련 토픽 추가**

`topics` 배열 끝에 추가:
- `"AI 파츠 생성 (Meshy/Tripo)"`
- `"Decimate로 AI 메쉬 정리"`

**Step 3: W4 steps 배열에서 기존 step 5(Apply 시점) 앞에 새 스텝 삽입**

새 스텝 (index 4에 삽입, 기존 step 5가 index 5로 밀림):

```json
{
  "title": "AI 파츠 생성 & 메쉬 정리",
  "copy": "자기 모델에 독특한 파츠를 더하고 싶다면 AI 3D 생성 도구를 써보세요. AI가 만든 메쉬는 폴리곤이 많아서 Decimate로 가볍게 정리한 뒤, Boolean으로 합치면 돼요.",
  "goal": [
    "AI 3D 생성 워크플로우를 이해한다",
    "Decimate로 메쉬를 정리한다"
  ],
  "done": [
    "AI 생성 메쉬를 Blender에서 Import했다",
    "Decimate로 폴리곤 수를 절반 이하로 줄였다"
  ],
  "tasks": [
    {
      "id": "w4-ai1",
      "label": "Meshy 또는 Tripo에서 파츠 생성",
      "detail": "안테나, 장식, 소품 등 로봇에 붙일 파츠를 AI로 생성해요"
    },
    {
      "id": "w4-ai2",
      "label": ".glb 파일 Blender에서 Import",
      "detail": "File → Import → glTF (.glb/.gltf)"
    },
    {
      "id": "w4-ai3",
      "label": "Viewport Overlay Statistics로 폴리곤 수 확인",
      "detail": "AI 메쉬는 보통 수만~수십만 폴리곤"
    },
    {
      "id": "w4-ai4",
      "label": "Decimate Modifier로 메쉬 경량화",
      "detail": "Ratio 0.3~0.5에서 형태 유지되는 지점 찾기"
    },
    {
      "id": "w4-ai5",
      "label": "Ctrl+A로 Scale 정리 후 Boolean으로 합치기",
      "detail": "Import 메쉬 크기 맞추고 모델에 결합"
    }
  ],
  "image": "assets/images/week05/ai-3d-generation.png",
  "showme": "decimate-modifier"
}
```

**Step 4: 밀린 기존 step 5의 task id 충돌 확인**

기존 step 5의 task id가 `w4-t14`, `w4-t15`, `w4-t16`이므로 새 스텝의 `w4-ai*`와 충돌 없음. 확인만.

**Step 5: JSON 유효성 검증**

Run: `python3 -c "import json; c=json.load(open('course-site/data/curriculum.json')); w4=[w for w in c if w['week']==4][0]; print(f'W4 steps: {len(w4[\"steps\"])}'); [print(f'  {i+1}. {s[\"title\"]}') for i,s in enumerate(w4['steps'])]; print('OK')"`
Expected: 6 steps, 5번째가 "AI 파츠 생성 & 메쉬 정리", `OK`

**Step 6: Commit**

```bash
git add course-site/data/curriculum.json
git commit -m "curriculum: add AI parts + Decimate step to Week 4 (from W5 mixing)"
```

---

### Task 7: W5 AI 스텝 심화 표현으로 업데이트

**Files:**
- Modify: `course-site/data/curriculum.json`

**Step 1: W5 step 1(AI 3D 생성 체험) copy 텍스트 업데이트**

W4에서 기본을 배웠으므로, W5에서는 심화 뉘앙스로 변경:

기존 copy: `"텍스트 몇 글자 입력하면 3D 메쉬가 뚝딱 나와요..."`
변경 copy: `"W4에서 AI 생성 기본을 체험했다면, 이번에는 프롬프트를 정교하게 다듬고 여러 결과를 비교하는 법을 배워요. 같은 주제라도 문장에 따라 결과가 크게 달라져요."`

**Step 2: W5 step 2(AI 메쉬 정리) copy 텍스트 업데이트**

기존 copy: `"AI가 만든 메쉬는 대부분 폴리곤이 지나치게 많아요..."`
변경 copy: `"W4에서 Decimate 기본을 배웠다면, 이번에는 Planar 모드, Vertex Group 마스킹 등 고급 기법으로 AI 메쉬를 더 정교하게 정리해요."`

**Step 3: JSON 유효성 검증**

Run: `python3 -c "import json; json.load(open('course-site/data/curriculum.json')); print('OK')"`
Expected: `OK`

**Step 4: Commit**

```bash
git add course-site/data/curriculum.json
git commit -m "curriculum: update W5 AI steps to advanced framing (post W4 mixing)"
```

---

## Phase 4: 전체 검증

### Task 8: 전체 검증

**Files:**
- Verify: `course-site/assets/showme/_supplements.json`
- Verify: `course-site/assets/showme/boolean-modifier.html`
- Verify: `course-site/assets/showme/bevel-modifier.html`
- Verify: `course-site/assets/showme/weighted-normal.html`
- Verify: `course-site/data/curriculum.json`

**Step 1: supplements.json 최종 검증**

Run: `python3 -c "import json; d=json.load(open('course-site/assets/showme/_supplements.json')); week4_ids=['boolean-modifier','bevel-modifier','weighted-normal','join-separate','edge-split-modifier','triangulate-modifier','weld-modifier','build-modifier','decimate-modifier','remesh-modifier','screw-modifier','skin-modifier','wireframe-modifier','mask-modifier','multiresolution-modifier','volume-to-mesh','curve-to-tube','scatter-on-surface']; found=[k for k in week4_ids if k in d]; missing=[k for k in week4_ids if k not in d]; print(f'Found: {len(found)}/18'); print(f'Missing: {missing}'); print(f'Total entries: {len(d)}')"`
Expected: `Found: 18/18`, `Missing: []`, `Total entries: 33`

**Step 2: HTML 구문 검증**

Run: `for f in boolean-modifier bevel-modifier weighted-normal; do python3 -c "from html.parser import HTMLParser; p=HTMLParser(); p.feed(open('course-site/assets/showme/$f.html').read()); print('$f: OK')"; done`
Expected: 3개 모두 `OK`

**Step 3: curriculum.json 구조 검증**

Run: `python3 -c "import json; c=json.load(open('course-site/data/curriculum.json')); w4=[w for w in c if w['week']==4][0]; w5=[w for w in c if w['week']==5][0]; print(f'W4: {len(w4[\"steps\"])} steps, topics: {len(w4[\"topics\"])}'); print(f'W5: {len(w5[\"steps\"])} steps'); assert len(w4['steps'])==6, 'W4 should have 6 steps'; assert w4['steps'][4]['title']=='AI 파츠 생성 & 메쉬 정리', 'Step 5 title mismatch'; print('All checks passed')"`
Expected: `W4: 6 steps`, `W5: 5 steps`, `All checks passed`

**Step 4: 최종 Commit (필요 시)**

```bash
git add -A
git commit -m "content: Week 4 card quality upgrade + W4-W5 mixing complete"
```
