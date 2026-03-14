# Week 02: Blender 5.0 설치 & 기초 조작

## 📑 목차

- [학습 목표](#학습-목표)
- [영상 구성](#영상-구성-총-28분)
- [설치](#설치)
- [프리퍼런스 설정](#프리퍼런스-설정)
- [UI 구조](#ui-구조)
  - [3D Viewport](#3d-viewport-뷰포트--메인-작업-공간)
  - [Outliner](#outliner-아웃라이너--씬-목록-관리자)
  - [Properties](#properties-프로퍼티--세부-설정-패널)
  - [Timeline](#timeline-타임라인--애니메이션-시간축)
- [뷰포트 조작](#뷰포트-조작)
- [Transform 기초](#transform-기초)
- [Apply Transform & Origin](#apply-transform--origin)
  - [왜 따로 있을까? — Origin vs 3D Cursor](#-근데-왜-따로-있을까--origin과-3d-cursor가-분리된-진짜-이유)
- [Join / Separate / Bridge](#join--separate--bridge)
  - [Join (Ctrl+J)](#join-ctrlj--오브젝트-합치기)
  - [Separate (P)](#separate-p--오브젝트-분리)
  - [Bridge Edge Loops](#bridge-edge-loops--두-루프를-면으로-연결)
- [기본 도형으로 나만의 장면 만들기](#기본-도형으로-나만의-장면-만들기)
- [흔한 실수](#️-흔한-실수)
- [과제](#과제)
- [주차 체크리스트](#-주차-체크리스트)
- [참고 자료](#참고-자료)

---

## 학습 목표

- [ ] Blender 5.0을 설치하고 기본 환경 설정을 완료할 수 있다
- [ ] Blender UI 4개 영역의 역할을 설명할 수 있다
- [ ] 뷰포트를 자유롭게 회전·이동·줌 할 수 있다
- [ ] G·R·S + 축 제한으로 오브젝트를 원하는 위치에 배치할 수 있다
- [ ] Apply Transform과 Origin의 개념을 이해하고 적용할 수 있다
- [ ] Join·Separate·Bridge로 오브젝트를 합치고, 분리하고, 연결할 수 있다

---

## 영상 구성 (총 ~28분)

| # | 영상 제목 | 시간 |
|---|-----------|------|
| Seg A | 설치 & 환경설정 | 7분 |
| Seg B | 화면 구조 & 뷰포트 조작 | 10분 |
| Seg C | Transform & Apply Transform | 11분 |

---

## 설치

1. https://www.blender.org/download/ 에서 OS에 맞는 버전 다운로드
2. **Mac**: .dmg → Blender를 Applications 폴더로 드래그
3. **Windows**: .msi → Next → Install
4. 첫 실행 → Splash Screen에서 **General** 선택

> 💡 **Apple Silicon(M1·M2·M3) 사용자**: macOS Apple Silicon 버전을 받아야 합니다

---

## 프리퍼런스 설정

`Edit → Preferences` 에서 아래 항목 설정 후 **Save Preferences** 클릭

| 탭 | 설정 항목 | 값 |
|----|-----------|-----|
| System | GPU Compute | CUDA(NVIDIA) / Metal(Apple) 체크 |
| Input | Emulate Numpad | ✅ 체크 (노트북 필수) |
| Input | Emulate 3 Button Mouse | 마우스 휠 없으면 체크 |
| Interface | Resolution Scale | 고해상도 모니터는 1.2~1.5 |

---

## UI 구조

Blender를 처음 열면 4개의 주요 영역이 보입니다.
각 영역은 독립된 **Editor**이며, 좌상단 아이콘을 클릭해 언제든 다른 타입으로 바꿀 수 있습니다.

```
┌─────────────────────────────────────────────────────┐
│  Topbar  (File / Edit / Render / Window / Help)      │
├──────────────────────────────┬──────────────────────┤
│                              │  [🔍] Outliner       │
│     3D Viewport              │  ▾ Scene Collection  │
│     (작업 공간)               │    ▸ Camera          │
│                              │    ▸ Cube            │
│                              │    ▸ Light           │
│                              ├──────────────────────┤
│                              │  [🔧] Properties     │
│                              │  🖥 Scene            │
│                              │  🌍 World           │
│                              │  📐 Object          │
│                              │  ⚙ Modifier         │
│                              │  🎨 Material        │
├──────────────────────────────┴──────────────────────┤
│  [⏱] Timeline  ◀◀ ◀ ▶ ▶▶   Frame: 1   End: 250     │
└─────────────────────────────────────────────────────┘
```

---

### 3D Viewport (뷰포트) — 메인 작업 공간

> "3D 뷰포트는 Blender의 심장입니다. 모델링, 배치, 애니메이션까지 거의 모든 작업이 여기서 시작됩니다."

![Blender 3D Viewport 전체](images/viewport_overview.png)

**뷰포트 Header (상단 바)**

뷰포트 최상단 줄에는 작업 맥락을 제어하는 핵심 컨트롤이 있습니다.

```
[Object Mode ▾]  [View] [Select] [Add] [Object]     [⬚ Overlay▾] [🔵 Shading]
      ①                  ②                                 ③           ④
```

| # | 이름 | 설명 |
|---|------|------|
| ① | **Mode Selector** | Object / Edit / Sculpt 등 작업 모드 전환 (`Tab` 키로도 전환) |
| ② | **메뉴 바** | View·Select·Add·Object 등 상황별 메뉴 |
| ③ | **Overlay** | 와이어프레임, 통계, 그리드 등 표시 옵션 |
| ④ | **Viewport Shading** | Solid / Wireframe / Material / Rendered 전환 |

**뷰포트 좌측 — Tool Shelf (T 패널)**

`T` 키를 누르면 좌측에 툴 팔레트가 나타납니다.

| 아이콘 | 도구 | 단축키 |
|--------|------|--------|
| 커서 | Select Box | W |
| 이동 화살표 | Move | G |
| 회전 원 | Rotate | R |
| 크기 화살표 | Scale | S |
| 변환 통합 | Transform | — |

> 💡 실제 작업에서는 마우스를 들지 않고 단축키(G·R·S)를 더 많이 씁니다. 툴 팔레트는 입문 단계에서 확인용으로 활용하세요.

**뷰포트 우측 — Item / View / Tool 패널 (N 패널)**

`N` 키를 누르면 우측에 수치 패널이 나타납니다.

| 탭 | 내용 |
|----|------|
| **Item** | 선택된 오브젝트의 위치(Location)·회전(Rotation)·크기(Scale) 수치 표시 |
| **View** | 카메라 렌즈·클리핑 거리 설정 |
| **Tool** | 현재 선택된 툴의 세부 옵션 |

> 💡 N 패널의 **Item 탭**은 G·R·S 조작 후 정확한 수치를 확인하거나 직접 입력할 때 매우 유용합니다.

**뷰포트 우상단 — Navigation Gizmo**

![Navigation Gizmo](images/viewport_gizmo.png)

뷰포트 오른쪽 상단의 나침반 모양 기즈모입니다.

- **축 클릭** → 해당 방향 정면 뷰로 즉시 이동 (X = 측면, Y = 정면, Z = 상단)
- **가운데 격자** 클릭 → 원근(Perspective) ↔ 직교(Orthographic) 전환
- MMB 대신 **드래그**로도 뷰 회전 가능

**작업 모드 (Mode)**

`Tab` 키 또는 상단 Mode Selector로 전환합니다.

| 모드 | 용도 | 주로 쓰는 시기 |
|------|------|----------------|
| **Object Mode** | 오브젝트 배치·이동·복제 | 씬 전체 구성 |
| **Edit Mode** | 버텍스·엣지·페이스 편집 | 메시 형태 변경 |
| **Sculpt Mode** | 점토처럼 형태 조각 | 유기체 모델링 (Week 05) |

> ⚠️ 가장 흔한 실수: **Edit Mode**에서 작업해야 하는데 **Object Mode**에서 G를 눌러 오브젝트 전체가 이동되는 경우. 항상 상단 Mode 확인!

**Edit Mode 선택 모드 (1 · 2 · 3)**

Edit Mode(`Tab`)에 진입하면 상단 Header에 3가지 선택 모드 버튼이 나타납니다.

```
  [·]  [/]  [▣]
   1    2    3
```

| 키 | 모드 | 선택 단위 | 설명 |
|----|------|-----------|------|
| **1** | **Vertex** (점) | 꼭짓점 하나하나 | 가장 세밀한 조작. 점을 이동해 형태를 변형 |
| **2** | **Edge** (선) | 두 꼭짓점을 잇는 선분 | 엣지 루프 선택·슬라이드에 유용 |
| **3** | **Face** (면) | 면 하나 | 면 돌출(Extrude)·삭제 등에 사용 |

> 💡 `Shift`를 누르고 모드 키를 추가로 누르면 **복수 모드 동시 선택**도 가능합니다 (예: `1` 선택 후 `Shift+2` → Vertex + Edge 동시).

**선택 방법 정리**

| 조작 | 동작 |
|------|------|
| **클릭** | 요소 1개 선택 (기존 선택 해제) |
| **Shift + 클릭** | 추가/해제 선택 (기존 유지하며 토글) |
| **Alt + 클릭** | **루프 선택** — 연결된 요소를 한 줄로 쭉 선택 |
| **Shift + Alt + 클릭** | 루프를 **추가 선택** (기존 선택 유지하며 루프 추가) |
| **A** | 전체 선택 / 전체 해제 |
| **B** | Box Select — 드래그로 사각 영역 선택 |
| **C** | Circle Select — 브러시처럼 칠해서 선택 (휠로 크기 조절, 우클릭 종료) |
| **Ctrl + 클릭** | Shortest Path — 마지막 선택에서 클릭한 곳까지 최단 경로 선택 |
| **L** | Linked Select — 마우스 아래 연결된 덩어리 전체 선택 |

```
   Alt+클릭 예시 (Edge 모드에서)

   ┌──┬──┬──┬──┐         ┌──┬──┬──┬──┐
   │  │  │  │  │         │  ║  │  │  │
   ├──┼──┼──┼──┤   →     ├──╬══╬══╬══╡   Alt+클릭으로
   │  │  │  │  │         │  ║  │  │  │   세로 엣지 루프
   ├──┼──┼──┼──┤         ├──╬══╬══╬══╡   한 줄이 쭉 선택됨
   │  │  │  │  │         │  ║  │  │  │
   └──┴──┴──┴──┘         └──┴──┴──┴──┘
```

> 💡 **Alt+클릭 루프 선택**은 Bridge Edge Loops, Loop Cut, 부분 선택 후 Separate 등 거의 모든 Edit Mode 작업의 기본이 됩니다. 꼭 연습해 두세요!

---

### Outliner (아웃라이너) — 씬 목록 관리자

> "아웃라이너는 씬의 '레이어 목록'입니다. Photoshop의 레이어 패널과 같은 역할입니다."

![Outliner 패널](images/outliner_overview.png)

Blender를 처음 열면 기본으로 **Camera, Cube, Light** 3개의 오브젝트가 있습니다.

**아이콘으로 오브젝트 타입 파악**

| 아이콘 | 타입 |
|--------|------|
| ▲ (삼각형) | 메시 (Mesh) |
| 📷 | 카메라 |
| 💡 | 라이트 |
| 🦴 | 아마추어 (리깅용 뼈대) |
| 📦 | 컬렉션 (폴더) |

**우측 가시성 컨트롤 (클릭해서 토글)**

```
[오브젝트 이름]     👁  🖱  📷  🚫
                    ①  ②  ③  ④
```

| # | 아이콘 | 기능 |
|---|--------|------|
| ① | 👁 눈 | 뷰포트에서 보이기/숨기기 (`H` 키와 동일) |
| ② | 🖱 커서 | 뷰포트에서 선택 가능/불가 |
| ③ | 📷 카메라 | 렌더 시 포함 여부 |
| ④ | 🚫 제외 | 레이어캐스트·그림자 등 |

> 💡 **컬렉션(Collection)**을 활용하면 오브젝트를 폴더처럼 그룹화할 수 있습니다. 복잡한 씬에서 `M` 키로 컬렉션에 오브젝트를 넣어 정리하세요.

**계층(Hierarchy) 읽기**

```
▾ Scene Collection
  ▾ Collection
    ▸ Armature        ← 부모
      ▸ Body_Mesh     ← 자식 (들여쓰기로 표시)
      ▸ Head_Mesh
```

들여쓰기로 부모-자식 관계를 표시합니다. 부모를 이동하면 자식도 함께 움직입니다.

---

### Properties (프로퍼티) — 세부 설정 패널

> "Properties는 선택된 오브젝트의 모든 속성이 모인 '설정판'입니다. 탭마다 완전히 다른 내용을 담고 있습니다."

![Properties 패널 탭 목록](images/properties_tabs.png)

Properties 패널의 **왼쪽 세로 탭 목록**을 익히는 것이 핵심입니다.

**주요 탭 (상단 → 하단 순서)**

| 탭 아이콘 | 탭 이름 | 내용 | 자주 쓰는 시기 |
|-----------|---------|------|----------------|
| 📷 | **Render Properties** | 렌더 엔진, 해상도, 샘플 수 | 최종 렌더 설정 (Week 13) |
| 📤 | **Output Properties** | 저장 경로, 파일 형식 | 렌더 출력 |
| 🌍 | **World Properties** | 배경색, HDRI 환경 | 조명 설정 (Week 09) |
| 📐 | **Object Properties** | Location / Rotation / Scale 수치, 가시성 | Transform 확인 필수 |
| 🔧 | **Modifier Properties** | Subdivision, Boolean, Array 등 | 모델링 작업 (Week 03~) |
| 🔵 | **Material Properties** | 색상, 금속/비금속, 거칠기 | 재질 설정 (Week 06) |
| 📊 | **Object Data Properties** | 버텍스 그룹, UV 맵, Shape Key | 메시 세부 데이터 |

> 💡 지금 당장 가장 중요한 탭: **Object Properties (📐)** — 여기서 Scale이 (1,1,1)인지 확인합니다.

**Object Properties 탭 상세 (📐)**

![Object Properties 탭](images/properties_object.png)

```
Transform
  Location X: 0 m   Y: 0 m   Z: 0 m
  Rotation  X: 0°   Y: 0°   Z: 0°
  Scale     X: 1    Y: 1    Z: 1    ← 이 값이 1,1,1이어야 정상

Visibility
  [✅] Show in Viewports
  [✅] Show in Renders
```

> ⚠️ Scale 값이 (1,1,1)이 아니면 → `Ctrl + A → Apply All Transforms`

---

### Timeline (타임라인) — 애니메이션 시간축

> "타임라인은 '애니메이션 전용 영역'입니다. 지금은 구조만 파악하고, 자세한 내용은 Week 10에서 다룹니다."

![Timeline 패널](images/timeline_overview.png)

```
◀◀  ◀  ▶  ▶▶    Frame: [  1  ]    Start: 1   End: 250
  재생 컨트롤          현재 프레임        재생 구간
```

| 요소 | 설명 |
|------|------|
| **Playhead (파란 세로선)** | 현재 시간 위치 (드래그로 이동) |
| **▶ Play / Space** | 애니메이션 재생·정지 |
| **키프레임 마커 (노란 점)** | 해당 프레임에 저장된 오브젝트 상태 |
| **Start / End** | 애니메이션 재생 구간 (기본 1~250 프레임 = 약 10초) |

> 💡 지금 바로 써볼 것: Cube를 선택하고 `I` 키 → Location 선택 → 프레임 이동 → 다시 `I` → 재생! 키프레임의 원리를 미리 체험해보세요.

---

### 📸 스크린샷 촬영 가이드 (강의 자료용)

아래 이미지를 직접 촬영해서 `images/` 폴더에 저장하세요:

| 파일명 | 캡처 내용 | 팁 |
|--------|-----------|-----|
| `viewport_overview.png` | 3D 뷰포트 전체 (기본 Cube 씬) | Blender 기본 실행 상태 |
| `viewport_gizmo.png` | 우상단 Navigation Gizmo 클로즈업 | 줌인해서 캡처 |
| `outliner_overview.png` | Outliner 패널 (Camera, Cube, Light) | 아웃라이너 우클릭 메뉴까지 |
| `properties_tabs.png` | Properties 패널 탭 전체 목록 | 세로 탭 아이콘이 다 보이게 |
| `properties_object.png` | Object Properties 탭 열린 상태 | Scale (1,1,1) 보이게 |
| `timeline_overview.png` | Timeline 전체 (재생바 포함) | 기본 상태 |

> Mac 스크린샷: `Cmd + Shift + 4` → 드래그 캡처
> Windows: `Win + Shift + S` → 캡처 도구

---

## 뷰포트 조작

> **핵심 개념**: 뷰포트 조작 = 오브젝트가 아닌 나의 시점(카메라)을 움직이는 것

| 조작 | 방법 |
|------|------|
| 뷰 회전 | Middle Mouse Button(MMB) 드래그 |
| 뷰 이동 | Shift + MMB 드래그 |
| 줌 | 마우스 휠 |
| 정면 뷰 | Numpad **1** |
| 측면 뷰 | Numpad **3** |
| 상단 뷰 | Numpad **7** |
| 카메라 뷰 | Numpad **0** |
| 원근/직교 전환 | Numpad **5** |

### Shading 모드 (Z 키 Pie Menu)

| 모드 | 용도 |
|------|------|
| **Solid** | 기본 작업 (빠름) |
| **Wireframe** | 메시 구조 확인 |
| **Material Preview** | 재질 미리보기 |
| **Rendered** | 렌더 결과 확인 (느림) |

> 💡 Gizmo(뷰포트 오른쪽 상단 나침반)를 클릭해도 뷰를 전환할 수 있습니다

---

## Transform 기초

| 키 | 기능 | 예시 |
|----|------|------|
| **G** | 이동 (Grab) | G → 마우스 이동 → 클릭 |
| **R** | 회전 (Rotate) | R → 마우스 → 클릭 |
| **S** | 크기 (Scale) | S → 마우스 → 클릭 |

### 축 제한 패턴

```
G + X          → X축으로만 이동
G + X + 2 + Enter  → X축으로 정확히 2 이동
R + Z + 45 + Enter → Z축 기준 45도 회전
S + 0.5 + Enter    → 절반 크기로 축소
G + Shift + Z  → Z 제외(XY 평면)에서만 이동
```

**취소**: 조작 중 우클릭 또는 ESC | **되돌리기**: Ctrl + Z

---

## Apply Transform & Origin

### Apply Transform (Ctrl + A)

**왜 필요한가?**
Scale 값이 (1,1,1)이 아닌 상태에서 Modifier나 내보내기를 하면 형태 왜곡, 리깅 오류 등이 발생합니다.

**언제 해야 하나?**
→ 모디파이어 추가 전 / 리깅 시작 전 / FBX·GLB 내보내기 전

```
Ctrl + A → Apply All Transforms
```
→ Location(0,0,0) / Rotation(0,0,0) / Scale(1,1,1) 확인

### Origin 설정

**Origin(주황 점)**: 오브젝트의 기준점. 이동·회전·스케일의 중심.

```
Right-click → Set Origin
  ├─ Origin to Geometry     ← 메시 중심으로 (가장 많이 씀)
  ├─ Origin to 3D Cursor    ← 3D Cursor 위치로
  └─ Origin to Center of Mass
```

### 🤔 근데 왜 따로 있을까? — Origin과 3D Cursor가 분리된 진짜 이유

**비유: 문 경첩 vs 연필**

- **Origin = 문 경첩** — 문에 고정된 회전축. 문을 열고 닫을 때 항상 경첩을 중심으로 회전합니다.
- **3D Cursor = 연필** — 어디든 자유롭게 놓을 수 있는 표시. "여기에 새 가구 놓자" 표시하거나, "이 점을 기준으로 회전" 같은 임시 기준점으로 쓸 수 있습니다.

경첩을 떼어서 연필 자리로 옮길 수도 있지만 (`Set Origin to 3D Cursor`), 경첩 자체를 매번 옮기면 안 됩니다 — 매번 문의 회전이 달라지니까요.

**만약 둘이 합쳐져 있다면 무슨 문제가 생길까?**

1. **새 오브젝트 생성 위치를 바꿀 때마다** 기존 오브젝트의 회전 중심이 달라져 버림
2. **"저기를 기준으로 회전하고 싶다"를 표현할 수 없음** — 오브젝트와 독립적인 기준점이 필요
3. **여러 오브젝트가 하나의 공통 점을 기준으로** 회전하는 것이 불가능

**실전 예시 3가지:**

| 상황 | 쓰는 것 | 설명 |
|------|---------|------|
| "이 컵을 손잡이 위치에서 회전시키고 싶다" | Origin 이동 | Origin을 컵 아래쪽으로 → R을 누르면 그 점 기준 회전 |
| "저기 바닥 위에 새 오브젝트를 놓고 싶다" | 3D Cursor 이동 | Shift+RClick으로 Cursor 배치 → Shift+A로 추가 |
| "여러 개를 테이블 중앙 기준으로 돌리고 싶다" | 3D Cursor + Pivot | Cursor를 테이블 중앙에 → Pivot=3D Cursor → 전체 선택 후 R |

> 🔑 **핵심:** Origin은 오브젝트의 **영구적인 정체성** (= "나의 중심은 여기다")이고, 3D Cursor는 사용자의 **임시 도구** (= "여기를 기준점으로 쓰자")입니다. 이 구분이 있어야 "객체의 고유 중심"과 "작업자가 원하는 임의 중심"을 독립적으로 쓸 수 있습니다.

---

## Join / Separate / Bridge

> **핵심 개념**: 오브젝트를 합치고, 분리하고, 연결하는 3가지 기본 오퍼레이션

### 개념 개요

```
  ┌──────────────────────────────────────────────────────────┐
  │                  Object 구조 변환 3종                      │
  ├──────────────────────────────────────────────────────────┤
  │                                                          │
  │   JOIN (Ctrl+J)          여러 오브젝트 → 하나로 합치기     │
  │   ──────────────────────────────────────────              │
  │                                                          │
  │    🟦  🟩  🟥            🟦🟩🟥                            │
  │    A    B    C    →    A+B+C (하나의 오브젝트)              │
  │    (3개 오브젝트)        (1개 오브젝트, 3개 메시 덩어리)     │
  │                                                          │
  │   SEPARATE (P)          하나의 오브젝트 → 분리하기         │
  │   ──────────────────────────────────────────              │
  │                                                          │
  │    🟦🟩🟥                🟦  🟩  🟥                        │
  │    A+B+C (하나)   →    A    B    C                        │
  │    Edit Mode에서          (다시 3개 오브젝트)               │
  │    분리할 부분 선택                                        │
  │                                                          │
  │   BRIDGE (Bridge Edge Loops)  두 구멍을 면으로 연결        │
  │   ──────────────────────────────────────────              │
  │                                                          │
  │    ╭──╮      ╭──╮       ╭──╮══════╭──╮                   │
  │    │  │      │  │  →    │  │      │  │                   │
  │    ╰──╯      ╰──╯       ╰──╯══════╰──╯                   │
  │    (열린 루프) (열린 루프)   (면으로 연결됨)                 │
  │                                                          │
  └──────────────────────────────────────────────────────────┘
```

---

### Join (Ctrl+J) — 오브젝트 합치기

**사용 시기**: 여러 파트를 하나의 오브젝트로 만들고 싶을 때

```
1. Object Mode에서 합칠 오브젝트들을 Shift+클릭으로 복수 선택
2. 마지막에 선택한 것이 "Active Object" (주황 테두리)
3. Ctrl+J → Join
```

| 항목 | 설명 |
|------|------|
| **모드** | Object Mode에서만 가능 |
| **단축키** | `Ctrl + J` |
| **Active Object** | 마지막 선택된 오브젝트 → 이름/원점(Origin) 기준 |
| **결과** | 하나의 오브젝트, 여러 메시 덩어리(Loose Parts) |

> ⚠️ Join 후 Origin이 Active Object 기준으로 설정됩니다. 필요하면 `Right-click → Set Origin to Geometry`로 중심을 재설정하세요.

> 💡 Join은 "합체"이지 "합집합(Boolean Union)"이 아닙니다. 내부 면이 남아있을 수 있으므로 나중에 정리가 필요할 수 있습니다.

---

### Separate (P) — 오브젝트 분리

**사용 시기**: 하나의 오브젝트에서 특정 부분을 독립 오브젝트로 떼어내고 싶을 때

```
1. Edit Mode (Tab) 진입
2. 분리할 면/버텍스 선택
3. P 키 → Separate 메뉴
```

| 분리 방식 | 설명 | 사용 예 |
|-----------|------|---------|
| **Selection** | 현재 선택한 요소만 분리 | 특정 파트를 떼어낼 때 |
| **By Material** | 머티리얼별로 분리 | 색상별로 나눌 때 |
| **By Loose Parts** | 연결되지 않은 덩어리별 분리 | Join 후 다시 되돌릴 때 |

```
          ┌─────── Separate (P) ───────┐
          │                            │
     Selection      By Material     By Loose Parts
     (선택 기준)    (재질 기준)      (연결 기준)
          │              │              │
     선택한 면만      재질A → Obj1    덩어리1 → Obj1
     새 오브젝트로    재질B → Obj2    덩어리2 → Obj2
                     재질C → Obj3    덩어리3 → Obj3
```

> 💡 **By Loose Parts**는 Join(Ctrl+J)의 역연산입니다. Join으로 합쳤던 것을 다시 분리할 때 유용합니다.

---

### Bridge Edge Loops — 두 루프를 면으로 연결

**사용 시기**: 두 개의 열린 엣지 루프 사이를 면으로 채우고 싶을 때 (팔-몸통, 목-머리 연결 등)

```
1. 두 파트가 같은 오브젝트여야 합니다 (필요하면 Ctrl+J로 먼저 합치기)
2. Edit Mode → Edge 모드 (2)
3. 연결할 두 Edge Loop를 Alt+클릭으로 각각 선택 (Shift+Alt+클릭)
4. Edge 메뉴 → Bridge Edge Loops (또는 Ctrl+E → Bridge Edge Loops)
```

```
   Bridge 적용 전                    Bridge 적용 후
   ─────────────                    ─────────────

       ╭───╮                           ╭───╮
       │   │  ← Edge Loop 1           │   │
       ╰─○─╯                          ╰─┬─╯
                                        │ ← 자동 생성된 면
         (빈 공간)                       │
                                        │
       ╭─○─╮                           ╭─┴─╮
       │   │  ← Edge Loop 2           │   │
       ╰───╯                           ╰───╯
```

| 항목 | 설명 |
|------|------|
| **필수 조건** | 두 루프가 **같은 오브젝트** 안에 있어야 함 |
| **루프 조건** | 두 루프의 **버텍스 수가 같으면** 가장 깔끔 |
| **옵션** | Segments(중간 분할 수), Twist(꼬임 보정) 등 |
| **대안** | 수동으로 Face(F)를 하나씩 만드는 것보다 훨씬 빠름 |

> ⚠️ Bridge가 안 될 때 체크리스트:
> 1. 두 루프가 같은 오브젝트인가? → 아니면 `Ctrl+J`로 합치기
> 2. Edge Loop가 제대로 선택되었는가? → `Alt+클릭`으로 루프 선택
> 3. 열린 루프인가? → 닫힌 면이 있으면 삭제 후 시도

---

### 기본 도형으로 나만의 장면 만들기

기본 도형(Cube, Sphere, Cylinder, Cone, Torus 등)을 **3개 이상** 조합하여 자유롭게 장면을 구성해 봅니다.

**예시 아이디어** (택 1 또는 자유 주제)

| 아이디어 | 사용 도형 예시 | 핵심 조작 |
|----------|----------------|-----------|
| 눈사람 / 캐릭터 | Sphere × 3 + Cylinder(모자) + Cone(코) | G(배치) · S(크기 비율) |
| 탁자 + 의자 세트 | Cube(상판·좌석) + Cylinder(다리) | G·S + 축 제한 (S+Z 등) |
| 도시 풍경 | Cube 여러 개(건물) + Plane(바닥) | G·R·S + 수치 입력 |
| 나무 / 식물 | Cylinder(줄기) + Sphere(잎) + Cone | S 축별 비율 조절 |
| 자유 추상 조형물 | 아무 도형 조합 | 다양한 Transform 시도 |

**진행 순서**

```
Step 1: Shift+A → Mesh 에서 도형 3개 이상 추가
Step 2: G·R·S + 축 제한으로 원하는 위치·크기·각도에 배치
Step 3: 완성 후 Ctrl+A → Apply All Transforms
Step 4: 여유가 되면 Ctrl+J로 합치기, P로 분리하기도 시도
```

> 💡 정답은 없습니다! G·R·S 조작과 축 제한에 익숙해지는 것이 목표입니다. 다양한 도형을 추가하고 Transform을 반복 연습해 보세요.

---

## ⚠️ 흔한 실수

| 실수 | 원인 | 해결 |
|------|------|------|
| Numpad 키가 안 됨 | 노트북 Numpad 없음 | Preferences → Emulate Numpad 체크 |
| 뷰 회전이 안 됨 | MMB 없음 | Emulate 3 Button Mouse 체크 |
| Modifier 적용 시 형태 왜곡 | Apply Transform 안 함 | Ctrl+A → Apply All Transforms |
| 회전 중심이 이상함 | Origin 위치 문제 | Set Origin to Geometry |

---

## 과제

- **제출:** Discord #week02-assignment 채널
- **내용:**
  - 1장: 기본 도형 **3개 이상**을 G·R·S로 조합하여 만든 캐릭터·장면·조형물 스크린샷
  - 1장: Properties에서 Scale이 (1,1,1)로 Apply된 상태 확인 스크린샷
  - (선택) 간단한 설명 한 줄 — 무엇을 만들었는지
- **기한:** 다음 수업 전까지

## 📋 주차 체크리스트

- [ ] Blender 5.0 설치 + GPU 설정 확인
- [ ] Emulate Numpad 설정 (노트북)
- [ ] UI 4개 영역 위치 파악
- [ ] 뷰포트 회전·이동·줌 자유롭게 가능
- [ ] G·R·S + 축 제한 조작 가능
- [ ] Ctrl+A Apply Transform 습관화
- [ ] Join(Ctrl+J), Separate(P), Bridge Edge Loops 사용 가능

## 참고 자료

- [Blender 단축키 모음](../../resources/blender-shortcuts.md)
- Blender Guru 2026 Donut Part 1: https://www.youtube.com/watch?v=-tbSCMbJA6o
- 차녹 블렌더 기초: https://www.youtube.com/watch?v=gVteZaQGry0
- Ryan King Art (Quick Start Guides): https://www.youtube.com/@RyanKingArt
