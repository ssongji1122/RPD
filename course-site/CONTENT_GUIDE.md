# RPD Course Site — Content Guide

> **목적**: 15주 커리큘럼 데이터를 누가 작성해도 일관된 품질이 나오도록 하는 규칙 문서.  
> **적용 파일**: `course-site/data/curriculum.js`

---

## 1. 전체 철학

**토스가 금융을 쉽게 만든 것처럼, 우리는 Blender와 AI를 쉽게 만든다.**

- 학생은 Blender 전문가가 아니다. 처음 보는 사람이 읽는다고 가정하고 쓴다.
- 설명하지 말고 비유한다. "Extrude는 메쉬를 돌출시키는 기능입니다" ❌ → "점토를 손으로 당기는 것처럼 면을 뽑아내요" ✅
- 없어도 이해되는 말은 뺀다.
- 학생이 막혔을 때 읽는다고 생각하고 쓴다. 긴 문장은 읽지 않는다.

---

## 2. 언어 가이드 (토스 스타일)

### 말투
- **~해요 / ~이에요** 체 사용. (~합니다 ❌)
- 주어를 생략한다. "학생은 이렇게 합니다" ❌ → "이렇게 하면 돼요" ✅
- 먼저 결론, 그 다음 이유. "왜냐하면 ~ 그래서 ~" ❌ → "~ 거예요. 왜냐면 ~" ✅

### 금지 표현
| 금지 | 대체 |
|---|---|
| ~할 수 있습니다 | ~할 수 있어요 |
| ~하도록 합니다 | ~하세요 |
| ~를 이해했다 | ~가 됐다 |
| 중요합니다 | (그냥 설명) |
| 매우 / 굉장히 | (없애거나 구체적 수치로) |
| 학생이 / 사용자가 | (주어 생략) |

### 문장 길이
- `copy` 필드: 2문장 이내. 1문장이면 더 좋음.
- `goal` / `done` 항목: 한 줄 15자 이내가 이상적.
- `tasks` label: 동사로 시작 ("확인하기", "눌러보기", "바꿔보기")

---

## 3. 비유 작성 규칙

비유는 **학생이 이미 경험한 것**에서 가져온다.

### 좋은 비유 소스
- 앱/인터넷: 구글 지도, 카카오맵, 유튜브, 인스타그램
- 일상 물건: 점토, 레고, 종이 접기, 문방구 도구
- 신체 감각: 잡아당기기, 두드리기, 펴기, 누르기
- 요리/제작: 반죽하기, 자르기, 붙이기

### 비유 패턴 (복붙 가능)
```
[Blender 개념]은 [일상 경험]과 같아요. [한 줄 보충 설명].
```

**예시**
- Extrude → "점토를 손으로 당기는 것처럼 면을 뽑아내요."
- Loop Cut → "케이크를 칼로 자르듯 메쉬에 선을 추가해요."
- Mirror Modifier → "거울 앞에서 한쪽을 바꾸면 반대쪽이 자동으로 따라오는 거예요."
- Subdivision → "스케치를 더 세밀하게 다시 그리는 것처럼, 메쉬를 더 부드럽게 나눠요."
- UV Unwrap → "종이 박스를 펼쳐서 평평하게 만드는 것처럼 3D 메쉬를 2D로 펼쳐요."
- HDRI 조명 → "360도 파노라마 사진이 전구 역할을 해요."
- 키프레임 → "A 위치를 사진 찍고, 다른 프레임에서 B 위치를 찍으면 둘 사이가 자동으로 움직여요."
- Armature → "인형에 철사 뼈대를 넣는 것처럼, 메쉬 안에 본(Bone)을 만들어요."
- Weight Paint → "뼈대가 피부를 얼마나 잡아끄는지 색으로 칠하는 거예요."

### 비유 쓰면 안 되는 경우
- 이미 직관적인 기능 ("저장하기", "파일 열기" 등)
- 코드/수식 설명 (비유보다 그냥 정확하게 설명)

---

## 4. 데이터 스키마 (curriculum.js)

각 week 객체의 필드별 작성 기준:

```js
{
  week: 3,                    // 숫자
  status: "upcoming",         // done | active | upcoming
  title: "기초 모델링 1",      // 핵심 키워드만. 15자 이내.
  subtitle: "선택 · Mirror", // 이번 주 주요 개념 나열. 짧게.
  summary: "...",             // 사용 안 함 (index.html에 노출 안 됨)
  duration: "~3시간",         // 대략적인 소요 시간
  topics: [],                 // 이번 주 배우는 것 목록. 4~6개.
  steps: [],                  // 아래 Step 규칙 참고
  shortcuts: [],              // (선택) 이번 주 핵심 단축키
  explore: [],                // (선택) 심화 과제
  assignment: {},             // 과제 정보
  mistakes: [],               // 자주 막히는 지점
  docs: [],                   // 공식 문서 링크
}
```

