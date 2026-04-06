# Week 05 콘텐츠 보강 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 5주차 curriculum.js Step 텍스트 보강 + ShowMe 카드 4개 신규 구현으로 학생이 브러시 선택, 프롬프트 작성, Before/After 촬영에서 막히지 않게 한다.

**Architecture:** curriculum.js(SSOT) 직접 편집 → _registry.js에 카드 ID 등록 → _supplements.json에 카드 내용 추가. 웹사이트와 Notion은 자동 반영.

**Tech Stack:** JavaScript(curriculum.js, _registry.js), JSON(_supplements.json), Node.js(검증), Python3(JSON 검증)

---

## 파일 변경 목록

| 파일 | 유형 | 변경 내용 |
|------|------|-----------|
| `course-site/data/curriculum.js` | 수정 | Step 2·4·6 텍스트, shortcuts 2개, checklist 1개 |
| `course-site/assets/showme/_registry.js` | 수정 | 신규 항목 3개 추가 |
| `course-site/assets/showme/_supplements.json` | 수정 | 신규 카드 4개 추가 |

모든 작업 디렉토리: `/Users/ssongji/Developer/Workspace/RPD`

---

## Task 1: curriculum.js — Step 2 브러시 판단 기준 추가

**Files:**
- Modify: `course-site/data/curriculum.js`

- [ ] **Step 1: 현재 상태 확인**

```bash
cd /Users/ssongji/Developer/Workspace/RPD
node -e "
const c = require('./course-site/data/curriculum.js');
const w5 = c.find(w=>w.week===5);
w5.steps[1].tasks.forEach(t => console.log(t.id, '|', t.detail));
"
```

Expected:
```
w5-t12 | 넓은 면 위에 층층이 쌓기
w5-t13 | 관절, 눈, 입 라인에 활용
w5-t14 | 볼이나 근육 강조에 유용
w5-t-snake | 끝점이 따라오며 길게 늘어나요
```

- [ ] **Step 2: 4개 task detail 수정**

`course-site/data/curriculum.js`에서 아래 4개를 순서대로 교체 (Edit 도구 사용):

```
"detail": "넓은 면 위에 층층이 쌓기"
→
"detail": "넓은 면 위에 층층이 쌓기 — 큰 볼륨을 올려야 할 때"
```

```
"detail": "관절, 눈, 입 라인에 활용"
→
"detail": "관절, 눈, 입 라인에 활용 — 선이 파여야 할 때"
```

```
"detail": "볼이나 근육 강조에 유용"
→
"detail": "볼이나 근육 강조에 유용 — 표면 전체를 부풀려야 할 때"
```

```
"detail": "끝점이 따라오며 길게 늘어나요"
→
"detail": "끝점이 따라오며 길게 늘어나요 — 뿔·안테나·꼬리를 끄집어낼 때"
```

- [ ] **Step 3: 검증**

```bash
node -e "
const c = require('./course-site/data/curriculum.js');
const w5 = c.find(w=>w.week===5);
const tasks = w5.steps[1].tasks;
const checks = [
  tasks.find(t=>t.id==='w5-t12').detail.includes('큰 볼륨'),
  tasks.find(t=>t.id==='w5-t13').detail.includes('선이 파여야'),
  tasks.find(t=>t.id==='w5-t14').detail.includes('부풀려야'),
  tasks.find(t=>t.id==='w5-t-snake').detail.includes('끄집어낼'),
];
console.log(checks.every(Boolean) ? 'PASS' : 'FAIL', checks);
"
```

Expected: `PASS [ true, true, true, true ]`

- [ ] **Step 4: 커밋**

```bash
git add course-site/data/curriculum.js
git commit -m "content(w5): add brush selection criteria to step 2 task details"
```

---

## Task 2: curriculum.js — Step 4 프롬프트 보강 + Step 6 촬영 가이드 + shortcuts + checklist

**Files:**
- Modify: `course-site/data/curriculum.js`

- [ ] **Step 1: Step 4 copy 보강**

`course-site/data/curriculum.js`에서 Step 4(`w5-t-mood1`이 포함된 step)의 copy를 교체:

