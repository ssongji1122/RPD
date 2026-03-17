# Week 3 시각화 업데이트 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Week 3 스텝 카드에 영상 클립 인라인 플레이어 + ShowMe 모듈을 결합하여 학생 이해도를 높인다.

**Architecture:** curriculum.js에 `clips` 필드를 추가하고, week.html에 인라인 비디오 플레이어 컴포넌트를 구현한다. 실제 Mint Robot 튜토리얼 영상에서 핵심 구간을 추출하여 클립으로 제공하고, 범용 ShowMe 교육 모듈로 개념을 보강한다.

**Tech Stack:** HTML/CSS/JS (vanilla), ffmpeg (클립 추출), Canvas 2D (ShowMe)

**Source Videos:**
- `001.Mint_Robot_reference_setting.mov` (8min, 3024x1894) — 경로: `/Users/ssongji/Developer/Workspace/RPD/Blender_2026/Mint_robot/MR_Tutorial_videos/`
- `002.Mint_Robot_head_mirror.mov` (6min, 3024x1894) — 동일 경로

---

### Task 1: 영상 클립 추출 디렉토리 생성 및 클립 추출

**Files:**
- Create: `course-site/assets/clips/week03/` (디렉토리)
- Create: `course-site/assets/clips/week03/*.mp4` (6개 클립)

**Step 1: 디렉토리 생성**

```bash
mkdir -p course-site/assets/clips/week03
```

**Step 2: Video 001에서 클립 3개 추출**

영상 내용 타임라인:
- 0:00-1:30 — 기본 씬 정리 (Collection 이동)
- 1:30-3:00 — Shift+A → Image → File Browser에서 선택
- 3:00-4:30 — 3개 레퍼런스 이미지 배치 (정면/측면/후면)
- 4:30-6:00 — 크기/Opacity 조정, Orthographic 뷰 정렬
- 6:00-8:00 — 최종 확인, 사이드뷰 정리

```bash
SRC="/Users/ssongji/Developer/Workspace/RPD/Blender_2026/Mint_robot/MR_Tutorial_videos/001.Mint_Robot_reference_setting.mov"
OUT="course-site/assets/clips/week03"

# 클립 1: Shift+A → Image → 파일 선택 (1:30~3:00, 90초 → 30초 2x)
ffmpeg -ss 90 -i "$SRC" -t 90 -vf "scale=1280:-2" -c:v libx264 -preset slow -crf 26 -an -movflags +faststart "$OUT/ref-import.mp4"

# 클립 2: 3장 배치 + Orthographic 정렬 (3:00~4:30, 90초)
ffmpeg -ss 180 -i "$SRC" -t 90 -vf "scale=1280:-2" -c:v libx264 -preset slow -crf 26 -an -movflags +faststart "$OUT/ref-position.mp4"

# 클립 3: Opacity 조절 + 최종 뷰 설정 (5:30~7:00, 90초)
ffmpeg -ss 330 -i "$SRC" -t 90 -vf "scale=1280:-2" -c:v libx264 -preset slow -crf 26 -an -movflags +faststart "$OUT/ref-opacity.mp4"
```

**Step 3: Video 002에서 클립 3개 추출**

영상 내용 타임라인:
- 0:00-2:00 — Cube → 머리 비율 스케일 + X-Ray
- 2:00-3:30 — Edit Mode → Edge Slide로 형태 조정
- 3:30-5:00 — 절반 삭제 + Mirror Modifier + Clipping
- 5:00-6:00 — 대칭 편집 결과 확인

