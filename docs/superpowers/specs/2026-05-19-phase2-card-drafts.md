# Phase 2 카드 콘텐츠 초안 — 8개 백로그

**날짜:** 2026-05-19
**대상:** "ShowMe 신규 카드 보강 계획" Notion page (32754d65-4971-81fc-b832-f8cbb3388e66) 백로그
**상태:** Draft — 사용자 검수 대기

---

## 검수 기준

각 카드 4가지 영역을 자체 점검 후 사용자가 OK 주시면 Notion 푸시:
1. **비유 (concept_md)**: 학생이 즉시 그림이 그려지는가?
2. **사용 시점 (usage_md)**: 어떤 작업 중에 이 도구를 떠올려야 하나?
3. **흔한 실수 (pitfall_md)**: 실제로 학생이 막히는 지점인가?
4. **절차 (steps_json)**: Blender 5.0 단축키·메뉴 정확한가? `5.0` 명시.

본문 톤은 Week 03 페이지의 "레고 블록 + 사포 + 필름 필터" 비유 패밀리를 유지.

---

## P0 카드 (5개)

### 1. collection-outliner (이미 Notion에 row 존재 — UPDATE)

| 필드 | 값 |
|---|---|
| `card_id` | `collection-outliner` |
| `label` | Collection 과 Outliner 이해 |
| `icon` | folder-tree |
| `category` | `object` |
| `week` | `["3"]` |
| `priority` | `P0` |
| `status` | `published` |
| `blender_version` | `5.0` |
| `official_docs` | https://docs.blender.org/manual/en/latest/scene_layout/collections/index.html |
| `widget_id` | (비움) |

**concept_md:**
```
Collection은 **폴더**처럼 오브젝트를 묶는 단위예요. Outliner는 그 폴더 구조를 보여주는 트리.

로봇처럼 파츠가 많은 모델은 머리/몸통/팔/다리를 Collection으로 분리하면 가시성, 선택 잠금, 일괄 조작이 한결 쉬워져요. 책상 위에 부품을 통 안에 나눠 담는 것과 같아요.
```

**usage_md:**
```
파츠 수가 많아질 때, 좌우 대칭 작업 중 한쪽만 숨기고 싶을 때, 렌더에서 일부만 제외하고 싶을 때.
```

**pitfall_md:**
```
Outliner 옆 두 아이콘은 역할이 달라요. **눈 아이콘 = 뷰포트 가시성**, **모니터(카메라) 아이콘 = 렌더 가시성**. 렌더에서만 사라지는 파츠가 있다면 모니터 아이콘이 꺼져 있는 거예요.
```

**steps_json:**
```json
{
  "blender_version": "5.0",
  "platform_note": null,
  "steps": [
    {"n": 1, "action": "Outliner 빈 공간 우클릭 → New Collection", "hotkey": null, "menu": "Outliner > New Collection", "screenshot": null, "note": null},
    {"n": 2, "action": "오브젝트 선택 후 Collection으로 이동", "hotkey": "M", "menu": "Move to Collection", "screenshot": null, "note": null},
    {"n": 3, "action": "뷰포트에서 Collection 숨기기/보이기", "hotkey": null, "menu": "눈 아이콘 클릭", "screenshot": null, "note": "H로도 토글 가능"},
    {"n": 4, "action": "Collection 선택 잠금", "hotkey": null, "menu": "화살표(필터) 아이콘 클릭", "screenshot": null, "note": "실수로 움직이는 것 방지"}
  ]
}
```

---

### 2. modifier-stack-order

| 필드 | 값 |
|---|---|
| `card_id` | `modifier-stack-order` |
| `label` | Modifier Stack 순서 |
| `icon` | layers |
| `category` | `modifier` |
| `week` | `["3"]` |
| `priority` | `P0` |
| `status` | `draft` |
| `blender_version` | `5.0` |
| `official_docs` | https://docs.blender.org/manual/en/latest/modeling/modifiers/introduction.html#the-modifier-stack |
| `widget_id` | (비움 — 위젯은 Phase 2.5에서) |

**concept_md:**
```
Modifier는 **요리 레시피**처럼 위에서 아래로 순서대로 계산돼요. **같은 재료라도 넣는 순서가 다르면 결과가 달라져요.**

가장 안전한 시작 순서는 **Mirror → Boolean → Subdivision Surface → Bevel → Weighted Normal**. Mirror로 좌우 대칭을 먼저 잡고, Boolean으로 구멍을 뚫고, 마지막에 Subdivision으로 부드럽게 만드는 흐름이에요.
```