```
"copy": "1주차에 만든 무드보드, 기억하죠? 오늘 그걸 3D로 만들기 시작해요. AI한테 잘 설명하려면 이미지 느낌을 단어로 번역하는 과정이 필요해요."
```

→

```
"copy": "1주차에 만든 무드보드, 기억하죠? 오늘 그걸 3D로 만들기 시작해요. AI한테 잘 설명하려면 이미지 느낌을 단어로 번역하는 과정이 필요해요. 프롬프트는 짧을수록 AI가 멋대로 해석해요. 형태·스타일·재질감을 구체적으로 써야 원하는 결과가 나와요."
```

- [ ] **Step 2: Step 4에 신규 task 추가**

같은 Step 4의 `tasks` 배열에서 `w5-t-mood3` 항목 닫는 `}` 다음에 추가:

```json
            ,{
              "id": "w5-t-prompt-compare",
              "label": "나쁜 예 → 좋은 예 직접 고쳐보기",
              "detail": "나쁜 예: 'cute robot' → 좋은 예: 'small companion robot, spherical head, stubby arms, matte plastic finish, 3D model' — 공식: [형태]+[스타일]+[재질감]+3D model"
            }
```

- [ ] **Step 3: Step 6 마지막 task detail 수정**

`course-site/data/curriculum.js`에서 (`w5-t-clean3` task):

```
"detail": "정리 전후를 비교할 수 있게 저장"
```

→

```
"detail": "Numpad 1(앞면 고정) + Material Preview 모드에서 Before/After 동일 앵글로 촬영. 스크린샷: Ctrl+F3. After도 반드시 Numpad 1로 — 앵글 바꾸면 비교 안 돼요"
```

- [ ] **Step 4: shortcuts 2개 추가**

week5의 `shortcuts` 배열 마지막 항목(`"X" → "Draw 브러시 빠른 선택"`) 닫는 `}` 다음에 추가:

```json
        ,{
          "keys": "Numpad 1",
          "action": "앞면 뷰 고정 (Before/After 촬영 기준)"
        },
        {
          "keys": "Ctrl + F3",
          "action": "뷰포트 스크린샷 저장"
        }
```

- [ ] **Step 5: assignment checklist 항목 추가**

week5의 `assignment.checklist` 배열 마지막 항목 다음에 추가:

```json
        ,"완성 .blend 파일 저장 완료 — Week 6 Material 실습에서 이 파일을 씁니다"
```

- [ ] **Step 6: 검증**

```bash
node -e "
const c = require('./course-site/data/curriculum.js');
const w5 = c.find(w=>w.week===5);
const s4 = w5.steps[3];
const s6 = w5.steps[5];
const checks = [
  s4.copy.includes('짧을수록'),
  s4.tasks.some(t=>t.id==='w5-t-prompt-compare'),
  s6.tasks[s6.tasks.length-1].detail.includes('Numpad 1'),
  w5.shortcuts.some(s=>s.keys==='Numpad 1'),
  w5.shortcuts.some(s=>s.keys==='Ctrl + F3'),
  w5.assignment.checklist.some(c=>c.includes('Week 6')),
];
console.log(checks.every(Boolean) ? 'PASS' : 'FAIL', checks);
"
```

Expected: `PASS [ true, true, true, true, true, true ]`

- [ ] **Step 7: 커밋**

```bash
git add course-site/data/curriculum.js
git commit -m "content(w5): enrich step4 prompt guide, step6 screenshot guide, shortcuts, checklist"
```

---

## Task 3: _registry.js — ShowMe 카드 3개 등록

**Files:**
- Modify: `course-site/assets/showme/_registry.js`

- [ ] **Step 1: 현재 week 5 항목 확인**

```bash
grep "week: 5" course-site/assets/showme/_registry.js
```

Expected: `sculpt-basics` 1줄만 출력

- [ ] **Step 2: 신규 항목 3개 추가**

`_registry.js`에서 아래 줄을 찾아:

```
  "sculpt-basics":          { label: "Sculpt Mode 기초",        icon: "🎨", week: 5 },
```

→ 아래처럼 교체 (3줄 추가):