```bash
SRC="/Users/ssongji/Developer/Workspace/RPD/Blender_2026/Mint_robot/MR_Tutorial_videos/002.Mint_Robot_head_mirror.mov"

# 클립 4: Cube 스케일 + X-Ray (0:00~2:00, 120초)
ffmpeg -ss 0 -i "$SRC" -t 120 -vf "scale=1280:-2" -c:v libx264 -preset slow -crf 26 -an -movflags +faststart "$OUT/head-scale.mp4"

# 클립 5: Edge Slide 형태 조정 (2:00~3:30, 90초)
ffmpeg -ss 120 -i "$SRC" -t 90 -vf "scale=1280:-2" -c:v libx264 -preset slow -crf 26 -an -movflags +faststart "$OUT/head-edit.mp4"

# 클립 6: Mirror 설정 + 결과 (3:30~6:00, 150초)
ffmpeg -ss 210 -i "$SRC" -t 150 -vf "scale=1280:-2" -c:v libx264 -preset slow -crf 26 -an -movflags +faststart "$OUT/mirror-setup.mp4"
```

**Step 4: 파일 크기 확인**

```bash
ls -lh course-site/assets/clips/week03/
```

Expected: 각 파일 2-8MB 범위

**Step 5: .gitignore에 클립 추가 (대용량 바이너리)**

`.gitignore`에 클립 디렉토리를 추가해야 할지 확인. 파일이 10MB 이하이면 git에 포함, 아니면 `.gitignore`에 추가하고 별도 호스팅.

```bash
du -sh course-site/assets/clips/week03/
```

**Step 6: Commit**

```bash
git add course-site/assets/clips/week03/
git commit -m "content: Week 3 Mint Robot 튜토리얼 영상 클립 6개 추출"
```

---

### Task 2: week.html에 인라인 비디오 플레이어 컴포넌트 추가

**Files:**
- Modify: `course-site/week.html` (CSS + JS)

**Step 1: CSS 추가 — 클립 플레이어 스타일**

`week.html`의 `<style>` 블록에 추가 (`.btn-showme.is-complete:hover` 뒤, 약 line 147 이후):

```css
/* ── Clip Player ── */
.clip-player {
  border-radius: var(--radius-md);
  border: 1px solid var(--line);
  background: var(--surface);
  overflow: hidden;
  margin-bottom: 14px;
}
.clip-player video {
  display: block; width: 100%;
  border-radius: var(--radius-md) var(--radius-md) 0 0;
  cursor: pointer;
}
.clip-tabs {
  display: flex; gap: 0;
  border-top: 1px solid var(--line);
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}
.clip-tabs::-webkit-scrollbar { display: none; }
.clip-tab {
  flex: 1; min-width: 0;
  padding: 9px 14px;
  font: inherit; font-size: .78rem; font-weight: 500;
  color: var(--muted);
  background: none; border: none;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  white-space: nowrap;
  text-align: center;
  transition: color .14s, border-color .14s, background .14s;
}
.clip-tab:hover { color: var(--muted-strong); background: rgba(255,255,255,.03); }
.clip-tab.is-active {
  color: var(--key-soft);
  border-bottom-color: var(--key);
  background: rgba(10,132,255,.04);
}
/* 클립이 1개일 때 탭 바 숨기기 */
.clip-tabs:has(.clip-tab:only-child) { display: none; }
.clip-player-hint {
  font-size: .72rem; color: var(--muted);
  text-align: center; padding: 4px 0 6px;
}
```

**Step 2: JS — 스텝 렌더링에 clips 필드 처리 추가**

`week.html`의 `stepsHtml` 빌드 코드 (약 line 434)에서, `step.image` 렌더링 뒤에 clips 렌더링을 추가:

현재 코드 (line 464-466):
```js
${step.image ? (step.link
  ? `<a href="${step.link}" target="_blank" rel="noopener noreferrer"><img src="${step.image}" alt="${step.title}" class="step-image" loading="lazy" /></a>`
  : `<img src="${step.image}" alt="${step.title}" class="step-image" loading="lazy" />`) : ""}
```