### Step 규칙

```js
{
  title: "화면 조작",       // 명사형. 10자 이내.
  copy: "...",              // ★ 비유 포함 2문장 이내. 핵심 규칙.
  goal: [],                 // 이 단계에서 배울 것. 2~3개. 명사/동사형.
  done: [],                 // 완료 기준. "~가 됐다" 또는 "~할 수 있다". 2~3개.
  tasks: [                  // 실제 체크리스트 항목
    {
      id: "w3-t1",          // 규칙: w{주차}-t{번호}
      label: "...",         // 동사로 시작. "Tab으로 Edit Mode 진입"
      detail: "...",        // 힌트/단축키. 없으면 "" 비워둠.
    }
  ]
}
```

### Step 수 기준
| 주차 유형 | Step 수 |
|---|---|
| 기술 중심 주차 (Modifier, UV 등) | 3~5개 |
| 발표/시험 주차 | 1~2개 |
| AI tool 주차 | 2~3개 |

### Task 수 기준
- Step당 Task: 2~5개
- 너무 많으면 Task를 새 Step으로 분리

---

## 5. Mistakes 작성 규칙

실제로 수업 중 학생이 막히는 상황을 "증상 → 해결" 형식으로.

```
"증상이 이래요 → 이렇게 하세요." 형식
```

**Good**
```
"새 박스가 이상한 곳에 생겼어요 → 3D Cursor가 이동한 거예요. Shift+C로 원점으로 돌려놓으세요."
```

**Bad**
```
"3D Cursor 오류 → Shift+C"  (증상 설명 없음)
"3D Cursor 위치를 모르고 새 오브젝트를 만들었을 경우 Shift+C를 통해 초기화할 수 있습니다."  (너무 딱딱함)
```

---

## 6. 주차별 작성 체크리스트

새 주차 데이터 작성 시 확인:

```
[ ] title이 15자 이내인가?
[ ] 각 step copy에 비유 또는 맥락이 있는가?
[ ] copy가 2문장 이내인가?
[ ] done 항목이 "~됐다 / ~할 수 있다" 형식인가?
[ ] task label이 동사로 시작하는가?
[ ] task id가 w{N}-t{번호} 형식인가?
[ ] mistakes가 "증상 → 해결" 형식인가?
[ ] docs URL이 유효한 Blender 공식 문서인가?
```

---

## 7. 주차별 핵심 비유 (빠른 참조)

| 주차 | 핵심 개념 | 비유 방향 |
|---|---|---|
| 1 | Blender 설치, 컨셉 | — |
| 2 | 인터페이스, G/R/S, Extrude | 구글 지도, G/R/S 세 글자, 점토 |
| 3 | Vertex/Edge/Face 선택, Mirror | 레고 조각 고르기, 거울 |
| 4 | Subdivision, Array, Solidify | 스케치 세밀화, 도장 찍기, 두께 주기 |
| 5 | AI 3D 생성, Sculpt | AI가 초안 만들고 내가 다듬기 |
| 6 | Material, Shader | 색/재질 페인팅 |
| 7 | UV Unwrap, AI Texture | 종이 박스 펼치기 |
| 8 | 중간고사 | — |
| 9 | Lighting, HDRI | 사진 스튜디오 조명 세팅 |
| 10 | Animation, Keyframe | 사진 두 장 → 그 사이를 자동으로 이어줌 |
| 11 | Rigging, Armature | 철사 뼈대 넣은 인형 |
| 12 | Mixamo 자동 리깅 | AI가 리깅을 대신 해줌 |
| 13 | Cycles/EEVEE, 렌더링 | 사진 인화 퀄리티 vs 즉석 미리보기 |
| 14 | 최종 프로젝트 | — |
| 15 | 기말 발표 | — |

---

## 8. 빠른 템플릿 (새 주차 추가 시 복붙)

```js
{
  week: N,
  status: "upcoming",
  title: "제목",
  subtitle: "개념1 · 개념2 · 개념3",
  summary: "",
  duration: "~3시간",
  topics: ["개념1", "개념2", "개념3", "개념4"],
  steps: [
    {
      title: "단계 제목",
      copy: "[비유 포함 1~2문장]",
      goal: ["배울 것 1", "배울 것 2"],
      done: ["완료 기준 1 — ~됐다", "완료 기준 2 — ~할 수 있다"],
      tasks: [
        { id: "wN-t1", label: "동사로 시작하는 Task", detail: "힌트" },
        { id: "wN-t2", label: "동사로 시작하는 Task", detail: "" },
      ],
    },
  ],
  shortcuts: [
    { keys: "단축키", action: "기능 설명" },
  ],
  explore: [
    { title: "심화 도전 제목", hint: "어떻게 할지 한 줄 힌트" },
  ],
  assignment: {
    title: "과제 이름",
    description: "과제 설명. 2문장 이내.",
    checklist: ["제출 항목 1", "제출 항목 2"],
  },
  mistakes: [
    "증상이 이래요 → 이렇게 하세요.",
  ],
  docs: [
    { title: "문서 제목", url: "https://docs.blender.org/..." },
  ],
},
```