```
  "sculpt-basics":          { label: "Sculpt Mode 기초",        icon: "🎨", week: 5 },
  "sculpt-brushes":         { label: "Sculpt 브러시 선택 기준",  icon: "🖌️", week: 5 },
  "ai-prompt-design":       { label: "AI 프롬프트 설계법",       icon: "✍️", week: 5 },
  "ai-3d-generation":       { label: "AI 3D 생성 워크플로우",    icon: "🤖", week: 5 },
```

- [ ] **Step 3: 검증**

```bash
grep -c "week: 5" course-site/assets/showme/_registry.js
grep "sculpt-brushes\|ai-prompt-design\|ai-3d-generation" course-site/assets/showme/_registry.js
```

Expected:
```
4
  "sculpt-brushes":  ...
  "ai-prompt-design": ...
  "ai-3d-generation": ...
```

- [ ] **Step 4: 커밋**

```bash
git add course-site/assets/showme/_registry.js
git commit -m "feat(showme): register sculpt-brushes, ai-prompt-design, ai-3d-generation for week5"
```

---

## Task 4: _supplements.json — sculpt-basics 카드

**Files:**
- Modify: `course-site/assets/showme/_supplements.json`

- [ ] **Step 1: JSON 유효성 + 현재 상태 확인**

```bash
python3 -c "
import json
data = json.load(open('course-site/assets/showme/_supplements.json'))
print('cards:', len(data), '| sculpt-basics exists:', 'sculpt-basics' in data)
"
```

Expected: `cards: 33 | sculpt-basics exists: False`

- [ ] **Step 2: sculpt-basics 카드 추가**

`_supplements.json`의 마지막 카드(`scatter-on-surface`) 닫는 `}` 뒤에 `,` 추가 후 아래 내용 삽입 (파일 끝 `}` 앞):

```json
  "sculpt-basics": {
    "title": "Sculpt Mode, 어렵게 생각 말아요",
    "analogy": {
      "emoji": "🏺",
      "headline": "디지털 점토 조각이에요",
      "body": "Sculpt Mode는 마우스로 디지털 점토를 주무르는 거예요. 버텍스 좌표를 계산하는 게 아니라, 브러시로 밀고 당기고 부드럽게 만들면 돼요. 조각가가 점토 덩어리를 손으로 다듬는 느낌과 완전히 같아요."
    },
    "before_after": {
      "before": "Edit Mode로만 유기적인 형태를 만들려면 버텍스 하나하나를 G키로 이동시켜야 해서 자연스러운 곡면이 나오지 않는다.",
      "after": "Sculpt Mode에서 Grab 브러시 하나로 형태를 잡아당기면 자연스러운 곡면이 즉시 만들어진다."
    },
    "confusion": [
      {
        "symptom": "브러시로 칠해도 메쉬가 움직이지 않아요.",
        "reason": "폴리곤 수가 너무 적으면 브러시 효과가 눈에 보이지 않아요.",
        "fix": "Sculpt Mode 상단 Remesh 버튼(Ctrl+R)으로 폴리곤을 늘린 다음 다시 시도하세요."
      }
    ],
    "takeaway": "Sculpt는 계산이 아니라 감각이에요. 일단 브러시로 밀고 당겨보면서 형태를 잡는 거예요.",
    "officialVideos": [
      {
        "url": "https://studio.blender.org/training/sculpting-in-blender/introduction/",
        "label": "Blender Studio — Introduction to Sculpting"
      }
    ],
    "targets": ["sculpt-basics"]
  }
```

- [ ] **Step 3: 검증**

```bash
python3 -c "
import json
data = json.load(open('course-site/assets/showme/_supplements.json'))
card = data.get('sculpt-basics', {})
checks = [
  'sculpt-basics' in data,
  'analogy' in card,
  'before_after' in card,
  'confusion' in card,
  'officialVideos' in card,
  len(card.get('officialVideos',[])) >= 1,
]
print('PASS' if all(checks) else 'FAIL', checks)
"
```

Expected: `PASS [True, True, True, True, True, True]`

- [ ] **Step 4: 커밋**

```bash
git add course-site/assets/showme/_supplements.json
git commit -m "feat(showme): add sculpt-basics supplement card with officialVideos"
```

