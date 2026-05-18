# 리서치 브리프: 아마추어 (Armature)
> 생성일: 2026-05-18 | Blender 5.0 기준

---

## 1. 공식 정의

- **영문**: "An Armature is a type of editable object used to control other objects through a hierarchical system of interconnected bones."
- **한글 풀이**: 아마추어는 뼈(Bone)의 집합으로 이루어진 골격 오브젝트예요. 메시(캐릭터 몸통 등)에 연결해서 뼈를 움직이면 메시가 따라 변형되도록 하는 리깅의 핵심 도구예요. 다른 3D 소프트웨어에서 "Skeleton"이라 부르는 것과 동일한 개념이에요.
- **공식 문서**: [Blender Manual — Armatures](https://docs.blender.org/manual/en/latest/animation/armatures/index.html)

---

## 2. 핵심 파라미터

| 파라미터 | 기본값 | 설명 | 학생에게 중요한 이유 |
|---------|-------|------|-------------------|
| In Front (X-Ray) | Off | 아마추어를 메시 앞에 항상 표시 | 메시 안에 뼈가 묻혀 선택이 안 될 때 켜면 해결됨 |
| Show Names | Off | 각 본 이름을 뷰포트에 표시 | 뼈가 많아지면 이름 없이는 선택 불가능 |
| Show Axes | Off | 각 본의 로컬 축(X/Y/Z) 시각화 | Roll 값 확인 및 IK 문제 진단에 필수 |
| Bone Connected | True (부모 연결 시) | 자식 본의 Head를 부모 Tail에 고정 | 끄면 자식 본이 독립 이동 가능, 척추·팔 구조 설계 시 자주 조절 |
| Bone Roll | 0° | 본의 Y축(길이 방향) 기준 회전각 | 잘못된 Roll은 회전 방향이 반대로 나오는 주요 원인 |
| Bone Head / Tail | 3D 좌표 | 본의 시작점(굵은 쪽) / 끝점(얇은 쪽) | 관절 위치 정밀도가 변형 품질을 결정 |
| Deform | True | 이 본이 메시를 실제로 변형하는지 여부 | 컨트롤 전용 본(IK Target 등)은 반드시 Off |

---

## 3. 단축키

| 키 | 동작 | 컨텍스트 | 비고 |
|----|------|---------|------|
| Shift + A | 아마추어 / 단일 본 추가 | Object Mode / Edit Mode | Object Mode에서는 새 Armature 오브젝트, Edit Mode에서는 기존 아마추어에 본 추가 |
| Tab | Object Mode ↔ Edit Mode 전환 | 아마추어 선택 상태 | Armature 선택 시 Tab은 Object/Edit 전환 |
| Ctrl + Tab | 모드 파이 메뉴 | 아마추어 선택 상태 | Object / Edit / Pose Mode 선택 가능 |
| E | 본 Extrude (연결 생성) | Edit Mode | 선택한 Tail에서 연결된 자식 본 생성 |
| Shift + D | 본 복제 | Edit Mode | 비연결 복사본 생성 |
| Ctrl + P | 부모 설정 | Edit Mode (본 간) / Object Mode (메시-아마추어) | Object Mode에서 메시 → Armature 순 선택 후 실행 |
| Alt + P | 부모 해제 | Edit Mode / Object Mode | — |
| G | 이동 | Edit Mode / Pose Mode | — |
| R | 회전 | Edit Mode / Pose Mode | — |
| Alt + R | 회전 초기화 | Pose Mode | 포즈 리셋 시 사용 |
| Alt + G | 위치 초기화 | Pose Mode | 포즈 리셋 시 사용 |
| Ctrl + N | Roll 재계산 | Edit Mode | 본 선택 후 실행, 로컬 축 정렬 문제 해결 |

---

## 4. 연관 개념 그래프

### 선수 지식 (이걸 모르면 이해 불가)

- **Object Mode / Edit Mode**: 아마추어도 일반 오브젝트와 동일하게 모드가 나뉘어요. 모드 개념 없이는 왜 뼈가 안 움직이는지 이해할 수 없어요.
- **오브젝트 원점(Origin)**: 아마추어 전체를 이동·회전할 때의 기준점이에요. 메시와 아마추어의 원점이 어긋나면 변형이 틀어져요.
- **부모-자식 관계(Parenting)**: 뼈의 계층 구조와 메시-아마추어 연결 모두 Parent 개념으로 작동해요.
- **로컬 좌표계**: 본은 각자 자신만의 로컬 X/Y/Z 축을 가져요. Y축이 항상 본의 길이 방향(Head → Tail)이에요.

### 연결 개념 (함께 쓰이는 것)

- **Weight Painting**: 메시의 각 버텍스가 어느 뼈에 얼마나 영향을 받는지 칠하는 작업이에요. 아마추어 없이는 웨이트 페인팅 자체가 의미 없어요.
- **Pose Mode**: 아마추어 Edit Mode에서 구조를 잡고, Pose Mode에서 실제로 포즈를 잡아요. 두 모드를 번갈아 쓰는 게 기본 워크플로예요.
- **Armature Modifier**: 메시 오브젝트에 추가되어 아마추어와 메시를 실제로 연결하는 모디파이어예요. Ctrl+P로 부모 설정 시 자동 추가돼요.
- **Vertex Group**: 메시 내 버텍스의 집합이에요. 각 뼈 이름과 동일한 버텍스 그룹이 자동 생성되고, 이 그룹이 웨이트 정보를 저장해요.

### 심화 (알면 이해가 깊어지는 것)

- **IK (Inverse Kinematics)**: 기본 계층 구조는 부모가 자식을 끌어요(FK). IK는 반대로 끝 뼈의 위치를 지정하면 위쪽 체인이 자동 계산돼요. 팔다리 리깅 시 IK/FK 전환이 핵심이에요.
- **Bone Roll**: 본의 길이 축(Y) 기준 회전값이에요. 같은 Head/Tail 위치라도 Roll에 따라 로컬 X/Z 방향이 달라져서, 미러 리깅이나 IK 방향이 뒤집힐 수 있어요.
- **Rest Pose / Bind Pose**: 아마추어를 메시에 연결하는 순간의 포즈가 Rest Pose예요. 이후 모든 변형은 Rest Pose를 기준으로 계산돼요.

---

## 5. 학생 혼란 포인트

| # | 질문 (실제) | 출처 | 핵심 원인 | 검증된 답변 |
|---|-----------|------|----------|-----------|
| 1 | "Edit Mode에서 뼈를 수정했는데 Pose Mode로 가면 원래대로 돌아가요" | CGCookie Community, Quora | Edit Mode 변경과 Pose Mode 포즈를 혼동함. Edit Mode는 구조(Rest Pose), Pose Mode는 애니메이션용 변형 | Edit Mode 변경은 구조 변경이에요. Pose Mode에서 보이는 건 포즈로 인한 변형이고, Rest Pose 자체는 변한 게 맞아요. Ctrl+A로 적용하거나 Pose → Apply Pose as Rest Pose로 동기화하세요. |
| 2 | "Tab을 눌러도 Pose Mode가 안 열려요" | CGCookie Noob Q&A | Tab이 Object↔Edit 전환이라 Pose Mode 진입 방법을 모름 | Ctrl+Tab으로 파이 메뉴를 열고 Pose Mode를 선택하거나, 헤더의 모드 드롭다운에서 직접 선택하세요. |
| 3 | "메시를 선택하고 뼈를 붙였는데 움직여도 메시가 안 따라와요" | Blender Artists, 한국어 커뮤니티 블로그 | 선택 순서 오류 (Armature가 Active여야 함) 또는 Armature Modifier가 없음 | 메시 먼저, Armature 나중에 Shift+클릭(Armature가 Active 오브젝트)한 뒤 Ctrl+P → With Automatic Weights를 선택하세요. |
| 4 | "Automatic Weights가 이상해요. 팔을 올리면 몸통도 같이 늘어나요" | Blender Artists, 3DModels.org | 버텍스 밀도가 너무 높거나 낮아서 자동 가중치 계산 실패 | 웨이트 페인팅으로 해당 본의 영향 범위를 수동 수정하세요. 또는 메시를 임시로 스케일업 후 연결하면 자동 가중치 품질이 나아지는 경우도 있어요. |
| 5 | "오른쪽 팔 뼈와 왼쪽 팔 뼈 Roll 값이 달라서 미러 애니메이션이 이상해요" | BlenderArtists (Bone Roll 스레드), CGCookie | 본을 수동 추가할 때 Roll 정렬을 안 함 | Edit Mode에서 양쪽 본 선택 후 Ctrl+N → Recalculate Roll로 정렬하거나, 한쪽 본을 완성 후 Mirror 기능으로 대칭 복사하세요. |
| 6 | "Weight Paint 모드에서 뼈를 클릭할 수가 없어요" | Blender Developer Forum, CyPaint 블로그 | Weight Paint 모드에서 본 선택은 일반 클릭이 아닌 Ctrl+클릭 | Weight Paint Mode 진입 후 뼈는 Ctrl+좌클릭으로 선택해요. Pose Mode로 먼저 돌아가서 포즈를 잡은 뒤 Weight Paint Mode로 오는 게 권장 워크플로예요. |

---

## 6. 흔한 실수 & 해결

| 증상 | 원인 | 해결 |
|------|------|------|
| 뼈가 메시 안에 가려져서 선택이 안 됨 | 아마추어 In Front(X-Ray) 옵션 비활성화 | Properties → Object Data (아마추어 선택) → Viewport Display → In Front 체크 |
| Pose Mode에서 뼈를 움직여도 메시 변형 없음 | 메시에 Armature Modifier가 없거나 Object 슬롯이 비어 있음 | 메시 선택 → Properties → Modifier → Armature Modifier의 Object 필드에 아마추어 오브젝트 지정 |
| 오브젝트 변형 후 리깅 시 뼈 위치가 어긋남 | 메시나 아마추어에 미적용(unapplied) Scale/Rotation 존재 | 리깅 전 Ctrl+A → Apply All Transforms 실행 |
| Copy/Paste로 뼈가 복사 안 됨 | 뼈는 일반 오브젝트와 달리 Ctrl+C/V 미지원 | Edit Mode에서 Shift+D로 복제 |
| Deform 본이 아닌 컨트롤 본도 메시 변형에 영향 줌 | 컨트롤 본의 Deform 옵션이 켜져 있음 | 해당 본 선택 → Bone Properties → Deform 체크 해제 |
| 본 이름이 없어 선택 불가 | Show Names 비활성화 | Properties → Object Data → Viewport Display → Names 체크 |
| Automatic Weights 파란 화면(버텍스 누락) | 메시 버텍스 일부가 어떤 본 영향권에도 없음 | Weight Paint로 누락 버텍스 수동 배정, 또는 메시 구조 재검토 |

---

## 7. 추천 비유 후보

1. **인형극 줄 구조** — 인형 팔다리에 줄(뼈)을 달고 줄을 당기면(Pose Mode 조작) 인형(메시)이 따라 움직이는 구조와 동일해요. Edit Mode가 줄을 다는 위치를 정하는 단계, Pose Mode가 실제로 줄을 당기는 단계예요.
2. **팔 골격과 피부** — 실제 사람 팔이 움직일 때 뼈(아마추어)가 먼저 회전하고 그 위에 근육과 피부(메시)가 따라 변형되는 원리와 같아요. Weight Painting은 "이 피부 부위는 어느 뼈에 얼마나 잡아당겨지는지" 지정하는 것이에요.
3. **레이어드 조명 리그(촬영 경험자 대상)** — 조명 붐 암처럼 Root 본에서 출발해 계층적으로 뻗어나가는 구조예요. 붐 전체(Root)를 움직이면 모든 하위 조명이 따라가고, 개별 조명(말단 본)만 독립 조정도 가능해요.

---

## 8. 크로스체크 로그

| 주장 | 소스 | 검증 | 결과 |
|------|------|------|------|
| "Tab = Pose Mode 진입" | 일부 블로그·튜토리얼 | Blender 5.x 공식 모드 문서, katsbits.com | 불일치. Tab은 Object↔Edit 전환이에요. Pose Mode는 Ctrl+Tab 파이 메뉴 또는 헤더 드롭다운으로 진입해요. |
| "본의 Y축은 항상 길이 방향(Head→Tail)" | katsbits.com, artisticrender.com | Blender API 문서 (info_gotchas_armatures_and_bones) | 일치. Y축이 Roll 축이고 Head에서 Tail 방향이 Y+ 방향이에요. |
| "Ctrl+P → With Automatic Weights는 메시 먼저, 아마추어 나중에 선택" | velog 블로그, artisticrender.com | CGCookie 커뮤니티, Blender 공식 Ctrl+P 동작 설명 | 일치. 마지막으로 선택된 오브젝트(Active)가 아마추어여야 해요. |
| "Copy/Paste로 본 복사 가능" | 일부 포럼 댓글 | katsbits.com 명시("Copy/Paste doesn't work on bones") | 불일치. Edit Mode에서 Shift+D 복제를 사용해야 해요. |
| "Automatic Weights는 항상 완벽하게 작동" | 일부 초보자 인식 | 3DModels.org, BlenderArtists 다수 스레드 | 불일치. 메시 밀도나 구조에 따라 누락·오배정이 발생하며, 수동 웨이트 페인팅 후처리가 필요해요. |

---

**참고 출처**

- [Armature & Bone Basics — katsbits.com](https://www.katsbits.com/codex/armature-bone/)
- [How to Work with Armatures — artisticrender.com](https://artisticrender.com/how-to-work-with-armatures-in-blender/)
- [Blender Python API — Bones & Armatures Gotchas](https://docs.blender.org/api/current/info_gotchas_armatures_and_bones.html)
- [Blender 5.1 Manual — Posing Introduction](https://docs.blender.org/manual/en/latest/animation/armatures/posing/editing/introduction.html)
- [Blender 리깅과 애니메이션 — velog](https://velog.io/@eogh773/Blender-%EB%A6%AC%EA%B9%85%EA%B3%BC-%EC%95%A0%EB%8B%88%EB%A9%94%EC%9D%B4%EC%85%98)
- [Mastering Blender: Switch Between Weight Paint and Pose Modes — CyPaint](https://cypaint.com/article/how-to-switch-between-wieght-paint-and-pose)
- [Automatic Weights in Blender — 3DModels.org](https://3dmodels.org/blog/automatic-weights-in-blender/)