**usage_md:**
```
여러 Modifier를 같이 쓸 때 결과가 의도와 다르게 보이면 가장 먼저 순서를 점검해요. Stack 핸들(::)을 드래그하거나 화살표 아이콘으로 위/아래로 옮길 수 있어요.
```

**pitfall_md:**
```
**Subdivision Surface를 먼저 넣고 Boolean을 하면** 곡면이 깨져서 결과가 지저분해져요. Subdivision은 거의 항상 마지막 또는 끝에서 두 번째로 두는 게 안전해요. Weighted Normal은 Bevel 이후에 와야 음영 정리가 의도대로 됩니다.
```

**steps_json:**
```json
{
  "blender_version": "5.0",
  "platform_note": null,
  "steps": [
    {"n": 1, "action": "Properties 패널 > 렌치 아이콘(Modifier Properties) 열기", "hotkey": null, "menu": "Properties > 🔧", "screenshot": null, "note": null},
    {"n": 2, "action": "Modifier 항목 좌측의 핸들(::) 잡기", "hotkey": null, "menu": null, "screenshot": null, "note": "드래그해서 위/아래로 이동"},
    {"n": 3, "action": "메뉴에서 Move Up / Move Down 선택", "hotkey": null, "menu": "Modifier 우상단 ▾ > Move Up/Down", "screenshot": null, "note": null},
    {"n": 4, "action": "권장 순서: Mirror → Boolean → Subdivision → Bevel → Weighted Normal", "hotkey": null, "menu": null, "screenshot": null, "note": "Apply 타이밍은 가장 마지막"}
  ]
}
```

---

### 3. shade-smooth-auto-smooth

| 필드 | 값 |
|---|---|
| `card_id` | `shade-smooth-auto-smooth` |
| `label` | Shade Smooth & Auto Smooth |
| `icon` | sparkles |
| `category` | `modeling` |
| `week` | `["3", "4"]` |
| `priority` | `P0` |
| `status` | `draft` |
| `blender_version` | `5.0` |
| `official_docs` | https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/normals.html#shade-smooth-flat |

**concept_md:**
```
같은 메쉬도 **빛이 부드럽게 흐르는지 / 면마다 뚝뚝 끊기는지** 셰이딩 모드로 바뀌어요. **Flat**은 모든 면을 각진 그대로, **Shade Smooth**는 전체를 부드럽게 보간해요.

**Auto Smooth by Angle**은 절충안 — 각도가 작은 모서리는 부드럽게, 큰 모서리(예: 30° 초과)는 날카롭게 유지해요. 로봇처럼 모서리와 곡면이 섞인 모델에 가장 자주 써요.
```

**usage_md:**
```
원기둥·구·캐릭터 등 부드러워야 할 모델에는 Shade Smooth. 로봇·도구처럼 일부 모서리가 살아야 하는 모델에는 Auto Smooth by Angle (30~45°).
```

**pitfall_md:**
```
Shade Smooth만 켜면 **모서리까지 다 뭉개져요.** Auto Smooth 각도가 너무 작으면(예: 10°) 부드러워야 할 곳도 끊겨 보이고, 너무 크면(예: 80°) 뭉개져요. **30° 근처에서 시작**해서 모델 보면서 조정하세요. Blender 5.0에서는 Object Data Properties → Normals → Auto Smooth 토글로 들어가요.
```

**steps_json:**
```json
{
  "blender_version": "5.0",
  "platform_note": null,
  "steps": [
    {"n": 1, "action": "Object Mode에서 메쉬 우클릭", "hotkey": null, "menu": "Object Context Menu", "screenshot": null, "note": null},
    {"n": 2, "action": "Shade Smooth 선택", "hotkey": null, "menu": "Shade Smooth", "screenshot": null, "note": "전체 매끄럽게"},
    {"n": 3, "action": "Properties > Object Data (역삼각형) > Normals", "hotkey": null, "menu": "Object Data Properties", "screenshot": null, "note": "Blender 5.0 위치"},
    {"n": 4, "action": "Auto Smooth 토글 → Angle 입력", "hotkey": null, "menu": null, "screenshot": null, "note": "보통 30°로 시작"}
  ]
}
```

---

### 4. merge-by-distance

| 필드 | 값 |
|---|---|
| `card_id` | `merge-by-distance` |
| `label` | Merge by Distance (겹친 버텍스 정리) |
| `icon` | combine |
| `category` | `edit-mode` |
| `week` | `["3", "4"]` |
| `priority` | `P0` |
| `status` | `draft` |
| `blender_version` | `5.0` |
| `official_docs` | https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/merge.html#by-distance |