---

## Task 5: _supplements.json — sculpt-brushes 카드

**Files:**
- Modify: `course-site/assets/showme/_supplements.json`

- [ ] **Step 1: sculpt-brushes 카드 추가**

`sculpt-basics` 카드 닫는 `}` 뒤에 `,` 추가 후 삽입:

```json
  "sculpt-brushes": {
    "title": "어떤 브러시를 써야 할지 모르겠다면?",
    "analogy": {
      "emoji": "🎨",
      "headline": "연필·지우개·블렌더를 상황마다 골라 쓰듯이",
      "body": "그림 그릴 때 스케치는 연필, 실수는 지우개, 경계는 블렌더로 처리하잖아요. Sculpt 브러시도 똑같아요. 처음엔 Grab과 Smooth만 써도 충분해요. 익숙해지면 Clay, Crease, Inflate, Snake Hook을 추가하면 돼요."
    },
    "before_after": {
      "before": "Draw 브러시 하나만 쓰면 모든 형태를 올리고 내리는 것만 반복하게 되어서, 형태 잡기도 느리고 디테일 표현도 힘들다.",
      "after": "큰 형태는 Grab, 볼륨은 Clay Strips, 선은 Crease, 정리는 Smooth로 나눠 쓰면 훨씬 빠르게 원하는 형태가 나온다."
    },
    "confusion": [
      {
        "symptom": "어떤 브러시를 써야 할지 모르겠어요.",
        "reason": "브러시가 너무 많아서 선택 자체가 어렵게 느껴지기 때문이에요.",
        "fix": "형태 잡기=Grab, 볼륨 쌓기=Clay Strips, 선 파기=Crease, 부풀리기=Inflate, 길게 뽑기=Snake Hook, 정리=Smooth. 이 6개만 기억하세요."
      }
    ],
    "takeaway": "브러시를 많이 아는 것보다 상황에 맞는 브러시를 바로 떠올리는 게 더 중요해요.",
    "officialVideos": [
      {
        "url": "https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/index.html",
        "label": "Blender 공식 — Sculpt Brushes 전체 목록"
      }
    ],
    "targets": ["sculpt-brushes"]
  }
```

- [ ] **Step 2: 검증**

```bash
python3 -c "
import json
data = json.load(open('course-site/assets/showme/_supplements.json'))
card = data.get('sculpt-brushes', {})
checks = [
  'sculpt-brushes' in data,
  card.get('analogy',{}).get('emoji') == '🎨',
  len(card.get('confusion',[])) >= 1,
  len(card.get('officialVideos',[])) >= 1,
]
print('PASS' if all(checks) else 'FAIL', checks)
"
```

Expected: `PASS [True, True, True, True]`

- [ ] **Step 3: 커밋**

```bash
git add course-site/assets/showme/_supplements.json
git commit -m "feat(showme): add sculpt-brushes supplement card with brush selection guide"
```

---

## Task 6: _supplements.json — ai-prompt-design 카드

**Files:**
- Modify: `course-site/assets/showme/_supplements.json`

- [ ] **Step 1: ai-prompt-design 카드 추가**

`sculpt-brushes` 카드 닫는 `}` 뒤에 `,` 추가 후 삽입:

```json
  "ai-prompt-design": {
    "title": "AI한테 어떻게 설명해야 원하는 게 나올까요?",
    "analogy": {
      "emoji": "📦",
      "headline": "배달 주소처럼 구체적으로 말해야 해요",
      "body": "'서울 어딘가'라고 하면 못 찾아요. 동·건물명·층수까지 말해야 찾아가죠. AI 프롬프트도 같아요. '로봇'은 너무 막연하고, '동글한 머리, 짧은 팔, 매트한 플라스틱 재질의 소형 동반자 로봇'이라고 해야 내 의도에 가깝게 나와요."
    },
    "before_after": {
      "before": "'cute robot'으로 생성하면 AI가 마음대로 해석해서 전혀 다른 스타일이 나온다.",
      "after": "'small companion robot, spherical head, stubby arms, matte plastic finish, 3D model'로 생성하면 형태와 재질감이 훨씬 의도에 가깝게 나온다."
    },
    "confusion": [
      {
        "symptom": "프롬프트를 길게 썼는데도 결과가 이상해요.",
        "reason": "'귀여운', '멋진' 같은 추상적인 형용사만 넣었기 때문이에요.",
        "fix": "추상 형용사 대신 형태를 묘사하는 구체적 명사를 쓰세요. 'cute' 대신 'spherical head, round body'처럼요."
      }
    ],
    "takeaway": "공식: [형태 1~2개] + [스타일 1개] + [재질감 1~2개] + '3D model'. 이 순서로 쓰면 대부분 의도에 가깝게 나와요.",
    "officialVideos": [
      {
        "url": "https://docs.meshy.ai/",
        "label": "Meshy AI — 공식 문서 (프롬프트 가이드 포함)"
      }
    ],
    "targets": ["ai-prompt-design"]
  }
```