이 뒤에 추가:
```js
${step.clips && step.clips.length ? `
  <div class="clip-player" data-step-clips>
    <video src="${step.clips[0].src}" autoplay loop muted playsinline
           onclick="this.paused ? this.play() : this.pause()"
           title="클릭하면 일시정지/재생"></video>
    ${step.clips.length > 1 ? `
      <div class="clip-tabs">${step.clips.map((c, ci) =>
        `<button class="clip-tab${ci === 0 ? ' is-active' : ''}" type="button"
                 data-clip-src="${c.src}" data-clip-idx="${ci}">${c.label}</button>`
      ).join('')}</div>` : ''}
    <div class="clip-player-hint">클릭하면 일시정지 · 다시 클릭하면 재생</div>
  </div>` : ""}
```

**Step 3: JS — 클립 탭 전환 이벤트 핸들러**

`buildPage` 함수 끝, `initProgress()` 호출 전에 추가:

```js
// ─── Clip tab switching ───
document.querySelectorAll(".clip-player").forEach(function(player) {
  player.querySelectorAll(".clip-tab").forEach(function(tab) {
    tab.addEventListener("click", function() {
      player.querySelectorAll(".clip-tab").forEach(function(t) { t.classList.remove("is-active"); });
      tab.classList.add("is-active");
      var video = player.querySelector("video");
      video.src = tab.dataset.clipSrc;
      video.play();
    });
  });
});
```

**Step 4: 확인 — 브라우저에서 week.html?week=3 열어서 클립 플레이어 확인**

Expected: 클립이 있는 스텝에 인라인 비디오가 autoplay loop muted로 재생, 탭 전환 가능

**Step 5: Commit**

```bash
git add course-site/week.html
git commit -m "feat: week.html에 인라인 클립 플레이어 컴포넌트 추가"
```

---

### Task 3: curriculum.js Week 3 구조 업데이트

**Files:**
- Modify: `course-site/data/curriculum.js` (Week 3 steps 섹션)

**Step 1: Step 1을 "레퍼런스 이미지 설정"으로 분리**

현재 Step 1 "기본형 만들기"는 레퍼런스 설정 + Edit Mode 작업이 합쳐져 있다. 레퍼런스 설정 부분을 독립 Step 1로 분리.

**새 Step 1:**
```js
{
  "title": "레퍼런스 이미지 설정",
  "copy": "Shift+A → Image로 정면·측면·후면 레퍼런스를 불러와요. Orthographic 뷰(Numpad 1/3)에 맞춰 배치하고, Opacity를 낮추면 모델링 가이드로 쓸 수 있어요.",
  "goal": [
    "Reference Image를 뷰포트에 배치한다",
    "Orthographic 뷰에서 정렬한다"
  ],
  "tasks": [
    {
      "id": "w3-t1",
      "label": "Shift+A → Image → Reference로 정면 이미지 불러오기",
      "detail": "Downloads에서 robot-ref-front.png 선택"
    },
    {
      "id": "w3-t1b",
      "label": "측면·후면 이미지도 추가하기",
      "detail": "각각 Numpad 3, Ctrl+Numpad 1 뷰에서 추가"
    },
    {
      "id": "w3-t1c",
      "label": "Opacity를 0.3으로 낮추고 크기 조절하기",
      "detail": "Properties > Object Data > Opacity"
    }
  ],
  "clips": [
    { "label": "이미지 불러오기", "src": "assets/clips/week03/ref-import.mp4" },
    { "label": "3장 배치", "src": "assets/clips/week03/ref-position.mp4" },
    { "label": "Opacity · 정렬", "src": "assets/clips/week03/ref-opacity.mp4" }
  ],
  "done": [
    "3장의 Reference Image가 뷰포트에 깔려 있다",
    "Orthographic 뷰에서 레퍼런스와 3D 커서가 정렬되어 있다"
  ],
  "showme": "image-reference",
  "link": "https://docs.blender.org/manual/en/latest/editors/3dview/display/overlays.html"
}
```