**concept_md:**
```
Boolean이나 Extrude를 잘못 누르면 **같은 자리에 버텍스가 두 개씩 쌓여요**. 눈에는 멀쩡해 보여도 메쉬가 끊어진 상태라 Subdivision이 깨지거나 Smooth가 이상하게 적용돼요.

**Merge by Distance**는 설정한 거리 안에 있는 버텍스를 하나로 합쳐주는 청소 도구예요. 빨래 짤 때 물기 빼듯, 메쉬에서 중복 정보를 짜내는 작업.
```

**usage_md:**
```
Boolean 직후, Mirror에 Clipping 없이 작업한 직후, 외부 메쉬(AI 생성·STL import)를 받았을 때 가장 먼저 돌려요. Subdivision이 갑자기 이상해지면 십중팔구 중복 버텍스가 원인.
```

**pitfall_md:**
```
거리가 너무 크면(예: 1m) **분리되어 있어야 할 버텍스까지 합쳐져** 메쉬가 뭉개져요. 기본값 **0.0001m**부터 시작하고, 안 합쳐지면 단계적으로 키워요. 작업 후에는 합쳐진 개수가 화면 하단에 표시돼요 — "Removed 12 vertices" 같은 메시지.
```

**steps_json:**
```json
{
  "blender_version": "5.0",
  "platform_note": null,
  "steps": [
    {"n": 1, "action": "Edit Mode 진입", "hotkey": "Tab", "menu": null, "screenshot": null, "note": null},
    {"n": 2, "action": "전체 선택", "hotkey": "A", "menu": null, "screenshot": null, "note": null},
    {"n": 3, "action": "Merge 메뉴 열기", "hotkey": "M", "menu": "Mesh > Merge", "screenshot": null, "note": null},
    {"n": 4, "action": "By Distance 선택", "hotkey": null, "menu": "By Distance", "screenshot": null, "note": null},
    {"n": 5, "action": "좌하단 패널에서 거리 조정", "hotkey": null, "menu": "Merge Distance", "screenshot": null, "note": "0.0001m → 0.001m 순으로"}
  ]
}
```

---

### 5. bridge-edge-loops

| 필드 | 값 |
|---|---|
| `card_id` | `bridge-edge-loops` |
| `label` | Bridge Edge Loops (열린 루프 연결) |
| `icon` | git-merge |
| `category` | `edit-mode` |
| `week` | `["4"]` |
| `priority` | `P0` |
| `status` | `draft` |
| `blender_version` | `5.0` |
| `official_docs` | https://docs.blender.org/manual/en/latest/modeling/meshes/editing/edge/bridge_edge_loops.html |

**concept_md:**
```
모자와 머리를 따로 만들었는데 둘이 안 붙어 있다면 **두 열린 루프를 다리(bridge)로 연결**해야 해요. Bridge Edge Loops는 두 Edge 루프 사이에 면을 자동으로 만들어줘요.

휴지심 두 개를 마주 보게 놓고 사이에 종이를 감아 붙이는 것과 비슷해요. 빈 공간을 면으로 메워주는 도구.
```

**usage_md:**
```
파츠를 따로 만든 뒤 하나의 메쉬로 합쳐야 할 때, 구멍(Delete Face로 만든)을 다른 메쉬 루프와 연결할 때, 캐릭터 모자·후드·옷깃처럼 두 표면을 잇는 형태를 만들 때.
```

**pitfall_md:**
```
**두 루프의 버텍스 개수가 다르면** 결과 토폴로지가 지저분해져요. 비슷한 개수로 맞춘 뒤 Bridge 하거나, 한쪽을 Loop Cut으로 분할해 개수를 맞춰요. **두 루프가 같은 메쉬에 있어야** 동작해요 — 다른 오브젝트면 먼저 `Ctrl + J`로 Join.
```

**steps_json:**
```json
{
  "blender_version": "5.0",
  "platform_note": null,
  "steps": [
    {"n": 1, "action": "두 루프가 다른 오브젝트면 Join", "hotkey": "Ctrl + J", "menu": null, "screenshot": null, "note": "Object Mode에서"},
    {"n": 2, "action": "Edit Mode 진입 + Edge 모드", "hotkey": "Tab → 2", "menu": null, "screenshot": null, "note": null},
    {"n": 3, "action": "두 루프 선택 (Alt+클릭으로 루프 단위 선택, Shift+Alt+클릭으로 추가)", "hotkey": null, "menu": null, "screenshot": null, "note": null},
    {"n": 4, "action": "Bridge Edge Loops 실행", "hotkey": null, "menu": "Edge > Bridge Edge Loops", "screenshot": null, "note": null}
  ]
}
```