- [ ] **Step 2: 검증**

```bash
python3 -c "
import json
data = json.load(open('course-site/assets/showme/_supplements.json'))
card = data.get('ai-prompt-design', {})
checks = [
  'ai-prompt-design' in data,
  card.get('takeaway','').startswith('공식:'),
  '3D model' in card.get('before_after',{}).get('after',''),
  len(card.get('officialVideos',[])) >= 1,
]
print('PASS' if all(checks) else 'FAIL', checks)
"
```

Expected: `PASS [True, True, True, True]`

- [ ] **Step 3: 커밋**

```bash
git add course-site/assets/showme/_supplements.json
git commit -m "feat(showme): add ai-prompt-design supplement card with prompt formula"
```

---

## Task 7: _supplements.json — ai-3d-generation 카드 + 전체 검증

**Files:**
- Modify: `course-site/assets/showme/_supplements.json`

- [ ] **Step 1: ai-3d-generation 카드 추가** (파일의 마지막 카드로)

`ai-prompt-design` 카드 닫는 `}` 뒤에 `,` 추가 후 삽입:

```json
  "ai-3d-generation": {
    "title": "AI가 만든 3D, 그냥 써도 될까요?",
    "analogy": {
      "emoji": "🤝",
      "headline": "AI는 조수예요. 70% 방향만 잡아줘요",
      "body": "AI 3D 생성 결과를 완성품으로 기대하면 실망해요. AI는 대략적인 형태를 빠르게 잡아주는 조수예요. 나머지 30%는 Blender에서 내가 다듬는 거예요. 오늘 목표는 '방향이 맞는지 확인'이지 '완성'이 아니에요."
    },
    "before_after": {
      "before": "AI 결과를 그대로 제출하면 토폴로지 문제, 디테일 부족, 의도와 다른 형태가 그대로 남는다.",
      "after": "AI 러프를 Sculpt나 Edit Mode로 다듬으면 작업 시간이 크게 줄면서도 완성도 높은 결과물이 나온다."
    },
    "confusion": [
      {
        "symptom": "AI가 만든 게 내 의도와 너무 달라요.",
        "reason": "프롬프트 키워드 하나가 AI 해석에 크게 영향을 줘요.",
        "fix": "키워드 하나씩 바꿔가며 2~3개 결과를 비교하세요. 가장 가까운 걸 선택하고 Blender에서 수정하면 돼요."
      },
      {
        "symptom": "Import한 메쉬 폴리곤이 너무 많아서 느려요.",
        "reason": "AI 도구는 기본으로 고해상도 메쉬를 생성해요.",
        "fix": "Decimate Modifier로 Ratio 0.3~0.5 적용하세요. 형태가 유지되는 최저 수치를 찾아요."
      }
    ],
    "takeaway": "AI 결과는 시작점이에요. 완벽하지 않아도 괜찮아요 — 방향이 맞는지 확인하고, 나머지는 Blender에서 다듬어요.",
    "officialVideos": [
      {
        "url": "https://docs.meshy.ai/",
        "label": "Meshy AI — 공식 문서"
      },
      {
        "url": "https://platform.tripo3d.ai/",
        "label": "Tripo AI — 공식 사이트"
      }
    ],
    "targets": ["ai-3d-generation"]
  }
```