**Step 2 수정 (기존 Step 1 → "기본형 만들기", Edit Mode 중심):**

레퍼런스 관련 task를 제거하고, 클립 추가:

```js
{
  "title": "기본형 만들기",
  "copy": "Cube를 레퍼런스에 맞춰 스케일하고, Edit Mode에서 Edge Slide로 형태를 잡아요. X-Ray(Alt+Z)를 켜면 레퍼런스를 투시하면서 작업할 수 있어요.",
  "goal": [
    "Cube를 레퍼런스 비율에 맞게 스케일한다",
    "Edit Mode에서 형태를 다듬는다"
  ],
  "tasks": [
    {
      "id": "w3-t2",
      "label": "Cube를 머리 크기에 맞게 S로 스케일하기",
      "detail": "Alt+Z로 X-Ray 켜서 레퍼런스 확인"
    },
    {
      "id": "w3-t3",
      "label": "Loop Cut (Ctrl+R)으로 분할선 추가하기",
      "detail": "스크롤로 루프 개수 조절"
    },
    {
      "id": "w3-t4",
      "label": "Edge Slide (G+G)로 엣지를 레퍼런스에 맞추기",
      "detail": "정면·측면 뷰를 번갈아 확인"
    }
  ],
  "clips": [
    { "label": "Cube 스케일", "src": "assets/clips/week03/head-scale.mp4" },
    { "label": "Edge Slide", "src": "assets/clips/week03/head-edit.mp4" }
  ],
  "done": [
    "Cube가 머리 레퍼런스와 비슷한 비율이다",
    "Edge가 주요 윤곽선에 맞게 배치되었다"
  ],
  "showme": "edit-mode-tools",
  "link": "https://docs.blender.org/manual/en/latest/modeling/meshes/tools/extrude_region.html"
}
```

**Step 3 수정 (기존 Step 2 → Mirror, 클립 추가):**

```js
{
  "title": "Mirror",
  "copy": "X축을 기준으로 반쪽을 대칭 복사해요. 한쪽만 만들면 작업량이 반으로 줄어요. Clipping을 켜면 중앙 정점이 넘어가지 않게 붙잡아줘요.",
  "goal": [
    "Mirror를 추가하고 Clipping을 설정한다"
  ],
  "tasks": [
    {
      "id": "w3-t5",
      "label": "절반 지우고 Add Modifier → Mirror 추가하기",
      "detail": "Axis: X 확인"
    },
    {
      "id": "w3-t6",
      "label": "Clipping 옵션 켜기",
      "detail": "중심선 버텍스가 넘어가지 않게 고정"
    },
    {
      "id": "w3-t7",
      "label": "한쪽만 Extrude해서 대칭 반영 확인하기",
      "detail": "중심선 벌어지면 S+X+0으로 정렬"
    }
  ],
  "clips": [
    { "label": "Mirror 워크플로우", "src": "assets/clips/week03/mirror-setup.mp4" }
  ],
  "image": "assets/images/week03/mirror-modifier.png",
  "done": [
    "한쪽을 움직이면 반대쪽도 같이 바뀐다",
    "Clipping으로 중심선이 벌어지지 않는다"
  ],
  "showme": ["mirror-modifier", "mirror-workflow"],
  "link": "https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/mirror.html"
}
```

**Step 2: 나머지 steps (Subdivision, Solidify, Array, Boolean 등) — 기존 유지, 번호만 조정**

기존 Step 3 → Step 4, Step 4 → Step 5 ... (task ID는 기존 유지)

**Step 3: Commit**

```bash
git add course-site/data/curriculum.js
git commit -m "content: Week 3 스텝 구조 재편 + clips 필드 추가 (레퍼런스 설정 분리)"
```

---

### Task 4: ShowMe 레지스트리에 mirror-workflow 추가

**Files:**
- Modify: `course-site/assets/showme/_registry.js`