---

## 9. Admin 페이지 사용법

### 서버 실행

```bash
cd /Users/ssongji/Developer/Workspace/RPD

# 기본 (인증 없음, 로컬 개발용)
python3 tools/admin-server.py

# 인증 모드 (외부 접속 시)
ADMIN_KEY=비밀번호 python3 tools/admin-server.py

# Notion 동기화 포함
NOTION_TOKEN=ntn_xxxxx python3 tools/admin-server.py

# 전부 켜기
ADMIN_KEY=비밀번호 NOTION_TOKEN=ntn_xxxxx python3 tools/admin-server.py
```

접속: **http://localhost:8765/admin.html**

### 기본 편집 흐름

1. 좌측 사이드바에서 주차를 클릭
2. 우측 편집 영역에서 텍스트 수정
3. 상단 **💾 저장** 버튼 클릭 (또는 `Ctrl/Cmd+S`)
4. "저장 완료" 토스트가 뜨면 성공

> 저장하면 `curriculum.js`가 즉시 업데이트됩니다.
> `week.html?week=N`을 새로고침하면 변경사항이 바로 반영됩니다.

### 주차 상태 변경

상단의 "상태" 드롭다운에서 변경 → 저장:

| 상태 | 의미 | index.html 배지 |
|------|------|-----------------|
| `done` | 완료된 주차 | 🟢 녹색 |
| `active` | 이번 주 진행 중 | 🔵 파란색 |
| `upcoming` | 아직 안 한 주차 | ⚪ 회색 |

### 이미지 업로드

각 Step의 "📷 업로드" 버튼 → 파일 선택 → 자동 업로드
저장 위치: `course-site/assets/images/week-NN/step-N.png`

### 미리보기

상단 "미리보기 ↗" 버튼 → 학생용 페이지(`week.html`)가 새 탭에서 열림

---

## 10. 콘텐츠 워크플로우

### 큰 단위 수정 (새 주차 콘텐츠 작성)

```
Claude Code에서 md 파일 작성/수정
    ↓
curriculum.js에 반영 (Claude Code가 직접 편집)
    ↓
Admin 페이지에서 미세 조정
    ↓
📤 Notion에 푸시 (선택)
```

### 소규모 수정 (오타, 문구 변경)

```
Admin 페이지에서 직접 수정 → 저장
    ↓
📤 Notion에 푸시 (선택)
```

### Notion에서 수정한 내용 가져오기

```
Notion에서 내용 수정 (교수자가 직접)
    ↓
Admin 페이지에서 📥 Notion 버튼 클릭
    ↓
변경사항 diff 확인 → "적용" 선택
    ↓
💾 저장 버튼으로 curriculum.js에 확정
```

### Notion 동기화 주의사항

- **📤 Push (Admin → Notion)**: Notion 페이지의 기존 내용을 **모두 교체**합니다. Notion에서 직접 꾸민 포맷(색상, 콜아웃 등)은 유실될 수 있으므로, 내용이 확정된 후에만 Push하세요.
- **📥 Pull (Notion → Admin)**: 비파괴적입니다. 변경사항을 미리보기로 보여주고, 교수자가 확인 후에만 적용됩니다. "저장" 버튼을 눌러야 최종 반영됩니다.
- Notion 토큰이 없으면 동기화 버튼이 표시되지 않습니다.

### Notion 토큰 설정

1. https://www.notion.so/my-integrations 에서 Internal Integration 생성
2. RPD 워크스페이스의 "주차별 강의자료 원본" 페이지에 Integration 연결
3. 토큰을 `NOTION_TOKEN` 환경변수로 전달

---

## 11. 파일 구조 참고

```
course-site/
├── index.html          # 메인 페이지 (15주차 카드 그리드)
├── week.html           # 주차별 상세 페이지 (?week=N)
├── admin.html          # 관리자 편집 페이지
├── data/
│   └── curriculum.js   # ★ 단일 소스 오브 트루스
├── assets/
│   ├── tokens.css      # 공통 디자인 토큰
│   └── images/         # 스텝별 스크린샷
│       ├── week-03/
│       └── week-04/
tools/
├── admin-server.py     # Admin 서버 (Python stdlib)
└── notion-mapping.json # Week ↔ Notion 페이지 ID 매핑
```
