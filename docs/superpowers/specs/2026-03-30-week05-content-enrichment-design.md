# Week 05 콘텐츠 보강 설계

**날짜**: 2026-03-30
**범위**: RPD 5주차 (AI 3D 생성 + Sculpting + MCP 활용)
**SSOT**: `course-site/data/curriculum.js`

---

## 배경

5주차 curriculum.js에 6개 Step이 정의되어 있으나, 학생 입장에서 아래 4가지 갭이 확인됨:

1. 프롬프트 작성 전략 — "왜 이 표현이 더 좋은가" 비교 없음
2. Sculpt 브러시 판단 기준 — 나열만 있고 "언제 이걸 쓰는가" 없음
3. Before/After 촬영 가이드 — "동일한 각도에서" 외 구체 방법 없음
4. Week 6 연계 안내 — 이번 결과물이 다음 주 재료임을 학생이 모름

추가로, curriculum.js에서 참조하는 ShowMe 카드 8개 중 4개(sculpt-basics, sculpt-brushes, ai-prompt-design, ai-3d-generation)가 미구현 상태.

---

## 설계 원칙

- SSOT는 `curriculum.js` 단독. `lecture-note.md`, `slides.md`, `assignment.md` 건드리지 않음
- 기존 Step 순서·구조 유지. `tasks[].detail` 강화가 주요 수단
- `done` 필드 추가 없음
- ShowMe 카드는 `officialVideos` 포함 — 영상을 카드 안에 임베드

---

## 변경 파일

| 파일 | 변경 유형 |
|------|-----------|
| `course-site/data/curriculum.js` | Step 텍스트 보강 (4곳) + shortcuts 2개 + checklist 1개 |
| `course-site/assets/showme/_registry.js` | 신규 항목 3개 추가 |
| `course-site/assets/showme/_supplements.json` | 신규 카드 4개 추가 |

---

## A. curriculum.js 변경 명세

### Step 2: Sculpt 브러시 심화

각 `task.detail`에 판단 기준(언제 쓰는가) 추가:

| 브러시 | 기존 detail | 추가 내용 |
|--------|-------------|-----------|
| Clay Strips | 넓은 면 위에 층층이 쌓기 | "큰 볼륨을 올려야 할 때" |
| Crease | 관절, 눈, 입 라인에 활용 | "선이 파여야 할 때" |
| Inflate | 볼이나 근육 강조에 유용 | "표면 전체를 부풀려야 할 때" |
| Snake Hook | 끝점이 따라오며 길게 늘어나요 | "뿔·안테나·꼬리를 끄집어낼 때" |

### Step 4: 무드보드 → AI 프롬프트 설계

`copy` 마지막에 한 문장 추가:
> "프롬프트는 짧을수록 AI가 멋대로 해석해요. 형태·스타일·재질감을 구체적으로 써야 원하는 결과가 나와요."

`tasks`에 신규 항목 1개 추가:
```json
{
  "id": "w5-t-prompt-compare",
  "label": "나쁜 예 → 좋은 예 직접 고쳐보기",
  "detail": "나쁜 예: 'cute robot' → 좋은 예: 'small companion robot, spherical head, stubby arms, matte plastic finish, 3D model' — 공식: [형태]+[스타일]+[재질감]+3D model"
}
```

### Step 6: AI 메쉬 정리 실전

마지막 task(`w5-t-clean3`) `detail` 변경:

- 기존: "정리 전후를 비교할 수 있게 저장"
- 변경: "Numpad 1(앞면 고정) + Material Preview 모드에서 Before/After 동일 앵글로 촬영. 스크린샷: Ctrl+F3. 앵글 바꾸지 않기 — After도 똑같이 Numpad 1"

### shortcuts 추가

```json
{ "keys": "Numpad 1", "action": "앞면 뷰 고정 (Before/After 촬영 기준)" },
{ "keys": "Ctrl + F3", "action": "뷰포트 스크린샷 저장" }
```

### assignment.checklist 마지막 항목 추가

```
".blend 파일 저장 완료 — Week 6 Material 실습에서 이 파일을 씁니다"
```

---

## B. ShowMe 카드 명세

### 신규 registry 항목 (_registry.js)

```js
"sculpt-brushes":   { label: "Sculpt 브러시 선택 기준", icon: "🖌️", week: 5 },
"ai-prompt-design": { label: "AI 프롬프트 설계법",       icon: "✍️", week: 5 },
"ai-3d-generation": { label: "AI 3D 생성 워크플로우",    icon: "🤖", week: 5 },
```

### 신규 supplement 카드 (_supplements.json)

#### `sculpt-basics`
- **아날로지**: 점토 조각 — "마우스로 디지털 점토를 주무르는 거예요"
- **before_after**: 브러시 없이 Edit Mode로만 유기적 형태 만들기 → Sculpt Mode로 자연스럽게 표면 조각
- **confusion**: "Sculpt가 먹히지 않아요" → 폴리곤이 너무 적으면 Remesh로 늘리기
- **officialVideos**: Blender Studio - Introduction to Sculpting

#### `sculpt-brushes`
- **아날로지**: 그림 도구처럼 — "연필·지우개·블렌더를 상황마다 골라 쓰듯이"
- **판단 기준표**: Draw(올리기/파기) / Clay(쌓기) / Grab(잡아끌기) / Smooth(정리) / Crease(선긋기) / Inflate(부풀리기) / Snake Hook(뽑기)
- **before_after**: 브러시 하나로만 작업 → 상황별 브러시 선택으로 훨씬 빠른 형태 완성
- **confusion**: "어떤 브러시 써야 해요?" → 형태 잡기=Grab/Clay, 선=Crease, 볼록=Inflate, 끌어내기=Snake Hook
- **officialVideos**: Blender Studio - Brush Types

#### `ai-prompt-design`
- **아날로지**: 배달 주문 — "주소만 말하면 못 찾아요. 동, 건물명, 층수까지 말해야 해요"
- **공식**: `[형태] + [스타일] + [재질감] + "3D model"`
- **before_after**: "cute robot" → "small companion robot, spherical head, stubby arms, matte plastic finish, 3D model"
- **confusion**: "프롬프트를 길게 썼는데도 이상해요" → 추상적 단어 대신 형태를 묘사하는 구체적 명사로
- **officialVideos**: Meshy AI 공식 튜토리얼

#### `ai-3d-generation`
- **아날로지**: AI가 초벌을 잡아주는 조수 — "초안 100%가 아니라 70% 방향 확인용"
- **워크플로우**: 프롬프트 → 생성 → 비교(2개 이상) → 선택 → Import → 정리
- **before_after**: AI 결과 그대로 쓰기 → Sculpt/Edit로 다듬어서 완성도 올리기
- **confusion**: "AI가 만든 게 내 의도와 달라요" → 정상. 프롬프트 키워드 하나씩 바꿔가며 비교
- **officialVideos**: Meshy AI 공식 튜토리얼

---

## 변경하지 않는 것

- `lecture-note.md`, `slides.md`, `assignment.md` — curriculum.js가 SSOT
- MCP 실습 — curriculum.js에서 이미 제거된 상태 유지
- 기존 Step 순서·구조
- 이미 구현된 ShowMe 카드 (remesh-modifier, decimate-modifier 등)