- [ ] **Step 2: supplements.json 전체 최종 검증**

```bash
python3 -c "
import json
data = json.load(open('course-site/assets/showme/_supplements.json'))
new_cards = ['sculpt-basics', 'sculpt-brushes', 'ai-prompt-design', 'ai-3d-generation']
all_pass = True
for cid in new_cards:
    card = data.get(cid, {})
    ok = all([
        cid in data,
        'analogy' in card,
        'before_after' in card,
        'confusion' in card,
        'officialVideos' in card,
        len(card.get('targets',[])) > 0,
    ])
    print(('PASS' if ok else 'FAIL'), cid)
    if not ok: all_pass = False
print()
print('ALL PASS' if all_pass else 'SOME FAILED')
"
```

Expected:
```
PASS sculpt-basics
PASS sculpt-brushes
PASS ai-prompt-design
PASS ai-3d-generation

ALL PASS
```

- [ ] **Step 3: curriculum.js 전체 최종 검증**

```bash
node -e "
const c = require('./course-site/data/curriculum.js');
const w5 = c.find(w=>w.week===5);
const s2 = w5.steps[1]; const s4 = w5.steps[3]; const s6 = w5.steps[5];
const results = {
  's2 Clay': s2.tasks.find(t=>t.id==='w5-t12').detail.includes('큰 볼륨'),
  's2 Crease': s2.tasks.find(t=>t.id==='w5-t13').detail.includes('선이 파여야'),
  's2 Inflate': s2.tasks.find(t=>t.id==='w5-t14').detail.includes('부풀려야'),
  's2 Snake': s2.tasks.find(t=>t.id==='w5-t-snake').detail.includes('끄집어낼'),
  's4 copy': s4.copy.includes('짧을수록'),
  's4 task': s4.tasks.some(t=>t.id==='w5-t-prompt-compare'),
  's6 screenshot': s6.tasks[s6.tasks.length-1].detail.includes('Numpad 1'),
  'shortcut Numpad1': w5.shortcuts.some(s=>s.keys==='Numpad 1'),
  'shortcut CtrlF3': w5.shortcuts.some(s=>s.keys==='Ctrl + F3'),
  'checklist w6': w5.assignment.checklist.some(c=>c.includes('Week 6')),
};
const failed = Object.entries(results).filter(([,v])=>!v);
console.log(failed.length ? 'FAIL: ' + failed.map(([k])=>k).join(', ') : 'ALL PASS');
"
```

Expected: `ALL PASS`

- [ ] **Step 4: 최종 커밋**

```bash
git add course-site/assets/showme/_supplements.json
git commit -m "feat(showme): add ai-3d-generation supplement card — week5 showme complete"
```

---

## Self-Review

**Spec coverage:**

| 스펙 항목 | 구현 Task |
|-----------|-----------|
| Step 2 브러시 판단 기준 | Task 1 ✅ |
| Step 4 copy 보강 + 나쁜예/좋은예 task | Task 2 ✅ |
| Step 6 Before/After 촬영 가이드 | Task 2 ✅ |
| shortcuts Numpad1, Ctrl+F3 | Task 2 ✅ |
| checklist Week 6 연계 | Task 2 ✅ |
| _registry.js 3개 신규 | Task 3 ✅ |
| sculpt-basics supplement | Task 4 ✅ |
| sculpt-brushes supplement | Task 5 ✅ |
| ai-prompt-design supplement | Task 6 ✅ |
| ai-3d-generation supplement | Task 7 ✅ |
| done 필드 추가 없음 | 전 Task ✅ |
| lecture-note/slides/assignment.md 미수정 | 전 Task ✅ |

**Placeholder 스캔:** 없음. 모든 step에 실제 코드/값 포함.

**일관성 체크:**
- Task 3에서 등록한 registry key(`sculpt-brushes`, `ai-prompt-design`, `ai-3d-generation`)가 Task 5·6·7의 supplement key와 정확히 일치
- Task 2에서 추가한 task id `w5-t-prompt-compare`는 기존 id 패턴(`w5-t-*`)과 일치
- curriculum.js Step 4의 `"showme": "ai-prompt-design"` 참조값과 registry/supplement key가 일치