**Step 1: mirror-workflow 엔트리 추가**

`_registry.js`의 Generate Modifiers 섹션에서 `mirror-modifier` 뒤에 추가:

```js
"mirror-workflow":        { label: "Mirror 작업 흐름",          icon: "🔄" },
```

**Step 2: Commit**

```bash
git add course-site/assets/showme/_registry.js
git commit -m "feat: ShowMe 레지스트리에 mirror-workflow 추가"
```

---

### Task 5: ShowMe 위젯 — mirror-workflow.html 신규 제작

**Files:**
- Create: `course-site/assets/showme/mirror-workflow.html`

**Step 1: _template.html 기반으로 mirror-workflow.html 작성**

4개 탭 구성:
1. **개념 이해** — Mirror 워크플로우 3단계 (절반 삭제 → Mirror 추가 → Clipping 편집) 개념 카드
2. **시각적 비교** — Canvas 2D 애니메이션: 큐브가 절반 삭제되고, 미러가 적용되고, 한쪽을 편집하면 반대쪽이 따라가는 과정
3. **언제 쓰나요?** — 대칭 캐릭터/로봇/차량 등 사용 사례
4. **퀴즈** — Mirror 워크플로우 관련 3문제

**Canvas 애니메이션 핵심 로직:**

```js
// 상태: "full" → "half" → "mirror" → "edit"
var phase = "full";    // 현재 단계
var t = 0;             // 애니메이션 타이머

function draw() {
  ctx.clearRect(0, 0, W, H);
  drawGrid();
  drawCenterLine();     // 빨간 점선 (X=0 축)

  switch(phase) {
    case "full":
      drawBox(-80, 80);  // 전체 큐브 (양쪽)
      break;
    case "half":
      drawBox(0, 80);    // 오른쪽만 (왼쪽 삭제됨)
      drawDeleteAnim(t); // 왼쪽이 사라지는 애니메이션
      break;
    case "mirror":
      drawBox(0, 80);           // 원본 (오른쪽)
      drawMirrorBox(-80, 0, 0.4); // 미러 (왼쪽, 반투명)
      break;
    case "edit":
      var ex = Math.sin(t * 0.02) * 20; // 편집 움직임
      drawBox(0, 80 + ex);              // 원본 변형
      drawMirrorBox(-80 - ex, 0, 0.4);  // 미러가 따라감
      break;
  }
}
```

**데모 컨트롤:** 4개 버튼으로 단계 전환
- "1. 전체 형태" / "2. 절반 삭제" / "3. Mirror 추가" / "4. 한쪽 편집"

**퀴즈 데이터:**
```js
initQuiz([
  {
    question: "Mirror를 쓰기 전에 먼저 해야 할 작업은?",
    options: ["Subdivision Surface 추가", "대칭축 기준으로 절반 삭제", "Apply All Transforms", "오브젝트 복제"],
    answer: 1,
    explanation: "Mirror는 남은 절반을 기준으로 대칭 복사하므로, 먼저 한쪽을 지워야 합니다."
  },
  {
    question: "Clipping 옵션의 역할은?",
    options: ["미러를 비활성화한다", "중심선 버텍스가 축을 넘지 못하게 고정한다", "미러 결과를 Apply한다", "UV를 자동 펼친다"],
    answer: 1,
    explanation: "Clipping을 켜면 중심선의 버텍스가 대칭축을 넘어가지 않아서 이음새 없는 대칭을 유지할 수 있어요."
  },
  {
    question: "중심선이 벌어졌을 때 빠르게 정렬하는 단축키는?",
    options: ["G+X+0", "S+X+0", "R+X+0", "Alt+M"],
    answer: 1,
    explanation: "S+X+0은 X축 스케일을 0으로 만들어서 선택한 버텍스들을 X축 기준으로 일직선에 놓아줍니다."
  }
]);
```

**Step 2: 브라우저에서 독립 확인**