---

## P1 카드 (3개)

### 6. duplicate-vs-linked-duplicate

| 필드 | 값 |
|---|---|
| `card_id` | `duplicate-vs-linked-duplicate` |
| `label` | Duplicate vs Linked Duplicate |
| `icon` | copy-plus |
| `category` | `object` |
| `week` | `["4"]` |
| `priority` | `P1` |
| `status` | `draft` |
| `blender_version` | `5.0` |
| `official_docs` | https://docs.blender.org/manual/en/latest/scene_layout/object/editing/duplicate.html |

**concept_md:**
```
**Duplicate (Shift+D)**는 완전 복사 — 원본과 무관한 별개 오브젝트가 생겨요. 한쪽을 수정해도 다른 쪽엔 영향 없어요.

**Linked Duplicate (Alt+D)**는 **같은 메쉬 데이터를 공유하는 인스턴스**. 한쪽 Edit Mode에서 수정하면 모든 복제본이 동시에 변해요. 한 손가락을 만들면 다섯 손가락이 동시에 갱신되는 식.
```

**usage_md:**
```
같은 모양 부품을 여러 개 배치하면서 **나중에 한 번에 수정**하고 싶으면 Linked Duplicate. 복사 후 **개별적으로 다르게** 변형할 거면 일반 Duplicate.
```

**pitfall_md:**
```
Linked Duplicate를 만든 뒤 한쪽을 따로 수정하고 싶어졌다면 `U > Object & Data`로 메쉬 데이터 연결을 끊을 수 있어요. 거꾸로 Linked로 만들었는지 알려면 Outliner에서 오브젝트 아래 메쉬 아이콘 옆 숫자(예: `2`)를 확인하세요.
```

**steps_json:**
```json
{
  "blender_version": "5.0",
  "platform_note": null,
  "steps": [
    {"n": 1, "action": "오브젝트 선택", "hotkey": null, "menu": null, "screenshot": null, "note": null},
    {"n": 2, "action": "일반 복제 (독립)", "hotkey": "Shift + D", "menu": "Object > Duplicate Objects", "screenshot": null, "note": null},
    {"n": 3, "action": "연결 복제 (메쉬 공유)", "hotkey": "Alt + D", "menu": "Object > Duplicate Linked", "screenshot": null, "note": null},
    {"n": 4, "action": "연결 끊기 (필요 시)", "hotkey": "U", "menu": "Object > Make Single User > Object & Data", "screenshot": null, "note": null}
  ]
}
```

---

### 7. face-orientation-normals

| 필드 | 값 |
|---|---|
| `card_id` | `face-orientation-normals` |
| `label` | Face Orientation & Normals |
| `icon` | flip-horizontal-2 |
| `category` | `edit-mode` |
| `week` | `["3", "4", "6"]` |
| `priority` | `P1` |
| `status` | `draft` |
| `blender_version` | `5.0` |
| `official_docs` | https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/normals.html |

**concept_md:**
```
모든 면에는 **앞면/뒷면 방향(Normal)**이 있어요. Blender는 앞면을 파란색, 뒷면을 빨간색으로 표시할 수 있어요 — **Viewport Overlays > Face Orientation**.

쿠키 모양 틀이 뒤집힌 채로 반죽을 누르면 모양이 거꾸로 나오죠? Normal이 뒤집힌 면도 마찬가지로 셰이딩·렌더·Boolean에서 이상한 결과를 만들어요.
```

**usage_md:**
```
Boolean 결과가 이상할 때, Auto Smooth가 한쪽만 어색할 때, 렌더에 검은 얼룩이 보일 때 가장 먼저 Face Orientation 오버레이를 켜고 확인.
```

**pitfall_md:**
```
빨간 면을 발견하면 `Mesh > Normals > Recalculate Outside` (`Shift+N`)로 일괄 정리. 일부만 뒤집고 싶으면 면 선택 후 `Alt+N > Flip`. **AI로 생성한 메쉬는 Normal이 일관성 없게 들어오는 경우가 많아** 항상 한 번 점검하세요.
```

**steps_json:**
```json
{
  "blender_version": "5.0",
  "platform_note": null,
  "steps": [
    {"n": 1, "action": "Viewport Overlays 메뉴 열기", "hotkey": null, "menu": "뷰포트 우상단 두 원 겹친 아이콘", "screenshot": null, "note": null},
    {"n": 2, "action": "Face Orientation 토글", "hotkey": null, "menu": "Geometry > Face Orientation", "screenshot": null, "note": "파랑=앞, 빨강=뒤"},
    {"n": 3, "action": "Edit Mode에서 일괄 재계산", "hotkey": "Shift + N", "menu": "Mesh > Normals > Recalculate Outside", "screenshot": null, "note": null},
    {"n": 4, "action": "특정 면만 뒤집기", "hotkey": "Alt + N", "menu": "Mesh > Normals > Flip", "screenshot": null, "note": "Flip 선택"}
  ]
}
```