```
open course-site/assets/showme/mirror-workflow.html
```

Expected: 4개 탭 모두 정상 동작, Canvas 애니메이션 재생

**Step 3: Commit**

```bash
git add course-site/assets/showme/mirror-workflow.html
git commit -m "feat: ShowMe mirror-workflow 위젯 신규 제작 (범용 교육 모듈)"
```

---

### Task 6: /clip 스킬 생성

**Files:**
- Create: `.claude/skills/clip.md`

**Step 1: 스킬 파일 작성**

```markdown
---
name: clip
description: 영상 클립 추출 자동화. 예: /clip week 3 001.mov 0:30-0:55 "이미지 불러오기"
user_invocable: true
---

# Clip 추출 스킬

## 사용법

```
/clip week <주차> <source.mov> <start>-<end> "<label>"
/clip list week <주차>
```

## 동작

1. ffmpeg으로 소스 영상에서 지정 구간 추출
2. 720p (1280px width) H.264 MP4로 압축, 오디오 제거
3. `course-site/assets/clips/week{NN}/` 에 저장
4. curriculum.js의 해당 주차 step에 clips 엔트리 추가

## 추출 명령

```bash
ffmpeg -ss <start> -i "<source>" -t <duration> \
  -vf "scale=1280:-2" -c:v libx264 -preset slow -crf 26 \
  -an -movflags +faststart \
  "course-site/assets/clips/week{NN}/<slug>.mp4"
```

## 파일명 규칙
- 소문자 영문, 하이픈 구분
- 예: `ref-import.mp4`, `mirror-setup.mp4`

## curriculum.js 업데이트
- 해당 step의 `clips` 배열에 `{ "label": "<label>", "src": "assets/clips/week{NN}/<slug>.mp4" }` 추가
- clips 배열이 없으면 새로 생성
```

**Step 2: Commit**

```bash
git add .claude/skills/clip.md
git commit -m "feat: /clip 스킬 생성 (영상 클립 추출 자동화)"
```

---

### Task 7: Blender 5.0 메모리 저장

**Files:**
- Modify: `/Users/ssongji/.claude/projects/-Users-ssongji-Developer-Workspace-RPD/memory/` (user memory)

**Step 1: Blender 5.0 사용 정보 저장**

```markdown
---
name: blender-version
description: 사용자가 Blender 5.0을 사용 중 — ShowMe/curriculum 콘텐츠는 5.0 UI 기준으로 작성
type: user
---

Blender 5.0.1 사용 중.
ShowMe 위젯과 curriculum.js 콘텐츠에서 UI 참조(메뉴 위치, 패널 이름, 단축키)는 Blender 5.0 기준으로 작성해야 한다.
```

**Step 2: MEMORY.md 업데이트**

---

### Task 8: 통합 테스트 및 프리뷰 확인

**Step 1: 정적 서버 실행**

```bash
python3 -m http.server 8895 -d course-site
```

**Step 2: week.html?week=3 접속하여 확인 항목:**

- [ ] Step 1 (레퍼런스 이미지 설정)에 클립 3개 탭 표시
- [ ] 클립 autoplay loop muted 재생
- [ ] 탭 클릭 시 영상 전환
- [ ] 클립 클릭 시 일시정지/재생
- [ ] Step 2 (기본형 만들기)에 클립 2개 탭 표시
- [ ] Step 3 (Mirror)에 클립 1개 + 이미지 표시
- [ ] ShowMe 버튼 "Mirror 작업 흐름" 표시
- [ ] ShowMe 모달에서 mirror-workflow.html 정상 로드
- [ ] Canvas 애니메이션 재생 + 데모 버튼 전환
- [ ] 퀴즈 동작

**Step 3: 최종 Commit**

```bash
git add -A
git commit -m "feat: Week 3 시각화 업데이트 완료 — 클립 플레이어 + ShowMe mirror-workflow"
```