---

### 8. apply-modifier-vs-keep-procedural

| 필드 | 값 |
|---|---|
| `card_id` | `apply-modifier-vs-keep-procedural` |
| `label` | Apply Modifier vs 비파괴 유지 |
| `icon` | archive-restore |
| `category` | `modifier` |
| `week` | `["3", "4"]` |
| `priority` | `P1` |
| `status` | `draft` |
| `blender_version` | `5.0` |
| `official_docs` | https://docs.blender.org/manual/en/latest/modeling/modifiers/introduction.html#applying |

**concept_md:**
```
Modifier는 **투명한 효과 필름**이에요. 값을 바꾸거나 끄거나 지우면 원본 메쉬는 그대로 남아요 — 이게 **비파괴(Non-destructive)**.

**Apply**는 그 필름을 원본에 도장 찍어버리는 작업. 한 번 Apply하면 더 이상 값을 못 바꿔요. 사진 보정에서 RAW를 JPEG으로 굳히는 것과 비슷. 보정 정보가 사라지면 되돌릴 수 없죠.
```

**usage_md:**
```
**보통은 Apply 하지 마세요.** Apply가 필요한 시점은 (1) 다음 Modifier가 Apply된 결과를 입력으로 받아야 할 때, (2) 외부로 export할 때(FBX/GLTF), (3) Edit Mode에서 수동으로 다듬어야 할 때.
```

**pitfall_md:**
```
**Apply Transform (`Ctrl+A`)과 Apply Modifier는 달라요.** Ctrl+A는 Object의 위치/회전/크기를 수치적으로 정리하는 거고, Modifier Apply는 효과를 메쉬에 굳히는 거예요. Modifier Apply는 거의 항상 **맨 마지막에만** 합니다. Mirror를 너무 일찍 Apply하면 좌우 비대칭으로 다듬기 어려워져요.
```

**steps_json:**
```json
{
  "blender_version": "5.0",
  "platform_note": null,
  "steps": [
    {"n": 1, "action": "Modifier 우상단 ▾ 메뉴 열기", "hotkey": null, "menu": "Modifier > ▾", "screenshot": null, "note": null},
    {"n": 2, "action": "Apply 선택", "hotkey": null, "menu": "Apply", "screenshot": null, "note": "되돌리기 어려움"},
    {"n": 3, "action": "Apply 대신 Visibility 토글로 임시 확인", "hotkey": null, "menu": "Modifier 패널 눈/모니터 아이콘", "screenshot": null, "note": "비파괴 유지"},
    {"n": 4, "action": "여러 Modifier 일괄 적용은 Object Convert", "hotkey": null, "menu": "Object > Convert > Mesh", "screenshot": null, "note": "스택 전체를 Mesh로 굳힘"}
  ]
}
```

---

## 검수 후 진행 순서

1. 사용자 OK → Task 2 (Notion push) 진행
2. Task 3 (build) → Task 4 (snapshot + smoke)
3. 모두 통과 → Phase 2 PR 생성 또는 PR #79에 누적

## 미해결 / 확인 요청

- **icon 이름** — Lucide 라이브러리에서 실재하는지 검증 필요 (`folder-tree`, `layers`, `sparkles`, `combine`, `git-merge`, `copy-plus`, `flip-horizontal`, `archive-restore`). 사이트 사용 아이콘 매핑(`assets/icons/` 또는 `_helpers.js`)이 Lucide면 그대로, 다른 라이브러리면 대체 필요.
- **week multi-select 멀티값** — `shade-smooth-auto-smooth`, `merge-by-distance`, `face-orientation-normals` 등이 여러 주차에 노출. 학생 페이지(`week.html`)에서 같은 카드가 중복 노출돼도 OK인지 검토.
- **위젯** — P0 카드 중 `modifier-stack-order`, `shade-smooth-auto-smooth`는 시각 비교 위젯이 효과 큼. 이번 Phase 2에서 같이? 별도 Phase 2.5?
- **steps_json 정확도** — Blender 5.0 메뉴 경로 (예: Object Data Properties의 Normals 위치)는 5.x에서 위치 이동 가능. 한 번 실제 5.0 띄워서 검증 추천.
